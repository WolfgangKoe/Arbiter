"""armyList — Full sidebar: army card + detachment cards."""

import streamlit as st

from gameMechanic.game_state import faction_dir_for, units_key_for, units_list_for
from gameObjects.loader import load_faction_abilities
from gameObjects.unit import Unit
from uiLayout.armyCard import render_army_card
from uiLayout.detachmentCard import render_detachment_card

_ABILITIES_CACHE: dict[str, list] = {}


def _faction_abilities_for(faction: str) -> list:
    faction_dir = faction_dir_for(faction)
    if faction_dir not in _ABILITIES_CACHE:
        _ABILITIES_CACHE[faction_dir] = load_faction_abilities(faction_dir)
    return _ABILITIES_CACHE[faction_dir]


def _units_for(faction: str) -> list[Unit]:
    return units_list_for(faction)


def _states_for(faction: str) -> dict:  # type: ignore[type-arg]
    return st.session_state[units_key_for(faction)]


def _subfaction_for(faction: str) -> str | None:
    units = _units_for(faction)
    if units:
        return units[0].subfaction
    return None


def render_army_list(faction: str) -> None:
    units = _units_for(faction)
    states = _states_for(faction)
    subfaction = _subfaction_for(faction)
    faction_abilities = _faction_abilities_for(faction)

    render_army_card(faction, subfaction, faction_abilities, units, states)
    render_detachment_card(faction, units, states)
