"""Shared UI utilities for phase handlers.

Provides: lookup, state_badges_html, wound_adjustment_buttons,
          render_player_column, render_group_cards, render_group_assignment,
          render_attack_resolution, PHASE_RULES.

Handlers import from here — never from gameActionsArea — to avoid circular imports.
"""

from __future__ import annotations

from collections.abc import Callable

import streamlit as st

from gameMechanic.attack_math import (  # noqa: F401
    _compute_attacks,
    _detect_weapon_special,
    _group_melee_budget,
    _parse_strength,
    _restriction_label,
    _total_attacks_int,
)
from gameMechanic.game_state import PHASES, units_key_for, units_list_for
from gameMechanic.unit_mutations import apply_damage, heal_unit
from gameObjects.unit import Unit
from gameObjects.weapon import WeaponProfile
from uiLayout.dice_html import (  # noqa: F401
    _render_dice_roll_block,
    _render_dice_save_block,
    _render_dice_wound_block,
    block_divider_html,
    dice_face_svg,
    dice_row_html,
    grid_row_html,
    modifier_die_pair_html,
    save_modifier_die_pair_html,
    special_die_html,
    threshold_header_html,
)

# ---------------------------------------------------------------------------
# Phase description texts
# ---------------------------------------------------------------------------

PHASE_RULES: dict[str, str] = {
    "command": (
        "**Command Phase**\n\n"
        "The active player receives **+1 CP** (Battle-forged armies). "
        "Activate abilities and stratagems that trigger in the Command Phase."
    ),
    "movement": (
        "**Movement Phase**\n\n"
        "Select a unit and choose its movement type:\n"
        '- **Normal** — move up to M"\n'
        '- **Advance** — move up to M"+D6", cannot shoot or charge afterwards\n'
        "- **Stationary** — do not move\n"
        '- **Retreat** — only if in melee; move up to M", cannot shoot or charge afterwards'
    ),
    "psychic": (
        "**Psychic Phase**\n\n"
        "PSYKER units attempt to manifest psychic powers. "
        "Roll **2D6** ≥ Warp Charge value to manifest. "
        "Opponent may attempt to deny with their own PSYKER (2D6 > manifesting roll)."
    ),
    "shooting": (
        "**Shooting Phase**\n\n"
        "Select a unit to shoot, then select a target. "
        "Units that Advanced or Retreated cannot shoot. "
        "Units in melee cannot shoot.\n\n"
        "Attack sequence: **Hit** (BS) → **Wound** (S vs T) → **Save** (Sv−AP) → **Damage**"
    ),
    "charge": (
        "**Charge Phase**\n\n"
        'Eligible units (≤ 12" from enemy, did not Advance or Retreat) may declare a charge. '
        "Roll **2D6** — result must be ≥ distance to closest target model. "
        "On success: move into melee range."
    ),
    "fight": (
        "**Fight Phase**\n\n"
        "Starting with the **non-active player**, both sides alternate selecting eligible units. "
        "Units that charged this turn fight **before** other units. "
        'Each unit: **Pile In** (up to 3") → **Melee attacks** → **Consolidate** (up to 3").'
    ),
    "morale": (
        "**Morale Phase**\n\n"
        "Units that suffered model losses this turn must take a morale test: "
        "Roll **D6** + models lost. If result > Leadership: additional models flee (result − Ld).\n\n"
        "Single-model units auto-pass."
    ),
}

# ---------------------------------------------------------------------------
# Badge rendering
# ---------------------------------------------------------------------------

_BADGE_COLORS: dict[str, tuple[str, str]] = {
    "MOVED": ("#4a9a5a", "#0a1a0a"),
    "STATIONARY": ("#6b5f44", "#1c1a14"),
    "ADVANCED": ("#d4a017", "#2e2618"),
    "RETREATED": ("#c04040", "#1e1010"),
    "IN MELEE": ("#e07050", "#2a1810"),
    "CHARGED": ("#b070d8", "#1a0a2a"),
    "FOUGHT": ("#c080e8", "#200a30"),
    "SHOT": ("#40a0b8", "#081418"),
    "CAST": ("#9060d0", "#180a28"),
    "RESERVE": ("#4090b0", "#101820"),
    "DESTROYED": ("#c04040", "#1e1010"),
}

_BUFF_COLOR: tuple[str, str] = ("#60a5fa", "#0a1020")
_DEBUFF_COLOR: tuple[str, str] = ("#ef4444", "#1e0808")

_MOVEMENT_BADGE: dict[str, str] = {
    "moved": "MOVED",
    "stationary": "STATIONARY",
    "advanced": "ADVANCED",
    "retreated": "RETREATED",
}


def _badge(text: str, variant: str = "") -> str:
    if text in _BADGE_COLORS:
        fg, bg = _BADGE_COLORS[text]
    elif variant == "buff":
        fg, bg = _BUFF_COLOR
    elif variant == "debuff":
        fg, bg = _DEBUFF_COLOR
    else:
        fg, bg = ("#c9a84c", "#2e2618")
    return (
        f'<span style="background:{bg};border:1px solid {fg};border-radius:2px;'
        f"padding:1px 6px;font-size:10px;color:{fg};letter-spacing:0.06em;"
        f'font-weight:600;margin-right:3px;">{text}</span>'
    )


def state_badges_html(unit_state: dict) -> str:  # type: ignore[type-arg]
    """Generate HTML state badges from movement_choice, turn_flags and active_buffs."""
    parts: list[str] = []
    flags = unit_state.get("turn_flags", {})
    mc = unit_state.get("movement_choice")

    # Movement slot: FOUGHT > CHARGED > movement_choice (suppressed when in_reserve)
    if flags.get("fought"):
        movement_slot = "FOUGHT"
    elif flags.get("charged"):
        movement_slot = "CHARGED"
    elif mc in _MOVEMENT_BADGE and not unit_state.get("in_reserve"):
        movement_slot = _MOVEMENT_BADGE[mc]
    else:
        movement_slot = None

    if movement_slot:
        parts.append(_badge(movement_slot))

    # SHOT and CAST are always additive alongside the movement slot
    if flags.get("shot"):
        parts.append(_badge("SHOT"))
    if flags.get("cast"):
        parts.append(_badge("CAST"))

    # IN MELEE: always visible except when CHARGED is the active movement slot
    if unit_state.get("in_melee") and movement_slot != "CHARGED":
        parts.append(_badge("IN MELEE"))

    if unit_state.get("in_reserve"):
        parts.append(_badge("RESERVE"))

    for buf in unit_state.get("active_buffs", []):
        parts.append(_badge(buf.get("badge_label", "BUFF"), variant="buff"))

    return "".join(parts)


