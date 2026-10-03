import json
import subprocess
from pathlib import Path

import pytest

from rueckverfolgung import (
    getesteKriterien,
    hauptprogramm,
    kriterien,
    spur,
    verstöße,
    wartende,
)

wurzel = Path(__file__).resolve().parents[2]

zweiKriterien = 2
zweiVerstöße = 2
anforderungstext = """# Aufstellen

### AUF-1 · Reihenfolge

- AUF-1.1 Vom *Roll-off* wird nur der *Gewinner* eingegeben.
- AUF-1.4 Ein *Modell* außerhalb der *Einheit in Aufstellung* *setzen*: *Sperre*.
"""


def aufbau(tmp_path: Path, testtext: str) -> None:
    anforderung = tmp_path / "domaene" / "anforderungen" / "phasen" / "aufstellen.md"
    anforderung.parent.mkdir(parents=True)
    anforderung.write_text(anforderungstext, encoding="utf-8")
    test = tmp_path / "technik" / "tests" / "akzeptanz" / "phasen" / "aufstellenTest.py"
    test.parent.mkdir(parents=True)
    test.write_text(testtext, encoding="utf-8")


def testDasRepoHältDieRückverfolgung():
    assert verstöße(wurzel) == []


def testKriterienStehenAlsListenpunktMitKürzelUndNummer(tmp_path):
    aufbau(tmp_path, "")
    anforderung = tmp_path / "domaene" / "anforderungen" / "phasen" / "aufstellen.md"
    assert kriterien(anforderung) == {("AUF", 1, 1), ("AUF", 1, 4)}


def testEinTestMitKürzelUndNummernWirdAlsKriteriumErkannt(tmp_path):
    aufbau(tmp_path, "def testAuf1_4EinModellDerEinheitInAufstellungLässtSichSetzen(): ...\n")
    testdatei = tmp_path / "technik" / "tests" / "akzeptanz" / "phasen" / "aufstellenTest.py"
    assert getesteKriterien(testdatei) == {("AUF", 1, 4)}


def testAlleKriterienMitTestIstGrün(tmp_path):
    aufbau(tmp_path, "def testAuf1_1Eins(): ...\ndef testAuf1_4Vier(): ...\n")
    assert verstöße(tmp_path) == []


def freigegebenerPlanMitItem(wurzel: Path, itemtext: str) -> None:
    (wurzel / "handoff").mkdir(exist_ok=True)
    (wurzel / "handoff" / "plan.md").write_text(
        "# Plan · Zyklus 1\n\n1. [Probe](../domaene/items/probe.md)\n", encoding="utf-8"
    )
    (wurzel / "domaene" / "items").mkdir(parents=True, exist_ok=True)
    (wurzel / "domaene" / "items" / "probe.md").write_text(itemtext, encoding="utf-8")
    for befehl in (
        ["init", "-q"],
        ["add", "-A"],
        ["-c", "user.name=t", "-c", "user.email=t@t", "commit", "-q", "-m", "Freigabe Plan 1"],
    ):
        subprocess.run(["git", *befehl], cwd=wurzel, check=True)


def testFehlenderTestZumKriteriumIstRot(tmp_path):
    aufbau(tmp_path, "def testAuf1_1Eins(): ...\n")
    freigegebenerPlanMitItem(tmp_path, "# Probe\n\nUmfang: AUF-1.\n")
    meldungen = verstöße(tmp_path)
    assert len(meldungen) == 1
    assert "AUF-1.4 hat keinen Test" in meldungen[0]


def testTestOhneKriteriumIstRot(tmp_path):
    aufbau(tmp_path, "def testAuf1_1Eins(): ...\ndef testAuf1_4Vier(): ...\ndef testAuf1_9X(): ...")
    meldungen = verstöße(tmp_path)
    assert len(meldungen) == 1
    assert "AUF-1.9" in meldungen[0]


@pytest.mark.parametrize("test", ["def test_auf_1_1_eins(): ...\n", "def testAuf1Eins(): ...\n"])
def testAltesOderUnvollständigesSchemaZähltNichtAlsTest(tmp_path, test):
    aufbau(tmp_path, test)
    freigegebenerPlanMitItem(tmp_path, "# Probe\n\nUmfang: AUF-1.\n")
    assert len(verstöße(tmp_path)) == zweiKriterien


