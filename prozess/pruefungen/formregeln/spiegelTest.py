from pathlib import Path

import pytest

from formregeln.spiegel import verstöße
from gemeinsam.pfade import wurzel

anforderungstext = """### AUF-7 · Einheit in Aufstellung

- AUF-7.1 Erstes.
- AUF-7.3 Drittes.
- AUF-7.5 Fünftes.
"""


def kopfMitDocstring(überschrift: str = "AUF-7 · Einheit in Aufstellung.") -> str:
    return f'"""{überschrift}"""\n\n'


def funktionen(*namen: str) -> str:
    return "".join(f"def {name}(): ...\n\n\n" for name in namen)


def akzeptanztestAufbauen(tmp_path: Path, quelltext: str, anforderung: str = anforderungstext):
    datei = tmp_path / "domaene" / "anforderungen" / "phasen" / "einheitInAufstellung.md"
    datei.parent.mkdir(parents=True, exist_ok=True)
    datei.write_text(anforderung, encoding="utf-8")
    test = tmp_path / "technik" / "tests" / "akzeptanz" / "phasen" / "einheitInAufstellungTest.py"
    test.parent.mkdir(parents=True, exist_ok=True)
    test.write_text(quelltext, encoding="utf-8")


def modulAufbauen(tmp_path: Path, modul: str, *anforderungen: str):
    datei = tmp_path / "technik" / "arbiter" / "domaene" / modul
    datei.parent.mkdir(parents=True, exist_ok=True)
    datei.write_text('"""Probe."""\n', encoding="utf-8")
    for anforderung in anforderungen:
        ziel = tmp_path / "domaene" / "anforderungen" / anforderung
        ziel.parent.mkdir(parents=True, exist_ok=True)
        if ziel.suffix:
            ziel.write_text("### AUF-1 · Probe\n", encoding="utf-8")
        else:
            ziel.mkdir(exist_ok=True)


@pytest.mark.stand
def testDasRepoHältDenSpiegel():
    assert verstöße(wurzel) == []


def testPassenderAkzeptanztestIstGrün(tmp_path):
    quelltext = kopfMitDocstring() + funktionen(
        "testAuf7_1Erstes", "testAuf7_1Nochmal", "testAuf7_3Drittes"
    )
    akzeptanztestAufbauen(tmp_path, quelltext)
    assert verstöße(tmp_path) == []


def testDocstringAndersAlsDieÜberschriftIstRot(tmp_path):
    quelltext = kopfMitDocstring("AUF-7 · Einheit.") + funktionen("testAuf7_1Erstes")
    akzeptanztestAufbauen(tmp_path, quelltext)
    assert any("Docstring" in meldung for meldung in verstöße(tmp_path))


def testDocstringOhnePunktIstRot(tmp_path):
    quelltext = kopfMitDocstring("AUF-7 · Einheit in Aufstellung") + funktionen("testAuf7_1Erstes")
    akzeptanztestAufbauen(tmp_path, quelltext)
    assert any("Docstring" in meldung for meldung in verstöße(tmp_path))


def testFehlenderDocstringIstRot(tmp_path):
    akzeptanztestAufbauen(tmp_path, funktionen("testAuf7_1Erstes"))
    assert any("Docstring" in meldung for meldung in verstöße(tmp_path))


def testKennungEinerAnderenAnforderungIstRot(tmp_path):
    quelltext = kopfMitDocstring() + funktionen("testAuf7_1Erstes", "testAuf3_2Fremdes")
    akzeptanztestAufbauen(tmp_path, quelltext)
    assert any("AUF-3.2" in meldung and "AUF-7" in meldung for meldung in verstöße(tmp_path))


def testKürzelEinerAnderenAnforderungIstRot(tmp_path):
    akzeptanztestAufbauen(tmp_path, kopfMitDocstring() + funktionen("testQue7_1Fremdes"))
    assert any("QUE-7.1" in meldung for meldung in verstöße(tmp_path))


@pytest.mark.parametrize(
    "namen",
    [
        pytest.param(("testAuf7_3Drittes", "testAuf7_1Erstes"), id="Kriterien vertauscht"),
        pytest.param(
            ("testAuf7_1Erstes", "testAuf7_3Drittes", "testAuf7_1Nochmal"), id="Kennung getrennt"
        ),
        pytest.param(("testAuf7_5Fünftes", "testAuf7_3Drittes"), id="Spätes vor frühem"),
    ],
)
def testFalscheFolgeDerKennungenIstRot(tmp_path, namen):
    akzeptanztestAufbauen(tmp_path, kopfMitDocstring() + funktionen(*namen))
    assert any("nach" in meldung for meldung in verstöße(tmp_path))


def testLückeInDerFolgeDerKriterienIstGrün(tmp_path):
    quelltext = kopfMitDocstring() + funktionen("testAuf7_1Erstes", "testAuf7_5Fünftes")
    akzeptanztestAufbauen(tmp_path, quelltext)
    assert verstöße(tmp_path) == []


def testAkzeptanztestOhneAnforderungMeldetDieseNichtHier(tmp_path):
    akzeptanztestAufbauen(tmp_path, kopfMitDocstring() + funktionen("testAuf7_1Erstes"))
    (tmp_path / "domaene" / "anforderungen" / "phasen" / "einheitInAufstellung.md").unlink()
    assert verstöße(tmp_path) == []


@pytest.mark.parametrize(
    ("modul", "anforderungen"),
    [
        pytest.param("spielobjekte.py", ("spielobjekte",), id="Modul zum Ordner"),
        pytest.param("phasen/aufstellen.py", ("phasen/aufstellen",), id="Modul zum Unterordner"),
        pytest.param("phasen/__init__.py", ("phasen",), id="Paket zum Ordner"),
        pytest.param(
            "phasen/aufstellen/zug.py", ("phasen/aufstellen/zug.md",), id="Modul zur Datei"
        ),
        pytest.param("messen.py", (), id="Werkzeug messen"),
        pytest.param("sperre.py", (), id="Werkzeug sperre"),
    ],
)
def testModuleDerDomäneMitSpiegelSindGrün(tmp_path, modul, anforderungen):
    modulAufbauen(tmp_path, modul, *anforderungen)
    assert verstöße(tmp_path) == []


@pytest.mark.parametrize(
    "modul",
    [
        pytest.param("phasen/aufstellen/zug.py", id="Modul ohne Datei"),
        pytest.param("erfunden.py", id="Modul ohne Ordner"),
        pytest.param("erfunden/__init__.py", id="Paket ohne Ordner"),
    ],
)
def testModulDerDomäneOhneSpiegelIstRot(tmp_path, modul):
    modulAufbauen(tmp_path, modul, "phasen/aufstellen/ziehen.md")
    assert any(modul in meldung for meldung in verstöße(tmp_path))
