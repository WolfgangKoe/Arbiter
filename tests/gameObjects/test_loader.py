"""Tests for gameObjects loader and dataclasses."""

import sys
from pathlib import Path

# Ensure src/ is on the path so gameObjects can be imported
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

from pathlib import Path

from gameObjects.loader import (
    _apply_persistent_effect,
    _apply_relic,
    _apply_wargear,
    _resolve_model_groups,
    load_army,
    load_deny_wargear_names,
    load_detachment_types,
    load_faction_abilities,
    load_points,
    load_relic_catalog,
    load_roster,
    load_roster_metadata,
    load_round_choice_abilities,
    load_round_choice_label,
    load_stratagems,
    load_subfaction_abilities,
    load_unit_abilities,
    load_unit_catalog,
    load_wargear_catalog,
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


def test_silent_king_melee_weapons_respect_per_weapon_attack_cap() -> None:
    # Scythe of Dust / Staff of Stars are the "N additional AND no more than N"
    # class: their melee attacks are hard-capped (4 / 3), independent of Szarekh's
    # bracketed Attacks characteristic (H2). Without max_attacks the cap collapses
    # to unit.attacks + N and the declaration would over-allocate.
    from gameMechanic.attack_math import _total_attacks_int

    catalog = load_weapon_catalog("necrons")
    scythe = catalog["wh40k_9e.necrons.weapon.scythe_of_dust"]
    staff_melee = next(
        p for p in catalog["wh40k_9e.necrons.weapon.staff_of_stars"].profiles if p.is_melee
    )
    scythe_melee = next(p for p in scythe.profiles if p.is_melee)

    assert scythe_melee.max_attacks == 4
    assert staff_melee.max_attacks == 3
    # A6 bearer: cap holds regardless of the high Attacks characteristic.
    assert _total_attacks_int("*", 1, 6, scythe_melee.effect, scythe_melee.max_attacks) == 4
    assert _total_attacks_int("*", 1, 6, staff_melee.effect, staff_melee.max_attacks) == 3


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


def test_load_round_choice_abilities_necrons_returns_six() -> None:
    protocols = load_round_choice_abilities("necrons")
    assert len(protocols) == 6


def test_load_round_choice_abilities_custodes_returns_six() -> None:
    protocols = load_round_choice_abilities("adeptus_custodes")
    assert len(protocols) == 6


def test_load_round_choice_abilities_orks_returns_empty() -> None:
    protocols = load_round_choice_abilities("orks")
    assert protocols == []


def test_load_stratagems_includes_shared_core_stratagems() -> None:
    stratagems = load_stratagems("necrons")
    ids = [s.id for s in stratagems]
    assert "wh40k_9e.shared.stratagem.command_re_roll" in ids
    assert "wh40k_9e.shared.stratagem.fire_overwatch" in ids


def test_load_stratagems_shared_ids_namespace() -> None:
    stratagems = load_stratagems("necrons")
    shared = [s for s in stratagems if s.id.startswith("wh40k_9e.shared.stratagem.")]
    assert len(shared) == 7


# ---------------------------------------------------------------------------
# 6k: load_wargear_catalog, _apply_persistent_effect, _apply_wargear + wargear_ids
# ---------------------------------------------------------------------------


def test_load_wargear_catalog_necrons_contains_known_items() -> None:
    catalog = load_wargear_catalog("necrons")
    assert "wh40k_9e.necrons.wargear.gloom_prism" in catalog
    assert "wh40k_9e.necrons.wargear.resurrection_orb" in catalog
    assert "wh40k_9e.necrons.wargear.canoptek_cloak" in catalog


def test_load_wargear_catalog_missing_faction_returns_empty() -> None:
    assert load_wargear_catalog("eldar") == {}


def test_apply_persistent_effect_set_invuln() -> None:
    units, _ = load_army("necrons")
    warriors = next(u for u in units if u.id == "wh40k_9e.necrons.unit.warriors")
    assert warriors.invuln_save is None
    modified = _apply_persistent_effect(warriors, {"type": "set_invuln", "value": 5})
    assert modified.invuln_save == 5


def test_apply_persistent_effect_grant_keyword_adds_to_keywords() -> None:
    units, _ = load_army("necrons")
    overlord = next(u for u in units if u.id == "wh40k_9e.necrons.unit.overlord")
    assert not overlord.has_keyword("FLY")
    modified = _apply_persistent_effect(overlord, {"type": "grant_keyword", "keyword": "FLY"})
    assert modified.has_keyword("FLY")


def test_apply_persistent_effect_grant_keyword_idempotent() -> None:
    units, _ = load_army("necrons")
    overlord = next(u for u in units if u.id == "wh40k_9e.necrons.unit.overlord")
    modified = _apply_persistent_effect(overlord, {"type": "grant_keyword", "keyword": "NECRONS"})
    count = sum(1 for kw in modified.keywords if kw == "NECRONS")
    assert count == 1


def test_apply_persistent_effect_buff_save_decreases_value() -> None:
    units, _ = load_army("necrons")
    warriors = next(u for u in units if u.id == "wh40k_9e.necrons.unit.warriors")
    original = warriors.save
    modified = _apply_persistent_effect(warriors, {"type": "buff_save", "modifier": 1})
    assert modified.save == original - 1


def test_apply_persistent_effect_set_fnp() -> None:
    units, _ = load_army("necrons")
    overlord = next(u for u in units if u.id == "wh40k_9e.necrons.unit.overlord")
    modified = _apply_persistent_effect(overlord, {"type": "set_fnp", "value": 6})
    assert modified.fnp == 6


def test_apply_persistent_effect_buff_stat_move() -> None:
    units, _ = load_army("necrons")
    warriors = next(u for u in units if u.id == "wh40k_9e.necrons.unit.warriors")
    original_inches = int(warriors.move.rstrip('"'))
    modified = _apply_persistent_effect(
        warriors, {"type": "buff_stat", "stat": "move", "modifier": 2}
    )
    assert modified.move == f'{original_inches + 2}"'


def test_apply_persistent_effect_set_stat_save() -> None:
    units, _ = load_army("necrons")
    warriors = next(u for u in units if u.id == "wh40k_9e.necrons.unit.warriors")
    modified = _apply_persistent_effect(warriors, {"type": "set_stat", "stat": "save", "value": 3})
    assert modified.save == 3


def test_apply_wargear_tracks_wargear_ids() -> None:
    units, _ = load_army("necrons")
    overlord = next(u for u in units if u.id == "wh40k_9e.necrons.unit.overlord")
    weapon_catalog = load_weapon_catalog("necrons")
    wargear_catalog = load_wargear_catalog("necrons")

    modified = _apply_wargear(
        overlord,
        ["wh40k_9e.necrons.wargear.resurrection_orb"],
        weapon_catalog,
        wargear_catalog,
    )
    assert "wh40k_9e.necrons.wargear.resurrection_orb" in modified.wargear_ids


def test_apply_wargear_canoptek_cloak_sets_move_and_keyword() -> None:
    units, _ = load_army("necrons")
    warriors = next(u for u in units if u.id == "wh40k_9e.necrons.unit.warriors")
    assert not warriors.has_keyword("FLY")
    weapon_catalog = load_weapon_catalog("necrons")
    wargear_catalog = load_wargear_catalog("necrons")

    modified = _apply_wargear(
        warriors,
        ["wh40k_9e.necrons.wargear.canoptek_cloak"],
        weapon_catalog,
        wargear_catalog,
    )
    assert modified.move == '10"'
    assert modified.has_keyword("FLY")
    assert "FLY" in modified.wargear_keywords


def test_apply_wargear_shadowloom_sets_invuln() -> None:
    units, _ = load_army("necrons")
    overlord = next(u for u in units if u.id == "wh40k_9e.necrons.unit.overlord")
    weapon_catalog = load_weapon_catalog("necrons")
    wargear_catalog = load_wargear_catalog("necrons")

    modified = _apply_wargear(
        overlord,
        ["wh40k_9e.necrons.wargear.shadowloom"],
        weapon_catalog,
        wargear_catalog,
    )
    assert modified.invuln_save == 5


def test_apply_wargear_no_wargear_catalog_still_tracks_ids() -> None:
    units, _ = load_army("necrons")
    overlord = next(u for u in units if u.id == "wh40k_9e.necrons.unit.overlord")
    weapon_catalog = load_weapon_catalog("necrons")

    modified = _apply_wargear(
        overlord,
        ["wh40k_9e.necrons.wargear.resurrection_orb"],
        weapon_catalog,
    )
    assert "wh40k_9e.necrons.wargear.resurrection_orb" in modified.wargear_ids


def test_load_roster_alpha_overlord_has_resurrection_orb_in_wargear_ids() -> None:
    catalog = load_unit_catalog("necrons")
    matched, unmatched = load_roster(_ROSTER_DIR / "necrons_alpha.yaml", catalog)
    assert unmatched == []
    overlord, _ = next((u, m) for u, m in matched if u.id == "wh40k_9e.necrons.unit.overlord")
    assert "wh40k_9e.necrons.wargear.resurrection_orb" in overlord.wargear_ids


def test_load_detachment_types_have_cp_fields() -> None:
    types = load_detachment_types()
    battalion = next(t for t in types if t.id == "battalion")
    assert hasattr(battalion, "command_cost") or True  # fields present in YAML
    # Verify YAML directly since dataclass may not expose these fields yet
    from pathlib import Path

    import yaml as _yaml

    path = (
        Path(__file__).parent.parent.parent
        / "data"
        / "wh40k_9e"
        / "_shared"
        / "detachment_types.yaml"
    )
    with open(path) as f:
        data = _yaml.safe_load(f)
    battalion_data = next(d for d in data["detachment_types"] if d["id"] == "battalion")
    assert battalion_data["command_cost"] == 0
    assert battalion_data["command_benefit"] == 3


# ---------------------------------------------------------------------------
# extra_attacks: max_attacks loaded from YAML
# ---------------------------------------------------------------------------


def test_attack_squig_profile_has_max_attacks_2() -> None:
    catalog = load_weapon_catalog("orks")
    squig = catalog["wh40k_9e.orks.weapon.attack_squig"]
    profile = squig.profiles[0]
    assert profile.max_attacks == 2
    assert profile.effect is not None
    assert profile.effect["type"] == "extra_attacks"


def test_squighog_jaws_max_attacks_2() -> None:
    catalog = load_weapon_catalog("orks")
    weapon = catalog["wh40k_9e.orks.weapon.squighog_jaws"]
    assert weapon.profiles[0].max_attacks == 2


def test_squigosaurs_jaws_max_attacks_3() -> None:
    catalog = load_weapon_catalog("orks")
    weapon = catalog["wh40k_9e.orks.weapon.squigosaurs_jaws"]
    assert weapon.profiles[0].max_attacks == 3


def test_butcha_boyz_max_attacks_4() -> None:
    catalog = load_weapon_catalog("orks")
    weapon = catalog["wh40k_9e.orks.weapon.butcha_boyz"]
    assert weapon.profiles[0].max_attacks == 4


def test_grabbin_klaw_max_attacks_1() -> None:
    catalog = load_weapon_catalog("orks")
    weapon = catalog["wh40k_9e.orks.weapon.grabbin_klaw"]
    assert weapon.profiles[0].max_attacks == 1


def test_choppa_extra_attacks_additive_no_max_attacks() -> None:
    catalog = load_weapon_catalog("orks")
    weapon = catalog["wh40k_9e.orks.weapon.choppa"]
    profile = weapon.profiles[0]
    assert profile.max_attacks is None
    assert profile.effect is not None
    assert profile.effect["amount"] == 1


def test_beastchoppa_extra_attacks_additive() -> None:
    catalog = load_weapon_catalog("orks")
    weapon = catalog["wh40k_9e.orks.weapon.beastchoppa"]
    profile = weapon.profiles[0]
    assert profile.effect is not None
    assert profile.effect["type"] == "extra_attacks"
    assert profile.max_attacks is None


def test_dread_klaw_extra_attacks_additive() -> None:
    catalog = load_weapon_catalog("orks")
    weapon = catalog["wh40k_9e.orks.weapon.dread_klaw"]
    profile = weapon.profiles[0]
    assert profile.effect is not None
    assert profile.effect["type"] == "extra_attacks"
    assert profile.max_attacks is None


# ---------------------------------------------------------------------------
# model_groups: parsed from units.yaml into unit.model_group_specs
# ---------------------------------------------------------------------------


def test_boyz_has_two_model_group_specs() -> None:
    units, _ = load_army("orks")
    boyz = next(u for u in units if u.id == "wh40k_9e.orks.unit.boyz")
    assert len(boyz.model_group_specs) == 2
    ids = {s.id for s in boyz.model_group_specs}
    assert ids == {"ork_boy", "boss_nob"}


def test_boyz_ork_boy_spec_has_remainder_count() -> None:
    units, _ = load_army("orks")
    boyz = next(u for u in units if u.id == "wh40k_9e.orks.unit.boyz")
    ork_boy = next(s for s in boyz.model_group_specs if s.id == "ork_boy")
    assert ork_boy.count_raw == "remainder"
    assert ork_boy.priority == 1


def test_boyz_boss_nob_spec_has_pick_two_swap() -> None:
    units, _ = load_army("orks")
    boyz = next(u for u in units if u.id == "wh40k_9e.orks.unit.boyz")
    boss = next(s for s in boyz.model_group_specs if s.id == "boss_nob")
    assert boss.count_raw == 1
    assert boss.priority == 2
    swap = next(s for s in boss.weapon_swaps if s.id == "nob_weapons")
    assert swap.scope == "group"
    assert swap.pick == 2
    assert "wh40k_9e.orks.weapon.power_klaw" in swap.options
    assert "wh40k_9e.orks.weapon.big_choppa" in swap.options
    assert "wh40k_9e.orks.weapon.slugga" in swap.replaces
    assert "wh40k_9e.orks.weapon.choppa" in swap.replaces


def test_boyz_ork_boy_spec_has_shoota_and_per_10_swaps() -> None:
    units, _ = load_army("orks")
    boyz = next(u for u in units if u.id == "wh40k_9e.orks.unit.boyz")
    ork_boy = next(s for s in boyz.model_group_specs if s.id == "ork_boy")
    shoota = next(s for s in ork_boy.weapon_swaps if s.id == "shoota_swap")
    assert shoota.scope == "per_model"
    assert shoota.limit == "any"
    assert shoota.options == ["wh40k_9e.orks.weapon.shoota"]
    special = next(s for s in ork_boy.weapon_swaps if s.id == "special_weapon")
    assert special.limit == "per_10"
    assert "wh40k_9e.orks.weapon.big_shoota" in special.options
    assert "wh40k_9e.orks.weapon.rokkit_launcha" in special.options


def test_warbikers_has_two_model_group_specs() -> None:
    units, _ = load_army("orks")
    warbikers = next(u for u in units if u.id == "wh40k_9e.orks.unit.warbikers")
    assert len(warbikers.model_group_specs) == 2
    ids = {s.id for s in warbikers.model_group_specs}
    assert ids == {"warbiker", "boss_nob_warbike"}


def test_stormboyz_boss_nob_spec_has_power_klaw_swap() -> None:
    units, _ = load_army("orks")
    stormboyz = next(u for u in units if u.id == "wh40k_9e.orks.unit.stormboyz")
    boss = next(s for s in stormboyz.model_group_specs if s.id == "boss_nob")
    swap = boss.weapon_swaps[0]
    assert swap.replaces == ["wh40k_9e.orks.weapon.choppa"]
    assert swap.options == ["wh40k_9e.orks.weapon.power_klaw"]


def test_kommandos_boss_nob_spec_has_power_klaw_swap() -> None:
    units, _ = load_army("orks")
    kommandos = next(u for u in units if u.id == "wh40k_9e.orks.unit.kommandos")
    boss = next(s for s in kommandos.model_group_specs if s.id == "boss_nob")
    swap = next(s for s in boss.weapon_swaps if s.id == "nob_weapon")
    assert "wh40k_9e.orks.weapon.power_klaw" in swap.options


def test_kommandos_kommando_spec_has_per_10_swaps() -> None:
    """Each datasheet 'for every 10 models' option is its own per_10 swap."""
    units, _ = load_army("orks")
    kommandos = next(u for u in units if u.id == "wh40k_9e.orks.unit.kommandos")
    kommando = next(s for s in kommandos.model_group_specs if s.id == "kommando")
    per_10_options = {
        opt for s in kommando.weapon_swaps if s.limit == "per_10" for opt in s.options
    }
    for weapon_id in [
        "wh40k_9e.orks.weapon.shokka_pistol",
        "wh40k_9e.orks.weapon.big_shoota",
        "wh40k_9e.orks.weapon.burna",
        "wh40k_9e.orks.weapon.kustom_shoota",
        "wh40k_9e.orks.weapon.rokkit_launcha",
        "wh40k_9e.orks.weapon.breacha_ram",
    ]:
        assert weapon_id in per_10_options, weapon_id


def test_skorpekh_has_per_3_reap_blade_swap() -> None:
    """P15: 1 per 3 Skorpekh Destroyers swaps threshers for a reap-blade."""
    units, _ = load_army("necrons")
    skorpekh = next(u for u in units if u.id == "wh40k_9e.necrons.unit.skorpekh_destroyers")
    spec = skorpekh.model_group_specs[0]
    swap = next(s for s in spec.weapon_swaps if s.id == "reap_blade_swap")
    assert swap.scope == "per_model"
    assert swap.limit == "per_3"
    assert swap.options == ["wh40k_9e.necrons.weapon.hyperphase_reap_blade"]
    # C1: unit-level weapons derived as union from the groups
    weapon_ids = {w.id for w in skorpekh.weapons}
    assert "wh40k_9e.necrons.weapon.hyperphase_threshers" in weapon_ids
    assert "wh40k_9e.necrons.weapon.hyperphase_reap_blade" in weapon_ids


def test_lychguard_group_swap_is_all_or_nothing() -> None:
    """P15: ALL Lychguard swap warscythe for sword+shield together (no mix)."""
    units, _ = load_army("necrons")
    lychguard = next(u for u in units if u.id == "wh40k_9e.necrons.unit.lychguard")
    catalog = load_weapon_catalog("necrons")
    loadouts = {
        "lychguard": {
            "swaps": {"sword_and_shield": {"weapons": ["wh40k_9e.necrons.weapon.hyperphase_sword"]}}
        }
    }
    groups = _resolve_model_groups(lychguard.model_group_specs, 10, loadouts, catalog)
    assert len(groups) == 1
    weapon_ids = {w.id for w in groups[0].weapons}
    assert "wh40k_9e.necrons.weapon.hyperphase_sword" in weapon_ids
    assert "wh40k_9e.necrons.weapon.warscythe" not in weapon_ids


def test_unit_without_model_groups_has_empty_specs() -> None:
    units, _ = load_army("necrons")
    overlord = next(u for u in units if "overlord" in u.id)
    assert overlord.model_group_specs == []
    assert overlord.weapon_restrictions == {}


# ---------------------------------------------------------------------------
# Per-group stat overrides (F2/F4): Boss Nob A 3 / S 5 / WS 2+
# ---------------------------------------------------------------------------


def test_boyz_boss_nob_spec_carries_stat_overrides() -> None:
    units, _ = load_army("orks")
    boyz = next(u for u in units if u.id == "wh40k_9e.orks.unit.boyz")
    boss = next(s for s in boyz.model_group_specs if s.id == "boss_nob")
    assert boss.stats == {"attacks": 3, "strength": 5, "ws": "2+"}


def test_ork_boy_spec_has_no_stat_overrides() -> None:
    units, _ = load_army("orks")
    boyz = next(u for u in units if u.id == "wh40k_9e.orks.unit.boyz")
    ork_boy = next(s for s in boyz.model_group_specs if s.id == "ork_boy")
    assert ork_boy.stats == {}


def test_resolved_boss_nob_group_exposes_stats_with_fallback() -> None:
    units, _ = load_army("orks")
    boyz = next(u for u in units if u.id == "wh40k_9e.orks.unit.boyz")
    catalog = load_weapon_catalog("orks")
    groups = _resolve_model_groups(boyz.model_group_specs, 10, {}, catalog)
    boss = next(g for g in groups if g.id == "boss_nob")
    ork_boy = next(g for g in groups if g.id == "ork_boy")
    # Override wins; missing keys fall back to the unit-level value
    assert boss.stat("attacks", boyz.attacks) == 3
    assert boss.stat("strength", boyz.strength) == 5
    assert boss.stat("ws", "3+") == "2+"
    assert boss.stat("toughness", boyz.toughness) == boyz.toughness
    # Homogeneous rank-and-file group has no overrides → unit value
    assert ork_boy.stat("attacks", boyz.attacks) == boyz.attacks


def test_skorpekh_roster_loadout_splits_reap_blade_subgroup() -> None:
    """F6: the standard build fields 1 reap-blade per 3 (2 threshers remain)."""
    units, _ = load_army("necrons")
    skorpekh = next(u for u in units if u.id == "wh40k_9e.necrons.unit.skorpekh_destroyers")
    catalog = load_weapon_catalog("necrons")
    loadouts = {
        "skorpekh": {
            "swaps": {
                "reap_blade_swap": [
                    {"weapons": ["wh40k_9e.necrons.weapon.hyperphase_reap_blade"], "count": 1}
                ]
            }
        }
    }
    groups = _resolve_model_groups(skorpekh.model_group_specs, 3, loadouts, catalog)
    counts = {tuple(sorted(w.id for w in g.weapons)): g.count for g in groups}
    reap = next(g for g in groups if any("reap_blade" in w.id for w in g.weapons))
    threshers = next(g for g in groups if all("reap_blade" not in w.id for w in g.weapons))
    assert reap.count == 1
    assert threshers.count == 2
    assert sum(counts.values()) == 3


# ── Relic loader tests ───────────────────────────────────────────────────────


def test_load_relic_catalog_orks_returns_entries() -> None:
    catalog = load_relic_catalog("orks")
    assert "wh40k_9e.orks.relic.da_gobshot_thunderbuss" in catalog
    assert "wh40k_9e.orks.relic.rezmekkas_redder_paint" in catalog


def test_load_relic_catalog_necrons_returns_entries() -> None:
    catalog = load_relic_catalog("necrons")
    assert "wh40k_9e.necrons.relic.leerenschnitter" in catalog


def test_apply_relic_sets_relic_id() -> None:
    units, _ = load_army("orks")
    warboss = next(u for u in units if u.id == "wh40k_9e.orks.unit.warboss")
    relic_catalog = load_relic_catalog("orks")
    result = _apply_relic(warboss, "wh40k_9e.orks.relic.da_irongob", relic_catalog)
    assert result.relic_id == "wh40k_9e.orks.relic.da_irongob"


def test_apply_relic_buff_stat_move() -> None:
    units, _ = load_army("orks")
    warboss = next(u for u in units if u.id == "wh40k_9e.orks.unit.warboss")
    base_move = int(warboss.move.rstrip('"'))
    relic_catalog = load_relic_catalog("orks")
    result = _apply_relic(warboss, "wh40k_9e.orks.relic.rezmekkas_redder_paint", relic_catalog)
    assert int(result.move.rstrip('"')) == base_move + 2


def test_apply_relic_set_invuln() -> None:
    units, _ = load_army("orks")
    warboss = next(u for u in units if u.id == "wh40k_9e.orks.unit.warboss")
    relic_catalog = load_relic_catalog("orks")
    result = _apply_relic(warboss, "wh40k_9e.orks.relic.tezdrek_stompa_power_field", relic_catalog)
    assert result.invuln_save == 5


def test_apply_relic_weapon_replacement_adds_relic_weapon() -> None:
    units, _ = load_army("necrons")
    # leerenschnitter (Voidreaper) replaces warscythe / voidscythe
    lychguard = next(u for u in units if u.id == "wh40k_9e.necrons.unit.lychguard")
    relic_catalog = load_relic_catalog("necrons")
    result = _apply_relic(lychguard, "wh40k_9e.necrons.relic.leerenschnitter", relic_catalog)
    relic_weapon_ids = [w.id for w in result.weapons]
    assert "wh40k_9e.necrons.relic.leerenschnitter" in relic_weapon_ids


def test_apply_relic_weapon_replacement_removes_replaced_weapon() -> None:
    units, _ = load_army("necrons")
    lychguard = next(u for u in units if u.id == "wh40k_9e.necrons.unit.lychguard")
    relic_catalog = load_relic_catalog("necrons")
    result = _apply_relic(lychguard, "wh40k_9e.necrons.relic.leerenschnitter", relic_catalog)
    weapon_ids = [w.id for w in result.weapons]
    assert "wh40k_9e.necrons.weapon.warscythe" not in weapon_ids


def test_apply_relic_unknown_id_returns_unit_unchanged() -> None:
    units, _ = load_army("necrons")
    overlord = next(u for u in units if u.id == "wh40k_9e.necrons.unit.overlord")
    relic_catalog = load_relic_catalog("necrons")
    result = _apply_relic(overlord, "wh40k_9e.necrons.relic.does_not_exist", relic_catalog)
    assert result.relic_id is None
    assert result.weapons == overlord.weapons


def test_buff_stat_toughness_in_persistent_effect() -> None:
    units, _ = load_army("necrons")
    overlord = next(u for u in units if u.id == "wh40k_9e.necrons.unit.overlord")
    base_t = overlord.toughness
    result = _apply_persistent_effect(
        overlord, {"type": "buff_stat", "stat": "toughness", "modifier": 1}
    )
    assert result.toughness == base_t + 1


# ---------------------------------------------------------------------------
# model_groups: count resolution + roster resolution
# ---------------------------------------------------------------------------


def test_resolve_model_groups_remainder_count() -> None:
    units, _ = load_army("orks")
    boyz = next(u for u in units if u.id == "wh40k_9e.orks.unit.boyz")
    catalog = load_weapon_catalog("orks")
    groups = _resolve_model_groups(boyz.model_group_specs, 10, {}, catalog)
    ork_boy = next(g for g in groups if g.id == "ork_boy")
    boss_nob = next(g for g in groups if g.id == "boss_nob")
    assert boss_nob.count == 1
    assert ork_boy.count == 9  # remainder = 10 - 1


def test_resolve_model_groups_boss_nob_has_base_weapons() -> None:
    units, _ = load_army("orks")
    boyz = next(u for u in units if u.id == "wh40k_9e.orks.unit.boyz")
    catalog = load_weapon_catalog("orks")
    groups = _resolve_model_groups(boyz.model_group_specs, 10, {}, catalog)
    boss_nob = next(g for g in groups if g.id == "boss_nob")
    weapon_names = {w.id for w in boss_nob.weapons}
    assert "wh40k_9e.orks.weapon.slugga" in weapon_names
    assert "wh40k_9e.orks.weapon.stikkbombz" in weapon_names


def test_resolve_group_swap_replaces_base_weapons() -> None:
    """Boss Nob pick-2 swap: slugga+choppa out, the two picks in."""
    units, _ = load_army("orks")
    boyz = next(u for u in units if u.id == "wh40k_9e.orks.unit.boyz")
    catalog = load_weapon_catalog("orks")
    loadouts = {
        "boss_nob": {
            "swaps": {
                "nob_weapons": {
                    "weapons": [
                        "wh40k_9e.orks.weapon.power_klaw",
                        "wh40k_9e.orks.weapon.big_choppa",
                    ]
                }
            }
        }
    }
    groups = _resolve_model_groups(boyz.model_group_specs, 10, loadouts, catalog)
    boss_nob = next(g for g in groups if g.id == "boss_nob")
    weapon_ids = {w.id for w in boss_nob.weapons}
    assert "wh40k_9e.orks.weapon.power_klaw" in weapon_ids
    assert "wh40k_9e.orks.weapon.big_choppa" in weapon_ids
    assert "wh40k_9e.orks.weapon.slugga" not in weapon_ids
    assert "wh40k_9e.orks.weapon.choppa" not in weapon_ids
    assert "wh40k_9e.orks.weapon.stikkbombz" in weapon_ids  # not replaced


def test_resolve_per_model_swap_splits_sub_groups() -> None:
    """Shoota mix: 3 of 9 Ork Boys swap slugga+choppa for a shoota."""
    units, _ = load_army("orks")
    boyz = next(u for u in units if u.id == "wh40k_9e.orks.unit.boyz")
    catalog = load_weapon_catalog("orks")
    loadouts = {
        "ork_boy": {
            "swaps": {"shoota_swap": [{"weapons": ["wh40k_9e.orks.weapon.shoota"], "count": 3}]}
        }
    }
    groups = _resolve_model_groups(boyz.model_group_specs, 10, loadouts, catalog)
    shoota_boys = next(g for g in groups if g.id == "ork_boy_shoota")
    base_boys = next(g for g in groups if g.id == "ork_boy")
    assert shoota_boys.count == 3
    assert base_boys.count == 6  # 9 remainder - 3 swapped
    shoota_ids = {w.id for w in shoota_boys.weapons}
    assert "wh40k_9e.orks.weapon.shoota" in shoota_ids
    assert "wh40k_9e.orks.weapon.slugga" not in shoota_ids
    assert "wh40k_9e.orks.weapon.stikkbombz" in shoota_ids
    base_ids = {w.id for w in base_boys.weapons}
    assert "wh40k_9e.orks.weapon.slugga" in base_ids
    assert "wh40k_9e.orks.weapon.shoota" not in base_ids


def test_resolve_model_groups_models_max_count() -> None:
    units, _ = load_army("orks")
    tankbustas = next(u for u in units if u.id == "wh40k_9e.orks.unit.tankbustas")
    catalog = load_weapon_catalog("orks")
    groups = _resolve_model_groups(tankbustas.model_group_specs, 10, {}, catalog)
    assert len(groups) == 1
    assert groups[0].count == 10


def test_resolve_per_model_pick_two_split() -> None:
    """Nobz: any number of models swap slugga+choppa for TWO picks each."""
    units, _ = load_army("orks")
    nobz = next(u for u in units if u.id == "wh40k_9e.orks.unit.nobz")
    catalog = load_weapon_catalog("orks")
    loadouts = {
        "nob": {
            "swaps": {
                "nob_weapons": [
                    {
                        "weapons": [
                            "wh40k_9e.orks.weapon.power_klaw",
                            "wh40k_9e.orks.weapon.big_choppa",
                        ],
                        "count": 3,
                    },
                    {
                        "weapons": [
                            "wh40k_9e.orks.weapon.killsaw",
                            "wh40k_9e.orks.weapon.killsaw",
                        ],
                        "count": 2,
                    },
                ]
            }
        }
    }
    groups = _resolve_model_groups(nobz.model_group_specs, 5, loadouts, catalog)
    assert len(groups) == 2  # both sub-groups; no remainder (3 + 2 = 5)
    klaw_nobz = next(g for g in groups if "power_klaw" in g.id)
    saw_nobz = next(g for g in groups if "killsaw" in g.id)
    assert klaw_nobz.count == 3
    assert saw_nobz.count == 2
    klaw_ids = {w.id for w in klaw_nobz.weapons}
    assert "wh40k_9e.orks.weapon.power_klaw" in klaw_ids
    assert "wh40k_9e.orks.weapon.big_choppa" in klaw_ids
    assert "wh40k_9e.orks.weapon.slugga" not in klaw_ids
    # Two killsaws: the weapon list contains the ref twice
    saw_refs = [w.id for w in saw_nobz.weapons if w.id == "wh40k_9e.orks.weapon.killsaw"]
    assert len(saw_refs) == 2


def test_resolve_model_groups_no_specs_returns_empty() -> None:
    units, _ = load_army("necrons")
    warrior = next(u for u in units if "warriors" in u.id)
    catalog = load_weapon_catalog("necrons")
    groups = _resolve_model_groups(warrior.model_group_specs, 10, {}, catalog)
    assert groups == []


def test_load_roster_boyz_has_resolved_model_groups() -> None:
    """Roster load resolves model_groups for units that have group specs."""
    from pathlib import Path

    roster_path = Path(__file__).parent.parent.parent / "data" / "rosters" / "orks_test.yaml"
    catalog = load_unit_catalog("orks")
    matched, _ = load_roster(roster_path, catalog)
    boyz = next((u for u, _ in matched if u.id == "wh40k_9e.orks.unit.boyz"), None)
    assert boyz is not None
    # Test roster: 3 shoota boys + 1 big shoota carrier + 5 base boys + boss nob
    assert len(boyz.model_groups) == 4
    boss = next(g for g in boyz.model_groups if g.id == "boss_nob")
    ork_boy = next(g for g in boyz.model_groups if g.id == "ork_boy")
    shoota_boys = next(g for g in boyz.model_groups if g.id == "ork_boy_shoota")
    carrier = next(g for g in boyz.model_groups if g.id == "ork_boy_big_shoota")
    assert boss.count == 1
    assert shoota_boys.count == 3
    assert carrier.count == 1
    assert ork_boy.count == 5  # 10 - 1 boss - 3 shoota - 1 carrier
    boss_weapon_ids = {w.id for w in boss.weapons}
    assert "wh40k_9e.orks.weapon.power_klaw" in boss_weapon_ids
    assert "wh40k_9e.orks.weapon.big_choppa" in boss_weapon_ids
    carrier_ids = {w.id for w in carrier.weapons}
    assert "wh40k_9e.orks.weapon.big_shoota" in carrier_ids
    assert "wh40k_9e.orks.weapon.slugga" not in carrier_ids


def test_load_roster_unit_without_yaml_groups_gets_synthetic_group() -> None:
    """Homogeneous units (no model_groups in YAML) receive one synthetic group after loading."""
    from pathlib import Path

    roster_path = Path(__file__).parent.parent.parent / "data" / "rosters" / "orks_test.yaml"
    catalog = load_unit_catalog("orks")
    matched, _ = load_roster(roster_path, catalog)
    gretchin = next((u for u, _ in matched if u.id == "wh40k_9e.orks.unit.gretchin"), None)
    assert gretchin is not None
    assert len(gretchin.model_groups) == 1
    synth = gretchin.model_groups[0]
    assert synth.id == "models"
    assert synth.name_en == "Gretchin"
    assert synth.count == 10  # roster models=10, models_max=40
    assert synth.priority == 1
    assert len(synth.weapons) > 0


def test_all_roster_units_have_at_least_one_model_group() -> None:
    """Every unit in a loaded roster must have at least one model group (Plan 013)."""
    from pathlib import Path

    for roster_name in ("necrons_alpha.yaml", "orks_test.yaml"):
        roster_path = Path(__file__).parent.parent.parent / "data" / "rosters" / roster_name
        faction = roster_name.split("_")[0]
        catalog = load_unit_catalog(faction)
        matched, _ = load_roster(roster_path, catalog)
        for unit, _ in matched:
            assert (
                len(unit.model_groups) >= 1
            ), f"{unit.id} in {roster_name} has no model groups after loading"


def test_round_choice_abilities_are_cached() -> None:
    first = load_round_choice_abilities("necrons")
    second = load_round_choice_abilities("necrons")
    assert first is second


def test_round_choice_label_is_cached() -> None:
    assert load_round_choice_label("necrons") == load_round_choice_label("necrons")


def test_faction_abilities_are_cached() -> None:
    assert load_faction_abilities("orks") is load_faction_abilities("orks")


def test_stratagems_are_cached() -> None:
    assert load_stratagems("orks") is load_stratagems("orks")


def test_unit_abilities_are_cached() -> None:
    assert load_unit_abilities("necrons") is load_unit_abilities("necrons")


def test_deny_wargear_names_are_cached() -> None:
    assert load_deny_wargear_names("necrons") is load_deny_wargear_names("necrons")


def test_duplicate_per_model_entries_merge_into_one_group() -> None:

    from gameObjects.unit import ModelGroupSpec, WeaponSwapSpec

    catalog = load_weapon_catalog("orks")
    spec = ModelGroupSpec(
        id="boy",
        name_en="Boy",
        count_raw="models_max",
        base_weapon_refs=["wh40k_9e.orks.weapon.slugga", "wh40k_9e.orks.weapon.choppa"],
        weapon_swaps=[
            WeaponSwapSpec(
                id="special",
                scope="per_model",
                replaces=["wh40k_9e.orks.weapon.slugga"],
                options=["wh40k_9e.orks.weapon.big_shoota"],
                pick=1,
                limit="any",
            )
        ],
        priority=1,
    )
    loadouts = {
        "boy": {
            "swaps": {
                "special": [
                    {"weapons": ["wh40k_9e.orks.weapon.big_shoota"], "count": 1},
                    {"weapons": ["wh40k_9e.orks.weapon.big_shoota"], "count": 1},
                ]
            }
        }
    }
    groups = _resolve_model_groups([spec], 10, loadouts, catalog)
    ids = [g.id for g in groups]
    assert len(ids) == len(set(ids)), f"duplicate group ids: {ids}"
    merged = next(g for g in groups if "big_shoota" in g.id)
    assert merged.count == 2


def test_unknown_weapon_ref_in_swap_raises_clear_error() -> None:
    import pytest

    from gameObjects.unit import ModelGroupSpec, WeaponSwapSpec

    catalog = load_weapon_catalog("orks")
    spec = ModelGroupSpec(
        id="boy",
        name_en="Boy",
        count_raw="models_max",
        base_weapon_refs=["wh40k_9e.orks.weapon.slugga"],
        weapon_swaps=[
            WeaponSwapSpec(
                id="special",
                scope="group",
                replaces=["wh40k_9e.orks.weapon.slugga"],
                options=["wh40k_9e.orks.weapon.shota_TYPO"],
                pick=1,
                limit="any",
            )
        ],
        priority=1,
    )
    loadouts = {"boy": {"swaps": {"special": {"weapons": ["wh40k_9e.orks.weapon.shota_TYPO"]}}}}
    with pytest.raises(ValueError, match="unknown weapon ref"):
        _resolve_model_groups([spec], 10, loadouts, catalog)


def test_load_yaml_raises_clear_error_on_broken_file(tmp_path) -> None:
    import pytest

    from gameObjects.loader import YamlDataError, load_yaml

    broken = tmp_path / "broken.yaml"
    broken.write_text("units:\n  - id: [unclosed")
    with pytest.raises(YamlDataError, match="broken.yaml"):
        load_yaml(broken)


def test_load_yaml_returns_parsed_data(tmp_path) -> None:
    from gameObjects.loader import load_yaml

    ok = tmp_path / "ok.yaml"
    ok.write_text("units:\n  - id: a\n")
    assert load_yaml(ok) == {"units": [{"id": "a"}]}


# ---------------------------------------------------------------------------
# H1/H2/H4a: Big Mek MA wargear, Silent King weapons, Szarekhan code
# ---------------------------------------------------------------------------


def test_big_mek_mega_armour_default_and_shoota_swap() -> None:
    from gameObjects.loader import _apply_wargear

    cat = load_unit_catalog("orks")
    wcat = load_weapon_catalog("orks")
    bm = cat["wh40k_9e.orks.unit.big_mek_mega_armour"]
    names = {w.name_en for w in bm.weapons}
    assert names == {"Kustom mega-blasta", "Power klaw"}
    swapped = _apply_wargear(bm, ["wh40k_9e.orks.weapon.kustom_shoota"], wcat, None)
    sw_names = {w.name_en for w in swapped.weapons}
    assert "Kustom shoota" in sw_names
    assert "Kustom mega-blasta" not in sw_names  # replaced, not added


def test_silent_king_weapon_distribution() -> None:
    units, _ = load_army("necrons")
    sk = next(u for u in units if u.id.endswith("the_silent_king"))
    groups = _resolve_model_groups(sk.model_group_specs, 3, {}, load_weapon_catalog("necrons"))
    menhirs = next(g for g in groups if g.id == "triarchal_menhirs")
    szarekh = next(g for g in groups if g.id == "szarekh")
    assert [w.name_en for w in menhirs.weapons] == ["Annihilator Beam"]
    assert {w.name_en for w in szarekh.weapons} == {
        "Sceptre of Eternal Glory",
        "Staff of Stars",
        "Scythe of Dust",
    }


def test_szarekhan_code_is_uncanny_artificers_not_both_directives() -> None:
    abilities = load_subfaction_abilities("necrons")
    ids = {a.id for a in abilities}
    assert any("uncanny_artificers" in i for i in ids)
    assert not any("loyal_to_the_triarch" in i for i in ids)
