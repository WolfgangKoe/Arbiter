from pathlib import Path

import pytest

from standregeln.abhaken import abhaken, offeneZeilen
from standregeln.fortschritt import fortschrittSchreiben

planText = (
    "# Plan · Zyklus 1\n\n## Items\n1. [Stellen](../domaene/items/stellen.md)\n\n"
    "## Freigabe\nFreigabe: offen\nKommentar: .\n"
)


def schreiben(wurzel: Path, pfad: str, text: str) -> Path:
    datei = wurzel / pfad
    datei.parent.mkdir(parents=True, exist_ok=True)
    datei.write_text(text, encoding="utf-8")
    return datei


@pytest.fixture
def plan(tmp_path, gitRepo):
    datei = schreiben(tmp_path, "handoff/plan.md", planText)
    schreiben(tmp_path, "domaene/items/stellen.md", "# Stellen\n")
    gitRepo.festhalten("Freigabe Plan 1")
    return datei


def testDieRolleHaktIhrenSchrittAbUndSonstNichts(tmp_path, plan):
    assert abhaken(tmp_path, "Reviewer", "Kritik am Code") == ["Kritik am Code zu Item stellen"]
    text = plan.read_text(encoding="utf-8")
    assert "- [x] Reviewer: Kritik am Code zu Item stellen\n" in text
    assert "- [ ] Fachkritiker: Item stellen abgenommen\n" in text
    assert "- [ ] Reviewer: Review geschrieben\n" in text


def testEineFremdeZeileBleibtOffen(tmp_path, plan):
    assert abhaken(tmp_path, "Reviewer", "Item stellen abgenommen") == []
    assert "- [ ] Fachkritiker: Item stellen abgenommen\n" in plan.read_text(encoding="utf-8")


def testEinFaktHaktKeinBefehlAb(tmp_path, plan):
    assert abhaken(tmp_path, "Testautor", "Tests zu Item stellen") == []
    assert "- [ ] Testautor: Tests zu Item stellen\n" in plan.read_text(encoding="utf-8")


def testDerHakenBleibtBeimNächstenLauf(tmp_path, plan):
    abhaken(tmp_path, "Reviewer", "Kritik am Code")
    fortschrittSchreiben(tmp_path)
    assert "- [x] Reviewer: Kritik am Code zu Item stellen\n" in plan.read_text(encoding="utf-8")


@pytest.mark.usefixtures("plan")
def testDieRolleSiehtNurIhreOffenenSchritte(tmp_path):
    fortschrittSchreiben(tmp_path)
    assert "Kritik am Code zu Item stellen" in offeneZeilen(tmp_path, "reviewer")
    abhaken(tmp_path, "Reviewer", "Kritik am Code")
    assert "Kritik am Code zu Item stellen" not in offeneZeilen(tmp_path, "reviewer")
    assert "Item stellen abgenommen" not in offeneZeilen(tmp_path, "reviewer")
