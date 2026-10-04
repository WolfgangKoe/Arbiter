"""Höchstmaße in Zeichen für die Dateien im Repo; ein Verstoß sperrt den Commit."""

import re
from pathlib import Path

import pytest

from agenten import kopfzeilen
from anliegen import antwortZeile
from freigabeKommentare import artefakte, kommentarZeile, pfadDer
from pfade import (
    akzeptanzOrdner,
    anliegenOrdner,
    etappenOrdner,
    mockupOrdner,
    perspektiven,
    wurzel,
)

aktuelleEtappe = 1000
spätereEtappe = 200
agentendefinition = 2500
beschreibung = 150
rootClaudeMitZiel = 4000
ordnerClaude = 1500
anliegen = 4000
freigabeDatei = 4000
moderation = 4000
akzeptanztest = 20000
mockup = 8000
rollenordner = wurzel / ".claude" / "agents"


def zeichen(datei: Path) -> int:
    return len(datei.read_text(encoding="utf-8"))


def zeichenMitErsatz(datei: Path, zeile: re.Pattern, ersatz: str) -> int:
    zeilen = datei.read_text(encoding="utf-8").split("\n")
    return sum(len(ersatz if zeile.match(text) else text) + 1 for text in zeilen) - 1


def zeichenOhneAntworten(datei: Path) -> int:
    return zeichenMitErsatz(datei, antwortZeile, "Antwort: .")


def zeichenOhneKommentare(datei: Path) -> int:
    return zeichenMitErsatz(datei, re.compile(f"^{kommentarZeile}"), f"{kommentarZeile} .")


def mockupFälle():
    for datei in sorted((wurzel / mockupOrdner).rglob("*")):
        if datei.is_file():
            yield datei, zeichen(datei), mockup


def fälle():
    etappen = sorted((wurzel / etappenOrdner).glob("*.md"))
    for nummer, datei in enumerate(etappen):
        grenze = aktuelleEtappe if nummer == 0 else spätereEtappe
        yield datei, zeichen(datei), grenze
    for datei in sorted((wurzel / ".claude" / "agents").glob("*.md")):
        yield datei, zeichen(datei), agentendefinition
    for datei in sorted((wurzel / anliegenOrdner).glob("*.md")):
        yield datei, zeichenOhneAntworten(datei), anliegen
    for artefakt in artefakte:
        datei = pfadDer(wurzel, artefakt)
        if datei.is_file():
            yield datei, zeichenOhneKommentare(datei), freigabeDatei
    moderationsdatei = wurzel / "handoff" / "moderation.md"
    if moderationsdatei.is_file():
        yield moderationsdatei, zeichen(moderationsdatei), moderation
    for datei in sorted((wurzel / akzeptanzOrdner).rglob("*Test.py")):
        yield datei, zeichen(datei), akzeptanztest
    yield from mockupFälle()
    for ordner in perspektiven:
        datei = wurzel / ordner / "CLAUDE.md"
        if datei.is_file():
            yield datei, zeichen(datei), ordnerClaude
    root = wurzel / "CLAUDE.md"
    yield root, zeichen(root) + zeichen(wurzel / "domaene" / "ziel.md"), rootClaudeMitZiel


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
