"""Tests for gameMechanic/abilityEngine.py."""

import sys
from pathlib import Path
from unittest.mock import MagicMock

import pytest

_st_mock = MagicMock()
sys.modules["streamlit"] = _st_mock
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

import gameMechanic.abilityEngine as _eng  # noqa: E402
from gameMechanic.abilityEngine import (  # noqa: E402
    _sum_effect_value,
    _unit_matches_target,
    ability_badge_label,
    ability_invuln_save,
    buff_stat_bonus,
    charge_after_advance_allowed,
    check_conditions,
    check_trigger,
    execute_effect,
    find_unit_ability_by_effect,
    get_activated_command_abilities,
    get_active_heal_bonus,
    get_active_protocol_effects,
    get_active_round_choice_ap_on_wound_6,
    get_active_round_choice_ignores_cover_half_range,
    get_active_round_choice_light_cover_if_stationary,
    get_active_round_choice_modifier,
    get_active_round_choice_shoot_after_fall_back,
    get_active_round_choice_strength_if_charged,
    get_active_rp_modifiers,
    get_after_attack_revive_ability,
    get_short_label_for_effect_type,
    get_triggered_abilities,
    get_unit_rp_reroll_ability,
    is_effect_executable,
    mortal_wounds_target,
    resolve_explode_effect,
    resolve_mortal_wounds_effect,
    revive_dice_count,
    unit_hit_reroll_ones,
    unit_wound_auto_fail_label,
    unit_wound_auto_fail_max,
    unit_wound_reroll_ones,
)
from gameObjects.ability import Ability, Condition, Effect, Trigger  # noqa: E402
from gameObjects.loader import load_army  # noqa: E402
from gameObjects.unit import Unit  # noqa: E402


def _make_unit(rules: list[str], keywords: list[str] | None = None) -> Unit:
    return Unit(
        id="test.unit",
        name_en="Test Unit",
        name_de="Test-Einheit",
        faction="Necrons",
        subfaction=None,
        battlefield_role=["Troops"],
        keywords=keywords or [],
        wounds=3,
        models_min=1,
        models_max=3,
        power_level=4,
        move='6"',
        bs="3+",
        ws="3+",
        strength=4,
        toughness=4,
        attacks=3,
        save=3,
        invuln_save=None,
        leadership=10,
        oc=2,
        fnp=None,
        rules=rules,
    )


def _living_metal_ability() -> Ability:
    return Ability(
        id="necrons.faction.living_metal",
        name_en="Living Metal",
        source="faction_rule",
        rule_text="Regains 1 wound.",
        trigger=Trigger(timing="phase_start", phase="command", player="active"),
        conditions=[
            Condition(has_rules=["livingMetal"], unit_not_destroyed=True, needs_healing=True)
        ],
        effect=Effect(type="heal", target="self", amount="1", revive=False),
    )


# ---------------------------------------------------------------------------
# check_trigger
# ---------------------------------------------------------------------------


def test_check_trigger_matches_correct_phase_and_timing() -> None:
    ability = _living_metal_ability()
    assert check_trigger(ability, "command", "phase_start", "active") is True


def test_check_trigger_wrong_timing_returns_false() -> None:
    ability = _living_metal_ability()
    assert check_trigger(ability, "command", "phase_end", "active") is False


def test_check_trigger_wrong_phase_returns_false() -> None:
    ability = _living_metal_ability()
    assert check_trigger(ability, "movement", "phase_start", "active") is False


def test_check_trigger_wrong_player_returns_false() -> None:
    ability = _living_metal_ability()
    assert check_trigger(ability, "command", "phase_start", "inactive") is False


def test_check_trigger_either_player_matches_both() -> None:
    ability = Ability(
        id="test",
        name_en="T",
        source="faction_rule",
        rule_text="",
        trigger=Trigger(timing="persistent", phase="any", player="either"),
        conditions=[],
        effect=Effect(type="heal", target="self"),
    )
    assert check_trigger(ability, "any", "persistent", "active") is True
    assert check_trigger(ability, "any", "persistent", "inactive") is True


def test_check_trigger_list_phase_matches_any_phase_in_list() -> None:
    ability = Ability(
        id="test",
        name_en="T",
        source="faction_rule",
        rule_text="",
        trigger=Trigger(timing="phase_reactive", phase=["shooting", "fight"], player="inactive"),
        conditions=[],
        effect=Effect(type="reanimate", target="self"),
    )
    assert check_trigger(ability, "shooting", "phase_reactive", "inactive") is True
    assert check_trigger(ability, "fight", "phase_reactive", "inactive") is True
    assert check_trigger(ability, "command", "phase_reactive", "inactive") is False


# ---------------------------------------------------------------------------
# check_conditions
# ---------------------------------------------------------------------------


def test_check_conditions_has_rules_match() -> None:
    ability = _living_metal_ability()
    unit = _make_unit(rules=["livingMetal"])
    assert (
        check_conditions(ability, unit, {"destroyed": False, "models": 2, "current_wounds": 5})
        is True
    )


def test_check_conditions_has_rules_no_match() -> None:
    ability = _living_metal_ability()
    unit = _make_unit(rules=["reanimationProtocols"])
    assert (
        check_conditions(ability, unit, {"destroyed": False, "models": 3, "current_wounds": 8})
        is False
    )


def test_check_conditions_unit_destroyed_fails_when_required() -> None:
    ability = Ability(
        id="test",
        name_en="T",
        source="faction_rule",
        rule_text="",
        trigger=Trigger(timing="phase_reactive", phase="fight", player="inactive"),
        conditions=[Condition(has_rules=["reanimationProtocols"], unit_not_destroyed=True)],
        effect=Effect(type="reanimate", target="self"),
    )
    unit = _make_unit(rules=["reanimationProtocols"])
    assert check_conditions(ability, unit, {"destroyed": True}) is False
    assert check_conditions(ability, unit, {"destroyed": False}) is True


def test_check_conditions_has_keywords_match() -> None:
    ability = Ability(
        id="test",
        name_en="T",
        source="unit_ability",
        rule_text="",
        trigger=Trigger(timing="phase_any", phase="command", player="active"),
        conditions=[Condition(has_keywords=["Core"])],
        effect=Effect(type="buff_roll", target="selected_unit"),
    )
    unit_with_core = _make_unit(rules=[], keywords=["Necrons", "Core", "Infantry"])
    unit_without_core = _make_unit(rules=[], keywords=["Necrons", "Infantry"])
    assert check_conditions(ability, unit_with_core, {}) is True
    assert check_conditions(ability, unit_without_core, {}) is False


def test_check_conditions_needs_healing_false_when_full_health() -> None:
    ability = _living_metal_ability()
    unit = _make_unit(rules=["livingMetal"])
    # 3 models × 3 wounds = 9 max HP, full health → not eligible
    assert (
        check_conditions(ability, unit, {"destroyed": False, "models": 3, "current_wounds": 9})
        is False
    )


def test_check_conditions_needs_healing_true_when_wounded() -> None:
    ability = _living_metal_ability()
    unit = _make_unit(rules=["livingMetal"])
    # 3 models × 3 wounds = 9 max HP, 8 wounds → eligible
    assert (
        check_conditions(ability, unit, {"destroyed": False, "models": 3, "current_wounds": 8})
        is True
    )


def test_check_conditions_needs_healing_uses_current_models_not_max() -> None:
    """A unit with 1 dead model at full living-model HP is not eligible (no wound to heal)."""
    ability = _living_metal_ability()
    unit = _make_unit(rules=["livingMetal"])
    # 1 model dead, 2 remaining at full HP: models=2, wounds=3 → max_hp=6, current=6
    assert (
        check_conditions(ability, unit, {"destroyed": False, "models": 2, "current_wounds": 6})
        is False
    )


def test_check_conditions_needs_healing_living_models_wounded() -> None:
    """A unit with 1 dead model AND remaining models wounded IS eligible."""
    ability = _living_metal_ability()
    unit = _make_unit(rules=["livingMetal"])
    # 1 model dead, 2 remaining, 1 wound taken: models=2, current=5
    assert (
        check_conditions(ability, unit, {"destroyed": False, "models": 2, "current_wounds": 5})
        is True
    )


# ---------------------------------------------------------------------------
# execute_effect
# ---------------------------------------------------------------------------


class _S(dict):
    def __getattr__(self, key: str):  # type: ignore[override]
        try:
            return self[key]
        except KeyError:
            raise AttributeError(key)

    def __setattr__(self, key: str, value: object) -> None:
        self[key] = value


def test_execute_effect_heal_heals_unit() -> None:
    session = _S(
        first_player="Necrons",
        p1_units={"test.unit": {"current_wounds": 4, "models": 2, "destroyed": False}},
    )
    _eng.heal_unit.__module__  # ensure imported
    import gameMechanic.unitMutations as _mut  # noqa: PLC0415

    _mut.st.session_state = session
    _st_mock.session_state = session
    unit = _make_unit(rules=["livingMetal"])
    unit = Unit(
        id="test.unit",
        name_en="T",
        name_de="T",
        faction="Necrons",
        subfaction=None,
        battlefield_role=[],
        keywords=[],
        wounds=3,
        models_min=1,
        models_max=3,
        power_level=4,
        move='6"',
        bs="3+",
        ws="3+",
        strength=4,
        toughness=4,
        attacks=3,
        save=3,
        invuln_save=None,
        leadership=10,
        oc=2,
        fnp=None,
        rules=["livingMetal"],
    )
    ability = _living_metal_ability()
    result = execute_effect(ability, "test.unit", "Necrons", unit)
    assert result is True
    assert session["p1_units"]["test.unit"]["current_wounds"] == 5


def test_execute_effect_heal_adds_active_directive_bonus() -> None:
    """Undying Legions D1/primary (+1 wound per Living Metal use) lifts the heal amount."""
    import gameMechanic.unitMutations as _mut  # noqa: PLC0415

    session = _S(
        first_player="Necrons",
        p1_faction_dir="necrons",
        p2_faction_dir="necrons",
        p1_units={"test.unit": {"current_wounds": 3, "models": 2, "destroyed": False}},
    )
    session["round_choice_active_Necrons"] = "wh40k_9e.necrons.faction.protocol_undying_legions"
    session["round_choice_directive_Necrons"] = "primary"
    _mut.st.session_state = session
    _st_mock.session_state = session
    unit = _make_unit(rules=["livingMetal"])
    result = execute_effect(
        unit=unit, ability=_living_metal_ability(), uid="test.unit", faction="Necrons"
    )
    assert result is True
    # base 1 + directive 1 = 2 wounds healed: 3 -> 5
    assert session["p1_units"]["test.unit"]["current_wounds"] == 5


def test_execute_effect_heal_no_revive_caps_at_living_models() -> None:
    """revive=False must not push wounds beyond current_models × wounds."""
    import gameMechanic.unitMutations as _mut  # noqa: PLC0415

    # 1 model dead, 2 remaining at full HP: cannot be healed further
    session = _S(
        first_player="Necrons",
        p1_units={"test.unit": {"current_wounds": 6, "models": 2, "destroyed": False}},
    )
    _mut.st.session_state = session
    _st_mock.session_state = session
    unit = Unit(
        id="test.unit",
        name_en="T",
        name_de="T",
        faction="Necrons",
        subfaction=None,
        battlefield_role=[],
        keywords=[],
        wounds=3,
        models_min=1,
        models_max=3,
        power_level=4,
        move='6"',
        bs="3+",
        ws="3+",
        strength=4,
        toughness=4,
        attacks=3,
        save=3,
        invuln_save=None,
        leadership=10,
        oc=2,
        fnp=None,
        rules=["livingMetal"],
    )
    ability = _living_metal_ability()
    result = execute_effect(ability, "test.unit", "Necrons", unit)
    assert result is False
    assert session["p1_units"]["test.unit"]["current_wounds"] == 6


def test_execute_effect_unknown_type_returns_false() -> None:
    ability = Ability(
        id="test",
        name_en="T",
        source="faction_rule",
        rule_text="",
        trigger=Trigger(timing="phase_start", phase="command"),
        conditions=[],
        effect=Effect(type="unknown_effect", target="self"),
    )
    unit = _make_unit(rules=[])
    result = execute_effect(ability, "test.unit", "Necrons", unit)
    assert result is False


# ---------------------------------------------------------------------------
# is_effect_executable — single source of truth for the armyCard Apply-button
# gate (S148 Brief 1: the button must not appear, and no state/log must be
# written, for effect types execute_effect() cannot actually apply).
# ---------------------------------------------------------------------------


def test_is_effect_executable_true_for_heal() -> None:
    assert is_effect_executable("heal") is True


def test_is_effect_executable_false_for_unwired_triggered_effect_types() -> None:
    # Sample of real Necron triggered-ability effect types with no execute_effect
    # dispatch branch (S147 audit, e.g. Royal Warden buff_stat, United in
    # Destruction reroll_wound_1, Translocation Protocols teleport).
    for effect_type in ("buff_stat", "reroll_wound_1", "reroll_hit", "fight_last", "teleport"):
        assert is_effect_executable(effect_type) is False


