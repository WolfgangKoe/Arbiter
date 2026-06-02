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

CP_BY_GAME_SIZE: dict[str, int] = {
    "Combat Patrol": 3,
    "Incursion": 6,
    "Strike Force": 12,
    "Onslaught": 18,
}


# ---------------------------------------------------------------------------
# Roster loading helper
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


def list_available_rosters() -> list[str]:
    """Return all .yaml filenames in the rosters directory."""
    return sorted(p.name for p in _ROSTER_DIR.glob("*.yaml"))


# ---------------------------------------------------------------------------
# Player-slot helpers  (require Streamlit session state to be active)
# ---------------------------------------------------------------------------


def units_key_for(player: str) -> str:
    """Return the session_state key that holds a player's unit states."""
    return "p1_units" if player == st.session_state.get("first_player") else "p2_units"


def faction_dir_for(player: str) -> str:
    """Return the data-directory name for a player's faction."""
    if player == st.session_state.get("first_player"):
        return st.session_state.get("p1_faction_dir", "necrons")
    return st.session_state.get("p2_faction_dir", "necrons")


def is_necron_faction(player: str) -> bool:
    """True when the player's faction uses Necron rules (command protocols etc.)."""
    return faction_dir_for(player) == "necrons"


def units_list_for(player: str) -> list[Unit]:
    """Return the Unit-definition list for a player (for stats / name lookups)."""
    if player == st.session_state.get("first_player"):
        return st.session_state.get("p1_units_list", [])
    return st.session_state.get("p2_units_list", [])


def unit_keys_for(player: str) -> list[str]:
    """Return the ordered list of state-dict keys for a player's units.

    Matches the order of units_list_for(). For duplicate unit IDs a '#N' suffix
    is appended (e.g. 'wh40k_9e.necrons.unit.warriors#1' for the second squad).
    """
    if player == st.session_state.get("first_player"):
        return st.session_state.get("p1_unit_keys", [])
    return st.session_state.get("p2_unit_keys", [])


def unit_id_from_state_key(state_key: str) -> str:
    """Strip the deduplication suffix from a state key to get the canonical unit ID.

    'wh40k_9e.necrons.unit.warriors#1' → 'wh40k_9e.necrons.unit.warriors'
    """
    return state_key.split("#")[0]


# ---------------------------------------------------------------------------
# Session state helpers
# ---------------------------------------------------------------------------


def _make_unit_state_dict(
    matched: list[tuple[Unit, int]],
) -> tuple[dict, list[str]]:  # type: ignore[type-arg]
    """Build the state dict and ordered key list for a matched unit list.

    Duplicate unit IDs are disambiguated with a '#N' suffix so each unit
    instance has its own independent state.
    """
    counts: dict[str, int] = {}
    state_dict: dict[str, dict] = {}  # type: ignore[type-arg]
    keys: list[str] = []
    for u, m in matched:
        n = counts.get(u.id, 0)
        counts[u.id] = n + 1
        key = u.id if n == 0 else f"{u.id}#{n}"
        state_dict[key] = _unit_state(u, m)
        keys.append(key)
    return state_dict, keys


def _unit_state(u: Unit, models: int | None = None) -> dict:  # type: ignore[type-arg]
    count = min(models, u.models_max) if models is not None else u.models_max
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


def init_state(
    roster_p1: str = "necrons_alpha.yaml",
    roster_p2: str = "necrons_beta.yaml",
    game_size: str = "Incursion",
    vp_phase: str = "Morale",
    vp_from_round: int = 1,
    game_mode: str = "matched",
    mission: str | None = None,
    attacker: str | None = None,
    use_secondaries: bool = False,
    secondaries: dict | None = None,  # type: ignore[type-arg]
    secondary_vp: dict | None = None,  # type: ignore[type-arg]
) -> None:
    if "initialized" in st.session_state:
        return

    p1_matched, p1_unmatched, p1_name, p1_faction_dir = _load_roster_for(roster_p1, "necrons")
    p2_matched, p2_unmatched, p2_name, p2_faction_dir = _load_roster_for(roster_p2, "necrons")

    starting_cp = CP_BY_GAME_SIZE.get(game_size, 3) if game_mode == "matched" else 3

    st.session_state.initialized = True
    st.session_state.round = 1
    st.session_state.phase_idx = 0
    st.session_state.first_player = p1_name
    st.session_state.second_player = p2_name
    st.session_state.active = p1_name
    st.session_state.cp = {p1_name: starting_cp, p2_name: starting_cp}
    st.session_state.vp = {p1_name: 0, p2_name: 0}
    st.session_state.selected_unit = None
    st.session_state.selected_targets = []
    st.session_state.resurrection_orb_used = False
    st.session_state.phase_stage = "active"
    st.session_state.active_effect = None
    st.session_state.cp_granted_this_phase = False
    st.session_state.mwbd_target_uid = None
    st.session_state.res_orb_target_uid = None

    # Unit lists for stat/name lookups (indexed by player slot, not faction)
    st.session_state.p1_units_list = [u for u, _ in p1_matched]
    st.session_state.p2_units_list = [u for u, _ in p2_matched]
    st.session_state.p1_faction_dir = p1_faction_dir
    st.session_state.p2_faction_dir = p2_faction_dir

    p1_states, p1_keys = _make_unit_state_dict(p1_matched)
    p2_states, p2_keys = _make_unit_state_dict(p2_matched)
    st.session_state.p1_units = p1_states
    st.session_state.p2_units = p2_states
    st.session_state.p1_unit_keys = p1_keys
    st.session_state.p2_unit_keys = p2_keys

    st.session_state.vp_phase = vp_phase
    st.session_state.vp_from_round = vp_from_round

    # Game configuration
    st.session_state.game_mode = game_mode
    st.session_state.game_size = game_size
    st.session_state.mission = mission
    st.session_state.attacker = attacker
    st.session_state.use_secondaries = use_secondaries
    st.session_state.secondaries = secondaries
    st.session_state.secondary_vp = secondary_vp

    st.session_state.active_protocol_id = "eternal_guardian"
    st.session_state.used_protocol_ids = ["eternal_guardian"]
    st.session_state.psi_attempts_this_phase = 0
    if p1_unmatched or p2_unmatched:
        st.session_state.roster_warnings = {
            p1_name: p1_unmatched,
            p2_name: p2_unmatched,
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
    for key in ("p1_units", "p2_units"):
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
