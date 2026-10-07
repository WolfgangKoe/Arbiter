"""Scheiter-Test und Messung: Zweigabdeckung (DoD 1) und toter Code (DoD 2)."""

import pytest

from formregeln.abdeckung import (
    Abdeckung,
    abdeckungMessen,
    abdeckungText,
    aussetzung,
    prozentText,
    roteTests,
    schwelle,
    unbenutzterCode,
    verstoß,
)
from gemeinsam.pfade import akzeptanzOrdner, wurzel

vollständig = 100
modulMitZweig = "def zeichen(wert):\n    if wert:\n        return 'ja'\n    return 'nein'\n"
modulMitVielenZeilenUndEinemZweig = (
    "def zeichen(wert):\n"
    + "    wert += 1\n" * 40
    + "    if wert:\n        wert += 1\n    return wert\n"
)
testDerNurJaProbt = "from modul import zeichen\n\n\ndef testJa():\n    assert zeichen(1) == 'ja'\n"
testDerBeidesProbt = testDerNurJaProbt + "\n\ndef testNein():\n    assert zeichen(0) == 'nein'\n"
testDerNurDieZeilenProbt = (
    "from modul import zeichen\n\n\ndef testZeilen():\n    assert zeichen(1) == 42\n"
)
konfigurationDerProbe = (
    '[tool.pytest.ini_options]\npython_files = ["*Test.py"]\npythonpath = ["quelle"]\n'
    'markers = ["stand: Stand des Repos"]\n'
)


def messungAusDemRepo() -> str:
    abschnitt = (wurzel / "pyproject.toml").read_text(encoding="utf-8").split("[tool.coverage.run]")
    return "[tool.coverage.run]" + abschnitt[1].split("\n[")[0] + "\n"


def probeAnlegen(tmp_path, modul: str, test: str):
    for ordner in ("quelle", "tests"):
        (tmp_path / ordner).mkdir()
    (tmp_path / "pyproject.toml").write_text(konfigurationDerProbe + messungAusDemRepo())
    (tmp_path / "quelle" / "modul.py").write_text(modul)
    (tmp_path / "tests" / "probeTest.py").write_text(test)


def probeMessen(tmp_path, modul: str, test: str, auswahl: str | None = None) -> Abdeckung:
    probeAnlegen(tmp_path, modul, test)
    return abdeckungMessen(tmp_path, "quelle", "tests", auswahl)


def testEinNichtGeprobterZweigIstUnterDerSchwelle(tmp_path):
    assert probeMessen(tmp_path, modulMitZweig, testDerNurJaProbt).zweige < schwelle


def testVolleAbdeckungErreichtDieSchwelle(tmp_path):
    gemessen = probeMessen(tmp_path, modulMitZweig, testDerBeidesProbt)
    assert verstoß("probe", gemessen) is None


def testVieleGedeckteZeilenVerdeckenEinenFehlendenZweigNicht(tmp_path):
    gemessen = probeMessen(tmp_path, modulMitVielenZeilenUndEinemZweig, testDerNurDieZeilenProbt)
    assert gemessen.zeilen > schwelle
    assert gemessen.zweige < schwelle
    assert "Zweige" in verstoß("probe", gemessen)


def testDieMessungNimmtDieTestsAusDerAbdeckungAus(tmp_path):
    probeAnlegen(tmp_path, modulMitZweig, testDerBeidesProbt)
    (tmp_path / "quelle" / "andereTest.py").write_text("def testNie():\n    pass\n")
    assert abdeckungMessen(tmp_path, "quelle", "tests") == Abdeckung(vollständig, vollständig)


def testEinMitStandMarkierterTestZähltInDerAuswahlNichtMit(tmp_path):
    test = testDerNurJaProbt + "\n\n@pytest.mark.stand\ndef testNein():\n    zeichen(0)\n"
    test = "import pytest\n" + test
    mitStand = probeMessen(tmp_path, modulMitZweig, test)
    assert mitStand.zweige == vollständig
    ohneStand = abdeckungMessen(tmp_path, "quelle", "tests", "not stand")
    assert ohneStand.zweige < schwelle


def testEineMeldungRundetNichtAuf():
    assert prozentText(94.96) == "94.9 %"
    assert "94.9 %" in verstoß("probe", Abdeckung(vollständig, 94.96))


def testGrünUndRotNennenDieZahlenGleich():
    text = abdeckungText("probe", Abdeckung(98.26, 96.69))
    assert text == "Abdeckung von probe: Zeilen 98.2 %, Zweige 96.6 %"
    assert verstoß("probe", Abdeckung(98.26, 90)).startswith("Abdeckung von probe: Zeilen 98.2 %")


def testEinFalscherQuellpfadNenntDenPfad(tmp_path):
    probeAnlegen(tmp_path, modulMitZweig, testDerBeidesProbt)
    with pytest.raises(AssertionError, match="quelleFalsch"):
        abdeckungMessen(tmp_path, "quelleFalsch", "tests")


testDerNurEinKindprozessProbt = (
    "import os\nimport subprocess\nimport sys\n\n\n"
    "def testKind():\n"
    '    umgebung = {**os.environ, "PYTHONPATH": "quelle"}\n'
    '    befehl = [sys.executable, "-c", "import modul; modul.eins()"]\n'
    "    subprocess.run(befehl, env=umgebung, check=True)\n"
)


