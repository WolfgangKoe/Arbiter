"""Shared UI utilities for phase handlers.

Provides: lookup, state_badges_html, wound_adjustment_buttons,
          render_player_column, render_attack_declaration,
          render_attack_resolution, PHASE_RULES.

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


def _compute_attacks(attacks_str: str, models_count: int, unit_attacks: int) -> str:
    """Return display string for total attack count."""
    s = str(attacks_str).strip()
    if s in ("Melee", "None", ""):
        return str(models_count * unit_attacks)
    try:
        return str(models_count * int(s))
    except ValueError:
        return f"{models_count}×{s}"


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
# 6d-v2 Display helpers
# ---------------------------------------------------------------------------


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


def _render_wound_table(
    strength: int,
    toughness: int,
    wound_stack: list[dict],  # type: ignore[type-arg]
) -> None:
    """Render the 5-row wound threshold table with the active row highlighted."""
    from gameMechanic.combat import wound_threshold  # noqa: PLC0415

    base = wound_threshold(strength, toughness)
    net = min(1, max(-1, sum(e["value"] for e in wound_stack)))
    modified = max(2, base - net)

    thresholds = [
        (f"S ≥ 2T &nbsp;(S≥{toughness * 2})", 2),
        (f"S > T &nbsp;&nbsp;(S>{toughness})", 3),
        (f"S = T &nbsp;&nbsp;(S={toughness})", 4),
        (f"S < T &nbsp;&nbsp;(S<{toughness})", 5),
        (f"S ≤ ½T (S≤{toughness // 2})", 6),
    ]
    rows = []
    for label, thresh in thresholds:
        active = thresh == base
        col = "#c9a84c" if active else "#666"
        bg = "#1a1a2e" if active else "transparent"
        arrow = "▶" if active else "&nbsp;&nbsp;"
        thresh_cell = f"<b>{thresh}+</b>" if active else f"{thresh}+"
        rows.append(
            f'<tr style="background:{bg};color:{col};">'
            f'<td style="padding:1px 4px;font-size:12px;width:16px;">{arrow}</td>'
            f'<td style="padding:1px 8px;font-size:12px;">{label}</td>'
            f'<td style="padding:1px 6px;font-size:12px;">→ {thresh_cell}</td>'
            f"</tr>"
        )
    html = (
        '<table style="border-collapse:collapse;width:100%;margin:2px 0;">'
        + "".join(rows)
        + "</table>"
    )
    st.markdown(html, unsafe_allow_html=True)
    if wound_stack:
        for e in wound_stack:
            sign = "+" if e["value"] > 0 else ""
            st.markdown(f"&nbsp;&nbsp;{sign}{e['value']} _{e['label']}_", unsafe_allow_html=True)
        st.markdown(f"→ &nbsp;**{modified}+**", unsafe_allow_html=True)


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
    """Render Reanimation Protocols block after damage if target is a Necron unit."""
    from gameMechanic.game_state import faction_dir_for  # noqa: PLC0415
    from gameMechanic.unit_mutations import heal_unit  # noqa: PLC0415

    if models_lost <= 0:
        return
    try:
        fdir = faction_dir_for(def_faction)
    except KeyError:
        return
    if not fdir.startswith("necron"):
        return

    rp_key = f"rp_{tab_key}"
    rp_state = st.session_state.get(rp_key, {})
    if rp_state.get("applied"):
        mb = rp_state.get("models_back", 0)
        if mb > 0:
            st.caption(f"RP: {mb} Modelle zurückgekehrt ✓")
        return

    rp_dice = models_lost * def_unit.wounds
    st.markdown(
        f"**REANIMATION PROTOCOLS** &nbsp; "
        f"{models_lost} × {def_unit.name_en} gefallen → **{rp_dice} Würfel** · Erfolg: 5+"
    )
    models_back = st.number_input(
        "Modelle zurück",
        min_value=0,
        max_value=models_lost,
        step=1,
        key=f"rp_mb_{tab_key}",
    )
    c1, c2 = st.columns(2)
    with c1:
        if c1.button("RP anwenden", key=f"rp_apply_{tab_key}", type="primary"):
            if int(models_back) > 0:
                heal_unit(def_uid, def_faction, int(models_back) * def_unit.wounds, def_unit)
            st.session_state[rp_key] = {"applied": True, "models_back": int(models_back)}
            st.rerun()
    with c2:
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
        st.success(f"✓ {m_lost} Modelle · {mw} MW · {total} Schaden angewandt")
        _render_rp_block(def_unit, def_faction, def_uid, m_lost, tab_key)
        if st.button("↺ Zurücksetzen", key=f"res_reset_{tab_key}"):
            for k in (res_key, f"rp_{tab_key}"):
                st.session_state.pop(k, None)
            st.rerun()
        return

    st.markdown("**SCHADEN**")
    st.caption("Modelle verloren = vollständig vernichtete Modelle")
    is_multi_lp = def_unit.wounds > 1
    dmg_str = str(profile.damage)
    dmg_label = f"D{dmg_str}" if not dmg_str.lstrip("+-").isdigit() else f"{dmg_str} fix"
    st.caption(f"Schaden: {dmg_label} pro missgl. Rettungswurf · Ziel: {def_unit.wounds} LP/Modell")

    c1, c2 = st.columns(2)
    with c1:
        models_lost = st.number_input(
            "Modelle verloren",
            min_value=0,
            step=1,
            key=f"ml_{tab_key}",
        )
    with c2:
        mortal_wounds = st.number_input(
            "Tödliche Verwundungen",
            min_value=0,
            step=1,
            key=f"mw_{tab_key}",
        )

    wounds_on_front = 0
    if is_multi_lp:
        wounds_on_front = st.number_input(
            f"Wunden Frontmodell (0–{def_unit.wounds - 1})",
            min_value=0,
            max_value=def_unit.wounds - 1,
            step=1,
            key=f"wf_{tab_key}",
        )

    total = apply_damage_attacks(
        int(models_lost), int(wounds_on_front), int(mortal_wounds), def_unit.wounds
    )
    btn_label = f"⚔ {total} Schaden → {def_unit.name_en}" if total > 0 else "Schaden anwenden"
    if st.button(btn_label, key=f"apply_{tab_key}", type="primary", use_container_width=True):
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

_COVER_OPTIONS: list[str] = [
    "Kein Cover",
    "Light Cover (+1 Save)",
    "Dense Cover (−1 Hit)",
    "Heavy Cover (+1 Save vs Melee)",
]


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

    def_unit, _ = lookup(def_faction, def_uid)

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

    strength = _parse_strength(str(profile.strength), atk_unit.strength)
    ap = int(profile.ap)
    skill_label = "WS" if use_melee else "BS"
    advanced = atk_state.get("turn_flags", {}).get("advanced", False)

    per_model_hp = atk_state.get("current_wounds", atk_unit.wounds) // max(
        1, atk_state.get("models", atk_unit.models_max)
    )
    live = resolve_bracket_stats(atk_unit, per_model_hp)
    skill = int(live["ws"].rstrip("+")) if use_melee else int(live["bs"].rstrip("+"))

    # Read cover from session_state (set by selectbox from previous render, default Kein Cover)
    cover = st.session_state.get(f"cover_{tab_key}", _COVER_OPTIONS[0])

    # Build modifier lists including cover effects
    base_atk_mods = _collect_atk_modifiers(atk_faction, atk_state, phase_key, use_melee)
    base_save_mods = _collect_def_save_modifiers(def_faction, phase_key, use_melee)

    final_atk_mods = list(base_atk_mods)
    final_save_mods = list(base_save_mods)
    if cover.startswith("Dense"):
        final_atk_mods.append(
            {"label": "Dense Cover", "value": -1, "roll_type": "hit", "source": "terrain"}
        )
    if cover.startswith("Light"):
        final_save_mods.append({"label": "Light Cover", "value": 1})
    elif cover.startswith("Heavy") and not atk_state.get("turn_flags", {}).get("charged"):
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
    save_result = resolve_save(
        base_save=def_unit.save,
        invuln_save=def_unit.invuln_save,
        ap=ap,
        save_modifiers=final_save_mods,
    )
    fnp_value = resolve_fnp(def_unit.fnp, profile.ignores_fnp)

    # Header
    atk_count = _compute_attacks(profile.attacks, models_count, atk_unit.attacks)
    ap_str = f"AP{ap}" if ap != 0 else "AP0"
    st.markdown(
        f"**{atk_unit.name_en}** → **{def_unit.name_en}**  \n"
        f"_{weapon.name_en}_ — {atk_count} att · S{strength} · {ap_str} · D{profile.damage}"
    )
    waaagh_atk = st.session_state.get("waaagh_state", {}).get(atk_faction)
    if waaagh_atk and use_melee:
        stage = waaagh_atk.get("stage", 1)
        inv_txt = "5+" if stage == 1 else "6+"
        st.caption(f"Waaagh! Stage {stage}: +1 Strength · +1 Attacks · {inv_txt} invuln")

    # HIT BLOCK
    _render_roll_block("TREFFER", skill_label, atk_result["hit"])
    st.markdown("")

    # WOUND TABLE
    st.markdown("**VERWUNDUNG**")
    _render_wound_table(strength, def_unit.toughness, atk_result["wound"]["stack"])

    st.markdown("---")

    # SAVE BLOCK + FNP + COVER
    _render_save_block(save_result, ap)
    if def_unit.fnp is not None:
        st.markdown("")
        if fnp_value is None:
            st.markdown(f"~~**FNP**~~ ~~{def_unit.fnp}+~~ _(ignoriert)_")
        else:
            st.markdown(f"**FNP** &nbsp; [ {fnp_value}+ ]", unsafe_allow_html=True)
    st.selectbox("Deckung", _COVER_OPTIONS, key=f"cover_{tab_key}")

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


def render_attack_declaration(
    atk_faction: str,
    atk_uid: str,
    atk_unit: Unit,
    atk_state: dict,  # type: ignore[type-arg]
    use_melee: bool,
    phase_key: str,
    in_melee: bool = False,
) -> None:
    """Phase 1 — Declare targets, weapons, model counts. Writes to attack_declaration on confirm."""
    tgts: list[tuple[str, str]] = st.session_state.selected_targets
    if not tgts:
        st.caption("Designate a target (▷) to begin attack declaration.")
        return

    models_alive = atk_state.get("models", atk_unit.models_max)

    if in_melee and not use_melee:
        weapons = [
            w
            for w in atk_unit.weapons
            if any(not p.is_melee and p.weapon_type.startswith("Pistol") for p in w.profiles)
        ]
    else:
        weapons = [w for w in atk_unit.weapons if any(p.is_melee == use_melee for p in w.profiles)]

    if not weapons:
        st.info("No melee weapons." if use_melee else "No ranged weapons.")
        return

    st.markdown(f"**{atk_unit.name_en}** — Angriff deklarieren")
    if in_melee:
        st.info("Engaged in melee — Pistol weapons only.")

    entries: list[dict] = []  # type: ignore[type-arg]
    models_assigned = 0
    models_lbl = "Anzahl kämpfende Modelle" if use_melee else "Anzahl schießende Modelle"

    for i, (def_faction, def_uid) in enumerate(tgts):
        def_unit, _ = lookup(def_faction, def_uid)

        with st.container(border=True):
            st.markdown(f"**→ {def_unit.name_en}**")
            c_t, c_sv, c_inv = st.columns(3)
            c_t.metric("T", def_unit.toughness)
            c_sv.metric("Sv", f"{def_unit.save}+")
            c_inv.metric("++", f"{def_unit.invuln_save}+" if def_unit.invuln_save else "—")

            # Weapon selection — multiselect allows MONSTER/VEHICLE to fire all weapons
            if len(weapons) > 1:
                sel_w_names: list[str] = st.multiselect(
                    "Waffen",
                    [w.name_en for w in weapons],
                    default=[weapons[0].name_en],
                    key=f"decl_ws_{atk_uid}_{def_uid}",
                )
                sel_weapons = [w for w in weapons if w.name_en in sel_w_names]
            else:
                sel_weapons = [weapons[0]]
                st.caption(f"Waffe: **{weapons[0].name_en}**")

            # Model counter (shared — same models fire all selected weapons)
            models_key = f"decl_m_{atk_uid}_{def_uid}"
            if models_key not in st.session_state:
                st.session_state[models_key] = models_alive if i == 0 else 0

            models_val = st.number_input(
                models_lbl,
                min_value=0,
                max_value=models_alive,
                step=1,
                key=models_key,
            )

            if not sel_weapons:
                st.warning("Mindestens eine Waffe auswählen.")
            else:
                # Profile selection + attack count per selected weapon
                for weapon in sel_weapons:
                    profiles = [p for p in weapon.profiles if p.is_melee == use_melee]
                    if not profiles:
                        profiles = weapon.profiles
                    if len(profiles) > 1:
                        p_names = [p.name or f"Profil {j + 1}" for j, p in enumerate(profiles)]
                        p_key = f"decl_p_{atk_uid}_{def_uid}_{weapon.name_en}"
                        sel_p = st.radio(
                            f"Profil — {weapon.name_en}", p_names, key=p_key, horizontal=True
                        )
                        profile_idx = p_names.index(sel_p)
                    else:
                        profile_idx = 0
                    profile = profiles[profile_idx]
                    atk_count = _compute_attacks(profile.attacks, int(models_val), atk_unit.attacks)
                    st.markdown(
                        f"**{weapon.name_en}** → "
                        f'<span style="font-size:1.1rem;font-weight:700;color:#fbbf24;">'
                        f"{atk_count}</span> Attacken",
                        unsafe_allow_html=True,
                    )
                    entries.append(
                        {
                            "def_faction": def_faction,
                            "def_uid": def_uid,
                            "weapon_name": weapon.name_en,
                            "profile_idx": profile_idx,
                            "models_count": int(models_val),
                        }
                    )

                models_assigned += int(models_val)

    remaining = models_alive - models_assigned
    if remaining < 0:
        st.error(f"Zu viele Modelle zugeteilt ({models_assigned}/{models_alive})")
    elif remaining > 0:
        st.caption(f"Verbleibend: {remaining} / {models_alive} nicht zugeteilt")
    else:
        st.caption(f"✓ {models_alive} / {models_alive} Modelle zugeteilt")

    can_start = 0 < models_assigned <= models_alive
    if st.button(
        "Auflösung starten →",
        type="primary",
        disabled=not can_start,
        key=f"start_res_{atk_uid}",
    ):
        st.session_state.attack_declaration = {
            "active": True,
            "atk_faction": atk_faction,
            "atk_uid": atk_uid,
            "phase_key": phase_key,
            "use_melee": use_melee,
            "in_melee": in_melee,
            "entries": [e for e in entries if e["models_count"] > 0],
        }
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

    st.markdown(f"**{atk_unit.name_en}** — Auflösung")
    if badges:
        st.markdown(badges, unsafe_allow_html=True)

    if st.button("↺ Deklaration zurücksetzen", key="reset_decl"):
        st.session_state.attack_declaration = _empty_attack_declaration()
        st.rerun()

    if not entries:
        return

    tab_labels = []
    for entry in entries:
        def_unit, _ = lookup(entry["def_faction"], entry["def_uid"])
        tab_labels.append(f"{entry['weapon_name']} → {def_unit.name_en}")

    tabs = st.tabs(tab_labels)
    for i, (tab, entry) in enumerate(zip(tabs, entries)):
        with tab:
            tab_key = f"{atk_uid}_{entry['def_uid']}_{i}"
            res_key = f"res_{tab_key}"
            tab_state = st.session_state.get(res_key, {})

            if tab_state.get("applied"):
                def_unit_t, _ = lookup(entry["def_faction"], entry["def_uid"])
                m_lost = tab_state.get("models_lost", 0)
                mw = tab_state.get("mortal_wounds", 0)
                total = tab_state.get("total_damage", 0)
                st.success(f"✓ {m_lost} Modelle · {mw} MW · {total} Schaden")
                _render_rp_block(
                    def_unit_t, entry["def_faction"], entry["def_uid"], m_lost, tab_key
                )
                if st.button("↺ Zurücksetzen", key=f"res_reset_{tab_key}"):
                    for k in (res_key, f"rp_{tab_key}"):
                        st.session_state.pop(k, None)
                    st.rerun()
            else:
                _render_resolution_tab(
                    entry, atk_faction, atk_unit, atk_state, use_melee, phase_key, tab_key
                )

    all_applied = all(
        st.session_state.get(f"res_{atk_uid}_{e['def_uid']}_{j}", {}).get("applied", False)
        for j, e in enumerate(entries)
    )
    if all_applied and entries:
        st.markdown("---")
        if st.button("✓ Alle Tabs abgeschlossen — Weiter", type="primary", key="all_done"):
            st.session_state.attack_declaration = _empty_attack_declaration()
            st.rerun()