# ---------------------------------------------------------------------------
# Unit lookup
# ---------------------------------------------------------------------------


def lookup(faction: str, uid: str) -> tuple[Unit, dict]:  # type: ignore[type-arg]
    """Return (Unit, unit_state_dict) for the given faction + state_key (uid).

    uid may be a bare unit ID or a deduplicated state key ('unit.id#N').
    """
    from gameMechanic.game_state import unit_id_from_state_key

    unit_id = unit_id_from_state_key(uid)
    units = units_list_for(faction)
    unit = next((u for u in units if u.id == unit_id), None)
    if unit is None:
        raise KeyError(
            f"No unit with id {unit_id!r} in catalog for faction {faction!r} "
            f"(state key {uid!r}). Session state and unit catalog are out of sync."
        )
    return unit, st.session_state[units_key_for(faction)][uid]


# ---------------------------------------------------------------------------
# Wound / heal buttons
# ---------------------------------------------------------------------------


def wound_adjustment_buttons(faction: str, uid: str, unit: Unit) -> None:
    """Render ±1/2/3 wound-adjustment buttons for a unit."""
    bc = st.columns(6)
    for col, delta, label in zip(bc, [-3, -2, -1, 1, 2, 3], ["−3", "−2", "−1", "+1", "+2", "+3"]):
        with col:
            is_mortal = delta == -1
            if st.button(
                label,
                key=f"w{delta}_{faction}_{uid}",
                type="primary" if is_mortal else "secondary",
            ):
                if delta < 0:
                    apply_damage(uid, faction, -delta, unit, mortal=is_mortal)
                else:
                    heal_unit(uid, faction, delta, unit)
                st.rerun()


# ---------------------------------------------------------------------------
# Melee engagement display
# ---------------------------------------------------------------------------


def render_melee_engagements(faction: str, uid: str, unit_state: dict) -> None:  # type: ignore[type-arg]
    """Show the list of enemy units this unit is engaged with, each with a Break button."""
    from gameMechanic.unit_mutations import leave_melee_pair

    melee_with: list[list[str]] = unit_state.get("melee_with", [])
    if not unit_state.get("in_melee") or not melee_with:
        return

    p1 = st.session_state.get("first_player", "")
    p2 = st.session_state.get("second_player", "")
    units_by_faction = {
        p1: {u.id: u for u in units_list_for(p1)},
        p2: {u.id: u for u in units_list_for(p2)},
    }

    st.markdown("**⚔ Engaged with:**")
    for i, (enemy_fac, enemy_uid) in enumerate(list(melee_with)):
        enemy_unit = units_by_faction.get(enemy_fac, {}).get(enemy_uid)
        name = enemy_unit.name_en if enemy_unit else enemy_uid
        cols = st.columns([4, 1])
        cols[0].markdown(f"- {name}")
        if cols[1].button("Break ✕", key=f"break_{faction}_{uid}_{enemy_fac}_{enemy_uid}_{i}"):
            leave_melee_pair(uid, faction, enemy_uid, enemy_fac)
            st.rerun()


# ---------------------------------------------------------------------------
# Standard player-column renderer (shared by all handlers)
# ---------------------------------------------------------------------------


def render_player_column(
    faction: str,
    state: dict,  # type: ignore[type-arg]
    *,
    active_content: Callable[[str, str, Unit, dict, dict], None],
    inactive_content: Callable[[str, str, Unit, dict], None] | None = None,
    no_target_caption: str = "—",
    inactive_override: Callable[[], None] | None = None,
    show_wound_buttons: bool = True,
) -> None:
    """Render one player column (active or inactive).

    active_content(faction, uid, unit, unit_state, state) — called when a unit is
    selected for the active player; renders phase-specific actions.

    inactive_content(faction, uid, unit, unit_state) — called when the inactive
    player has a target selected from their army; renders target stats etc.
    If None, only wound adjustment buttons are shown for selected targets.

    no_target_caption — shown to the inactive player when the active player has a
    unit selected but no target from this faction is designated.

    inactive_override — replaces the whole inactive branch when set (used by the
    model-group flow to render the group attack assignment panel).

    show_wound_buttons — set False in phases where targets take no damage
    (e.g. charge declaration) to hide the manual wound adjustment buttons.
    """
    is_active = faction == state["active"]
    indicator = "▶" if is_active else "◀"
    st.markdown(f"**{indicator} {faction}**")

    if is_active:
        sel = st.session_state.selected_unit
        if sel and sel[0] == faction:
            _, uid = sel
            unit, unit_state = lookup(faction, uid)
            badges = state_badges_html(unit_state)
            st.markdown(f"*{unit.name_en}*")
            if badges:
                st.markdown(badges, unsafe_allow_html=True)
            active_content(faction, uid, unit, unit_state, state)
        else:
            st.caption("← Select a unit from your army list.")

    elif inactive_override is not None:
        inactive_override()

    else:
        targets: list[tuple[str, str]] = st.session_state.selected_targets
        matching = [t for t in targets if t[0] == faction]
        if matching:
            for tgt in matching:
                _, uid = tgt
                unit, unit_state = lookup(faction, uid)
                badges = state_badges_html(unit_state)
                st.markdown(f"*{unit.name_en}* ← Target")
                if badges:
                    st.markdown(badges, unsafe_allow_html=True)
                if inactive_content is not None:
                    inactive_content(faction, uid, unit, unit_state)
                if show_wound_buttons:
                    st.divider()
                    wound_adjustment_buttons(faction, uid, unit)
        elif st.session_state.get("selected_unit"):
            st.caption(no_target_caption)
        else:
            st.caption("—")


# ---------------------------------------------------------------------------
# 6d-v2 Attack sequence — shared utilities
# ---------------------------------------------------------------------------


def _empty_attack_declaration() -> dict:  # type: ignore[type-arg]
    return {
        "active": False,
        "atk_faction": "",
        "atk_uid": "",
        "phase_key": "",
        "use_melee": False,
        "in_melee": False,
        "entries": [],
    }


def _next_declaration_seq() -> int:
    """Monotonic counter namespacing per-resolution widget keys.

    Without it, res_/rp_ keys from an earlier resolution of the same unit and
    target survive in session_state and the new tabs start as already applied.
    """
    seq = st.session_state.get("attack_decl_seq", 0) + 1
    st.session_state.attack_decl_seq = seq
    return seq


def _protocol_source_label(faction_dir: str) -> str:
    from gameObjects.loader import load_round_choice_abilities  # noqa: PLC0415

    protocol_id = st.session_state.get(f"protocol_active_{faction_dir}")
    directive = st.session_state.get(f"protocol_directive_{faction_dir}")
    if not protocol_id or not directive or not faction_dir:
        return "Protocol"
    protocols = load_round_choice_abilities(faction_dir)
    p = next((proto for proto in protocols if proto.id == protocol_id), None)
    return f"{p.name_en} ({directive.capitalize()})" if p else "Protocol"


