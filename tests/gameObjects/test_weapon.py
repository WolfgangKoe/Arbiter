"""Tests for gameObjects/weapon.py — Weapon properties and for_phase()."""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

from gameObjects.weapon import Weapon, WeaponProfile  # noqa: E402

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _profile(
    weapon_type: str = "Rapid Fire",
    is_melee: bool = False,
    range_inches: int = 24,
    attacks: str = "1",
    strength: int = 4,
    ap: int = 0,
    damage: str = "1",
    abilities: str = "",
) -> WeaponProfile:
    return WeaponProfile(
        weapon_type=weapon_type,
        range_inches=range_inches,
        attacks=attacks,
        strength=strength,
        ap=ap,
        damage=damage,
        is_melee=is_melee,
        abilities=abilities,
    )


def _melee_profile(**kw: object) -> WeaponProfile:
    return _profile(weapon_type="Melee", is_melee=True, range_inches=0, **kw)  # type: ignore[arg-type]


def _pistol_profile(**kw: object) -> WeaponProfile:
    return _profile(weapon_type="Pistol 1", is_melee=False, **kw)  # type: ignore[arg-type]


# ---------------------------------------------------------------------------
# Properties with profiles present
# ---------------------------------------------------------------------------


class TestWeaponPropertiesWithProfiles:
    def _w(self) -> Weapon:
        p = _profile(
            weapon_type="Rapid Fire",
            range_inches=24,
            attacks="3",
            strength=5,
            ap=-1,
            damage="2",
            abilities="Blast",
        )
        return Weapon(id="test.weapon", name_en="Test Gun", profiles=[p])

    def test_is_melee_false_for_ranged(self) -> None:
        assert self._w().is_melee is False

    def test_range_inches(self) -> None:
        assert self._w().range_inches == 24

    def test_attacks(self) -> None:
        assert self._w().attacks == "3"

    def test_strength(self) -> None:
        assert self._w().strength == 5

    def test_ap(self) -> None:
        assert self._w().ap == -1

    def test_damage(self) -> None:
        assert self._w().damage == "2"

    def test_abilities(self) -> None:
        assert self._w().abilities == "Blast"


# ---------------------------------------------------------------------------
# Properties when profiles is empty (else branches)
# ---------------------------------------------------------------------------


class TestWeaponPropertiesEmpty:
    def _empty(self) -> Weapon:
        return Weapon(id="empty", name_en="Empty", profiles=[])

    def test_is_melee_false_when_no_profiles(self) -> None:
        assert self._empty().is_melee is False

    def test_range_inches_zero_when_no_profiles(self) -> None:
        assert self._empty().range_inches == 0

    def test_attacks_zero_when_no_profiles(self) -> None:
        assert self._empty().attacks == "0"

    def test_strength_zero_when_no_profiles(self) -> None:
        assert self._empty().strength == 0

    def test_ap_zero_when_no_profiles(self) -> None:
        assert self._empty().ap == 0

    def test_damage_zero_when_no_profiles(self) -> None:
        assert self._empty().damage == "0"

    def test_abilities_empty_when_no_profiles(self) -> None:
        assert self._empty().abilities == ""


# ---------------------------------------------------------------------------
# for_phase()
# ---------------------------------------------------------------------------


class TestWeaponForPhase:
    def test_selects_ranged_profile(self) -> None:
        ranged = _profile()
        melee = _melee_profile()
        w = Weapon(id="dual", name_en="Dual", profiles=[ranged, melee])
        assert w.for_phase(use_melee=False) is ranged

    def test_selects_melee_profile(self) -> None:
        ranged = _profile()
        melee = _melee_profile()
        w = Weapon(id="dual", name_en="Dual", profiles=[ranged, melee])
        assert w.for_phase(use_melee=True) is melee

    def test_falls_back_to_first_profile_when_no_match(self) -> None:
        p1 = _profile(is_melee=False)
        p2 = _profile(is_melee=False)
        w = Weapon(id="ranged_only", name_en="Ranged Only", profiles=[p1, p2])
        assert w.for_phase(use_melee=True) is p1

    def test_single_ranged_profile_returned_for_ranged(self) -> None:
        p = _profile()
        w = Weapon(id="w", name_en="W", profiles=[p])
        assert w.for_phase(use_melee=False) is p

    def test_single_melee_profile_returned_for_melee(self) -> None:
        p = _melee_profile()
        w = Weapon(id="w", name_en="W", profiles=[p])
        assert w.for_phase(use_melee=True) is p
