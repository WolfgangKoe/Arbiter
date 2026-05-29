"""Shared UI utilities for phase handlers.

Provides: lookup, state_badges_html, wound_adjustment_buttons,
          render_player_column, render_attack_form, PHASE_RULES.

Handlers import from here — never from gameActionsArea — to avoid circular imports.
"""

from __future__ import annotations

from collections.abc import Callable

import streamlit as st

from gameMechanic.game_state import _NECRON_UNITS, _ORK_UNITS
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
    "MWBD": ("#60a5fa", "#0a1020"),
}

_MOVEMENT_BADGE: dict[str, str] = {
    "moved": "MOVED",
    "stationary": "STATIONARY",
    "advanced": "ADVANCED",
    "retreated": "RETREATED",
}


def state_badges_html(unit_state: dict) -> str:  # type: ignore[type-arg]
    """Generate HTML state badges from movement_choice, turn_flags and persistent state.

    Priority: FOUGHT > CHARGED > movement_choice (mutex movement slot).
    SHOT is always additive. IN MELEE shows always except when CHARGED is active.
    """

    def _badge(text: str) -> str:
        fg, bg = _BADGE_COLORS.get(text, ("#c9a84c", "#2e2618"))
        return (
            f'<span style="background:{bg};border:1px solid {fg};border-radius:2px;'
            f"padding:1px 6px;font-size:10px;color:{fg};letter-spacing:0.06em;"
            f'font-weight:600;margin-right:3px;">{text}</span>'
        )

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
    if unit_state.get("my_will_be_done_active"):
        parts.append(_badge("MWBD"))
    return "".join(parts)


# ---------------------------------------------------------------------------
# Unit lookup
# ---------------------------------------------------------------------------


def lookup(faction: str, uid: str) -> tuple[Unit, dict]:  # type: ignore[type-arg]
    """Return (Unit, unit_state_dict) for the given faction + uid."""
    units = _NECRON_UNITS if faction == "Necrons" else _ORK_UNITS
    unit = next(u for u in units if u.id == uid)
    key = "necron_units" if faction == "Necrons" else "ork_units"
    return unit, st.session_state[key][uid]


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


