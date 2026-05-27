"""MovementPhaseHandler — Movement Phase for WH40k 9E.

Ziel 3a: Migrates existing movement UI from gameActionsArea.
Ziel 4:  Full turn_flags tracking, advance-roll, reserve deployment.
"""

from __future__ import annotations

import streamlit as st

from engine import log_action, set_deployment, set_movement_status
from uiLayout._common import PHASE_RULES, render_player_column


class MovementPhaseHandler:
    """PhaseHandler for the Movement Phase."""

    phase_name: str = "movement"

    def render_start(self, state: dict) -> None:  # type: ignore[type-arg]
        pass

    def render_active(self, state: dict) -> None:  # type: ignore[type-arg]
        first: str = state["first_player"]
        second: str = state["second_player"]

        col1, col2 = st.columns(2)
        with col1:
            render_player_column(first, state, active_content=_active_movement)
        with col2:
            render_player_column(second, state, active_content=_active_movement)

        st.divider()
        st.info(PHASE_RULES["movement"])

    def render_end(self, state: dict) -> None:  # type: ignore[type-arg]
        pass


# ---------------------------------------------------------------------------
# Phase-specific content helpers
# ---------------------------------------------------------------------------


def _active_movement(
    faction: str, uid: str, unit, unit_state: dict, state: dict  # type: ignore[type-arg]
) -> None:
    """Render movement type buttons for the active player's selected unit."""
    if unit_state.get("in_reserve"):
        if st.session_state.round == 1:
            st.warning("In Reserve — cannot deploy until Round 2.")
        else:
            st.info("In Reserve — deploy from the board edge.")
            if st.button(
                "Deploy from Reserve",
                key=f"deploy_reserve_{faction}_{uid}",
                type="primary",
                use_container_width=True,
            ):
                set_deployment(uid, faction, "normal")
                set_movement_status(uid, faction, "normal")
                log_action(
                    st.session_state.round, "movement", unit.name_en, "deployed from reserve"
                )
                st.rerun()
        return

    flags = unit_state.get("turn_flags", {})
    in_melee = unit_state.get("in_melee", False)

    # Determine current display state from turn_flags
    if flags.get("advanced"):
        current = "advanced"
    elif flags.get("retreated"):
        current = "retreated"
    else:
        current = "none"

    st.markdown("Set movement status:")
    cols = st.columns(4)
    options = [
        ("Normal", "normal", 'Move up to M"'),
        ("Advance", "advanced", 'M"+D6", no shoot/charge'),
        ("Stationary", "stationary", "Do not move"),
        ("Retreat", "retreated", "Exit melee, no shoot/charge"),
    ]
    for col, (label, value, tip) in zip(cols, options):
        with col:
            disabled = value == "retreated" and not in_melee
            btn_type = "primary" if current == value else "secondary"
            if st.button(
                label,
                key=f"mv_{faction}_{uid}_{value}",
                type=btn_type,
                disabled=disabled,
                use_container_width=True,
                help=tip,
            ):
                set_movement_status(uid, faction, value)
                log_action(st.session_state.round, "movement", unit.name_en, f"movement: {value}")
                st.rerun()

    if in_melee and current not in ("retreated",):
        st.caption("Unit is in melee — only Stationary or Retreat allowed.")
