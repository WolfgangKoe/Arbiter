"""Kommentare und Freigabe des Stakeholders in Plan, Review und Retro, wie der Stand sie liest."""

import re
from pathlib import Path

from gemeinsam.gitAufruf import freigaben
from lesen.artefakt import Artefakt, artefakte, freigabeJa, istStakeholderKommentar, pfadDer
from lesen.plan import zyklus

stellungnahmeZeile = "Stellungnahme:"
freigabeAbschnitt = "Freigabe"
überschrift = re.compile(r"^## (.+)$")


def zeilenDer(wurzel: Path, artefakt: Artefakt) -> list[str]:
    datei = pfadDer(wurzel, artefakt)
    if not datei.is_file():
        return []
    return [zeile.strip() for zeile in datei.read_text(encoding="utf-8").splitlines()]


def abschnitte(zeilen: list[str]) -> list[tuple[str, list[str]]]:
    """Paare (Überschrift, Zeilen), in Reihenfolge der Datei, auch bei wiederholter Überschrift."""
    gefunden: list[tuple[str, list[str]]] = []
    for zeile in zeilen:
        treffer = überschrift.match(zeile)
        if treffer:
            gefunden.append((treffer[1], []))
        elif gefunden:
            gefunden[-1][1].append(zeile)
    return gefunden


def freigabeZeilen(zeilen: list[str]) -> list[str]:
    """Die Zeilen unter `## Freigabe`; nur dort steht das Feld."""
    return [
        zeile
        for titel, inhalt in abschnitte(zeilen)
        if titel == freigabeAbschnitt
        for zeile in inhalt
    ]


def freigegebenerZyklus(wurzel: Path, artefakt: Artefakt) -> int | None:
    """Der Zyklus der Datei, wenn `## Freigabe` `Freigabe: ja` trägt, sonst `None`."""
    if freigabeJa not in freigabeZeilen(zeilenDer(wurzel, artefakt)):
        return None
    return zyklus(pfadDer(wurzel, artefakt))


def hatKommentarOhneStellungnahme(zeilen: list[str]) -> bool:
    """Ein Kommentar des Stakeholders, auf den keine `Stellungnahme:` folgt."""
    for nummer, zeile in enumerate(zeilen):
        if not istStakeholderKommentar(zeile):
            continue
        folgende = [spätere for spätere in zeilen[nummer + 1 :] if spätere]
        if not folgende or not folgende[0].startswith(stellungnahmeZeile):
            return True
    return False


def autorenDran(wurzel: Path) -> dict[str, list[str]]:
    """Autor → Dateien mit einem Kommentar ohne Stellungnahme."""
    dran: dict[str, list[str]] = {}
    for artefakt in artefakte:
        if hatKommentarOhneStellungnahme(zeilenDer(wurzel, artefakt)):
            dran.setdefault(artefakt.autor, []).append(artefakt.datei)
    return dran


def freigabeZuCommitten(wurzel: Path) -> str | None:
    """Der Commit-Betreff `Freigabe <Gegenstand> <n>`, wenn die Datei `Freigabe: ja` trägt."""
    vorhanden = {betreff for _, betreff in freigaben(wurzel)}
    for artefakt in artefakte:
        nummer = freigegebenerZyklus(wurzel, artefakt)
        betreff = f"Freigabe {artefakt.gegenstand} {nummer}"
        if nummer is not None and betreff not in vorhanden:
            return betreff
    return None
