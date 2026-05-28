"""Game state — phase definitions, army loading, init / reset / next_phase."""

from __future__ import annotations

import streamlit as st

from gameObjects.loader import load_army
from gameObjects.unit import Unit

PHASES: list[tuple[str, str]] = [
    ("Setup", "setup"),
    ("Command", "command"),
    ("Movement", "movement"),
    ("Psychic", "psychic"),
    ("Shooting", "shooting"),
    ("Charge", "charge"),
    ("Fight", "fight"),
    ("Morale", "morale"),
]

_NECRON_UNITS = load_army("necrons")
_ORK_UNITS = load_army("orks")


def _unit_state(u: Unit) -> dict:  # type: ignore[type-arg]
    return {
        "current_wounds": u.wounds * u.models_max,
        "models": u.models_max,
        "destroyed": False,
        "in_melee": False,
        "in_reserve": False,
        "deployment": "stationary",
        "lost_models_this_turn": 0,
        "movement_choice": "stationary",
        "melee_with": [],
        "turn_flags": {
            "advanced": False,
            "retreated": False,
            "charged": False,
            "shot": False,
            "fought": False,
        },
        "my_will_be_done_active": False,
        "active_buffs": [],
        "models_lost_since_last_rp": 0,
    }


def init_state() -> None:
    if "initialized" in st.session_state:
        return
    st.session_state.initialized = True
    st.session_state.round = 1
    st.session_state.phase_idx = 0
    st.session_state.active = "Necrons"
    st.session_state.first_player = "Necrons"
    st.session_state.second_player = "Orks"
    st.session_state.cp = {"Necrons": 3, "Orks": 3}
    st.session_state.vp = {"Necrons": 0, "Orks": 0}
    st.session_state.selected_unit = None
    st.session_state.selected_targets = []
    st.session_state.resurrection_orb_used = False
    st.session_state.phase_stage = "active"
    st.session_state.active_effect = None
    st.session_state.cp_granted_this_phase = False
    st.session_state.mwbd_target_uid = None
    st.session_state.res_orb_target_uid = None
    st.session_state.necron_units = {u.id: _unit_state(u) for u in _NECRON_UNITS}
    st.session_state.ork_units = {u.id: _unit_state(u) for u in _ORK_UNITS}
    st.session_state.active_protocol_id = "eternal_guardian"
    st.session_state.used_protocol_ids = ["eternal_guardian"]


def reset_game() -> None:
    from gameMechanic.game_log import clear_game_log  # noqa: PLC0415

    clear_game_log()
    for k in list(st.session_state.keys()):
        del st.session_state[k]


def _reset_phase_state() -> None:
    st.session_state.cp_granted_this_phase = False


def _reset_turn_state() -> None:
    for key in ("necron_units", "ork_units"):
        for state in st.session_state[key].values():
            flags = state["turn_flags"]
            for flag in flags:
                flags[flag] = False
            state["lost_models_this_turn"] = 0
            state["movement_choice"] = "stationary"
            state["my_will_be_done_active"] = False
    st.session_state.active_protocol_id = None


def next_phase() -> None:
    idx = st.session_state.phase_idx
    num = len(PHASES)

    if idx == 0:  # Setup → first Command phase
        st.session_state.phase_idx = 1
        _reset_phase_state()
    elif idx >= num - 1:  # Morale done → switch player
        if st.session_state.active == "Necrons":
            st.session_state.active = "Orks"
        else:
            st.session_state.active = "Necrons"
            st.session_state.round += 1
        _reset_turn_state()
        _reset_phase_state()
        st.session_state.phase_idx = 1
    else:
        st.session_state.phase_idx = idx + 1
        _reset_phase_state()

    st.session_state.selected_unit = None
    st.session_state.selected_targets = []
