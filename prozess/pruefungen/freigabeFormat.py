"""Format von Plan, Review und Retro bis zur Freigabe: Abschnitt `## Freigabe`."""

import re
from pathlib import Path

from freigabeKommentare import Artefakt, artefakte, zeilenDer
from gitAufruf import freigabeCommit
from plan import zyklus

abschnitt = re.compile(r"^## (.+)$")
freigabeFeld = re.compile(r"^Freigabe: (offen|ja)$")
vorgehenAbschnitt = "Nächstes Vorgehen"
vorgehenPunkte = ("Produktziel", "Etappenziel", "Zyklusziel")


def abschnitte(zeilen: list[str]) -> dict[str, list[str]]:
    """Überschrift → Zeilen des Abschnitts, in Reihenfolge der Datei."""
    gefunden: dict[str, list[str]] = {}
    aktuell = None
    for zeile in zeilen:
        treffer = abschnitt.match(zeile)
        if treffer:
            aktuell = treffer[1]
            gefunden[aktuell] = []
        elif aktuell is not None:
            gefunden[aktuell].append(zeile)
    return gefunden


def vorgehenVerstoß(teile: dict[str, list[str]]) -> str | None:
    text = "\n".join(teile.get(vorgehenAbschnitt, []))
    fehlend = [punkt for punkt in vorgehenPunkte if punkt not in text]
    if vorgehenAbschnitt not in teile:
        return f"Abschnitt `## {vorgehenAbschnitt}` fehlt"
    if list(teile).index(vorgehenAbschnitt) > list(teile).index("Freigabe"):
        return f"`## {vorgehenAbschnitt}` steht nach `## Freigabe`"
    return f"{vorgehenAbschnitt}: {', '.join(fehlend)} fehlt" if fehlend else None


def formatVerstoß(zeilen: list[str], artefakt: Artefakt) -> str | None:
    teile = abschnitte(zeilen)
    if list(teile)[-1:] != ["Freigabe"]:
        return "endet nicht mit `## Freigabe`"
    felder = [zeile for zeile in teile["Freigabe"] if zeile.startswith("Freigabe:")]
    if len(felder) != 1 or not freigabeFeld.match(felder[0]):
        return "`## Freigabe` braucht genau eine Zeile `Freigabe: offen` oder `Freigabe: ja`"
    return vorgehenVerstoß(teile) if artefakt.gegenstand == "Review" else None


def ungeprüft(wurzel: Path, artefakt: Artefakt, nummer: int) -> bool:
    """Mit Freigabe-Commit, oder ein Review, zu dem die Retro schon vorliegt."""
    if freigabeCommit(wurzel, artefakt.gegenstand, nummer) is not None:
        return True
    retro = zyklus(wurzel / "handoff" / "retro.md")
    return artefakt.gegenstand == "Review" and retro == nummer


def verstöße(wurzel: Path) -> list[str]:
    meldungen = []
    for artefakt in artefakte:
        nummer = zyklus(wurzel / "handoff" / artefakt.datei)
        if nummer is None or ungeprüft(wurzel, artefakt, nummer):
            continue
        grund = formatVerstoß(zeilenDer(wurzel, artefakt), artefakt)
        if grund:
            meldungen.append(f"handoff/{artefakt.datei}: {grund}")
    return meldungen
