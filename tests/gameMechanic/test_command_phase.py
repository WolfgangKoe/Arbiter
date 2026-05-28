"""Tests for gameMechanic/commandPhase.py — pure logic only (no Streamlit UI)."""

import sys
from pathlib import Path
from unittest.mock import MagicMock

# Stub streamlit before importing commandPhase
_st_mock = MagicMock()
sys.modules["streamlit"] = _st_mock
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

from gameMechanic.commandPhase import resolve_command_start  # noqa: E402
from gameObjects.loader import load_army  # noqa: E402

# ---------------------------------------------------------------------------
# resolve_command_start — integration
# ---------------------------------------------------------------------------


def _make_necron_state() -> dict:
    units = load_army("necrons")
    return {
        "active": "Necrons",
        "necron_units": {
            u.id: {
                "current_wounds": max(1, u.wounds * u.models_max - 1),  # 1 wound below max
                "models": u.models_max,
                "destroyed": False,
            }
            for u in units
        },
    }


def test_resolve_command_start_returns_living_metal() -> None:
    state = _make_necron_state()
    triggered = resolve_command_start(state)
    ids = [a.id for a, _ in triggered]
    assert "necrons.faction.living_metal" in ids


def test_resolve_command_start_ork_returns_empty() -> None:
    units = load_army("orks")
    state = {
        "active": "Orks",
        "ork_units": {
            u.id: {
                "current_wounds": u.wounds * u.models_max,
                "models": u.models_max,
                "destroyed": False,
            }
            for u in units
        },
    }
    triggered = resolve_command_start(state)
    assert triggered == []
