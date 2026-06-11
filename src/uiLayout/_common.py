"""Shared UI utilities for phase handlers.

Provides: lookup, state_badges_html, wound_adjustment_buttons,
          render_player_column, render_attack_declaration,
          render_attack_resolution, PHASE_RULES.

Handlers import from here — never from gameActionsArea — to avoid circular imports.
"""

from __future__ import annotations

from collections.abc import Callable

import streamlit as st

from gameMechanic.game_state import PHASES, units_key_for, units_list_for
from gameMechanic.unit_mutations import apply_damage, heal_unit
from gameObjects.unit import Unit
from gameObjects.weapon import WeaponProfile

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


def _parse_strength(raw: int | str, unit_strength: int) -> int:
    """Resolve weapon strength to a numeric value.

    int      → fixed strength
    "User"   → unit_strength
    "+N"     → unit_strength + N  (also "User+N")
    "×N"     → unit_strength × N  (also "User×N")
    "-N"     → unit_strength - N  (also "User-N", rare)
    "*"      → 0 (special-mechanic weapon)
    """
    if isinstance(raw, int):
        return raw
    s = raw.strip()
    if s == "*":
        return 0  # special-mechanic weapon; handled by effect handler
    # Strip optional "User" prefix before the operator
    body = s[4:] if s[:4].upper() == "USER" else s
    if not body or body.upper() == "USER":
        return unit_strength
    if body.startswith("+"):
        return unit_strength + int(body[1:])
    if body.startswith("×"):
        return unit_strength * int(body[1:])
    if body.startswith("-"):
        return unit_strength - int(body[1:])
    return int(s)


def _protocol_source_label(faction_dir: str) -> str:
    from gameObjects.loader import load_round_choice_abilities  # noqa: PLC0415

    protocol_id = st.session_state.get(f"protocol_active_{faction_dir}")
    directive = st.session_state.get(f"protocol_directive_{faction_dir}")
    if not protocol_id or not directive or not faction_dir:
        return "Protocol"
    protocols = load_round_choice_abilities(faction_dir)
    p = next((proto for proto in protocols if proto.id == protocol_id), None)
    return f"{p.name_en} ({directive.capitalize()})" if p else "Protocol"


def _restriction_label(restriction: str) -> str:
    labels = {
        "boss_nob_only": "Boss Nob only",
        "1_per_10": "1 per 10 models",
        "1_per_5": "1 per 5 models",
    }
    return labels.get(restriction, restriction)


def _compute_attacks(
    attacks_str: str,
    models_count: int,
    unit_attacks: int,
    effect: dict | None = None,
    max_attacks: int | None = None,
) -> str:
    """Return display string for total attack count."""
    if effect and effect.get("type") == "extra_attacks":
        if max_attacks is not None:
            return str(models_count * max_attacks)
        amount = int(effect.get("amount", 1))
        return str(models_count * (unit_attacks + amount))
    s = str(attacks_str).strip()
    if s in ("Melee", "None", "", "*"):
        return str(models_count * unit_attacks)
    if "/" in s:
        return str(models_count * int(s.split("/")[0]))
    try:
        return str(models_count * int(s))
    except ValueError:
        return f"{models_count}×{s}"


def _total_attacks_int(
    attacks_str: str,
    models_alive: int,
    unit_attacks: int,
    effect: dict | None = None,
    max_attacks: int | None = None,
) -> int | None:
    """Return total attack count as int, or None if dice-based (cannot pre-split)."""
    if effect and effect.get("type") == "extra_attacks":
        if max_attacks is not None:
            return models_alive * max_attacks
        amount = int(effect.get("amount", 1))
        return models_alive * (unit_attacks + amount)
    s = str(attacks_str).strip()
    if s in ("Melee", "None", "", "*"):
        return models_alive * unit_attacks
    if "/" in s:
        return models_alive * int(s.split("/")[0])
    try:
        return models_alive * int(s)
    except ValueError:
        return None


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


def _detect_weapon_special(profile: WeaponProfile) -> dict:  # type: ignore[type-arg]
    """Detect special weapon abilities from profile fields."""
    abilities = profile.abilities or ""
    return {
        "auto_hit": "Auto-hits" in abilities,
        "tesla": "additional hits" in abilities,
        "dakka": profile.weapon_type == "Dakka",
        "klaw_penalty": profile.is_melee and "subtract" in abilities,
        "has_mortal_wounds": "mortal wound" in abilities.lower(),
    }


