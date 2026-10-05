from pathlib import Path

import pytest

from formregeln.benennung import (
    dateinamenVerstoß,
    geprüfteDateien,
    nameVerstoß,
    quelltextVerstöße,
    verstöße,
)
from gemeinsam.pfade import altbestandOrdner, wurzel


def grundZu(quelltext: str, dateiname: str = "modul.py", *, akzeptanz: bool = False) -> list[str]:
    return quelltextVerstöße(quelltext, dateiname, imAkzeptanzordner=akzeptanz)


@pytest.mark.stand
def testDasRepoHältDieBenennung():
    assert verstöße(wurzel) == []


def testAltbestandOrdnerWerdenNichtGeprüft(tmp_path):
    for ordner in (*altbestandOrdner, "technik"):
        (tmp_path / ordner).mkdir()
        (tmp_path / ordner / "schlechterName.py").write_text("x = 1\n")
    geprüft = {pfad.relative_to(tmp_path).parts[0] for pfad in geprüfteDateien(tmp_path)}
    assert geprüft == {"technik"}


def testFrontendDateienUndNodeModulesWerdenGeprüftBeziehungsweiseAusgelassen(tmp_path):
    for pfad in ("technik/frontend/a.js", "node_modules/b/c.js", "technik/frontend/d.png"):
        (tmp_path / pfad).parent.mkdir(parents=True, exist_ok=True)
        (tmp_path / pfad).write_text("")
    geprüft = {pfad.relative_to(tmp_path).as_posix() for pfad in geprüfteDateien(tmp_path)}
    assert geprüft == {"technik/frontend/a.js"}


@pytest.mark.parametrize(
    "name",
    [
        pytest.param("einheitInAufstellungWählen", id="camelCase"),
        pytest.param("anDerReihe", id="Umlaut-frei"),
        pytest.param("nichtWählbar", id="Enum-Wert in camelCase (Anliegen 28 F1)"),
        pytest.param("_privat", id="führender Unterstrich"),
        pytest.param("__init__", id="Dunder"),
        pytest.param("tmp_path", id="Name, den pytest vorgibt"),
    ],
)
def testGuteNamenSindErlaubt(name):
    assert nameVerstoß(name) is None


@pytest.mark.parametrize(
    "name",
    [
        pytest.param("einheit_in_aufstellung", id="snake_case"),
        pytest.param("NICHT_WÄHLBAR", id="Konstante in Großbuchstaben"),
        pytest.param("ZONE", id="Konstante ohne Unterstrich"),
        pytest.param("a", id="ein Buchstabe"),
        pytest.param("zu", id="zwei Zeichen"),
        pytest.param("Einheit", id="PascalCase als Variable"),
    ],
)
def testSchlechteNamenSindVerstöße(name):
    assert nameVerstoß(name) is not None


def testKlassenHeißenInPascalCase():
    assert nameVerstoß("Aufstellungszone", istKlasse=True) is None
    assert nameVerstoß("aufstellungszone", istKlasse=True) is not None


@pytest.mark.parametrize(
    "quelltext",
    [
        pytest.param("def einheit_wählen(): ...", id="Funktion in snake_case"),
        pytest.param("def wählen(einheit, z): ...", id="einbuchstabiger Parameter"),
        pytest.param("ZONE = 1", id="Konstante"),
        pytest.param("for e in einheiten: ...", id="Schleifenvariable"),
        pytest.param("class a: ...", id="Klasse klein"),
        pytest.param("with open('x') as f: ...", id="with-Name"),
        pytest.param("class Ort:\n    def __init__(self):\n        self.an_der = 1", id="Attribut"),
        pytest.param("import json as j", id="Alias"),
        pytest.param("kriteriumsnummer = tuple[str, int]", id="Typalias klein"),
        pytest.param("type kriteriumsnummer = tuple[str, int]", id="type-Alias klein"),
        pytest.param("try:\n    pass\nexcept ValueError as e:\n    pass", id="except-Name"),
    ],
)
def testQuelltextMitSchlechtenNamenIstRot(quelltext):
    assert grundZu(quelltext)