def test_is_effect_executable_matches_execute_effect_dispatch() -> None:
    # No second hardcoded set: whatever execute_effect() actually applies (a real
    # state change) must be exactly what is_effect_executable() reports as executable.
    import gameMechanic.unitMutations as _mut  # noqa: PLC0415

    session = _S(
        first_player="Necrons",
        p1_units={"test.unit": {"current_wounds": 4, "models": 2, "destroyed": False}},
    )
    _mut.st.session_state = session
    _st_mock.session_state = session
    unit = _make_unit(rules=["livingMetal"])
    heal_ability = _living_metal_ability()
    assert is_effect_executable(heal_ability.effect.type) is True
    assert execute_effect(heal_ability, "test.unit", "Necrons", unit) is True

    unknown_ability = Ability(
        id="test",
        name_en="T",
        source="faction_rule",
        rule_text="",
        trigger=Trigger(timing="phase_start", phase="command"),
        conditions=[],
        effect=Effect(type="buff_stat", target="self"),
    )
    assert is_effect_executable(unknown_ability.effect.type) is False
    assert execute_effect(unknown_ability, "test.unit", "Necrons", unit) is False


# ---------------------------------------------------------------------------
# get_triggered_abilities — integration with real YAML
# ---------------------------------------------------------------------------


def _make_necron_state() -> dict:
    units, _ = load_army("necrons")
    session = _S(first_player="Necrons", p1_faction_dir="necrons", p2_faction_dir="necrons")
    _st_mock.session_state = session
    return {
        "active": "Necrons",
        "first_player": "Necrons",
        "p1_units": {
            u.id: {
                "current_wounds": max(
                    1, u.wounds * u.models_max - 1
                ),  # 1 wound below max → all eligible for LM
                "models": u.models_max,
                "destroyed": False,
            }
            for u in units
        },
    }


def test_get_triggered_abilities_command_phase_start_includes_living_metal() -> None:
    state = _make_necron_state()
    triggered = get_triggered_abilities(state, "command", "phase_start")
    ability_ids = [a.id for a, _ in triggered]
    assert "wh40k_9e.necrons.faction.living_metal" in ability_ids


def test_get_triggered_abilities_living_metal_excludes_warriors() -> None:
    state = _make_necron_state()
    triggered = get_triggered_abilities(state, "command", "phase_start")
    lm_entry = next(
        (a, uids) for a, uids in triggered if a.id == "wh40k_9e.necrons.faction.living_metal"
    )
    _, eligible_ids = lm_entry
    # Warriors have reanimationProtocols but NOT livingMetal
    warriors_id = "wh40k_9e.necrons.unit.warriors"
    assert warriors_id not in eligible_ids


def test_get_triggered_abilities_living_metal_includes_overlord_and_skorpekh() -> None:
    state = _make_necron_state()
    triggered = get_triggered_abilities(state, "command", "phase_start")
    _, lm_units = next(t for t in triggered if t[0].id == "wh40k_9e.necrons.faction.living_metal")
    assert "wh40k_9e.necrons.unit.overlord" in lm_units
    assert "wh40k_9e.necrons.unit.skorpekh_destroyers" in lm_units
    assert "wh40k_9e.necrons.unit.triarch_stalker" in lm_units
    assert "wh40k_9e.necrons.unit.canoptek_scarabs" in lm_units


def test_get_triggered_abilities_living_metal_excludes_full_health_units() -> None:
    """Units at full health are not eligible even if they have the livingMetal rule."""
    units, _ = load_army("necrons")
    session = _S(first_player="Necrons", p1_faction_dir="necrons", p2_faction_dir="necrons")
    _st_mock.session_state = session
    state = {
        "active": "Necrons",
        "first_player": "Necrons",
        "p1_units": {
            u.id: {
                "current_wounds": u.wounds * u.models_max,  # full health
                "models": u.models_max,
                "destroyed": False,
            }
            for u in units
        },
    }
    triggered = get_triggered_abilities(state, "command", "phase_start")
    ability_ids = [a.id for a, _ in triggered]
    assert "wh40k_9e.necrons.faction.living_metal" not in ability_ids


# ---------------------------------------------------------------------------
# get_active_round_choice_modifier — protocol effect lookup
# ---------------------------------------------------------------------------


def _protocol_session(
    protocol_id: str | None, directive: str | None, *, subfaction: str | None = None
) -> _S:
    # Round-choice runtime state is keyed by the player slot ("Necrons"), not the
    # faction directory — see round_choice_state_key (mirror-match safe).
    session = _S(
        first_player="Necrons",
        p1_faction_dir="necrons",
        p2_faction_dir="necrons",
    )
    session["round_choice_active_Necrons"] = protocol_id
    session["round_choice_directive_Necrons"] = directive
    if subfaction:
        session["p1_subfaction"] = subfaction
    _st_mock.session_state = session
    return session


def test_protocol_modifier_no_active_protocol_returns_empty() -> None:
    _protocol_session(None, None)
    assert get_active_round_choice_modifier("Necrons", "shooting", False) == {}


def test_protocol_modifier_no_directive_returns_empty() -> None:
    _protocol_session("wh40k_9e.necrons.faction.protocol_hungry_void", None)
    assert get_active_round_choice_modifier("Necrons", "shooting", False) == {}


def test_hungry_void_primary_not_a_numeric_modifier() -> None:
    # 9E D1 (ap_on_unmod_wound_6) is a per-die, class-B effect — never surfaced as
    # a numeric hit/wound/save modifier. Migrated from the old hit_modifier vehicle.
    _protocol_session("wh40k_9e.necrons.faction.protocol_hungry_void", "primary")
    assert get_active_round_choice_modifier("Necrons", "fight", True) == {}


def test_ap_on_wound_6_hungry_void_primary_melee() -> None:
    _protocol_session("wh40k_9e.necrons.faction.protocol_hungry_void", "primary")
    assert get_active_round_choice_ap_on_wound_6("Necrons", True) == 1


def test_ap_on_wound_6_skipped_in_shooting() -> None:
    _protocol_session("wh40k_9e.necrons.faction.protocol_hungry_void", "primary")
    assert get_active_round_choice_ap_on_wound_6("Necrons", False) == 0


def test_ap_on_wound_6_inactive_returns_zero() -> None:
    _protocol_session(None, None)
    assert get_active_round_choice_ap_on_wound_6("Necrons", True) == 0


def test_protocol_modifier_vengeful_stars_primary_ap_on_wound_6_in_shooting() -> None:
    # Plan 025 Step 3: D1 migrated from wound_modifier → ap_on_unmod_wound_6 (ranged).
    # Generic modifier dict no longer returns a wound key; the dedicated fn is used.
    _protocol_session("wh40k_9e.necrons.faction.protocol_vengeful_stars", "primary")
    result = get_active_round_choice_modifier("Necrons", "shooting", False)
    assert result == {}
    assert get_active_round_choice_ap_on_wound_6("Necrons", use_melee=False) == 1


def test_protocol_modifier_vengeful_stars_primary_ap_on_wound_6_not_in_melee() -> None:
    # D1 phase=shooting — must not fire in melee.
    _protocol_session("wh40k_9e.necrons.faction.protocol_vengeful_stars", "primary")
    assert get_active_round_choice_ap_on_wound_6("Necrons", use_melee=True) == 0


def test_protocol_modifier_eternal_guardian_primary_no_generic_save_key() -> None:
    # Plan 025 Step 4: D1 migrated from save_modifier → light_cover_if_stationary.
    # The generic modifier dict must NOT return a "save" key for Eternal Guardian primary.
    _protocol_session("wh40k_9e.necrons.faction.protocol_eternal_guardian", "primary")
    assert get_active_round_choice_modifier("Necrons", "shooting", False) == {}
    assert get_active_round_choice_modifier("Necrons", "fight", True) == {}


def test_light_cover_if_stationary_eternal_guardian_primary_when_stationary() -> None:
    # D1 active + unit did not move → light cover granted automatically.
    session = _protocol_session("wh40k_9e.necrons.faction.protocol_eternal_guardian", "primary")
    session["p1_units"] = {"test.unit": {"movement_choice": "stationary"}}
    assert get_active_round_choice_light_cover_if_stationary("Necrons", "test.unit") is True


def test_light_cover_if_stationary_eternal_guardian_primary_when_moved() -> None:
    # D1 active + unit moved → no automatic light cover.
    session = _protocol_session("wh40k_9e.necrons.faction.protocol_eternal_guardian", "primary")
    session["p1_units"] = {"test.unit": {"movement_choice": "moved"}}
    assert get_active_round_choice_light_cover_if_stationary("Necrons", "test.unit") is False


def test_light_cover_if_stationary_false_when_directive_inactive() -> None:
    # No protocol active → always False regardless of movement.
    session = _protocol_session(None, None)
    session["p1_units"] = {"test.unit": {"movement_choice": "stationary"}}
    assert get_active_round_choice_light_cover_if_stationary("Necrons", "test.unit") is False


def test_conquering_tyrant_secondary_not_a_generic_numeric_modifier() -> None:
    # 9E Directive 2 (shoot_after_fall_back) is not a generic numeric modifier — it is
    # only active in the shooting phase when the unit Fell Back, queried via the
    # dedicated get_active_round_choice_shoot_after_fall_back function.
    _protocol_session("wh40k_9e.necrons.faction.protocol_conquering_tyrant", "secondary")
    result = get_active_round_choice_modifier("Necrons", "fight", True)
    assert result == {}


def test_strength_if_charged_hungry_void_secondary_when_charged() -> None:
    _protocol_session("wh40k_9e.necrons.faction.protocol_hungry_void", "secondary")
    assert get_active_round_choice_strength_if_charged("Necrons", {"charged": True}, True) == 1


def test_strength_if_charged_when_was_charged() -> None:
    _protocol_session("wh40k_9e.necrons.faction.protocol_hungry_void", "secondary")
    assert get_active_round_choice_strength_if_charged("Necrons", {"was_charged": True}, True) == 1


def test_strength_if_charged_when_heroic_intervened() -> None:
    _protocol_session("wh40k_9e.necrons.faction.protocol_hungry_void", "secondary")
    flags = {"heroic_intervened": True}
    assert get_active_round_choice_strength_if_charged("Necrons", flags, True) == 1


def test_strength_if_charged_zero_when_not_charged() -> None:
    _protocol_session("wh40k_9e.necrons.faction.protocol_hungry_void", "secondary")
    assert get_active_round_choice_strength_if_charged("Necrons", {}, True) == 0


def test_strength_if_charged_zero_in_shooting() -> None:
    _protocol_session("wh40k_9e.necrons.faction.protocol_hungry_void", "secondary")
    assert get_active_round_choice_strength_if_charged("Necrons", {"charged": True}, False) == 0


def test_strength_if_charged_not_a_numeric_modifier() -> None:
    # Secondary directive is consumed via the dedicated function, not the generic
    # numeric-modifier dict. Migrated from the old strength_modifier vehicle.
    _protocol_session("wh40k_9e.necrons.faction.protocol_hungry_void", "secondary")
    assert get_active_round_choice_modifier("Necrons", "fight", True) == {}


def test_modifier_inactive_returns_empty() -> None:
    _protocol_session(None, None)
    assert get_active_round_choice_modifier("Necrons", "shooting", False) == {}


def test_vengeful_stars_secondary_ignore_cover_half_range_active() -> None:
    # Plan 025 Step 3: D2 migrated from ap_bonus → ignore_cover_half_range (ranged, class B).
    # Generic modifier dict no longer returns an ap key for this directive.
    _protocol_session("wh40k_9e.necrons.faction.protocol_vengeful_stars", "secondary")
    result = get_active_round_choice_modifier("Necrons", "shooting", False)
    assert result == {}
    assert get_active_round_choice_ignores_cover_half_range("Necrons") is True


def test_vengeful_stars_secondary_ignore_cover_false_when_inactive() -> None:
    _protocol_session(None, None)
    assert get_active_round_choice_ignores_cover_half_range("Necrons") is False


def test_move_bonus_wired_movement() -> None:
    _protocol_session("wh40k_9e.necrons.faction.protocol_sudden_storm", "primary")
    result = get_active_round_choice_modifier("Necrons", "movement", False)
    assert result == {"move": 1}


def test_conquering_tyrant_primary_aura_range_bonus_not_a_numeric_modifier() -> None:
    # 9E Directive 1: +3" aura range. Class B (table-only), enforcement: table.
    # The App does NOT compute a numeric modifier for this — get_active_round_choice_modifier
    # must return {} (no "leadership" key, no hit/wound/strength/ap/move key).
    _protocol_session("wh40k_9e.necrons.faction.protocol_conquering_tyrant", "primary")
    result = get_active_round_choice_modifier("Necrons", "any", False)
    assert result == {}


