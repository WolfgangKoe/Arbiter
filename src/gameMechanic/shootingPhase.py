"""ShootingPhaseHandler — Shooting Phase for WH40k 9E.

Ziel 3c: can_shoot(), full AttackSequence via combat.py.
"""

from __future__ import annotations

from typing import ClassVar

import streamlit as st

from constants.symbols import SYM_EXPAND_ALT
from gameMechanic.ability_engine import get_active_round_choice_shoot_after_fall_back
from gameMechanic.game_state import units_key_for
from uiLayout._common import (
    group_flow_attacker,
    render_attack_resolution,
    render_group_assignment,
    render_group_cards,
    render_player_column,
)


def can_shoot(
    unit_state: dict,
    unit=None,  # type: ignore[type-arg]
    faction: str | None = None,
    uid: str | None = None,
) -> bool:
    """Return True if the unit may shoot this turn.

    9E: units that advanced, retreated, are in melee (unless VEHICLE/MONSTER), or in reserve
    cannot shoot. VEHICLE and MONSTER units may shoot even while in melee (Big Guns Never Tire).

    Exception: if faction and uid are provided and an active shoot_after_fall_back effect
    grants the unit permission to shoot after falling back (e.g. Conquering Tyrant D2),
    the retreated block is bypassed. The advanced and in_reserve blocks remain enforced.
    """
    flags = unit_state.get("turn_flags", {})
    if flags.get("shot"):
        return False
    if flags.get("advanced") or unit_state.get("in_reserve"):
        return False
    if flags.get("retreated"):
        if faction and uid and get_active_round_choice_shoot_after_fall_back(faction, uid) != 0:
            pass  # D2 exemption: unit may shoot after falling back
        else:
            return False
    if unit_state.get("in_melee"):
        if unit is not None and (unit.has_keyword("VEHICLE") or unit.has_keyword("MONSTER")):
            return True
        if unit is not None and any(
            p.weapon_type.startswith("Pistol") for w in unit.weapons for p in w.profiles
        ):
            return True
        return False
    return True


def target_in_friendly_melee(atk_faction: str, def_faction: str, def_uid: str) -> bool:
    """Return True if the target is in melee with a unit friendly to the attacker.

    9E: a unit may not shoot into a combat involving friendly units.
    """
    def_key = units_key_for(def_faction)
    def_state = st.session_state[def_key].get(def_uid, {})
    return any(fac == atk_faction for fac, _ in def_state.get("melee_with", []))


class ShootingPhaseHandler:
    """PhaseHandler for the Shooting Phase."""

    phase_name: ClassVar[str] = "shooting"

    def render_active(self, state: dict) -> None:  # type: ignore[type-arg]
        first: str = state["first_player"]
        second: str = state["second_player"]

        attack_form_shown = _render_display(state)
        if attack_form_shown:
            return

        st.divider()

        # Model-group flow: the defender column shows the group attack assignment
        group_override = None
        atk_faction = ""
        ginfo = group_flow_attacker()
        if ginfo is not None:
            atk_faction, atk_uid, atk_unit, atk_state = ginfo
            if can_shoot(atk_state, atk_unit, faction=atk_faction, uid=atk_uid):
                in_melee = atk_state.get("in_melee", False)

                def group_override() -> None:
                    render_group_assignment(
                        atk_faction,
                        atk_uid,
                        atk_unit,
                        atk_state,
                        use_melee=False,
                        in_melee=in_melee,
                    )

        col1, col2 = st.columns(2)
        with col1:
            render_player_column(
                first,
                state,
                active_content=_active_shooting,
                inactive_content=_inactive_target_stats,
                no_target_caption=f"← Designate a target ({SYM_EXPAND_ALT}) from your army list.",
                inactive_override=group_override if first != atk_faction else None,
                show_wound_buttons=False,
            )
        with col2:
            render_player_column(
                second,
                state,
                active_content=_active_shooting,
                inactive_content=_inactive_target_stats,
                no_target_caption=f"← Designate a target ({SYM_EXPAND_ALT}) from your army list.",
                inactive_override=group_override if second != atk_faction else None,
                show_wound_buttons=False,
            )


# ---------------------------------------------------------------------------
# Phase-specific content helpers
# ---------------------------------------------------------------------------


def _active_shooting(
    faction: str, uid: str, unit, unit_state: dict, state: dict  # type: ignore[type-arg]
) -> None:
    """Show shooting eligibility and ranged weapon list for the selected unit."""
    flags = unit_state.get("turn_flags", {})
    if flags.get("shot"):
        st.info("Already shot this phase.")
        return
    if not can_shoot(unit_state, unit, faction=faction, uid=uid):
        if flags.get("advanced"):
            st.warning("Advanced this turn — cannot shoot.")
        elif flags.get("retreated"):
            st.warning("Retreated this turn — cannot shoot.")
        elif unit_state.get("in_melee"):
            st.warning("Bound in melee — no Pistol weapons to fire.")
        else:
            st.warning("In reserve — cannot shoot.")
        return

    in_melee = unit_state.get("in_melee", False)

    if in_melee:
        st.info("Engaged in melee — Pistol weapons only.")
    render_group_cards(
        faction,
        uid,
        unit,
        unit_state,
        use_melee=False,
        phase_key="shooting",
        in_melee=in_melee,
    )


def _inactive_target_stats(
    faction: str, uid: str, unit, unit_state: dict  # type: ignore[type-arg]
) -> None:
    """Show target defensive stats (T / Sv / ++) in the inactive column."""
    inv_display = f"{unit.invuln_save}+" if unit.invuln_save else "—"
    cols = st.columns(3)
    cols[0].metric("T", unit.toughness)
    cols[1].metric("Sv", f"{unit.save}+")
    cols[2].metric("++", inv_display)


def _render_display(state: dict) -> bool:  # type: ignore[type-arg]
    """Render attack form if applicable. Returns True when the form is shown."""
    decl = st.session_state.get("attack_declaration", {})
    if decl.get("active") and decl.get("phase_key") == "shooting":
        render_attack_resolution("shooting")
        return True

    return False
