"""Tests for Ability dataclass and ability loaders."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

from gameObjects.ability import Ability, Condition, Effect, Trigger
from gameObjects.loader import (
    load_army,
    load_faction_abilities,
    load_unit_abilities,
    load_wargear_abilities,
)


def test_ability_dataclass_fields() -> None:
    ability = Ability(
        id="test.id",
        name_en="Test Ability",
        source="faction_rule",
        rule_text="Does something.",
        trigger=Trigger(timing="phase_start", phase="command"),
        conditions=[],
        effect=Effect(type="heal", target="self", amount="1"),
    )
    assert ability.id == "test.id"
    assert ability.source == "faction_rule"
    assert ability.trigger.timing == "phase_start"
    assert ability.trigger.phase == "command"
    assert ability.trigger.player == "active"
    assert ability.unit_id is None
    assert ability.ability_type == "triggered"


def test_ability_type_activated() -> None:
    ability = Ability(
        id="test.activated",
        name_en="Activated Ability",
        source="unit_ability",
        rule_text="Must be chosen.",
        trigger=Trigger(timing="activated", phase="command"),
        conditions=[],
        effect=Effect(type="buff_roll", target="friendly", modifier=1),
        ability_type="activated",
    )
    assert ability.ability_type == "activated"


def test_condition_defaults() -> None:
    cond = Condition()
    assert cond.has_rules is None
    assert cond.has_keywords is None
    assert cond.within_inches is None
    assert cond.max_uses is None
    assert cond.unit_not_destroyed is False


def test_load_faction_abilities_necrons_returns_at_least_seven() -> None:
    abilities = load_faction_abilities("necrons")
    assert len(abilities) >= 7


def test_living_metal_ability_parsed_correctly() -> None:
    abilities = load_faction_abilities("necrons")
    lm = next(a for a in abilities if a.id == "wh40k_9e.necrons.faction.living_metal")
    assert lm.name_en == "Living Metal"
    assert lm.source == "faction_rule"
    assert lm.trigger.timing == "phase_start"
    assert lm.trigger.phase == "command"
    assert lm.trigger.player == "active"
    assert len(lm.conditions) == 1
    assert lm.conditions[0].has_rules == ["livingMetal"]
    assert lm.effect.type == "heal"
    assert lm.effect.amount == "1"


def test_reanimation_protocols_reactive_trigger() -> None:
    abilities = load_faction_abilities("necrons")
    rp = next(a for a in abilities if a.id == "wh40k_9e.necrons.faction.reanimation_protocols")
    assert rp.trigger.timing == "phase_reactive"
    assert isinstance(rp.trigger.phase, list)
    assert "shooting" in rp.trigger.phase
    assert "fight" in rp.trigger.phase
    assert rp.trigger.player == "inactive"
    assert rp.trigger.event == "after_enemy_attack"


def test_load_faction_abilities_orks_returns_empty() -> None:
    abilities = load_faction_abilities("orks")
    assert abilities == []


def test_load_unit_abilities_necrons_returns_at_least_eight() -> None:
    abilities = load_unit_abilities("necrons")
    assert len(abilities) >= 8


def test_my_will_be_done_parsed() -> None:
    abilities = load_unit_abilities("necrons")
    mwbd = next(a for a in abilities if a.id == "wh40k_9e.necrons.unit.overlord.my_will_be_done")
    assert mwbd.name_en == "My Will Be Done"
    assert mwbd.source == "unit_ability"
    assert mwbd.unit_id == "wh40k_9e.necrons.unit.overlord"
    assert mwbd.trigger.phase == "command"
    assert mwbd.conditions[0].has_keywords == ["Core"]
    assert mwbd.effect.type == "buff_roll"
    assert mwbd.effect.modifier == 1


def test_resurrection_orb_wargear_source() -> None:
    abilities = load_wargear_abilities("necrons")
    orb = next(a for a in abilities if a.id == "wh40k_9e.necrons.wargear.resurrection_orb.ability")
    assert orb.source == "wargear"
    assert orb.wargear_id == "wh40k_9e.necrons.wargear.resurrection_orb"
    assert orb.conditions[0].max_uses == 1
    assert orb.effect.type == "complex"
    assert orb.effect.handler == "resurrectionOrb"


def test_overlord_has_rules_field_loaded() -> None:
    units, _ = load_army("necrons")
    overlord = next(u for u in units if u.id == "wh40k_9e.necrons.unit.overlord")
    assert "livingMetal" in overlord.rules
    assert "myWillBeDone" in overlord.rules


def test_warriors_rules_no_living_metal() -> None:
    units, _ = load_army("necrons")
    warriors = next(u for u in units if u.id == "wh40k_9e.necrons.unit.warriors")
    assert "livingMetal" not in warriors.rules
    assert "reanimationProtocols" in warriors.rules


def test_skorpekh_destroyers_has_living_metal_and_rp() -> None:
    units, _ = load_army("necrons")
    skorp = next(u for u in units if u.id == "wh40k_9e.necrons.unit.skorpekh_destroyers")
    assert "livingMetal" in skorp.rules
    assert "reanimationProtocols" in skorp.rules


def test_faction_abilities_have_ability_type() -> None:
    abilities = load_faction_abilities("necrons")
    for ability in abilities:
        assert ability.ability_type in (
            "triggered",
            "activated",
        ), f"{ability.id} has invalid ability_type: {ability.ability_type!r}"


def test_living_metal_is_triggered() -> None:
    abilities = load_faction_abilities("necrons")
    lm = next(a for a in abilities if a.id == "wh40k_9e.necrons.faction.living_metal")
    assert lm.ability_type == "triggered"


def test_reanimation_protocols_is_triggered() -> None:
    abilities = load_faction_abilities("necrons")
    rp = next(a for a in abilities if a.id == "wh40k_9e.necrons.faction.reanimation_protocols")
    assert rp.ability_type == "triggered"
