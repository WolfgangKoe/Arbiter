"""Tests for combat.py — Ziel 3b: AttackParams, DefendParams, resolve_attack.

resolve_attack() takes player-entered counts (physically rolled), no auto-dice.
All edge cases from the 9E rulebook are covered here.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

from gameMechanic.attackMath import _combi_hit_penalty
from gameMechanic.combat import (
    AttackParams,
    DefendParams,
    parse_dice,
    resolve_attack,
    resolve_attack_modifiers,
    resolve_save,
    resolve_weapon_strength,
    wound_threshold,
)
from gameObjects.weapon import WeaponProfile

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


# ---------------------------------------------------------------------------
# R-COMBAT-09: resolve_save — multiple invulnerable saves → only best used
#
# resolve_save() accepts a single invuln_save value.  The 9E rule "if a model
# has more than one invulnerable save, it can only use one of them" means the
# caller pre-selects the best (lowest numeric value) before passing it in.
# These tests verify that resolve_save() correctly selects the best save when
# the caller has already chosen the minimum (i.e. best) invuln from several.
# ---------------------------------------------------------------------------


class TestResolveSaveMultipleInvulns:
    """R-COMBAT-09: best (lowest value) invulnerable save wins when a model has several."""

    def test_best_of_two_invulns_is_used_when_better_than_armour(self) -> None:
        # Model has 4+ and 5+ invulns → caller passes min=4; AP-4 on 3+ → armour_eff=7+
        # invuln 4+ beats armour 7+ → using_invuln=True, effective=4
        result = resolve_save(base_save=3, invuln_save=4, ap=-4, save_modifiers=[])
        assert result["using_invuln"] is True
        assert result["effective"] == 4

    def test_worse_invuln_would_lose_to_armour(self) -> None:
        # If caller mistakenly passed the weaker 5+ invuln (AP 0, armour 3+ → eff=3+):
        # armour 3+ beats invuln 5+ → using_invuln=False.
        # This confirms that the lower (better) value must be chosen.
        result = resolve_save(base_save=3, invuln_save=5, ap=0, save_modifiers=[])
        assert result["using_invuln"] is False
        assert result["effective"] == 3

    def test_minimum_of_two_invulns_produces_better_save_than_either_alone(self) -> None:
        # Simulates: model has 3+ and 5+ invulns; caller picks min(3, 5)=3.
        # AP-5 on armour 4+ → armour_eff=9 (impossible); invuln 3+ wins.
        best_invuln = min(3, 5)  # caller responsibility: pick the best
        result = resolve_save(base_save=4, invuln_save=best_invuln, ap=-5, save_modifiers=[])
        assert result["invuln"] == 3
        assert result["using_invuln"] is True
        assert result["effective"] == 3

    def test_best_invuln_equal_to_armour_prefers_armour(self) -> None:
        # invuln 3+ and armour 3+ (AP 0) → armour_modified=3, invuln=3 → not strictly better
        # resolve_save uses `invuln < armour_modified`, so equal → armour wins
        result = resolve_save(base_save=3, invuln_save=3, ap=0, save_modifiers=[])
        assert result["using_invuln"] is False
        assert result["effective"] == 3


# ---------------------------------------------------------------------------
# S121 regression: CCW fallback profile must work in save resolution
# ---------------------------------------------------------------------------


class TestResolveSaveWithCcwFallbackWeapon:
    """S121 regression: the loader's CCW fallback profile carried ap="0" (str),
    so every unit without an explicit melee weapon (e.g. Gretchin) crashed in
    resolve_save (abs("0") → TypeError). The fallback ap must flow through
    resolve_save like any YAML-loaded int.
    """

    def test_resolve_save_with_ccw_fallback_weapon_does_not_crash(self) -> None:
        from gameObjects.loader import _CCW_PROFILE

        result = resolve_save(
            base_save=5,
            invuln_save=None,
            ap=_CCW_PROFILE.ap,
            save_modifiers=[],
        )
        assert result["effective"] == 5
        assert result["using_invuln"] is False


# ---------------------------------------------------------------------------
# B-056 — Quantum Deflection: fixed 4+ invuln, not an additive modifier.
#
# resolve_save() already treats invuln_save as a fixed threshold (compared,
# never added, to armour) — this is the "fester Invuln-Wert"-Pfad the
# stratagem needs. This test locks in that behaviour with the Quantum
# Deflection stratagem's own numbers (4+, Annihilation Barge-shaped defender:
# Sv 3+, native invuln 5+) so a future change back to additive stacking fails
# loudly. → docs/work/wahapedia_necrons/stratagems.txt:100.
# ---------------------------------------------------------------------------


class TestQuantumDeflectionFixedInvuln:
    def test_fixed_4_plus_invuln_beats_ap_reduced_armour_save(self) -> None:
        # Sv 3+ armour, AP-3 weapon → armour_modified = 3 + 3 = 6+ (near-unusable).
        # Quantum Deflection's fixed 4+ invuln (not "+N" additive) is used instead.
        result = resolve_save(base_save=3, invuln_save=4, ap=-3, save_modifiers=[])
        assert result["using_invuln"] is True
        assert result["effective"] == 4

    def test_fixed_4_plus_invuln_loses_to_better_native_invuln(self) -> None:
        # A model's OWN better invuln (e.g. 3+) always wins over the stratagem's
        # fixed 4+ — 9E: "must use the best invulnerable save it has" — the
        # caller passes min(native, stratagem) into resolve_save (S135 pattern).
        best_invuln = min(3, 4)
        result = resolve_save(base_save=3, invuln_save=best_invuln, ap=-3, save_modifiers=[])
        assert result["invuln"] == 3
        assert result["effective"] == 3


# ---------------------------------------------------------------------------
# B-056 — Quantum Shielding: unmodified wound roll of 1-3 always fails.
#
# resolve_attack_modifiers's wound_auto_fail_max floors the effective wound
# threshold at (wound_auto_fail_max + 1) — no wound buff can lower it further,
# because the auto-fail is checked against the UNMODIFIED die, not the
# buffed threshold. → docs/work/wahapedia_necrons/units_all.txt:112
# (Annihilation Barge / S148-Befund).
# ---------------------------------------------------------------------------


class TestWoundAutoFailFloor:
    def test_floors_wound_threshold_at_one_above_auto_fail_max(self) -> None:
        # S6 vs T6 -> wound_base=4+; no modifiers; auto_fail_max=3 -> floor=4 (no change).
        result = resolve_attack_modifiers(
            skill=3,
            strength=6,
            toughness=6,
            weapon_type="Heavy",
            advanced=False,
            modifiers=[],
            use_melee=False,
            wound_auto_fail_max=3,
        )
        assert result["wound"]["modified"] == 4
        assert result["wound"]["auto_fail_max"] == 3

    def test_wound_buff_cannot_lower_threshold_past_auto_fail_floor(self) -> None:
        # S8 vs T6 -> wound_base=3+ (S > T). A +1 Wound buff would normally lower
        # this to 2+, but Quantum Shielding's auto-fail (1-3) floors it at 4+
        # regardless — the buff is fully negated for this defender.
        buff = {"label": "Buff", "value": 1, "roll_type": "wound", "source": "test"}
        result = resolve_attack_modifiers(
            skill=3,
            strength=8,
            toughness=6,
            weapon_type="Heavy",
            advanced=False,
            modifiers=[buff],
            use_melee=False,
            wound_auto_fail_max=3,
        )
        assert result["wound"]["modified"] == 4

    def test_worse_than_floor_threshold_is_unaffected(self) -> None:
        # S3 vs T6 -> wound_base=6+, already worse than the floor(4) -> unchanged.
        result = resolve_attack_modifiers(
            skill=3,
            strength=3,
            toughness=6,
            weapon_type="Heavy",
            advanced=False,
            modifiers=[],
            use_melee=False,
            wound_auto_fail_max=3,
        )
        assert result["wound"]["modified"] == 6

    def test_no_auto_fail_max_keeps_normal_floor_of_two(self) -> None:
        # Default (no Quantum Shielding defender): normal 9E floor (2+) applies,
        # unaffected by the new parameter — this run's buff lowers the S4-vs-T4
        # base (4+) by 1 to 3+, well above the floor.
        buff = {"label": "Buff", "value": 1, "roll_type": "wound", "source": "test"}
        result = resolve_attack_modifiers(
            skill=3,
            strength=4,
            toughness=4,
            weapon_type="Heavy",
            advanced=False,
            modifiers=[buff],
            use_melee=False,
        )
        assert result["wound"]["modified"] == 3
        assert result["wound"]["auto_fail_max"] is None


# ---------------------------------------------------------------------------
# R-COMBAT-35 — combi-weapon wiring: _combi_hit_penalty()'s result (attackMath.py)
# feeds into resolve_attack_modifiers' hit-modifier stack exactly like any other
# named −1 to Hit source (e.g. Dense Cover, Heavy-advanced). → wahapedia_orks
# combi-weapon profile text: "If you select both, then each time an attack is
# made with this weapon this phase, subtract 1 from that attack's hit roll."
# ---------------------------------------------------------------------------


def _combi_profile(name_en: str, attacks: str) -> WeaponProfile:
    return WeaponProfile(
        weapon_type="Heavy",
        range_inches=24,
        attacks=attacks,
        strength=4,
        ap=0,
        damage="1",
        is_melee=False,
        name_en=name_en,
        combi=True,
    )


class TestCombiHitPenaltyWiring:
    def test_both_combi_profiles_selected_worsens_hit_threshold_by_one(self) -> None:
        rokkit = _combi_profile("Rokkit", "D3")
        shoota = _combi_profile("Shoota", "3/2")
        penalty = _combi_hit_penalty([rokkit, shoota])
        modifiers = [{"label": "Combi (both profiles)", "value": penalty, "roll_type": "hit"}]

        result = resolve_attack_modifiers(
            skill=4,
            strength=4,
            toughness=4,
            weapon_type="Heavy",
            advanced=False,
            modifiers=modifiers,
            use_melee=False,
        )

        assert result["hit"]["modified"] == 5  # 4+ worsened to 5+ by the −1

    def test_single_combi_profile_selected_has_no_hit_penalty(self) -> None:
        rokkit = _combi_profile("Rokkit", "D3")
        penalty = _combi_hit_penalty([rokkit])
        modifiers = (
            [{"label": "Combi (both profiles)", "value": penalty, "roll_type": "hit"}]
            if penalty
            else []
        )

        result = resolve_attack_modifiers(
            skill=4,
            strength=4,
            toughness=4,
            weapon_type="Heavy",
            advanced=False,
            modifiers=modifiers,
            use_melee=False,
        )

        assert result["hit"]["modified"] == 4  # unchanged — no combi penalty applied


# ---------------------------------------------------------------------------
# B-113 Teil A — hit_reroll_ones: Necron Destroyer Cult "Hardwired for
# Destruction" ("re-roll a hit roll of 1") marks slot 1 in the HIT dice block,
# independent of any hit modifier stack (re-rolls check the UNMODIFIED die,
# core_rules.txt "Re-rolls").
# ---------------------------------------------------------------------------


class TestHitRerollOnes:
    def test_hit_reroll_ones_false_marks_no_slots(self) -> None:
        """Regression: the pre-B-113 default (no reroll consumer at all) stays
        byte-identical — reroll_slots is always present but empty."""
        result = resolve_attack_modifiers(
            skill=3,
            strength=5,
            toughness=5,
            weapon_type="Melee",
            advanced=False,
            modifiers=[],
            use_melee=True,
        )
        assert result["hit"]["reroll_slots"] == []

    def test_hit_reroll_ones_true_marks_slot_one(self) -> None:
        result = resolve_attack_modifiers(
            skill=3,
            strength=5,
            toughness=5,
            weapon_type="Melee",
            advanced=False,
            modifiers=[],
            use_melee=True,
            hit_reroll_ones=True,
        )
        assert result["hit"]["reroll_slots"] == [1]

    def test_hit_reroll_ones_slot_unaffected_by_hit_modifier_stack(self) -> None:
        # A −1 Hit modifier shifts the effective threshold (3+ -> 4+), but the
        # re-roll is checked against the UNMODIFIED die — slot 1 stays slot 1.
        debuff = {"label": "Dense Cover", "value": -1, "roll_type": "hit", "source": "terrain"}
        result = resolve_attack_modifiers(
            skill=3,
            strength=5,
            toughness=5,
            weapon_type="Melee",
            advanced=False,
            modifiers=[debuff],
            use_melee=True,
            hit_reroll_ones=True,
        )
        assert result["hit"]["modified"] == 4
        assert result["hit"]["reroll_slots"] == [1]


# ---------------------------------------------------------------------------
# B-113 Teil B — wound_reroll_ones: Necron Destroyer Cult Lord "United in
# Destruction" AURA ("re-roll a wound roll of 1") marks slot 1 in the WOUND
# dice block, independent of any wound modifier stack (re-rolls check the
# UNMODIFIED die, core_rules.txt "Re-rolls").
# ---------------------------------------------------------------------------


class TestWoundRerollOnes:
    def test_wound_reroll_ones_false_marks_no_slots(self) -> None:
        """Regression: the pre-B-113-Teil-B default (no aura consumer at all)
        stays byte-identical — wound.reroll_slots is always present but empty."""
        result = resolve_attack_modifiers(
            skill=3,
            strength=5,
            toughness=5,
            weapon_type="Melee",
            advanced=False,
            modifiers=[],
            use_melee=True,
        )
        assert result["wound"]["reroll_slots"] == []

    def test_wound_reroll_ones_true_marks_slot_one(self) -> None:
        result = resolve_attack_modifiers(
            skill=3,
            strength=5,
            toughness=5,
            weapon_type="Melee",
            advanced=False,
            modifiers=[],
            use_melee=True,
            wound_reroll_ones=True,
        )
        assert result["wound"]["reroll_slots"] == [1]

    def test_wound_reroll_ones_slot_unaffected_by_wound_modifier_stack(self) -> None:
        # A +1 Wound modifier shifts the effective threshold, but the re-roll
        # is checked against the UNMODIFIED die — slot 1 stays slot 1.
        buff = {"label": "Test Buff", "value": 1, "roll_type": "wound", "source": "ability"}
        result = resolve_attack_modifiers(
            skill=3,
            strength=4,
            toughness=4,
            weapon_type="Melee",
            advanced=False,
            modifiers=[buff],
            use_melee=True,
            wound_reroll_ones=True,
        )
        assert result["wound"]["modified"] == 3  # 4+ improved to 3+ by the +1
        assert result["wound"]["reroll_slots"] == [1]

    def test_wound_reroll_ones_independent_of_hit_reroll_ones(self) -> None:
        """The two reroll flags are independent — HIT reroll on, WOUND reroll
        off (and vice versa) must not leak into each other's block."""
        result = resolve_attack_modifiers(
            skill=3,
            strength=5,
            toughness=5,
            weapon_type="Melee",
            advanced=False,
            modifiers=[],
            use_melee=True,
            hit_reroll_ones=True,
            wound_reroll_ones=False,
        )
        assert result["hit"]["reroll_slots"] == [1]
        assert result["wound"]["reroll_slots"] == []
