"""Tests for fightPhase.py — Ziel 3c: can_fight() + integration smoke tests."""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

from gameMechanic.combat import AttackParams, DefendParams, resolve_attack
from gameMechanic.fightPhase import can_fight

# ---------------------------------------------------------------------------
# can_fight — pure-function tests
# ---------------------------------------------------------------------------


class TestCanFight:
    def _state(self, in_melee: bool = False, **flags) -> dict:
        return {"turn_flags": flags, "in_melee": in_melee}

    def test_default_unit_cannot_fight(self):
        assert can_fight(self._state()) is False

    def test_in_melee_can_fight(self):
        assert can_fight(self._state(in_melee=True)) is True

    def test_charged_can_fight(self):
        assert can_fight(self._state(charged=True)) is True

    def test_in_melee_and_charged(self):
        assert can_fight(self._state(in_melee=True, charged=True)) is True

    def test_advanced_not_in_melee_cannot_fight(self):
        assert can_fight(self._state(advanced=True)) is False

    def test_retreated_not_in_melee_cannot_fight(self):
        assert can_fight(self._state(retreated=True)) is False

    def test_empty_state_cannot_fight(self):
        assert can_fight({"turn_flags": {}}) is False

    def test_in_reserve_cannot_fight(self):
        assert can_fight({"turn_flags": {}, "in_melee": False, "in_reserve": True}) is False

    def test_stationary_not_in_melee_cannot_fight(self):
        assert can_fight(self._state(advanced=False, retreated=False)) is False

    def test_charged_takes_priority_over_advanced(self):
        # Charged units are always eligible regardless of other flags.
        assert can_fight(self._state(charged=True, advanced=True)) is True


# ---------------------------------------------------------------------------
# Integration smoke tests — resolve_attack with typical melee profiles
# ---------------------------------------------------------------------------


class TestFightSmoke:
    def test_hyperphase_sword_1hit_1wound_1failed_save(self):
        """Overlord Hyperphase Sword: S6, AP-3, D2 vs T4 Sv4+."""
        params = AttackParams(attacks=4, skill=2, strength=6, ap=-3, damage=2)
        defender = DefendParams(toughness=4, save=4, wounds=2)
        damage, log = resolve_attack(
            params, defender, hits_rolled=2, wounds_rolled=1, saves_failed=1
        )
        assert damage == 2

    def test_mwbd_hit_modifier_applied(self):
        params = AttackParams(attacks=4, skill=2, strength=6, ap=-3, damage=2, mwbd_active=True)
        defender = DefendParams(toughness=4, save=4, wounds=2)
        damage, log = resolve_attack(
            params, defender, hits_rolled=3, wounds_rolled=2, saves_failed=2
        )
        assert damage == 4
        assert any("MWBD" in line for line in log)

    def test_invuln_better_than_armour(self):
        """AP-3 vs 5++ invuln: armour 3+3=6+ → invuln 5+ applies."""
        params = AttackParams(attacks=4, skill=2, strength=6, ap=-3, damage=2)
        defender = DefendParams(toughness=4, save=3, wounds=2, invul_save=5)
        damage, log = resolve_attack(
            params, defender, hits_rolled=2, wounds_rolled=2, saves_failed=1
        )
        assert any("Invuln" in line for line in log)

    def test_no_melee_wounds_no_damage(self):
        params = AttackParams(attacks=3, skill=3, strength=4, ap=-1, damage=1)
        defender = DefendParams(toughness=4, save=3, wounds=1)
        damage, log = resolve_attack(params, defender, hits_rolled=2, wounds_rolled=0)
        assert damage == 0

    def test_fnp_reduces_melee_damage(self):
        """3 failed saves, 2 FNP saved → 1 wound through."""
        params = AttackParams(attacks=5, skill=3, strength=5, ap=-1, damage=1)
        defender = DefendParams(toughness=4, save=4, wounds=1, fnp=5)
        damage, log = resolve_attack(
            params, defender, hits_rolled=4, wounds_rolled=3, saves_failed=3, fnp_saved=2
        )
        assert damage == 1