def _collect_atk_modifiers(
    atk_faction: str,
    atk_state: dict,  # type: ignore[type-arg]
    phase_key: str,
    use_melee: bool,
) -> list[dict]:  # type: ignore[type-arg]
    """Collect hit/wound modifiers for the attacker from protocols, buffs, and active_modifiers."""
    from gameMechanic.ability_engine import get_active_protocol_modifier  # noqa: PLC0415
    from gameMechanic.game_state import faction_dir_for  # noqa: PLC0415

    mods: list[dict] = []  # type: ignore[type-arg]
    try:
        fdir = faction_dir_for(atk_faction)
        proto = get_active_protocol_modifier(fdir, phase_key, use_melee)
        label = _protocol_source_label(fdir)
        if proto.get("hit"):
            mods.append(
                {"label": label, "value": proto["hit"], "roll_type": "hit", "source": "protocol"}
            )
        if proto.get("wound"):
            mods.append(
                {
                    "label": label,
                    "value": proto["wound"],
                    "roll_type": "wound",
                    "source": "protocol",
                }
            )
    except KeyError:
        pass
    for b in atk_state.get("active_buffs", []):
        if b.get("effect_type") == "buff_roll":
            mods.append(
                {
                    "label": b.get("badge_label", "Buff"),
                    "value": 1,
                    "roll_type": "hit",
                    "source": "buff",
                }
            )
    for m in st.session_state.get("active_modifiers", []):
        eff = m.get("effect", {})
        rt = eff.get("roll_type")
        tgt = eff.get("target", "attacker")
        if rt in ("hit", "wound") and tgt in ("attacker", "any"):
            mods.append(
                {
                    "label": m.get("source", "Modifier"),
                    "value": eff.get("value", 0),
                    "roll_type": rt,
                    "source": "stratagem",
                }
            )
    return mods


def _collect_def_save_modifiers(
    def_faction: str,
    phase_key: str,
    use_melee: bool,
) -> list[dict]:  # type: ignore[type-arg]
    """Collect save modifiers for the defender from protocols and active_modifiers."""
    from gameMechanic.ability_engine import get_active_protocol_modifier  # noqa: PLC0415
    from gameMechanic.game_state import faction_dir_for  # noqa: PLC0415

    mods: list[dict] = []  # type: ignore[type-arg]
    try:
        fdir = faction_dir_for(def_faction)
        proto = get_active_protocol_modifier(fdir, phase_key, use_melee)
        if proto.get("save"):
            label = _protocol_source_label(fdir)
            mods.append({"label": f"{label} (defender)", "value": proto["save"]})
    except KeyError:
        pass
    for m in st.session_state.get("active_modifiers", []):
        eff = m.get("effect", {})
        if eff.get("roll_type") == "save" and eff.get("target") in ("defender", "any"):
            mods.append({"label": m.get("source", "Modifier"), "value": eff.get("value", 0)})
    return mods


# ---------------------------------------------------------------------------
# 6d-v2 Damage + RP blocks
# ---------------------------------------------------------------------------


def _render_rp_block(
    def_unit: Unit,
    def_faction: str,
    def_uid: str,
    models_lost: int,
    tab_key: str,
) -> None:
    """Render Reanimation Protocols block after damage if the unit has the keyword."""
    from gameMechanic.unit_mutations import heal_unit  # noqa: PLC0415

    if models_lost <= 0:
        return
    if "reanimationProtocols" not in def_unit.rules:
        return

    rp_key = f"rp_{tab_key}"
    rp_state = st.session_state.get(rp_key, {})
    if rp_state.get("applied"):
        mb = rp_state.get("models_back", 0)
        if mb > 0:
            st.caption(f"RP: {mb} models returned ✓")
        return

    rp_dice = models_lost * def_unit.wounds
    st.markdown(
        f"**REANIMATION PROTOCOLS** &nbsp; "
        f"{models_lost} × {def_unit.name_en} gefallen → **{rp_dice} Würfel** · Erfolg: 5+"
    )
    # Half-width block — keep the RP entry compact
    rp_col, _ = st.columns(2)
    models_back = rp_col.number_input(
        "Modelle zurück",
        min_value=0,
        max_value=models_lost,
        step=1,
        key=f"rp_mb_{tab_key}",
    )
    c1, c2 = rp_col.columns(2)
    if c1.button("RP anwenden", key=f"rp_apply_{tab_key}", type="primary"):
        if int(models_back) > 0:
            heal_unit(def_uid, def_faction, int(models_back) * def_unit.wounds, def_unit)
        st.session_state[rp_key] = {"applied": True, "models_back": int(models_back)}
        st.rerun()
    if c2.button("Überspringen", key=f"rp_skip_{tab_key}"):
        st.session_state[rp_key] = {"applied": True, "models_back": 0}
        st.rerun()