# ---------------------------------------------------------------------------
# 6d-v3 SVG dice components
# ---------------------------------------------------------------------------

_THRESHOLD_COLOR: dict[int, str] = {
    2: "#22c55e",
    3: "#22c55e",
    4: "#f59e0b",
    5: "#f97316",
    6: "#f97316",
}

_PIP_POSITIONS: dict[int, list[tuple[int, int]]] = {
    1: [(16, 16)],
    2: [(9, 9), (23, 23)],
    3: [(9, 9), (16, 16), (23, 23)],
    4: [(9, 9), (9, 23), (23, 9), (23, 23)],
    5: [(9, 9), (9, 23), (23, 9), (23, 23), (16, 16)],
    6: [(9, 9), (9, 16), (9, 23), (23, 9), (23, 16), (23, 23)],
}


# Shared column grid (D5): every dice row = badge column + die-sized slots.
# The boundary gap (one die wide) appears in header AND dice row → labels stay
# flush above the die of their value.
_DIE_SLOT = 34  # svg 32px + 2px margin
_FRAME_INSET = 5  # success-frame border+padding shifts dice right by this much
_BUFF_COLOR_HEX = "#4a9a5a"  # Buff = grün (design_colors.md §0)
_DEBUFF_COLOR_HEX = "#ef4444"


def _boundary_gap_html(with_line: bool) -> str:
    """One die-wide gap slot at the success boundary ('Luft' + separator line)."""
    line = (
        '<span style="display:inline-block;width:2px;height:34px;'
        'background:#6b7280;border-radius:1px;"></span>'
        if with_line
        else ""
    )
    return (
        f'<span style="display:inline-block;width:{_DIE_SLOT}px;text-align:center;'
        f'vertical-align:middle;">{line}</span>'
    )


def threshold_header_html(threshold: int) -> str:
    """Header labels 1..6, die-sized and full brightness, aligned with dice_row_html."""
    color = _THRESHOLD_COLOR.get(min(6, threshold), "#f97316")
    parts = []
    for v in range(1, 7):
        if 2 <= threshold <= 6 and v == threshold:
            parts.append(_boundary_gap_html(with_line=False))
        label = f"{v}+"
        if v == threshold:
            style = (
                f"width:{_DIE_SLOT}px;text-align:center;display:inline-block;"
                f"font-size:15px;font-weight:700;color:{color};"
                f"border:1px solid {color};border-radius:3px;"
            )
        else:
            style = (
                f"width:{_DIE_SLOT}px;text-align:center;display:inline-block;"
                f"font-size:15px;font-weight:600;color:#e7e5e4;"
            )
        parts.append(f'<span style="{style}">{label}</span>')
    return f'<div style="display:flex;align-items:center;margin:0 0 1px 0;">{"".join(parts)}</div>'


def dice_face_svg(value: int, color: str = "#6b7280", miss: bool = False, size: int = 32) -> str:
    """SVG for a single d6 face with pip pattern. Value 1 always shows × (always-miss marker)."""
    pips = _PIP_POSITIONS.get(max(1, min(6, value)), [])
    bg = "#111827" if miss else "#1e293b"
    border = "#374151" if miss else color
    if miss and value == 1:
        pip_html = (
            '<line x1="9" y1="9" x2="23" y2="23" stroke="#c0392b" stroke-width="2.5"/>'
            '<line x1="23" y1="9" x2="9" y2="23" stroke="#c0392b" stroke-width="2.5"/>'
        )
    else:
        pip_color = "#374151" if miss else color
        pip_html = "".join(f'<circle cx="{x}" cy="{y}" r="2" fill="{pip_color}"/>' for x, y in pips)
    return (
        f'<svg width="{size}" height="{size}" viewBox="0 0 32 32" '
        f'style="display:inline-block;vertical-align:middle;margin:1px;">'
        f'<rect x="1" y="1" width="30" height="30" rx="4" ry="4" '
        f'fill="{bg}" stroke="{border}" stroke-width="1.5"/>'
        f"{pip_html}</svg>"
    )


