"""Tests for phase_runner.py — PHASE_REGISTRY and advance_stage.

Tests verify that:
- All seven game phases are registered with their correct handler.
- advance_stage() progresses the phase_stage correctly.
"""

from __future__ import annotations

import sys
from pathlib import Path
from unittest.mock import MagicMock

_st_mock = MagicMock()
sys.modules.setdefault("streamlit", _st_mock)
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

import gameMechanic.game_state as _gs  # noqa: E402
import gameMechanic.phase_runner as _pr  # noqa: E402
from gameMechanic.phase_runner import PHASE_REGISTRY, advance_stage  # noqa: E402

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


class _S(dict):
    def __getattr__(self, key: str):
        try:
            return self[key]
        except KeyError:
            raise AttributeError(key)

    def __setattr__(self, key: str, value: object) -> None:
        self[key] = value


def _unit_state() -> dict:
    return {
        "current_wounds": 5,
        "models": 1,
        "models_initial": 1,
        "destroyed": False,
        "in_melee": False,
        "in_reserve": False,
        "deployment": "stationary",
        "lost_models_this_turn": 0,
        "fled_models_this_turn": 0,
        "movement_choice": "stationary",
        "movement_chosen": False,
        "melee_with": [],
        "active_buffs": [],
        "models_lost_since_last_rp": 0,
        "group_models": {},
        "turn_flags": {
            "advanced": False,
            "retreated": False,
            "charged": False,
            "shot": False,
            "fought": False,
            "cast": False,
            "heroic_intervened": False,
            "morale_tested": False,
            "movement_locked": False,
            "mortal_effect_applied": False,
        },
    }


def _make_session(phase_idx: int = 1, stage: str = "active") -> _S:
    s = _S(
        first_player="Necrons",
        second_player="Orks",
        phase_idx=phase_idx,
        phase_stage=stage,
        active="Necrons",
        round=1,
        cp={"Necrons": 6, "Orks": 6},
        selected_unit=None,
        selected_targets=[],
        p1_units={"u1": _unit_state()},
        p2_units={"u2": _unit_state()},
        p1_faction_dir="necrons",
        p2_faction_dir="orks",
    )
    _pr.st.session_state = s
    _gs.st.session_state = s
    return s


# ---------------------------------------------------------------------------
# PHASE_REGISTRY
# ---------------------------------------------------------------------------


class TestPhaseRegistry:
    def test_all_seven_phase_keys_registered(self) -> None:
        expected = {"command", "movement", "psychic", "shooting", "charge", "fight", "morale"}
        assert expected == set(PHASE_REGISTRY.keys())

    def test_each_handler_reports_correct_phase_name(self) -> None:
        for key, handler in PHASE_REGISTRY.items():
            assert handler.phase_name == key, f"Handler for '{key}' reports wrong phase_name"

    def test_all_handlers_have_render_start(self) -> None:
        for key, handler in PHASE_REGISTRY.items():
            assert callable(
                getattr(handler, "render_start", None)
            ), f"Missing render_start for '{key}'"

    def test_all_handlers_have_render_active(self) -> None:
        for key, handler in PHASE_REGISTRY.items():
            assert callable(
                getattr(handler, "render_active", None)
            ), f"Missing render_active for '{key}'"

    def test_all_handlers_have_render_end(self) -> None:
        for key, handler in PHASE_REGISTRY.items():
            assert callable(getattr(handler, "render_end", None)), f"Missing render_end for '{key}'"


# ---------------------------------------------------------------------------
# advance_stage
# ---------------------------------------------------------------------------


# ---------------------------------------------------------------------------
# render_current_phase — dispatcher (lines 30-44)
# ---------------------------------------------------------------------------