def testAnforderungOhneTestdateiWartetAufDenTestautor(tmp_path):
    anforderung = tmp_path / "domaene" / "anforderungen" / "phasen" / "aufstellen.md"
    anforderung.parent.mkdir(parents=True)
    anforderung.write_text(anforderungstext, encoding="utf-8")
    assert verstöße(tmp_path) == []


def testKriteriumOhneTestWartetSolangeKeinFreigegebenerPlanEsUmfasst(tmp_path):
    aufbau(tmp_path, "def testAuf1_1Eins(): ...\n")
    assert verstöße(tmp_path) == []
    assert wartende(tmp_path) == ["AUF-1.4"]


def testPlanOhneFreigabeUmfasstNichts(tmp_path):
    aufbau(tmp_path, "def testAuf1_1Eins(): ...\n")
    freigegebenerPlanMitItem(tmp_path, "# Probe\n\nUmfang: AUF-1.\n")
    amend = ["-c", "user.name=t", "-c", "user.email=t@t", "commit", "-q", "--amend", "-m", "Plan 1"]
    subprocess.run(["git", *amend], cwd=tmp_path, check=True)
    assert verstöße(tmp_path) == []


@pytest.mark.parametrize("umfang", ["AUF-1", "AUF-1.4"])
def testFreigegebenerPlanMachtDasFehlendeKriteriumRot(tmp_path, umfang):
    aufbau(tmp_path, "def testAuf1_1Eins(): ...\n")
    freigegebenerPlanMitItem(tmp_path, f"# Probe\n\nUmfang: {umfang}.\n")
    assert len(verstöße(tmp_path)) == 1
    assert wartende(tmp_path) == []


@pytest.mark.parametrize("umfang", ["AUF-14", "AUF-1.5", "AUF-2"])
def testItemMitAndererKennungMachtDasKriteriumNichtRot(tmp_path, umfang):
    aufbau(tmp_path, "def testAuf1_1Eins(): ...\n")
    freigegebenerPlanMitItem(tmp_path, f"# Probe\n\nUmfang: {umfang}.\n")
    assert verstöße(tmp_path) == []


def testDoppeltesKriteriumIstAuchOhneTestdateiRot(tmp_path):
    anforderung = tmp_path / "domaene" / "anforderungen" / "phasen" / "aufstellen.md"
    anforderung.parent.mkdir(parents=True)
    anforderung.write_text(anforderungstext + "- AUF-1.1 Noch einmal.\n", encoding="utf-8")
    assert verstöße(tmp_path) == [
        "domaene/anforderungen/phasen/aufstellen.md: AUF-1.1 steht zweimal"
    ]


def testDoppelteAnforderungIstRot(tmp_path):
    anforderung = tmp_path / "domaene" / "anforderungen" / "phasen" / "aufstellen.md"
    anforderung.parent.mkdir(parents=True)
    anforderung.write_text(anforderungstext + "\n### AUF-1 · Noch einmal\n", encoding="utf-8")
    assert verstöße(tmp_path) == ["domaene/anforderungen/phasen/aufstellen.md: AUF-1 steht zweimal"]


zweiAnforderungen = """### AUF-1 · Reihenfolge

- AUF-1.1 Eins.

### AUF-2 · Ablage

- AUF-2.1 Zwei.
"""


def zweiAnforderungenMitTests(wurzel: Path, dateien: dict[str, str]) -> None:
    anforderung = wurzel / "domaene" / "anforderungen" / "phasen" / "aufstellen.md"
    anforderung.parent.mkdir(parents=True)
    anforderung.write_text(zweiAnforderungen, encoding="utf-8")
    for name, text in dateien.items():
        datei = wurzel / "technik" / "tests" / "akzeptanz" / "phasen" / name
        datei.parent.mkdir(parents=True, exist_ok=True)
        datei.write_text(text, encoding="utf-8")


