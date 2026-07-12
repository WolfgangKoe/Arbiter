"""armyList — Full sidebar: army card + detachment cards."""

import streamlit as st

from gameMechanic.gameState import (
    faction_dir_for,
    unit_keys_for,
    units_key_for,
    units_list_for,
)
from gameObjects.loader import load_faction_abilities
from gameObjects.unit import Unit
from uiLayout.armyCard import render_army_card
from uiLayout.detachmentCard import render_detachment_card


def _faction_abilities_for(faction: str) -> list:
    faction_dir = faction_dir_for(faction)
    try:
        return load_faction_abilities(faction_dir)
    except Exception:
        return []


def _units_for(faction: str) -> list[Unit]:
    return units_list_for(faction)


def _states_for(faction: str) -> dict:  # type: ignore[type-arg]
    return st.session_state[units_key_for(faction)]


def render_army_list(faction: str) -> None:
    units = _units_for(faction)
    states = _states_for(faction)
    unit_keys = unit_keys_for(faction)
    faction_abilities = _faction_abilities_for(faction)

    render_army_card(faction, faction_abilities, units, states)
    render_detachment_card(faction, units, states, unit_keys)