def _render_damage_block(
    def_unit: Unit,
    def_faction: str,
    def_uid: str,
    profile,
    atk_unit_name: str,
    phase_key: str,
    tab_key: str,
) -> None:
    """Render damage input, apply button, post-apply summary, and RP block."""
    from gameMechanic.combat import apply_damage_attacks  # noqa: PLC0415
    from gameMechanic.game_log import log_action  # noqa: PLC0415
    from gameMechanic.game_state import units_key_for  # noqa: PLC0415
    from gameMechanic.unit_mutations import apply_damage  # noqa: PLC0415

    res_key = f"res_{tab_key}"
    tab_state = st.session_state.get(res_key, {})

    if tab_state.get("applied"):
        m_lost = tab_state.get("models_lost", 0)
        mw = tab_state.get("mortal_wounds", 0)
        total = tab_state.get("total_damage", 0)
        st.success(f"✓ {m_lost} models · {mw} MW · {total} damage applied")
        _render_rp_block(def_unit, def_faction, def_uid, m_lost, tab_key)
        if st.button("↺ Reset", key=f"res_reset_{tab_key}"):
            for k in (res_key, f"rp_{tab_key}"):
                st.session_state.pop(k, None)
            st.rerun()
        return

    st.markdown("**DAMAGE**")
    is_multi_lp = def_unit.wounds > 1
    is_single_model = def_unit.models_max <= 1
    dmg_str = str(profile.damage)
    dmg_label = f"D{dmg_str}" if not dmg_str.lstrip("+-").isdigit() else f"{dmg_str} fixed"
    st.markdown(
        f'<span style="font-size:1.05rem;font-weight:700;color:#fbbf24;">{dmg_label}</span> '
        f"per failed save · Target: "
        f'<span style="font-size:1.05rem;font-weight:700;color:#fbbf24;">'
        f"{def_unit.wounds} HP/model</span>",
        unsafe_allow_html=True,
    )

    # Half-width block — the damage entry does not need the whole displayArea
    dmg_col, _ = st.columns(2)

    models_lost = 0
    if not is_single_model:
        models_lost = dmg_col.number_input(
            "Models lost",
            min_value=0,
            step=1,
            key=f"ml_{tab_key}",
        )

    wounds_on_front = 0
    if is_multi_lp:
        wf_label = (
            f"Wounds taken (0–{def_unit.wounds - 1})"
            if is_single_model
            else f"Wounds on front model (0–{def_unit.wounds - 1})"
        )
        wounds_on_front = dmg_col.number_input(
            wf_label,
            min_value=0,
            max_value=def_unit.wounds - 1,
            step=1,
            key=f"wf_{tab_key}",
        )

    weapon_special = _detect_weapon_special(profile)
    mortal_wounds = 0
    if weapon_special.get("has_mortal_wounds"):
        mortal_wounds = dmg_col.number_input(
            "Mortal Wounds",
            min_value=0,
            step=1,
            key=f"mw_{tab_key}",
        )

    total = apply_damage_attacks(
        int(models_lost), int(wounds_on_front), int(mortal_wounds), def_unit.wounds
    )
    btn_label = f"⚔ Apply {total} Damage → {def_unit.name_en}" if total > 0 else "Apply Damage"
    if dmg_col.button(btn_label, key=f"apply_{tab_key}", type="primary", use_container_width=True):
        if total > 0:
            apply_damage(def_uid, def_faction, total, def_unit, resolved=True)
        decl = st.session_state.get("attack_declaration", {})
        atk_uid = decl.get("atk_uid", "")
        atk_f = decl.get("atk_faction", "")
        if atk_uid and atk_f:
            atk_flags = (
                st.session_state[units_key_for(atk_f)].get(atk_uid, {}).get("turn_flags", {})
            )
            if phase_key == "shooting":
                atk_flags["shot"] = True
            elif phase_key == "fight":
                atk_flags["fought"] = True
                try:
                    atk_unit, _ = lookup(atk_f, atk_uid)
                    if atk_unit.get_triggered_effect("after_fight", "fight", "mortal_after_melee"):
                        st.session_state.pending_irongob = {
                            "uid": atk_uid,
                            "faction": atk_f,
                            "step": "initial",
                            "target_uid": None,
                            "target_faction": None,
                            "mortals": 0,
                        }
                except (StopIteration, KeyError):
                    pass
        log_action(
            st.session_state.round,
            phase_key,
            atk_unit_name,
            f"dealt {total} damage to {def_unit.name_en}",
        )
        st.session_state[res_key] = {
            "applied": True,
            "models_lost": int(models_lost),
            "wounds_on_front": int(wounds_on_front),
            "mortal_wounds": int(mortal_wounds),
            "total_damage": total,
        }
        st.rerun()


# ---------------------------------------------------------------------------
# 6d-v2 Resolution tab
# ---------------------------------------------------------------------------


