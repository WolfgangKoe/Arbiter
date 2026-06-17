"""Tests for the round-choice ability slot swap (setup reordering).

Every slot (rounds 1–5 + the always-active 6th) is a dropdown over all
protocols; choosing one already placed elsewhere swaps the two so the map
stays a bijection.
"""

import sys
from pathlib import Path
from unittest.mock import MagicMock

sys.modules["streamlit"] = MagicMock()
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

from uiLayout.gameActionsArea import _round_choice_slots_after_swap  # noqa: E402


def test_swap_between_two_rounds_exchanges_them() -> None:
    slots = {"extra": "p6", 1: "p1", 2: "p2", 3: "p3", 4: "p4", 5: "p5"}
    # Put p4 (currently round 4) into round 2 → round 4 takes p2.
    result = _round_choice_slots_after_swap(slots, 2, "p4")
    assert result[2] == "p4"
    assert result[4] == "p2"
    assert sorted(result.values()) == ["p1", "p2", "p3", "p4", "p5", "p6"]


def test_swap_round_with_extra_slot() -> None:
    slots = {"extra": "p6", 1: "p1", 2: "p2", 3: "p3", 4: "p4", 5: "p5"}
    # Move the 6th ability into round 1 → round 1's old ability becomes the 6th.
    result = _round_choice_slots_after_swap(slots, 1, "p6")
    assert result[1] == "p6"
    assert result["extra"] == "p1"
    assert sorted(result.values()) == ["p1", "p2", "p3", "p4", "p5", "p6"]


def test_selecting_same_value_is_a_noop() -> None:
    slots = {"extra": "p6", 1: "p1", 2: "p2"}
    assert _round_choice_slots_after_swap(slots, 1, "p1") == slots


def test_original_map_is_not_mutated() -> None:
    slots = {"extra": "p6", 1: "p1", 2: "p2"}
    _round_choice_slots_after_swap(slots, 1, "p2")
    assert slots == {"extra": "p6", 1: "p1", 2: "p2"}