def test_conquering_tyrant_secondary_shoot_after_fall_back_returns_minus_one_when_fell_back() -> (
    None
):
    # 9E Directive 2: eligible to shoot after Fall Back with −1 Hit. Class A.
    # units_key_for("Necrons") == "p1_units" because first_player == "Necrons".
    # Migration note: movement_choice is "retreated" (the value the app sets in
    # movementPhase.py / unitMutations.py) — the earlier "fall_back" value was
    # app-foreign and never matched actual session state (bug root cause).
    session = _protocol_session("wh40k_9e.necrons.faction.protocol_conquering_tyrant", "secondary")
    session["p1_units"] = {"uid-overlord": {"movement_choice": "retreated"}}
    assert get_active_round_choice_shoot_after_fall_back("Necrons", "uid-overlord") == -1


def test_conquering_tyrant_secondary_shoot_after_fall_back_zero_when_not_fell_back() -> None:
    # No penalty if the unit did not Fall Back.
    session = _protocol_session("wh40k_9e.necrons.faction.protocol_conquering_tyrant", "secondary")
    session["p1_units"] = {"uid-overlord": {"movement_choice": "normal"}}
    assert get_active_round_choice_shoot_after_fall_back("Necrons", "uid-overlord") == 0


def test_conquering_tyrant_secondary_shoot_after_fall_back_zero_when_inactive() -> None:
    # Directive not active → no modifier.
    session = _protocol_session(None, None)
    session["p1_units"] = {"uid-overlord": {"movement_choice": "retreated"}}
    assert get_active_round_choice_shoot_after_fall_back("Necrons", "uid-overlord") == 0


def test_fall_back_hit_mod_wiring_requires_atk_uid_in_entry() -> None:
    """Bug 1: _render_resolution_tab reads ``entry.get("atk_uid", "")`` and feeds it
    to get_active_round_choice_shoot_after_fall_back. With the resolution-tab read
    path, a populated ``atk_uid`` yields the −1 Hit debuff; the old buggy entry dict
    (no ``atk_uid`` → empty string) silently dropped it to 0.
    """
    session = _protocol_session("wh40k_9e.necrons.faction.protocol_conquering_tyrant", "secondary")
    session["p1_units"] = {"uid-overlord": {"movement_choice": "retreated"}}

    # Mirrors the exact read in _common._render_resolution_tab:
    #     atk_uid = entry.get("atk_uid", "")
    fixed_entry = {"def_faction": "Necrons", "def_uid": "uid-target", "atk_uid": "uid-overlord"}
    buggy_entry = {"def_faction": "Necrons", "def_uid": "uid-target"}  # pre-fix: no atk_uid

    assert (
        get_active_round_choice_shoot_after_fall_back("Necrons", fixed_entry.get("atk_uid", ""))
        == -1
    )
    assert (
        get_active_round_choice_shoot_after_fall_back("Necrons", buggy_entry.get("atk_uid", ""))
        == 0
    )


def test_sudden_storm_secondary_does_not_grant_advance_and_charge() -> None:
    # 9E Directive 2 of Sudden Storm is "shoot during an Action" (B-hint), NOT
    # advance-and-charge (Plan 025 Step 1: that effect was non-canonical).
    _protocol_session("wh40k_9e.necrons.faction.protocol_sudden_storm", "secondary")
    unit = _make_unit(rules=[], keywords=["NECRON"])
    assert charge_after_advance_allowed("Necrons", unit) is False


def test_advance_and_charge_inactive_returns_false() -> None:
    _protocol_session(None, None)
    unit = _make_unit(rules=[], keywords=["NECRON"])
    assert charge_after_advance_allowed("Necrons", unit) is False


def test_rp_reroll_undying_legions_secondary() -> None:
    # 9E Directive 2 = RP re-roll (Plan 025 Step 1: slots aligned to D1/D2 order).
    _protocol_session("wh40k_9e.necrons.faction.protocol_undying_legions", "secondary")
    assert get_active_rp_modifiers("Necrons") == {"rp_reroll": True}


def test_rp_modifiers_empty_for_undying_legions_primary() -> None:
    # Primary (9E Directive 1) is a Living-Metal heal_bonus, NOT a Reanimation-pool
    # effect — get_active_rp_modifiers must not surface it (S89 data fix).
    _protocol_session("wh40k_9e.necrons.faction.protocol_undying_legions", "primary")
    assert get_active_rp_modifiers("Necrons") == {}


def test_rp_modifier_empty_when_other_directive() -> None:
    _protocol_session("wh40k_9e.necrons.faction.protocol_hungry_void", "primary")
    assert get_active_rp_modifiers("Necrons") == {}


def test_heal_bonus_undying_legions_primary_applies_to_living_metal() -> None:
    # 9E Directive 1 = Living Metal +1 heal (Plan 025 Step 1: slots aligned to D1/D2).
    _protocol_session("wh40k_9e.necrons.faction.protocol_undying_legions", "primary")
    unit = _make_unit(rules=["livingMetal"])
    assert get_active_heal_bonus("Necrons", unit) == 1


def test_heal_bonus_zero_when_unit_lacks_target_rule() -> None:
    _protocol_session("wh40k_9e.necrons.faction.protocol_undying_legions", "primary")
    unit = _make_unit(rules=[])  # no livingMetal -> directive does not match
    assert get_active_heal_bonus("Necrons", unit) == 0


def test_heal_bonus_zero_for_reroll_directive() -> None:
    _protocol_session("wh40k_9e.necrons.faction.protocol_undying_legions", "secondary")
    unit = _make_unit(rules=["livingMetal"])
    assert get_active_heal_bonus("Necrons", unit) == 0


def test_heal_bonus_zero_when_no_directive() -> None:
    _protocol_session(None, None)
    unit = _make_unit(rules=["livingMetal"])
    assert get_active_heal_bonus("Necrons", unit) == 0


def test_protocol_modifier_ork_faction_no_protocols_returns_empty() -> None:
    _protocol_session("wh40k_9e.necrons.faction.protocol_hungry_void", "primary")
    result = get_active_round_choice_modifier("orks", "shooting", False)
    assert result == {}


# ---------------------------------------------------------------------------
# 6th (always-active) protocol + dynasty bonus — effects must reach the engine,
# not only the badge/caption (S93 root-cause fix for bugs 1b/1c).
# ---------------------------------------------------------------------------

_ALL_PROTOCOLS = [
    "wh40k_9e.necrons.faction.protocol_eternal_guardian",
    "wh40k_9e.necrons.faction.protocol_hungry_void",
    "wh40k_9e.necrons.faction.protocol_conquering_tyrant",
    "wh40k_9e.necrons.faction.protocol_sudden_storm",
    "wh40k_9e.necrons.faction.protocol_undying_legions",
    "wh40k_9e.necrons.faction.protocol_vengeful_stars",
]


def _extra_protocol_session(
    extra_id: str,
    *,
    extra_directive: str | None = None,
    subfaction: str | None = None,
    round_active: str | None = None,
    round_directive: str | None = None,
) -> _S:
    """Session where ``extra_id`` is the always-active 6th protocol.

    The other five protocols fill rounds 1-5 (so ``extra_id`` is the leftover).
    Optionally also assigns a round-assigned protocol and a subfaction.
    """
    assigned = [p for p in _ALL_PROTOCOLS if p != extra_id]
    session = _S(first_player="Necrons", p1_faction_dir="necrons", p2_faction_dir="necrons")
    session["round_choice_active_Necrons"] = round_active
    session["round_choice_directive_Necrons"] = round_directive
    session["round_choice_assignments"] = {
        "Necrons": {i + 1: pid for i, pid in enumerate(assigned)}
    }
    if extra_directive:
        session["round_choice_extra_directive_Necrons"] = extra_directive
    if subfaction:
        session["p1_subfaction"] = subfaction
    _st_mock.session_state = session
    return session


def test_extra_protocol_rp_reroll_via_6th_directive() -> None:
    # Bug 1b: Undying Legions as the always-active 6th protocol, secondary directive
    # (9E D2 = RP re-roll) chosen -> RP re-roll active (previously only the round slot
    # was read). Slots aligned to D1/D2 order in Plan 025 Step 1.
    _extra_protocol_session(
        "wh40k_9e.necrons.faction.protocol_undying_legions", extra_directive="secondary"
    )
    assert get_active_rp_modifiers("Necrons") == {"rp_reroll": True}


def test_extra_protocol_heal_bonus_via_6th_directive() -> None:
    # Bug 1c: Undying Legions as the 6th protocol, primary directive (9E D1 = Living
    # Metal +1 heal).
    _extra_protocol_session(
        "wh40k_9e.necrons.faction.protocol_undying_legions", extra_directive="primary"
    )
    unit = _make_unit(rules=["livingMetal"])
    assert get_active_heal_bonus("Necrons", unit) == 1


def test_extra_protocol_inactive_without_directive() -> None:
    # 6th protocol present but no directive chosen and no affinity -> no effect.
    _extra_protocol_session("wh40k_9e.necrons.faction.protocol_undying_legions")
    assert get_active_rp_modifiers("Necrons") == {}
    assert get_active_heal_bonus("Necrons", _make_unit(rules=["livingMetal"])) == 0


def test_dynasty_affinity_activates_both_directives() -> None:
    # Bug 3 wiring: matching subfaction -> the 6th protocol's BOTH directives apply
    # with no explicit choice. Undying Legions affinity is szarekhan: primary
    # (rp_reroll) and secondary (heal_bonus) are both active.
    _extra_protocol_session(
        "wh40k_9e.necrons.faction.protocol_undying_legions", subfaction="szarekhan"
    )
    assert get_active_rp_modifiers("Necrons") == {"rp_reroll": True}
    assert get_active_heal_bonus("Necrons", _make_unit(rules=["livingMetal"])) == 1


def test_dynasty_affinity_other_subfaction_inert() -> None:
    # Non-matching subfaction -> no implicit both-directive activation.
    _extra_protocol_session(
        "wh40k_9e.necrons.faction.protocol_undying_legions", subfaction="nihilakh"
    )
    assert get_active_rp_modifiers("Necrons") == {}


# ---------------------------------------------------------------------------
# S140: dynasty affinity in the ROUND-ASSIGNED protocol slot (not just the 6th).
# has_round now gates on active_id alone (not active_id AND directive) so the
# affinity check is reachable without a manual directive pick. One case per
# official dynasty (S139 concept table), plus non-affinity/non-regression cases.
# ---------------------------------------------------------------------------


def test_round_dynasty_affinity_nihilakh_eternal_guardian_both_directives() -> None:
    _protocol_session(
        "wh40k_9e.necrons.faction.protocol_eternal_guardian", None, subfaction="nihilakh"
    )
    types = {"light_cover_if_stationary", "hold_steady_or_set_to_defend"}
    assert {e["type"] for e in get_active_protocol_effects("Necrons", types)} == types


def test_round_dynasty_affinity_novokh_hungry_void_both_directives() -> None:
    _protocol_session("wh40k_9e.necrons.faction.protocol_hungry_void", None, subfaction="novokh")
    types = {"ap_on_unmod_wound_6", "strength_if_charged"}
    assert {e["type"] for e in get_active_protocol_effects("Necrons", types)} == types


def test_round_dynasty_affinity_sautekh_conquering_tyrant_both_directives() -> None:
    _protocol_session(
        "wh40k_9e.necrons.faction.protocol_conquering_tyrant", None, subfaction="sautekh"
    )
    types = {"aura_range_bonus", "shoot_after_fall_back"}
    assert {e["type"] for e in get_active_protocol_effects("Necrons", types)} == types


def test_round_dynasty_affinity_nephrekh_sudden_storm_both_directives() -> None:
    _protocol_session("wh40k_9e.necrons.faction.protocol_sudden_storm", None, subfaction="nephrekh")
    types = {"move_bonus", "shoot_during_action"}
    assert {e["type"] for e in get_active_protocol_effects("Necrons", types)} == types


def test_round_dynasty_affinity_szarekhan_undying_legions_both_directives() -> None:
    _protocol_session(
        "wh40k_9e.necrons.faction.protocol_undying_legions", None, subfaction="szarekhan"
    )
    types = {"heal_bonus", "rp_reroll"}
    assert {e["type"] for e in get_active_protocol_effects("Necrons", types)} == types


def test_round_dynasty_affinity_mephrit_vengeful_stars_both_directives() -> None:
    _protocol_session(
        "wh40k_9e.necrons.faction.protocol_vengeful_stars", None, subfaction="mephrit"
    )
    types = {"ap_on_unmod_wound_6", "ignore_cover_half_range"}
    assert {e["type"] for e in get_active_protocol_effects("Necrons", types)} == types


def test_round_dynasty_affinity_other_subfaction_inert_no_directive() -> None:
    # Non-matching subfaction, no manual directive -> round slot contributes nothing.
    _protocol_session("wh40k_9e.necrons.faction.protocol_hungry_void", None, subfaction="sautekh")
    types = {"ap_on_unmod_wound_6", "strength_if_charged"}
    assert get_active_protocol_effects("Necrons", types) == []


