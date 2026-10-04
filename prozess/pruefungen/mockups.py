"""Prüft die Dateien in domaene/mockups/ auf Kommentare, eigene Stile und Skripte."""

import re
from pathlib import Path

from pfade import mockupOrdner, wurzel

verboteneInHtml = ("<!--", "<script", "<style")
verbotenesAttribut = re.compile(r"<[^>]*\sstyle\s*=", re.IGNORECASE)
erlaubteEndungen = (".html", ".css")
verbotenInCss = "/*"


def htmlVerstöße(text: str) -> list[str]:
    kleinText = text.lower()
    gefunden = [muster for muster in verboteneInHtml if muster in kleinText]
    if verbotenesAttribut.search(text):
        gefunden.append("style=")
    return gefunden


def cssVerstöße(text: str) -> list[str]:
    return [verbotenInCss] if verbotenInCss in text else []


def istMockupDatei(datei: Path) -> bool:
    return datei.suffix.lower() in erlaubteEndungen


def dateiVerstöße(datei: Path) -> list[str]:
    if not istMockupDatei(datei):
        return ["nur .html und .css"]
    text = datei.read_text(encoding="utf-8")
    if datei.suffix.lower() == ".html":
        return htmlVerstöße(text)
    return cssVerstöße(text)


def verstöße(wurzelOrdner: Path = wurzel) -> list[str]:
    ordner = wurzelOrdner / mockupOrdner
    if not ordner.is_dir():
        return []
    ergebnis: list[str] = []
    for datei in sorted(ordner.rglob("*")):
        if datei.is_file():
            name = datei.relative_to(wurzelOrdner).as_posix()
            ergebnis += [f"{name}: {grund}" for grund in dateiVerstöße(datei)]
    return ergebnis