def testJeAnforderungEineTestdateiIstGrün(tmp_path):
    zweiAnforderungenMitTests(
        tmp_path,
        {
            "aufstellen/auf1Test.py": "def testAuf1_1Eins(): ...\n",
            "aufstellen/auf2Test.py": "def testAuf2_1Zwei(): ...\n",
        },
    )
    assert verstöße(tmp_path) == []


def testTestsZuZweiAnforderungenInEinerDateiSindRot(tmp_path):
    zweiAnforderungenMitTests(
        tmp_path, {"aufstellenTest.py": "def testAuf1_1Eins(): ...\ndef testAuf2_1Zwei(): ...\n"}
    )
    planMitUmfang(tmp_path, "AUF-2")
    assert "teilen nach Anforderung" in verstöße(tmp_path)[0]


def testTestZuAuf2InDerDateiVonAuf1IstRot(tmp_path):
    zweiAnforderungenMitTests(
        tmp_path,
        {"aufstellen/auf1Test.py": "def testAuf1_1Eins(): ...\ndef testAuf2_1Zwei(): ...\n"},
    )
    meldungen = verstöße(tmp_path)
    assert len(meldungen) == 1
    assert "Test zu AUF-2.1" in meldungen[0]


def spurProbe(wurzel: Path) -> None:
    aufbau(wurzel, "def testAuf1_1Eins(): ...\n\n\ndef testAuf1_4Vier(): ...\n")
    test = wurzel / "technik" / "tests" / "akzeptanz" / "phasen" / "aufstellenTest.py"
    test.write_text(test.read_text(encoding="utf-8") + "\n\ndef testAuf1_4NochEins(): ...\n")


kriteriumsPfad = "domaene/anforderungen/phasen/aufstellen.md"
testPfad = "technik/tests/akzeptanz/phasen/aufstellenTest.py"


def testSpurNenntDasKriteriumUndJedenSeinerTests(tmp_path):
    spurProbe(tmp_path)
    assert spur(tmp_path, "AUF-1.4") == [
        ("Kriterium", kriteriumsPfad, 6),
        ("Test", testPfad, 4),
        ("Test", testPfad, 7),
    ]


@pytest.mark.parametrize(
    "eingabe", ["auf-1.4", "testAuf1_4Vier", f"{kriteriumsPfad}:6", f"{testPfad}:7"]
)
def testSpurKenntDasKriteriumAuchAnTestnameUndStelle(tmp_path, eingabe):
    spurProbe(tmp_path)
    assert spur(tmp_path, eingabe) == spur(tmp_path, "AUF-1.4")


@pytest.mark.parametrize("eingabe", ["AUF-9.9", "nichts", f"{testPfad}:3", "x.md:3"])
def testSpurZuUnbekanntemKriteriumIstEinFehler(tmp_path, eingabe, monkeypatch, capsys):
    spurProbe(tmp_path)
    monkeypatch.setenv("CLAUDE_PROJECT_DIR", str(tmp_path))
    assert spur(tmp_path, eingabe) is None
    assert hauptprogramm([eingabe]) == 1
    assert "Unbekanntes Kriterium" in capsys.readouterr().err


def testSpurAlsJsonIstEineListeVonObjekten(tmp_path, monkeypatch, capsys):
    spurProbe(tmp_path)
    monkeypatch.setenv("CLAUDE_PROJECT_DIR", str(tmp_path))
    assert hauptprogramm(["AUF-1.1", "--json"]) == 0
    assert json.loads(capsys.readouterr().out) == [
        {"art": "Kriterium", "pfad": kriteriumsPfad, "zeile": 5},
        {"art": "Test", "pfad": testPfad, "zeile": 1},
    ]


def planMitUmfang(wurzel: Path, umfang: str) -> None:
    freigegebenerPlanMitItem(wurzel, f"# Probe\n\nUmfang: {umfang}.\n")


def testFehlendeTestdateiEinerUmfasstenAnforderungIstRot(tmp_path):
    zweiAnforderungenMitTests(tmp_path, {"aufstellen/auf1Test.py": "def testAuf1_1Eins(): ...\n"})
    planMitUmfang(tmp_path, "AUF-2")
    meldungen = verstöße(tmp_path)
    assert meldungen == ["technik/tests/akzeptanz/phasen/aufstellen/auf2Test.py fehlt"]