def test_round_no_affinity_manual_directive_still_picks_one_effect() -> None:
    # Non-regression (case c): no affinity, directive explicitly chosen -> unchanged
    # single-directive behaviour survives the has_round gate loosening.
    _protocol_session(
        "wh40k_9e.necrons.faction.protocol_hungry_void", "primary", subfaction="sautekh"
    )
    types = {"ap_on_unmod_wound_6", "strength_if_charged"}
    effects = get_active_protocol_effects("Necrons", types)
    assert {e["type"] for e in effects} == {"ap_on_unmod_wound_6"}


# ---------------------------------------------------------------------------
# get_active_protocol_effects — generic directive-effect filter (Plan 016 Step 2)
# ---------------------------------------------------------------------------


def test_get_active_protocol_effects_empty_when_no_protocol_active() -> None:
    """No active protocol -> empty list for any requested type set."""
    _protocol_session(None, None)
    assert get_active_protocol_effects("Necrons", {"rp_reroll"}) == []


def test_get_active_protocol_effects_returns_rp_reroll_for_undying_legions_secondary() -> None:
    """Undying Legions D2 (rp_reroll) is returned when requested by type."""
    _protocol_session("wh40k_9e.necrons.faction.protocol_undying_legions", "secondary")
    effects = get_active_protocol_effects("Necrons", {"rp_reroll"})
    assert len(effects) == 1
    assert effects[0]["type"] == "rp_reroll"


def test_get_active_protocol_effects_type_filter_excludes_non_matching() -> None:
    """rp_reroll directive is NOT returned when a different type set is requested."""
    _protocol_session("wh40k_9e.necrons.faction.protocol_undying_legions", "secondary")
    effects = get_active_protocol_effects("Necrons", {"heal_bonus"})
    assert effects == []


def test_get_active_protocol_effects_dynasty_both_directives_included() -> None:
    """Dynasty bonus activates both directives of the 6th protocol;
    get_active_protocol_effects returns effects of both types."""
    _extra_protocol_session(
        "wh40k_9e.necrons.faction.protocol_undying_legions", subfaction="szarekhan"
    )
    rp_effects = get_active_protocol_effects("Necrons", {"rp_reroll"})
    heal_effects = get_active_protocol_effects("Necrons", {"heal_bonus"})
    assert len(rp_effects) == 1
    assert rp_effects[0]["type"] == "rp_reroll"
    assert len(heal_effects) == 1
    assert heal_effects[0]["type"] == "heal_bonus"


def test_get_active_protocol_effects_multi_type_query_returns_all_matching() -> None:
    """Querying multiple types at once includes every matching effect."""
    _extra_protocol_session(
        "wh40k_9e.necrons.faction.protocol_undying_legions", subfaction="szarekhan"
    )
    effects = get_active_protocol_effects("Necrons", {"rp_reroll", "heal_bonus"})
    types_found = {e["type"] for e in effects}
    assert types_found == {"rp_reroll", "heal_bonus"}


def test_get_active_protocol_effects_carries_source_id() -> None:
    """Returned effect dicts have _source_id for label resolution."""
    _protocol_session("wh40k_9e.necrons.faction.protocol_undying_legions", "secondary")
    effects = get_active_protocol_effects("Necrons", {"rp_reroll"})
    assert all("_source_id" in e for e in effects)


def test_get_active_rp_modifiers_delegates_to_protocol_effects() -> None:
    """get_active_rp_modifiers returns rp_reroll:True iff get_active_protocol_effects finds it."""
    _protocol_session("wh40k_9e.necrons.faction.protocol_undying_legions", "secondary")
    assert get_active_rp_modifiers("Necrons") == {"rp_reroll": True}
    _protocol_session("wh40k_9e.necrons.faction.protocol_undying_legions", "primary")
    assert get_active_rp_modifiers("Necrons") == {}


def test_round_and_extra_modifiers_accumulate() -> None:
    # Round-assigned directive AND the 6th protocol's directive both feed the engine.
    # Plan 025 Step 4: Eternal Guardian primary is now light_cover_if_stationary — it no
    # longer contributes a "save" key to the generic modifier dict. The generic dict is
    # empty; only the Vengeful D1 ap_on_wound_6 effect is reachable via the dedicated fn.
    _extra_protocol_session(
        "wh40k_9e.necrons.faction.protocol_vengeful_stars",
        extra_directive="primary",
        round_active="wh40k_9e.necrons.faction.protocol_eternal_guardian",
        round_directive="primary",
    )
    assert get_active_round_choice_modifier("Necrons", "shooting", False) == {}
    # The ap_on_wound_6 effect from the 6th Vengeful protocol is reachable via the dedicated fn.
    assert get_active_round_choice_ap_on_wound_6("Necrons", use_melee=False) == 1


def test_get_short_label_for_effect_type_returns_source_protocol_not_round_active() -> None:
    # Regression: when Vengeful Stars is the 6th (extra) protocol and Eternal Guardian
    # is round-assigned, the AP-on-wound-6 badge must show "Vengeful Stars", NOT
    # "Eternal Guardian" (the round-active one). Previously _round_choice_short_label
    # always read the round-active slot, causing wrong labels for extra-protocol effects.
    _extra_protocol_session(
        "wh40k_9e.necrons.faction.protocol_vengeful_stars",
        extra_directive="primary",
        round_active="wh40k_9e.necrons.faction.protocol_eternal_guardian",
        round_directive="primary",
    )
    label = get_short_label_for_effect_type("Necrons", "ap_on_unmod_wound_6")
    assert label == "Vengeful Stars", (
        f"Expected 'Vengeful Stars' but got {label!r}. "
        "The label must reflect the effect's actual source protocol, not the round-assigned one."
    )


def test_get_short_label_for_effect_type_ignore_cover_returns_source_protocol() -> None:
    # Regression: Light Cover badge also uses get_short_label_for_effect_type.
    # Vengeful Stars secondary (ignore_cover_half_range) as the 6th protocol —
    # the label must be "Vengeful Stars" regardless of the round-assigned protocol.
    _extra_protocol_session(
        "wh40k_9e.necrons.faction.protocol_vengeful_stars",
        extra_directive="secondary",
        round_active="wh40k_9e.necrons.faction.protocol_eternal_guardian",
        round_directive="primary",
    )
    label = get_short_label_for_effect_type("Necrons", "ignore_cover_half_range")
    assert label == "Vengeful Stars", f"Expected 'Vengeful Stars' but got {label!r}."


def test_get_short_label_for_effect_type_returns_none_when_inactive() -> None:
    # No ap_on_unmod_wound_6 active → must return None (not crash, not return stale data).
    _extra_protocol_session(
        "wh40k_9e.necrons.faction.protocol_eternal_guardian",
        extra_directive="primary",
    )
    label = get_short_label_for_effect_type("Necrons", "ap_on_unmod_wound_6")
    assert label is None


def test_get_short_label_for_effect_type_round_assigned_protocol_correct() -> None:
    # When Vengeful Stars IS the round-assigned protocol (not the 6th), the label
    # should still resolve correctly to "Vengeful Stars".
    session = _S(first_player="Necrons", p1_faction_dir="necrons", p2_faction_dir="necrons")
    session["round_choice_active_Necrons"] = "wh40k_9e.necrons.faction.protocol_vengeful_stars"
    session["round_choice_directive_Necrons"] = "primary"
    _st_mock.session_state = session
    label = get_short_label_for_effect_type("Necrons", "ap_on_unmod_wound_6")
    assert label == "Vengeful Stars"


# ---------------------------------------------------------------------------
# get_activated_command_abilities — unit-scoped activated abilities
# ---------------------------------------------------------------------------


def test_get_activated_command_abilities_overlord_returns_mwbd() -> None:
    abilities = get_activated_command_abilities("wh40k_9e.necrons.unit.overlord", "necrons")
    assert any(a.id == "wh40k_9e.necrons.unit.overlord.my_will_be_done" for a in abilities)


def test_get_activated_command_abilities_mwbd_has_badge_label() -> None:
    abilities = get_activated_command_abilities("wh40k_9e.necrons.unit.overlord", "necrons")
    mwbd = next(a for a in abilities if a.id == "wh40k_9e.necrons.unit.overlord.my_will_be_done")
    assert mwbd.badge_label == "MWBD"


def test_get_activated_command_abilities_mwbd_effect_type_buff_roll() -> None:
    abilities = get_activated_command_abilities("wh40k_9e.necrons.unit.overlord", "necrons")
    mwbd = next(a for a in abilities if a.id == "wh40k_9e.necrons.unit.overlord.my_will_be_done")
    assert mwbd.effect.type == "buff_roll"


def test_get_activated_command_abilities_necron_lord_returns_lords_will() -> None:
    abilities = get_activated_command_abilities("wh40k_9e.necrons.unit.necron_lord", "necrons")
    assert any(a.id == "wh40k_9e.necrons.unit.necron_lord.the_lords_will" for a in abilities)


def test_get_activated_command_abilities_warriors_returns_empty() -> None:
    abilities = get_activated_command_abilities("wh40k_9e.necrons.unit.warriors", "necrons")
    assert abilities == []


def test_get_activated_command_abilities_ork_faction_returns_empty() -> None:
    abilities = get_activated_command_abilities("wh40k_9e.necrons.unit.overlord", "orks")
    assert abilities == []


def test_get_triggered_abilities_ork_command_returns_empty() -> None:
    units, _ = load_army("orks")
    session = _S(first_player="Necrons", p1_faction_dir="necrons", p2_faction_dir="orks")
    _st_mock.session_state = session
    state = {
        "active": "Orks",
        "first_player": "Necrons",
        "p2_units": {
            u.id: {
                "current_wounds": u.wounds * u.models_max,
                "models": u.models_max,
                "destroyed": False,
            }
            for u in units
        },
    }
    triggered = get_triggered_abilities(state, "command", "phase_start")
    assert triggered == []


def _orks_activated_session() -> _S:
    """Session state with WAAAGH stage 1 active via the generic activated_abilities key."""
    return _S(
        activated_abilities={
            "Orks": {"ability_id": "wh40k_9e.orks.faction.waaagh_stage1", "round_activated": 1}
        },
        first_player="Orks",
        p1_faction_dir="orks",
    )


def test_atk_bonus_one_for_ork_with_active_ability() -> None:
    _eng.st.session_state = _orks_activated_session()
    unit = _make_unit(rules=[], keywords=["ORK", "CORE"])
    assert buff_stat_bonus("Orks", unit, "attacks") == 1


def test_atk_bonus_zero_without_active_ability() -> None:
    _eng.st.session_state = {"activated_abilities": {}}
    unit = _make_unit(rules=[], keywords=["ORK"])
    assert buff_stat_bonus("Orks", unit, "attacks") == 0


def test_atk_bonus_zero_for_non_ork_unit() -> None:
    _eng.st.session_state = _orks_activated_session()
    unit = _make_unit(rules=[], keywords=["NECRON"])
    assert buff_stat_bonus("Orks", unit, "attacks") == 0


def test_atk_bonus_applies_to_ork_keyword_unit() -> None:
    _eng.st.session_state = _orks_activated_session()
    unit = _make_unit(rules=[], keywords=["ORK"])
    assert buff_stat_bonus("Orks", unit, "attacks") == 1


def test_atk_bonus_zero_without_ability_id_in_state() -> None:
    _eng.st.session_state = {"activated_abilities": {"Orks": {}}}
    unit = _make_unit(rules=[], keywords=["ORK"])
    assert buff_stat_bonus("Orks", unit, "attacks") == 0


def test_buff_stat_bonus_generic_strength() -> None:
    _eng.st.session_state = _orks_activated_session()
    unit = _make_unit(rules=[], keywords=["ORK"])
    assert buff_stat_bonus("Orks", unit, "strength") == 1
    assert buff_stat_bonus("Orks", unit, "toughness") == 0


# stratagem_strength_bonus tests moved to
# tests/gameMechanic/test_stratagem_engine.py (S142 Aufgabe 1, Option B — the
# function itself moved to gameMechanic.stratagemEngine).


# ---------------------------------------------------------------------------
# Failsafe Overcharger dispatch pilot (Plan 024 Step 5)
# ---------------------------------------------------------------------------

_FAILSAFE_ID = "wh40k_9e.necrons.arkana.failsafe_overcharger"


def test_failsafe_overcharger_loaded_as_activated() -> None:
    from gameObjects.loader import load_faction_abilities  # noqa: PLC0415

    abilities = load_faction_abilities("necrons")
    failsafe = next((a for a in abilities if a.id == _FAILSAFE_ID), None)
    assert failsafe is not None
    assert failsafe.ability_type == "activated"
    assert failsafe.effect.type == "multi"


def _failsafe_activated_session() -> _S:
    return _S(
        activated_abilities={"Necrons": {"ability_id": _FAILSAFE_ID, "round_activated": 1}},
        first_player="Necrons",
        p1_faction_dir="necrons",
    )


