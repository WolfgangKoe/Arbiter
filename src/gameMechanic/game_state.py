"""Game state — phase definitions, army loading, init / reset / next_phase."""

from __future__ import annotations

from pathlib import Path

import streamlit as st

from gameObjects.loader import (
    load_roster,
    load_roster_metadata,
    load_unit_catalog,
)
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

_ROSTER_DIR = Path(__file__).parent.parent.parent / "data" / "rosters"

# ---------------------------------------------------------------------------
# Module-level roster loading (runs once per worker process)
# ---------------------------------------------------------------------------


def _load_roster_for(
    roster_file: str,
    fallback_faction: str,
) -> tuple[list[tuple[Unit, int]], list[str], str, str]:
    """Load a roster; fall back to full catalog if file is missing.

    Returns (matched_entries, unmatched_ids, display_name, faction_dir).
    """
    path = _ROSTER_DIR / roster_file
    meta = load_roster_metadata(path)
    faction_dir = meta.get("faction_dir") or fallback_faction
    display_name = meta.get("display_name") or roster_file

    catalog = load_unit_catalog(faction_dir)
    if path.exists():
        matched, unmatched = load_roster(path, catalog)
    else:
        matched = [(u, u.models_max) for u in catalog.values()]
        unmatched = []
    return matched, unmatched, display_name, faction_dir


_P1_MATCHED, _P1_UNMATCHED, _P1_NAME, _P1_FACTION_DIR = _load_roster_for(
    "necrons_alpha.yaml", "necrons"
)
_P2_MATCHED, _P2_UNMATCHED, _P2_NAME, _P2_FACTION_DIR = _load_roster_for(
    "necrons_beta.yaml", "necrons"
)

# Unit lists used by UI/stats lookups (order matches player slot)
_NECRON_UNITS: list[Unit] = [u for u, _ in _P1_MATCHED]
_ORK_UNITS: list[Unit] = [u for u, _ in _P2_MATCHED]

# Player-name → faction directory  (populated at init, used by helpers below)
PLAYER_FACTION_DIR: dict[str, str] = {
    _P1_NAME: _P1_FACTION_DIR,
    _P2_NAME: _P2_FACTION_DIR,
}


# ---------------------------------------------------------------------------
# Player-slot helpers  (require Streamlit session state to be active)
# ---------------------------------------------------------------------------


def units_key_for(player: str) -> str:
    """Return the session_state key that holds a player's unit states."""
    return "necron_units" if player == st.session_state.get("first_player") else "ork_units"


def faction_dir_for(player: str) -> str:
    """Return the data-directory name for a player's faction."""
    return PLAYER_FACTION_DIR.get(player, "necrons")


def is_necron_faction(player: str) -> bool:
    """True when the player's faction uses Necron rules (command protocols etc.)."""
    return faction_dir_for(player) == "necrons"


def units_list_for(player: str) -> list[Unit]:
    """Return the Unit-definition list for a player (for stats / name lookups)."""
    return _NECRON_UNITS if player == st.session_state.get("first_player") else _ORK_UNITS


# ---------------------------------------------------------------------------
# Session state helpers
# ---------------------------------------------------------------------------


def _unit_state(u: Unit, models: int | None = None) -> dict:  # type: ignore[type-arg]
    count = models if models is not None else u.models_max
    return {
        "current_wounds": u.wounds * count,
        "models": count,
        "models_initial": count,
        "destroyed": False,
        "in_melee": False,
        "in_reserve": False,
        "deployment": "stationary",
        "lost_models_this_turn": 0,
        "fled_models_this_turn": 0,
        "movement_choice": "stationary",
        "melee_with": [],
        "turn_flags": {
            "advanced": False,
            "retreated": False,
            "charged": False,
            "shot": False,
            "fought": False,
            "cast": False,
            "heroic_intervened": False,
            "morale_tested": False,
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
    st.session_state.first_player = _P1_NAME
    st.session_state.second_player = _P2_NAME
    st.session_state.active = _P1_NAME
    st.session_state.cp = {_P1_NAME: 3, _P2_NAME: 3}
    st.session_state.vp = {_P1_NAME: 0, _P2_NAME: 0}
    st.session_state.selected_unit = None
    st.session_state.selected_targets = []
    st.session_state.resurrection_orb_used = False
    st.session_state.phase_stage = "active"
    st.session_state.active_effect = None
    st.session_state.cp_granted_this_phase = False
    st.session_state.mwbd_target_uid = None
    st.session_state.res_orb_target_uid = None
    st.session_state.necron_units = {u.id: _unit_state(u, m) for u, m in _P1_MATCHED}
    st.session_state.ork_units = {u.id: _unit_state(u, m) for u, m in _P2_MATCHED}
    st.session_state.active_protocol_id = "eternal_guardian"
    st.session_state.used_protocol_ids = ["eternal_guardian"]
    st.session_state.psi_attempts_this_phase = 0
    if _P1_UNMATCHED or _P2_UNMATCHED:
        st.session_state.roster_warnings = {
            _P1_NAME: _P1_UNMATCHED,
            _P2_NAME: _P2_UNMATCHED,
        }
    else:
        st.session_state.roster_warnings = {}


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
            state["fled_models_this_turn"] = 0
            state["movement_choice"] = "stationary"
            state["my_will_be_done_active"] = False
    st.session_state.active_protocol_id = None


def next_phase() -> None:
    idx = st.session_state.phase_idx
    num = len(PHASES)
    first = st.session_state.first_player
    second = st.session_state.second_player

    if idx == 0:  # Setup → first Command phase
        st.session_state.phase_idx = 1
        _reset_phase_state()
    elif idx >= num - 1:  # Morale done → switch player
        st.session_state.active = second if st.session_state.active == first else first
        st.session_state.round += 1 if st.session_state.active == first else 0
        _reset_turn_state()
        _reset_phase_state()
        st.session_state.phase_idx = 1
    else:
        st.session_state.phase_idx = idx + 1
        _reset_phase_state()

    st.session_state.selected_unit = None
    st.session_state.selected_targets = []
    st.session_state.psi_result = None
    st.session_state.psychic_denies_used = {}
    st.session_state.psi_attempts_this_phase = 0