def dice_row_html(threshold: int) -> str:
    """Row of 6 dice (values 1–6): miss dice left, success dice inside colored frame.

    D5: one die-wide boundary gap with a separator line sits between the last
    miss die and the success frame — same gap as in threshold_header_html, so
    the columns stay aligned. Threshold > 6 (impossible): 6 miss dice + red ×.
    """
    if threshold > 6:
        miss_dice = "".join(dice_face_svg(v, miss=True) for v in range(1, 7))
        impossible = (
            '<span style="font-size:16px;color:#ef4444;vertical-align:middle;'
            'margin:0 4px;font-weight:bold;">×</span>'
        )
        return f'<div style="margin:4px 0;">{miss_dice}{impossible}</div>'
    frame_color = _THRESHOLD_COLOR.get(threshold, "#f97316")
    success_dice = "".join(dice_face_svg(v, color=frame_color) for v in range(threshold, 7))
    framed = (
        f'<span style="border:2px solid {frame_color};border-radius:5px;'
        f"padding:2px 3px;display:inline-block;vertical-align:middle;"
        f'margin-left:-{_FRAME_INSET}px;">'
        f"{success_dice}</span>"
    )
    if threshold <= 1:
        # All dice succeed — no miss dice, no gap
        return f'<div style="margin:4px 0;">{framed}</div>'
    miss_section = "".join(dice_face_svg(v, miss=True) for v in range(1, threshold))
    gap = _boundary_gap_html(with_line=True)
    return f'<div style="margin:4px 0;">{miss_section}{gap}{framed}</div>'


_BADGE_COL_W = 96  # left badge column (D5): AP-X, Heavy Cover, MWBD, Eff., …


def _badge_chip(label: str, color: str) -> str:
    return (
        f'<span style="font-size:11px;color:{color};background:#111827;'
        f"border:1px solid {color};border-radius:3px;padding:1px 5px;"
        f'white-space:nowrap;">{label}</span>'
    )


def grid_row_html(label_html: str, content: str) -> str:
    """One row of the D5 grid: fixed badge column on the left, content right.

    Every row of a dice block (header+dice, modifier pairs, Eff., Inv.) goes
    through this so the dice columns align vertically.
    """
    return (
        f'<div style="display:flex;align-items:center;margin:2px 0;">'
        f'<div style="width:{_BADGE_COL_W}px;flex-shrink:0;display:flex;'
        f'align-items:center;font-size:12px;color:#9ca3af;">{label_html}</div>'
        f'<div style="flex:1;">{content}</div></div>'
    )


def block_divider_html() -> str:
    """Horizontal separator between HIT / WOUND / SAVE blocks (D5: 'Luft')."""
    return '<hr style="border:none;border-top:1px solid #2e2618;margin:10px 0;">'


def modifier_die_pair_html(
    from_thresh: int, to_thresh: int, label: str, value: int, color: str
) -> str:
    """Modifier row: badge column + from-die (neutral) + arrow + to-die (colored).

    Convention: lower die value always on left, higher on right (aligns with dice row).
    Arrow: → for improvements (value > 0), ← for penalties (value < 0).
    For improvements the threshold decreases, so to_thresh < from_thresh — swap so
    the lower value (to_thresh) appears on the left and higher (from_thresh) on the right.
    """
    sign = "+" if value > 0 else ("-" if value < 0 else "")
    arrow = "→" if value > 0 else "←"
    from_clamped = max(1, min(6, from_thresh))
    to_clamped = max(1, min(6, to_thresh))
    # Improvements: grey = new threshold, colored = old threshold (newly passes).
    # Penalties: grey = from_thresh−1 (never hit anyway), colored = from_thresh (newly fails).
    boundary = max(1, min(6, from_thresh - 1))
    if value > 0:
        left_die = dice_face_svg(to_clamped, color="#6b7280")
        right_die = dice_face_svg(from_clamped, color=color)
    else:
        left_die = dice_face_svg(boundary, color="#6b7280")
        right_die = dice_face_svg(from_clamped, color=color)
    pair = (
        f'<div style="display:flex;align-items:center;gap:4px;">'
        f"{left_die}"
        f'<span style="color:{color};font-size:12px;font-weight:bold;">'
        f"{arrow}{sign}{abs(value)}{arrow}</span>"
        f"{right_die}</div>"
    )
    return grid_row_html(_badge_chip(label, color), pair)


