"""Tests for moralePhase.py — Ziel 4h: threshold calculation and flee_models."""

from __future__ import annotations

import sys
from pathlib import Path
from unittest.mock import MagicMock, patch

sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

from gameMechanic.moralePhase import _fail_threshold
from gameMechanic.unit_mutations import flee_models

# ---------------------------------------------------------------------------
# _fail_threshold — pure-function tests
# ---------------------------------------------------------------------------


class TestFailThreshold:
    def test_typical_case(self):
        # Ld 7, lost 2 → fails on D6 >= 6
        assert _fail_threshold(7, 2) == 6

    def test_auto_pass_above_6(self):
        # Ld 7, lost 1 → threshold 7 → impossible to fail
        assert _fail_threshold(7, 1) == 7

    def test_always_fails_threshold_1(self):
        # Ld 7, lost 7 → threshold 1 → always fails
        assert _fail_threshold(7, 7) == 1

    def test_always_fails_threshold_below_1(self):
        # Ld 5, lost 8 → threshold -2 → always fails
        assert _fail_threshold(5, 8) == -2

    def test_fails_only_on_6(self):
        # Ld 10, lost 5 → fails on D6 >= 6
        assert _fail_threshold(10, 5) == 6

    def test_high_leadership_rarely_fails(self):
        # Ld 10, lost 1 → threshold 10 → impossible
        assert _fail_threshold(10, 1) == 10

    def test_low_leadership_many_losses(self):
        # Ld 4, lost 4 → threshold 1 → always fails
        assert _fail_threshold(4, 4) == 1


# ---------------------------------------------------------------------------
# flee_models — state mutation tests
# ---------------------------------------------------------------------------


def _make_unit(wounds: int = 1, models_max: int = 10) -> MagicMock:
    u = MagicMock()
    u.wounds = wounds
    u.models_max = models_max
    return u


def _make_state(models: int = 10, wounds_per_model: int = 1) -> dict:
    return {
        "current_wounds": models * wounds_per_model,
        "models": models,
        "destroyed": False,
        "fled_models_this_turn": 0,
        "turn_flags": {"morale_tested": False},
    }


def _necron_session(unit_state: dict) -> dict:
    return {"first_player": "Necrons", "p1_units": {"u1": unit_state}}


class TestFleeModels:
    def test_flee_reduces_models(self):
        unit_state = _make_state(models=10)
        unit = _make_unit(wounds=1, models_max=10)
        with (
            patch("gameMechanic.unit_mutations.st") as mock_st,
            patch("gameMechanic.game_state.st", mock_st),
        ):
            mock_st.session_state = _necron_session(unit_state)
            flee_models("u1", "Necrons", 3, unit)
        assert unit_state["models"] == 7
        assert unit_state["current_wounds"] == 7

    def test_flee_sets_fled_counter(self):
        unit_state = _make_state(models=10)
        unit = _make_unit(wounds=1, models_max=10)
        with (
            patch("gameMechanic.unit_mutations.st") as mock_st,
            patch("gameMechanic.game_state.st", mock_st),
        ):
            mock_st.session_state = _necron_session(unit_state)
            flee_models("u1", "Necrons", 2, unit)
        assert unit_state["fled_models_this_turn"] == 2

    def test_flee_marks_morale_tested(self):
        unit_state = _make_state(models=10)
        unit = _make_unit(wounds=1, models_max=10)
        with (
            patch("gameMechanic.unit_mutations.st") as mock_st,
            patch("gameMechanic.game_state.st", mock_st),
        ):
            mock_st.session_state = _necron_session(unit_state)
            flee_models("u1", "Necrons", 1, unit)
        assert unit_state["turn_flags"]["morale_tested"] is True

    def test_flee_all_models_marks_destroyed(self):
        unit_state = _make_state(models=3)
        unit = _make_unit(wounds=1, models_max=3)
        with (
            patch("gameMechanic.unit_mutations.st") as mock_st,
            patch("gameMechanic.game_state.st", mock_st),
        ):
            mock_st.session_state = _necron_session(unit_state)
            flee_models("u1", "Necrons", 3, unit)
        assert unit_state["destroyed"] is True
        assert unit_state["models"] == 0

    def test_flee_accumulates_across_calls(self):
        unit_state = _make_state(models=10)
        unit = _make_unit(wounds=1, models_max=10)
        with (
            patch("gameMechanic.unit_mutations.st") as mock_st,
            patch("gameMechanic.game_state.st", mock_st),
        ):
            mock_st.session_state = _necron_session(unit_state)
            flee_models("u1", "Necrons", 2, unit)
            flee_models("u1", "Necrons", 1, unit)
        assert unit_state["fled_models_this_turn"] == 3

    def test_flee_multi_wound_model(self):
        unit_state = _make_state(models=5, wounds_per_model=3)
        unit = _make_unit(wounds=3, models_max=5)
        with (
            patch("gameMechanic.unit_mutations.st") as mock_st,
            patch("gameMechanic.game_state.st", mock_st),
        ):
            mock_st.session_state = _necron_session(unit_state)
            flee_models("u1", "Necrons", 2, unit)
        assert unit_state["models"] == 3
        assert unit_state["current_wounds"] == 9