def test_failsafe_overcharger_buff_stat_applied() -> None:
    _eng.st.session_state = _failsafe_activated_session()
    canoptek = _make_unit(rules=[], keywords=["NECRON", "CANOPTEK"])
    assert buff_stat_bonus("Necrons", canoptek, "attacks") == 1


def test_failsafe_overcharger_skips_non_canoptek_unit() -> None:
    _eng.st.session_state = _failsafe_activated_session()
    warrior = _make_unit(rules=[], keywords=["NECRON", "CORE"])
    assert buff_stat_bonus("Necrons", warrior, "attacks") == 0


def test_charge_after_advance_requires_core_or_character() -> None:
    _eng.st.session_state = _orks_activated_session()
    unit_plain = _make_unit(rules=[], keywords=["ORK"])
    unit_core = _make_unit(rules=[], keywords=["ORK", "CORE"])
    unit_char = _make_unit(rules=[], keywords=["ORK", "CHARACTER"])
    assert not charge_after_advance_allowed("Orks", unit_plain)
    assert charge_after_advance_allowed("Orks", unit_core)
    assert charge_after_advance_allowed("Orks", unit_char)


def test_ability_badge_label_returns_yaml_value() -> None:
    _eng.st.session_state = _orks_activated_session()
    unit = _make_unit(rules=[], keywords=["ORK"])
    assert ability_badge_label("Orks", unit) == "WAAAGH! S1"


def test_ability_badge_label_none_for_non_matching_unit() -> None:
    _eng.st.session_state = _orks_activated_session()
    unit = _make_unit(rules=[], keywords=["NECRON"])
    assert ability_badge_label("Orks", unit) is None


def test_unit_matches_target_any_of_logic() -> None:
    unit = _make_unit(rules=[], keywords=["ORK", "CORE"])
    assert _unit_matches_target(
        unit, {"target_keywords": ["ORK"], "target_keywords_any": ["CORE", "CHARACTER"]}
    )
    assert not _unit_matches_target(
        unit, {"target_keywords": ["ORK"], "target_keywords_any": ["CHARACTER"]}
    )
    assert _unit_matches_target(unit, {})
    assert not _unit_matches_target(unit, {"target_keywords": ["NECRON"]})


# ---------------------------------------------------------------------------
# ability_invuln_save — R-COMBAT-09: best (smallest) of multiple invuln saves
# ---------------------------------------------------------------------------


def test_ability_invuln_save_picks_best_of_multiple(monkeypatch: pytest.MonkeyPatch) -> None:
    """R-COMBAT-09: two active invuln effects → the smaller value (better save) wins."""
    monkeypatch.setattr(
        _eng,
        "_active_effects_for_faction",
        lambda faction: [
            {"type": "invuln_save", "modifier": 5},
            {"type": "invuln_save", "modifier": 4},
        ],
    )
    unit = _make_unit(rules=[], keywords=["NECRON"])
    assert ability_invuln_save("Necrons", unit) == 4


def test_ability_invuln_save_none_without_invuln_effect(monkeypatch: pytest.MonkeyPatch) -> None:
    """No invuln_save effect active → no granted invuln save."""
    monkeypatch.setattr(
        _eng,
        "_active_effects_for_faction",
        lambda faction: [{"type": "buff_stat", "stat": "attacks", "modifier": 1}],
    )
    unit = _make_unit(rules=[], keywords=["NECRON"])
    assert ability_invuln_save("Necrons", unit) is None


def test_ability_invuln_save_skips_non_matching_unit(monkeypatch: pytest.MonkeyPatch) -> None:
    """An invuln effect targeting other keywords does not apply to this unit."""
    monkeypatch.setattr(
        _eng,
        "_active_effects_for_faction",
        lambda faction: [
            {"type": "invuln_save", "modifier": 4, "target_keywords": ["VEHICLE"]},
        ],
    )
    unit = _make_unit(rules=[], keywords=["NECRON"])
    assert ability_invuln_save("Necrons", unit) is None


# ---------------------------------------------------------------------------
# unit_wound_auto_fail_max — B-056: Quantum Shielding's "unmodified wound roll
# of 1-3 always fails" clause (docs/work/wahapedia_necrons/units_all.txt:112).
# ---------------------------------------------------------------------------


def _wound_auto_fail_ability(rule: str, max_roll: int, badge_label: str | None = None) -> Ability:
    return Ability(
        id=f"test.ability.wound_auto_fail.{rule}.{max_roll}",
        name_en="Test Wound Auto-fail",
        source="unit_ability",
        rule_text="test",
        trigger=Trigger(timing="persistent", phase="any", player="either"),
        conditions=[Condition(has_rules=[rule])],
        effect=Effect(type="wound_auto_fail", modifier=max_roll),
        badge_label=badge_label,
    )


