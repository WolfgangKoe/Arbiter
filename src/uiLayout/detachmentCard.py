"""detachmentCard — Detachment header + unit cards."""

import streamlit as st

from gameObjects.unit import Unit
from uiLayout.unitCard import render_unit_card

_DETACHMENT_NAME = "Patrol Detachment"


def render_detachment_card(
    faction: str,
    units: list[Unit],
    states: dict,  # type: ignore[type-arg]
    unit_keys: list[str] | None = None,
) -> None:
    st.caption(_DETACHMENT_NAME)
    keys = unit_keys if unit_keys is not None else [u.id for u in units]
    for unit, state_key in zip(units, keys):
        render_unit_card(unit, states[state_key], faction, state_key=state_key)
