from dataclasses import dataclass
from fractions import Fraction

import pytest

from arbiter.domaene import messen
from arbiter.domaene.phasen.aufstellen import Aufstellung
from arbiter.domaene.spielobjekte import Modell, Stelle
from tests.akzeptanz.dienst import stelleImSpielstand
from tests.akzeptanz.handgriffe import (
    erwarteteStelle,
    modellZurEbeneMachen,
    stelleInDerZoneDesSpielersAnDerReihe,
    stellenAllerModelle,
    wegVon,
)

abstandBeimAnhalten = Fraction(1, 100)


def stelleAn(aufstellung: Aufstellung, ort: tuple[Fraction | int, Fraction | int]) -> Stelle:
    tiefe, länge = ort
    return stelleInDerZoneDesSpielersAnDerReihe(aufstellung, tiefe, länge)


def stellenAlsZahlen(aufstellung: Aufstellung) -> frozenset[tuple[float, float]]:
    return frozenset(
        stelleImSpielstand(stelle)
        for stelle in stellenAllerModelle(aufstellung).values()
        if stelle is not None
    )


def nichtAuswählen(aufstellung, einheit, modell): ...


mitUndOhneEbene = pytest.mark.parametrize(
    "ebeneLegen",
    [nichtAuswählen, modellZurEbeneMachen],
    ids=["nichtAusgewählt", "ebeneIstEinModell"],
)


def aufDerStrecke(stelle: Stelle, von: Stelle, nach: Stelle) -> bool:
    wegInX, wegInY = wegVon(von, nach)
    teilInX, teilInY = wegVon(von, stelle)
    kollinear = wegInX * teilInY == wegInY * teilInX
    skalarprodukt = wegInX * teilInX + wegInY * teilInY
    return kollinear and 0 <= skalarprodukt <= wegInX**2 + wegInY**2


def überdeckt(modell: Modell, stelle: Stelle, anderes: Modell, stelleDesAnderen: Stelle) -> bool:
    return messen.überdecken(modell.base, stelle, anderes.base, stelleDesAnderen)


def angehaltenVor(
    modell: Modell, stelle: Stelle, angestoßenes: Modell, stelleDesAngestoßenen: Stelle
) -> bool:
    return not überdeckt(
        modell, stelle, angestoßenes, stelleDesAngestoßenen
    ) and messen.abstandHöchstens(
        modell.base, stelle, angestoßenes.base, stelleDesAngestoßenen, abstandBeimAnhalten
    )


@dataclass(frozen=True)
class Zug:
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
