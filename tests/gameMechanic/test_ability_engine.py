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
    get_active_round_choice_modifier,
    get_active_round_choice_rerolls,
    get_active_rp_modifiers,
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
    """Undying Legions S (+1 wound per Living Metal use) lifts the heal amount."""
    import gameMechanic.unit_mutations as _mut  # noqa: PLC0415

    session = _S(
        first_player="Necrons",
        p1_faction_dir="necrons",
        p2_faction_dir="necrons",
        p1_units={"test.unit": {"current_wounds": 3, "models": 2, "destroyed": False}},
    )
    session["round_choice_active_necrons"] = "wh40k_9e.necrons.faction.protocol_undying_legions"
    session["round_choice_directive_necrons"] = "secondary"
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
    session = _S(
        first_player="Necrons",
        p1_faction_dir="necrons",
        p2_faction_dir="necrons",
    )
    session["round_choice_active_necrons"] = protocol_id
    session["round_choice_directive_necrons"] = directive
    _st_mock.session_state = session
    return session


def test_protocol_modifier_no_active_protocol_returns_empty() -> None:
    _protocol_session(None, None)
    assert get_active_round_choice_modifier("necrons", "shooting", False) == {}


def test_protocol_modifier_no_directive_returns_empty() -> None:
    _protocol_session("wh40k_9e.necrons.faction.protocol_hungry_void", None)
    assert get_active_round_choice_modifier("necrons", "shooting", False) == {}


def test_protocol_modifier_hungry_void_primary_hit_in_shooting() -> None:
    _protocol_session("wh40k_9e.necrons.faction.protocol_hungry_void", "primary")
    result = get_active_round_choice_modifier("necrons", "shooting", False)
    assert result == {"hit": 1}


def test_protocol_modifier_hungry_void_primary_no_effect_in_melee() -> None:
    _protocol_session("wh40k_9e.necrons.faction.protocol_hungry_void", "primary")
    result = get_active_round_choice_modifier("necrons", "fight", True)
    assert result == {}


def test_protocol_modifier_vengeful_stars_primary_wound_in_shooting() -> None:
    _protocol_session("wh40k_9e.necrons.faction.protocol_vengeful_stars", "primary")
    result = get_active_round_choice_modifier("necrons", "shooting", False)
    assert result == {"wound": 1}


def test_protocol_modifier_eternal_guardian_primary_save_any_phase() -> None:
    _protocol_session("wh40k_9e.necrons.faction.protocol_eternal_guardian", "primary")
    result = get_active_round_choice_modifier("necrons", "shooting", False)
    assert result == {"save": 1}
    result_melee = get_active_round_choice_modifier("necrons", "fight", True)
    assert result_melee == {"save": 1}


def test_protocol_modifier_conquering_tyrant_secondary_not_wired() -> None:
    _protocol_session("wh40k_9e.necrons.faction.protocol_conquering_tyrant", "secondary")
    result = get_active_round_choice_modifier("necrons", "fight", True)
    assert result == {}


def test_strength_modifier_wired_in_shooting() -> None:
    _protocol_session("wh40k_9e.necrons.faction.protocol_hungry_void", "secondary")
    result = get_active_round_choice_modifier("necrons", "shooting", False)
    assert result == {"strength": 1}


def test_strength_modifier_skipped_in_melee() -> None:
    _protocol_session("wh40k_9e.necrons.faction.protocol_hungry_void", "secondary")
    result = get_active_round_choice_modifier("necrons", "fight", True)
    assert result == {}


def test_strength_modifier_inactive_returns_empty() -> None:
    _protocol_session(None, None)
    assert get_active_round_choice_modifier("necrons", "shooting", False) == {}


def test_ap_bonus_wired_shooting() -> None:
    _protocol_session("wh40k_9e.necrons.faction.protocol_vengeful_stars", "secondary")
    result = get_active_round_choice_modifier("necrons", "shooting", False)
    assert result == {"ap": -1}


def test_ap_bonus_skipped_in_melee() -> None:
    _protocol_session("wh40k_9e.necrons.faction.protocol_vengeful_stars", "secondary")
    result = get_active_round_choice_modifier("necrons", "fight", True)
    assert result == {}


