"""Tests for Necron Command Protocol loading and subfaction affinity correctness."""

import sys
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from gameObjects.loader import (  # noqa: E402
    load_faction_abilities,
    load_round_choice_abilities,
    load_round_choice_label,
)

_FACTION_ABILITIES_PATH = "data/wh40k_9e/necrons/faction_abilities.yaml"


class TestNecronProtocolLoading:
    def test_load_necron_protocols_returns_six(self) -> None:
        protocols = load_round_choice_abilities("necrons")
        assert len(protocols) == 6

    def test_necron_label_is_command_protocols(self) -> None:
        label = load_round_choice_label("necrons")
        assert label == "Command Protocols"

    def test_necron_protocols_all_have_primary_and_secondary(self) -> None:
        protocols = load_round_choice_abilities("necrons")
        for p in protocols:
            assert p.primary, f"{p.name_en} missing primary"
            assert p.secondary, f"{p.name_en} missing secondary"

    def test_necron_protocols_all_have_effects(self) -> None:
        protocols = load_round_choice_abilities("necrons")
        for p in protocols:
            assert p.primary_effect, f"{p.name_en} missing primary_effect"
            assert p.secondary_effect, f"{p.name_en} missing secondary_effect"

    def test_necron_protocols_id_namespace(self) -> None:
        protocols = load_round_choice_abilities("necrons")
        for p in protocols:
            assert p.id.startswith("wh40k_9e.necrons.faction.protocol_")


class TestNecronSubfactionAffinities:
    def test_all_protocols_have_subfaction_affinity(self) -> None:
        protocols = load_round_choice_abilities("necrons")
        for p in protocols:
            assert p.subfaction_affinity, f"{p.name_en} missing subfaction_affinity"

    def test_affinities_are_unique(self) -> None:
        protocols = load_round_choice_abilities("necrons")
        affinities = [p.subfaction_affinity for p in protocols]
        assert len(affinities) == len(set(affinities)), "Duplicate subfaction affinities"

    def test_eternal_guardian_affinity_is_nihilakh(self) -> None:
        protocols = load_round_choice_abilities("necrons")
        p = next(x for x in protocols if "eternal_guardian" in x.id)
        assert p.subfaction_affinity == "nihilakh"

    def test_hungry_void_affinity_is_novokh(self) -> None:
        protocols = load_round_choice_abilities("necrons")
        p = next(x for x in protocols if "hungry_void" in x.id)
        assert p.subfaction_affinity == "novokh"

    def test_conquering_tyrant_affinity_is_sautekh(self) -> None:
        protocols = load_round_choice_abilities("necrons")
        p = next(x for x in protocols if "conquering_tyrant" in x.id)
        assert p.subfaction_affinity == "sautekh"

    def test_sudden_storm_affinity_is_nephrekh(self) -> None:
        protocols = load_round_choice_abilities("necrons")
        p = next(x for x in protocols if "sudden_storm" in x.id)
        assert p.subfaction_affinity == "nephrekh"

    def test_undying_legions_affinity_is_szarekhan(self) -> None:
        protocols = load_round_choice_abilities("necrons")
        p = next(x for x in protocols if "undying_legions" in x.id)
        assert p.subfaction_affinity == "szarekhan"

    def test_vengeful_stars_affinity_is_mephrit(self) -> None:
        protocols = load_round_choice_abilities("necrons")
        p = next(x for x in protocols if "vengeful_stars" in x.id)
        assert p.subfaction_affinity == "mephrit"


class TestNecronArkanaSchema:
    def _load_raw_arkana(self) -> list[dict]:
        with open(_FACTION_ABILITIES_PATH) as f:
            data = yaml.safe_load(f)
        return [a for a in data["abilities"] if a.get("category") == "arkana"]

    def test_all_arkana_have_rule_text(self) -> None:
        arkana = self._load_raw_arkana()
        for entry in arkana:
            suffix = entry["id"].split(".")[-1]
            assert entry.get("rule_text"), f"{suffix}: missing rule_text"
            assert "description" not in entry, f"{suffix}: legacy 'description' field still present"

    def test_all_arkana_have_trigger_and_effect(self) -> None:
        arkana = self._load_raw_arkana()
        for entry in arkana:
            suffix = entry["id"].split(".")[-1]
            assert "trigger" in entry, f"{suffix}: missing trigger"
            assert "effect" in entry, f"{suffix}: missing effect"

    def test_arkana_point_costs_match_wahapedia(self) -> None:
        expected = {
            "failsafe_overcharger": 25,
            "countertemporal_nanomines": 25,
            "atavindicator": 20,
            "dimensional_sanctum": 10,
            "hypermaterial_ablator": 20,
            "cortical_subjugator_scarabs": 10,
            "cryptogeometric_adjuster": 10,
            "metalodermal_tesla_weave": 15,
            "photonic_transubjector": 15,
            "phylacterine_hive": 15,
            "prismatic_obfuscatron": 15,
            "quantum_orb": 15,
        }
        arkana = self._load_raw_arkana()
        actual = {a["id"].split(".")[-1]: a.get("cost_pts") for a in arkana}
        for key, pts in expected.items():
            assert actual.get(key) == pts, f"{key}: expected {pts}pts, got {actual.get(key)}"

    def test_descriptive_arkana_not_dispatched(self) -> None:
        abilities = load_faction_abilities("necrons")
        descriptive_ids = [a.id for a in abilities if a.ability_type == "descriptive"]
        assert (
            descriptive_ids == []
        ), f"descriptive entries leaked into dispatcher: {descriptive_ids}"
        activated_ids = [a.id for a in abilities if "failsafe_overcharger" in a.id]
        assert (
            activated_ids
        ), "failsafe_overcharger (activated) must be present in load_faction_abilities result"