def _render_resolution_tab(
    entry: dict,  # type: ignore[type-arg]
    atk_faction: str,
    atk_unit: Unit,
    atk_state: dict,  # type: ignore[type-arg]
    use_melee: bool,
    phase_key: str,
    tab_key: str,
) -> None:
    """Render one resolution tab: Hit + Wound table + Save + Cover + Damage."""
    from gameMechanic.combat import (  # noqa: PLC0415
        resolve_attack_modifiers,
        resolve_fnp,
        resolve_save,
    )
    from gameObjects.loader import resolve_bracket_stats  # noqa: PLC0415

    def_faction = entry["def_faction"]
    def_uid = entry["def_uid"]
    weapon_name = entry["weapon_name"]
    profile_idx = entry["profile_idx"]
    models_count = entry["models_count"]
    # Per-group stat overrides carried from the declaration (Boss Nob etc.);
    # fall back to the unit-level stats for homogeneous groups.
    grp_strength = entry.get("atk_strength", atk_unit.strength)
    grp_attacks = entry.get("atk_attacks", atk_unit.attacks)
    grp_ws = entry.get("atk_ws")
    grp_bs = entry.get("atk_bs")

    def_unit, def_state = lookup(def_faction, def_uid)

    # Resolve weapon + profile
    in_melee_flag = st.session_state.get("attack_declaration", {}).get("in_melee", False)
    if use_melee:
        weapons = [w for w in atk_unit.weapons if any(p.is_melee for p in w.profiles)]
    elif in_melee_flag:
        weapons = [
            w
            for w in atk_unit.weapons
            if any(not p.is_melee and p.weapon_type.startswith("Pistol") for p in w.profiles)
        ]
    else:
        weapons = [w for w in atk_unit.weapons if any(not p.is_melee for p in w.profiles)]

    weapon = next((w for w in weapons if w.name_en == weapon_name), weapons[0] if weapons else None)
    if weapon is None:
        st.error("Weapon not found.")
        return
    profiles = [p for p in weapon.profiles if p.is_melee == use_melee]
    if not profiles:
        profiles = weapon.profiles
    profile = profiles[min(profile_idx, len(profiles) - 1)]

    from gameMechanic.ability_engine import (  # noqa: PLC0415
        ability_invuln_save,
        buff_stat_bonus,
    )

    str_bonus = buff_stat_bonus(atk_faction, atk_unit, "strength")
    # str_bonus is added after weapon-strength calculation so that ×N weapons
    # give (User×N) + bonus rather than (User + bonus)×N. Base strength is the
    # group's value (e.g. Boss Nob S 5), not the unit-level S.
    strength = _parse_strength(profile.strength, grp_strength) + str_bonus
    ap = profile.ap
    skill_label = "WS" if use_melee else "BS"
    advanced = atk_state.get("turn_flags", {}).get("advanced", False)

    per_model_hp = atk_state.get("current_wounds", atk_unit.wounds) // max(
        1, atk_state.get("models", atk_unit.models_max)
    )
    live = resolve_bracket_stats(atk_unit, per_model_hp)
    # Per-group WS/BS override (e.g. Boss Nob WS 2+) wins over the bracket value.
    ws_str = grp_ws or live["ws"]
    bs_str = grp_bs or live["bs"]
    skill = int(str(ws_str).rstrip("+")) if use_melee else int(str(bs_str).rstrip("+"))

    is_shooting = phase_key == "shooting"
    is_fight = phase_key == "fight"

    # Cover checkboxes live inside their own resolution block (Dense → HIT,
    # Light/Heavy → SAVE), so each weapon×target tab carries its own cover state.
    cover_key = tab_key

    # Read cover checkbox states (checkboxes are rendered later, state read now)
    dense_cover = is_shooting and st.session_state.get(f"dense_cover_{cover_key}", False)
    light_cover = is_shooting and st.session_state.get(f"light_cover_{cover_key}", False)
    heavy_cover = (
        is_fight
        and st.session_state.get(f"heavy_cover_{cover_key}", False)
        and not def_state.get("turn_flags", {}).get("charged")
    )

    # Build modifier lists including cover effects
    base_atk_mods = _collect_atk_modifiers(atk_faction, atk_state, phase_key, use_melee)
    base_save_mods = _collect_def_save_modifiers(def_faction, phase_key, use_melee)

    weapon_special = _detect_weapon_special(profile)

    final_atk_mods = list(base_atk_mods)
    final_save_mods = list(base_save_mods)
    if weapon_special["klaw_penalty"]:
        final_atk_mods.append(
            {"label": "Power Klaw", "value": -1, "roll_type": "hit", "source": "weapon"}
        )
    if dense_cover:
        final_atk_mods.append(
            {"label": "Dense Cover", "value": -1, "roll_type": "hit", "source": "terrain"}
        )
    if light_cover:
        final_save_mods.append({"label": "Light Cover", "value": 1})
    if heavy_cover:
        final_save_mods.append({"label": "Heavy Cover", "value": 1})

    atk_result = resolve_attack_modifiers(
        skill=skill,
        strength=strength,
        toughness=def_unit.toughness,
        weapon_type=profile.weapon_type,
        advanced=advanced,
        modifiers=final_atk_mods,
        use_melee=use_melee,
    )
    ability_inv = ability_invuln_save(def_faction, def_unit)
    native_inv = def_unit.invuln_save
    if ability_inv is not None and (native_inv is None or ability_inv < native_inv):
        effective_invuln: int | None = ability_inv
        invuln_from_ability = True
    else:
        effective_invuln = native_inv
        invuln_from_ability = False

    save_result = resolve_save(
        base_save=def_unit.save,
        invuln_save=effective_invuln,
        ap=ap,
        save_modifiers=final_save_mods,
    )
    fnp_value = resolve_fnp(def_unit.fnp, profile.ignores_fnp)

    # Header
    atk_override = entry.get("atk_override")
    atk_count = (
        str(atk_override)
        if atk_override is not None
        else _compute_attacks(
            profile.attacks, models_count, grp_attacks, profile.effect, profile.max_attacks
        )
    )
    # D5: no redundant weapon profile line — S/T, AP, Sv and damage all appear
    # in their blocks below. Only the attack count is needed up front.
    st.markdown(
        f"**{atk_unit.name_en}** → **{def_unit.name_en}**  \n"
        f"_{weapon.name_en}_ — "
        f'<span style="font-size:1.05rem;font-weight:700;color:#fbbf24;">{atk_count}</span>'
        " Attacks",
        unsafe_allow_html=True,
    )

    # HIT BLOCK
    if weapon_special["auto_hit"]:
        st.markdown("**HIT** &nbsp; AUTO-HIT", unsafe_allow_html=True)
    else:
        _render_dice_roll_block("HIT", skill_label, atk_result["hit"], weapon_special)

    # Dense Cover checkbox: Shooting phase only, affects hit roll → in the HIT block
    if is_shooting:
        st.checkbox("Dense Cover (−1 Hit)", key=f"dense_cover_{cover_key}")

    st.markdown("")

    # WOUND BLOCK
    _render_dice_wound_block(
        strength, def_unit.toughness, atk_result["wound"]["stack"], strength_buff=str_bonus
    )

    st.markdown("---")

    # SAVE BLOCK
    _render_dice_save_block(save_result, ap, ability_invuln=invuln_from_ability)

    # Cover checkboxes for save modifiers (phase-bound) → in the SAVE block
    if is_shooting:
        st.checkbox("Light Cover (+1 Save vs Ranged)", key=f"light_cover_{cover_key}")
    if is_fight:
        def_charged = def_state.get("turn_flags", {}).get("charged", False)
        if not def_charged:
            st.checkbox("Heavy Cover (+1 Save vs Melee)", key=f"heavy_cover_{cover_key}")

    if def_unit.fnp is not None:
        st.markdown("")
        if fnp_value is None:
            st.markdown(f"~~**FNP**~~ ~~{def_unit.fnp}+~~ _(ignored)_")
        else:
            st.markdown(f"**FNP** &nbsp; [ {fnp_value}+ ]", unsafe_allow_html=True)

    st.markdown("---")

    # DAMAGE BLOCK
    _render_damage_block(
        def_unit,
        def_faction,
        def_uid,
        profile,
        atk_unit.name_en,
        phase_key,
        tab_key,
    )


# ---------------------------------------------------------------------------
# 6d-v2 Declaration phase
# ---------------------------------------------------------------------------


def reset_group_declaration_state() -> None:
    """Clear group-by-group declaration state (on unit switch, phase change, resolution)."""
    st.session_state.selected_model_group = None
    st.session_state.group_targets = {}
    st.session_state.group_decl = {}
    sel = st.session_state.get("selected_unit")
    if sel:
        st.session_state.pop(f"group_autosel_done_{sel[1]}", None)


def group_flow_attacker() -> tuple[str, str, Unit, dict] | None:  # type: ignore[type-arg]
    """Return (faction, uid, unit, state) when the selected unit declares via model groups."""
    sel = st.session_state.get("selected_unit")
    if not sel:
        return None
    faction, uid = sel
    unit, unit_state = lookup(faction, uid)
    if not unit.model_groups:
        return None
    return faction, uid, unit, unit_state


def is_group_target(def_faction: str, def_uid: str) -> bool:
    """True if the target is assigned to the currently selected model group."""
    gid = st.session_state.get("selected_model_group")
    if not gid:
        return False
    targets: dict = st.session_state.get("group_targets", {})  # type: ignore[type-arg]
    return (def_faction, def_uid) in targets.get(gid, [])


def _is_engaged_with(atk_state: dict, def_faction: str, def_uid: str) -> bool:  # type: ignore[type-arg]
    """True if the defender is in the attacker's melee_with list."""
    melee_with = atk_state.get("melee_with", [])
    return [def_faction, def_uid] in melee_with or (def_faction, def_uid) in melee_with


def _in_friendly_melee(atk_faction: str, def_faction: str, def_uid: str) -> bool:
    """True if the target is locked in melee with a unit friendly to the attacker.

    9E: a unit may not shoot into a combat involving friendly units.
    """
    def_state = st.session_state.get(units_key_for(def_faction), {}).get(def_uid, {})
    return any(fac == atk_faction for fac, _ in def_state.get("melee_with", []))