def testAchsenXUndYSindFelderVonStelle():
    assert grundZu("class Stelle:\n    x: int\n    y: int\n") == []


def testAchsenAußerhalbVonStelleBleibenRot():
    assert grundZu("class Ort:\n    x: int\n")
    assert grundZu("x = 1\n")


def testTypaliaseStehenInPascalCase():
    assert grundZu("Kriteriumsnummer = tuple[str, int]\ntype Zeile = int\n") == []


def testQuelltextMitGutenNamenIstGrün():
    quelltext = "class Spieler:\n    def __init__(self, armee):\n        self.armee = armee\n"
    assert grundZu(quelltext) == []


def testAufrufeMitFremdenSchlüsselwortenSindKeineDefinition():
    assert grundZu("print(x_y=1)") == []


@pytest.mark.parametrize(
    "dateiname, akzeptanz, funktion, gut",
    [
        pytest.param("aufstellenTest.py", True, "testAuf1_4EinModellSetzen", True, id="Kriterium"),
        pytest.param("aufstellenTest.py", True, "testAuf1_4", False, id="ohne Satz"),
        pytest.param("aufstellenTest.py", True, "test_auf_1_4_ein_modell", False, id="snake_case"),
        pytest.param("aufstellenTest.py", True, "testEinModell", False, id="ohne Kriterium"),
        pytest.param("standTest.py", False, "testOhneEtappeWartet", True, id="Test eines Moduls"),
        pytest.param("standTest.py", False, "testOhne_etappe", False, id="Unterstrich im Test"),
        pytest.param("standTest.py", False, "testauf", False, id="klein nach test"),
    ],
)
def testTestfunktionenHeißenNachDerPrämisse(dateiname, akzeptanz, funktion, gut):
    meldungen = grundZu(f"def {funktion}(): ...\n", dateiname, akzeptanz=akzeptanz)
    assert (meldungen == []) is gut


@pytest.mark.parametrize(
    "pfad, gut",
    [
        pytest.param("technik/bashPositivliste.py", True, id="camelCase"),
        pytest.param("technik/bash_positivliste.py", False, id="snake_case"),
        pytest.param("technik/test_auf_1.py", False, id="altes Testschema"),
        pytest.param("technik/Größe.py", False, id="Umlaut im Dateinamen"),
        pytest.param("technik/conftest.py", True, id="Name, den pytest vorgibt"),
        pytest.param("domaene/anforderungen/phasen/aufstellen.md", True, id="Anforderung"),
        pytest.param("domaene/anforderungen/phasen/Aufstellen.md", False, id="Anforderung groß"),
        pytest.param("domaene/etappen/01-aufstellen.md", True, id="Etappe, nummeriert"),
        pytest.param("handoff/anliegen/09-fragen-freigabe-etappen.md", True, id="altes Anliegen"),
        pytest.param("handoff/anliegen/28-benennungOffenePunkte.md", True, id="neues Anliegen"),
        pytest.param("handoff/anliegen/32-neue-sache.md", False, id="Anliegen mit Bindestrich"),
        pytest.param("technik/CLAUDE.md", True, id="CLAUDE.md"),
        pytest.param("technik/frontend/spielfeld.js", True, id="Frontend camelCase"),
        pytest.param("technik/frontend/komponenten.html", True, id="Frontend html"),
        pytest.param("technik/frontend/spiel-feld.js", False, id="Frontend kebab"),
        pytest.param("technik/frontend/Spielfeld.css", False, id="Frontend groß"),
        pytest.param("technik/frontend/größe.js", False, id="Frontend Umlaut"),
    ],
)
def testDateinamen(tmp_path, pfad, gut):
    datei = tmp_path / pfad
    assert (dateinamenVerstoß(datei, tmp_path) is None) is gut


