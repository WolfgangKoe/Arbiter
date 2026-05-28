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
    shot: bool = False,
    fought: bool = False,
    in_melee: bool = False,
    in_reserve: bool = False,
    mwbd: bool = False,
) -> dict:
    return {
        "movement_choice": movement_choice,
        "turn_flags": {
            "advanced": movement_choice == "advanced",
            "retreated": movement_choice == "retreated",
            "charged": charged,
            "shot": shot,
            "fought": fought,
        },
        "in_melee": in_melee,
        "in_reserve": in_reserve,
        "my_will_be_done_active": mwbd,
    }


# ---------------------------------------------------------------------------
# Movement badge tests
# ---------------------------------------------------------------------------


def test_no_movement_choice_shows_no_movement_badge() -> None:
    html = state_badges_html(_state(movement_choice=None))
    for badge in ("MOVED", "STATIONARY", "ADVANCED", "RETREATED"):
        assert badge not in html


def test_movement_choice_moved_shows_moved_badge() -> None:
    assert "MOVED" in state_badges_html(_state(movement_choice="moved"))


def test_movement_choice_stationary_shows_stationary_badge() -> None:
    assert "STATIONARY" in state_badges_html(_state(movement_choice="stationary"))


def test_movement_choice_advanced_shows_advanced_badge() -> None:
    assert "ADVANCED" in state_badges_html(_state(movement_choice="advanced"))


def test_movement_choice_retreated_shows_retreated_badge() -> None:
    assert "RETREATED" in state_badges_html(_state(movement_choice="retreated"))


def test_movement_badge_does_not_show_other_movement_types() -> None:
    html = state_badges_html(_state(movement_choice="advanced"))
    assert "RETREATED" not in html
    assert "MOVED" not in html
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
# SHOT badge tests
# ---------------------------------------------------------------------------


def test_shot_flag_shows_shot_badge() -> None:
    assert "SHOT" in state_badges_html(_state(movement_choice="stationary", shot=True))


def test_shot_is_additive_with_stationary() -> None:
    html = state_badges_html(_state(movement_choice="stationary", shot=True))
    assert "STATIONARY" in html
    assert "SHOT" in html


def test_shot_is_additive_with_moved() -> None:
    html = state_badges_html(_state(movement_choice="moved", shot=True))
    assert "MOVED" in html
    assert "SHOT" in html


def test_shot_is_additive_with_charged() -> None:
    """Szenario 4: schoss und charged — CHARGED + SHOT zeigen."""
    html = state_badges_html(_state(movement_choice="moved", charged=True, shot=True))
    assert "CHARGED" in html
    assert "SHOT" in html
    assert "MOVED" not in html


# ---------------------------------------------------------------------------
# FOUGHT badge tests
# ---------------------------------------------------------------------------


def test_fought_flag_shows_fought_badge() -> None:
    assert "FOUGHT" in state_badges_html(_state(fought=True))


def test_fought_replaces_charged_in_display() -> None:
    """Szenario 5: nach Kampf verschwindet CHARGED — FOUGHT zeigt stattdessen."""
    html = state_badges_html(_state(charged=True, fought=True))
    assert "FOUGHT" in html
    assert "CHARGED" not in html


def test_fought_replaces_movement_badge() -> None:
    """FOUGHT hat höchste Priorität im Bewegungs-Slot."""
    html = state_badges_html(_state(movement_choice="moved", fought=True))
    assert "FOUGHT" in html
    assert "MOVED" not in html


def test_fought_with_in_melee_shows_both() -> None:
    """Szenario 8: FOUGHT + IN MELEE — kämpfte, noch gebunden."""
    html = state_badges_html(_state(in_melee=True, fought=True))
    assert "FOUGHT" in html
    assert "IN MELEE" in html


def test_fought_does_not_suppress_in_melee() -> None:
    """IN MELEE wird nur bei CHARGED unterdrückt, nicht bei FOUGHT."""
    html = state_badges_html(_state(charged=True, fought=True, in_melee=True))
    assert "FOUGHT" in html
    assert "IN MELEE" in html
    assert "CHARGED" not in html


def test_shot_fought_in_melee_all_show() -> None:
    """Szenario 4 Vollzustand: SHOT + FOUGHT + IN MELEE."""
    html = state_badges_html(
        _state(movement_choice="moved", charged=True, shot=True, fought=True, in_melee=True)
    )
    assert "FOUGHT" in html
    assert "SHOT" in html
    assert "IN MELEE" in html
    assert "CHARGED" not in html
    assert "MOVED" not in html


# ---------------------------------------------------------------------------
# Combination edge cases
# ---------------------------------------------------------------------------


def test_charged_suppresses_movement_badge() -> None:
    """When charged=True, the movement badge is hidden — CHARGED is the relevant state."""
    html = state_badges_html(_state(movement_choice="moved", charged=True))
    assert "MOVED" not in html
    assert "CHARGED" in html


def test_charged_suppresses_advanced_badge() -> None:
    """ADVANCED is also suppressed when charged."""
    html = state_badges_html(_state(movement_choice="advanced", charged=True))
    assert "ADVANCED" not in html
    assert "CHARGED" in html


def test_in_reserve_suppresses_movement_badge() -> None:
    """RESERVE units don't show a movement badge."""
    html = state_badges_html(_state(movement_choice="advanced", in_reserve=True))
    assert "ADVANCED" not in html
    assert "RESERVE" in html


def test_mwbd_shows_when_active() -> None:
    assert "MWBD" in state_badges_html(_state(movement_choice="stationary", mwbd=True))


def test_mwbd_is_additive() -> None:
    html = state_badges_html(_state(movement_choice="stationary", shot=True, mwbd=True))
    assert "STATIONARY" in html
    assert "SHOT" in html
    assert "MWBD" in html
