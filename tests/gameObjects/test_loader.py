"""Tests for gameObjects loader and dataclasses."""

import sys
from pathlib import Path

# Ensure src/ is on the path so gameObjects can be imported
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

from gameObjects.loader import (
    load_army,
    load_detachment_types,
    load_faction_abilities,
)


def test_load_necron_army_returns_six_units() -> None:
    units = load_army("necrons")
    assert len(units) == 6


def test_overlord_name_and_stats() -> None:
    units = load_army("necrons")
    overlord = units[0]
    assert overlord.name_en == "Overlord (Warlord)"
    assert overlord.toughness == 5
    assert overlord.wounds == 5


def test_overlord_weapons_melee_flags() -> None:
    units = load_army("necrons")
    overlord = units[0]
    assert len(overlord.weapons) == 2
    assert overlord.weapons[0].is_melee is False
    assert overlord.weapons[1].is_melee is True


def test_warriors_models_and_save() -> None:
    units = load_army("necrons")
    warriors = units[1]
    assert warriors.models_max == 10
    assert warriors.save == 4


def test_load_ork_army_returns_eight_units() -> None:
    units = load_army("orks")
    assert len(units) == 8


def test_load_necron_faction_abilities_returns_at_least_one() -> None:
    abilities = load_faction_abilities("necrons")
    assert len(abilities) >= 1


def test_living_metal_ability_id_and_trigger() -> None:
    abilities = load_faction_abilities("necrons")
    living_metal = next(a for a in abilities if a.id == "necrons.faction.living_metal")
    assert living_metal.trigger.phase == "command"
    assert living_metal.conditions[0].has_rules == ["livingMetal"]


def test_load_detachment_types_returns_at_least_five() -> None:
    types = load_detachment_types()
    assert len(types) >= 5


def test_patrol_hq_slot_constraint() -> None:
    types = load_detachment_types()
    patrol = next(t for t in types if t.id == "patrol")
    hq_slot = next(s for s in patrol.slot_constraints if s.role == "HQ")
    assert hq_slot.min_units == 1
    assert hq_slot.max_units == 2
