"""Tests for gameMechanic/commandPhase.py — pure logic only (no Streamlit UI)."""

import sys
from pathlib import Path
from unittest.mock import MagicMock

# Stub streamlit before importing commandPhase
_st_mock = MagicMock()
sys.modules["streamlit"] = _st_mock
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

import gameMechanic.game_state as _gs  # noqa: E402
from gameMechanic.commandPhase import resolve_command_start  # noqa: E402
from gameObjects.loader import load_army  # noqa: E402

# ---------------------------------------------------------------------------
# resolve_command_start — integration
# ---------------------------------------------------------------------------


class _S(dict):
    def __getattr__(self, key: str):  # type: ignore[override]
        try:
            return self[key]
        except KeyError:
            raise AttributeError(key)

    def __setattr__(self, key: str, value: object) -> None:
        self[key] = value


def _make_necron_state() -> dict:
    units, _ = load_army("necrons")
    session = _S(first_player="Necrons", p1_faction_dir="necrons", p2_faction_dir="necrons")
    _st_mock.session_state = session
    _gs.st.session_state = session
    return {
        "active": "Necrons",
        "first_player": "Necrons",
        "p1_units": {
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
    assert "wh40k_9e.necrons.faction.living_metal" in ids


def test_resolve_command_start_ork_returns_empty() -> None:
    units, _ = load_army("orks")
    session = _S(first_player="Necrons", p1_faction_dir="necrons", p2_faction_dir="orks")
    _st_mock.session_state = session
    _gs.st.session_state = session
    state = {
        "active": "Orks",
        "first_player": "Necrons",
        "p2_units": {
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