def group_target_selectable(def_faction: str, def_uid: str) -> bool:
    """Whether ▷ may select this enemy as a target right now.

    Shooting: targets in melee with the attacker's friends are blocked (9E).
    Group flow: a group must be selected first; in the fight phase only
    engaged enemies are legal targets (Engagement Range, core rules).
    """
    phase_key = PHASES[st.session_state.phase_idx][1]
    if phase_key not in ("shooting", "fight"):
        return True
    sel = st.session_state.get("selected_unit")
    if phase_key == "shooting" and sel and _in_friendly_melee(sel[0], def_faction, def_uid):
        return False
    info = group_flow_attacker()
    if info is None:
        return True
    if not st.session_state.get("selected_model_group"):
        return False
    if phase_key != "fight":
        return True
    _, _, _, atk_state = info
    return _is_engaged_with(atk_state, def_faction, def_uid)


def toggle_group_target(def_faction: str, def_uid: str) -> bool:
    """Assign/unassign a target to the selected model group. Returns True if handled."""
    gid = st.session_state.get("selected_model_group")
    info = group_flow_attacker()
    if not gid or info is None:
        return False
    if not group_target_selectable(def_faction, def_uid):
        return True  # consume the click — never fall back to selected_targets
    _, _, unit, unit_state = info
    group = next((g for g in unit.model_groups if g.id == gid), None)
    if group is None:
        return False

    targets: dict = dict(st.session_state.get("group_targets", {}))  # type: ignore[type-arg]
    current: list = list(targets.get(gid, []))  # type: ignore[type-arg]
    key = (def_faction, def_uid)
    if key in current:
        current.remove(key)
    else:
        alive = unit_state.get("group_models", {}).get(gid, group.count)
        phase_key = PHASES[st.session_state.phase_idx][1]
        # In shooting phase a single-model group can only shoot one target;
        # in fight phase even a 1-model group may split attacks across targets.
        current = [key] if (alive == 1 and phase_key != "fight") else current + [key]
    targets[gid] = current
    st.session_state.group_targets = targets
    return True


def _group_phase_weapons(group, use_melee: bool, in_melee: bool) -> list:  # type: ignore[no-untyped-def, type-arg]
    """Weapons of a group usable in the current phase (Pistols only while engaged)."""
    if in_melee and not use_melee:
        return [
            w
            for w in group.weapons
            if any(not p.is_melee and p.weapon_type.startswith("Pistol") for p in w.profiles)
        ]
    return [w for w in group.weapons if any(p.is_melee == use_melee for p in w.profiles)]


def _target_display_name(def_faction: str, def_uid: str) -> str:
    tgt_unit, _ = lookup(def_faction, def_uid)
    return tgt_unit.name_en


def render_group_cards(
    atk_faction: str,
    atk_uid: str,
    atk_unit: Unit,
    atk_state: dict,  # type: ignore[type-arg]
    use_melee: bool,
    phase_key: str,
    in_melee: bool = False,
) -> None:
    """Owner-side subUnitCards: select a group, review declared groups, start resolution.

    Rendered in the player area of the unit's owner. Declared groups collapse to a
    summary with an Edit button; the resolution starts once at least one group has
    declared attacks.
    """
    from gameMechanic.ability_engine import buff_stat_bonus  # noqa: PLC0415

    atk_bonus = buff_stat_bonus(atk_faction, atk_unit, "attacks")
    group_models: dict[str, int] = atk_state.get("group_models", {})
    group_decl: dict = st.session_state.get("group_decl", {})  # type: ignore[type-arg]
    group_targets: dict = st.session_state.get("group_targets", {})  # type: ignore[type-arg]
    sel_gid = st.session_state.get("selected_model_group")

    autosel_flag = f"group_autosel_done_{atk_uid}"
    if sel_gid is None and not st.session_state.get(autosel_flag):
        eligible = [
            g
            for g in atk_unit.model_groups
            if group_models.get(g.id, g.count) > 0
            and _group_phase_weapons(g, use_melee, in_melee)
            and group_decl.get(g.id) is None
        ]
        if len(eligible) == 1:
            st.session_state.selected_model_group = eligible[0].id
            st.session_state[autosel_flag] = True
            sel_gid = eligible[0].id

    for group in atk_unit.model_groups:
        alive = group_models.get(group.id, group.count)
        if alive == 0:
            continue
        grp_weapons = _group_phase_weapons(group, use_melee, in_melee)
        if not grp_weapons:
            continue

        with st.container(border=True):
            entries = group_decl.get(group.id)
            if entries is not None and sel_gid != group.id:
                st.markdown(f"**✓ {group.name_en}** ({alive})")
                for e in entries:
                    count = e.get("atk_override", e["models_count"])
                    if count > 0:
                        st.caption(
                            f"{e['weapon_name']} → {count} @ "
                            f"{_target_display_name(e['def_faction'], e['def_uid'])}"
                        )
                if st.button(
                    "✎ Edit",
                    key=f"editgrp_{atk_uid}_{group.id}",
                    use_container_width=True,
                ):
                    st.session_state.selected_model_group = group.id
                    st.rerun()
                continue

            is_sel = sel_gid == group.id
            label = f"◀ {group.name_en} ({alive})" if is_sel else f"▶ {group.name_en} ({alive})"
            if st.button(
                label,
                key=f"selgrp_{atk_uid}_{group.id}",
                type="primary" if is_sel else "secondary",
                use_container_width=True,
            ):
                st.session_state.selected_model_group = None if is_sel else group.id
                st.rerun()
            if use_melee:
                grp_attacks = int(group.stat("attacks", atk_unit.attacks or 0))
                budget = _group_melee_budget(grp_weapons, alive, grp_attacks + atk_bonus)
                st.caption(f"{budget} attacks")
            st.caption(", ".join(w.name_en for w in grp_weapons))
            if is_sel:
                assigned = group_targets.get(group.id, [])
                melee_with = atk_state.get("melee_with", [])
                if phase_key == "fight" and melee_with:
                    st.caption("Targets (engaged):")
                    for entry in melee_with:
                        def_faction, def_uid = entry[0], entry[1]
                        _, def_state = lookup(def_faction, def_uid)
                        if def_state.get("destroyed") or def_state.get("in_reserve"):
                            continue
                        is_assigned = (def_faction, def_uid) in [(f, u) for f, u in assigned]
                        tgt_name = _target_display_name(def_faction, def_uid)
                        btn_label = f"✓ {tgt_name}" if is_assigned else f"＋ {tgt_name}"
                        if st.button(
                            btn_label,
                            key=f"engtgt_{atk_uid}_{group.id}_{def_uid}",
                            type="primary" if is_assigned else "secondary",
                            use_container_width=True,
                        ):
                            toggle_group_target(def_faction, def_uid)
                            st.rerun()
                else:
                    if assigned:
                        for tgt_faction, tgt_uid in assigned:
                            st.caption(f"→ {_target_display_name(tgt_faction, tgt_uid)}")
                    else:
                        st.caption("Designate a target (▷) from the enemy army list.")

    all_entries = [
        e
        for grp_entries in group_decl.values()
        for e in grp_entries
        if e.get("atk_override", e["models_count"]) > 0
    ]
    if st.button(
        "Start Resolution →",
        type="primary",
        disabled=not all_entries,
        key=f"start_res_{atk_uid}",
    ):
        st.session_state.attack_declaration = {
            "active": True,
            "atk_faction": atk_faction,
            "atk_uid": atk_uid,
            "phase_key": phase_key,
            "use_melee": use_melee,
            "in_melee": in_melee,
            "entries": all_entries,
            "seq": _next_declaration_seq(),
        }
        reset_group_declaration_state()
        st.rerun()


