from pathlib import Path

import pytest

from rueckverfolgung import getesteKriterien, kriterien, verstöße

wurzel = Path(__file__).resolve().parents[2]

zweiKriterien = 2
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


def testFehlenderTestZumKriteriumIstRot(tmp_path):
    aufbau(tmp_path, "def testAuf1_1Eins(): ...\n")
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
    assert len(verstöße(tmp_path)) == zweiKriterien


def testAnforderungOhneTestdateiWartetAufDenTestautor(tmp_path):
    anforderung = tmp_path / "domaene" / "anforderungen" / "phasen" / "aufstellen.md"
    anforderung.parent.mkdir(parents=True)
    anforderung.write_text(anforderungstext, encoding="utf-8")
    assert verstöße(tmp_path) == []
