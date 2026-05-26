"""armyList — Full sidebar: army card + detachment cards."""

import streamlit as st

from models import NECRON_UNITS, ORK_UNITS, Unit
from uiLayout.armyCard import render_army_card
from uiLayout.detachmentCard import render_detachment_card


def _units_for(faction: str) -> list[Unit]:
    return NECRON_UNITS if faction == "Necrons" else ORK_UNITS


def _states_for(faction: str) -> dict:  # type: ignore[type-arg]
    key = "necron_units" if faction == "Necrons" else "ork_units"
    return st.session_state[key]


def render_army_list(faction: str) -> None:
    render_army_card(faction)
    units = _units_for(faction)
    states = _states_for(faction)
    render_detachment_card(faction, units, states)
