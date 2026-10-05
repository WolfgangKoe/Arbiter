"""Die Artefakte Plan, Review und Retro mit Pfad und den Zeilen, die der Stakeholder setzt."""

from pathlib import Path
from typing import NamedTuple

from gemeinsam.pfade import handoffOrdner
from lesen.plan import planDatei


class Artefakt(NamedTuple):
    datei: str
    gegenstand: str
    autor: str


artefakte = (
    Artefakt(planDatei.name, "Plan", "Planer"),
    Artefakt("review.md", "Review", "Reviewer"),
    Artefakt("retro.md", "Retro", "Organisationsentwickler"),
)

kommentarZeile = "Kommentar:"
freigabeJa = "Freigabe: ja"
freigabeOffen = "Freigabe: offen"


def artefaktVon(gegenstand: str) -> Artefakt:
    return next(artefakt for artefakt in artefakte if artefakt.gegenstand == gegenstand)


def pfadDer(wurzel: Path, artefakt: Artefakt) -> Path:
    return wurzel / handoffOrdner / artefakt.datei


def istStakeholderKommentar(zeile: str) -> bool:
    """Eine Zeile `Kommentar:` mit anderem Text als `.`; sie gehört dem Stakeholder."""
    return zeile.startswith(kommentarZeile) and zeile.removeprefix(kommentarZeile).strip() not in (
        "",
        ".",
    )
