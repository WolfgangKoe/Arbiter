"""Anhalten der Akzeptanztests: Züge zum Anhalten aufbauen und prüfen."""

from dataclasses import dataclass
from fractions import Fraction

from arbiter.domaene.phasen.aufstellen import Aufstellung
from arbiter.domaene.spielobjekte import Einheit, Modell, Stelle
from tests.akzeptanz.dienst import stelleImSpielstand
from tests.akzeptanz.handgriffe import (
    erwarteteStelle,
    stellenAllerModelle,
)


def ebeneAufDasModellLegen(aufstellung: Aufstellung, einheit: Einheit, modell: Modell) -> None:
    aufstellung.auswählen(einheit)
    aufstellung.ebeneWählen(modell)


def stellenAlsZahlen(aufstellung: Aufstellung) -> frozenset[tuple[float, float]]:
    """Die Stellen aller gesetzten Modelle beider Spieler, wie JSON und Seite sie nennen."""
    return frozenset(
        stelleImSpielstand(stelle)
        for stelle in stellenAllerModelle(aufstellung).values()
        if stelle is not None
    )


@dataclass(frozen=True)
class Zug:
    """Orte als Tiefe und Länge je in (Zoll, Radien): Start, Loslassen, Base im Weg, Ende."""

    start: tuple
    loslassen: tuple
    hindernis: tuple
    streckenende: tuple


freiesZiel = Zug(
    start=((4, 0), (20, 0)),
    loslassen=((4, 0), (25, 0)),
    hindernis=((4, 0), (30, 0)),
    streckenende=((4, 0), (25, 0)),
)
hineinrückenOhneBase = Zug(
    start=((4, 0), (20, 0)),
    loslassen=((12, 0), (20, 0)),
    hindernis=((4, 0), (40, 0)),
    streckenende=((9, -1), (20, 0)),
)


def stellenDesZugs(
    aufstellung: Aufstellung, radius: Fraction, zug: Zug
) -> tuple[Stelle, Stelle, Stelle, Stelle]:
    orte = (zug.start, zug.loslassen, zug.hindernis, zug.streckenende)
    davor, loslassen, hindernis, streckenende = (
        erwarteteStelle(aufstellung, radius, ort) for ort in orte
    )
    return davor, loslassen, hindernis, streckenende
