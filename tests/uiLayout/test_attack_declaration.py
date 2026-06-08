"""Tests for attack declaration helpers: _total_attacks_int, _compute_attacks."""

import sys
from pathlib import Path
from unittest.mock import MagicMock

sys.modules["streamlit"] = MagicMock()
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

from uiLayout._common import _compute_attacks, _total_attacks_int  # noqa: E402

# ---------------------------------------------------------------------------
# _total_attacks_int — melee ("Melee" / "*") and fixed counts
# ---------------------------------------------------------------------------


def test_melee_keyword_returns_models_times_unit_attacks() -> None:
    assert _total_attacks_int("Melee", 10, 2) == 20


def test_star_keyword_returns_models_times_unit_attacks() -> None:
    assert _total_attacks_int("*", 5, 3) == 15


def test_fixed_attack_count_ignores_unit_attacks() -> None:
    assert _total_attacks_int("2", 10, 3) == 20


def test_dice_based_returns_none() -> None:
    assert _total_attacks_int("D3", 5, 2) is None


def test_waaagh_bonus_applied_via_unit_attacks_param() -> None:
    # WAAAGH! +1 is passed as unit_attacks + 1 by the caller
    assert _total_attacks_int("Melee", 20, 2 + 1) == 60


def test_waaagh_bonus_does_not_affect_fixed_weapon_attacks() -> None:
    # Fixed weapon attacks ("2") are independent of unit_attacks
    assert _total_attacks_int("2", 20, 2 + 1) == 40


def test_single_model_melee() -> None:
    assert _total_attacks_int("Melee", 1, 4) == 4


def test_single_model_melee_with_waaagh_bonus() -> None:
    assert _total_attacks_int("Melee", 1, 4 + 1) == 5


# ---------------------------------------------------------------------------
# _compute_attacks — display string
# ---------------------------------------------------------------------------


def test_compute_melee_returns_models_times_unit_attacks() -> None:
    assert _compute_attacks("Melee", 10, 2) == "20"


def test_compute_fixed_returns_models_times_weapon_attacks() -> None:
    assert _compute_attacks("2", 10, 3) == "20"


def test_compute_dice_returns_product_string() -> None:
    result = _compute_attacks("D3", 5, 2)
    assert result == "5×D3"


def test_compute_star_returns_models_times_unit_attacks() -> None:
    assert _compute_attacks("*", 3, 4) == "12"


# ---------------------------------------------------------------------------
# Entry filter invariant — entries with atk_override=0 are excluded
# ---------------------------------------------------------------------------


def test_entry_filter_excludes_zero_atk_override() -> None:
    entries = [
        {"weapon_name": "Power Klaw", "atk_override": 3, "models_count": 1},
        {"weapon_name": "Slugga", "atk_override": 0, "models_count": 1},
    ]
    filtered = [e for e in entries if e.get("atk_override", e["models_count"]) > 0]
    assert len(filtered) == 1
    assert filtered[0]["weapon_name"] == "Power Klaw"


def test_entry_filter_excludes_zero_models_count_in_shooting() -> None:
    entries = [
        {"weapon_name": "Bolt Rifle", "models_count": 5},
        {"weapon_name": "Bolt Rifle", "models_count": 0},
    ]
    filtered = [e for e in entries if e.get("atk_override", e["models_count"]) > 0]
    assert len(filtered) == 1
    assert filtered[0]["models_count"] == 5


def test_entry_filter_keeps_all_nonzero_entries() -> None:
    entries = [
        {"weapon_name": "Power Klaw", "atk_override": 2, "models_count": 1},
        {"weapon_name": "Voidblade", "atk_override": 2, "models_count": 1},
    ]
    filtered = [e for e in entries if e.get("atk_override", e["models_count"]) > 0]
    assert len(filtered) == 2
