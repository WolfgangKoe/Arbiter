"""Prüft die Dateien in domaene/mockups/ auf Kommentare, eigene Stile und Skripte."""

from pathlib import Path

from pfade import mockupOrdner, wurzel

verboteneInHtml = ("<!--", "<script", "<style")
verbotenesAttribut = "style="
verbotenInCss = "/*"


def htmlVerstöße(text: str) -> list[str]:
    kleinText = text.lower()
    gefunden = [muster for muster in verboteneInHtml if muster in kleinText]
    if verbotenesAttribut in kleinText.replace(" ", ""):
        gefunden.append(verbotenesAttribut)
    return gefunden


def cssVerstöße(text: str) -> list[str]:
    return [verbotenInCss] if verbotenInCss in text else []


def dateiVerstöße(datei: Path) -> list[str]:
    text = datei.read_text(encoding="utf-8")
    if datei.suffix == ".html":
        gefunden = htmlVerstöße(text)
    elif datei.suffix == ".css":
        gefunden = cssVerstöße(text)
    else:
        gefunden = []
    return [f"{datei.name}: {muster}" for muster in gefunden]


def verstöße(wurzelOrdner: Path = wurzel) -> list[str]:
    ordner = wurzelOrdner / mockupOrdner
    if not ordner.is_dir():
        return []
    ergebnis: list[str] = []
    for datei in sorted(ordner.rglob("*")):
        if datei.is_file():
            ergebnis += dateiVerstöße(datei)
    return ergebnis
