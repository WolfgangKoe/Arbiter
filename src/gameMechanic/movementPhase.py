"""MovementPhaseHandler — Movement Phase for WH40k 9E.

Ziel 3a: Migrates existing movement UI from gameActionsArea.
Ziel 4:  Full turn_flags tracking, advance-roll, reserve deployment.
"""

from __future__ import annotations

import streamlit as st

from gameMechanic.game_log import log_action
from gameMechanic.unit_mutations import set_deployment, set_movement_status
from uiLayout._common import PHASE_RULES, lookup, render_player_column


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
            if first == state["active"]:
                _render_reinforcements_step(first)
        with col2:
            render_player_column(second, state, active_content=_active_movement)
            if second == state["active"]:
                _render_reinforcements_step(second)

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
        st.caption("In reserve — manage deployment in 'Step 2: Reinforcements' below.")
        return

    in_melee = unit_state.get("in_melee", False)
    current = unit_state.get("movement_choice") or "none"
    flags = unit_state.get("turn_flags", {})
    already_retreated = flags.get("retreated", False)

    if already_retreated:
        st.caption("Already retreated this turn — no further movement possible.")
        return

    st.markdown("Set movement status:")
    options = [
        ("Move", "moved", 'Move up to M"'),
        ("Advance", "advanced", 'M"+D6", no shoot/charge'),
        ("Stay Stationary", "stationary", "Do not move"),
        ("Retreat", "retreated", "Exit melee, no shoot/charge"),
    ]

    for label, value, tip in options:
        disabled = (value in ("moved", "advanced") and in_melee) or (
            value == "retreated" and not in_melee
        )
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

    if in_melee:
        st.caption("Unit is in melee — only Stay Stationary or Retreat allowed.")


def _render_reinforcements_step(faction: str) -> None:
    """Always-visible reinforcements section for the active player."""
    key = "necron_units" if faction == "Necrons" else "ork_units"
    units_state = st.session_state[key]
    reserve_units = [(uid, us) for uid, us in units_state.items() if us.get("in_reserve")]

    st.markdown("**Step 2: Reinforcements**")

    if not reserve_units:
        st.caption("No reinforcements this round.")
        return

    if st.session_state.round == 1:
        st.caption("Units in reserve — cannot deploy until Round 2.")
        return

    for uid, _ in reserve_units:
        unit, _ = lookup(faction, uid)
        if st.button(
            f"Deploy {unit.name_en} from Reserve",
            key=f"deploy_reserve_{faction}_{uid}",
            type="primary",
            use_container_width=True,
        ):
            set_deployment(uid, faction, "normal")
            set_movement_status(uid, faction, "moved")
            log_action(st.session_state.round, "movement", unit.name_en, "deployed from reserve")
            st.rerun()
