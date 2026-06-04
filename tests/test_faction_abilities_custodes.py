"""Tests for Custodes Ka'tah loading via the generic round_choice pipeline."""

from gameObjects.loader import (
    load_round_choice_abilities,
    load_round_choice_label,
)


class TestCustodesKatahLoading:
    def test_load_custodes_katah_returns_six(self) -> None:
        protocols = load_round_choice_abilities("adeptus_custodes")
        assert len(protocols) == 6

    def test_custodes_katah_no_auto_round_1(self) -> None:
        protocols = load_round_choice_abilities("adeptus_custodes")
        assert not any(p.auto_round_1 for p in protocols)

    def test_custodes_katah_first_is_calistus(self) -> None:
        protocols = load_round_choice_abilities("adeptus_custodes")
        assert protocols[0].name_en == "Calistus Ka'tah"

    def test_custodes_katah_all_have_primary_and_secondary(self) -> None:
        protocols = load_round_choice_abilities("adeptus_custodes")
        for p in protocols:
            assert p.primary, f"{p.name_en} missing primary"
            assert p.secondary, f"{p.name_en} missing secondary"

    def test_custodes_katah_all_have_primary_effect(self) -> None:
        protocols = load_round_choice_abilities("adeptus_custodes")
        for p in protocols:
            assert p.primary_effect, f"{p.name_en} missing primary_effect"

    def test_custodes_katah_all_have_secondary_effect(self) -> None:
        protocols = load_round_choice_abilities("adeptus_custodes")
        for p in protocols:
            assert p.secondary_effect, f"{p.name_en} missing secondary_effect"

    def test_custodes_katah_all_have_subfaction_affinity(self) -> None:
        protocols = load_round_choice_abilities("adeptus_custodes")
        for p in protocols:
            assert p.subfaction_affinity, f"{p.name_en} missing subfaction_affinity"

    def test_custodes_katah_affinities_are_unique(self) -> None:
        protocols = load_round_choice_abilities("adeptus_custodes")
        affinities = [p.subfaction_affinity for p in protocols]
        assert len(affinities) == len(set(affinities)), "Duplicate subfaction affinities"

    def test_custodes_katah_kaptaris_last(self) -> None:
        protocols = load_round_choice_abilities("adeptus_custodes")
        assert protocols[-1].name_en == "Kaptaris Ka'tah"

    def test_custodes_katah_id_namespace(self) -> None:
        protocols = load_round_choice_abilities("adeptus_custodes")
        for p in protocols:
            assert p.id.startswith("wh40k_9e.adeptus_custodes.faction.")

    def test_custodes_katah_rendax_primary_effect_type(self) -> None:
        protocols = load_round_choice_abilities("adeptus_custodes")
        rendax = next(p for p in protocols if "rendax" in p.id)
        assert rendax.primary_effect.get("type") == "extra_wound_on_6"

    def test_custodes_katah_dacatarai_secondary_attacks_modifier(self) -> None:
        protocols = load_round_choice_abilities("adeptus_custodes")
        dacatarai = next(p for p in protocols if "dacatarai" in p.id)
        assert dacatarai.secondary_effect.get("type") == "attacks_modifier"


class TestCustodesRoundChoiceLabel:
    def test_custodes_label_is_katah(self) -> None:
        label = load_round_choice_label("adeptus_custodes")
        assert "Ka'tah" in label

    def test_necrons_label_is_command_protocols(self) -> None:
        label = load_round_choice_label("necrons")
        assert label == "Command Protocols"

    def test_orks_label_fallback(self) -> None:
        label = load_round_choice_label("orks")
        assert label == "Round Abilities"


class TestCustodesSubfactionAffinityCorrectness:
    def test_rendax_affinity_is_emperors_chosen(self) -> None:
        protocols = load_round_choice_abilities("adeptus_custodes")
        rendax = next(p for p in protocols if "rendax" in p.id)
        assert rendax.subfaction_affinity == "emperors_chosen"

    def test_calistus_affinity_is_solar_watch(self) -> None:
        protocols = load_round_choice_abilities("adeptus_custodes")
        calistus = next(p for p in protocols if "calistus" in p.id)
        assert calistus.subfaction_affinity == "solar_watch"

    def test_conservai_affinity_is_emissaries_imperatus(self) -> None:
        protocols = load_round_choice_abilities("adeptus_custodes")
        conservai = next(p for p in protocols if "conservai" in p.id)
        assert conservai.subfaction_affinity == "emissaries_imperatus"

    def test_all_affinities_unique(self) -> None:
        protocols = load_round_choice_abilities("adeptus_custodes")
        affinities = [p.subfaction_affinity for p in protocols]
        assert len(affinities) == len(set(affinities))


class TestNecronSubfactionAffinity:
    def test_necrons_protocols_have_subfaction_affinity(self) -> None:
        protocols = load_round_choice_abilities("necrons")
        for p in protocols:
            assert p.subfaction_affinity is not None, f"{p.name_en} missing subfaction_affinity"

    def test_necrons_eternal_guardian_affinity_is_nihilakh(self) -> None:
        protocols = load_round_choice_abilities("necrons")
        eg = next(p for p in protocols if "eternal_guardian" in p.id)
        assert eg.subfaction_affinity == "nihilakh"

    def test_necrons_eternal_guardian_auto_round_1(self) -> None:
        protocols = load_round_choice_abilities("necrons")
        eg = next(p for p in protocols if "eternal_guardian" in p.id)
        assert eg.auto_round_1 is True

    def test_necrons_all_other_protocols_not_auto_round_1(self) -> None:
        protocols = load_round_choice_abilities("necrons")
        for p in protocols:
            if "eternal_guardian" not in p.id:
                assert not p.auto_round_1, f"{p.name_en} should not have auto_round_1"
