"""Format von Plan, Review und Retro bis zur Freigabe: Abschnitt `## Freigabe`."""

import re
from pathlib import Path

from gemeinsam.gitAufruf import freigabeCommit
from standregeln.freigabeKommentare import (
    Artefakt,
    abschnitte,
    artefakte,
    artefaktVon,
    freigabeAbschnitt,
    freigabeZeilen,
    pfadDer,
    zeilenDer,
)
from standregeln.plan import zyklus

freigabeFeld = re.compile(r"^Freigabe: (offen|ja)$")
vorgehenAbschnitt = "Nächstes Vorgehen"
vorgehenPunkte = ("Produktziel", "Etappenziel", "Zyklusziel")


def vorgehenVerstoß(teile: list[tuple[str, list[str]]]) -> str | None:
    texte = ["\n".join(inhalt) for titel, inhalt in teile if titel == vorgehenAbschnitt]
    if not texte:
        return f"Abschnitt `## {vorgehenAbschnitt}` fehlt"
    fehlend = [punkt for punkt in vorgehenPunkte if punkt not in texte[0]]
    return f"{vorgehenAbschnitt}: {', '.join(fehlend)} fehlt" if fehlend else None


def formatVerstoß(zeilen: list[str], artefakt: Artefakt) -> str | None:
    teile = abschnitte(zeilen)
    if [titel for titel, _ in teile][-1:] != [freigabeAbschnitt]:
        return "endet nicht mit `## Freigabe`"
    felder = [zeile for zeile in freigabeZeilen(zeilen) if zeile.startswith("Freigabe:")]
    if len(felder) != 1 or not freigabeFeld.match(felder[0]):
        return "`## Freigabe` braucht genau eine Zeile `Freigabe: offen` oder `Freigabe: ja`"
    return vorgehenVerstoß(teile) if artefakt.gegenstand == "Review" else None


def ungeprüft(wurzel: Path, artefakt: Artefakt, nummer: int) -> bool:
    """Mit Freigabe-Commit, oder ein Review, zu dem die Retro schon vorliegt."""
    if freigabeCommit(wurzel, artefakt.gegenstand, nummer) is not None:
        return True
    retro = zyklus(pfadDer(wurzel, artefaktVon("Retro")))
    return artefakt.gegenstand == "Review" and retro == nummer


def verstöße(wurzel: Path) -> list[str]:
    meldungen = []
    for artefakt in artefakte:
        nummer = zyklus(pfadDer(wurzel, artefakt))
        if nummer is None or ungeprüft(wurzel, artefakt, nummer):
            continue
        grund = formatVerstoß(zeilenDer(wurzel, artefakt), artefakt)
        if grund:
            meldungen.append(f"handoff/{artefakt.datei}: {grund}")
    return meldungen
