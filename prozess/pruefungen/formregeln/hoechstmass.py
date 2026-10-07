"""Höchstmaße in Zeichen für die Dateien im Repo und die Zählung dazu."""

import re
from pathlib import Path

from anliegenregeln.antworten import antwortZeile
from formregeln.mockups import istMockupDatei
from gemeinsam.pfade import (
    akzeptanzOrdner,
    anliegenOrdner,
    etappenOrdner,
    handoffOrdner,
    mockupOrdner,
    perspektiven,
    wurzel,
)
from lesen.artefakt import artefakte, kommentarZeile, pfadDer

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
architekturDatei = 6000
architekturGesamt = 24000
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
        if datei.is_file() and istMockupDatei(datei):
            yield datei, zeichen(datei), mockup


def architekturDateien(ordner: Path = wurzel) -> list[Path]:
    übersicht = ordner / "technik" / "architektur.md"
    themen = sorted((ordner / "technik" / "architektur").glob("*.md"))
    return ([übersicht] if übersicht.is_file() else []) + themen


def architekturFälle():
    for datei in architekturDateien():
        yield datei, zeichen(datei), architekturDatei


def fälle():
    etappen = sorted((wurzel / etappenOrdner).glob("*.md"))
    for nummer, datei in enumerate(etappen):
        grenze = aktuelleEtappe if nummer == 0 else spätereEtappe
        yield datei, zeichen(datei), grenze
    for datei in sorted(rollenordner.glob("*.md")):
        yield datei, zeichen(datei), agentendefinition
    for datei in sorted((wurzel / anliegenOrdner).glob("*.md")):
        yield datei, zeichenOhneAntworten(datei), anliegen
    for artefakt in artefakte:
        datei = pfadDer(wurzel, artefakt)
        if datei.is_file():
            yield datei, zeichenOhneKommentare(datei), freigabeDatei
    moderationsdatei = wurzel / handoffOrdner / "moderation.md"
    if moderationsdatei.is_file():
        yield moderationsdatei, zeichen(moderationsdatei), moderation
    for datei in sorted((wurzel / akzeptanzOrdner).rglob("*Test.py")):
        yield datei, zeichen(datei), akzeptanztest
    yield from mockupFälle()
    yield from architekturFälle()
    for ordner in perspektiven:
        datei = wurzel / ordner / "CLAUDE.md"
        if datei.is_file():
            yield datei, zeichen(datei), ordnerClaude
    root = wurzel / "CLAUDE.md"
    yield root, zeichen(root) + zeichen(wurzel / "domaene" / "ziel.md"), rootClaudeMitZiel


def architekturSumme(ordner: Path = wurzel) -> int:
    return sum(zeichen(datei) for datei in architekturDateien(ordner))
