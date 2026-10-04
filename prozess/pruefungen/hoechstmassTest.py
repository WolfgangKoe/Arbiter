"""Höchstmaße in Zeichen für die Dateien im Repo; ein Verstoß sperrt den Commit."""

from pathlib import Path

import pytest

from agenten import kopfzeilen
from anliegen import antwortZeile
from pfade import akzeptanzOrdner, anliegenOrdner, etappenOrdner, perspektiven, wurzel

aktuelleEtappe = 1000
spätereEtappe = 200
agentendefinition = 2500
beschreibung = 150
rootClaudeMitZiel = 4000
ordnerClaude = 1500
anliegen = 4000
moderation = 4000
akzeptanztest = 20000
rollenordner = wurzel / ".claude" / "agents"


def zeichen(datei: Path) -> int:
    return len(datei.read_text(encoding="utf-8"))


def zeichenOhneAntworten(datei: Path) -> int:
    ersatz = "Antwort: ."
    zeilen = datei.read_text(encoding="utf-8").split("\n")
    return sum(len(ersatz if antwortZeile.match(zeile) else zeile) + 1 for zeile in zeilen) - 1


def fälle():
    etappen = sorted((wurzel / etappenOrdner).glob("*.md"))
    for nummer, datei in enumerate(etappen):
        grenze = aktuelleEtappe if nummer == 0 else spätereEtappe
        yield datei, zeichen(datei), grenze
    for datei in sorted((wurzel / ".claude" / "agents").glob("*.md")):
        yield datei, zeichen(datei), agentendefinition
    for datei in sorted((wurzel / anliegenOrdner).glob("*.md")):
        yield datei, zeichenOhneAntworten(datei), anliegen
    moderationsdatei = wurzel / "handoff" / "moderation.md"
    if moderationsdatei.is_file():
        yield moderationsdatei, zeichen(moderationsdatei), moderation
    for datei in sorted((wurzel / akzeptanzOrdner).rglob("*Test.py")):
        yield datei, zeichen(datei), akzeptanztest
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