def test_move_bonus_wired_movement() -> None:
    _protocol_session("wh40k_9e.necrons.faction.protocol_sudden_storm", "primary")
    result = get_active_round_choice_modifier("necrons", "movement", False)
    assert result == {"move": 1}


def test_leadership_bonus_wired() -> None:
    _protocol_session("wh40k_9e.necrons.faction.protocol_conquering_tyrant", "primary")
    result = get_active_round_choice_modifier("necrons", "morale", False)
    assert result == {"leadership": 1}


def test_reroll_save_1_eternal_guardian_s() -> None:
    _protocol_session("wh40k_9e.necrons.faction.protocol_eternal_guardian", "secondary")
    assert get_active_round_choice_rerolls("necrons", "shooting", False) == {"reroll_save_1"}


def test_reroll_hit_wound_1_conquering_tyrant_s_melee() -> None:
    _protocol_session("wh40k_9e.necrons.faction.protocol_conquering_tyrant", "secondary")
    result = get_active_round_choice_rerolls("necrons", "fight", True)
    assert result == {"reroll_hit_1", "reroll_wound_1"}


def test_reroll_hit_wound_skipped_in_shooting() -> None:
    _protocol_session("wh40k_9e.necrons.faction.protocol_conquering_tyrant", "secondary")
    assert get_active_round_choice_rerolls("necrons", "shooting", False) == set()


def test_reroll_empty_when_no_directive() -> None:
    _protocol_session(None, None)
    assert get_active_round_choice_rerolls("necrons", "shooting", False) == set()


def test_advance_and_charge_via_directive() -> None:
    _protocol_session("wh40k_9e.necrons.faction.protocol_sudden_storm", "secondary")
    unit = _make_unit(rules=[], keywords=["NECRON"])
    assert charge_after_advance_allowed("Necrons", unit) is True


def test_advance_and_charge_inactive_returns_false() -> None:
    _protocol_session(None, None)
    unit = _make_unit(rules=[], keywords=["NECRON"])
    assert charge_after_advance_allowed("Necrons", unit) is False


def test_rp_reroll_undying_legions_p() -> None:
    _protocol_session("wh40k_9e.necrons.faction.protocol_undying_legions", "primary")
    assert get_active_rp_modifiers("necrons") == {"rp_reroll": True}


def test_rp_modifiers_empty_for_undying_legions_secondary() -> None:
    # Secondary is a Living-Metal heal_bonus per RAW, NOT a Reanimation-pool
    # effect — get_active_rp_modifiers must not surface it (S89 data fix).
    _protocol_session("wh40k_9e.necrons.faction.protocol_undying_legions", "secondary")
    assert get_active_rp_modifiers("necrons") == {}


def test_rp_modifier_empty_when_other_directive() -> None:
    _protocol_session("wh40k_9e.necrons.faction.protocol_hungry_void", "primary")
    assert get_active_rp_modifiers("necrons") == {}


def test_heal_bonus_undying_legions_secondary_applies_to_living_metal() -> None:
    _protocol_session("wh40k_9e.necrons.faction.protocol_undying_legions", "secondary")
    unit = _make_unit(rules=["livingMetal"])
    assert get_active_heal_bonus("necrons", unit) == 1


def test_heal_bonus_zero_when_unit_lacks_target_rule() -> None:
    _protocol_session("wh40k_9e.necrons.faction.protocol_undying_legions", "secondary")
    unit = _make_unit(rules=[])  # no livingMetal -> directive does not match
    assert get_active_heal_bonus("necrons", unit) == 0


def test_heal_bonus_zero_for_reroll_directive() -> None:
    _protocol_session("wh40k_9e.necrons.faction.protocol_undying_legions", "primary")
    unit = _make_unit(rules=["livingMetal"])
    assert get_active_heal_bonus("necrons", unit) == 0


def test_heal_bonus_zero_when_no_directive() -> None:
    _protocol_session(None, None)
    unit = _make_unit(rules=["livingMetal"])
    assert get_active_heal_bonus("necrons", unit) == 0


def test_protocol_modifier_ork_faction_no_protocols_returns_empty() -> None:
    _protocol_session("wh40k_9e.necrons.faction.protocol_hungry_void", "primary")
    result = get_active_round_choice_modifier("orks", "shooting", False)
    assert result == {}


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
