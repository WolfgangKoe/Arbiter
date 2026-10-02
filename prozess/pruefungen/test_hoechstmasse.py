"""Höchstmaße in Zeichen für die Dateien im Repo; ein Verstoß sperrt den Commit."""

from pathlib import Path

import pytest

from agenten import kopfzeilen

WURZEL = Path(__file__).resolve().parents[2]

AKTUELLE_ETAPPE = 1000
SPAETERE_ETAPPE = 200
AGENTENDEFINITION = 2500
BESCHREIBUNG = 150
ROOT_CLAUDE_MIT_ZIEL = 4000
ORDNER_CLAUDE = 1500
ANLIEGEN = 2400


def zeichen(datei: Path) -> int:
    return len(datei.read_text(encoding="utf-8"))


def faelle():
    etappen = sorted((WURZEL / "domaene" / "etappen").glob("*.md"))
    for nummer, datei in enumerate(etappen):
        grenze = AKTUELLE_ETAPPE if nummer == 0 else SPAETERE_ETAPPE
        yield datei, zeichen(datei), grenze
    for datei in sorted((WURZEL / ".claude" / "agents").glob("*.md")):
        yield datei, zeichen(datei), AGENTENDEFINITION
    for datei in sorted((WURZEL / "handoff" / "anliegen").glob("*.md")):
        yield datei, zeichen(datei), ANLIEGEN
    for ordner in ("domaene", "technik", "prozess"):
        datei = WURZEL / ordner / "CLAUDE.md"
        if datei.is_file():
            yield datei, zeichen(datei), ORDNER_CLAUDE
    root = WURZEL / "CLAUDE.md"
    yield root, zeichen(root) + zeichen(WURZEL / "domaene" / "ziel.md"), ROOT_CLAUDE_MIT_ZIEL


@pytest.mark.parametrize(
    "datei, laenge, grenze",
    [pytest.param(*fall, id=str(fall[0].relative_to(WURZEL))) for fall in faelle()],
)
def test_datei_haelt_ihr_hoechstmass(datei, laenge, grenze):
    assert laenge <= grenze, f"{datei.relative_to(WURZEL)}: {laenge} Zeichen, höchstens {grenze}"


@pytest.mark.parametrize(
    "datei",
    [pytest.param(d, id=d.stem) for d in sorted((WURZEL / ".claude" / "agents").glob("*.md"))],
)
def test_beschreibung_einer_rolle_ist_kurz(datei):
    zeile = next(z for z in kopfzeilen(datei.stem, WURZEL) if z.startswith("description:"))
    beschreibung = zeile.removeprefix("description:").strip()
    assert len(beschreibung) <= BESCHREIBUNG, f"{datei.stem}: {len(beschreibung)} Zeichen"
