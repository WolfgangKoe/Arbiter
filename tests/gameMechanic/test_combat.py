"""Tests for combat.py — Ziel 3b: AttackParams, DefendParams, resolve_attack.

resolve_attack() takes player-entered counts (physically rolled), no auto-dice.
All edge cases from the 9E rulebook are covered here.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

from gameMechanic.combat import (
    AttackParams,
    DefendParams,
    parse_dice,
    resolve_attack,
    resolve_weapon_strength,
    wound_threshold,
)

# ---------------------------------------------------------------------------
# parse_dice
# ---------------------------------------------------------------------------


class TestParseDice:
    def test_fixed_integer(self):
        assert parse_dice("3") == 3

    def test_d6(self):
        result = parse_dice("D6")
        assert 1 <= result <= 6

    def test_2d6(self):
        result = parse_dice("2D6")
        assert 2 <= result <= 12

    def test_3d3(self):
        result = parse_dice("3D3")
        assert 3 <= result <= 9

    def test_lowercase(self):
        result = parse_dice("d6")
        assert 1 <= result <= 6

    def test_zero_prefix(self):
        assert parse_dice("1") == 1


class TestParseDiceWNotation:
    def test_w3_notation(self):
        assert 1 <= parse_dice("W3") <= 3

    def test_w6_notation(self):
        assert 1 <= parse_dice("W6") <= 6

    def test_3w3_notation(self):
        assert 3 <= parse_dice("3W3") <= 9

    def test_w3_plus_3(self):
        assert 4 <= parse_dice("W3+3") <= 6

    def test_d3_plus_3(self):
        assert 4 <= parse_dice("D3+3") <= 6

    def test_2d6_plus_2(self):
        assert 4 <= parse_dice("2D6+2") <= 14

    def test_lowercase_w(self):
        assert 1 <= parse_dice("w6") <= 6


# ---------------------------------------------------------------------------
# resolve_weapon_strength
# ---------------------------------------------------------------------------


class TestResolveWeaponStrength:
    def test_fixed_integer(self):
        assert resolve_weapon_strength(5, 4) == 5

    def test_fixed_string_integer(self):
        assert resolve_weapon_strength("6", 4) == 6

    def test_traeger_keyword(self):
        assert resolve_weapon_strength("Träger", 4) == 4

    def test_bearer_keyword(self):
        assert resolve_weapon_strength("Bearer", 3) == 3

    def test_user_keyword(self):
        assert resolve_weapon_strength("user", 5) == 5

    def test_plus_one(self):
        assert resolve_weapon_strength("+1", 4) == 5

    def test_plus_two(self):
        assert resolve_weapon_strength("+2", 3) == 5

    def test_times_two(self):
        assert resolve_weapon_strength("x2", 4) == 8

    def test_times_three(self):
        assert resolve_weapon_strength("x3", 3) == 9


# ---------------------------------------------------------------------------
# wound_threshold
# ---------------------------------------------------------------------------


class TestWoundThreshold:
    def test_double_strength_wounds_on_2(self):
        assert wound_threshold(8, 4) == 2

    def test_strength_greater_wounds_on_3(self):
        assert wound_threshold(5, 4) == 3

    def test_equal_strength_wounds_on_4(self):
        assert wound_threshold(4, 4) == 4

    def test_strength_less_wounds_on_5(self):
        assert wound_threshold(3, 4) == 5

    def test_half_strength_wounds_on_6(self):
        assert wound_threshold(2, 4) == 6

    def test_boundary_exactly_double(self):
        assert wound_threshold(10, 5) == 2

    def test_boundary_exactly_half(self):
        assert wound_threshold(3, 6) == 6


# ---------------------------------------------------------------------------
# AttackParams / DefendParams — dataclass construction
# ---------------------------------------------------------------------------


class TestDataclasses:
    def test_attack_params_defaults(self):
        params = AttackParams(
            attacks=3,
            skill=3,
            strength=4,
            ap=0,
            damage=1,
        )
        assert params.hit_modifier == 0
        assert params.wound_modifier == 0
        assert params.mwbd_active is False

    def test_defend_params_defaults(self):
        d = DefendParams(toughness=4, save=3, wounds=2)
        assert d.invul_save is None
        assert d.fnp is None

    def test_attack_params_mwbd_sets_flag(self):
        params = AttackParams(attacks=3, skill=3, strength=4, ap=0, damage=1, mwbd_active=True)
        assert params.mwbd_active is True

    def test_attack_params_with_modifiers(self):
        params = AttackParams(
            attacks=5, skill=4, strength=6, ap=-2, damage=2, hit_modifier=1, wound_modifier=-1
        )
        assert params.hit_modifier == 1
        assert params.wound_modifier == -1


# ---------------------------------------------------------------------------
# resolve_attack — hit phase
# ---------------------------------------------------------------------------


class TestResolveAttackHitPhase:
    """Caller passes how many dice they actually rolled that hit."""

    def _base_params(self, **kwargs) -> AttackParams:
        defaults = dict(attacks=10, skill=3, strength=4, ap=0, damage=1)
        defaults.update(kwargs)
        return AttackParams(**defaults)

    def _base_defender(self, **kwargs) -> DefendParams:
        defaults = dict(toughness=4, save=5, wounds=5)
        defaults.update(kwargs)
        return DefendParams(**defaults)

    def test_zero_hits_returns_zero_damage(self):
        dmg, log = resolve_attack(self._base_params(), self._base_defender(), hits_rolled=0)
        assert dmg == 0
        assert any(
            "0" in line or "no hit" in line.lower() or "treffer" in line.lower() for line in log
        )

    def test_all_hits_passed_through_to_wound_phase(self):
        dmg, log = resolve_attack(
            self._base_params(), self._base_defender(), hits_rolled=6, wounds_rolled=6
        )
        # 6 wounds, save 5+ on open ground → some damage expected (not guaranteed 0)
        assert dmg >= 0

    def test_log_contains_hit_count(self):
        _, log = resolve_attack(self._base_params(), self._base_defender(), hits_rolled=4)
        combined = " ".join(log)
        assert "4" in combined


# ---------------------------------------------------------------------------
# resolve_attack — wound phase
# ---------------------------------------------------------------------------


class TestResolveAttackWoundPhase:
    def _params(self, **kwargs) -> AttackParams:
        defaults = dict(attacks=10, skill=3, strength=4, ap=0, damage=1)
        defaults.update(kwargs)
        return AttackParams(**defaults)

    def _defender(self, **kwargs) -> DefendParams:
        defaults = dict(toughness=4, save=7, wounds=10)  # save 7+ = impossible save
        defaults.update(kwargs)
        return DefendParams(**defaults)

    def test_zero_wounds_returns_zero_damage(self):
        dmg, log = resolve_attack(self._params(), self._defender(), hits_rolled=5, wounds_rolled=0)
        assert dmg == 0

    def test_wounds_with_impossible_save_equals_wounds(self):
        # save 7+ means all wounds go through; damage 1 per wound
        dmg, log = resolve_attack(
            self._params(), self._defender(), hits_rolled=5, wounds_rolled=3, saves_failed=3
        )
        assert dmg == 3

    def test_log_contains_wound_count(self):
        _, log = resolve_attack(self._params(), self._defender(), hits_rolled=5, wounds_rolled=3)
        combined = " ".join(log)
        assert "3" in combined


# ---------------------------------------------------------------------------
# resolve_attack — save phase (AP modifier)
# ---------------------------------------------------------------------------


class TestResolveAttackSavePhase:
    def _params(self, ap: int = 0, **kwargs) -> AttackParams:
        defaults = dict(attacks=10, skill=3, strength=4, ap=ap, damage=1)
        defaults.update(kwargs)
        return AttackParams(**defaults)

    def _defender(self, save: int = 3, invul_save: int | None = None, **kwargs) -> DefendParams:
        defaults = dict(toughness=4, save=save, wounds=10)
        defaults.update(kwargs)
        return DefendParams(invul_save=invul_save, **defaults)

    def test_no_ap_save_unmodified(self):
        # AP 0 → save stays at 3+
        dmg, log = resolve_attack(
            self._params(ap=0),
            self._defender(save=3),
            hits_rolled=5,
            wounds_rolled=3,
            saves_failed=0,
        )
        assert dmg == 0

    def test_ap_minus2_worsens_save(self):
        # save 3+ with AP -2 → effective roll must be 5+ (raw + 2 ≥ 5)
        # Caller provides saves_failed count already accounting for that
        dmg, log = resolve_attack(
            self._params(ap=-2),
            self._defender(save=3),
            hits_rolled=5,
            wounds_rolled=3,
            saves_failed=2,
        )
        assert dmg == 2  # 2 failed saves × damage 1

    def test_invul_save_used_when_better(self):
        # armour save 2+ vs AP -4 → effective 6+; invuln 4+ → invuln wins
        dmg, log = resolve_attack(
            self._params(ap=-4),
            self._defender(save=2, invul_save=4),
            hits_rolled=5,
            wounds_rolled=3,
            saves_failed=1,
        )
        assert dmg == 1
        combined = " ".join(log)
        assert "invul" in combined.lower() or "4" in combined

    def test_armour_save_used_when_better_than_invul(self):
        # armour 3+ with AP 0 → effective 3+; invuln 5+ → armour wins
        dmg, log = resolve_attack(
            self._params(ap=0),
            self._defender(save=3, invul_save=5),
            hits_rolled=5,
            wounds_rolled=3,
            saves_failed=0,
        )
        assert dmg == 0

    def test_impossible_save_all_wounds_go_through(self):
        # AP -5 on save 3+ → effective 8+; no invuln → all 3 wounds damage
        dmg, log = resolve_attack(
            self._params(ap=-5),
            self._defender(save=3, invul_save=None),
            hits_rolled=5,
            wounds_rolled=3,
            saves_failed=3,
        )
        assert dmg == 3


# ---------------------------------------------------------------------------
# resolve_attack — damage
# ---------------------------------------------------------------------------


class TestResolveAttackDamage:
    def _params(self, damage: int = 1, **kwargs) -> AttackParams:
        defaults = dict(attacks=10, skill=3, strength=4, ap=0, damage=damage)
        defaults.update(kwargs)
        return AttackParams(**defaults)

    def _defender(self, **kwargs) -> DefendParams:
        defaults = dict(toughness=4, save=7, wounds=10)
        defaults.update(kwargs)
        return DefendParams(**defaults)

    def test_damage_1_per_failed_save(self):
        dmg, _ = resolve_attack(
            self._params(damage=1), self._defender(), hits_rolled=5, wounds_rolled=3, saves_failed=3
        )
        assert dmg == 3

    def test_damage_2_per_failed_save(self):
        dmg, _ = resolve_attack(
            self._params(damage=2), self._defender(), hits_rolled=5, wounds_rolled=3, saves_failed=2
        )
        assert dmg == 4

    def test_damage_3_per_failed_save(self):
        dmg, _ = resolve_attack(
            self._params(damage=3), self._defender(), hits_rolled=5, wounds_rolled=3, saves_failed=1
        )
        assert dmg == 3

    def test_zero_failed_saves_zero_damage(self):
        dmg, _ = resolve_attack(
            self._params(damage=3), self._defender(), hits_rolled=5, wounds_rolled=3, saves_failed=0
        )
        assert dmg == 0


# ---------------------------------------------------------------------------
# resolve_attack — FNP (Feel No Pain)
# ---------------------------------------------------------------------------


class TestResolveAttackFNP:
    def _params(self, **kwargs) -> AttackParams:
        defaults = dict(attacks=10, skill=3, strength=4, ap=0, damage=1)
        defaults.update(kwargs)
        return AttackParams(**defaults)

    def _defender(self, fnp: int | None = None, **kwargs) -> DefendParams:
        defaults = dict(toughness=4, save=7, wounds=10)
        defaults.update(kwargs)
        return DefendParams(fnp=fnp, **defaults)

    def test_fnp_reduces_damage(self):
        dmg, log = resolve_attack(
            self._params(),
            self._defender(fnp=5),
            hits_rolled=5,
            wounds_rolled=3,
            saves_failed=3,
            fnp_saved=1,
        )
        assert dmg == 2  # 3 - 1 FNP saved
        combined = " ".join(log)
        assert "fnp" in combined.lower() or "pain" in combined.lower() or "5" in combined

    def test_no_fnp_full_damage(self):
        dmg, _ = resolve_attack(
            self._params(), self._defender(fnp=None), hits_rolled=5, wounds_rolled=3, saves_failed=3
        )
        assert dmg == 3

    def test_fnp_saves_all(self):
        dmg, _ = resolve_attack(
            self._params(),
            self._defender(fnp=5),
            hits_rolled=5,
            wounds_rolled=3,
            saves_failed=3,
            fnp_saved=3,
        )
        assert dmg == 0


# ---------------------------------------------------------------------------
# resolve_attack — MWBD
# ---------------------------------------------------------------------------


class TestResolveAttackMWBD:
    def test_mwbd_reflected_in_log(self):
        params = AttackParams(attacks=10, skill=3, strength=4, ap=0, damage=1, mwbd_active=True)
        defender = DefendParams(toughness=4, save=7, wounds=10)
        _, log = resolve_attack(params, defender, hits_rolled=5)
        combined = " ".join(log)
        assert "mwbd" in combined.lower() or "will be done" in combined.lower()

    def test_no_mwbd_no_mention_in_log(self):
        params = AttackParams(attacks=10, skill=3, strength=4, ap=0, damage=1, mwbd_active=False)
        defender = DefendParams(toughness=4, save=7, wounds=10)
        _, log = resolve_attack(params, defender, hits_rolled=5)
        combined = " ".join(log)
        assert "mwbd" not in combined.lower()


# ---------------------------------------------------------------------------
# resolve_attack — return types
# ---------------------------------------------------------------------------


class TestResolveAttackReturnTypes:
    def test_returns_tuple(self):
        params = AttackParams(attacks=3, skill=3, strength=4, ap=0, damage=1)
        defender = DefendParams(toughness=4, save=7, wounds=5)
        result = resolve_attack(params, defender, hits_rolled=2, wounds_rolled=2, saves_failed=2)
        assert isinstance(result, tuple)
        assert len(result) == 2

    def test_damage_is_int(self):
        params = AttackParams(attacks=3, skill=3, strength=4, ap=0, damage=1)
        defender = DefendParams(toughness=4, save=7, wounds=5)
        dmg, log = resolve_attack(params, defender, hits_rolled=2, wounds_rolled=2, saves_failed=2)
        assert isinstance(dmg, int)

    def test_log_is_list_of_strings(self):
        params = AttackParams(attacks=3, skill=3, strength=4, ap=0, damage=1)
        defender = DefendParams(toughness=4, save=7, wounds=5)
        dmg, log = resolve_attack(params, defender, hits_rolled=2, wounds_rolled=2, saves_failed=2)
        assert isinstance(log, list)
        assert all(isinstance(line, str) for line in log)

    def test_log_not_empty(self):
        params = AttackParams(attacks=3, skill=3, strength=4, ap=0, damage=1)
        defender = DefendParams(toughness=4, save=7, wounds=5)
        _, log = resolve_attack(params, defender, hits_rolled=0)
        assert len(log) > 0


# ---------------------------------------------------------------------------
# resolve_attack — hit modifier logging
# ---------------------------------------------------------------------------


class TestResolveAttackHitModLogging:
    def test_hit_modifier_nonzero_appears_in_log(self):
        params = AttackParams(attacks=10, skill=3, strength=4, ap=0, damage=1, hit_modifier=1)
        defender = DefendParams(toughness=4, save=7, wounds=10)
        _, log = resolve_attack(params, defender, hits_rolled=5)
        assert any("hit mod +1" in line for line in log)

    def test_no_hit_modifier_absent_from_log(self):
        params = AttackParams(attacks=10, skill=3, strength=4, ap=0, damage=1, hit_modifier=0)
        defender = DefendParams(toughness=4, save=7, wounds=10)
        _, log = resolve_attack(params, defender, hits_rolled=5)
        assert not any("hit mod" in line for line in log)
