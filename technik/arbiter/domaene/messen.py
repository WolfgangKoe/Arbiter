"""Die drei Messungen der Phasen (technik/architektur.md, M1); gerechnet wird exakt."""

from fractions import Fraction

from arbiter.domaene.spielobjekte import Base, Stelle

# Regel: 1 Zoll sind 25,4 mm (domaene/glossar.md, Durchmesser)
_millimeterJeZoll = Fraction(254, 10)


def _radiusInZoll(base: Base) -> Fraction:
    return Fraction(base.durchmesser, 2) / _millimeterJeZoll


def _quadratDerMittelpunkte(ersteStelle: Stelle, zweiteStelle: Stelle) -> Fraction:
    return (ersteStelle.x - zweiteStelle.x) ** 2 + (ersteStelle.y - zweiteStelle.y) ** 2


def überdecken(
    ersteBase: Base, ersteStelle: Stelle, zweiteBase: Base, zweiteStelle: Stelle
) -> bool:
    radien = _radiusInZoll(ersteBase) + _radiusInZoll(zweiteBase)
    return _quadratDerMittelpunkte(ersteStelle, zweiteStelle) < radien**2


def abstandHöchstens(
    ersteBase: Base, ersteStelle: Stelle, zweiteBase: Base, zweiteStelle: Stelle, zoll: Fraction
) -> bool:
    reichweite = _radiusInZoll(ersteBase) + _radiusInZoll(zweiteBase) + zoll
    return _quadratDerMittelpunkte(ersteStelle, zweiteStelle) <= reichweite**2


def ganzIn(
    base: Base, stelle: Stelle, grenzenInX: tuple[Fraction, Fraction], länge: Fraction
) -> bool:
    """Die Fläche liegt zwischen den Grenzen in x und von 0 bis länge in y."""
    radius = _radiusInZoll(base)
    vonX, bisX = grenzenInX
    inX = vonX <= stelle.x - radius and stelle.x + radius <= bisX
    inY = radius <= stelle.y and stelle.y + radius <= länge
    return inX and inY
