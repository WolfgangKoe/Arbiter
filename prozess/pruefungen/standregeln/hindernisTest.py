from pathlib import Path

import pytest

from anliegenregeln.anliegen import kopfVerstöße
from lesen.anliegenKopf import kopfLesen
from standregeln.fortschritt import fortschrittSchreiben
from standregeln.hindernis import dateiname, hindernisMelden

planText = (
    "# Plan · Zyklus 1\n\n## Items\n1. [Stellen](../domaene/items/stellen.md)\n\n"
    "## Freigabe\nFreigabe: offen\nKommentar: .\n"
)
hindernis = "Pfad gesperrt."
nummerNachDerGelöschten = 41


def schreiben(wurzel: Path, pfad: str, text: str) -> Path:
    datei = wurzel / pfad
    datei.parent.mkdir(parents=True, exist_ok=True)
    datei.write_text(text, encoding="utf-8")
    return datei


@pytest.fixture
def plan(tmp_path, gitRepo):
    datei = schreiben(tmp_path, "handoff/plan.md", planText)
    schreiben(tmp_path, "domaene/items/stellen.md", "# Stellen\n")
    for rolle in ("implementierer", "planer", "regelumsetzer"):
        schreiben(tmp_path, f".claude/agents/{rolle}.md", f"---\nname: {rolle}\n---\n")
    gitRepo.festhalten("Freigabe Plan 1")
    return datei


def anliegenDateien(wurzel: Path) -> list[Path]:
    return sorted((wurzel / "handoff/anliegen").glob("*.md"))


def testEinHindernisLegtAnliegenUndZeileAn(tmp_path, plan):
    nummer = hindernisMelden(tmp_path, "Implementierer", "grün", "Planer", hindernis)
    assert nummer == 1
    zeile = "- [ ] Implementierer: Tests zu Item stellen grün\n"
    assert f"{zeile}  Hindernis: {hindernis} (Anliegen 1)\n" in plan.read_text(encoding="utf-8")
    (datei,) = anliegenDateien(tmp_path)
    gelesen = kopfLesen(datei)
    beteiligte = (gelesen.typ, gelesen.absender, gelesen.empfänger)
    assert beteiligte == ("Kritik", "Implementierer", "Planer")
    assert kopfVerstöße(datei, tmp_path) == []
    assert hindernis in datei.read_text(encoding="utf-8")


def testEinHindernisAnDenStakeholderIstEineFrageMitAntwort(tmp_path, plan):
    hindernisMelden(tmp_path, "Implementierer", "grün", "stakeholder", hindernis)
    (datei,) = anliegenDateien(tmp_path)
    assert kopfLesen(datei).typ == "Fragen"
    assert "**F1 · " in datei.read_text(encoding="utf-8")
    assert "Antwort: .\n" in datei.read_text(encoding="utf-8")
    assert plan.read_text(encoding="utf-8").count("Hindernis:") == 1


@pytest.mark.usefixtures("plan")
def testDieNummerIstGrößerAlsJedeVorhandeneUndGelöschte(tmp_path, gitRepo):
    schreiben(tmp_path, "handoff/anliegen/40-alt.md", "x\n")
    gitRepo.festhalten("alt")
    (tmp_path / "handoff/anliegen/40-alt.md").unlink()
    gitRepo.festhalten("alt gelöscht")
    schreiben(tmp_path, "handoff/anliegen/07-neu.md", "x\n")
    nummer = hindernisMelden(tmp_path, "Implementierer", "grün", "Planer", hindernis)
    assert nummer == nummerNachDerGelöschten


def testEineFremdeOderUnbekannteZeileMeldetNichts(tmp_path, plan):
    assert hindernisMelden(tmp_path, "Reviewer", "abgenommen", "Planer", hindernis) is None
    assert hindernisMelden(tmp_path, "Implementierer", "grün", "Niemand", hindernis) is None
    assert hindernisMelden(tmp_path, "Implementierer", "gibtEsNicht", "Planer", hindernis) is None
    assert anliegenDateien(tmp_path) == []
    assert "Hindernis:" not in plan.read_text(encoding="utf-8")


def testDasHindernisBleibtBeimNeuschreibenUndBekommtDenBeseitigendenCommit(
    tmp_path, gitRepo, plan
):
    hindernisMelden(tmp_path, "Implementierer", "grün", "Planer", hindernis)
    gitRepo.festhalten("Hindernis gemeldet")
    fortschrittSchreiben(tmp_path)
    assert "beseitigt" not in plan.read_text(encoding="utf-8")
    (datei,) = anliegenDateien(tmp_path)
    datei.write_text(
        datei.read_text(encoding="utf-8").replace("Runde 1/3 · offen", "Runde 1/3 · angenommen"),
        encoding="utf-8",
    )
    fortschrittSchreiben(tmp_path)
    assert "beseitigt" not in plan.read_text(encoding="utf-8")
    gitRepo.festhalten("Pfad freigegeben")
    fortschrittSchreiben(tmp_path)
    zeile = f"  Hindernis: {hindernis} (Anliegen 1); beseitigt: Commit „Pfad freigegeben“\n"
    assert zeile in plan.read_text(encoding="utf-8")
    assert fortschrittSchreiben(tmp_path) is None


def testEinGelöschtesErledigtesAnliegenBeseitigtMitDemCommitDavor(tmp_path, gitRepo, plan):
    hindernisMelden(tmp_path, "Implementierer", "grün", "Planer", hindernis)
    (datei,) = anliegenDateien(tmp_path)
    datei.write_text(
        datei.read_text(encoding="utf-8").replace("Runde 1/3 · offen", "Runde 1/3 · erledigt"),
        encoding="utf-8",
    )
    gitRepo.festhalten("Pfad freigegeben")
    datei.unlink()
    gitRepo.festhalten("Anliegen gelöscht")
    fortschrittSchreiben(tmp_path)
    assert "beseitigt: Commit „Pfad freigegeben“" in plan.read_text(encoding="utf-8")


def testDerDateinameIstAsciiUndCamelCase():
    assert dateiname(5, "Tests zu Item stellen grün") == "05-hindernisTestsZuItemStellenGruen.md"