def _try_parse_damage(damage_str: str) -> int | None:
    """Return int if damage is fixed, None if variable (D/W notation)."""
    try:
        return int(str(damage_str).strip())
    except ValueError:
        return None


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
    """Render weapon selector, dice inputs, resolve, and apply-damage flow."""
    from gameMechanic.combat import AttackParams, DefendParams, resolve_attack, wound_threshold
    from gameMechanic.game_log import log_action

    weapons = [w for w in atk_unit.weapons if w.is_melee == use_melee]
    if not weapons:
        st.info("No melee weapons." if use_melee else "No ranged weapons.")
        return

    st.markdown(f"**{atk_unit.name_en}** → **{def_unit.name_en}**")

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

    # Resolve "User" strength to unit strength.
    raw_str = str(weapon.strength)
    strength = atk_unit.strength if raw_str.upper() == "USER" else int(raw_str)

    skill = int(atk_unit.ws.rstrip("+")) if use_melee else int(atk_unit.bs.rstrip("+"))
    skill_label = "WS" if use_melee else "BS"
    thresh = wound_threshold(strength, def_unit.toughness)
    eff_save = def_unit.save + abs(int(weapon.ap))
    if def_unit.invuln_save and def_unit.invuln_save < eff_save:
        eff_save = def_unit.invuln_save
    save_str = f"{eff_save}+" if eff_save <= 6 else "none"
    inv_display = f"{def_unit.invuln_save}+" if def_unit.invuln_save else "none"

    st.caption(
        f"**{weapon.name_en}**: {weapon.attacks} att · {skill_label}{skill}+ · "
        f"wound {thresh}+ · save {save_str} (++ {inv_display}) · D{weapon.damage}"
    )

    unit_key = "necron_units" if atk_faction == "Necrons" else "ork_units"
    atk_state = st.session_state[unit_key][atk_uid]
    mwbd_active = atk_state.get("my_will_be_done_active", False)
    if mwbd_active:
        st.info("MWBD active — +1 to hit modifier.")

    c1, c2, c3, c4 = st.columns(4)
    hits = c1.number_input(
        "Hits", min_value=0, step=1, key=f"atk_hits_{phase_key}_{atk_faction}_{atk_uid}"
    )
    wounds = c2.number_input(
        "Wounds", min_value=0, step=1, key=f"atk_wnds_{phase_key}_{atk_faction}_{atk_uid}"
    )
    saves_failed = c3.number_input(
        "Failed Saves", min_value=0, step=1, key=f"atk_sfail_{phase_key}_{atk_faction}_{atk_uid}"
    )
    fnp_saved = c4.number_input(
        "FNP Saved", min_value=0, step=1, key=f"atk_fnp_{phase_key}_{atk_faction}_{atk_uid}"
    )

    fixed_dmg = _try_parse_damage(str(weapon.damage))
    total_dmg_input = None
    if fixed_dmg is None:
        total_dmg_input = st.number_input(
            f"Total damage rolled ({weapon.damage} per failed save)",
            min_value=0,
            step=1,
            key=f"atk_dmgtotal_{phase_key}_{atk_faction}_{atk_uid}",
        )

    result_key = f"atk_result_{phase_key}_{atk_faction}_{atk_uid}"

    if st.button(
        "Resolve Attack",
        key=f"atk_resolve_{phase_key}_{atk_faction}_{atk_uid}",
        type="primary",
        use_container_width=True,
    ):
        if fixed_dmg is not None:
            params = AttackParams(
                attacks=1,
                skill=skill,
                strength=strength,
                ap=int(weapon.ap),
                damage=fixed_dmg,
                mwbd_active=mwbd_active,
            )
            def_params = DefendParams(
                toughness=def_unit.toughness,
                save=def_unit.save,
                wounds=def_unit.wounds,
                invul_save=def_unit.invuln_save,
                fnp=def_unit.fnp,
            )
            damage, log = resolve_attack(
                params,
                def_params,
                int(hits),
                int(wounds),
                int(saves_failed),
                int(fnp_saved),
            )
        else:
            raw = int(total_dmg_input or 0)
            fnp_n = int(fnp_saved)
            net = max(0, raw - fnp_n)
            log = [
                f"Hits: {hits}",
                f"Wounds: {wounds}",
                f"Failed saves: {saves_failed}",
                f"Variable damage {weapon.damage}: {raw} total",
                f"FNP saved: {fnp_n}",
                f"Damage: **{net}**",
            ]
            damage = net
        st.session_state[result_key] = (damage, log)
        st.rerun()

    result = st.session_state.get(result_key)
    if result:
        damage, log = result
        for line in log:
            st.markdown(f"- {line}")
        if damage > 0:
            if st.button(
                f"Apply {damage} damage to {def_unit.name_en}",
                key=f"atk_apply_{phase_key}_{atk_faction}_{atk_uid}",
                type="primary",
                use_container_width=True,
            ):
                apply_damage(def_uid, def_faction, damage, def_unit)
                atk_key = "necron_units" if atk_faction == "Necrons" else "ork_units"
                atk_flags = st.session_state[atk_key][atk_uid]["turn_flags"]
                if phase_key == "shooting":
                    atk_flags["shot"] = True
                elif phase_key == "fight":
                    atk_flags["fought"] = True
                log_action(
                    st.session_state.round,
                    phase_key,
                    atk_unit.name_en,
                    f"dealt {damage} damage to {def_unit.name_en}",
                )
                del st.session_state[result_key]
                st.rerun()
        else:
            st.info("No damage dealt.")
            if st.button("Clear", key=f"atk_clear_{phase_key}_{atk_faction}_{atk_uid}"):
                del st.session_state[result_key]
                st.rerun()
