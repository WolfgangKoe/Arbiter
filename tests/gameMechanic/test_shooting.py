"""Tests for shootingPhase.py — Ziel 3c: can_shoot() + integration smoke tests."""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

from unittest.mock import MagicMock

from gameMechanic.combat import AttackParams, DefendParams, resolve_attack
from gameMechanic.shootingPhase import can_shoot

# ---------------------------------------------------------------------------
# can_shoot — pure-function tests
# ---------------------------------------------------------------------------


class TestCanShoot:
    def _state(self, in_melee: bool = False, in_reserve: bool = False, **flags) -> dict:
        return {"turn_flags": flags, "in_melee": in_melee, "in_reserve": in_reserve}

    def test_default_unit_can_shoot(self):
        assert can_shoot(self._state()) is True

    def test_advanced_cannot_shoot(self):
        assert can_shoot(self._state(advanced=True)) is False

    def test_retreated_cannot_shoot(self):
        assert can_shoot(self._state(retreated=True)) is False

    def test_in_melee_cannot_shoot(self):
        assert can_shoot(self._state(in_melee=True)) is False

    def test_in_reserve_cannot_shoot(self):
        assert can_shoot(self._state(in_reserve=True)) is False

    def test_charged_can_still_shoot(self):
        assert can_shoot(self._state(charged=True)) is True

    def test_stationary_can_shoot(self):
        assert can_shoot(self._state(advanced=False, retreated=False)) is True

    def test_empty_flags_can_shoot(self):
        assert can_shoot({"turn_flags": {}}) is True

    def test_advanced_and_in_melee_cannot_shoot(self):
        assert can_shoot(self._state(in_melee=True, advanced=True)) is False

    def test_in_reserve_takes_priority(self):
        # Even with no blocking flags, in_reserve blocks shooting.
        assert can_shoot({"turn_flags": {}, "in_reserve": True}) is False

    def test_already_shot_cannot_shoot(self):
        assert can_shoot(self._state(shot=True)) is False

    def test_pistol_in_melee_can_shoot(self):
        profile = MagicMock()
        profile.weapon_type = "Pistol 1"
        weapon = MagicMock()
        weapon.profiles = [profile]
        unit = MagicMock()
        unit.has_keyword.return_value = False
        unit.weapons = [weapon]
        assert can_shoot(self._state(in_melee=True), unit) is True

    def test_no_pistol_infantry_in_melee_cannot_shoot(self):
        profile = MagicMock()
        profile.weapon_type = "Rapid Fire"
        weapon = MagicMock()
        weapon.profiles = [profile]
        unit = MagicMock()
        unit.has_keyword.return_value = False
        unit.weapons = [weapon]
        assert can_shoot(self._state(in_melee=True), unit) is False


# ---------------------------------------------------------------------------
# Integration smoke tests — resolve_attack called with typical ranged profiles
# ---------------------------------------------------------------------------


class TestShootingSmoke:
    def test_gauss_flayer_3hits_2wounds_1failed_save(self):
        """Gauss Flayer: S4, AP0, D1 vs T4 Sv4+."""
        params = AttackParams(attacks=1, skill=4, strength=4, ap=0, damage=1)
        defender = DefendParams(toughness=4, save=4, wounds=1)
        damage, log = resolve_attack(
            params, defender, hits_rolled=3, wounds_rolled=2, saves_failed=1
        )
        assert damage == 1
        assert len(log) > 0

    def test_no_hits_ends_attack(self):
        params = AttackParams(attacks=1, skill=4, strength=4, ap=0, damage=1)
        defender = DefendParams(toughness=4, save=4, wounds=1)
        damage, log = resolve_attack(params, defender, hits_rolled=0)
        assert damage == 0
        assert any("No hits" in line for line in log)

    def test_no_wounds_ends_attack(self):
        params = AttackParams(attacks=1, skill=4, strength=4, ap=0, damage=1)
        defender = DefendParams(toughness=4, save=4, wounds=1)
        damage, log = resolve_attack(params, defender, hits_rolled=3, wounds_rolled=0)
        assert damage == 0
        assert any("No wounds" in line for line in log)

    def test_all_saves_pass(self):
        params = AttackParams(attacks=1, skill=4, strength=4, ap=0, damage=1)
        defender = DefendParams(toughness=4, save=4, wounds=1)
        damage, log = resolve_attack(
            params, defender, hits_rolled=3, wounds_rolled=2, saves_failed=0
        )
        assert damage == 0
        assert any("All saves passed" in line for line in log)

    def test_heavy_weapon_ap_minus3(self):
        """Gauss Cannon: S6, AP-3, D3 (fixed as 3) vs T4 Sv3+."""
        params = AttackParams(attacks=1, skill=4, strength=6, ap=-3, damage=3)
        defender = DefendParams(toughness=4, save=3, wounds=3)
        damage, log = resolve_attack(
            params, defender, hits_rolled=1, wounds_rolled=1, saves_failed=1
        )
        assert damage == 3

    def test_invuln_save_shown_in_log(self):
        """AP-3 weapon vs 4++ invuln — invuln beats degraded armour."""
        params = AttackParams(attacks=1, skill=4, strength=6, ap=-3, damage=2)
        defender = DefendParams(toughness=4, save=3, wounds=2, invul_save=4)
        damage, log = resolve_attack(
            params, defender, hits_rolled=2, wounds_rolled=2, saves_failed=1
        )
        # Invuln (4+) vs armour (3+3=6+) → invuln wins.
        assert any("Invuln" in line for line in log)

    def test_mwbd_logged(self):
        params = AttackParams(attacks=1, skill=4, strength=4, ap=0, damage=1, mwbd_active=True)
        defender = DefendParams(toughness=4, save=4, wounds=1)
        damage, log = resolve_attack(
            params, defender, hits_rolled=3, wounds_rolled=2, saves_failed=2
        )
        assert damage == 2
        assert any("MWBD" in line for line in log)

    def test_fnp_reduces_damage(self):
        params = AttackParams(attacks=1, skill=4, strength=4, ap=0, damage=1)
        defender = DefendParams(toughness=4, save=5, wounds=1, fnp=5)
        damage, log = resolve_attack(
            params, defender, hits_rolled=4, wounds_rolled=3, saves_failed=3, fnp_saved=2
        )
        assert damage == 1
        assert any("Feel No Pain" in line for line in log)