def testWasNurEinKindprozessDerTestsAusführtIstGedeckt(tmp_path):
    gemessen = probeMessen(tmp_path, "def eins():\n    return 1\n", testDerNurEinKindprozessProbt)
    assert gemessen == Abdeckung(vollständig, vollständig)


def testOhneMessungDerKindprozesseIstDieselbeProbeNichtGedeckt(tmp_path):
    probeAnlegen(tmp_path, "def eins():\n    return 1\n", testDerNurEinKindprozessProbt)
    (tmp_path / "pyproject.toml").write_text(konfigurationDerProbe)
    assert abdeckungMessen(tmp_path, "quelle", "tests").zeilen < schwelle


def testDieSchwelleGiltAuchFürDieZeilen():
    assert verstoß("probe", Abdeckung(90, 100)) is not None


def testEinProduktOhneZweigeHatVolleZweigabdeckung(tmp_path):
    gemessen = probeMessen(
        tmp_path,
        "def eins():\n    return 1\n",
        "from modul import eins\n\n\ndef testEins():\n    eins()\n",
    )
    assert gemessen.zweige == vollständig


testDerRotIst = "from modul import zeichen\n\n\ndef testRot():\n    assert zeichen(1) == 42\n"


def rotMessen(tmp_path) -> Abdeckung:
    return probeMessen(
        tmp_path, modulMitZweig, testDerRotIst + testDerBeidesProbt.split("\n\n\n", 1)[1]
    )


def testRoteTestsSetzenDieSchwelleAus(tmp_path):
    gemessen = rotMessen(tmp_path)
    assert gemessen.rote == 1
    assert "1 Tests rot" in aussetzung(gemessen)


def testGrüneTestsSetzenDieSchwelleNichtAus(tmp_path):
    gemessen = probeMessen(tmp_path, modulMitZweig, testDerNurJaProbt)
    assert gemessen.rote == 0
    assert aussetzung(gemessen) is None
    assert verstoß("probe", gemessen) is not None


def testRoteTestsZähltNurDieSchlusszeile():
    ausgabe = "assert '2 errors' == '0 errors'\nE  3 failed\n\n1 failed in 0.02s\n"
    assert roteTests(ausgabe) == 1


def testRoteTestsBeiLeererAusgabeIstNull():
    assert roteTests("  \n") == 0


@pytest.mark.stand
def testDasProduktErreichtDieSchwelleMitSeinenTests():
    gemessen = abdeckungMessen(wurzel, "technik/arbiter", "technik/tests")
    ausgesetzt = aussetzung(gemessen)
    if ausgesetzt:
        pytest.skip(ausgesetzt)
    assert verstoß("technik/arbiter", gemessen) is None, verstoß("technik/arbiter", gemessen)


def vultureProbe(tmp_path, quelle: str, akzeptanz: str, einheit: str) -> list[str]:
    (tmp_path / "pyproject.toml").write_text((wurzel / "pyproject.toml").read_text())
    for ordner in ("quelle", "akzeptanz", "einheit"):
        (tmp_path / ordner).mkdir()
    (tmp_path / "quelle" / "modul.py").write_text(quelle)
    (tmp_path / "akzeptanz" / "aTest.py").write_text(akzeptanz)
    (tmp_path / "einheit" / "eTest.py").write_text(einheit)
    return unbenutzterCode(tmp_path, "quelle", "akzeptanz")


gebraucht = "def gebraucht():\n    return 1\n"


def testCodeDenEinKriteriumAufruftIstBenutzt(tmp_path):
    kriterium = "from modul import gebraucht\n\n\ndef testA():\n    gebraucht()\n"
    assert vultureProbe(tmp_path, gebraucht, kriterium, "") == []


def testCodeDenNurEinEinheitstestAufruftMeldetVulture(tmp_path):
    einheit = "from modul import gebraucht\n\n\ngebraucht()\n"
    meldungen = vultureProbe(tmp_path, gebraucht, "def testA():\n    pass\n", einheit)
    assert any("gebraucht" in meldung for meldung in meldungen)


def testEineTestfunktionImProduktMeldetVultureAuch(tmp_path):
    produkt = gebraucht + "\n\ndef testlauf():\n    return 2\n"
    kriterium = "from modul import gebraucht\n\n\ndef testA():\n    gebraucht()\n"
    meldungen = vultureProbe(tmp_path, produkt, kriterium, "")
    assert any("testlauf" in meldung for meldung in meldungen)


def testEinFehlenderPfadIstRotStattLeer(tmp_path):
    with pytest.raises(AssertionError, match="gescheitert"):
        unbenutzterCode(tmp_path, "gibtsNicht")


def testEinSyntaxfehlerIstRotStattLeer(tmp_path):
    (tmp_path / "kaputt.py").write_text("def (:\n")
    with pytest.raises(AssertionError, match="gescheitert"):
        unbenutzterCode(tmp_path, "kaputt.py")


@pytest.mark.stand
def testDasProduktHatKeinenTotenCode():
    assert unbenutzterCode(wurzel, "technik/arbiter", akzeptanzOrdner) == []
