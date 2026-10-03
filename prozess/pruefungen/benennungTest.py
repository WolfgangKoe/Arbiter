from pathlib import Path

import pytest

import benennung
from benennung import (
    dateinamenVerstoß,
    fingerabdruck,
    nameVerstoß,
    quelltextVerstöße,
    rückstand,
    verstöße,
)

wurzel = Path(__file__).resolve().parents[2]


def grundZu(quelltext: str, dateiname: str = "modul.py", *, akzeptanz: bool = False) -> list[str]:
    return quelltextVerstöße(quelltext, dateiname, imAkzeptanzordner=akzeptanz)


def testDasRepoHältDieBenennung():
    assert verstöße(wurzel) == []


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
        pytest.param("try:\n    pass\nexcept ValueError as e:\n    pass", id="except-Name"),
    ],
)
def testQuelltextMitSchlechtenNamenIstRot(quelltext):
    assert grundZu(quelltext)


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


def testRückstandGiltNurFürDieUnveränderteDatei(tmp_path, monkeypatch):
    datei = aufbau(tmp_path, "test_auf_1.py")
    liste = tmp_path / "rueckstand.txt"
    pfad = datei.relative_to(tmp_path).as_posix()
    liste.write_text(f"{fingerabdruck(datei)} {pfad}\n", encoding="utf-8")
    monkeypatch.setattr(benennung, "rückstandsdatei", liste)
    assert pfad in rückstand(tmp_path)
    assert verstöße(tmp_path) == []

    datei.write_text(datei.read_text(encoding="utf-8") + "\n# berührt\n", encoding="utf-8")

    assert pfad not in rückstand(tmp_path)
    assert verstöße(tmp_path) != []


def testRückstandNimmtKeineDateienAußerhalbVonTechnikAus(tmp_path, monkeypatch):
    (tmp_path / "prozess").mkdir()
    datei = tmp_path / "prozess" / "schlecht_benannt.py"
    datei.write_text("x_y = 1\n", encoding="utf-8")
    liste = tmp_path / "rueckstand.txt"
    liste.write_text(f"{fingerabdruck(datei)} prozess/schlecht_benannt.py\n", encoding="utf-8")
    monkeypatch.setattr(benennung, "rückstandsdatei", liste)
    assert rückstand(tmp_path) == set()
    assert verstöße(tmp_path) != []
