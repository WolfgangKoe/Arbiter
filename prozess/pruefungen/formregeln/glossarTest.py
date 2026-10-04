import pytest

from formregeln.glossar import glossarBezeichner, gründe, quelltextVerstöße, verstöße
from gemeinsam.pfade import wurzel

glossarText = """Begriff | englisch | Code-Bezeichner | Definition
---|---|---|---
Aufstellungszone | zone | Aufstellungszone (erste, zweite) | Fläche.
Einheit | unit | Einheit | Modelle.
"""
glossar = glossarBezeichner(glossarText)


def meldungenZu(quelltext: str, gründeDerAnforderungen: set[str] | None = None) -> list[str]:
    return quelltextVerstöße(quelltext, "modul.py", glossar, gründeDerAnforderungen or set())


@pytest.mark.stand
def testDasRepoHältDieÜbereinstimmungVonCodeUndGlossar():
    assert verstöße(wurzel) == []


def testKlasseUndEnumWerteStehenInDerSpalteCodeBezeichner():
    assert glossar == {"Aufstellungszone": {"erste", "zweite"}, "Einheit": set()}


def testGründeStehenInEinfachenAnführungszeichen():
    assert gründe("*Sperre* ‚nicht wählbar‘, dann ‚Einheit begonnen‘.") == {
        "nicht wählbar",
        "Einheit begonnen",
    }


def testBekannteKlasseUndBekannteEnumWerteSindGrün():
    quelltext = "class Aufstellungszone(Enum):\n    erste = 1\n    zweite = 2\n"
    assert meldungenZu(quelltext) == []


def testErfundenerEnumWertScheitert():
    quelltext = "class Aufstellungszone(Enum):\n    erste = 1\n    nord = 2\n"
    meldungen = meldungenZu(quelltext)
    assert len(meldungen) == 1
    assert "Aufstellungszone.nord" in meldungen[0]
    assert "Anforderungsautor" in meldungen[0]


def testErfundeneKlasseScheitert():
    meldungen = meldungenZu("class Spielfeld:\n    pass\n")
    assert len(meldungen) == 1
    assert "Klasse Spielfeld" in meldungen[0]


def testEnumWertMitGrundInEinerAnforderungIstGrün():
    quelltext = 'class Einheit(Enum):\n    nichtWählbar = "nicht wählbar"\n'
    assert meldungenZu(quelltext, {"nicht wählbar"}) == []
    assert len(meldungenZu(quelltext)) == 1


def testEnumMitAttributAlsBasisWirdGeprüft():
    quelltext = "class Aufstellungszone(enum.Enum):\n    erste = 1\n    nord = 2\n"
    assert "Aufstellungszone.nord" in meldungenZu(quelltext)[0]


def testFlagUndIntFlagSindEnums():
    for basis in ("Flag", "IntFlag", "enum.IntFlag"):
        quelltext = f"class Aufstellungszone({basis}):\n    nord = 2\n"
        assert len(meldungenZu(quelltext)) == 1


def testEnumWertMitAnnotationWirdGeprüft():
    quelltext = "class Aufstellungszone(Enum):\n    erste = 1\n    nord: int = 2\n"
    assert "Aufstellungszone.nord" in meldungenZu(quelltext)[0]


def testAnnotationOhneWertIstKeinEnumWert():
    assert meldungenZu("class Aufstellungszone(Enum):\n    erste = 1\n    nord: int\n") == []


def testDieVerstößeEinesVerzeichnissesNennenDieDateiMitDemUnbekanntenEnumWert(tmp_path):
    (tmp_path / "domaene").mkdir()
    (tmp_path / "domaene" / "glossar.md").write_text(glossarText, encoding="utf-8")
    (tmp_path / "domaene" / "anforderungen").mkdir()
    (tmp_path / "domaene" / "anforderungen" / "a.md").write_text("‚Grund‘\n", encoding="utf-8")
    ordner = tmp_path / "technik" / "arbiter" / "domaene"
    ordner.mkdir(parents=True)
    (ordner / "gut.py").write_text("class Einheit:\n    pass\n", encoding="utf-8")
    (ordner / "schlecht.py").write_text(
        "from enum import Enum\n\n\nclass Aufstellungszone(Enum):\n    dritte = 3\n",
        encoding="utf-8",
    )
    meldungen = verstöße(tmp_path)
    assert len(meldungen) == 1
    assert "schlecht.py" in meldungen[0]
    assert "Aufstellungszone.dritte" in meldungen[0]
