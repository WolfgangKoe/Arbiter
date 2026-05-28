"""Tests for state_badges_html() — movement_choice and combat badges."""

import sys
from pathlib import Path
from unittest.mock import MagicMock

sys.modules["streamlit"] = MagicMock()
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

from uiLayout._common import state_badges_html  # noqa: E402

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _state(
    movement_choice: str | None = None,
    charged: bool = False,
    in_melee: bool = False,
    in_reserve: bool = False,
) -> dict:
    return {
        "movement_choice": movement_choice,
        "turn_flags": {
            "advanced": False,
            "retreated": False,
            "charged": charged,
            "shot": False,
            "fought": False,
        },
        "in_melee": in_melee,
        "in_reserve": in_reserve,
    }


# ---------------------------------------------------------------------------
# movement_choice badge tests
# ---------------------------------------------------------------------------


def test_no_movement_choice_shows_no_movement_badge() -> None:
    html = state_badges_html(_state(movement_choice=None))
    for badge in ("NORMAL", "STATIONARY", "ADVANCED", "RETREATED"):
        assert badge not in html


def test_movement_choice_normal_shows_normal_badge() -> None:
    assert "NORMAL" in state_badges_html(_state(movement_choice="normal"))


def test_movement_choice_stationary_shows_stationary_badge() -> None:
    assert "STATIONARY" in state_badges_html(_state(movement_choice="stationary"))


def test_movement_choice_advanced_shows_advanced_badge() -> None:
    assert "ADVANCED" in state_badges_html(_state(movement_choice="advanced"))


def test_movement_choice_retreated_shows_retreated_badge() -> None:
    assert "RETREATED" in state_badges_html(_state(movement_choice="retreated"))


def test_movement_badge_does_not_show_other_movement_types() -> None:
    html = state_badges_html(_state(movement_choice="advanced"))
    assert "RETREATED" not in html
    assert "NORMAL" not in html
    assert "STATIONARY" not in html


# ---------------------------------------------------------------------------
# Combat badge tests
# ---------------------------------------------------------------------------


def test_charged_flag_shows_charged_badge() -> None:
    assert "CHARGED" in state_badges_html(_state(charged=True))


def test_in_melee_without_charged_shows_in_melee_badge() -> None:
    html = state_badges_html(_state(in_melee=True))
    assert "IN MELEE" in html
    assert "CHARGED" not in html


def test_charged_suppresses_in_melee_badge() -> None:
    html = state_badges_html(_state(charged=True, in_melee=True))
    assert "CHARGED" in html
    assert "IN MELEE" not in html


def test_in_reserve_shows_reserve_badge() -> None:
    assert "RESERVE" in state_badges_html(_state(in_reserve=True))


# ---------------------------------------------------------------------------
# Combination edge cases
# ---------------------------------------------------------------------------


def test_charged_suppresses_movement_badge() -> None:
    """When charged=True, the movement badge is hidden — CHARGED is the relevant state."""
    html = state_badges_html(_state(movement_choice="normal", charged=True))
    assert "NORMAL" not in html
    assert "CHARGED" in html


def test_charged_suppresses_advanced_badge() -> None:
    """ADVANCED is also suppressed when charged — charge overrides the movement choice."""
    html = state_badges_html(_state(movement_choice="advanced", charged=True))
    assert "ADVANCED" not in html
    assert "CHARGED" in html


def test_in_reserve_suppresses_movement_badge() -> None:
    """RESERVE units don't show a movement badge — RESERVE alone communicates their state."""
    html = state_badges_html(_state(movement_choice="advanced", in_reserve=True))
    assert "ADVANCED" not in html
    assert "RESERVE" in html
