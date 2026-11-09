from pathlib import Path

import pytest

from standregeln.abhaken import abhaken, bereitsAbgehakt, hauptprogramm, offeneZeilen
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
    schreiben(tmp_path, "domaene/items/stellen.md", "# Stellen\n\nUmfang: AUF-1.1\n")
    anforderung = "### AUF-1 Stellen\n\n- AUF-1.1 Ein Modell.\n"
    schreiben(tmp_path, "domaene/anforderungen/auf.md", anforderung)
    gitRepo.festhalten("Freigabe Plan 1")
    return datei


def testDieRolleHaktIhrenSchrittAbUndSonstNichts(tmp_path, plan):
    assert abhaken(tmp_path, "Reviewer", "Kritik am Code") == ["Kritik am Code zu Item stellen"]
    text = plan.read_text(encoding="utf-8")
    assert "- [x] Reviewer: Kritik am Code zu Item stellen\n" in text
    assert "- [ ] Fachkritiker: Item stellen abgenommen\n" in text
    assert "- [ ] Reviewer: Review geschrieben\n" in text


def testEinSchonGesetzterHakenWirdAlsSolcherGemeldetUndNichtNochmalAbgehakt(
    tmp_path, plan, monkeypatch, capsys
):
    monkeypatch.setenv("CLAUDE_PROJECT_DIR", str(tmp_path))
    assert hauptprogramm(["Reviewer", "Kritik am Code"]) == 0
    assert capsys.readouterr().out.startswith("Abgehakt: ")
    assert abhaken(tmp_path, "Reviewer", "Kritik am Code") == []
    assert bereitsAbgehakt(tmp_path, "Reviewer", "Kritik am Code") == [
        "Kritik am Code zu Item stellen"
    ]
    assert hauptprogramm(["Reviewer", "Kritik am Code"]) == 0
    assert capsys.readouterr().out.startswith("Schon abgehakt")
    assert "- [x] Reviewer: Kritik am Code zu Item stellen\n" in plan.read_text(encoding="utf-8")


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


def akzeptanztestAnlegen(wurzel: Path, rumpf: str) -> None:
    schreiben(wurzel, ".claude/agents/testautor.md", "---\nname: testautor\n---\n")
    inhalt = f"def testAuf1_1EinModell():\n    {rumpf}\n"
    schreiben(wurzel, "technik/tests/akzeptanz/aufTest.py", inhalt)


@pytest.mark.usefixtures("plan")
def testEinGrünerTestVorDemCodeMeldetDemTestautorEinHindernis(tmp_path, monkeypatch, capsys):
    monkeypatch.setenv("CLAUDE_PROJECT_DIR", str(tmp_path))
    akzeptanztestAnlegen(tmp_path, "assert True")
    assert hauptprogramm(["Fachkritiker", "Kritik an den Tests"]) == 1
    assert "schon grün" in capsys.readouterr().err
    text = (tmp_path / "handoff/plan.md").read_text(encoding="utf-8")
    assert "- [ ] Fachkritiker: Kritik an den Tests zu Item stellen\n" in text
    assert "  Hindernis: Fachkritiker → Testautor:" in text
    assert "testAuf1_1EinModell" in text


def hindernisEintragen(
    wurzel: Path, rolle: str, tests: str, nummer: int, *, beseitigt: bool
) -> None:
    fortschrittSchreiben(wurzel)
    schreiben(wurzel, f"handoff/anliegen/{nummer}-hindernis.md", "# Hindernis\n")
    datei = wurzel / "handoff/plan.md"
    zeile = f"- [ ] {rolle}: Kritik an den Tests zu Item stellen\n"
    eintrag = f"  Hindernis: {rolle} → Testautor: Grün: {tests}. (Anliegen {nummer})"
    eintrag += "; beseitigt: Commit „Tests“\n" if beseitigt else "\n"
    text = datei.read_text(encoding="utf-8")
    datei.write_text(text.replace(zeile, zeile + eintrag), encoding="utf-8")


def anliegenNummern(wurzel: Path) -> list[str]:
    return sorted(datei.name.partition("-")[0] for datei in (wurzel / "handoff/anliegen").glob("*"))


@pytest.mark.usefixtures("plan")
def testEinGrünerTestImBeseitigtenHindernisDesSchrittsLässtDieKritikAbhaken(
    tmp_path, monkeypatch
):
    monkeypatch.setenv("CLAUDE_PROJECT_DIR", str(tmp_path))
    akzeptanztestAnlegen(tmp_path, "assert True")
    hindernisEintragen(tmp_path, "Fachkritiker", "testAuf1_1EinModell", 5, beseitigt=True)
    assert hauptprogramm(["Fachkritiker", "Kritik an den Tests"]) == 0
    text = (tmp_path / "handoff/plan.md").read_text(encoding="utf-8")
    assert "- [x] Fachkritiker: Kritik an den Tests zu Item stellen\n" in text
    assert anliegenNummern(tmp_path) == ["5"]


