"""detachmentCard — Detachment header + unit cards."""

import streamlit as st

from gameMechanic.gameState import PHASES, pinned_explode_target_keys, sort_units_pinned_first
from gameObjects.unit import Unit
from uiLayout.unitCard import render_unit_card

_DETACHMENT_NAME = "Patrol Detachment"

_HANDLED_PHASES = {"movement", "shooting", "psychic", "charge", "fight"}


def _is_handled(state: dict, phase_key: str) -> bool:  # type: ignore[type-arg]
    if phase_key not in _HANDLED_PHASES:
        return False
    if phase_key == "movement":
        return bool(state.get("movement_chosen", False))
    return bool(
        state.get("turn_flags", {}).get(
            {"shooting": "shot", "psychic": "cast", "charge": "charged", "fight": "fought"}[
                phase_key
            ],
            False,
        )
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
    sorted_units = [p[0] for p in pairs]
    sorted_keys = [p[1] for p in pairs]
    # Sort-to-top (design_system.md §1.7): a unit currently checked in the
    # explode Multi-Unit-Ziel-Auswahl-Panel always wins the top slot,
    # regardless of the turn-flag sort above.
    pinned_keys = pinned_explode_target_keys(faction)
    if pinned_keys:
        sorted_units, sorted_keys = sort_units_pinned_first(sorted_units, sorted_keys, pinned_keys)
    for unit, state_key in zip(sorted_units, sorted_keys):
        render_unit_card(unit, states[state_key], faction, state_key=state_key)
