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


def test_load_faction_abilities_necrons_returns_triggered_abilities_only() -> None:
    # round_choice entries (6 Protocols) are excluded — loaded via load_round_choice_abilities()
    # Only triggered faction-wide rules remain: Living Metal + Reanimation Protocols
    abilities = load_faction_abilities("necrons")
    assert len(abilities) >= 2
    assert all(a.ability_type != "round_choice" for a in abilities)


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


def test_load_faction_abilities_orks_returns_abilities() -> None:
    abilities = load_faction_abilities("orks")
    ids = [a.id for a in abilities]
    # 'Ere We Go and WAAAGH! are true faction-wide abilities
    assert "wh40k_9e.orks.faction.ere_we_go" in ids
    assert "wh40k_9e.orks.faction.waaagh_stage1" in ids
    # mob_rule/ramshackle/beast_snagga moved to unit_abilities.yaml (keyword-gated)
    assert "wh40k_9e.orks.faction.mob_rule" not in ids


def test_load_unit_abilities_orks_has_mob_rule_and_ramshackle() -> None:
    from gameObjects.loader import load_unit_abilities

    abilities = load_unit_abilities("orks")
    ids = [a.id for a in abilities]
    assert "wh40k_9e.orks.unit.mob_rule" in ids
    assert "wh40k_9e.orks.unit.ramshackle" in ids
    assert "wh40k_9e.orks.unit.beast_snagga" in ids


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
    assert mwbd.conditions[0].has_keywords == ["CORE"]
    assert mwbd.effect.type == "buff_roll"
    assert mwbd.effect.modifier == 1


def test_resurrection_orb_wargear_source() -> None:
    abilities = load_wargear_abilities("necrons")
    orb = next(a for a in abilities if a.id == "wh40k_9e.necrons.wargear.resurrection_orb.ability")
    assert orb.source == "wargear"
    assert orb.wargear_id == "wh40k_9e.necrons.wargear.resurrection_orb"
    # Schema unified (Plan 020): once_per_battle replaces the old max_uses: 1
    assert orb.conditions[0].once_per_battle is True
    assert orb.conditions[0].max_uses is None
    assert orb.effect.type == "complex"
    assert orb.effect.handler == "resurrectionOrb"


class _KeywordUnit:
    def __init__(self, keywords: list[str]) -> None:
        self._keywords = keywords

    def has_keyword(self, keyword: str) -> bool:
        return keyword in self._keywords


def test_mwbd_extra_uses_loaded_from_yaml() -> None:
    abilities = load_unit_abilities("necrons")
    mwbd = next(
        a for a in abilities if a.name_en == "My Will Be Done" and "overlord" in (a.unit_id or "")
    )
    assert [(e.has_keyword, e.bonus) for e in mwbd.extra_uses] == [("PHAERON", 1)]


def test_bonus_uses_for_grants_keyword_bonus() -> None:
    abilities = load_unit_abilities("necrons")
    mwbd = next(a for a in abilities if a.name_en == "My Will Be Done")
    assert mwbd.bonus_uses_for(_KeywordUnit(["PHAERON"])) == 1
    assert mwbd.bonus_uses_for(_KeywordUnit(["INFANTRY"])) == 0
    assert mwbd.bonus_uses_for(None) == 0


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


def test_reanimation_protocols_yaml_declares_ui_config() -> None:
    """Option B (S128): das YAML liefert Gate-Event, Label, Würfelformel und
    5+-Schwelle für den RP-Block — src/ kennt nur die generische Effekt-Form.
    Tippfehler hier würden das RP-Gate still brechen (Regressionsschutz)."""
    abilities = load_faction_abilities("necrons")
    rp = next(a for a in abilities if a.effect.type == "reanimate")
    assert rp.id == "wh40k_9e.necrons.faction.reanimation_protocols"
    assert rp.name_en == "Reanimation Protocols"
    assert rp.trigger.event == "after_enemy_attack"
    assert rp.conditions and rp.conditions[0].has_rules == ["reanimationProtocols"]
    assert rp.conditions[0].unit_not_destroyed is True
    assert rp.effect.amount == "D6_per_wound"
    assert rp.effect.success_on == 5  # success threshold (5+)