def test_unit_wound_auto_fail_max_returns_modifier_for_matching_rule(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(
        _eng,
        "load_unit_abilities",
        lambda faction_dir: [_wound_auto_fail_ability("quantumShielding", 3)],
    )
    monkeypatch.setattr(_eng, "faction_dir_for", lambda faction: "necrons")
    unit = _make_unit(rules=["quantumShielding"], keywords=["VEHICLE"])
    assert unit_wound_auto_fail_max("Necrons", unit) == 3


def test_unit_wound_auto_fail_max_none_without_matching_rule(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """A unit without the intrinsic rule tag is unaffected (e.g. plain Warriors)."""
    monkeypatch.setattr(
        _eng,
        "load_unit_abilities",
        lambda faction_dir: [_wound_auto_fail_ability("quantumShielding", 3)],
    )
    monkeypatch.setattr(_eng, "faction_dir_for", lambda faction: "necrons")
    unit = _make_unit(rules=["livingMetal"], keywords=["VEHICLE"])
    assert unit_wound_auto_fail_max("Necrons", unit) is None


def test_unit_wound_auto_fail_max_ignores_other_effect_types(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """An invuln_save-effect ability with the same has_rules must not leak in here."""
    invuln_ability = Ability(
        id="test.ability.invuln",
        name_en="Test Invuln",
        source="unit_ability",
        rule_text="test",
        trigger=Trigger(timing="persistent", phase="any", player="either"),
        conditions=[Condition(has_rules=["quantumShielding"])],
        effect=Effect(type="invuln_save", modifier=5),
    )
    monkeypatch.setattr(_eng, "load_unit_abilities", lambda faction_dir: [invuln_ability])
    monkeypatch.setattr(_eng, "faction_dir_for", lambda faction: "necrons")
    unit = _make_unit(rules=["quantumShielding"], keywords=["VEHICLE"])
    assert unit_wound_auto_fail_max("Necrons", unit) is None


def test_unit_wound_auto_fail_max_picks_highest_of_multiple(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(
        _eng,
        "load_unit_abilities",
        lambda faction_dir: [
            _wound_auto_fail_ability("quantumShielding", 3),
            _wound_auto_fail_ability("quantumShielding", 2),
        ],
    )
    monkeypatch.setattr(_eng, "faction_dir_for", lambda faction: "necrons")
    unit = _make_unit(rules=["quantumShielding"], keywords=["VEHICLE"])
    assert unit_wound_auto_fail_max("Necrons", unit) == 3


# ---------------------------------------------------------------------------
# unit_wound_auto_fail_max — S148 regression: real YAML, Annihilation Barge.
# ---------------------------------------------------------------------------


def test_unit_wound_auto_fail_max_annihilation_barge_real_data() -> None:
    """S148-Befund: Annihilation Barge's Quantum Shielding must auto-fail
    unmodified wound rolls of 1-3 — regression against the real
    unit_abilities.yaml entry (not just a synthetic Ability)."""
    session = _S(first_player="Necrons", p1_faction_dir="necrons", p2_faction_dir="necrons")
    _st_mock.session_state = session
    units, _ = load_army("necrons")
    barge = next(u for u in units if u.id == "wh40k_9e.necrons.unit.annihilation_barge")
    assert unit_wound_auto_fail_max("Necrons", barge) == 3


def test_unit_wound_auto_fail_max_none_for_unit_without_quantum_shielding() -> None:
    """Control: a non-vehicle unit (Warriors) without the rule tag is unaffected."""
    session = _S(first_player="Necrons", p1_faction_dir="necrons", p2_faction_dir="necrons")
    _st_mock.session_state = session
    units, _ = load_army("necrons")
    warriors = next(u for u in units if u.id == "wh40k_9e.necrons.unit.warriors")
    assert unit_wound_auto_fail_max("Necrons", warriors) is None


# ---------------------------------------------------------------------------
# unit_wound_auto_fail_label — B-103: the wound-block badge must show the
# triggering ability's own name (e.g. "Quantum Shielding"), read from YAML,
# instead of a hardcoded "Auto-fail" placeholder.
# ---------------------------------------------------------------------------


def test_unit_wound_auto_fail_label_uses_badge_label(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(
        _eng,
        "load_unit_abilities",
        lambda faction_dir: [
            _wound_auto_fail_ability("quantumShielding", 3, badge_label="Quantum Shielding")
        ],
    )
    monkeypatch.setattr(_eng, "faction_dir_for", lambda faction: "necrons")
    unit = _make_unit(rules=["quantumShielding"], keywords=["VEHICLE"])
    assert unit_wound_auto_fail_label("Necrons", unit) == "Quantum Shielding"


def test_unit_wound_auto_fail_label_falls_back_to_name_en(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """No badge_label set → fall back to the ability's name_en, never a fixed string."""
    monkeypatch.setattr(
        _eng,
        "load_unit_abilities",
        lambda faction_dir: [_wound_auto_fail_ability("quantumShielding", 3)],
    )
    monkeypatch.setattr(_eng, "faction_dir_for", lambda faction: "necrons")
    unit = _make_unit(rules=["quantumShielding"], keywords=["VEHICLE"])
    assert unit_wound_auto_fail_label("Necrons", unit) == "Test Wound Auto-fail"


def test_unit_wound_auto_fail_label_none_without_matching_rule(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(
        _eng,
        "load_unit_abilities",
        lambda faction_dir: [
            _wound_auto_fail_ability("quantumShielding", 3, badge_label="Quantum Shielding")
        ],
    )
    monkeypatch.setattr(_eng, "faction_dir_for", lambda faction: "necrons")
    unit = _make_unit(rules=["livingMetal"], keywords=["VEHICLE"])
    assert unit_wound_auto_fail_label("Necrons", unit) is None


def test_unit_wound_auto_fail_label_annihilation_barge_real_data() -> None:
    """B-103 regression: real unit_abilities.yaml entry must expose the
    'Quantum Shielding' badge_label — the S156 stakeholder-visible bug showed
    the generic 'Auto-fail' text instead."""
    session = _S(first_player="Necrons", p1_faction_dir="necrons", p2_faction_dir="necrons")
    _st_mock.session_state = session
    units, _ = load_army("necrons")
    barge = next(u for u in units if u.id == "wh40k_9e.necrons.unit.annihilation_barge")
    assert unit_wound_auto_fail_label("Necrons", barge) == "Quantum Shielding"


# ---------------------------------------------------------------------------
# find_unit_ability_by_effect — B-028b: ownership lookup for unit-owned
# reactive abilities with an empty conditions list (e.g. Noctilith Beacons'
# deny_psychic), which _wound_auto_fail_ability's has_rules match cannot
# scope on its own.
# ---------------------------------------------------------------------------


def test_find_unit_ability_by_effect_matches_owning_unit(monkeypatch: pytest.MonkeyPatch) -> None:
    deny_ability = Ability(
        id="test.unit.hero.deny_ability",
        name_en="Test Deny Ability",
        source="unit_ability",
        rule_text="test",
        trigger=Trigger(timing="phase_reactive", phase="psychic", player="inactive"),
        conditions=[],
        effect=Effect(type="deny_psychic", target="self"),
        unit_id="test.unit.hero",
    )
    monkeypatch.setattr(_eng, "load_unit_abilities", lambda faction_dir: [deny_ability])
    found = find_unit_ability_by_effect("necrons", "test.unit.hero", "deny_psychic")
    assert found is deny_ability


def test_find_unit_ability_by_effect_none_for_other_unit(monkeypatch: pytest.MonkeyPatch) -> None:
    """Empty conditions must not leak the ability onto a different unit_id —
    ownership (unit_id), not conditions, is the scoping mechanism here."""
    deny_ability = Ability(
        id="test.unit.hero.deny_ability",
        name_en="Test Deny Ability",
        source="unit_ability",
        rule_text="test",
        trigger=Trigger(timing="phase_reactive", phase="psychic", player="inactive"),
        conditions=[],
        effect=Effect(type="deny_psychic", target="self"),
        unit_id="test.unit.hero",
    )
    monkeypatch.setattr(_eng, "load_unit_abilities", lambda faction_dir: [deny_ability])
    assert find_unit_ability_by_effect("necrons", "test.unit.other", "deny_psychic") is None


def test_find_unit_ability_by_effect_none_for_other_effect_type(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    heal_ability = Ability(
        id="test.unit.hero.heal_ability",
        name_en="Test Heal Ability",
        source="unit_ability",
        rule_text="test",
        trigger=Trigger(timing="phase_start", phase="any", player="either"),
        conditions=[],
        effect=Effect(type="heal", amount="1"),
        unit_id="test.unit.hero",
    )
    monkeypatch.setattr(_eng, "load_unit_abilities", lambda faction_dir: [heal_ability])
    assert find_unit_ability_by_effect("necrons", "test.unit.hero", "deny_psychic") is None


def test_find_unit_ability_by_effect_noctilith_beacons_real_data() -> None:
    """B-028b acceptance: the real unit_abilities.yaml entry for Szarekh's
    Noctilith Beacons must resolve via ownership, not just effect type."""
    found = find_unit_ability_by_effect(
        "necrons", "wh40k_9e.necrons.unit.the_silent_king", "deny_psychic"
    )
    assert found is not None
    assert found.id == "wh40k_9e.necrons.unit.the_silent_king.noctilith_beacons"


# ---------------------------------------------------------------------------
# _sum_effect_value — shared accumulate helper (S144 Plan Aufgabe 5, Option B).
# One test per call-site shape it replaced: get_active_round_choice_strength_
# if_charged / get_active_round_choice_ap_on_wound_6 (phase-predicate sum),
# get_active_heal_bonus (target_rule predicate), buff_stat_bonus
# (value_key="modifier" + stat/unit predicate), ability_invuln_save
# (combine=min, missing_value=None). stratagemEngine.stratagem_strength_bonus
# (type_key="roll_type" override) is covered in test_stratagem_engine.py.
# ---------------------------------------------------------------------------


def test_sum_effect_value_sums_matching_type_with_predicate() -> None:
    """Mirrors strength_if_charged/ap_on_wound_6: default value_key, predicate filters."""
    effects = [
        {"type": "strength_if_charged", "value": 1, "phase": "melee"},
        {"type": "strength_if_charged", "value": 2, "phase": "shooting"},
        {"type": "other", "value": 99},
    ]
    assert (
        _sum_effect_value(
            effects, "strength_if_charged", predicate=lambda e: e.get("phase") != "shooting"
        )
        == 1
    )


def test_sum_effect_value_returns_none_when_nothing_matches() -> None:
    assert _sum_effect_value([{"type": "other", "value": 5}], "heal_bonus") is None


def test_sum_effect_value_missing_key_defaults_to_zero_and_is_counted() -> None:
    """Default missing_value=0: an effect without the value_key still contributes (as 0)."""
    effects = [{"type": "heal_bonus"}, {"type": "heal_bonus", "value": 3}]
    assert _sum_effect_value(effects, "heal_bonus") == 3


def test_sum_effect_value_heal_bonus_target_rule_predicate() -> None:
    effects = [
        {"type": "heal_bonus", "value": 1, "target_rule": "livingMetal"},
        {"type": "heal_bonus", "value": 5, "target_rule": "otherRule"},
    ]
    assert (
        _sum_effect_value(
            effects, "heal_bonus", predicate=lambda e: e.get("target_rule") in ("livingMetal",)
        )
        == 1
    )


def test_sum_effect_value_custom_value_key_for_buff_stat() -> None:
    """Mirrors buff_stat_bonus: value_key='modifier' instead of the 'value' default."""
    effects = [
        {"type": "buff_stat", "stat": "attacks", "modifier": 1},
        {"type": "buff_stat", "stat": "strength", "modifier": 9},
    ]
    assert (
        _sum_effect_value(
            effects,
            "buff_stat",
            value_key="modifier",
            predicate=lambda e: e.get("stat") == "attacks",
        )
        == 1
    )


def test_sum_effect_value_missing_value_none_skips_effect() -> None:
    """Mirrors ability_invuln_save: missing_value=None drops effects without a modifier
    instead of counting them as 0 — a spurious 0 would win every min() comparison."""
    effects = [{"type": "invuln_save"}, {"type": "invuln_save", "modifier": 4}]
    assert _sum_effect_value(effects, "invuln_save", value_key="modifier", missing_value=None) == 4


def test_sum_effect_value_combine_min_seeds_from_first_match_not_zero() -> None:
    """combine=min must seed from the first matching value, not a 0 baseline —
    otherwise min(0, 5) would always report 0 even though no effect grants it."""
    effects = [{"type": "invuln_save", "modifier": 5}]
    assert _sum_effect_value(effects, "invuln_save", value_key="modifier", combine=min) == 5


# ---------------------------------------------------------------------------
# Coverage gap tests — branches not reached by the tests above
# ---------------------------------------------------------------------------


def test_execute_effect_heal_keyerror_in_heal_bonus_is_silenced() -> None:
    """Z.71-72: KeyError from get_active_heal_bonus (no faction-dir in session) is caught.

    The heal still applies with the base amount; no exception escapes.
    """
    import gameMechanic.unitMutations as _mut  # noqa: PLC0415

    # Session has a round-choice active but NO faction_dir keys, so faction_dir_for
    # raises KeyError inside get_active_heal_bonus → the except branch (Z.71-72) fires.
    session: dict = {
        "first_player": "Necrons",
        "round_choice_active_Necrons": "wh40k_9e.necrons.faction.protocol_undying_legions",
        "round_choice_directive_Necrons": "primary",
        "p1_units": {"test.unit": {"current_wounds": 4, "models": 2, "destroyed": False}},
    }
    _mut.st.session_state = session
    _eng.st.session_state = session
    unit = _make_unit(rules=["livingMetal"])
    result = execute_effect(_living_metal_ability(), "test.unit", "Necrons", unit)
    # Heal succeeds (base 1 HP: 4 → 5), bonus silently skipped.
    assert result is True
    assert session["p1_units"]["test.unit"]["current_wounds"] == 5


def test_extra_directive_effects_returns_empty_when_all_protocols_assigned() -> None:
    """Z.113: _extra_directive_effects returns [] when all 6 protocols are assigned
    (no unassigned extra remains → len(extras) == 0 != 1).
    """
    # Assign all 6 protocols to rounds 1-6 → no leftover extra.
    session = _S(first_player="Necrons", p1_faction_dir="necrons", p2_faction_dir="necrons")
    session["round_choice_active_Necrons"] = None
    session["round_choice_directive_Necrons"] = None
    session["round_choice_assignments"] = {
        "Necrons": {i + 1: pid for i, pid in enumerate(_ALL_PROTOCOLS)}
    }
    session["round_choice_extra_directive_Necrons"] = "primary"
    _st_mock.session_state = session
    # No extra protocol available → no effect active → modifier dict is empty.
    assert get_active_round_choice_modifier("Necrons", "shooting", False) == {}


def test_active_directive_effects_empty_for_faction_without_round_choices() -> None:
    """Z.151: _active_directive_effects returns [] when load_round_choice_abilities
    returns [] (faction has no round-choice YAML — unknown faction_dir).
    """
    session = _S(
        first_player="Necrons",
        p1_faction_dir="unknown_faction_no_yaml",
        p2_faction_dir="necrons",
    )
    session["round_choice_active_Necrons"] = "some.id"
    session["round_choice_directive_Necrons"] = "primary"
    _st_mock.session_state = session
    assert get_active_round_choice_modifier("Necrons", "shooting", False) == {}


def test_modifier_skips_phase_excluded_effect() -> None:
    """Z.190: a move_bonus effect with phase=melee is skipped in shooting context."""
    _protocol_session("wh40k_9e.necrons.faction.protocol_sudden_storm", "primary")
    # Sudden Storm primary is move_bonus with phase=any — it IS included.
    # We patch _active_directive_effects to return a melee-only move_bonus so Z.190 fires.
    original = _eng._active_directive_effects

    def _patched(player: str):  # type: ignore[no-untyped-def]
        return [{"type": "move_bonus", "value": 2, "phase": "melee"}]

    _eng._active_directive_effects = _patched
    try:
        result = get_active_round_choice_modifier("Necrons", "shooting", False)
    finally:
        _eng._active_directive_effects = original
    assert result == {}


def test_active_effects_for_faction_returns_empty_without_ability_id() -> None:
    """Z.364: _active_effects_for_faction returns [] when entry has no ability_id key."""
    _eng.st.session_state = {"activated_abilities": {"Orks": {"round_activated": 1}}}
    unit = _make_unit(rules=[], keywords=["ORK"])
    assert buff_stat_bonus("Orks", unit, "attacks") == 0


def test_active_effects_for_faction_returns_empty_for_non_multi_ability(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Z.368: _active_effects_for_faction returns [] when ability effect.type != 'multi'."""
    from gameObjects.loader import load_faction_abilities  # noqa: PLC0415

    abilities = load_faction_abilities("necrons")
    # Use Living Metal (type='heal', not 'multi') to hit the non-multi branch.
    heal_ability = next(
        (a for a in abilities if a.effect.type == "heal"),
        None,
    )
    assert heal_ability is not None, "Need a heal-type ability in necrons YAML"
    _eng.st.session_state = {
        "activated_abilities": {"Necrons": {"ability_id": heal_ability.id}},
        "first_player": "Necrons",
        "p1_faction_dir": "necrons",
    }
    unit = _make_unit(rules=[], keywords=["NECRON"])
    assert buff_stat_bonus("Necrons", unit, "attacks") == 0


def test_ability_badge_label_none_without_activated_entry() -> None:
    """Z.400: ability_badge_label returns None when no activated_abilities entry exists."""
    _eng.st.session_state = {"activated_abilities": {}}
    unit = _make_unit(rules=[], keywords=["NECRON"])
    assert ability_badge_label("Necrons", unit) is None


def test_ability_badge_label_none_when_entry_has_no_ability_id() -> None:
    """Z.403: ability_badge_label returns None when entry exists but has no ability_id."""
    _eng.st.session_state = {"activated_abilities": {"Necrons": {"round_activated": 1}}}
    unit = _make_unit(rules=[], keywords=["NECRON"])
    assert ability_badge_label("Necrons", unit) is None


def test_ability_badge_label_none_when_ability_has_no_badge_label(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Z.407: ability_badge_label returns None when the matched ability has no badge_label."""
    from gameObjects.loader import load_faction_abilities  # noqa: PLC0415

    abilities = load_faction_abilities("necrons")
    # Pick any necron ability that has no badge_label set (badge_label is None/empty).
    no_badge = next(
        (a for a in abilities if not a.badge_label),
        None,
    )
    assert no_badge is not None, "Need an ability without badge_label in necrons YAML"
    _eng.st.session_state = {
        "activated_abilities": {"Necrons": {"ability_id": no_badge.id}},
        "first_player": "Necrons",
        "p1_faction_dir": "necrons",
    }
    unit = _make_unit(rules=[], keywords=["NECRON"])
    assert ability_badge_label("Necrons", unit) is None


# ---------------------------------------------------------------------------
# get_after_attack_revive_ability / revive_dice_count — data-driven RP gate
# (INV-4b Option B: gate/label/threshold/dice formula come from faction YAML)
# ---------------------------------------------------------------------------


def _revive_session() -> _S:
    session = _S(
        first_player="Necrons",
        p1_faction_dir="necrons",
        p2_faction_dir="orks",
    )
    _st_mock.session_state = session
    return session


def test_revive_ability_found_for_unit_with_rp_rule() -> None:
    """Warriors-artige Einheit (reanimationProtocols) bekommt die YAML-Fähigkeit."""
    _revive_session()
    unit = _make_unit(rules=["reanimationProtocols"])
    ability = get_after_attack_revive_ability("Necrons", unit, {"destroyed": False})
    assert ability is not None
    assert ability.effect.type == "reanimate"
    assert ability.trigger.event == "after_enemy_attack"


def test_revive_ability_yaml_delivers_label_threshold_and_formula() -> None:
    """Label, 5+-Schwelle und Würfelformel kommen aus faction_abilities.yaml,
    nicht aus src/ (Option B, S128)."""
    _revive_session()
    unit = _make_unit(rules=["reanimationProtocols"])
    ability = get_after_attack_revive_ability("Necrons", unit, {"destroyed": False})
    assert ability is not None
    assert ability.name_en == "Reanimation Protocols"
    assert ability.effect.success_on == 5  # success threshold: 5+
    assert ability.effect.amount == "D6_per_wound"


def test_revive_ability_none_for_unit_without_rule() -> None:
    """Overlord-artige Einheit (kein reanimationProtocols) → kein Revive-Block."""
    _revive_session()
    unit = _make_unit(rules=["livingMetal"])
    assert get_after_attack_revive_ability("Necrons", unit, {"destroyed": False}) is None


def test_revive_ability_none_for_destroyed_unit() -> None:
    """9E: 'if any models were destroyed but this unit was NOT destroyed' —
    die YAML-Condition unit_not_destroyed blockt zerstörte Einheiten."""
    _revive_session()
    unit = _make_unit(rules=["reanimationProtocols"])
    assert get_after_attack_revive_ability("Necrons", unit, {"destroyed": True}) is None


def test_revive_ability_requires_after_enemy_attack_event() -> None:
    """Eine reanimate-Fähigkeit ohne trigger.event after_enemy_attack zählt nicht
    (z. B. künftige Command-Phase-Revives laufen über eigene Gates)."""
    from unittest.mock import patch

    _revive_session()
    wrong_event = Ability(
        id="test.revive.wrong_event",
        name_en="Wrong Event Revive",
        source="faction_rule",
        rule_text="",
        trigger=Trigger(timing="phase_start", phase="command", player="active", event=None),
        conditions=[],
        effect=Effect(type="reanimate", target="self"),
    )
    unit = _make_unit(rules=["reanimationProtocols"])
    with patch.object(_eng, "load_faction_abilities", return_value=[wrong_event]):
        assert get_after_attack_revive_ability("Necrons", unit, {"destroyed": False}) is None


def test_revive_ability_none_for_faction_without_revive_yaml() -> None:
    """Orks deklarieren keine reanimate-Fähigkeit → None (fraktionsblind)."""
    _revive_session()
    unit = _make_unit(rules=["reanimationProtocols"])
    assert get_after_attack_revive_ability("Orks", unit, {"destroyed": False}) is None


def test_revive_ability_none_for_unknown_player_slot() -> None:
    """Fehlende faction_dir im Session-State (KeyError) → None statt Crash."""
    _st_mock.session_state = _S(first_player="Necrons")
    unit = _make_unit(rules=["reanimationProtocols"])
    assert get_after_attack_revive_ability("Necrons", unit, {"destroyed": False}) is None


def test_revive_dice_count_d6_per_wound() -> None:
    """D6_per_wound: 4 gefallene 2-Wunden-Modelle → 8 Würfel (RP-Formel)."""
    assert revive_dice_count("D6_per_wound", 4, 2) == 8


def test_revive_dice_count_d6_per_wound_single_wound_models() -> None:
    assert revive_dice_count("D6_per_wound", 3, 1) == 3


def test_revive_dice_count_default_one_die_per_model() -> None:
    """Unbekannte/fehlende Formel → ein Würfel pro gefallenem Modell."""
    assert revive_dice_count(None, 4, 2) == 4
    assert revive_dice_count("other_formula", 5, 3) == 5


# ---------------------------------------------------------------------------
# get_unit_rp_reroll_ability — Their Number is Legion unit-ability gate
# (B-028c2, Class B: reads unit_abilities.yaml effect.type reroll_rp)
# ---------------------------------------------------------------------------


def test_rp_reroll_ability_found_for_unit_with_their_number_is_legion_rule() -> None:
    """Warrior-artige Einheit mit theirNumberIsLegion bekommt die YAML-Fähigkeit."""
    _revive_session()
    unit = _make_unit(rules=["reanimationProtocols", "theirNumberIsLegion"])
    ability = get_unit_rp_reroll_ability("Necrons", unit, {"destroyed": False})
    assert ability is not None
    assert ability.effect.type == "reroll_rp"
    assert ability.name_en == "Their Number is Legion"


def test_rp_reroll_ability_none_for_unit_without_rule() -> None:
    """Einheit ohne theirNumberIsLegion (z. B. reine RP-Einheit) → kein Reroll-Hinweis."""
    _revive_session()
    unit = _make_unit(rules=["reanimationProtocols"])
    assert get_unit_rp_reroll_ability("Necrons", unit, {"destroyed": False}) is None


def test_rp_reroll_ability_none_for_faction_without_unit_abilities_yaml() -> None:
    """Orks deklarieren keine theirNumberIsLegion-Fähigkeit → None (fraktionsblind)."""
    _revive_session()
    unit = _make_unit(rules=["theirNumberIsLegion"])
    assert get_unit_rp_reroll_ability("Orks", unit, {"destroyed": False}) is None


def test_rp_reroll_ability_none_for_unknown_player_slot() -> None:
    """Fehlende faction_dir im Session-State (KeyError) → None statt Crash."""
    _st_mock.session_state = _S(first_player="Necrons")
    unit = _make_unit(rules=["theirNumberIsLegion"])
    assert get_unit_rp_reroll_ability("Necrons", unit, {"destroyed": False}) is None


def test_rp_reroll_ability_coexists_with_active_rp_directive() -> None:
    """Koexistenz-Regression: get_active_rp_modifiers (Direktiv-Pfad) bleibt
    unberührt, während die Unit-Ability parallel gefunden wird — beide Quellen
    sind unabhängig (B-028c2)."""
    from unittest.mock import patch

    _revive_session()
    unit = _make_unit(rules=["reanimationProtocols", "theirNumberIsLegion"])

    with patch.object(
        _eng,
        "get_active_protocol_effects",
        return_value=[{"type": "rp_reroll"}],
    ):
        directive_result = get_active_rp_modifiers("Necrons")
        ability_result = get_unit_rp_reroll_ability("Necrons", unit, {"destroyed": False})

    assert directive_result == {"rp_reroll": True}
    assert ability_result is not None
    assert ability_result.effect.type == "reroll_rp"


# ---------------------------------------------------------------------------
# unit_hit_reroll_ones — Destroyer Cult "Hardwired for Destruction" gate
# (B-113 Teil A: reads subfaction_abilities.yaml effect.type reroll_hit,
# modifier==1, target=="self" — full-reroll reroll_hit auras are NOT matched)
# ---------------------------------------------------------------------------


def test_hit_reroll_ones_true_for_unit_with_hardwired_for_destruction_rule() -> None:
    """Skorpekh-artige Einheit mit hardwiredForDestruction bekommt den Hit-Reroll."""
    _revive_session()
    unit = _make_unit(rules=["livingMetal", "hardwiredForDestruction"])
    assert unit_hit_reroll_ones("Necrons", unit, {"destroyed": False}) is True


def test_hit_reroll_ones_false_for_unit_without_rule() -> None:
    """Einheit ohne hardwiredForDestruction (z. B. Warriors) → kein Hit-Reroll."""
    _revive_session()
    unit = _make_unit(rules=["livingMetal", "reanimationProtocols"])
    assert unit_hit_reroll_ones("Necrons", unit, {"destroyed": False}) is False


def test_hit_reroll_ones_false_for_faction_without_subfaction_abilities_yaml() -> None:
    """Orks deklarieren keine Destroyer-Cult-Fähigkeit → False (fraktionsblind)."""
    _revive_session()
    unit = _make_unit(rules=["hardwiredForDestruction"])
    assert unit_hit_reroll_ones("Orks", unit, {"destroyed": False}) is False


def test_hit_reroll_ones_false_for_unknown_player_slot() -> None:
    """Fehlende faction_dir im Session-State (KeyError) → False statt Crash."""
    _st_mock.session_state = _S(first_player="Necrons")
    unit = _make_unit(rules=["hardwiredForDestruction"])
    assert unit_hit_reroll_ones("Necrons", unit, {"destroyed": False}) is False


def test_hit_reroll_ones_true_for_real_skorpekh_destroyer_unit() -> None:
    """Integration: die echte Skorpekh-Destroyers-Datasheet trägt hardwiredForDestruction
    intrinsisch (units.yaml) — die Destroyer-Cult-Subfaction-Ability gated per
    has_rules darauf. Beweist die End-zu-Ende-Verdrahtung von YAML bis zum
    generischen Konsumenten (B-113 Teil A)."""
    _revive_session()
    units, _ = load_army("necrons")
    skorpekh = next(u for u in units if u.id == "wh40k_9e.necrons.unit.skorpekh_destroyers")
    assert unit_hit_reroll_ones("Necrons", skorpekh, {"destroyed": False}) is True


def test_hit_reroll_ones_true_for_real_skorpekh_lord() -> None:
    """Integration: die echte Skorpekh-Lord-Datasheet trägt hardwiredForDestruction
    intrinsisch (units.yaml) — die Destroyer-Cult-Subfaction-Ability gated per
    has_rules darauf. Beweist die End-zu-Ende-Verdrahtung von YAML bis zum
    generischen Konsumenten (B-129)."""
    _revive_session()
    units, _ = load_army("necrons")
    skorpekh_lord = next(u for u in units if u.id == "wh40k_9e.necrons.unit.skorpekh_lord")
    assert unit_hit_reroll_ones("Necrons", skorpekh_lord, {"destroyed": False}) is True


def test_hit_reroll_ones_ignores_full_reroll_shape_without_modifier(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """A ``reroll_hit`` effect without ``modifier == 1`` — the differently-shaped
    full-reroll aura (e.g. Silent King 'Phaeron of the Stars': "you can re-roll
    the hit roll", no modifier, target an aura label) — must NOT satisfy
    unit_hit_reroll_ones. Only the narrow 'reroll a hit roll of 1' shape
    (modifier==1, target=='self') does, preventing the wrong reroll semantics
    from being marked in the HIT block."""
    _revive_session()
    full_reroll_ability = Ability(
        id="test.full_reroll_hit",
        name_en="Full Reroll Hit (test)",
        source="subfaction_rule",
        rule_text="test",
        trigger=Trigger(timing="persistent", phase="any", player="active"),
        conditions=[Condition(has_rules=["hardwiredForDestruction"])],
        effect=Effect(type="reroll_hit", target="some_aura"),
    )
    monkeypatch.setattr(
        _eng, "load_subfaction_abilities", lambda faction_dir: [full_reroll_ability]
    )
    monkeypatch.setattr(_eng, "load_unit_abilities", lambda faction_dir: [])
    unit = _make_unit(rules=["hardwiredForDestruction"])
    assert unit_hit_reroll_ones("Necrons", unit, {"destroyed": False}) is False


# ---------------------------------------------------------------------------
# unit_wound_reroll_ones — Destroyer Cult Lord "United in Destruction" AURA
# (B-113 Teil B: reroll_wound_1 effect, target != "self" — one unit's ability
# affects OTHER friendly units in the same roster, gated on the aura source
# being alive and the target unit's own has_keywords condition)
# ---------------------------------------------------------------------------

_LOKHUST_LORD_ID = "wh40k_9e.necrons.unit.lokhust_lord"


def _destroyer_cult_unit() -> Unit:
    return _make_unit(rules=[], keywords=["DESTROYER CULT"])


def test_wound_reroll_ones_true_for_destroyer_cult_unit_when_lord_alive_in_roster() -> None:
    """Ein Destroyer-Cult-Ziel bekommt den Aura-Reroll, solange der Lokhust Lord
    lebend im selben Roster steht (kein räumliches Modell in dieser App —
    Lord-Präsenz genügt, analog rules_appendix.txt "Aura Abilities")."""
    session = _S(
        first_player="Necrons",
        p1_faction_dir="necrons",
        p1_units={_LOKHUST_LORD_ID: {"destroyed": False}},
    )
    _st_mock.session_state = session
    unit = _destroyer_cult_unit()
    assert unit_wound_reroll_ones("Necrons", unit, {"destroyed": False}) is True


def test_wound_reroll_ones_false_when_lord_not_in_roster() -> None:
    """Kein Lokhust/Skorpekh Lord im Roster → keine Aura-Quelle → False."""
    session = _S(
        first_player="Necrons",
        p1_faction_dir="necrons",
        p1_units={},
    )
    _st_mock.session_state = session
    unit = _destroyer_cult_unit()
    assert unit_wound_reroll_ones("Necrons", unit, {"destroyed": False}) is False


def test_wound_reroll_ones_false_when_lord_destroyed() -> None:
    """Der Lord steht zwar im Roster, ist aber zerstört → keine aktive Aura mehr."""
    session = _S(
        first_player="Necrons",
        p1_faction_dir="necrons",
        p1_units={_LOKHUST_LORD_ID: {"destroyed": True}},
    )
    _st_mock.session_state = session
    unit = _destroyer_cult_unit()
    assert unit_wound_reroll_ones("Necrons", unit, {"destroyed": False}) is False


def test_wound_reroll_ones_false_for_unit_without_destroyer_cult_keyword() -> None:
    """Warriors (kein DESTROYER CULT keyword) profitieren nicht von der Aura,
    selbst wenn ein Lord lebend im Roster steht."""
    session = _S(
        first_player="Necrons",
        p1_faction_dir="necrons",
        p1_units={_LOKHUST_LORD_ID: {"destroyed": False}},
    )
    _st_mock.session_state = session
    unit = _make_unit(rules=["reanimationProtocols"], keywords=["NECRONS", "CORE"])
    assert unit_wound_reroll_ones("Necrons", unit, {"destroyed": False}) is False


def test_wound_reroll_ones_matches_duplicate_roster_key_with_hash_suffix() -> None:
    """Eine zweite Kopie desselben Lords im Roster trägt den Schlüssel 'id#1'
    (gameState._make_unit_state_dict) — muss trotzdem als lebende Aura-Quelle
    erkannt werden (Präfix-Match, nicht exakter Key-Vergleich)."""
    session = _S(
        first_player="Necrons",
        p1_faction_dir="necrons",
        p1_units={f"{_LOKHUST_LORD_ID}#1": {"destroyed": False}},
    )
    _st_mock.session_state = session
    unit = _destroyer_cult_unit()
    assert unit_wound_reroll_ones("Necrons", unit, {"destroyed": False}) is True


def test_wound_reroll_ones_false_for_faction_without_units_state() -> None:
    """Fehlender units-Key im Session-State (z. B. leeres p1_units) → False,
    kein Crash."""
    session = _S(first_player="Necrons", p1_faction_dir="necrons")
    _st_mock.session_state = session
    unit = _destroyer_cult_unit()
    assert unit_wound_reroll_ones("Necrons", unit, {"destroyed": False}) is False


def test_wound_reroll_ones_true_for_real_skorpekh_lord_and_destroyers_roster() -> None:
    """Integration: die echten Datasheets (Skorpekh Lord 'United in Destruction'
    + Skorpekh Destroyers, beide DESTROYER CULT) — beweist die End-zu-Ende-
    Verdrahtung von unit_abilities.yaml bis zum generischen Konsumenten."""
    session = _S(
        first_player="Necrons",
        p1_faction_dir="necrons",
        p1_units={"wh40k_9e.necrons.unit.skorpekh_lord": {"destroyed": False}},
    )
    _st_mock.session_state = session
    units, _ = load_army("necrons")
    skorpekh = next(u for u in units if u.id == "wh40k_9e.necrons.unit.skorpekh_destroyers")
    assert unit_wound_reroll_ones("Necrons", skorpekh, {"destroyed": False}) is True


# ── mortal_wounds effect handler (B-028c1 T1) ───────────────────────────────
#
# Synthetic Ability fixtures mirror the four unit_abilities.yaml shapes
# (vengeance_of_the_enchained, infused_madness, arc_fields, wrath_of_the_seraptek)
# rather than loading real necron YAML — the generic dispatch logic under test
# does not depend on which unit/faction owns the ability, only on the effect's
# target/amount/roll_threshold/roll_type fields.


def _mortal_wounds_ability(
    *,
    target: str,
    amount: str | int,
    roll_threshold: int | None,
    roll_type: str | None = None,
) -> Ability:
    return Ability(
        id="test.unit.mortal_wounds_ability",
        name_en="Test Mortal Wounds Ability",
        source="unit_ability",
        rule_text="Test rule text.",
        trigger=Trigger(
            timing="phase_reactive", phase="any", player="either", event="model_destroyed"
        ),
        conditions=[],
        effect=Effect(
            type="mortal_wounds",
            target=target,
            amount=str(amount),
            roll_threshold=roll_threshold,
            roll_type=roll_type,
        ),
    )


class TestMortalWoundsTarget:
    def test_returns_known_target_unchanged(self) -> None:
        ability = _mortal_wounds_ability(target="units_within_2d6", amount="D6", roll_threshold=4)
        assert mortal_wounds_target(ability) == "units_within_2d6"

    def test_raises_for_unknown_target(self) -> None:
        ability = _mortal_wounds_ability(target="bogus_target", amount=1, roll_threshold=4)
        with pytest.raises(ValueError):
            mortal_wounds_target(ability)


class TestResolveMortalWoundsEffect:
    def test_vengeance_of_the_enchained_shape_triggers_and_rolls_amount(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """units_within_2d6, D6 amount, roll_threshold 4: gate roll 4+ then a D6 amount roll."""
        ability = _mortal_wounds_ability(target="units_within_2d6", amount="D6", roll_threshold=4)
        rolls = iter([4, 5])  # gate roll (4 >= 4 -> triggered), amount roll (D6 -> 5)
        monkeypatch.setattr(_eng, "parse_dice", lambda s: next(rolls))
        assert resolve_mortal_wounds_effect(ability) == 5

    def test_vengeance_of_the_enchained_shape_below_threshold_inflicts_nothing(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        ability = _mortal_wounds_ability(target="units_within_2d6", amount="D6", roll_threshold=4)
        monkeypatch.setattr(_eng, "parse_dice", lambda s: 3)  # gate roll 3 < 4
        assert resolve_mortal_wounds_effect(ability) == 0

    def test_infused_madness_shape_fixed_amount_one(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """closest_enemy_within_6, fixed amount 1, roll_threshold 4."""
        ability = _mortal_wounds_ability(
            target="closest_enemy_within_6", amount=1, roll_threshold=4
        )
        monkeypatch.setattr(_eng, "parse_dice", lambda s: 5 if s == "D6" else int(s))
        assert resolve_mortal_wounds_effect(ability) == 1

    def test_infused_madness_shape_threshold_exact_boundary_triggers(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """Boundary check: gate roll == threshold still triggers ('4+' means >= 4)."""
        ability = _mortal_wounds_ability(
            target="closest_enemy_within_6", amount=1, roll_threshold=4
        )
        monkeypatch.setattr(_eng, "parse_dice", lambda s: 4 if s == "D6" else int(s))
        assert resolve_mortal_wounds_effect(ability) == 1

    def test_arc_fields_shape_uses_externally_supplied_trigger_not_a_gate_roll(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """roll_type=unmodified_hit_1: no internal D6 gate roll, caller decides the trigger."""
        ability = _mortal_wounds_ability(
            target="attacker", amount=1, roll_threshold=1, roll_type="unmodified_hit_1"
        )
        calls: list[str] = []

        def fake_parse_dice(s: str) -> int:
            calls.append(s)
            return 1

        monkeypatch.setattr(_eng, "parse_dice", fake_parse_dice)
        assert resolve_mortal_wounds_effect(ability, trigger_met=True) == 1
        assert calls == ["1"]  # only the amount roll happened, no D6 gate roll

    def test_arc_fields_shape_untriggered_returns_zero_without_rolling_amount(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        ability = _mortal_wounds_ability(
            target="attacker", amount=1, roll_threshold=1, roll_type="unmodified_hit_1"
        )
        monkeypatch.setattr(
            _eng, "parse_dice", lambda s: pytest.fail("should not roll when untriggered")
        )
        assert resolve_mortal_wounds_effect(ability, trigger_met=False) == 0

    def test_arc_fields_shape_defaults_trigger_met_to_false(self) -> None:
        """Caller omitting trigger_met is treated as 'not triggered' (safe default)."""
        ability = _mortal_wounds_ability(
            target="attacker", amount=1, roll_threshold=1, roll_type="unmodified_hit_1"
        )
        assert resolve_mortal_wounds_effect(ability) == 0

    def test_wrath_of_the_seraptek_shape_d3_amount(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """enemy_units_within_1, D3 amount, roll_threshold 4."""
        ability = _mortal_wounds_ability(
            target="enemy_units_within_1", amount="D3", roll_threshold=4
        )
        rolls = iter([6, 2])  # gate roll 6 -> triggered, amount roll D3 -> 2
        monkeypatch.setattr(_eng, "parse_dice", lambda s: next(rolls))
        assert resolve_mortal_wounds_effect(ability) == 2

    def test_missing_roll_threshold_defaults_to_always_trigger(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """Defensive: malformed YAML without roll_threshold falls back to 0, so any D6
        result (always >= 0) triggers — documents the fallback rather than a silent no-op.
        """
        ability = _mortal_wounds_ability(
            target="units_within_2d6", amount="D6", roll_threshold=None
        )
        monkeypatch.setattr(_eng, "parse_dice", lambda s: 1)
        assert resolve_mortal_wounds_effect(ability) == 1


# ── explode effect handler (B-028c1 b1) ─────────────────────────────────────
#
# Engine rollback: unlike resolve_mortal_wounds_effect, resolve_explode_effect
# never calls parse_dice/random — both the gate roll and the per-target
# mortal-wound amount are rolled at the table and entered by the player
# ("App würfelt nicht"). Synthetic fixture mirrors the real explode shape
# (roll_threshold/radius/damage, no target/amount).


def _explode_ability(*, mandatory: bool = True) -> Ability:
    return Ability(
        id="test.unit.explode_ability",
        name_en="Test Explodes Ability",
        source="unit_ability",
        rule_text="Test rule text.",
        trigger=Trigger(
            timing="phase_reactive", phase="any", player="either", event="model_destroyed"
        ),
        conditions=[],
        effect=Effect(type="explode", roll_threshold=4, radius="2D6", damage="D6"),
        mandatory=mandatory,
    )


class TestResolveExplodeEffect:
    def test_exploded_true_returns_true_without_rolling(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        ability = _explode_ability()
        monkeypatch.setattr(
            _eng, "parse_dice", lambda s: pytest.fail("explode path must never roll dice")
        )
        assert resolve_explode_effect(ability, exploded=True) is True

    def test_exploded_false_returns_false_without_rolling(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        ability = _explode_ability()
        monkeypatch.setattr(
            _eng, "parse_dice", lambda s: pytest.fail("explode path must never roll dice")
        )
        assert resolve_explode_effect(ability, exploded=False) is False

    def test_raises_for_non_explode_ability(self) -> None:
        """Wiring guard: calling this on a mortal_wounds-type ability fails loudly
        instead of silently misapplying the gate."""
        ability = _mortal_wounds_ability(target="attacker", amount=1, roll_threshold=1)
        with pytest.raises(ValueError, match="explode"):
            resolve_explode_effect(ability, exploded=True)


# ── vengeance_of_the_enchained real-data wiring (B-028c1 b1) ───────────────
#
# Unlike the synthetic fixtures above (effect-shape only), these load the
# actual necrons/unit_abilities.yaml entry. As of B-028c1 b1 (S169) this
# ability's effect.type migrated from mortal_wounds to explode (Explodes
# family, Pflicht-Trigger, `mandatory: true`) — see the YAML comment on
# vengeance_of_the_enchained for the re-scope rationale (S165). The old
# find_unit_ability_by_effect(..., "mortal_wounds") lookup this ability used
# to satisfy therefore now returns None; that lookup path stays covered by
# the Arc Fields / Wrath of the Seraptek shape tests above (still
# mortal_wounds-typed, unaffected by this migration).


class TestVengeanceOfTheEnchainedRealData:
    def test_find_unit_ability_by_effect_real_data(self) -> None:
        ability = find_unit_ability_by_effect(
            "necrons", "wh40k_9e.necrons.unit.the_silent_king", "explode"
        )
        assert ability is not None
        assert ability.id == "wh40k_9e.necrons.unit.the_silent_king.vengeance_of_the_enchained"
        assert ability.effect.type == "explode"
        assert ability.trigger.event == "model_destroyed"
        assert ability.mandatory is True

    def test_explode_fields_real_data(self) -> None:
        ability = find_unit_ability_by_effect(
            "necrons", "wh40k_9e.necrons.unit.the_silent_king", "explode"
        )
        assert ability is not None
        assert ability.effect.roll_threshold == 4
        assert ability.effect.radius == "2D6"
        assert ability.effect.damage == "D6"

    def test_check_conditions_passes_for_the_silent_king(self) -> None:
        """Ownership (unit_id) is the ability's only gate (empty `conditions`,
        matching the sibling noctilith_beacons ability on the same unit) — a
        `has_rules` condition here was a data bug (S164 T2 finding): the
        referenced rules-tag in units.yaml is not on The Silent King at all,
        it is misattached to tesseract_vault elsewhere in the same file."""
        army, *_ = load_army("necrons")
        silent_king = next(u for u in army if u.id == "wh40k_9e.necrons.unit.the_silent_king")
        ability = find_unit_ability_by_effect("necrons", silent_king.id, "explode")
        assert ability is not None
        assert ability.conditions == []
        assert check_conditions(ability, silent_king, {"destroyed": True})

    def test_vengeance_flow_explode_gate_applies(self) -> None:
        """Real YAML shape (D6 gate 4+, radius 2D6", damage D6) — the gate outcome
        is supplied externally (table roll), never rolled by resolve_explode_effect."""
        ability = find_unit_ability_by_effect(
            "necrons", "wh40k_9e.necrons.unit.the_silent_king", "explode"
        )
        assert ability is not None
        assert resolve_explode_effect(ability, exploded=True) is True

    def test_vengeance_flow_does_not_explode(self) -> None:
        ability = find_unit_ability_by_effect(
            "necrons", "wh40k_9e.necrons.unit.the_silent_king", "explode"
        )
        assert ability is not None
        assert resolve_explode_effect(ability, exploded=False) is False

    def test_rule_text_includes_it_explodes(self) -> None:
        """Regression for the Wahapedia wording gap noted in backlog_details.md
        B-028c1: the previous rule_text dropped "it explodes" from the quote."""
        ability = find_unit_ability_by_effect(
            "necrons", "wh40k_9e.necrons.unit.the_silent_king", "explode"
        )
        assert ability is not None
        assert "it explodes" in ability.rule_text