@pytest.mark.usefixtures("plan")
def testEinGrünerTestImBeseitigtenHindernisDesAnderenKritikersLässtAuchAbhaken(
    tmp_path, monkeypatch
):
    monkeypatch.setenv("CLAUDE_PROJECT_DIR", str(tmp_path))
    akzeptanztestAnlegen(tmp_path, "assert True")
    hindernisEintragen(tmp_path, "Architekt", "testAuf1_1EinModell", 5, beseitigt=True)
    assert hauptprogramm(["Fachkritiker", "Kritik an den Tests"]) == 0
    assert anliegenNummern(tmp_path) == ["5"]


@pytest.mark.usefixtures("plan")
def testEinGrünerTestNurImAnliegenDesBeseitigtenHindernisGenanntLässtAbhaken(
    tmp_path, monkeypatch
):
    monkeypatch.setenv("CLAUDE_PROJECT_DIR", str(tmp_path))
    akzeptanztestAnlegen(tmp_path, "assert True")
    hindernisEintragen(tmp_path, "Architekt", "zusammengefasst", 5, beseitigt=True)
    anliegen = tmp_path / "handoff/anliegen/5-hindernis.md"
    anliegen.write_text("Stelle für testAuf1_1EinModell\n", encoding="utf-8")
    assert hauptprogramm(["Fachkritiker", "Kritik an den Tests"]) == 0
    assert anliegenNummern(tmp_path) == ["5"]


@pytest.mark.usefixtures("plan")
def testEinTestZuEinerKennungNurInDerAbhängigkeitZähltNicht(tmp_path, monkeypatch):
    monkeypatch.setenv("CLAUDE_PROJECT_DIR", str(tmp_path))
    akzeptanztestAnlegen(tmp_path, "assert True")
    item = "# Stellen\n\nUmfang: AUF-2.1\n\nAbhängigkeit: AUF-1.1\n"
    schreiben(tmp_path, "domaene/items/stellen.md", item)
    assert hauptprogramm(["Fachkritiker", "Kritik an den Tests"]) == 0
    assert anliegenNummern(tmp_path) == []


@pytest.mark.usefixtures("plan")
def testEinNachDerUmsetzungNachgereichterTestWirdAmStandSeinesCommitsGemessen(
    tmp_path, gitRepo, monkeypatch, capsys
):
    monkeypatch.setenv("CLAUDE_PROJECT_DIR", str(tmp_path))
    akzeptanztestVomProduktAbhängig(tmp_path)
    produktcodeSetzen(tmp_path, "nein")
    datei = tmp_path / "handoff/plan.md"
    haken = "- [x] Testautor: Tests zu Item stellen\n"
    datei.write_text(datei.read_text(encoding="utf-8") + haken, encoding="utf-8")
    gitRepo.festhalten("Tests zu stellen")
    produktcodeSetzen(tmp_path, "kaputt")
    gitRepo.festhalten("stellen Umsetzung")
    testdatei = tmp_path / "technik/tests/akzeptanz/aufTest.py"
    nachgereicht = (
        "\n\ndef testAuf1_1NochEinModell():\n"
        '    assert Path("technik/arbiter/wert.txt").read_text(encoding="utf-8") != "kaputt"\n'
    )
    testdatei.write_text(testdatei.read_text(encoding="utf-8") + nachgereicht, encoding="utf-8")
    gitRepo.festhalten("Nachgereichter Test")
    produktcodeSetzen(tmp_path, "ja")
    gitRepo.festhalten("Behoben")
    assert hauptprogramm(["Fachkritiker", "Kritik an den Tests"]) == 0
    assert "schon grün" not in capsys.readouterr().err


@pytest.mark.usefixtures("plan")
def testEinGrünerTestImOffenenHindernisDesSchrittsMeldetKeinNeuesUndNenntEs(
    tmp_path, monkeypatch, capsys
):
    monkeypatch.setenv("CLAUDE_PROJECT_DIR", str(tmp_path))
    akzeptanztestAnlegen(tmp_path, "assert True")
    hindernisEintragen(tmp_path, "Fachkritiker", "testAuf1_1EinModell", 5, beseitigt=False)
    assert hauptprogramm(["Fachkritiker", "Kritik an den Tests"]) == 1
    assert "Anliegen 5" in capsys.readouterr().err
    assert anliegenNummern(tmp_path) == ["5"]


