"""armyList — Full sidebar: army card + detachment cards."""

import streamlit as st

from gameMechanic.game_state import _NECRON_UNITS, _ORK_UNITS
from gameObjects.ability import Ability
from gameObjects.loader import load_faction_abilities
from gameObjects.unit import Unit
from uiLayout.armyCard import render_army_card
from uiLayout.detachmentCard import render_detachment_card

_FACTION_DIR: dict[str, str] = {
    "Necrons": "necrons",
    "Orks": "orks",
}

_FACTION_ABILITIES: dict[str, list[Ability]] = {
    faction: load_faction_abilities(faction_dir) for faction, faction_dir in _FACTION_DIR.items()
}


def _units_for(faction: str) -> list[Unit]:
    return _NECRON_UNITS if faction == "Necrons" else _ORK_UNITS


def _states_for(faction: str) -> dict:  # type: ignore[type-arg]
    key = "necron_units" if faction == "Necrons" else "ork_units"
    return st.session_state[key]


def _subfaction_for(faction: str) -> str | None:
    units = _units_for(faction)
    if units:
        return units[0].subfaction
    return None


def render_army_list(faction: str) -> None:
    units = _units_for(faction)
    states = _states_for(faction)
    subfaction = _subfaction_for(faction)
    faction_abilities = _FACTION_ABILITIES.get(faction, [])

    render_army_card(faction, subfaction, faction_abilities, units, states)
    render_detachment_card(faction, units, states)
