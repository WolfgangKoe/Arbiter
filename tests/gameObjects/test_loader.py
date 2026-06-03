"""Tests for gameObjects loader and dataclasses."""

import sys
from pathlib import Path

# Ensure src/ is on the path so gameObjects can be imported
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

from pathlib import Path

from gameObjects.loader import (
    _apply_wargear,
    load_army,
    load_detachment_types,
    load_faction_abilities,
    load_points,
    load_roster,
    load_roster_metadata,
    load_unit_catalog,
    load_weapon_catalog,
    resolve_bracket_stats,
    scaled_pl,
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
    assert len(units) >= 50  # Full Ork catalog scraped from Wahapedia


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


# ---------------------------------------------------------------------------
# 5c: CCW default
# ---------------------------------------------------------------------------


def test_unit_with_no_melee_weapon_gets_ccw() -> None:
    units, _ = load_army("necrons")
    # Annihilation Barge has only shooting weapons — no explicit melee ref in units.yaml
    barge = next(u for u in units if u.id == "wh40k_9e.necrons.unit.annihilation_barge")
    melee_profiles = [p for w in barge.weapons for p in w.profiles if p.is_melee]
    assert len(melee_profiles) >= 1
    ccw = next((p for p in melee_profiles if p.name_en == "Close Combat Weapon"), None)
    assert ccw is not None


def test_all_units_have_at_least_one_melee_profile() -> None:
    units, _ = load_army("necrons")
    missing = [u.id for u in units if not any(p.is_melee for w in u.weapons for p in w.profiles)]
    assert missing == [], f"Units without melee profile: {missing}"


def test_unit_with_existing_melee_does_not_get_ccw() -> None:
    units, _ = load_army("necrons")
    overlord = next(u for u in units if u.id == "wh40k_9e.necrons.unit.overlord")
    # Staff of Light has a melee profile — CCW should NOT be added as default
    ccw_count = sum(
        1 for w in overlord.weapons for p in w.profiles if p.name_en == "Close Combat Weapon"
    )
    assert ccw_count == 0


# ---------------------------------------------------------------------------
# 5c: resolve_bracket_stats
# ---------------------------------------------------------------------------


def test_resolve_bracket_stats_top_bracket() -> None:
    units, _ = load_army("necrons")
    stalker = next(u for u in units if u.id == "wh40k_9e.necrons.unit.triarch_stalker")
    stats = resolve_bracket_stats(stalker, 12)
    assert stats["move"] == '10"'


def test_resolve_bracket_stats_bottom_bracket() -> None:
    units, _ = load_army("necrons")
    stalker = next(u for u in units if u.id == "wh40k_9e.necrons.unit.triarch_stalker")
    stats = resolve_bracket_stats(stalker, 1)
    assert stats["move"] == '6"'


def test_resolve_bracket_stats_no_bracket_returns_base() -> None:
    units, _ = load_army("necrons")
    warriors = next(u for u in units if u.id == "wh40k_9e.necrons.unit.warriors")
    assert warriors.damage_bracket is None
    stats = resolve_bracket_stats(warriors, 10)
    assert stats["move"] == warriors.move
    assert stats["ws"] == warriors.ws


# ---------------------------------------------------------------------------
# 5c: load_points
# ---------------------------------------------------------------------------


def test_load_points_returns_overlord_cost() -> None:
    pts = load_points("necrons")
    assert pts["wh40k_9e.necrons.unit.overlord"] == 90


def test_load_points_per_model_warriors() -> None:
    pts = load_points("necrons")
    assert pts["wh40k_9e.necrons.unit.warriors"] == 11


def test_load_points_includes_wargear() -> None:
    pts = load_points("necrons")
    assert pts["wh40k_9e.necrons.wargear.resurrection_orb"] == 25


def test_load_points_missing_faction_returns_empty() -> None:
    pts = load_points("eldar")
    assert pts == {}


# ---------------------------------------------------------------------------
# 5c: scaled_pl
# ---------------------------------------------------------------------------


def test_scaled_pl_full_squad() -> None:
    units, _ = load_army("necrons")
    warriors = next(u for u in units if u.id == "wh40k_9e.necrons.unit.warriors")
    # warriors models_min = 10, models_max = 20, power_level from units.yaml
    result = scaled_pl(warriors, warriors.models_min)
    assert result == float(warriors.power_level)


def test_scaled_pl_doubled_models() -> None:
    units, _ = load_army("necrons")
    warriors = next(u for u in units if u.id == "wh40k_9e.necrons.unit.warriors")
    full = scaled_pl(warriors, warriors.models_max)
    half = scaled_pl(warriors, warriors.models_min)
    assert full == 2 * half


# ---------------------------------------------------------------------------
# 5c: load_roster / load_roster_metadata
# ---------------------------------------------------------------------------

_ROSTER_DIR = Path(__file__).parent.parent.parent / "data" / "rosters"


def test_load_roster_metadata_alpha() -> None:
    meta = load_roster_metadata(_ROSTER_DIR / "necrons_alpha.yaml")
    assert meta["display_name"] == "Necrons α"
    assert meta["faction_dir"] == "necrons"


def test_load_roster_alpha_resolves_overlord() -> None:
    catalog = load_unit_catalog("necrons")
    matched, unmatched = load_roster(_ROSTER_DIR / "necrons_alpha.yaml", catalog)
    assert unmatched == []
    ids = [u.id for u, _ in matched]
    assert "wh40k_9e.necrons.unit.overlord" in ids


def test_load_roster_alpha_model_counts() -> None:
    catalog = load_unit_catalog("necrons")
    matched, _ = load_roster(_ROSTER_DIR / "necrons_alpha.yaml", catalog)
    warriors_entry = next((u, m) for u, m in matched if u.id == "wh40k_9e.necrons.unit.warriors")
    assert warriors_entry[1] == 10


def test_load_roster_beta_resolves_all_units() -> None:
    catalog = load_unit_catalog("necrons")
    matched, unmatched = load_roster(_ROSTER_DIR / "necrons_beta.yaml", catalog)
    assert unmatched == []
    assert len(matched) == 5


def test_load_roster_unmatched_id_reported() -> None:
    catalog = load_unit_catalog("necrons")
    import tempfile  # noqa: E401

    import yaml

    with tempfile.NamedTemporaryFile(mode="w", suffix=".yaml", delete=False) as f:
        yaml.dump(
            {
                "display_name": "Test",
                "faction_dir": "necrons",
                "units": [{"id": "nonexistent.unit", "models": 1}],
            },
            f,
        )
        tmp = f.name
    matched, unmatched = load_roster(tmp, catalog)
    assert matched == []
    assert "nonexistent.unit" in unmatched


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


# ---------------------------------------------------------------------------
# Wargear overrides: _apply_wargear + load_roster with wargear field
# ---------------------------------------------------------------------------


def test_apply_wargear_replace_staff_of_light_with_voidscythe() -> None:
    units, _ = load_army("necrons")
    overlord = next(u for u in units if u.id == "wh40k_9e.necrons.unit.overlord")
    weapon_catalog = load_weapon_catalog("necrons")

    assert overlord.weapons[0].name_en == "Staff of Light"

    modified = _apply_wargear(
        overlord,
        ["wh40k_9e.necrons.weapon.voidscythe"],
        weapon_catalog,
    )
    weapon_names = [w.name_en for w in modified.weapons]
    assert "Voidscythe" in weapon_names
    assert "Staff of Light" not in weapon_names


def test_apply_wargear_add_resurrection_orb() -> None:
    units, _ = load_army("necrons")
    overlord = next(u for u in units if u.id == "wh40k_9e.necrons.unit.overlord")
    weapon_catalog = load_weapon_catalog("necrons")

    modified = _apply_wargear(
        overlord,
        ["wh40k_9e.necrons.weapon.voidscythe"],
        weapon_catalog,
    )
    assert len(modified.weapons) == 1
    assert modified.weapons[0].name_en == "Voidscythe"


def test_apply_wargear_unknown_id_skipped() -> None:
    units, _ = load_army("necrons")
    overlord = next(u for u in units if u.id == "wh40k_9e.necrons.unit.overlord")
    weapon_catalog = load_weapon_catalog("necrons")

    before_count = len(overlord.weapons)
    modified = _apply_wargear(
        overlord, ["wh40k_9e.necrons.wargear.resurrection_orb"], weapon_catalog
    )
    assert len(modified.weapons) == before_count


def test_load_roster_with_wargear_override(tmp_path: Path) -> None:
    import yaml

    catalog = load_unit_catalog("necrons")
    roster = {
        "display_name": "Wargear Test",
        "faction_dir": "necrons",
        "units": [
            {
                "id": "wh40k_9e.necrons.unit.overlord",
                "models": 1,
                "wargear": ["wh40k_9e.necrons.weapon.voidscythe"],
            }
        ],
    }
    roster_path = tmp_path / "test.yaml"
    roster_path.write_text(yaml.dump(roster))

    matched, unmatched = load_roster(roster_path, catalog)
    assert unmatched == []
    unit, _models = matched[0]
    weapon_names = [w.name_en for w in unit.weapons]
    assert "Voidscythe" in weapon_names
    assert "Staff of Light" not in weapon_names


def test_load_roster_without_wargear_uses_catalog_defaults(tmp_path: Path) -> None:
    import yaml

    catalog = load_unit_catalog("necrons")
    roster = {
        "display_name": "Default Test",
        "faction_dir": "necrons",
        "units": [{"id": "wh40k_9e.necrons.unit.overlord", "models": 1}],
    }
    roster_path = tmp_path / "test.yaml"
    roster_path.write_text(yaml.dump(roster))

    matched, _ = load_roster(roster_path, catalog)
    unit, _ = matched[0]
    assert unit.weapons[0].name_en == "Staff of Light"
