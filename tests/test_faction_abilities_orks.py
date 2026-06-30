"""Tests for Orks faction ability data — WAAAGH!, ObjSec migration, powers."""

import sys
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from gameObjects.loader import load_faction_abilities, load_unit_abilities  # noqa: E402

_DATA_ROOT = Path(__file__).parent.parent / "data" / "wh40k_9e"


class TestOrksWaaagh:
    def test_waaagh_stage1_in_faction_abilities(self) -> None:
        abilities = load_faction_abilities("orks")
        ids = [a.id for a in abilities]
        assert "wh40k_9e.orks.faction.waaagh_stage1" in ids

    def test_speedwaaagh_in_faction_abilities(self) -> None:
        abilities = load_faction_abilities("orks")
        ids = [a.id for a in abilities]
        assert "wh40k_9e.orks.faction.speedwaaagh_stage1" in ids

    def test_ere_we_go_in_faction_abilities(self) -> None:
        abilities = load_faction_abilities("orks")
        ids = [a.id for a in abilities]
        assert "wh40k_9e.orks.faction.ere_we_go" in ids

    def test_waaagh_stage1_active_text_lists_buffs(self) -> None:
        abilities = load_faction_abilities("orks")
        waaagh_s1 = next(a for a in abilities if a.id == "wh40k_9e.orks.faction.waaagh_stage1")
        expected = "+1 Strength · +1 Attacks · 5+ invuln · Advance & Charge"
        assert waaagh_s1.active_text == expected

    def test_waaagh_stage2_active_text_lists_buffs(self) -> None:
        abilities = load_faction_abilities("orks")
        waaagh_s2 = next(a for a in abilities if a.id == "wh40k_9e.orks.faction.waaagh_stage2")
        expected = "+1 Strength · +1 Attacks · 6+ invuln"
        assert waaagh_s2.active_text == expected


class TestOrksObjectiveSecuredMigration:
    def test_objective_secured_not_in_faction_abilities(self) -> None:
        abilities = load_faction_abilities("orks")
        ids = [a.id for a in abilities]
        assert "wh40k_9e.orks.faction.objective_secured" not in ids

    def test_objective_secured_in_unit_abilities(self) -> None:
        abilities = load_unit_abilities("orks")
        ids = [a.id for a in abilities]
        assert "wh40k_9e.orks.unit.objective_secured" in ids

    def test_objective_secured_has_gretchin_exclusion(self) -> None:
        path = _DATA_ROOT / "orks" / "unit_abilities.yaml"
        with open(path) as f:
            data = yaml.safe_load(f)
        obj_sec = next(
            a for a in data["abilities"] if a["id"] == "wh40k_9e.orks.unit.objective_secured"
        )
        conditions = obj_sec.get("conditions", [])
        exclusions = [c.get("not_has_keywords") for c in conditions if "not_has_keywords" in c]
        assert any("GRETCHIN" in (e or []) for e in exclusions)

    def test_objective_secured_has_shared_ref(self) -> None:
        path = _DATA_ROOT / "orks" / "unit_abilities.yaml"
        with open(path) as f:
            data = yaml.safe_load(f)
        obj_sec = next(
            a for a in data["abilities"] if a["id"] == "wh40k_9e.orks.unit.objective_secured"
        )
        assert obj_sec.get("shared_ref") == "wh40k_9e.shared.objective_secured"


class TestOrksPsychicPowersMigration:
    def test_psychic_powers_not_in_faction_abilities(self) -> None:
        abilities = load_faction_abilities("orks")
        psychic_ids = [a.id for a in abilities if "psychic" in a.id]
        assert psychic_ids == [], f"Psychic abilities still in faction_abilities: {psychic_ids}"

    def test_powers_yaml_exists(self) -> None:
        path = _DATA_ROOT / "orks" / "powers.yaml"
        assert path.exists(), "orks/powers.yaml not found"

    def test_powers_yaml_contains_seven_powers(self) -> None:
        path = _DATA_ROOT / "orks" / "powers.yaml"
        with open(path) as f:
            data = yaml.safe_load(f)
        assert len(data["powers"]) == 7

    def test_smite_has_shared_ref(self) -> None:
        path = _DATA_ROOT / "orks" / "powers.yaml"
        with open(path) as f:
            data = yaml.safe_load(f)
        smite = next(p for p in data["powers"] if "smite" in p["id"])
        assert smite.get("shared_ref") == "wh40k_9e.shared.power.smite"

    def test_all_powers_have_power_type_psychic(self) -> None:
        path = _DATA_ROOT / "orks" / "powers.yaml"
        with open(path) as f:
            data = yaml.safe_load(f)
        for p in data["powers"]:
            assert p.get("power_type") == "psychic", f"{p['id']} missing power_type: psychic"
