import math
from fractions import Fraction
from typing import NamedTuple

from arbiter.domaene.spielobjekte import Modell, Stelle
from tests.akzeptanz.anhalten import überdeckt
from tests.akzeptanz.handgriffe import millionstel, versetzt, wegVon
from tests.akzeptanz.schlacht import (
    abstandImQuadrat,
    abständeZuDenSpielfeldkanten,
    hundertstelZoll,
    summeDerRadien,
)


def frei(modell: Modell, stelle: Stelle, anderes: Modell, stelleDesAnderen: Stelle) -> bool:
    return not überdeckt(modell, stelle, anderes, stelleDesAnderen)


def höchstensUmHundertstelWeiter(punkt: Stelle, stelle: Stelle, kürzesterWeg: Fraction) -> bool:
    return abstandImQuadrat(punkt, stelle) <= (kürzesterWeg + hundertstelZoll) ** 2


def wurzelAufgerundet(quadrat: Fraction) -> Fraction:
    return Fraction(math.sqrt(quadrat)) + millionstel


def ganzImSpielfeld(stelle: Stelle, modell: Modell) -> bool:
    return all(abstand >= 0 for abstand in abständeZuDenSpielfeldkanten(stelle, modell))


class Kreis(NamedTuple):
    mitte: Stelle
    radius: Fraction


def schnittpunkte(kreis: Kreis, andererKreis: Kreis) -> tuple[Stelle, ...]:
    abstandImQuadratDerMitten = abstandImQuadrat(kreis.mitte, andererKreis.mitte)
    abstand = math.sqrt(abstandImQuadratDerMitten)
    entlang = float(kreis.radius**2 - andererKreis.radius**2 + abstandImQuadratDerMitten) / (
        2 * abstand
    )
    quer = math.sqrt(kreis.radius**2 - entlang**2)
    wegInX, wegInY = (float(teil) / abstand for teil in wegVon(kreis.mitte, andererKreis.mitte))
    return tuple(
        versetzt(
            kreis.mitte,
            (
                Fraction(entlang * wegInX - seite * quer * wegInY),
                Fraction(entlang * wegInY + seite * quer * wegInX),
            ),
        )
        for seite in (1, -1)
    )


def wegZumNächstenSchnitt(punkt: Stelle, kreis: Kreis, andererKreis: Kreis) -> Fraction:
    return wurzelAufgerundet(
        min(abstandImQuadrat(punkt, schnitt) for schnitt in schnittpunkte(kreis, andererKreis))
    )


def randDerNahkampfreichweite(modell: Modell, stelleDesAnderen: Stelle, anderes: Modell) -> Kreis:
    return Kreis(stelleDesAnderen, summeDerRadien(modell, anderes) + 1)
