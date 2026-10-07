"""Scheiter-Test und Stand: jede Datei hält ihr Höchstmaß (`hoechstmass.py`)."""

from pathlib import Path

import pytest

from formregeln.hoechstmass import (
    akzeptanztest,
    anliegen,
    architekturDatei,
    architekturDateien,
    architekturGesamt,
    architekturSumme,
    beschreibung,
    freigabeDatei,
    fälle,
    mockup,
    moderation,
    rollenordner,
    zeichen,
    zeichenOhneAntworten,
    zeichenOhneKommentare,
)
from gemeinsam.pfade import wurzel
from lesen.agenten import kopfzeilen


@pytest.mark.stand
@pytest.mark.parametrize(
    "datei, länge, grenze",
    [pytest.param(*fall, id=str(fall[0].relative_to(wurzel))) for fall in fälle()],
)
def testDateiHältIhrHöchstmaß(datei, länge, grenze):
    name = datei.relative_to(wurzel) if datei.is_relative_to(wurzel) else datei
    assert länge <= grenze, f"{name}: {länge} Zeichen, höchstens {grenze}"


@pytest.mark.stand
@pytest.mark.parametrize(
    "datei",
    [pytest.param(pfad, id=pfad.stem) for pfad in sorted(rollenordner.glob("*.md"))],
)
def testBeschreibungEinerRolleIstKurz(datei):
    kopf = kopfzeilen(datei.stem, wurzel)
    zeile = next(zeile for zeile in kopf if zeile.startswith("description:"))
    text = zeile.removeprefix("description:").strip()
    assert len(text) <= beschreibung, f"{datei.stem}: {len(text)} Zeichen"


def testZuLangesAnliegenWärRot(tmp_path):
    zuLang = tmp_path / "99-zuLang.md"
    zuLang.write_text("x" * (anliegen + 1), encoding="utf-8")
    assert zeichen(zuLang) > anliegen


def testZuLangeModerationWärRot(tmp_path):
    zuLang = tmp_path / "moderation.md"
    zuLang.write_text("x" * (moderation + 1), encoding="utf-8")
    assert zeichen(zuLang) > moderation


def testZuLangerAkzeptanztestWärRot(tmp_path):
    zuLang = tmp_path / "aufstellenTest.py"
    zuLang.write_text("x" * (akzeptanztest + 1), encoding="utf-8")
    assert zeichen(zuLang) > akzeptanztest


@pytest.mark.stand
def testDieArchitekturHältIhrGesamtmaß():
    summe = architekturSumme()
    assert summe <= architekturGesamt, (
        f"technik/architektur: {summe} Zeichen, höchstens {architekturGesamt}"
    )


def architekturOrdner(tmp_path, größen: list[int]) -> Path:
    thema = tmp_path / "technik" / "architektur"
    thema.mkdir(parents=True)
    for nummer, größe in enumerate(größen):
        (thema / f"thema{nummer}.md").write_text("x" * größe, encoding="utf-8")
    return tmp_path


def testZuLangeArchitekturdateiWärRot(tmp_path):
    ordner = architekturOrdner(tmp_path, [architekturDatei + 1])
    (datei,) = architekturDateien(ordner)
    länge = zeichen(datei)
    with pytest.raises(AssertionError):
        testDateiHältIhrHöchstmaß(datei, länge, architekturDatei)


def testArchitekturdateienÜberDemGesamtmaßWärenRot(tmp_path):
    ordner = architekturOrdner(tmp_path, [architekturDatei] * 4 + [1])
    assert architekturSumme(ordner) > architekturGesamt


def testArchitekturdateienImGesamtmaßSindGrün(tmp_path):
    ordner = architekturOrdner(tmp_path, [architekturDatei] * 4)
    assert architekturSumme(ordner) <= architekturGesamt


def testFehlenderArchitekturordnerIstGrün(tmp_path):
    assert architekturDateien(tmp_path) == []
    assert architekturSumme(tmp_path) == 0


def testZuLangesMockupWärRot(tmp_path):
    zuLang = tmp_path / "QUE-2.html"
    zuLang.write_text("x" * (mockup + 1), encoding="utf-8")
    länge = zeichen(zuLang)
    with pytest.raises(AssertionError):
        testDateiHältIhrHöchstmaß(zuLang, länge, mockup)


def anliegenMitAntwort(tmp_path, eigener: int, antwort: int) -> Path:
    datei = tmp_path / "99-mitAntwort.md"
    datei.write_text("x" * eigener + "\nAntwort: " + "y" * antwort, encoding="utf-8")
    return datei


def testLangeAntwortLässtDenEchtenTestGrünDurch(tmp_path):
    datei = anliegenMitAntwort(tmp_path, 3980, 500)
    testDateiHältIhrHöchstmaß(datei, zeichenOhneAntworten(datei), anliegen)


def testZuLangerEigenerTextMachtDenEchtenTestRotTrotzAntwort(tmp_path):
    datei = anliegenMitAntwort(tmp_path, 4010, 500)
    gezählt = zeichenOhneAntworten(datei)
    with pytest.raises(AssertionError):
        testDateiHältIhrHöchstmaß(datei, gezählt, anliegen)


def freigabeDateiMitKommentar(tmp_path, eigener: int, kommentar: int) -> Path:
    datei = tmp_path / "retro.md"
    datei.write_text("x" * eigener + "\nKommentar: " + "y" * kommentar, encoding="utf-8")
    return datei


def testLangerKommentarLässtDenEchtenTestGrünDurch(tmp_path):
    datei = freigabeDateiMitKommentar(tmp_path, 3980, 500)
    testDateiHältIhrHöchstmaß(datei, zeichenOhneKommentare(datei), freigabeDatei)


def testZuLangerEigenerTextMachtDenEchtenTestRotTrotzKommentar(tmp_path):
    datei = freigabeDateiMitKommentar(tmp_path, 4010, 500)
    gezählt = zeichenOhneKommentare(datei)
    with pytest.raises(AssertionError):
        testDateiHältIhrHöchstmaß(datei, gezählt, freigabeDatei)