def save_modifier_die_pair_html(armour: int, value: int, label: str, color: str) -> str:
    """SAVE modifier pair always anchored to the base armour value (never cumulative).

    Buff  (value > 0, e.g. Cover+1, armour=3): grün(armour-value) → grau(armour)
      "A 2 that used to fail at 3+ now passes."
    Debuff (value < 0, e.g. AP-2,   armour=3): grau(armour-1) → rot(armour+|value|-1)
      "A 4 that used to pass at 3+ now fails (4-2=2 < 3)."
    P16 edge: if the newly-failing value exceeds 6 (e.g. Sv 6+ with AP-4), no die
    can show it — a red × marks the impossible range instead of a clamped die.
    """
    sign = "+" if value > 0 else ("-" if value < 0 else "")
    n = abs(value)
    if value > 0:
        left_val = max(1, min(6, armour - n))
        right_val = max(1, min(6, armour))
        arrow = "→"
        left_die = dice_face_svg(left_val, color=color)
        right_die = dice_face_svg(right_val, color="#6b7280")
    else:
        left_val = max(1, min(6, armour - 1))
        right_raw = armour + n - 1
        right_val = max(1, min(6, right_raw))
        arrow = "←"
        left_die = dice_face_svg(left_val, color="#6b7280")
        if right_raw > 6:
            right_die = (
                f'<span style="font-size:16px;color:{color};vertical-align:middle;'
                f'font-weight:bold;" title="exceeds 6 — save impossible">×</span>'
            )
        else:
            right_die = dice_face_svg(right_val, color=color)
    pair = (
        f'<div style="display:flex;align-items:center;gap:4px;">'
        f"{left_die}"
        f'<span style="color:{color};font-size:12px;font-weight:bold;">'
        f"{arrow}{sign}{n}{arrow}</span>"
        f"{right_die}</div>"
    )
    return grid_row_html(_badge_chip(label, color), pair)


def special_die_html(label: str, content: str = "") -> str:
    """Badge for special weapon abilities (Tesla, Dakka, Power Klaw, Reroll, etc.)."""
    text = f"{label}: {content}" if content else label
    return (
        f'<span style="background:#111827;border:1px solid #f59e0b;border-radius:4px;'
        f'padding:2px 6px;font-size:11px;color:#f59e0b;margin:2px;">'
        f"{text}</span>"
    )


def _render_dice_roll_block(
    title: str,
    skill_label: str,
    block: dict,  # type: ignore[type-arg]
    weapon_special: dict | None = None,  # type: ignore[type-arg]
) -> None:
    """HIT or WOUND roll block: threshold header + dice row + modifier pairs."""
    base = block["base"]
    stack = block.get("stack", [])
    modified = block.get("modified", base)
    st.markdown(f"**{title}** &nbsp; {skill_label} {base}+", unsafe_allow_html=True)
    st.markdown(
        grid_row_html("", threshold_header_html(base) + dice_row_html(base)),
        unsafe_allow_html=True,
    )
    if stack:
        current = base
        parts = []
        for entry in stack:
            next_thresh = max(2, current - entry["value"])
            color = _BUFF_COLOR_HEX if entry["value"] > 0 else _DEBUFF_COLOR_HEX
            parts.append(
                modifier_die_pair_html(current, next_thresh, entry["label"], entry["value"], color)
            )
            current = next_thresh
        parts.append(
            grid_row_html(
                f'<span style="color:#f8fafc;font-weight:600;">Eff. {modified}+</span>',
                threshold_header_html(min(modified, 7)) + dice_row_html(min(modified, 7)),
            )
        )
        st.markdown("".join(parts), unsafe_allow_html=True)
    if weapon_special:
        badges = []
        if weapon_special.get("tesla"):
            badges.append(special_die_html("Tesla", "unmod. 6 = +2 Hits"))
        if weapon_special.get("dakka"):
            badges.append(special_die_html("Dakka"))
        if weapon_special.get("klaw_penalty"):
            badges.append(special_die_html("Power Klaw", "−1 to Hit"))
        if badges:
            st.markdown(
                f'<div style="margin-top:4px;">{"".join(badges)}</div>',
                unsafe_allow_html=True,
            )