def render_group_assignment(
    atk_faction: str,
    atk_uid: str,
    atk_unit: Unit,
    atk_state: dict,  # type: ignore[type-arg]
    use_melee: bool,
    in_melee: bool = False,
) -> None:
    """Defender-side panel: assign attacks/models of the selected group to its targets.

    Rendered in the opposite player area. Writes the group's entries to
    st.session_state.group_decl when the player confirms the group.
    """
    gid = st.session_state.get("selected_model_group")
    if not gid:
        st.caption("Waiting — opponent selects a model group.")
        return
    group = next((g for g in atk_unit.model_groups if g.id == gid), None)
    if group is None:
        return
    alive = atk_state.get("group_models", {}).get(gid, group.count)
    tgts: list[tuple[str, str]] = st.session_state.get("group_targets", {}).get(gid, [])
    if not tgts:
        st.caption("← Designate a target (▷) from your army list.")
        return

    from gameMechanic.ability_engine import buff_stat_bonus  # noqa: PLC0415

    atk_bonus = buff_stat_bonus(atk_faction, atk_unit, "attacks")
    grp_weapons = _group_phase_weapons(group, use_melee, in_melee)

    # Per-group stat overrides (e.g. Boss Nob A 3 / S 5 / WS 2+) fall back to the
    # unit-level value for homogeneous groups.
    grp_attacks = int(group.stat("attacks", atk_unit.attacks or 0))
    grp_strength = int(group.stat("strength", atk_unit.strength))
    grp_ws = group.stat("ws", None)
    grp_bs = group.stat("bs", None)

    def _val(key: str) -> int:
        try:
            return int(st.session_state.get(key, 0) or 0)
        except (TypeError, ValueError):
            return 0

    def _ranged_profile(weapon) -> WeaponProfile:  # type: ignore[no-untyped-def]
        return next((p for p in weapon.profiles if not p.is_melee), weapon.profiles[0])

    # Budget overview on top; counters below are capped so overbooking is impossible.
    group_budget = 0
    weapon_caps: dict[str, int] = {}
    if use_melee:
        group_budget = _group_melee_budget(grp_weapons, alive, grp_attacks + atk_bonus)
        total_assigned = sum(
            _val(f"decl_a_{gid}_{atk_uid}_{d_uid}_{w.name_en}")
            for _, d_uid in tgts
            for w in grp_weapons
        )
        st.markdown(
            f"**{group.name_en}** — {alive} model(s) · "
            f'<span style="font-size:1.1rem;font-weight:700;color:#fbbf24;">'
            f"{total_assigned} / {group_budget}</span> attacks assigned",
            unsafe_allow_html=True,
        )
    else:
        # One model per unit may throw a grenade per phase (core rules: Grenade)
        for w in grp_weapons:
            grenade = _ranged_profile(w).weapon_type.startswith("Grenade")
            weapon_caps[w.name_en] = 1 if grenade else alive
        weapon_assigned = {
            w.name_en: sum(_val(f"decl_m_{gid}_{atk_uid}_{d_uid}_{w.name_en}") for _, d_uid in tgts)
            for w in grp_weapons
        }
        summary = " · ".join(
            f"{name}: {weapon_assigned[name]}/{cap}" for name, cap in weapon_caps.items()
        )
        st.markdown(f"**{group.name_en}** — {alive} model(s)")
        st.caption(summary)

    entries: list[dict] = []  # type: ignore[type-arg]
    models_assigned = 0
    attacks_assigned = 0

    for i, (def_faction, def_uid) in enumerate(tgts):
        def_unit, _ = lookup(def_faction, def_uid)
        with st.container(border=True):
            st.markdown(f"**→ {def_unit.name_en}**")
            c_t, c_sv, c_inv = st.columns(3)
            c_t.metric("T", def_unit.toughness)
            c_sv.metric("Sv", f"{def_unit.save}+")
            c_inv.metric("++", f"{def_unit.invuln_save}+" if def_unit.invuln_save else "—")

            if use_melee:
                for weapon in grp_weapons:
                    profiles = [p for p in weapon.profiles if p.is_melee]
                    if not profiles:
                        profiles = weapon.profiles
                    if len(profiles) > 1:
                        p_names = [p.name or f"Profile {j + 1}" for j, p in enumerate(profiles)]
                        p_key = f"decl_p_{gid}_{atk_uid}_{def_uid}_{weapon.name_en}"
                        sel_p = st.radio(
                            f"Profile — {weapon.name_en}", p_names, key=p_key, horizontal=True
                        )
                        profile_idx = p_names.index(sel_p)
                    else:
                        profile_idx = 0
                    profile = profiles[profile_idx]
                    rule_max = (
                        _total_attacks_int(
                            profile.attacks,
                            alive,
                            grp_attacks + atk_bonus,
                            profile.effect,
                            profile.max_attacks,
                        )
                        or group_budget
                    )
                    atk_key = f"decl_a_{gid}_{atk_uid}_{def_uid}_{weapon.name_en}"
                    if atk_key not in st.session_state:
                        is_first = i == 0 and weapon is grp_weapons[0]
                        st.session_state[atk_key] = rule_max if is_first else 0
                    # Remaining budget caps this counter — overbooking impossible
                    budget_left = group_budget - (total_assigned - _val(atk_key))
                    weapon_max = max(0, min(rule_max, budget_left))
                    if _val(atk_key) > weapon_max:
                        st.session_state[atk_key] = weapon_max
                    atk_count = st.number_input(
                        f"{weapon.name_en} — Attacks",
                        min_value=0,
                        max_value=weapon_max,
                        step=1,
                        key=atk_key,
                    )
                    entries.append(
                        {
                            "def_faction": def_faction,
                            "def_uid": def_uid,
                            "weapon_name": weapon.name_en,
                            "profile_idx": profile_idx,
                            "models_count": alive,
                            "atk_override": int(atk_count),
                            "atk_attacks": grp_attacks,
                            "atk_strength": grp_strength,
                            "atk_ws": grp_ws,
                            "atk_bs": grp_bs,
                        }
                    )
                    attacks_assigned += int(atk_count)
            else:
                for weapon in grp_weapons:
                    profiles = [p for p in weapon.profiles if p.is_melee == use_melee]
                    if not profiles:
                        profiles = list(weapon.profiles)
                    if len(profiles) > 1:
                        p_names = [p.name or f"Profile {j + 1}" for j, p in enumerate(profiles)]
                        p_key = f"decl_p_{gid}_{atk_uid}_{def_uid}_{weapon.name_en}"
                        sel_p = st.radio(
                            f"Profile — {weapon.name_en}",
                            p_names,
                            key=p_key,
                            horizontal=True,
                        )
                        profile_idx = p_names.index(sel_p)
                    else:
                        profile_idx = 0
                    profile = profiles[profile_idx]
                    cap = weapon_caps.get(weapon.name_en, alive)
                    models_key = f"decl_m_{gid}_{atk_uid}_{def_uid}_{weapon.name_en}"
                    if models_key not in st.session_state:
                        # Grenades start at 0 (optional); everything else fires fully
                        st.session_state[models_key] = cap if (i == 0 and cap > 1) else 0
                    # Remaining models for this weapon cap the counter
                    others = weapon_assigned[weapon.name_en] - _val(models_key)
                    weapon_max = max(0, cap - others)
                    if _val(models_key) > weapon_max:
                        st.session_state[models_key] = weapon_max
                    models_val = st.number_input(
                        f"{weapon.name_en} — models",
                        min_value=0,
                        max_value=weapon_max,
                        step=1,
                        key=models_key,
                    )
                    eff_models = int(models_val)
                    displayed_count = _compute_attacks(
                        profile.attacks,
                        eff_models,
                        atk_unit.attacks,
                        profile.effect,
                        profile.max_attacks,
                    )
                    if profile.weapon_type.startswith("Rapid Fire") and profile.range_inches > 0:
                        half = profile.range_inches // 2
                        st.caption(f'[RAPID FIRE · {profile.range_inches}" · ½ = {half}"]')
                    st.markdown(
                        f"**{weapon.name_en}** → "
                        f'<span style="font-size:1.1rem;font-weight:700;color:#fbbf24;">'
                        f"{displayed_count}</span> Attacks",
                        unsafe_allow_html=True,
                    )
                    entries.append(
                        {
                            "def_faction": def_faction,
                            "def_uid": def_uid,
                            "weapon_name": weapon.name_en,
                            "profile_idx": profile_idx,
                            "models_count": eff_models,
                            "atk_attacks": grp_attacks,
                            "atk_strength": grp_strength,
                            "atk_ws": grp_ws,
                            "atk_bs": grp_bs,
                        }
                    )
                    models_assigned += eff_models

    valid = attacks_assigned > 0 if use_melee else models_assigned > 0

    if st.button(
        "✓ Group done",
        type="primary",
        disabled=not valid,
        key=f"grp_done_{atk_uid}_{gid}",
    ):
        group_decl = dict(st.session_state.get("group_decl", {}))
        group_decl[gid] = entries
        st.session_state.group_decl = group_decl
        st.session_state.selected_model_group = None
        st.rerun()


