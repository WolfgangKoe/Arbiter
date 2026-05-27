"""Phase runner — central dispatcher for all game phases.

PHASE_REGISTRY maps phase_key → PhaseHandler instance.
render_current_phase(state) is the single entry point called by gameActionsArea.
"""

from __future__ import annotations

import streamlit as st

from gameMechanic.ability_engine import (
    get_triggered_abilities,
)
from gameMechanic.phase_handler import PhaseHandler

# ---------------------------------------------------------------------------
# Registry
# ---------------------------------------------------------------------------

PHASE_REGISTRY: dict[str, PhaseHandler] = {}


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------


def render_current_phase(state: dict) -> None:  # type: ignore[type-arg]
    """Look up the handler for the current phase and render its active stage."""
    from engine import PHASES  # noqa: PLC0415

    phase_key: str = PHASES[state["phase_idx"]][1]
    handler = PHASE_REGISTRY.get(phase_key)
    if handler is None:
        st.warning(f"Phase '{phase_key}' has no registered handler.")
        return

    stage: str = state.get("phase_stage", "active")

    # Fire ability hooks at phase transitions (start / end).
    if stage in ("start", "end"):
        get_triggered_abilities(state, phase_key, f"phase_{stage}")

    getattr(handler, f"render_{stage}")(state)


def advance_stage(state: dict) -> None:  # type: ignore[type-arg]
    """Advance the phase stage: start → active → end → next_phase.

    Called by the phase-navigation button in gameProtocoll.
    At end → next_phase transition, turn_flags are reset by engine.next_phase().
    """
    from engine import next_phase  # noqa: PLC0415

    stage: str = state.get("phase_stage", "active")
    if stage == "start":
        state["phase_stage"] = "active"
    elif stage == "active":
        state["phase_stage"] = "end"
    else:
        state["phase_stage"] = "active"
        next_phase()


# ---------------------------------------------------------------------------
# Registry population — runs once at import time
# ---------------------------------------------------------------------------


def _setup_registry() -> None:
    from gameMechanic.chargephase import ChargePhaseHandler  # noqa: PLC0415
    from gameMechanic.commandPhase import CommandPhaseHandler  # noqa: PLC0415
    from gameMechanic.fightPhase import FightPhaseHandler  # noqa: PLC0415
    from gameMechanic.moralePhase import MoralePhaseHandler  # noqa: PLC0415
    from gameMechanic.movementPhase import MovementPhaseHandler  # noqa: PLC0415
    from gameMechanic.psychicPhase import PsychicPhaseHandler  # noqa: PLC0415
    from gameMechanic.shootingPhase import ShootingPhaseHandler  # noqa: PLC0415

    handlers: list[PhaseHandler] = [
        CommandPhaseHandler(),
        MovementPhaseHandler(),
        PsychicPhaseHandler(),
        ShootingPhaseHandler(),
        ChargePhaseHandler(),
        FightPhaseHandler(),
        MoralePhaseHandler(),
    ]
    for h in handlers:
        PHASE_REGISTRY[h.phase_name] = h


_setup_registry()
