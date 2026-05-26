"""detachmentCard — Detachment header + unit cards."""

import streamlit as st

from models import Unit
from uiLayout.unitCard import render_unit_card

_DETACHMENT_NAME = "Patrol Detachment"


def render_detachment_card(
    faction: str, units: list[Unit], states: dict  # type: ignore[type-arg]
) -> None:
    st.caption(_DETACHMENT_NAME)
    for unit in units:
        render_unit_card(unit, states[unit.uid], faction)
