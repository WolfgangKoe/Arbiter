"""MoralePhaseHandler — Morale Phase for WH40k 9E.

Ziel 3a: Migrates existing morale check from gameActionsArea.
Ziel 4:  Model removal, fleeing logic.
"""

from __future__ import annotations

import streamlit as st

from uiLayout._common import PHASE_RULES, render_player_column


class MoralePhaseHandler:
    """PhaseHandler for the Morale Phase."""

    phase_name: str = "morale"

    def render_start(self, state: dict) -> None:  # type: ignore[type-arg]
        pass

    def render_active(self, state: dict) -> None:  # type: ignore[type-arg]
        first: str = state["first_player"]
        second: str = state["second_player"]

        col1, col2 = st.columns(2)
        with col1:
            render_player_column(first, state, active_content=_active_morale)
        with col2:
            render_player_column(second, state, active_content=_active_morale)

        st.divider()
        st.info(PHASE_RULES["morale"])

    def render_end(self, state: dict) -> None:  # type: ignore[type-arg]
        pass


# ---------------------------------------------------------------------------
# Phase-specific content helpers
# ---------------------------------------------------------------------------


def _active_morale(
    faction: str, uid: str, unit, unit_state: dict, state: dict  # type: ignore[type-arg]
) -> None:
    """Render morale test info for the active player's selected unit."""
    lost = unit_state.get("lost_models_this_turn", 0)
    if unit.models_max == 1:
        st.success("Single model — auto-pass.")
        return
    if lost == 0:
        st.success("No losses this turn — no morale test.")
        return
    st.warning(
        f"**Ld {unit.leadership}** | Lost **{lost}** model(s) this turn.\n\n"
        f"Roll D6 + {lost}. If result > {unit.leadership}: "
        f"remove (result − {unit.leadership}) additional model(s)."
    )
