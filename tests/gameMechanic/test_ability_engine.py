"""Tests for gameMechanic/ability_engine.py."""

import sys
from pathlib import Path
from unittest.mock import MagicMock

import pytest

_st_mock = MagicMock()
sys.modules["streamlit"] = _st_mock
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

import gameMechanic.ability_engine as _eng  # noqa: E402
from gameMechanic.ability_engine import (  # noqa: E402
    _unit_matches_target,
    ability_badge_label,
    ability_invuln_save,
    buff_stat_bonus,
    charge_after_advance_allowed,
    check_conditions,
    check_trigger,
    execute_effect,
    get_activated_command_abilities,
    get_active_heal_bonus,
    get_active_round_choice_ap_on_wound_6,
    get_active_round_choice_ignores_cover_half_range,
    get_active_round_choice_light_cover_if_stationary,
    get_active_round_choice_modifier,
    get_active_round_choice_rerolls,
    get_active_round_choice_strength_if_charged,
    get_active_rp_modifiers,
    get_short_label_for_effect_type,
    get_triggered_abilities,
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
    import gameMechanic.unit_mutations as _mut  # noqa: PLC0415

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
    import gameMechanic.unit_mutations as _mut  # noqa: PLC0415

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
    import gameMechanic.unit_mutations as _mut  # noqa: PLC0415

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


def _protocol_session(protocol_id: str | None, directive: str | None) -> _S:
    # Round-choice runtime state is keyed by the player slot ("Necrons"), not the
    # faction directory — see round_choice_state_key (mirror-match safe).
    session = _S(
        first_player="Necrons",
        p1_faction_dir="necrons",
        p2_faction_dir="necrons",
    )
    session["round_choice_active_Necrons"] = protocol_id
    session["round_choice_directive_Necrons"] = directive
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


def test_protocol_modifier_conquering_tyrant_secondary_not_wired() -> None:
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


def test_leadership_bonus_wired() -> None:
    _protocol_session("wh40k_9e.necrons.faction.protocol_conquering_tyrant", "primary")
    result = get_active_round_choice_modifier("Necrons", "morale", False)
    assert result == {"leadership": 1}


def test_reroll_hit_wound_1_conquering_tyrant_s_melee() -> None:
    _protocol_session("wh40k_9e.necrons.faction.protocol_conquering_tyrant", "secondary")
    result = get_active_round_choice_rerolls("Necrons", "fight", True)
    assert result == {"reroll_hit_1", "reroll_wound_1"}


def test_reroll_hit_wound_skipped_in_shooting() -> None:
    _protocol_session("wh40k_9e.necrons.faction.protocol_conquering_tyrant", "secondary")
    assert get_active_round_choice_rerolls("Necrons", "shooting", False) == set()


def test_reroll_empty_when_no_directive() -> None:
    _protocol_session(None, None)
    assert get_active_round_choice_rerolls("Necrons", "shooting", False) == set()


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
