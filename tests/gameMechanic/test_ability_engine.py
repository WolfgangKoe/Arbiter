"""Tests for gameMechanic/ability_engine.py."""

import sys
from pathlib import Path
from unittest.mock import MagicMock

_st_mock = MagicMock()
sys.modules["streamlit"] = _st_mock
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

import gameMechanic.ability_engine as _eng  # noqa: E402
from gameMechanic.ability_engine import (  # noqa: E402
    check_conditions,
    check_trigger,
    execute_effect,
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
    session = _S(necron_units={"test.unit": {"current_wounds": 4, "models": 2, "destroyed": False}})
    _eng.heal_unit.__module__  # ensure imported
    import gameMechanic.unit_mutations as _mut  # noqa: PLC0415

    _mut.st.session_state = session
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
    assert session["necron_units"]["test.unit"]["current_wounds"] == 5


def test_execute_effect_heal_no_revive_caps_at_living_models() -> None:
    """revive=False must not push wounds beyond current_models × wounds."""
    import gameMechanic.unit_mutations as _mut  # noqa: PLC0415

    # 1 model dead, 2 remaining at full HP: cannot be healed further
    session = _S(necron_units={"test.unit": {"current_wounds": 6, "models": 2, "destroyed": False}})
    _mut.st.session_state = session
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
    assert session["necron_units"]["test.unit"]["current_wounds"] == 6


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
    return {
        "active": "Necrons",
        "necron_units": {
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
    state = {
        "active": "Necrons",
        "necron_units": {
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


def test_get_triggered_abilities_ork_command_returns_empty() -> None:
    units, _ = load_army("orks")
    state = {
        "active": "Orks",
        "ork_units": {
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
