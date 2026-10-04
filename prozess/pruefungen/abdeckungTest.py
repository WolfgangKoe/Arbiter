"""Scheiter-Test und Messung: Zweigabdeckung (DoD 1) und toter Code (DoD 2)."""

import os

import pytest

from abdeckung import innenMarke, schwelle, unbenutzterCode, zweigabdeckung
from konfigurationTest import wurzel
from pfade import akzeptanzOrdner

vollständig = 100
modulMitZweig = "def zeichen(wert):\n    if wert:\n        return 'ja'\n    return 'nein'\n"
testDerBeideZweigeProbt = (
    "from modul import zeichen\n\n\ndef testJa():\n    assert zeichen(1) == 'ja'\n\n\n"
    "def testNein():\n    assert zeichen(0) == 'nein'\n"
)
testDerEinenZweigProbt = (
    "from modul import zeichen\n\n\ndef testJa():\n    assert zeichen(1) == 'ja'\n"
)
modulMitZweigOhneAnweisung = (
    "def zeichen(wert):\n    ergebnis = 'nein'\n    if wert:\n        ergebnis = 'ja'\n"
    "    return ergebnis\n"
)


def probeAnlegen(tmp_path, modul: str, test: str):
    (tmp_path / "quelle").mkdir()
    (tmp_path / "tests").mkdir()
    (tmp_path / "quelle" / "modul.py").write_text(modul)
    (tmp_path / "tests" / "probeTest.py").write_text(test)


def probeMessen(tmp_path, modul: str, test: str) -> float:
    probeAnlegen(tmp_path, modul, test)
    return zweigabdeckung(tmp_path, "quelle", "tests", suchpfad="quelle")


def testEineAbdeckungUnterDerSchwelleIstRot(tmp_path):
    assert probeMessen(tmp_path, modulMitZweig, testDerEinenZweigProbt) < schwelle


def testVolleAbdeckungErreichtDieSchwelle(tmp_path):
    assert probeMessen(tmp_path, modulMitZweig, testDerBeideZweigeProbt) >= schwelle


def testEinNichtGeprobterZweigOhneAnweisungZähltAlsLücke(tmp_path):
    prozent = probeMessen(tmp_path, modulMitZweigOhneAnweisung, testDerEinenZweigProbt)
    assert prozent < vollständig


def testDieMessungNimmtDieTestsAusDerAbdeckungAus(tmp_path):
    probeAnlegen(tmp_path, modulMitZweig, testDerBeideZweigeProbt)
    (tmp_path / "quelle" / "andereTest.py").write_text("def testNie():\n    pass\n")
    assert zweigabdeckung(tmp_path, "quelle", "tests", suchpfad="quelle") == vollständig


imÄußerenLauf = pytest.mark.skipif(
    innenMarke in os.environ, reason="Die Messung läuft schon im äußeren Lauf"
)


@imÄußerenLauf
def testDasProduktErreichtDieSchwelleMitSeinenTests():
    prozent = zweigabdeckung(wurzel, "technik/arbiter", "technik/tests", suchpfad="technik")
    assert prozent >= schwelle, f"Zweigabdeckung von technik/arbiter: {prozent:.1f} %"


@imÄußerenLauf
def testDiePrüfskripteErreichenDieSchwelleMitIhrenTests():
    prozent = zweigabdeckung(
        wurzel,
        "prozess/pruefungen",
        "prozess/pruefungen",
    )
    assert prozent >= schwelle, f"Zweigabdeckung von prozess/pruefungen: {prozent:.1f} %"


def vultureProbe(tmp_path, akzeptanz: str, einheit: str) -> list[str]:
    (tmp_path / "pyproject.toml").write_text('[tool.vulture]\nignore_names = ["test*"]\n')
    for ordner in ("quelle", "akzeptanz", "einheit"):
        (tmp_path / ordner).mkdir()
    (tmp_path / "quelle" / "modul.py").write_text("def gebraucht():\n    return 1\n")
    (tmp_path / "akzeptanz" / "aTest.py").write_text(akzeptanz)
    (tmp_path / "einheit" / "eTest.py").write_text(einheit)
    return unbenutzterCode(tmp_path, "quelle", "akzeptanz")


def testEinKriteriumDasDenCodeBraucht(tmp_path):
    meldungen = vultureProbe(
        tmp_path, "from modul import gebraucht\n\n\ndef testA():\n    gebraucht()\n", ""
    )
    assert meldungen == []


def testCodeDenNurEinEinheitstestAufruftMeldetVulture(tmp_path):
    meldungen = vultureProbe(
        tmp_path, "def testA():\n    pass\n", "from modul import gebraucht\n\n\ngebraucht()\n"
    )
    assert any("gebraucht" in meldung for meldung in meldungen)


def testDieKriterienAndersAlsEinheitstestsZählenAlsBenutzung():
    meldungen = unbenutzterCode(wurzel, "technik/arbiter", akzeptanzOrdner)
    assert meldungen == []
