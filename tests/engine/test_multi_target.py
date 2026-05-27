"""Tests for multi-target + melee tracking: enter_melee, leave_melee, set_charged,
selected_targets in session state, and movement_choice reset on turn end."""

import sys
from pathlib import Path
from unittest.mock import MagicMock

sys.modules["streamlit"] = MagicMock()
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

import engine  # noqa: E402
from engine import (  # noqa: E402
    enter_melee,
    leave_melee,
    next_phase,
    set_charged,
    set_movement_status,
)

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

OVERLORD = "wh40k_9e.necrons.unit.overlord"
WARRIORS = "wh40k_9e.necrons.unit.warriors"
BOYZ = "wh40k_9e.orks.unit.boyz"
WARBOSS = "wh40k_9e.orks.unit.warboss"


class _S(dict):
    def __getattr__(self, key: str):
        try:
            return self[key]
        except KeyError:
            raise AttributeError(key)

    def __setattr__(self, key: str, value: object) -> None:
        self[key] = value


def _unit() -> dict:
    return {
        "current_wounds": 5,
        "models": 1,
        "destroyed": False,
        "in_melee": False,
        "in_reserve": False,
        "deployment": "normal",
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


def _make_session(**kwargs) -> _S:  # type: ignore[no-untyped-def]
    s = _S(**kwargs)
    engine.st.session_state = s
    return s


def _two_unit_session() -> _S:
    return _make_session(
        necron_units={OVERLORD: _unit()},
        ork_units={BOYZ: _unit()},
        selected_targets=[],
        phase_idx=5,  # charge phase
        active="Necrons",
        round=1,
        cp={"Necrons": 4, "Orks": 4},
        selected_unit=None,
    )


def _four_unit_session() -> _S:
    return _make_session(
        necron_units={OVERLORD: _unit(), WARRIORS: _unit()},
        ork_units={BOYZ: _unit(), WARBOSS: _unit()},
        selected_targets=[],
        phase_idx=5,
        active="Necrons",
        round=1,
        cp={"Necrons": 4, "Orks": 4},
        selected_unit=None,
    )


# ---------------------------------------------------------------------------
# enter_melee
# ---------------------------------------------------------------------------


def test_enter_melee_registers_both_sides() -> None:
    session = _two_unit_session()
    enter_melee(OVERLORD, "Necrons", BOYZ, "Orks")
    assert BOYZ in session["necron_units"][OVERLORD]["melee_with"]
    assert OVERLORD in session["ork_units"][BOYZ]["melee_with"]


def test_enter_melee_sets_in_melee_true_for_both() -> None:
    session = _two_unit_session()
    enter_melee(OVERLORD, "Necrons", BOYZ, "Orks")
    assert session["necron_units"][OVERLORD]["in_melee"] is True
    assert session["ork_units"][BOYZ]["in_melee"] is True


def test_enter_melee_idempotent() -> None:
    """Calling enter_melee twice must not add duplicates."""
    session = _two_unit_session()
    enter_melee(OVERLORD, "Necrons", BOYZ, "Orks")
    enter_melee(OVERLORD, "Necrons", BOYZ, "Orks")
    assert session["necron_units"][OVERLORD]["melee_with"].count(BOYZ) == 1
    assert session["ork_units"][BOYZ]["melee_with"].count(OVERLORD) == 1


def test_enter_melee_multiple_enemies() -> None:
    """One attacker can enter melee with two targets."""
    session = _four_unit_session()
    enter_melee(OVERLORD, "Necrons", BOYZ, "Orks")
    enter_melee(OVERLORD, "Necrons", WARBOSS, "Orks")
    mw = session["necron_units"][OVERLORD]["melee_with"]
    assert BOYZ in mw
    assert WARBOSS in mw


# ---------------------------------------------------------------------------
# leave_melee
# ---------------------------------------------------------------------------


def test_leave_melee_clears_attacker_melee_with() -> None:
    session = _two_unit_session()
    enter_melee(OVERLORD, "Necrons", BOYZ, "Orks")
    leave_melee(OVERLORD, "Necrons")
    assert session["necron_units"][OVERLORD]["melee_with"] == []


def test_leave_melee_removes_from_enemy_melee_with() -> None:
    session = _two_unit_session()
    enter_melee(OVERLORD, "Necrons", BOYZ, "Orks")
    leave_melee(OVERLORD, "Necrons")
    assert OVERLORD not in session["ork_units"][BOYZ]["melee_with"]


def test_leave_melee_sets_in_melee_false_for_attacker() -> None:
    session = _two_unit_session()
    enter_melee(OVERLORD, "Necrons", BOYZ, "Orks")
    leave_melee(OVERLORD, "Necrons")
    assert session["necron_units"][OVERLORD]["in_melee"] is False


def test_leave_melee_sets_in_melee_false_for_enemy_when_no_other_engagements() -> None:
    session = _two_unit_session()
    enter_melee(OVERLORD, "Necrons", BOYZ, "Orks")
    leave_melee(OVERLORD, "Necrons")
    assert session["ork_units"][BOYZ]["in_melee"] is False


def test_leave_melee_enemy_stays_in_melee_if_still_engaged_elsewhere() -> None:
    """Boyz engaged with both Overlord and Warriors — Overlord retreating doesn't free Boyz."""
    session = _four_unit_session()
    enter_melee(OVERLORD, "Necrons", BOYZ, "Orks")
    enter_melee(WARRIORS, "Necrons", BOYZ, "Orks")
    leave_melee(OVERLORD, "Necrons")
    # Boyz still engaged with Warriors
    assert session["ork_units"][BOYZ]["in_melee"] is True
    assert WARRIORS in session["ork_units"][BOYZ]["melee_with"]


# ---------------------------------------------------------------------------
# set_charged
# ---------------------------------------------------------------------------


def test_set_charged_sets_charged_flag() -> None:
    session = _two_unit_session()
    set_charged(OVERLORD, "Necrons", BOYZ, "Orks")
    assert session["necron_units"][OVERLORD]["turn_flags"]["charged"] is True


def test_set_charged_enters_melee_for_both_units() -> None:
    session = _two_unit_session()
    set_charged(OVERLORD, "Necrons", BOYZ, "Orks")
    assert session["necron_units"][OVERLORD]["in_melee"] is True
    assert session["ork_units"][BOYZ]["in_melee"] is True
    assert BOYZ in session["necron_units"][OVERLORD]["melee_with"]
    assert OVERLORD in session["ork_units"][BOYZ]["melee_with"]


def test_set_charged_multiple_targets() -> None:
    """Charging two targets: both registered in melee_with."""
    session = _four_unit_session()
    set_charged(OVERLORD, "Necrons", BOYZ, "Orks")
    set_charged(OVERLORD, "Necrons", WARBOSS, "Orks")
    mw = session["necron_units"][OVERLORD]["melee_with"]
    assert BOYZ in mw
    assert WARBOSS in mw


# ---------------------------------------------------------------------------
# movement_choice via set_movement_status
# ---------------------------------------------------------------------------


def test_set_movement_status_sets_movement_choice() -> None:
    session = _two_unit_session()
    set_movement_status(OVERLORD, "Necrons", "advanced")
    assert session["necron_units"][OVERLORD]["movement_choice"] == "advanced"


def test_set_movement_status_advanced_sets_turn_flag() -> None:
    session = _two_unit_session()
    set_movement_status(OVERLORD, "Necrons", "advanced")
    assert session["necron_units"][OVERLORD]["turn_flags"]["advanced"] is True


def test_set_movement_status_normal_does_not_set_advanced_flag() -> None:
    session = _two_unit_session()
    set_movement_status(OVERLORD, "Necrons", "normal")
    assert session["necron_units"][OVERLORD]["turn_flags"]["advanced"] is False
    assert session["necron_units"][OVERLORD]["turn_flags"]["retreated"] is False


def test_set_movement_status_retreated_calls_leave_melee() -> None:
    """Retreating clears melee engagement."""
    session = _two_unit_session()
    enter_melee(OVERLORD, "Necrons", BOYZ, "Orks")
    set_movement_status(OVERLORD, "Necrons", "retreated")
    assert session["necron_units"][OVERLORD]["in_melee"] is False
    assert session["necron_units"][OVERLORD]["melee_with"] == []


# ---------------------------------------------------------------------------
# movement_choice reset on turn end
# ---------------------------------------------------------------------------


def test_reset_turn_state_clears_movement_choice() -> None:
    session = _make_session(
        necron_units={OVERLORD: {**_unit(), "movement_choice": "advanced"}},
        ork_units={BOYZ: {**_unit(), "movement_choice": "stationary"}},
        selected_targets=[],
        phase_idx=7,  # morale phase — triggers turn reset
        active="Necrons",
        round=1,
        cp={"Necrons": 4, "Orks": 4},
        selected_unit=None,
    )
    next_phase()
    assert session["necron_units"][OVERLORD]["movement_choice"] is None
    assert session["ork_units"][BOYZ]["movement_choice"] is None
