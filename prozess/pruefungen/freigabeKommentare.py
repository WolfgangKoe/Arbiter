"""Kommentare und Freigabe des Stakeholders in Plan, Review und Retro, wie der Stand sie liest."""

from pathlib import Path
from typing import NamedTuple

from gitAufruf import freigabeCommit
from plan import zyklus


class Artefakt(NamedTuple):
    datei: str
    gegenstand: str
    autor: str


artefakte = (
    Artefakt("plan.md", "Plan", "Planer"),
    Artefakt("review.md", "Review", "Reviewer"),
    Artefakt("retro.md", "Retro", "Organisationsentwickler"),
)
kommentarZeile = "Kommentar:"
stellungnahmeZeile = "Stellungnahme:"
freigabeJa = "Freigabe: ja"


def zeilenDer(wurzel: Path, artefakt: Artefakt) -> list[str]:
    datei = wurzel / "handoff" / artefakt.datei
    if not datei.is_file():
        return []
    return [zeile.strip() for zeile in datei.read_text(encoding="utf-8").splitlines()]


def hatKommentarOhneStellungnahme(zeilen: list[str]) -> bool:
    """Eine Zeile `Kommentar:` mit anderem Text als `.`, auf die keine `Stellungnahme:` folgt."""
    for nummer, zeile in enumerate(zeilen):
        text = zeile.removeprefix(kommentarZeile).strip()
        if not zeile.startswith(kommentarZeile) or text in ("", "."):
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
    for artefakt in artefakte:
        nummer = zyklus(wurzel / "handoff" / artefakt.datei)
        if nummer is None or freigabeJa not in zeilenDer(wurzel, artefakt):
            continue
        if freigabeCommit(wurzel, artefakt.gegenstand, nummer) is None:
            return f"Freigabe {artefakt.gegenstand} {nummer}"
    return None
