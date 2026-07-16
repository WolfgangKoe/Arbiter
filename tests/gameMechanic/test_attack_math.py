"""Tests for attackMath.py — pure attack-count helpers.

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

from gameMechanic.attackMath import (  # noqa: E402
    _compute_attacks,
    _is_variable_attacks,
    _rapid_fire_input_cap,
    _total_attacks_int,
)

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


class TestRapidFireInputCap:
    """P20 (S119): ranged group-assignment "models" field cap doubles for Rapid Fire.

    core_rules.txt:1578-1586 — Rapid Fire doubles a model's attacks when its
    target is within half range. The app has no target-range input, so the
    caller (render_group_assignment) uses this field's raised max as the
    attack-count lever, letting the player enter up to twice the physical
    model count. Only the cap changes here — the default value is a caller
    concern (base_cap, unchanged), not part of this pure function's contract.
    """

    def test_rapid_fire_doubles_base_cap(self) -> None:
        assert _rapid_fire_input_cap("Rapid Fire", 10) == 20

    def test_rapid_fire_n_variant_doubles_base_cap(self) -> None:
        # "Rapid Fire 2" (printed attack characteristic in the type string)
        # still matches the prefix check — the per-model rate is a separate
        # concern (attacks string), not this cap.
        assert _rapid_fire_input_cap("Rapid Fire 2", 10) == 20

    def test_non_rapid_fire_cap_unchanged(self) -> None:
        assert _rapid_fire_input_cap("Assault 2", 10) == 10

    def test_grenade_cap_unchanged(self) -> None:
        assert _rapid_fire_input_cap("Grenade", 1) == 1

    def test_pistol_cap_unchanged(self) -> None:
        assert _rapid_fire_input_cap("Pistol", 5) == 5

    def test_zero_base_cap_stays_zero(self) -> None:
        # No models alive (or grenade cap already exhausted) → still 0 doubled
        assert _rapid_fire_input_cap("Rapid Fire", 0) == 0

    def test_melee_weapon_type_unchanged(self) -> None:
        assert _rapid_fire_input_cap("Melee", 4) == 4


# ---------------------------------------------------------------------------
# _is_variable_attacks — S136 Befund 4c-b: Command Re-Roll only covers "the
# dice to determine the number of attacks" (rules_appendix.txt COMMAND
# RE-ROLL) — a fixed Attacks characteristic has no roll to offer a re-roll on.
# ---------------------------------------------------------------------------


class TestIsVariableAttacks:
    def test_d6_is_variable(self) -> None:
        assert _is_variable_attacks("D6") is True

    def test_d3_is_variable(self) -> None:
        assert _is_variable_attacks("D3") is True

    def test_2d6_is_variable(self) -> None:
        assert _is_variable_attacks("2D6") is True

    def test_fixed_int_string_is_not_variable(self) -> None:
        assert _is_variable_attacks("1") is False

    def test_fixed_multi_digit_is_not_variable(self) -> None:
        assert _is_variable_attacks("4") is False

    def test_melee_placeholder_is_not_variable(self) -> None:
        assert _is_variable_attacks("Melee") is False

    def test_none_placeholder_is_not_variable(self) -> None:
        assert _is_variable_attacks("None") is False

    def test_empty_string_is_not_variable(self) -> None:
        assert _is_variable_attacks("") is False

    def test_star_placeholder_is_not_variable(self) -> None:
        assert _is_variable_attacks("*") is False

    def test_slash_tiered_is_not_variable(self) -> None:
        assert _is_variable_attacks("2/4") is False

    def test_extra_attacks_effect_is_not_variable_even_if_dice_string(self) -> None:
        # extra_attacks resolves via a formula, not the printed attacks string
        assert _is_variable_attacks("D6", {"type": "extra_attacks", "amount": 1}) is False

    def test_whitespace_around_dice_notation_is_stripped(self) -> None:
        assert _is_variable_attacks(" D6 ") is True


# ---------------------------------------------------------------------------
# _restriction_label — lines 41-46
# ---------------------------------------------------------------------------

from gameMechanic.attackMath import _restriction_label  # noqa: E402


class TestRestrictionLabel:
    def test_boss_nob_only_returns_human_readable(self) -> None:
        assert _restriction_label("boss_nob_only") == "Boss Nob only"

    def test_1_per_10_returns_human_readable(self) -> None:
        assert _restriction_label("1_per_10") == "1 per 10 models"

    def test_1_per_5_returns_human_readable(self) -> None:
        assert _restriction_label("1_per_5") == "1 per 5 models"

    def test_unknown_restriction_passes_through(self) -> None:
        assert _restriction_label("custom_restriction") == "custom_restriction"


# ---------------------------------------------------------------------------
# _compute_attacks — line 66 (slash "/" branch)
# ---------------------------------------------------------------------------


class TestComputeAttacksSlashBranch:
    def test_slash_attacks_takes_first_value(self) -> None:
        # "2/4" → use 2 per model (e.g. alternating fire modes)
        assert _compute_attacks("2/4", 3, unit_attacks=1) == "6"

    def test_slash_attacks_multiple_models(self) -> None:
        assert _compute_attacks("3/6", 5, unit_attacks=2) == "15"


# ---------------------------------------------------------------------------
# _total_attacks_int — line 90 (slash "/" branch)
# ---------------------------------------------------------------------------


class TestTotalAttacksIntSlashBranch:
    def test_slash_attacks_returns_first_value_times_models(self) -> None:
        assert _total_attacks_int("2/4", 3, unit_attacks=1) == 6

    def test_slash_attacks_single_model(self) -> None:
        assert _total_attacks_int("1/2", 1, unit_attacks=1) == 1


# ---------------------------------------------------------------------------
# _detect_weapon_special — lines 105-108, 136
# ---------------------------------------------------------------------------

from gameMechanic.attackMath import _detect_weapon_special  # noqa: E402
from gameObjects.weapon import Weapon, WeaponProfile  # noqa: E402


def _make_profile(
    abilities: str = "",
    is_melee: bool = False,
    effect: dict | None = None,
    max_attacks: int | None = None,
) -> WeaponProfile:
    return WeaponProfile(
        weapon_type="Melee" if is_melee else "Rapid Fire",
        range_inches=0 if is_melee else 24,
        attacks="1",
        strength=4,
        ap=0,
        damage="1",
        is_melee=is_melee,
        abilities=abilities,
        effect=effect,
        max_attacks=max_attacks,
    )


class TestDetectWeaponSpecial:
    def test_auto_hit_detected_from_abilities(self) -> None:
        profile = _make_profile(abilities="Auto-hits, ignore cover")
        result = _detect_weapon_special(profile)
        assert result["auto_hit"] is True

    def test_auto_hit_false_when_not_in_abilities(self) -> None:
        profile = _make_profile(abilities="Blast")
        result = _detect_weapon_special(profile)
        assert result["auto_hit"] is False

    def test_extra_hits_detected_from_effect(self) -> None:
        profile = _make_profile(effect={"type": "extra_hits", "on": 6, "extra": 1})
        result = _detect_weapon_special(profile)
        assert result["extra_hits"] is True

    def test_alternating_fire_detected_from_effect(self) -> None:
        profile = _make_profile(effect={"type": "alternating_fire"})
        result = _detect_weapon_special(profile)
        assert result["alternating_fire"] is True

    def test_hit_roll_penalty_detected_for_melee_debuff(self) -> None:
        profile = _make_profile(
            is_melee=True,
            effect={"type": "debuff_roll", "stat": "hit_roll", "modifier": -1},
        )
        result = _detect_weapon_special(profile)
        assert result["hit_roll_penalty"] is True

    def test_hit_roll_penalty_false_when_not_melee(self) -> None:
        profile = _make_profile(
            is_melee=False,
            effect={"type": "debuff_roll", "stat": "hit_roll", "modifier": -1},
        )
        result = _detect_weapon_special(profile)
        assert result["hit_roll_penalty"] is False

    def test_hit_roll_penalty_false_when_modifier_positive(self) -> None:
        profile = _make_profile(
            is_melee=True,
            effect={"type": "debuff_roll", "stat": "hit_roll", "modifier": 1},
        )
        result = _detect_weapon_special(profile)
        assert result["hit_roll_penalty"] is False

    def test_mortal_wound_detected_case_insensitive(self) -> None:
        profile = _make_profile(abilities="Causes 1 Mortal Wound on a 6+")
        result = _detect_weapon_special(profile)
        assert result["has_mortal_wounds"] is True

    def test_no_special_properties_all_false(self) -> None:
        profile = _make_profile()
        result = _detect_weapon_special(profile)
        assert result == {
            "auto_hit": False,
            "extra_hits": False,
            "alternating_fire": False,
            "hit_roll_penalty": False,
            "has_mortal_wounds": False,
        }

    def test_none_effect_handled_gracefully(self) -> None:
        profile = _make_profile(effect=None)
        result = _detect_weapon_special(profile)
        assert result["extra_hits"] is False
        assert result["alternating_fire"] is False
        assert result["hit_roll_penalty"] is False


# ---------------------------------------------------------------------------
# _group_melee_budget — line 136 (skips weapons without melee profile / non-extra-attacks)
# ---------------------------------------------------------------------------

from gameMechanic.attackMath import _group_melee_budget  # noqa: E402


def _melee_weapon_with_extra_attacks(amount: int) -> Weapon:
    profile = WeaponProfile(
        weapon_type="Melee",
        range_inches=0,
        attacks="1",
        strength=4,
        ap=0,
        damage="1",
        is_melee=True,
        effect={"type": "extra_attacks", "amount": amount},
    )
    return Weapon(id="w1", name_en="Extra Attack Weapon", profiles=[profile])


def _ranged_weapon() -> Weapon:
    profile = WeaponProfile(
        weapon_type="Rapid Fire",
        range_inches=24,
        attacks="2",
        strength=4,
        ap=0,
        damage="1",
        is_melee=False,
    )
    return Weapon(id="w2", name_en="Ranged Weapon", profiles=[profile])


def _melee_weapon_no_effect() -> Weapon:
    profile = WeaponProfile(
        weapon_type="Melee",
        range_inches=0,
        attacks="1",
        strength=4,
        ap=0,
        damage="1",
        is_melee=True,
        effect=None,
    )
    return Weapon(id="w3", name_en="Plain Melee", profiles=[profile])


class TestGroupMeleeBudget:
    def test_no_extra_attack_weapons_returns_base(self) -> None:
        # No weapons at all → budget = alive × eff_attacks
        assert _group_melee_budget([], alive=3, eff_attacks=2) == 6

    def test_extra_attack_weapon_adds_bonus(self) -> None:
        w = _melee_weapon_with_extra_attacks(1)
        assert _group_melee_budget([w], alive=3, eff_attacks=2) == 9  # 6 base + 3×1

    def test_ranged_weapon_skipped_no_melee_profile(self) -> None:
        # Ranged weapon has no melee profile → skipped (line 136 'continue')
        w = _ranged_weapon()
        assert _group_melee_budget([w], alive=3, eff_attacks=2) == 6  # unchanged

    def test_melee_weapon_without_extra_attacks_effect_skipped(self) -> None:
        # Melee weapon with no effect → skipped (not extra_attacks type)
        w = _melee_weapon_no_effect()
        assert _group_melee_budget([w], alive=3, eff_attacks=2) == 6

    def test_max_attacks_weapon_uses_cap(self) -> None:
        # max_attacks set → uses cap instead of effect amount
        profile = WeaponProfile(
            weapon_type="Melee",
            range_inches=0,
            attacks="1",
            strength=4,
            ap=0,
            damage="1",
            is_melee=True,
            effect={"type": "extra_attacks", "amount": 99},
            max_attacks=2,
        )
        w = Weapon(id="w4", name_en="Capped", profiles=[profile])
        assert _group_melee_budget([w], alive=3, eff_attacks=2) == 6 + 6  # base 6 + 3×2


# ---------------------------------------------------------------------------
# _has_independent_attack_budget — B-068: capped extra_attacks weapons
# (e.g. Silent King's Staff of Stars / Scythe of Dust) default to their max
# instead of 0, since _group_melee_budget already reserves their cap.
# ---------------------------------------------------------------------------

from gameMechanic.attackMath import _has_independent_attack_budget  # noqa: E402


class TestHasIndependentAttackBudget:
    def test_capped_extra_attacks_weapon_has_own_budget(self) -> None:
        effect = {"type": "extra_attacks", "amount": 3}
        assert _has_independent_attack_budget(effect, max_attacks=3) is True

    def test_extra_attacks_without_cap_shares_pool(self) -> None:
        effect = {"type": "extra_attacks", "amount": 1}
        assert _has_independent_attack_budget(effect, max_attacks=None) is False

    def test_plain_weapon_shares_pool(self) -> None:
        assert _has_independent_attack_budget(None, max_attacks=None) is False

    def test_non_extra_attacks_effect_with_cap_shares_pool(self) -> None:
        effect = {"type": "something_else"}
        assert _has_independent_attack_budget(effect, max_attacks=3) is False
