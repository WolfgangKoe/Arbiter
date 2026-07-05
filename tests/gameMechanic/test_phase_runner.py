"""Tests for phase_runner.py — PHASE_REGISTRY and render_current_phase.

Tests verify that:
- All seven game phases are registered with their correct handler.
- render_current_phase() dispatches to the handler's render_active().
"""

from __future__ import annotations

import sys
from pathlib import Path
from unittest.mock import MagicMock, patch

_st_mock = MagicMock()
sys.modules.setdefault("streamlit", _st_mock)
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

import gameMechanic.phase_runner as _pr  # noqa: E402
from gameMechanic.phase_runner import PHASE_REGISTRY  # noqa: E402

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

    def test_all_handlers_have_render_active(self) -> None:
        for key, handler in PHASE_REGISTRY.items():
            assert callable(
                getattr(handler, "render_active", None)
            ), f"Missing render_active for '{key}'"


# ---------------------------------------------------------------------------
# render_current_phase — dispatcher
# ---------------------------------------------------------------------------


class TestRenderCurrentPhase:
    def test_warns_when_no_handler_registered(self) -> None:
        # phase_idx=0 → "setup" — not in PHASE_REGISTRY
        state = {
            "phase_idx": 0,
            "first_player": "Necrons",
            "second_player": "Orks",
        }
        with patch.object(_pr.st, "warning") as mock_warn:
            _pr.render_current_phase(state)
            mock_warn.assert_called_once()

    def test_calls_render_active(self) -> None:
        mock_handler = MagicMock()
        original = _pr.PHASE_REGISTRY.get("command")
        _pr.PHASE_REGISTRY["command"] = mock_handler
        try:
            state = {
                "phase_idx": 1,
                "first_player": "Necrons",
                "second_player": "Orks",
            }
            _pr.render_current_phase(state)
            mock_handler.render_active.assert_called_once_with(state)
        finally:
            _pr.PHASE_REGISTRY["command"] = original

    def test_does_not_fire_ability_hooks(self) -> None:
        """The dead start/end stage machinery is gone: the runner never calls
        ability hooks — get_triggered_abilities is not even imported anymore."""
        assert not hasattr(_pr, "get_triggered_abilities")
