"""Tests for attack_math.py — pure attack-count helpers.

Covers R-COMBAT-17: Rapid-Fire weapon attack doubling within half range.

Implementation note: _compute_attacks() and _total_attacks_int() are
range-agnostic pure functions.  They receive the attacks *string* from the
weapon profile (e.g. "2" for a Rapid Fire 2 weapon) and a model count.
The Rapid Fire doubling is a *caller* responsibility: the UI passes double
the model-count (or a doubled attacks value) when the target is within half
range.  These tests nail down:
  (a) the base (out-of-half-range) behaviour — no implicit doubling,
  (b) that calling with a doubled attacks argument produces the doubled total,
  confirming the contract callers must uphold to implement R-COMBAT-17.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

from gameMechanic.attack_math import _compute_attacks, _total_attacks_int  # noqa: E402

# ---------------------------------------------------------------------------
# R-COMBAT-17 — Rapid Fire: attack doubling at half range
# ---------------------------------------------------------------------------


class TestComputeAttacksRapidFire:
    """R-COMBAT-17: _compute_attacks returns models × base_attacks (no implicit doubling).

    For a Rapid Fire N weapon the attacks string encodes the base count (e.g. "2"
    for Rapid Fire 2).  At full range the function returns models × 2.  At half
    range the *caller* is expected to double either the attacks value or the model
    count before calling; the doubled result must equal 2 × full-range result.
    """

    def test_rapid_fire_base_attacks_returns_models_times_attacks(self) -> None:
        # 3 models with Rapid Fire 2 weapon at full range → 3 × 2 = 6
        assert _compute_attacks("2", 3, unit_attacks=4) == "6"

    def test_rapid_fire_at_half_range_caller_doubles_attacks(self) -> None:
        # Within half range the caller doubles the attacks string value:
        # base "2" → doubled "4" per model; 3 models → 12
        base = int(_compute_attacks("2", 3, unit_attacks=4))
        doubled = int(_compute_attacks("4", 3, unit_attacks=4))
        assert doubled == base * 2

    def test_rapid_fire_single_model_at_full_range(self) -> None:
        # 1 model, Rapid Fire 1 weapon → 1 attack
        assert _compute_attacks("1", 1, unit_attacks=2) == "1"

    def test_rapid_fire_single_model_doubled_at_half_range(self) -> None:
        # 1 model, Rapid Fire 1 → doubled to 2 at half range
        assert _compute_attacks("2", 1, unit_attacks=2) == "2"

    def test_rapid_fire_5_models_rapid_fire_2_base(self) -> None:
        # 5 models × 2 attacks = 10 at full range
        assert _compute_attacks("2", 5, unit_attacks=3) == "10"

    def test_rapid_fire_5_models_doubled_at_half_range(self) -> None:
        # Caller doubles: 5 models × 4 attacks = 20 at half range
        assert _compute_attacks("4", 5, unit_attacks=3) == "20"


class TestTotalAttacksIntRapidFire:
    """R-COMBAT-17: _total_attacks_int mirrors _compute_attacks as int (or None for dice)."""

    def test_rapid_fire_2_three_models_at_full_range(self) -> None:
        # 3 models × Rapid Fire 2 → 6 at full range
        assert _total_attacks_int("2", 3, unit_attacks=4) == 6

    def test_rapid_fire_1_one_model_at_full_range(self) -> None:
        assert _total_attacks_int("1", 1, unit_attacks=2) == 1

    def test_rapid_fire_at_half_range_doubled_by_caller(self) -> None:
        # Within half range caller passes doubled attack count:
        base = _total_attacks_int("2", 3, unit_attacks=4)
        doubled = _total_attacks_int("4", 3, unit_attacks=4)
        assert doubled == base * 2  # type: ignore[operator]

    def test_returns_int_not_string(self) -> None:
        result = _total_attacks_int("2", 3, unit_attacks=4)
        assert isinstance(result, int)

    def test_dice_attacks_returns_none(self) -> None:
        # Dice-based attacks (e.g. "D6") cannot be pre-computed → None
        result = _total_attacks_int("D6", 3, unit_attacks=4)
        assert result is None
