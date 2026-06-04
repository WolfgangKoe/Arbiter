"""Shared UI utilities for phase handlers.

Provides: lookup, state_badges_html, wound_adjustment_buttons,
          render_player_column, render_attack_form, PHASE_RULES.

Handlers import from here — never from gameActionsArea — to avoid circular imports.
"""

from __future__ import annotations

from collections.abc import Callable

import streamlit as st

from gameMechanic.game_state import units_key_for, units_list_for
from gameMechanic.unit_mutations import apply_damage, heal_unit
from gameObjects.unit import Unit

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
    unit = next(u for u in units if u.id == unit_id)
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
) -> None:
    """Render one player column (active or inactive).

    active_content(faction, uid, unit, unit_state, state) — called when a unit is
    selected for the active player; renders phase-specific actions.

    inactive_content(faction, uid, unit, unit_state) — called when the inactive
    player has a target selected from their army; renders target stats etc.
    If None, only wound adjustment buttons are shown for selected targets.

    no_target_caption — shown to the inactive player when the active player has a
    unit selected but no target from this faction is designated.
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
                st.divider()
                wound_adjustment_buttons(faction, uid, unit)
        elif st.session_state.get("selected_unit"):
            st.caption(no_target_caption)
        else:
            st.caption("—")


# ---------------------------------------------------------------------------
# Attack resolution form (shared by Shooting and Fight Phase)
# ---------------------------------------------------------------------------


def _parse_strength(raw: str, unit_strength: int) -> int:
    """Resolve weapon strength notation to a numeric value.

    Handles: "User" → unit_strength, "User×2" → unit_strength*2,
    "User+2" → unit_strength+2, "+3" → unit_strength+3, plain ints.
    Falls back to unit_strength on unrecognised input.
    """
    s = raw.strip()
    upper = s.upper()
    if upper == "USER":
        return unit_strength
    if upper.startswith("USER"):
        tail = s[4:].strip()
        if tail.startswith("×") or tail.startswith("*"):
            try:
                return unit_strength * int(tail[1:])
            except ValueError:
                pass
        if tail.startswith("+"):
            try:
                return unit_strength + int(tail[1:])
            except ValueError:
                pass
        if tail.startswith("-"):
            try:
                return unit_strength - int(tail[1:])
            except ValueError:
                pass
    if s.startswith("+"):
        try:
            return unit_strength + int(s[1:])
        except ValueError:
            pass
    try:
        return int(s)
    except ValueError:
        return unit_strength


def _protocol_source_label(faction_dir: str) -> str:
    from gameObjects.loader import load_round_choice_abilities  # noqa: PLC0415

    protocol_id = st.session_state.get("active_protocol_id")
    directive = st.session_state.get("active_directive")
    if not protocol_id or not directive or not faction_dir:
        return "Protocol"
    protocols = load_round_choice_abilities(faction_dir)
    p = next((proto for proto in protocols if proto.id == protocol_id), None)
    return f"{p.name_en} ({directive.capitalize()})" if p else "Protocol"


def _render_roll_block(title: str, base_label: str, block: dict) -> None:  # type: ignore[type-arg]
    """Render a hit or wound block with modifier stack."""
    st.markdown(f"**{title}**")
    line = f"[ {base_label} {block['base']}+ ]"
    for entry in block["stack"]:
        sign = "+" if entry["value"] > 0 else ""
        line += f" &nbsp;·&nbsp; {sign}{entry['value']} _{entry['label']}_"
    st.markdown(line, unsafe_allow_html=True)
    if block["stack"]:
        st.markdown(f"→ &nbsp;**{block['modified']}+**", unsafe_allow_html=True)


def _render_save_block(save: dict, ap: int) -> None:  # type: ignore[type-arg]
    """Render the save block with armour/invuln comparison."""
    st.markdown("**RETTUNGSWURF**")
    ap_str = f"AP{ap}" if ap != 0 else "AP0"
    line = f"[ Sv {save['armour']}+ / {ap_str} → {save['armour_eff']}+ ]"
    if save["invuln"] is not None:
        line += f" &nbsp;·&nbsp; Invuln {save['invuln']}+"
    st.markdown(line, unsafe_allow_html=True)
    for m in save["stack"]:
        sign = "+" if m["value"] > 0 else ""
        st.markdown(f"&nbsp;&nbsp;{sign}{m['value']} _{m['label']}_", unsafe_allow_html=True)
    if save["using_invuln"]:
        st.markdown(f"→ &nbsp;**{save['effective']}+** _(invuln)_", unsafe_allow_html=True)
    elif save["save_bonus"] or save["armour_eff"] != save["armour"]:
        st.markdown(f"→ &nbsp;**{save['effective']}+**", unsafe_allow_html=True)


def render_attack_form(
    atk_faction: str,
    atk_uid: str,
    atk_unit: Unit,
    def_faction: str,
    def_uid: str,
    def_unit: Unit,
    use_melee: bool,
    phase_key: str,
) -> None:
    """Simultaneous attack breakdown: hit/wound (attacker) + save/FNP/damage (defender)."""
    from gameMechanic.ability_engine import get_active_protocol_modifier  # noqa: PLC0415
    from gameMechanic.combat import (  # noqa: PLC0415
        resolve_attack_modifiers,
        resolve_fnp,
        resolve_save,
    )
    from gameMechanic.game_log import log_action  # noqa: PLC0415
    from gameMechanic.game_state import faction_dir_for  # noqa: PLC0415

    weapons = [w for w in atk_unit.weapons if any(p.is_melee == use_melee for p in w.profiles)]
    if not weapons:
        st.info("No melee weapons." if use_melee else "No ranged weapons.")
        return

    if len(weapons) > 1:
        weapon = st.radio(
            "Weapon",
            weapons,
            format_func=lambda w: w.name_en,
            key=f"atk_weapon_{phase_key}_{atk_faction}_{atk_uid}",
            horizontal=True,
        )
    else:
        weapon = weapons[0]

    profile = weapon.for_phase(use_melee)
    strength = _parse_strength(str(profile.strength), atk_unit.strength)
    ap = int(profile.ap)
    skill = int(atk_unit.ws.rstrip("+")) if use_melee else int(atk_unit.bs.rstrip("+"))
    skill_label = "WS" if use_melee else "BS"

    atk_state = st.session_state[units_key_for(atk_faction)][atk_uid]
    advanced = atk_state.get("turn_flags", {}).get("advanced", False)

    # Protocol modifiers
    try:
        atk_fdir = faction_dir_for(atk_faction)
        atk_proto = get_active_protocol_modifier(atk_fdir, phase_key, use_melee)
        atk_proto_label = _protocol_source_label(atk_fdir)
    except KeyError:
        atk_fdir, atk_proto, atk_proto_label = "", {}, "Protocol"
    try:
        def_fdir = faction_dir_for(def_faction)
        def_proto = get_active_protocol_modifier(def_fdir, phase_key, use_melee)
        def_proto_label = _protocol_source_label(def_fdir)
    except KeyError:
        def_fdir, def_proto, def_proto_label = "", {}, "Protocol"

    # Assemble attacker modifier list (hit + wound)
    atk_mods: list[dict] = []  # type: ignore[type-arg]
    if atk_proto.get("hit"):
        atk_mods.append(
            {
                "label": atk_proto_label,
                "value": atk_proto["hit"],
                "roll_type": "hit",
                "source": "protocol",
            }
        )
    if atk_proto.get("wound"):
        atk_mods.append(
            {
                "label": atk_proto_label,
                "value": atk_proto["wound"],
                "roll_type": "wound",
                "source": "protocol",
            }
        )
    for b in atk_state.get("active_buffs", []):
        if b.get("effect_type") == "buff_roll":
            atk_mods.append(
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
            atk_mods.append(
                {
                    "label": m.get("source", "Modifier"),
                    "value": eff.get("value", 0),
                    "roll_type": rt,
                    "source": "stratagem",
                }
            )

    # Assemble defender save modifier list
    def_save_mods: list[dict] = []  # type: ignore[type-arg]
    if def_proto.get("save"):
        def_save_mods.append({"label": f"{def_proto_label} (defender)", "value": def_proto["save"]})
    for m in st.session_state.get("active_modifiers", []):
        eff = m.get("effect", {})
        if eff.get("roll_type") == "save" and eff.get("target") in ("defender", "any"):
            def_save_mods.append(
                {"label": m.get("source", "Modifier"), "value": eff.get("value", 0)}
            )

    # Compute via pure functions
    atk_result = resolve_attack_modifiers(
        skill=skill,
        strength=strength,
        toughness=def_unit.toughness,
        weapon_type=profile.weapon_type,
        advanced=advanced,
        modifiers=atk_mods,
        use_melee=use_melee,
    )
    save_result = resolve_save(
        base_save=def_unit.save,
        invuln_save=def_unit.invuln_save,
        ap=ap,
        save_modifiers=def_save_mods,
    )
    fnp_value = resolve_fnp(def_unit.fnp, profile.ignores_fnp)

    # ── Header ─────────────────────────────────────────────────────────────
    atk_display = str(atk_unit.attacks) if profile.attacks in ("Melee", None) else profile.attacks
    ap_str = f"AP{ap}" if ap != 0 else "AP0"
    st.markdown(
        f"**{atk_unit.name_en}** → **{def_unit.name_en}**  \n"
        f"_{weapon.name_en}_ — {atk_display} att · S{strength} · {ap_str} · D{profile.damage}"
    )

    # WAAAGH! info note (fight phase only)
    waaagh_atk = st.session_state.get("waaagh_state", {}).get(atk_faction)
    if waaagh_atk and use_melee:
        stage = waaagh_atk.get("stage", 1)
        inv_txt = "5+" if stage == 1 else "6+"
        st.caption(f"Waaagh! Stage {stage}: +1 Strength · +1 Attacks · {inv_txt} invuln")

    # ── Two-column layout ───────────────────────────────────────────────────
    col_atk, col_def = st.columns(2)

    with col_atk:
        _render_roll_block("TREFFER", skill_label, atk_result["hit"])
        st.markdown("")
        _render_roll_block(
            "VERWUNDUNG",
            f"S{strength} vs T{def_unit.toughness}",
            atk_result["wound"],
        )

    with col_def:
        _render_save_block(save_result, ap)

        if def_unit.fnp is not None:
            st.markdown("")
            if fnp_value is None:
                st.markdown(f"~~**FEEL NO PAIN**~~ ~~{def_unit.fnp}+~~ _(ignoriert)_")
            else:
                st.markdown(f"**FEEL NO PAIN** &nbsp; [ {fnp_value}+ ]", unsafe_allow_html=True)

        st.markdown("---")
        st.markdown("**SCHADEN**")
        dc1, dc2 = st.columns(2)
        damage_input = dc1.number_input(
            f"Normal (D{profile.damage})" if not profile.damage.lstrip("-").isdigit() else "Normal",
            min_value=0,
            step=1,
            key=f"atk_dmg_{phase_key}_{atk_faction}_{atk_uid}",
        )
        mortal_input = dc2.number_input(
            "Mortal Wounds",
            min_value=0,
            step=1,
            key=f"atk_mw_{phase_key}_{atk_faction}_{atk_uid}",
        )
        total = int(damage_input) + int(mortal_input)

        btn_label = (
            f"{'⚔' if use_melee else '🎯'} {total} Schaden → {def_unit.name_en}"
            if total > 0
            else "Schaden zuweisen"
        )
        if st.button(
            btn_label,
            key=f"atk_apply_{phase_key}_{atk_faction}_{atk_uid}",
            type="primary",
            use_container_width=True,
        ):
            if total > 0:
                apply_damage(def_uid, def_faction, total, def_unit)
            atk_flags = st.session_state[units_key_for(atk_faction)][atk_uid]["turn_flags"]
            if phase_key == "shooting":
                atk_flags["shot"] = True
            elif phase_key == "fight":
                atk_flags["fought"] = True
            log_action(
                st.session_state.round,
                phase_key,
                atk_unit.name_en,
                f"dealt {total} damage to {def_unit.name_en}",
            )
            st.rerun()
