"""Tests for gameMechanic/commandPhase.py — pure logic only (no Streamlit UI)."""

import sys
from pathlib import Path
from unittest.mock import MagicMock

# Stub streamlit before importing commandPhase
_st_mock = MagicMock()
sys.modules["streamlit"] = _st_mock
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

import gameMechanic.game_state as _gs  # noqa: E402
from gameMechanic.commandPhase import (  # noqa: E402
    can_gain_command_point,
    resolve_command_start,
    resolve_gain_cp_roll,
)
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


# ---------------------------------------------------------------------------
# R-CMD-03 — can_gain_command_point (Battle-forged gate)
# ---------------------------------------------------------------------------


class TestCanGainCommandPoint:
    def test_matched_play_is_battle_forged(self) -> None:
        """Matched Play armies are Battle-forged → CP grant allowed."""
        assert can_gain_command_point("matched") is True

    def test_crusade_is_battle_forged(self) -> None:
        """Crusade armies are also Battle-forged → CP grant allowed."""
        assert can_gain_command_point("crusade") is True

    def test_open_play_is_not_battle_forged(self) -> None:
        """Open Play armies are Unbound → CP grant must be blocked."""
        assert can_gain_command_point("open") is False

    def test_unknown_mode_is_not_battle_forged(self) -> None:
        """Unexpected game_mode values are treated as non-Battle-forged."""
        assert can_gain_command_point("unknown") is False


# ---------------------------------------------------------------------------
# R-CMD-11 — resolve_gain_cp_roll (gain_cp_roll resolution + once-per-phase lock)
# ---------------------------------------------------------------------------


class TestResolveGainCpRoll:
    def test_success_returns_cp_delta(self) -> None:
        """Roll at/above threshold → active side gains `amount` CP and phase locks."""
        cp_delta, locked = resolve_gain_cp_roll(amount=1, roll_succeeded=True, already_rolled=False)
        assert cp_delta == 1
        assert locked is True

    def test_failure_returns_zero_but_locks(self) -> None:
        """Roll below threshold → no CP gained, but phase is still locked."""
        cp_delta, locked = resolve_gain_cp_roll(
            amount=1, roll_succeeded=False, already_rolled=False
        )
        assert cp_delta == 0
        assert locked is True

    def test_lock_prevents_second_resolution(self) -> None:
        """Calling resolve_gain_cp_roll when already_rolled=True raises ValueError."""
        import pytest

        with pytest.raises(ValueError, match="already resolved"):
            resolve_gain_cp_roll(amount=1, roll_succeeded=True, already_rolled=True)

    def test_success_with_multi_cp_amount(self) -> None:
        cp_delta, locked = resolve_gain_cp_roll(amount=2, roll_succeeded=True, already_rolled=False)
        assert cp_delta == 2
        assert locked is True