@pytest.mark.usefixtures("plan")
def testTeilsGenannteGrüneTestsMeldenNurDieÜbrigen(tmp_path, monkeypatch):
    monkeypatch.setenv("CLAUDE_PROJECT_DIR", str(tmp_path))
    akzeptanztestAnlegen(tmp_path, "assert True")
    datei = tmp_path / "technik/tests/akzeptanz/aufTest.py"
    zusatz = "\n\ndef testAuf1_1NochEinModell():\n    assert True\n"
    datei.write_text(datei.read_text(encoding="utf-8") + zusatz, encoding="utf-8")
    hindernisEintragen(tmp_path, "Fachkritiker", "testAuf1_1EinModell", 5, beseitigt=True)
    assert hauptprogramm(["Fachkritiker", "Kritik an den Tests"]) == 1
    (neues,) = (tmp_path / "handoff/anliegen").glob("06-*")
    inhalt = neues.read_text(encoding="utf-8")
    assert "testAuf1_1NochEinModell" in inhalt
    assert "testAuf1_1EinModell," not in inhalt
    assert "testAuf1_1EinModell." not in inhalt


@pytest.mark.usefixtures("plan")
def testEinRoterTestVorDemCodeLässtDieKritikAbhaken(tmp_path, monkeypatch):
    monkeypatch.setenv("CLAUDE_PROJECT_DIR", str(tmp_path))
    akzeptanztestAnlegen(tmp_path, "assert False")
    assert hauptprogramm(["Fachkritiker", "Kritik an den Tests"]) == 0
    text = (tmp_path / "handoff/plan.md").read_text(encoding="utf-8")
    assert "- [x] Fachkritiker: Kritik an den Tests zu Item stellen\n" in text


def produktcodeSetzen(wurzel: Path, wert: str) -> None:
    schreiben(wurzel, "technik/arbiter/wert.txt", wert)


def akzeptanztestVomProduktAbhängig(wurzel: Path) -> None:
    rumpf = 'assert Path("technik/arbiter/wert.txt").read_text(encoding="utf-8") == "ja"'
    schreiben(wurzel, ".claude/agents/testautor.md", "---\nname: testautor\n---\n")
    inhalt = f"from pathlib import Path\n\n\ndef testAuf1_1EinModell():\n    {rumpf}\n"
    schreiben(wurzel, "technik/tests/akzeptanz/aufTest.py", inhalt)


@pytest.mark.usefixtures("plan")
def testUncommitteterProduktcodeDerEinenTestGrünMachtMeldetKeinHindernis(
    tmp_path, gitRepo, monkeypatch
):
    monkeypatch.setenv("CLAUDE_PROJECT_DIR", str(tmp_path))
    akzeptanztestVomProduktAbhängig(tmp_path)
    produktcodeSetzen(tmp_path, "nein")
    gitRepo.festhalten("Stand vor der Umsetzung")
    produktcodeSetzen(tmp_path, "ja")
    assert hauptprogramm(["Fachkritiker", "Kritik an den Tests"]) == 0
    assert anliegenNummern(tmp_path) == []


@pytest.mark.usefixtures("plan")
def testCommitteterProduktcodeMitHakenDesImplementierersZähltNichtMehr(
    tmp_path, gitRepo, monkeypatch
):
    monkeypatch.setenv("CLAUDE_PROJECT_DIR", str(tmp_path))
    akzeptanztestVomProduktAbhängig(tmp_path)
    produktcodeSetzen(tmp_path, "nein")
    gitRepo.festhalten("Stand vor der Umsetzung")
    produktcodeSetzen(tmp_path, "ja")
    datei = tmp_path / "handoff/plan.md"
    haken = "- [x] Implementierer: Tests zu Item stellen grün\n"
    datei.write_text(datei.read_text(encoding="utf-8") + haken, encoding="utf-8")
    gitRepo.festhalten("Umsetzung")
    assert hauptprogramm(["Fachkritiker", "Kritik an den Tests"]) == 0
    assert anliegenNummern(tmp_path) == []


@pytest.mark.usefixtures("plan")
def testEinCommitteterTeilDerUmsetzungNachDenTestsMachtKeinenTestGrün(
    tmp_path, gitRepo, monkeypatch
):
    monkeypatch.setenv("CLAUDE_PROJECT_DIR", str(tmp_path))
    akzeptanztestVomProduktAbhängig(tmp_path)
    produktcodeSetzen(tmp_path, "nein")
    datei = tmp_path / "handoff/plan.md"
    haken = "- [x] Testautor: Tests zu Item stellen\n"
    datei.write_text(datei.read_text(encoding="utf-8") + haken, encoding="utf-8")
    gitRepo.festhalten("Tests zu stellen")
    produktcodeSetzen(tmp_path, "ja")
    gitRepo.festhalten("stellen Teil 1")
    assert hauptprogramm(["Fachkritiker", "Kritik an den Tests"]) == 0
    assert anliegenNummern(tmp_path) == []
