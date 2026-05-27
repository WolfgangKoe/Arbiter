"""PsychicPhaseHandler — Psychic Phase for WH40k 9E.

Ziel 3a: Migrates existing PSYKER check from gameActionsArea.
Ziel 4:  Manifest (2D6 ≥ WC), Deny, Perils.
"""

from __future__ import annotations

import streamlit as st

from uiLayout._common import PHASE_RULES, render_player_column


class PsychicPhaseHandler:
    """PhaseHandler for the Psychic Phase."""

    phase_name: str = "psychic"

    def render_start(self, state: dict) -> None:  # type: ignore[type-arg]
        pass

    def render_active(self, state: dict) -> None:  # type: ignore[type-arg]
        first: str = state["first_player"]
        second: str = state["second_player"]

        col1, col2 = st.columns(2)
        with col1:
            render_player_column(first, state, active_content=_active_psychic)
        with col2:
            render_player_column(second, state, active_content=_active_psychic)

        st.divider()
        st.info(PHASE_RULES["psychic"])

    def render_end(self, state: dict) -> None:  # type: ignore[type-arg]
        pass


# ---------------------------------------------------------------------------
# Phase-specific content helpers
# ---------------------------------------------------------------------------


def _active_psychic(
    faction: str, uid: str, unit, unit_state: dict, state: dict  # type: ignore[type-arg]
) -> None:
    """Render psychic action for the active player's selected unit."""
    is_psyker = any(kw.upper() == "PSYKER" for kw in unit.keywords)
    if is_psyker:
        st.info("PSYKER — declare Smite or psychic powers manually.")
    else:
        st.warning("Not a PSYKER — no action possible.")