class TestRenderCurrentPhase:
    def test_warns_when_no_handler_registered(self) -> None:
        from unittest.mock import patch  # noqa: PLC0415

        # phase_idx=0 → "setup" — not in PHASE_REGISTRY
        state = {
            "phase_idx": 0,
            "phase_stage": "active",
            "first_player": "Necrons",
            "second_player": "Orks",
        }
        with patch.object(_pr.st, "warning") as mock_warn:
            _pr.render_current_phase(state)
            mock_warn.assert_called_once()

    def test_calls_render_active_for_active_stage(self) -> None:
        from unittest.mock import patch  # noqa: PLC0415

        mock_handler = MagicMock()
        original = _pr.PHASE_REGISTRY.get("command")
        _pr.PHASE_REGISTRY["command"] = mock_handler
        try:
            state = {
                "phase_idx": 1,
                "phase_stage": "active",
                "first_player": "Necrons",
                "second_player": "Orks",
            }
            with patch("gameMechanic.phase_runner.get_triggered_abilities"):
                _pr.render_current_phase(state)
            mock_handler.render_active.assert_called_once_with(state)
        finally:
            _pr.PHASE_REGISTRY["command"] = original

    def test_calls_render_start_for_start_stage(self) -> None:
        from unittest.mock import patch  # noqa: PLC0415

        mock_handler = MagicMock()
        original = _pr.PHASE_REGISTRY.get("command")
        _pr.PHASE_REGISTRY["command"] = mock_handler
        try:
            state = {
                "phase_idx": 1,
                "phase_stage": "start",
                "first_player": "Necrons",
                "second_player": "Orks",
            }
            with patch("gameMechanic.phase_runner.get_triggered_abilities"):
                _pr.render_current_phase(state)
            mock_handler.render_start.assert_called_once_with(state)
        finally:
            _pr.PHASE_REGISTRY["command"] = original

    def test_calls_render_end_for_end_stage(self) -> None:
        from unittest.mock import patch  # noqa: PLC0415

        mock_handler = MagicMock()
        original = _pr.PHASE_REGISTRY.get("command")
        _pr.PHASE_REGISTRY["command"] = mock_handler
        try:
            state = {
                "phase_idx": 1,
                "phase_stage": "end",
                "first_player": "Necrons",
                "second_player": "Orks",
            }
            with patch("gameMechanic.phase_runner.get_triggered_abilities"):
                _pr.render_current_phase(state)
            mock_handler.render_end.assert_called_once_with(state)
        finally:
            _pr.PHASE_REGISTRY["command"] = original

    def test_fires_triggered_abilities_on_start_stage(self) -> None:
        from unittest.mock import patch  # noqa: PLC0415

        mock_handler = MagicMock()
        original = _pr.PHASE_REGISTRY.get("command")
        _pr.PHASE_REGISTRY["command"] = mock_handler
        try:
            state = {
                "phase_idx": 1,
                "phase_stage": "start",
                "first_player": "Necrons",
                "second_player": "Orks",
            }
            with patch("gameMechanic.phase_runner.get_triggered_abilities") as mock_ga:
                _pr.render_current_phase(state)
                mock_ga.assert_called_once_with(state, "command", "phase_start")
        finally:
            _pr.PHASE_REGISTRY["command"] = original

    def test_fires_triggered_abilities_on_end_stage(self) -> None:
        from unittest.mock import patch  # noqa: PLC0415

        mock_handler = MagicMock()
        original = _pr.PHASE_REGISTRY.get("movement")
        _pr.PHASE_REGISTRY["movement"] = mock_handler
        try:
            state = {
                "phase_idx": 2,
                "phase_stage": "end",
                "first_player": "Necrons",
                "second_player": "Orks",
            }
            with patch("gameMechanic.phase_runner.get_triggered_abilities") as mock_ga:
                _pr.render_current_phase(state)
                mock_ga.assert_called_once_with(state, "movement", "phase_end")
        finally:
            _pr.PHASE_REGISTRY["movement"] = original

    def test_does_not_fire_triggered_abilities_on_active_stage(self) -> None:
        from unittest.mock import patch  # noqa: PLC0415

        mock_handler = MagicMock()
        original = _pr.PHASE_REGISTRY.get("command")
        _pr.PHASE_REGISTRY["command"] = mock_handler
        try:
            state = {
                "phase_idx": 1,
                "phase_stage": "active",
                "first_player": "Necrons",
                "second_player": "Orks",
            }
            with patch("gameMechanic.phase_runner.get_triggered_abilities") as mock_ga:
                _pr.render_current_phase(state)
                mock_ga.assert_not_called()
        finally:
            _pr.PHASE_REGISTRY["command"] = original


class TestAdvanceStage:
    def test_start_transitions_to_active(self) -> None:
        s = _make_session(stage="start")
        advance_stage(s)
        assert s["phase_stage"] == "active"

    def test_active_transitions_to_end(self) -> None:
        s = _make_session(stage="active")
        advance_stage(s)
        assert s["phase_stage"] == "end"

    def test_end_resets_to_active_and_increments_phase(self) -> None:
        s = _make_session(phase_idx=1, stage="end")
        advance_stage(s)
        assert s["phase_stage"] == "active"
        assert s["phase_idx"] == 2

    def test_end_at_last_phase_switches_active_player(self) -> None:
        s = _make_session(phase_idx=7, stage="end")
        advance_stage(s)
        assert s["active"] == "Orks"
        assert s["phase_idx"] == 1

    def test_end_of_orks_turn_increments_round(self) -> None:
        s = _make_session(phase_idx=7, stage="end")
        s["active"] = "Orks"
        advance_stage(s)
        assert s["active"] == "Necrons"
        assert s["round"] == 2
