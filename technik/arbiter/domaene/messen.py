"""Die Messungen der Phasen (technik/architektur.md, M1); gerechnet wird exakt."""

from bisect import bisect_left
from collections.abc import Collection
from fractions import Fraction
from math import ceil, floor

from arbiter.domaene.spielobjekte import Base, Stelle

_millimeterJeZoll = Fraction(254, 10)
_rasterJeZoll = 100

type BaseAnStelle = tuple[Base, Stelle]
type BasenAnStellen = Collection[BaseAnStelle]
type Weg = tuple[Fraction, Fraction]


def radiusInZoll(base: Base) -> Fraction:
    return Fraction(base.durchmesser, 2) / _millimeterJeZoll


def _quadratDerMittelpunkte(ersteStelle: Stelle, zweiteStelle: Stelle) -> Fraction:
    return (ersteStelle.x - zweiteStelle.x) ** 2 + (ersteStelle.y - zweiteStelle.y) ** 2


def überdecken(
    ersteBase: Base, ersteStelle: Stelle, zweiteBase: Base, zweiteStelle: Stelle
) -> bool:
    radien = radiusInZoll(ersteBase) + radiusInZoll(zweiteBase)
    return _quadratDerMittelpunkte(ersteStelle, zweiteStelle) < radien**2


def abstandHöchstens(
    ersteBase: Base, ersteStelle: Stelle, zweiteBase: Base, zweiteStelle: Stelle, zoll: Fraction
) -> bool:
    reichweite = radiusInZoll(ersteBase) + radiusInZoll(zweiteBase) + zoll
    return _quadratDerMittelpunkte(ersteStelle, zweiteStelle) <= reichweite**2


def ganzIn(
    base: Base,
    stelle: Stelle,
    grenzenInX: tuple[Fraction, Fraction],
    grenzenInY: tuple[Fraction, Fraction],
) -> bool:
    radius = radiusInZoll(base)
    vonX, bisX = grenzenInX
    vonY, bisY = grenzenInY
    inX = vonX <= stelle.x - radius and stelle.x + radius <= bisX
    inY = vonY <= stelle.y - radius and stelle.y + radius <= bisY
    return inX and inY


def wegZwischen(von: Stelle, nach: Stelle) -> Weg:
    return nach.x - von.x, nach.y - von.y


def verschoben(stelle: Stelle, weg: Weg) -> Stelle:
    wegInX, wegInY = weg
    return Stelle(x=stelle.x + wegInX, y=stelle.y + wegInY)


def teilDesWegs(weg: Weg, anteil: Fraction) -> Weg:
    wegInX, wegInY = weg
    return wegInX * anteil, wegInY * anteil


def rückungInDieFläche(
    bases: BasenAnStellen,
    grenzenInX: tuple[Fraction, Fraction],
    grenzenInY: tuple[Fraction, Fraction],
) -> Weg:
    """Der kürzeste gemeinsame Weg in die Fläche, soweit die Bases zusammen hineinpassen."""
    mitRadius = [(radiusInZoll(base), stelle) for base, stelle in bases]
    rückungInX = _rückung(
        min(stelle.x - radius for radius, stelle in mitRadius),
        max(stelle.x + radius for radius, stelle in mitRadius),
        grenzenInX,
    )
    rückungInY = _rückung(
        min(stelle.y - radius for radius, stelle in mitRadius),
        max(stelle.y + radius for radius, stelle in mitRadius),
        grenzenInY,
    )
    return rückungInX, rückungInY


def _rückung(vorn: Fraction, hinten: Fraction, grenzen: tuple[Fraction, Fraction]) -> Fraction:
    """Zu weit vorn rückt hinein, zu weit hinten zurück; passt beides nicht, gilt vorn."""
    von, bis = grenzen
    return max(von - vorn, Fraction(0)) or min(bis - hinten, Fraction(0))


def _überdecktAm(bewegt: BaseAnStelle, ruhend: BaseAnStelle, weg: Weg, anteil: Fraction) -> bool:
    base, start = bewegt
    ruhendeBase, ort = ruhend
    stelle = verschoben(start, teilDesWegs(weg, anteil))
    return überdecken(base, stelle, ruhendeBase, ort)


def _ersterÜberdeckenderSchritt(
    bewegt: BaseAnStelle, ruhend: BaseAnStelle, weg: Weg, schritte: int
) -> int | None:
    """Erster Schritt mit Überdeckung; der Abstand fällt bis zum nächsten Punkt, dann steigt er."""
    _, start = bewegt
    _, ort = ruhend
    wegInX, wegInY = weg

    def überdecktBeiSchritt(schritt: int) -> bool:
        return _überdecktAm(bewegt, ruhend, weg, Fraction(schritt, schritte))

    anteilDesNächsten = -((start.x - ort.x) * wegInX + (start.y - ort.y) * wegInY) / (
        wegInX**2 + wegInY**2
    )
    davor = min(max(floor(anteilDesNächsten * schritte), 0), schritte)
    danach = min(davor + 1, schritte)
    if not überdecktBeiSchritt(davor):
        return danach if überdecktBeiSchritt(danach) else None
    return bisect_left(range(davor), x=True, key=überdecktBeiSchritt)


def anteilBisZurBerührung(
    bewegte: BasenAnStellen, hindernisse: BasenAnStellen, weg: Weg
) -> Fraction:
    """Der Anteil bis vor die erste Überdeckung auf dem Raster von S3; 1, wenn das Ende frei ist."""
    wegInX, wegInY = weg
    schritte = ceil(_rasterJeZoll * (abs(wegInX) + abs(wegInY)))
    if schritte == 0:
        return Fraction(1)
    paare = [(bewegt, hindernis) for bewegt in bewegte for hindernis in hindernisse]
    if not any(_überdecktAm(bewegt, hindernis, weg, Fraction(1)) for bewegt, hindernis in paare):
        return Fraction(1)
    erste = [
        _ersterÜberdeckenderSchritt(bewegt, hindernis, weg, schritte) for bewegt, hindernis in paare
    ]
    ersterÜberhaupt = min(schritt for schritt in erste if schritt is not None)
    return Fraction(max(ersterÜberhaupt - 1, 0), schritte)
