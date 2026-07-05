"""Phase runner — central dispatcher for all game phases.

PHASE_REGISTRY maps phase_key → PhaseHandler instance.
render_current_phase(state) is the single entry point called by gameActionsArea.
"""

from __future__ import annotations

import streamlit as st

from gameMechanic.phase_handler import PhaseHandler

# ---------------------------------------------------------------------------
# Registry
# ---------------------------------------------------------------------------

PHASE_REGISTRY: dict[str, PhaseHandler] = {}


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------


def render_current_phase(state: dict) -> None:  # type: ignore[type-arg]
    """Look up the handler for the current phase and render it."""
    from gameMechanic.game_state import PHASES  # noqa: PLC0415

    phase_key: str = PHASES[state["phase_idx"]][1]
    handler = PHASE_REGISTRY.get(phase_key)
    if handler is None:
        st.warning(f"Phase '{phase_key}' has no registered handler.")
        return

    handler.render_active(state)


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
