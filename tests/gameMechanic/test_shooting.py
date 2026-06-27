"""Tests for shootingPhase.py — Ziel 3c: can_shoot() + integration smoke tests."""

from __future__ import annotations

import sys
from pathlib import Path
from unittest.mock import MagicMock, patch

sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

from gameMechanic.ability_engine import get_active_round_choice_shoot_after_fall_back
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
# can_shoot — Conquering Tyrant D2 (shoot_after_fall_back) exemption
# ---------------------------------------------------------------------------

_D2_ENGINE_PATH = "gameMechanic.shootingPhase.get_active_round_choice_shoot_after_fall_back"


class TestCanShootD2FallBackExemption:
    """Conquering Tyrant D2 allows a retreated unit to shoot (−1 Hit, Class A)."""

    def _retreated_state(self) -> dict:
        return {"turn_flags": {"retreated": True}, "in_melee": False, "in_reserve": False}

    def test_retreated_unit_with_active_d2_can_shoot(self):
        # D2 active: get_active_round_choice_shoot_after_fall_back returns −1 → exempt.
        with patch(_D2_ENGINE_PATH, return_value=-1):
            assert can_shoot(self._retreated_state(), faction="Necrons", uid="uid-overlord") is True

    def test_retreated_unit_without_d2_cannot_shoot(self):
        # D2 inactive: no exemption → normal retreated block applies.
        with patch(_D2_ENGINE_PATH, return_value=0):
            assert (
                can_shoot(self._retreated_state(), faction="Necrons", uid="uid-overlord") is False
            )

    def test_retreated_unit_without_faction_uid_cannot_shoot(self):
        # No faction/uid provided → D2 lookup skipped → retreated block applies.
        # Regression guard: old call sites without faction/uid remain safe.
        assert can_shoot(self._retreated_state()) is False

    def test_d2_minus_one_hit_modifier_is_returned_when_retreated(self):
        # Verifies that get_active_round_choice_shoot_after_fall_back returns −1
        # when movement_choice == "retreated" and D2 is active — the value that
        # _common.py folds into the hit modifier row (9E canonical −1 Hit).
        # Patches both ability_engine.st and game_state.st so the dict-based
        # session state reaches all layers without a live Streamlit runtime.
        import gameMechanic.ability_engine as _eng
        import gameMechanic.game_state as _gs

        session = {
            "first_player": "Necrons",
            "p1_faction_dir": "necrons",
            "p2_faction_dir": "necrons",
            "round_choice_active_Necrons": "wh40k_9e.necrons.faction.protocol_conquering_tyrant",
            "round_choice_directive_Necrons": "secondary",
            "round_choice_assignments": {},
            "p1_units": {"uid-overlord": {"movement_choice": "retreated"}},
        }
        st_mock = MagicMock()
        st_mock.session_state = session
        with patch.object(_eng, "st", st_mock), patch.object(_gs, "st", st_mock):
            result = get_active_round_choice_shoot_after_fall_back("Necrons", "uid-overlord")
        assert (
            result == -1
        ), "D2 must return −1 when movement_choice == 'retreated' and directive is active"


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
