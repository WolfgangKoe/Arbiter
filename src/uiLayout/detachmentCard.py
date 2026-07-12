"""detachmentCard — Detachment header + unit cards."""

import streamlit as st

from gameMechanic.gameState import PHASES
from gameObjects.unit import Unit
from uiLayout.unitCard import render_unit_card

_DETACHMENT_NAME = "Patrol Detachment"

_HANDLED_PHASES = {"movement", "shooting", "psychic", "charge", "fight"}


def _is_handled(state: dict, phase_key: str) -> bool:  # type: ignore[type-arg]
    if phase_key not in _HANDLED_PHASES:
        return False
    if phase_key == "movement":
        return state.get("movement_chosen", False)
    return state.get("turn_flags", {}).get(
        {"shooting": "shot", "psychic": "cast", "charge": "charged", "fight": "fought"}[phase_key],
        False,
    )


def render_detachment_card(
    faction: str,
    units: list[Unit],
    states: dict,  # type: ignore[type-arg]
    unit_keys: list[str] | None = None,
) -> None:
    st.caption(_DETACHMENT_NAME)
    keys = unit_keys if unit_keys is not None else [u.id for u in units]
    phase_key = PHASES[st.session_state.get("phase_idx", 0)][1]
    pairs = sorted(
        zip(units, keys),
        key=lambda p: _is_handled(states.get(p[1], {}), phase_key),
    )
    for unit, state_key in pairs:
        render_unit_card(unit, states[state_key], faction, state_key=state_key)