def testFehlendeTestdateiEinerNichtUmfasstenAnforderungWartet(tmp_path):
    zweiAnforderungenMitTests(tmp_path, {"aufstellen/auf1Test.py": "def testAuf1_1Eins(): ...\n"})
    assert verstöße(tmp_path) == []
    assert wartende(tmp_path) == ["AUF-2"]


def testSammeldateiBleibtGrünBisEinPlanEineSpätereAnforderungUmfasst(tmp_path):
    zweiAnforderungenMitTests(tmp_path, {"aufstellenTest.py": "def testAuf1_1Eins(): ...\n"})
    assert verstöße(tmp_path) == []
    assert wartende(tmp_path) == ["AUF-2"]
    planMitUmfang(tmp_path, "AUF-2")
    meldungen = verstöße(tmp_path)
    assert len(meldungen) == zweiVerstöße
    assert "teilen nach Anforderung" in meldungen[0]
    assert meldungen[1].endswith("auf2Test.py fehlt")


def testSammeldateiMitTestZuAuf2OhnePlanIstRot(tmp_path):
    zweiAnforderungenMitTests(
        tmp_path, {"aufstellenTest.py": "def testAuf1_1Eins(): ...\ndef testAuf2_1Zwei(): ...\n"}
    )
    assert "Test zu AUF-2.1" in verstöße(tmp_path)[0]


def testEinzeldateiNebenGültigerSammeldateiWirdGeprüftUndIstRot(tmp_path):
    zweiAnforderungenMitTests(
        tmp_path,
        {
            "aufstellenTest.py": "def testAuf1_1Eins(): ...\n",
            "aufstellen/auf1Test.py": "def testAuf1_9Falsch(): ...\n",
        },
    )
    meldungen = verstöße(tmp_path)
    assert any("neben" in meldung for meldung in meldungen)
    assert any("Test zu AUF-1.9" in meldung for meldung in meldungen)


def einzigeAnforderung(wurzel: Path, dateien: dict[str, str]) -> None:
    anforderung = wurzel / "domaene" / "anforderungen" / "phasen" / "aufstellen.md"
    anforderung.parent.mkdir(parents=True)
    anforderung.write_text("### AUF-1 · Reihenfolge\n\n- AUF-1.1 Eins.\n", encoding="utf-8")
    for name, text in dateien.items():
        datei = wurzel / "technik" / "tests" / "akzeptanz" / "phasen" / name
        datei.parent.mkdir(parents=True, exist_ok=True)
        datei.write_text(text, encoding="utf-8")


def testEinzeldateiDerEinzigenAnforderungIstGrünUndNichtWartend(tmp_path):
    einzigeAnforderung(tmp_path, {"aufstellen/auf1Test.py": "def testAuf1_1Eins(): ...\n"})
    assert verstöße(tmp_path) == []
    assert wartende(tmp_path) == []


def testFehlenBeideDateienMeldetEinPlanAufDieEinzigeAnforderungDieEinzeldatei(tmp_path):
    einzigeAnforderung(tmp_path, {})
    planMitUmfang(tmp_path, "AUF-1")
    assert verstöße(tmp_path) == ["technik/tests/akzeptanz/phasen/aufstellen/auf1Test.py fehlt"]


def testTestsOhneAnforderungNennenDieKennungen(tmp_path):
    anforderung = tmp_path / "domaene" / "anforderungen" / "leer.md"
    anforderung.parent.mkdir(parents=True)
    anforderung.write_text("# Leer\n", encoding="utf-8")
    test = tmp_path / "technik" / "tests" / "akzeptanz" / "leerTest.py"
    test.parent.mkdir(parents=True)
    test.write_text("def testAuf7_1X(): ...\n", encoding="utf-8")
    meldungen = verstöße(tmp_path)
    assert len(meldungen) == 1
    assert meldungen[0].endswith("Tests ohne Anforderung: AUF-7.1")