# ---------------------------------------------------------------------------
# 6d-v2 Resolution phase
# ---------------------------------------------------------------------------


def render_attack_resolution(phase_key: str) -> None:
    """Phase 2 — One tab per (weapon × target). Reads state from attack_declaration."""
    decl = st.session_state.get("attack_declaration", {})
    if not decl.get("active"):
        return

    atk_faction = decl["atk_faction"]
    atk_uid = decl["atk_uid"]
    use_melee = decl["use_melee"]
    entries = decl.get("entries", [])

    atk_unit, atk_state = lookup(atk_faction, atk_uid)
    badges = state_badges_html(atk_state)

    st.markdown(f"**{atk_unit.name_en}** — Resolution")
    if badges:
        st.markdown(badges, unsafe_allow_html=True)

    if st.button("↺ Reset Declaration", key="reset_decl"):
        st.session_state.attack_declaration = _empty_attack_declaration()
        st.rerun()

    if not entries:
        return

    tab_labels = []
    for entry in entries:
        def_unit, _ = lookup(entry["def_faction"], entry["def_uid"])
        tab_labels.append(f"{entry['weapon_name']} → {def_unit.name_en}")

    seq = decl.get("seq", 0)

    # Cover checkboxes are rendered inside each tab's HIT/SAVE block (Option B),
    # so they appear in the block they actually modify.
    tabs = st.tabs(tab_labels)
    for i, (tab, entry) in enumerate(zip(tabs, entries)):
        with tab:
            tab_key = f"{seq}_{atk_uid}_{entry['def_uid']}_{i}"
            res_key = f"res_{tab_key}"
            tab_state = st.session_state.get(res_key, {})

            if tab_state.get("applied"):
                def_unit_t, _ = lookup(entry["def_faction"], entry["def_uid"])
                m_lost = tab_state.get("models_lost", 0)
                mw = tab_state.get("mortal_wounds", 0)
                total = tab_state.get("total_damage", 0)
                st.success(f"✓ {m_lost} models · {mw} MW · {total} damage")
                _render_rp_block(
                    def_unit_t, entry["def_faction"], entry["def_uid"], m_lost, tab_key
                )
                if st.button("↺ Reset", key=f"res_reset_{tab_key}"):
                    for k in (res_key, f"rp_{tab_key}"):
                        st.session_state.pop(k, None)
                    st.rerun()
            else:
                _render_resolution_tab(
                    entry,
                    atk_faction,
                    atk_unit,
                    atk_state,
                    use_melee,
                    phase_key,
                    tab_key,
                )

    all_applied = all(
        st.session_state.get(f"res_{seq}_{atk_uid}_{e['def_uid']}_{j}", {}).get("applied", False)
        for j, e in enumerate(entries)
    )
    if all_applied and entries:
        st.markdown("---")
        if st.button("✓ All done — Continue", type="primary", key="all_done"):
            st.session_state.attack_declaration = _empty_attack_declaration()
            st.rerun()
