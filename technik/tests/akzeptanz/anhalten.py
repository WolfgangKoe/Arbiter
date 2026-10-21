"""Anhalten der Akzeptanztests: Züge zum Anhalten aufbauen und prüfen."""

from collections.abc import Iterable
from dataclasses import dataclass
from fractions import Fraction
from math import hypot

from arbiter.domaene.messen import abstandHöchstens, überdecken
from arbiter.domaene.phasen.aufstellen import Aufstellung
from arbiter.domaene.spielobjekte import Einheit, Modell, Stelle
from tests.akzeptanz.dienst import stelleImSpielstand
from tests.akzeptanz.handgriffe import (
    abstandDerReihen,
    erwarteteStelle,
    gezogenesUndRest,
    modelleAnStellenSetzen,
    radiusInZoll,
    stelleInDerZoneDesSpielersAnDerReihe,
    stellenAllerModelle,
    tiefeDerErstenReihe,
)

# Regel: architektur.md, S3, der Halt liegt höchstens 1/100″ vor der Berührung
rasterweite = Fraction(1, 100)

Gesetzte = list[tuple[Modell, Stelle]]


def liegtAufDerStrecke(von: Stelle, bis: Stelle, stelle: Stelle) -> bool:
    """Exakt kollinear und zwischen den Enden, einschließlich der Enden."""
    wegInX, wegInY = bis.x - von.x, bis.y - von.y
    versatzInX, versatzInY = stelle.x - von.x, stelle.y - von.y
    kollinear = wegInX * versatzInY == wegInY * versatzInX
    anteil = versatzInX * wegInX + versatzInY * wegInY
    return kollinear and 0 <= anteil <= wegInX**2 + wegInY**2


def liegtNahAnDerStrecke(von: Stelle, bis: Stelle, stelle: Stelle, toleranz: float) -> bool:
    """Die Stelle ist höchstens `toleranz` Zoll von der Strecke entfernt, Enden eingeschlossen."""
    wegInX, wegInY = float(bis.x - von.x), float(bis.y - von.y)
    versatzInX, versatzInY = float(stelle.x - von.x), float(stelle.y - von.y)
    anteil = (versatzInX * wegInX + versatzInY * wegInY) / (wegInX**2 + wegInY**2)
    amFußpunkt = min(max(anteil, 0), 1)
    return hypot(versatzInX - amFußpunkt * wegInX, versatzInY - amFußpunkt * wegInY) <= toleranz


def überdecktEine(gruppe: Gesetzte, andere: Gesetzte) -> bool:
    return any(
        überdecken(modell.base, stelle, anderes.base, ort)
        for modell, stelle in gruppe
        for anderes, ort in andere
    )


def stößtAn(gruppe: Gesetzte, andere: Gesetzte) -> bool:
    """Eine Base der Gruppe ist höchstens 1/100″ von einer der anderen entfernt."""
    return any(
        abstandHöchstens(modell.base, stelle, anderes.base, ort, rasterweite)
        for modell, stelle in gruppe
        for anderes, ort in andere
    )


def gesetzteMit(aufstellung: Aufstellung, modelle: Iterable[Modell]) -> Gesetzte:
    return [(modell, aufstellung.stelle(modell)) for modell in modelle]


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
class Blockzug:
    """Ein Block, dessen Zug vor eine Base einer anderen Einheit führt."""

    gesetzte: Gesetzte
    gezogenes: Modell
    davor: Stelle
    ziel: Stelle


tiefeDerFremdenBase = tiefeDerErstenReihe + abstandDerReihen


def blockVorEinerFremdenBase(
    aufstellung: Aufstellung,
    einheit: Einheit,
    fremdesModell: Modell,
    *,
    zweitesGetroffen: bool,
    zweitesGezogen: bool,
) -> Blockzug:
    """Setzt die zwei Modelle der Einheit und zieht eines so, dass nur ein Modell trifft."""
    erstes, _ = einheit.modelle
    radius = radiusInZoll(erstes)
    fremdeLänge = aufstellung.stelle(fremdesModell).y
    # Warum: Das getroffene Modell steht auf der Länge der fremden Base, das andere daneben
    längen = (fremdeLänge + 2 * radius, fremdeLänge)
    längen = längen if zweitesGetroffen else tuple(reversed(längen))
    stellen = [stelleInDerZoneDesSpielersAnDerReihe(aufstellung, 8, länge) for länge in längen]
    gesetzte = modelleAnStellenSetzen(aufstellung, einheit, stellen)
    aufstellung.auswählen(einheit)
    (gezogenes, davor), _ = gezogenesUndRest(gesetzte, zweitesGezogen=zweitesGezogen)
    # Warum: Die fremde Base steht in der zweiten Reihe, das Ziel nur 0,5″ tiefer davor
    tiefeDesZiels = tiefeDerFremdenBase + Fraction(1, 2)
    ziel = stelleInDerZoneDesSpielersAnDerReihe(aufstellung, tiefeDesZiels, davor.y)
    return Blockzug(gesetzte, gezogenes, davor, ziel)


@dataclass(frozen=True)
class Zug:
    """Orte als Tiefe und Länge je in (Zoll, Radien): Start, Loslassen, Base im Weg, Ende."""

    start: tuple
    loslassen: tuple
    hindernis: tuple
    streckenende: tuple


# Warum: Das Ziel überdeckt die Base im Weg, der Weg liegt gerade entlang der Länge
geradeAufDieBase = Zug(
    start=((4, 0), (20, 0)),
    loslassen=((4, 0), (31, 0)),
    hindernis=((4, 0), (30, 0)),
    streckenende=((4, 0), (31, 0)),
)
# Warum: 3-4-5 hält den Weg schräg und exakt, die Base liegt 5″ vom Start, das Ziel 5,5″
schrägAufDieBase = Zug(
    start=((7, 0), (20, 0)),
    loslassen=((Fraction(37, 10), 0), (Fraction(244, 10), 0)),
    hindernis=((4, 0), (24, 0)),
    streckenende=((Fraction(37, 10), 0), (Fraction(244, 10), 0)),
)
# Warum: AUF-26.1 rückt das Ziel zuerst in die Zone, dort liegt die Base im Weg
anDerHineingerücktenStelle = Zug(
    start=((4, 0), (20, 0)),
    loslassen=((12, 0), (20, 0)),
    hindernis=((9, -1), (20, 0)),
    streckenende=((9, -1), (20, 0)),
)
# Warum: Das Ziel liegt schräg jenseits der Innenkante, die Strecke geht zur hineingerückten
schrägÜberDieGrenze = Zug(
    start=((4, 0), (20, 0)),
    loslassen=((12, 0), (26, 0)),
    hindernis=((9, -1), (26, 0)),
    streckenende=((9, -1), (26, 0)),
)
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