def _render_dice_wound_block(
    strength: int,
    toughness: int,
    wound_stack: list[dict],  # type: ignore[type-arg]
) -> None:
    """WOUND block: S vs T header, dice row, modifier pairs in blue."""
    from gameMechanic.combat import wound_threshold  # noqa: PLC0415

    base = wound_threshold(strength, toughness)
    net = min(1, max(-1, sum(e["value"] for e in wound_stack)))
    modified = max(2, base - net)
    rel = ">" if strength > toughness else ("=" if strength == toughness else "<")
    # D5: S/T comparison clearly highlighted; NO "→ N+" — the result is the
    # boxed threshold in the header row below.
    hl = 'style="font-size:1.05rem;font-weight:700;color:#fbbf24;"'
    st.markdown(block_divider_html(), unsafe_allow_html=True)
    st.markdown(
        f"**WOUND** &nbsp; <span {hl}>S {strength}</span> "
        f'<span style="font-size:1.05rem;font-weight:700;color:#e7e5e4;">{rel}</span> '
        f"<span {hl}>T {toughness}</span>",
        unsafe_allow_html=True,
    )
    st.markdown(
        grid_row_html("", threshold_header_html(base) + dice_row_html(base)),
        unsafe_allow_html=True,
    )
    if wound_stack:
        current = base
        parts = []
        for entry in wound_stack:
            next_thresh = max(2, current - entry["value"])
            color = _BUFF_COLOR_HEX if entry["value"] > 0 else _DEBUFF_COLOR_HEX
            parts.append(
                modifier_die_pair_html(current, next_thresh, entry["label"], entry["value"], color)
            )
            current = next_thresh
        parts.append(
            grid_row_html(
                f'<span style="color:#f8fafc;font-weight:600;">Eff. {modified}+</span>',
                threshold_header_html(min(modified, 7)) + dice_row_html(min(modified, 7)),
            )
        )
        st.markdown("".join(parts), unsafe_allow_html=True)


