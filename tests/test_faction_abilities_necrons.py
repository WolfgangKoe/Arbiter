"""Tests for Necron Command Protocol loading and subfaction affinity correctness."""

from gameObjects.loader import load_round_choice_abilities, load_round_choice_label


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


class TestNecronAutoRound1:
    def test_eternal_guardian_has_auto_round_1(self) -> None:
        protocols = load_round_choice_abilities("necrons")
        eg = next(p for p in protocols if "eternal_guardian" in p.id)
        assert eg.auto_round_1 is True

    def test_other_protocols_do_not_have_auto_round_1(self) -> None:
        protocols = load_round_choice_abilities("necrons")
        for p in protocols:
            if "eternal_guardian" not in p.id:
                assert not p.auto_round_1, f"{p.name_en} should not have auto_round_1"


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
