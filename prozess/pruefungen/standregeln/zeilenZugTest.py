from pathlib import Path

import pytest

from anliegenregeln.anliegen import kopfVerstöße
from lesen.anliegenKopf import kopfLesen
from standregeln.fortschritt import fortschrittSchreiben
from standregeln.zeilenZug import zeilenzugÜbernehmen

planText = (
    "# Plan · Zyklus 1\n\n## Items\n1. [Stellen](../domaene/items/stellen.md)\n\n"
    "## Freigabe\nFreigabe: offen\nKommentar: .\n"
)
zeile = "Implementierer: Tests zu Item stellen grün"
faktZeile = "Reviewer: Review geschrieben"
stakeholderZeile = "Stakeholder: Freigabe Review 1"


def schreiben(wurzel: Path, pfad: str, text: str) -> Path:
    datei = wurzel / pfad
    datei.parent.mkdir(parents=True, exist_ok=True)
    datei.write_text(text, encoding="utf-8")
    return datei


@pytest.fixture
def plan(tmp_path, gitRepo):
    datei = schreiben(tmp_path, "handoff/plan.md", planText)
    schreiben(tmp_path, "domaene/items/stellen.md", "# Stellen\n")
    for rolle in ("implementierer", "planer"):
        schreiben(tmp_path, f".claude/agents/{rolle}.md", f"---\nname: {rolle}\n---\n")
    gitRepo.festhalten("Freigabe Plan 1")
    fortschrittSchreiben(tmp_path)
    return datei


def testDerHakenDesStakeholdersSetztDieZeileUndNimmtSieNieWieder(tmp_path, plan):
    assert zeilenzugÜbernehmen(tmp_path, zeile, "haken", "x") is None
    assert f"- [x] {zeile}\n" in plan.read_text(encoding="utf-8")
    assert zeilenzugÜbernehmen(tmp_path, zeile, "haken", "") is None
    assert f"- [x] {zeile}\n" in plan.read_text(encoding="utf-8")


def testDerHakenAufEineZeileMitFaktWirdAbgewiesen(tmp_path, plan):
    vorher = plan.read_text(encoding="utf-8")
    assert zeilenzugÜbernehmen(tmp_path, faktZeile, "haken", "x")
    assert plan.read_text(encoding="utf-8") == vorher


def testEinKommentarLegtEinAnliegenAnDieRolleUndEineZeileAn(tmp_path, plan):
    assert zeilenzugÜbernehmen(tmp_path, zeile, "kommentarZeile", "Bitte  prüfen.") is None
    assert f"- [ ] {zeile}\n  Kommentar: Bitte prüfen. (Anliegen 1)\n" in plan.read_text(
        encoding="utf-8"
    )
    (datei,) = (tmp_path / "handoff/anliegen").glob("*.md")
    gelesen = kopfLesen(datei)
    beteiligte = (gelesen.typ, gelesen.absender, gelesen.empfänger, gelesen.status)
    assert beteiligte == ("Kritik", "Stakeholder", "Implementierer", "offen")
    assert kopfVerstöße(datei, tmp_path) == []
    assert "Bitte prüfen." in datei.read_text(encoding="utf-8")


def testDerKommentarBleibtBeimNeuschreibenDesFortschritts(tmp_path, plan):
    zeilenzugÜbernehmen(tmp_path, zeile, "kommentarZeile", "Bitte prüfen.")
    fortschrittSchreiben(tmp_path)
    assert "Kommentar: Bitte prüfen. (Anliegen 1)" in plan.read_text(encoding="utf-8")


def testEinLeererKommentarOderEineFremdeZeileLegtNichtsAn(tmp_path, plan):
    vorher = plan.read_text(encoding="utf-8")
    assert zeilenzugÜbernehmen(tmp_path, zeile, "kommentarZeile", "  ")
    assert zeilenzugÜbernehmen(tmp_path, "Reviewer: gibtEsNicht", "haken", "x")
    assert zeilenzugÜbernehmen(tmp_path, "Stakeholder: Freigabe Plan 1", "kommentarZeile", "Text")
    assert plan.read_text(encoding="utf-8") == vorher
    assert list((tmp_path / "handoff").glob("anliegen/*.md")) == []