def _render_dice_save_block(save: dict, ap: int) -> None:  # type: ignore[type-arg]
    """SAVE block: table-aligned rows (label | content) for armour, modifiers, eff, invuln."""
    armour = save["armour"]
    armour_eff = save["armour_eff"]
    invuln = save["invuln"]
    effective = save["effective"]
    using_invuln = save["using_invuln"]
    stack = save.get("stack", [])

    # D5: Sv value next to the SAVE title — consistent with WS/BS in the HIT title
    sv_text = f"Sv {armour}+" if armour <= 6 else "Sv —"
    st.markdown(block_divider_html(), unsafe_allow_html=True)
    st.markdown(f"**SAVE** &nbsp; {sv_text}", unsafe_allow_html=True)

    rows: list[str] = []

    # Armour base row
    rows.append(
        grid_row_html("", threshold_header_html(min(armour, 7)) + dice_row_html(min(armour, 7)))
    )

    # Modifier rows (AP + cover stack) — each anchored to base armour, never cumulative
    has_modifiers = ap != 0 or bool(stack)
    if ap != 0:
        rows.append(save_modifier_die_pair_html(armour, ap, f"AP{ap}", _DEBUFF_COLOR_HEX))
    for m in stack:
        color = _BUFF_COLOR_HEX if m["value"] > 0 else _DEBUFF_COLOR_HEX
        rows.append(save_modifier_die_pair_html(armour, m["value"], m["label"], color))

    # Effective save row: always shows the armour-path result (after AP + cover).
    # Invuln is shown separately below with its own row — not mixed into this value.
    if has_modifiers:
        armour_modified = armour_eff - sum(m["value"] for m in stack)
        eff_clamped = min(armour_modified, 7)
        eff_label_text = f"{armour_modified}+" if armour_modified <= 6 else "—"
        rows.append(
            grid_row_html(
                f'<span style="color:#f8fafc;font-weight:600;">Eff. {eff_label_text}</span>',
                threshold_header_html(eff_clamped) + dice_row_html(eff_clamped),
            )
        )

    st.markdown("".join(rows), unsafe_allow_html=True)

    # Invuln save block (separate section)
    if invuln is not None:
        inv_color = _THRESHOLD_COLOR.get(min(6, invuln), "#f97316")
        active_badge = (
            f'<span style="font-size:10px;color:{inv_color};border:1px solid {inv_color};'
            f'border-radius:3px;padding:0 3px;margin-left:4px;">active</span>'
            if using_invuln
            else ""
        )
        note = '<span style="font-size:10px;color:#4b5563;margin-left:4px;">AP/Cover N/A</span>'
        inv_label = f"Inv {invuln}+{active_badge}{note}"
        inv_row = grid_row_html(
            inv_label,
            threshold_header_html(min(invuln, 7)) + dice_row_html(min(invuln, 7)),
        )
        st.markdown(inv_row, unsafe_allow_html=True)


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
    show_cover_controls: bool = True,
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

    strength = _parse_strength(profile.strength, atk_unit.strength)
    ap = profile.ap
    skill_label = "WS" if use_melee else "BS"
    advanced = atk_state.get("turn_flags", {}).get("advanced", False)

    per_model_hp = atk_state.get("current_wounds", atk_unit.wounds) // max(
        1, atk_state.get("models", atk_unit.models_max)
    )
    live = resolve_bracket_stats(atk_unit, per_model_hp)
    skill = int(live["ws"].rstrip("+")) if use_melee else int(live["bs"].rstrip("+"))

    is_shooting = phase_key == "shooting"
    is_fight = phase_key == "fight"

    # Cover is a property of the TARGET, not of the weapon: key per target
    # (tab_key minus the trailing weapon index) so every weapon tab against the
    # same unit shares the cover state (P19).
    cover_key = tab_key.rsplit("_", 1)[0]

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
    save_result = resolve_save(
        base_save=def_unit.save,
        invuln_save=def_unit.invuln_save,
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
            profile.attacks, models_count, atk_unit.attacks, profile.effect, profile.max_attacks
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
    waaagh_atk = st.session_state.get("waaagh_state", {}).get(atk_faction)
    if waaagh_atk and use_melee:
        stage = waaagh_atk.get("stage", 1)
        inv_txt = "5+" if stage == 1 else "6+"
        st.caption(f"Waaagh! Stage {stage}: +1 Strength · +1 Attacks · {inv_txt} invuln")

    # HIT BLOCK
    if weapon_special["auto_hit"]:
        st.markdown("**HIT** &nbsp; AUTO-HIT", unsafe_allow_html=True)
    else:
        _render_dice_roll_block("HIT", skill_label, atk_result["hit"], weapon_special)

    # Dense Cover checkbox: Shooting phase only, affects hit roll → placed near HIT block
    if is_shooting and show_cover_controls:
        st.checkbox("Dense Cover (−1 Hit)", key=f"dense_cover_{cover_key}")

    st.markdown("")

    # WOUND BLOCK
    _render_dice_wound_block(strength, def_unit.toughness, atk_result["wound"]["stack"])

    st.markdown("---")

    # SAVE BLOCK
    _render_dice_save_block(save_result, ap)

    # Cover checkboxes for save modifiers (phase-bound)
    if is_shooting and show_cover_controls:
        st.checkbox("Light Cover (+1 Save vs Ranged)", key=f"light_cover_{cover_key}")
    if is_fight and show_cover_controls:
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
        # A single-model group attacks a single target
        current = [key] if alive == 1 else current + [key]
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


def _group_melee_budget(grp_weapons: list, alive: int, eff_attacks: int) -> int:  # type: ignore[type-arg]
    """Total melee attacks of a group: base attacks + extra-attack weapon bonuses.

    Base = models × attacks (incl. WAAAGH bonus, passed by the caller).
    Each carried weapon with an extra_attacks effect adds its bonus on top
    (e.g. Choppa: "1 additional attack with this weapon"); capped weapons
    (max_attacks, e.g. attack squig) add exactly their cap.
    """
    budget = alive * eff_attacks
    for w in grp_weapons:
        p = next((p for p in w.profiles if p.is_melee), None)
        if p is None or not isinstance(p.effect, dict):
            continue
        if p.effect.get("type") != "extra_attacks":
            continue
        if p.max_attacks:
            budget += alive * int(p.max_attacks)
        else:
            budget += alive * int(p.effect.get("amount", 0))
    return budget


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
    waaagh = st.session_state.get("waaagh_state", {}).get(atk_faction)
    waaagh_bonus = 1 if (waaagh and atk_unit.has_keyword("ORK")) else 0
    group_models: dict[str, int] = atk_state.get("group_models", {})
    group_decl: dict = st.session_state.get("group_decl", {})  # type: ignore[type-arg]
    group_targets: dict = st.session_state.get("group_targets", {})  # type: ignore[type-arg]
    sel_gid = st.session_state.get("selected_model_group")

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
                budget = _group_melee_budget(
                    grp_weapons, alive, (atk_unit.attacks or 0) + waaagh_bonus
                )
                st.caption(f"{budget} attacks")
            st.caption(", ".join(w.name_en for w in grp_weapons))
            if is_sel:
                assigned = group_targets.get(group.id, [])
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

    waaagh = st.session_state.get("waaagh_state", {}).get(atk_faction)
    waaagh_bonus = 1 if (waaagh and atk_unit.has_keyword("ORK")) else 0
    grp_weapons = _group_phase_weapons(group, use_melee, in_melee)

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
        group_budget = _group_melee_budget(
            grp_weapons, alive, (atk_unit.attacks or 0) + waaagh_bonus
        )
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
                            atk_unit.attacks + waaagh_bonus,
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

    st.markdown(f"**{atk_unit.name_en}** — Declare Attack")
    if in_melee:
        st.info("Engaged in melee — Pistol weapons only.")

    if atk_unit.model_groups:
        # Model-group units declare group-by-group via render_group_cards /
        # render_group_assignment in the player areas — never through this path.
        return

    # In fight phase, always distribute by attacks (not models).
    # Attacks can be freely split between targets regardless of model count.
    use_atk_counter = False
    total_attacks: int = 0
    if use_melee:
        first_melee_profiles = [p for w in weapons for p in w.profiles if p.is_melee]
        if first_melee_profiles:
            waaagh = st.session_state.get("waaagh_state", {}).get(atk_faction)
            waaagh_bonus = 1 if (waaagh and atk_unit.has_keyword("ORK")) else 0
            total_attacks_maybe = _total_attacks_int(
                first_melee_profiles[0].attacks,
                models_alive,
                atk_unit.attacks + waaagh_bonus,
                first_melee_profiles[0].effect,
                first_melee_profiles[0].max_attacks,
            )
            if total_attacks_maybe is not None:
                use_atk_counter = True
                total_attacks = total_attacks_maybe

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

            if use_atk_counter:
                # Melee: each weapon gets its own attack counter — no shared count, no multiselect
                for weapon in weapons:
                    profiles = [p for p in weapon.profiles if p.is_melee]
                    if not profiles:
                        profiles = weapon.profiles
                    if len(profiles) > 1:
                        p_names = [p.name or f"Profile {j + 1}" for j, p in enumerate(profiles)]
                        p_key = f"decl_p_{atk_uid}_{def_uid}_{weapon.name_en}"
                        sel_p = st.radio(
                            f"Profile — {weapon.name_en}", p_names, key=p_key, horizontal=True
                        )
                        profile_idx = p_names.index(sel_p)
                    else:
                        profile_idx = 0
                    atk_key = f"decl_a_{atk_uid}_{def_uid}_{weapon.name_en}"
                    restriction = atk_unit.weapon_restrictions.get(weapon.id)
                    atk_per_model = atk_unit.attacks + waaagh_bonus
                    if restriction == "boss_nob_only":
                        weapon_max = atk_per_model
                    elif restriction == "1_per_10":
                        weapon_max = (models_alive // 10) * atk_per_model
                    elif restriction == "1_per_5":
                        weapon_max = (models_alive // 5) * atk_per_model
                    else:
                        weapon_max = total_attacks
                    if atk_key not in st.session_state:
                        is_first = i == 0 and weapon == weapons[0]
                        st.session_state[atk_key] = weapon_max if is_first else 0
                    atk_count = st.number_input(
                        f"{weapon.name_en} — Attacks",
                        min_value=0,
                        max_value=weapon_max,
                        step=1,
                        key=atk_key,
                    )
                    restriction_suffix = (
                        f' &nbsp;<span style="font-size:0.75rem;color:#94a3b8;">[{_restriction_label(restriction)}]</span>'
                        if restriction
                        else ""
                    )
                    st.markdown(
                        f"**{weapon.name_en}**{restriction_suffix} → "
                        f'<span style="font-size:1.1rem;font-weight:700;color:#fbbf24;">'
                        f"{int(atk_count)}</span> Attacks",
                        unsafe_allow_html=True,
                    )
                    entries.append(
                        {
                            "def_faction": def_faction,
                            "def_uid": def_uid,
                            "weapon_name": weapon.name_en,
                            "profile_idx": profile_idx,
                            "models_count": models_alive,
                            "atk_override": int(atk_count),
                        }
                    )
                    attacks_assigned += int(atk_count)
            else:
                # Shooting: multiselect weapons + model counter (unchanged)
                if len(weapons) > 1:
                    sel_w_names: list[str] = st.multiselect(
                        "Weapons",
                        [w.name_en for w in weapons],
                        default=[weapons[0].name_en],
                        key=f"decl_ws_{atk_uid}_{def_uid}",
                    )
                    sel_weapons = [w for w in weapons if w.name_en in sel_w_names]
                else:
                    sel_weapons = [weapons[0]]
                    st.caption(f"Weapon: **{weapons[0].name_en}**")

                models_key = f"decl_m_{atk_uid}_{def_uid}"
                if models_key not in st.session_state:
                    st.session_state[models_key] = models_alive if i == 0 else 0
                models_val = st.number_input(
                    "Models shooting",
                    min_value=0,
                    max_value=models_alive,
                    step=1,
                    key=models_key,
                )

                if not sel_weapons:
                    st.warning("Select at least one weapon.")
                else:
                    for weapon in sel_weapons:
                        profiles = [p for p in weapon.profiles if p.is_melee == use_melee]
                        if not profiles:
                            profiles = weapon.profiles
                        if len(profiles) > 1:
                            p_names = [p.name or f"Profile {j + 1}" for j, p in enumerate(profiles)]
                            p_key = f"decl_p_{atk_uid}_{def_uid}_{weapon.name_en}"
                            sel_p = st.radio(
                                f"Profile — {weapon.name_en}", p_names, key=p_key, horizontal=True
                            )
                            profile_idx = p_names.index(sel_p)
                        else:
                            profile_idx = 0
                        profile = profiles[profile_idx]
                        restr = atk_unit.weapon_restrictions.get(weapon.id)
                        if restr == "boss_nob_only":
                            eff_models = 1
                        elif restr == "1_per_10":
                            eff_models = models_alive // 10
                        elif restr == "1_per_5":
                            eff_models = models_alive // 5
                        else:
                            eff_models = int(models_val)
                        displayed_count = _compute_attacks(
                            profile.attacks,
                            eff_models,
                            atk_unit.attacks,
                            profile.effect,
                            profile.max_attacks,
                        )
                        restr_suffix = (
                            f' &nbsp;<span style="font-size:0.75rem;color:#94a3b8;">[{_restriction_label(restr)}]</span>'
                            if restr
                            else ""
                        )
                        st.markdown(
                            f"**{weapon.name_en}**{restr_suffix} → "
                            f'<span style="font-size:1.1rem;font-weight:700;color:#fbbf24;">'
                            f"{displayed_count}</span> Attacks",
                            unsafe_allow_html=True,
                        )
                        if (
                            profile.weapon_type.startswith("Rapid Fire")
                            and profile.range_inches > 0
                        ):
                            half = profile.range_inches // 2
                            st.caption(f'[RAPID FIRE · {profile.range_inches}" · ½ = {half}"]')
                        entries.append(
                            {
                                "def_faction": def_faction,
                                "def_uid": def_uid,
                                "weapon_name": weapon.name_en,
                                "profile_idx": profile_idx,
                                "models_count": eff_models,
                            }
                        )
                    models_assigned += int(models_val)

    if use_atk_counter:
        remaining = total_attacks - attacks_assigned
        if remaining < 0:
            st.error(f"Too many attacks assigned ({attacks_assigned}/{total_attacks})")
        elif remaining > 0:
            st.caption(f"Remaining: {remaining} / {total_attacks} attacks unassigned")
        else:
            st.caption(f"✓ {total_attacks} / {total_attacks} attacks assigned")
        can_start = 0 < attacks_assigned <= total_attacks
    else:
        remaining = models_alive - models_assigned
        if remaining < 0:
            st.error(f"Too many models assigned ({models_assigned}/{models_alive})")
        elif remaining > 0:
            st.caption(f"Remaining: {remaining} / {models_alive} unassigned")
        else:
            st.caption(f"✓ {models_alive} / {models_alive} assigned")
        can_start = 0 < models_assigned <= models_alive
    if st.button(
        "Start Resolution →",
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
            "entries": [e for e in entries if e.get("atk_override", e["models_count"]) > 0],
            "seq": _next_declaration_seq(),
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
    tabs = st.tabs(tab_labels)
    # Cover checkboxes are per TARGET (P19) — render them only in the first
    # tab of each target, otherwise Streamlit raises DuplicateWidgetID.
    cover_rendered: set[str] = set()
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
                show_cover = entry["def_uid"] not in cover_rendered
                cover_rendered.add(entry["def_uid"])
                _render_resolution_tab(
                    entry,
                    atk_faction,
                    atk_unit,
                    atk_state,
                    use_melee,
                    phase_key,
                    tab_key,
                    show_cover_controls=show_cover,
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
