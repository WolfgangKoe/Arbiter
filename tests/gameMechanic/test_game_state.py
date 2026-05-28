"""Tests for game_state.py: next_phase, phase transitions, round increments."""

import sys
from pathlib import Path
from unittest.mock import MagicMock

_st_mock = MagicMock()
sys.modules["streamlit"] = _st_mock
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

import gameMechanic.unit_mutations as _mut  # noqa: E402
from gameMechanic.game_state import next_phase  # noqa: E402


class _S(dict):
    def __getattr__(self, key: str):
        try:
            return self[key]
        except KeyError:
            raise AttributeError(key)

    def __setattr__(self, key: str, value: object) -> None:
        self[key] = value


def _make_session(**kwargs) -> _S:
    s = _S(**kwargs)
    _mut.st.session_state = s
    return s


def _unit_state_dict() -> dict:
    return {
        "current_wounds": 5,
        "models": 1,
        "destroyed": False,
        "in_melee": False,
        "in_reserve": False,
        "deployment": "stationary",
        "lost_models_this_turn": 0,
        "movement_choice": None,
        "melee_with": [],
        "turn_flags": {
            "advanced": False,
            "retreated": False,
            "charged": False,
            "shot": False,
            "fought": False,
        },
    }


def _phase_session(phase_idx: int, active: str, round_num: int = 1, cp: dict | None = None) -> _S:
    return _make_session(
        phase_idx=phase_idx,
        active=active,
        round=round_num,
        cp=cp if cp is not None else {"Necrons": 4, "Orks": 4},
        selected_unit=None,
        selected_targets=[],
        necron_units={"u1": _unit_state_dict()},
        ork_units={"u2": _unit_state_dict()},
    )


# ---------------------------------------------------------------------------
# next_phase — state transitions
# ---------------------------------------------------------------------------


def test_next_phase_setup_goes_to_command() -> None:
    session = _phase_session(phase_idx=0, active="Necrons")
    next_phase()
    assert session["phase_idx"] == 1


def test_next_phase_advances_index_within_turn() -> None:
    session = _phase_session(phase_idx=1, active="Necrons")
    next_phase()
    assert session["phase_idx"] == 2


def test_next_phase_switches_active_player_after_necrons_morale() -> None:
    session = _phase_session(phase_idx=7, active="Necrons")
    next_phase()
    assert session["active"] == "Orks"
    assert session["phase_idx"] == 1


def test_next_phase_increments_round_after_orks_morale() -> None:
    session = _phase_session(phase_idx=7, active="Orks", round_num=1)
    next_phase()
    assert session["active"] == "Necrons"
    assert session["round"] == 2


def test_next_phase_does_not_award_cp_on_player_switch() -> None:
    """CP is granted manually via the Command Phase button — next_phase must not add CP."""
    session = _phase_session(phase_idx=7, active="Orks", cp={"Necrons": 4, "Orks": 4})
    next_phase()
    assert session["cp"]["Necrons"] == 4
    assert session["cp"]["Orks"] == 4


def test_next_phase_resets_selected_unit_and_targets() -> None:
    session = _make_session(
        phase_idx=1,
        active="Necrons",
        round=1,
        cp={"Necrons": 4, "Orks": 4},
        selected_unit=("Necrons", "wh40k_9e.necrons.unit.overlord"),
        selected_targets=[("Orks", "wh40k_9e.orks.unit.big_mek")],
        necron_units={"u1": _unit_state_dict()},
        ork_units={"u2": _unit_state_dict()},
    )
    next_phase()
    assert session["selected_unit"] is None
    assert session["selected_targets"] == []