def aufbau(tmp_path, akzeptanztest: str) -> Path:
    (tmp_path / "domaene" / "anforderungen" / "phasen").mkdir(parents=True)
    (tmp_path / "domaene" / "anforderungen" / "phasen" / "aufstellen.md").write_text("x")
    ordner = tmp_path / "technik" / "tests" / "akzeptanz" / "phasen"
    ordner.mkdir(parents=True)
    datei = ordner / akzeptanztest
    datei.write_text("def testAuf1_1Probe(): ...\n", encoding="utf-8")
    return datei


def testAkzeptanztestZurAnforderungIstGrün(tmp_path):
    aufbau(tmp_path, "aufstellenTest.py")
    assert verstöße(tmp_path) == []


@pytest.mark.parametrize(
    "dateiname",
    [
        pytest.param("test_auf_1.py", id="altes Schema"),
        pytest.param("auf1Test.py", id="keine Anforderung dazu"),
        pytest.param("aufstellen.py", id="ohne Test im Namen"),
    ],
)
def testAkzeptanztestOhneSpiegelDerAnforderungIstRot(tmp_path, dateiname):
    aufbau(tmp_path, dateiname)
    assert any(dateiname in meldung for meldung in verstöße(tmp_path))


def aufbauGeteilt(tmp_path, dateiname: str) -> Path:
    anforderungen = tmp_path / "domaene" / "anforderungen" / "phasen"
    anforderungen.mkdir(parents=True)
    (anforderungen / "aufstellen.md").write_text("### AUF-1 · Probe\n", encoding="utf-8")
    ordner = tmp_path / "technik" / "tests" / "akzeptanz" / "phasen" / "aufstellen"
    ordner.mkdir(parents=True)
    datei = ordner / dateiname
    datei.write_text("def testAuf1_1Probe(): ...\n", encoding="utf-8")
    return datei


def testGeteilterAkzeptanztestZurAnforderungInDerDateiIstGrün(tmp_path):
    aufbauGeteilt(tmp_path, "auf1Test.py")
    assert verstöße(tmp_path) == []


def testGeteilterAkzeptanztestOhneAnforderungInDerDateiIstRot(tmp_path):
    aufbauGeteilt(tmp_path, "auf2Test.py")
    assert any("auf2Test.py" in meldung and "AUF-2" in meldung for meldung in verstöße(tmp_path))


def testPytestHookInConftestIstEinWerkzeugname():
    quelltext = "def pytest_configure(config):\n    pass\n"
    assert grundZu(quelltext, "conftest.py") == []


def testPytestHookAußerhalbVonConftestBleibtRot():
    quelltext = "def pytest_configure(config):\n    pass\n"
    assert grundZu(quelltext, "modul.py") != []
    assert grundZu("def pytest_irgendwas(config):\n    pass\n", "conftest.py") == []


def hilfsmodulAufbauen(tmp_path, ordnername: str, quelltext: str) -> Path:
    ordner = tmp_path / "technik" / "tests" / "akzeptanz" / ordnername
    ordner.mkdir(parents=True)
    datei = ordner / "handgriffe.py"
    datei.write_text(quelltext, encoding="utf-8")
    return datei


def testHilfsmodulImAkzeptanzordnerBrauchtKeineAnforderung(tmp_path):
    hilfsmodulAufbauen(tmp_path, "", "def stelleSetzen(): ...\n")
    assert verstöße(tmp_path) == []


def testHilfsmodulMitTestfunktionIstRot(tmp_path):
    hilfsmodulAufbauen(tmp_path, "", "def testAuf1_1Probe(): ...\n")
    assert any(
        "handgriffe.py" in meldung and "Testfunktion" in meldung for meldung in verstöße(tmp_path)
    )


def testHilfsmodulInEinemUnterordnerBleibtRot(tmp_path):
    hilfsmodulAufbauen(tmp_path, "phasen", "def stelleSetzen(): ...\n")
    assert any("handgriffe.py" in meldung for meldung in verstöße(tmp_path))
