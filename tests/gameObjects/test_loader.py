"""Tests for gameObjects loader and dataclasses."""

import sys
from pathlib import Path

# Ensure src/ is on the path so gameObjects can be imported
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

from gameObjects.loader import (
    load_army,
    load_detachment_types,
    load_faction_abilities,
    load_unit_catalog,
)


def test_load_necron_army_returns_all_catalog_units() -> None:
    units, _ = load_army("necrons")
    assert len(units) >= 51


def test_overlord_loaded_from_catalog() -> None:
    units, _ = load_army("necrons")
    overlord = next(u for u in units if u.id == "wh40k_9e.necrons.unit.overlord")
    assert overlord.name_en == "Overlord"
    assert overlord.toughness == 5
    assert overlord.wounds == 5


def test_overlord_has_staff_of_light() -> None:
    units, _ = load_army("necrons")
    overlord = next(u for u in units if u.id == "wh40k_9e.necrons.unit.overlord")
    assert len(overlord.weapons) == 1
    staff = overlord.weapons[0]
    assert staff.name_en == "Staff of Light"
    shooting = next(p for p in staff.profiles if not p.is_melee)
    melee = next(p for p in staff.profiles if p.is_melee)
    assert shooting.is_melee is False
    assert melee.is_melee is True


def test_warriors_models_and_save() -> None:
    units, _ = load_army("necrons")
    warriors = next(u for u in units if u.id == "wh40k_9e.necrons.unit.warriors")
    assert warriors.models_max == 20
    assert warriors.save == 4


def test_load_ork_army_returns_units() -> None:
    units, _ = load_army("orks")
    assert len(units) == 8


def test_load_necron_faction_abilities_returns_at_least_one() -> None:
    abilities = load_faction_abilities("necrons")
    assert len(abilities) >= 1


def test_living_metal_ability_id_and_trigger() -> None:
    abilities = load_faction_abilities("necrons")
    living_metal = next(a for a in abilities if a.id == "wh40k_9e.necrons.faction.living_metal")
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


def test_overlord_power_level_and_attacks() -> None:
    units, _ = load_army("necrons")
    overlord = next(u for u in units if u.id == "wh40k_9e.necrons.unit.overlord")
    assert overlord.power_level == 6
    assert overlord.attacks == 4


def test_overlord_wargear_options_parsed() -> None:
    units, _ = load_army("necrons")
    overlord = next(u for u in units if u.id == "wh40k_9e.necrons.unit.overlord")
    assert len(overlord.wargear_options) == 5
    replace_opts = [o for o in overlord.wargear_options if o.type == "replace"]
    add_opts = [o for o in overlord.wargear_options if o.type == "add"]
    assert len(replace_opts) == 4
    assert len(add_opts) == 1
    assert add_opts[0].item == "wh40k_9e.necrons.wargear.resurrection_orb"


def test_triarch_stalker_damage_bracket() -> None:
    units, _ = load_army("necrons")
    stalker = next(u for u in units if u.id == "wh40k_9e.necrons.unit.triarch_stalker")
    assert stalker.damage_bracket is not None
    assert len(stalker.damage_bracket) == 3
    top = stalker.damage_bracket[0]
    assert top.wounds_min == 7
    assert top.wounds_max == 12
    assert top.move == '10"'


def test_building_has_none_attacks_and_leadership() -> None:
    units, _ = load_army("necrons")
    cov = next(u for u in units if u.id == "wh40k_9e.necrons.unit.convergence_of_dominion")
    assert cov.attacks is None
    assert cov.leadership is None


def test_warriors_no_damage_bracket() -> None:
    units, _ = load_army("necrons")
    warriors = next(u for u in units if u.id == "wh40k_9e.necrons.unit.warriors")
    assert warriors.damage_bracket is None


def test_load_unit_catalog_returns_dict_keyed_by_id() -> None:
    catalog = load_unit_catalog("necrons")
    assert isinstance(catalog, dict)
    assert "wh40k_9e.necrons.unit.overlord" in catalog
    assert catalog["wh40k_9e.necrons.unit.overlord"].name_en == "Overlord"


def test_triarch_stalker_replace_heat_ray_wargear_options() -> None:
    units, _ = load_army("necrons")
    stalker = next(u for u in units if u.id == "wh40k_9e.necrons.unit.triarch_stalker")
    heat_ray_opts = [
        o for o in stalker.wargear_options if o.replaces == "wh40k_9e.necrons.weapon.heat_ray"
    ]
    assert len(heat_ray_opts) == 2
    targets = {o.with_refs[0] for o in heat_ray_opts}
    assert "wh40k_9e.necrons.weapon.twin_heavy_gauss_cannon" in targets
    assert "wh40k_9e.necrons.weapon.particle_shredder" in targets
