from bisect import bisect_left
from collections.abc import Callable, Collection, Iterable
from dataclasses import dataclass
from fractions import Fraction
from itertools import combinations
from math import ceil, cos, floor, hypot, pi, sin, sqrt

from arbiter.domaene.spielobjekte import Base, Stelle

_millimeterJeZoll = Fraction(254, 10)
_rasterJeZoll = 100
_toleranz = 1e-6
_nenner = 10**6
_abständeUmDenKandidaten = (1 / 2000, 1 / 1000, 1 / 500, 1 / 250)
_richtungenUmDenKandidaten = 16

type BaseAnStelle = tuple[Base, Stelle]
type BasenAnStellen = Collection[BaseAnStelle]
type Weg = tuple[Fraction, Fraction]
type Berührung = Callable[[Base, Stelle, Base, Stelle], bool]
type Punkt = tuple[float, float]


@dataclass(frozen=True)
class Kreisrand:
    mitte: Punkt
    radius: float
    darin: bool


@dataclass(frozen=True)
class Geradenrand:
    inX: bool
    wert: float
    aufwärts: bool


type Rand = Kreisrand | Geradenrand


def radiusInZoll(base: Base) -> Fraction:
    return Fraction(base.durchmesser, 2) / _millimeterJeZoll


def abstandImQuadrat(ersteStelle: Stelle, zweiteStelle: Stelle) -> Fraction:
    return (ersteStelle.x - zweiteStelle.x) ** 2 + (ersteStelle.y - zweiteStelle.y) ** 2


def überdecken(
    ersteBase: Base, ersteStelle: Stelle, zweiteBase: Base, zweiteStelle: Stelle
) -> bool:
    radien = radiusInZoll(ersteBase) + radiusInZoll(zweiteBase)
    return abstandImQuadrat(ersteStelle, zweiteStelle) < radien**2


def abstandHöchstens(
    ersteBase: Base, ersteStelle: Stelle, zweiteBase: Base, zweiteStelle: Stelle, zoll: Fraction
) -> bool:
    reichweite = radiusInZoll(ersteBase) + radiusInZoll(zweiteBase) + zoll
    return abstandImQuadrat(ersteStelle, zweiteStelle) <= reichweite**2


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
    von, bis = grenzen
    return max(von - vorn, Fraction(0)) or min(bis - hinten, Fraction(0))


def _berührtAm(
    bewegt: BaseAnStelle,
    ruhend: BaseAnStelle,
    weg: Weg,
    anteil: Fraction,
    berührt: Berührung,
) -> bool:
    base, start = bewegt
    ruhendeBase, ort = ruhend
    stelle = verschoben(start, teilDesWegs(weg, anteil))
    return berührt(base, stelle, ruhendeBase, ort)


def _anteilDesNächstenPunkts(von: Stelle, weg: Weg, ort: Stelle) -> Fraction:
    wegInX, wegInY = weg
    return ((ort.x - von.x) * wegInX + (ort.y - von.y) * wegInY) / (wegInX**2 + wegInY**2)


def ersterSchrittMit(trifftMonotonAb: Callable[[int], bool], bis: int) -> int:
    return bisect_left(range(bis), x=True, key=trifftMonotonAb)


def _ersterBerührenderSchritt(
    bewegt: BaseAnStelle, ruhend: BaseAnStelle, weg: Weg, schritte: int, berührt: Berührung
) -> int | None:
    _, start = bewegt
    _, ort = ruhend

    def berührtBeiSchritt(schritt: int) -> bool:
        return _berührtAm(bewegt, ruhend, weg, Fraction(schritt, schritte), berührt)

    davor = min(max(floor(_anteilDesNächstenPunkts(start, weg, ort) * schritte), 0), schritte)
    danach = min(davor + 1, schritte)
    if not berührtBeiSchritt(davor):
        return danach if berührtBeiSchritt(danach) else None
    return ersterSchrittMit(berührtBeiSchritt, davor)


def schritteDesWegs(weg: Weg) -> int:
    wegInX, wegInY = weg
    return ceil(_rasterJeZoll * (abs(wegInX) + abs(wegInY)))


def anteilVorDemErstenSchrittMit(trifftMonotonAb: Callable[[Fraction], bool], weg: Weg) -> Fraction:
    schritte = schritteDesWegs(weg)
    if schritte == 0 or not trifftMonotonAb(Fraction(1)):
        return Fraction(1)

    def trifftBeiSchritt(schritt: int) -> bool:
        return trifftMonotonAb(Fraction(schritt, schritte))

    erster = ersterSchrittMit(trifftBeiSchritt, schritte + 1)
    return Fraction(max(erster - 1, 0), schritte)


def anteilBisZurBerührungAufDemWeg(
    bewegte: BasenAnStellen,
    hindernisse: BasenAnStellen,
    weg: Weg,
    berührt: Berührung = überdecken,
) -> Fraction:
    schritte = schritteDesWegs(weg)
    if schritte == 0:
        return Fraction(1)
    paare = [(bewegt, hindernis) for bewegt in bewegte for hindernis in hindernisse]
    erste = [
        _ersterBerührenderSchritt(bewegt, hindernis, weg, schritte, berührt)
        for bewegt, hindernis in paare
    ]
    berührende = [schritt for schritt in erste if schritt is not None]
    if not berührende:
        return Fraction(1)
    return Fraction(max(min(berührende) - 1, 0), schritte)


def _ersterSchrittBis(
    paar: tuple[BaseAnStelle, BaseAnStelle],
    weg: Weg,
    schritte: int,
    schritt: int,
    berührt: Berührung,
) -> int | None:
    def berührtBeiSchritt(beiSchritt: int) -> bool:
        return _berührtAm(*paar, weg, Fraction(beiSchritt, schritte), berührt)

    return ersterSchrittMit(berührtBeiSchritt, schritt) if berührtBeiSchritt(schritt) else None


def anteilVorDerLetztenBerührung(
    bewegte: BasenAnStellen,
    hindernisse: BasenAnStellen,
    weg: Weg,
    bis: Fraction,
    berührt: Berührung = überdecken,
) -> Fraction:
    schritte = schritteDesWegs(weg)
    paare = [(bewegt, hindernis) for bewegt in bewegte for hindernis in hindernisse]
    if schritte == 0 or not any(_berührtAm(*paar, weg, bis, berührt) for paar in paare):
        return Fraction(1)
    schritt = floor(bis * schritte)
    while schritt >= 0:
        ersteSchritte = [_ersterSchrittBis(paar, weg, schritte, schritt, berührt) for paar in paare]
        berührende = [erster for erster in ersteSchritte if erster is not None]
        if not berührende:
            break
        schritt = min(berührende) - 1
    return Fraction(max(schritt, 0), schritte)


def _lotpunkte(rand: Rand) -> list[Punkt]:
    match rand:
        case Kreisrand(mitte=(mitteInX, mitteInY), radius=radius):
            abstand = hypot(mitteInX, mitteInY)
            if abstand == 0:
                return [(radius, 0.0), (-radius, 0.0), (0.0, radius), (0.0, -radius)]
            anteil = 1 - radius / abstand
            return [(mitteInX * anteil, mitteInY * anteil)]
        case Geradenrand(inX=True, wert=wert):
            return [(wert, 0.0)]
        case Geradenrand(wert=wert):
            return [(0.0, wert)]


def _kreisMitKreis(erster: Kreisrand, zweiter: Kreisrand) -> list[Punkt]:
    ersteMitteInX, ersteMitteInY = erster.mitte
    zweiteMitteInX, zweiteMitteInY = zweiter.mitte
    wegInX, wegInY = zweiteMitteInX - ersteMitteInX, zweiteMitteInY - ersteMitteInY
    abstand = hypot(wegInX, wegInY)
    if abstand == 0:
        return []
    entlang = (erster.radius**2 - zweiter.radius**2 + abstand**2) / (2 * abstand)
    querQuadrat = erster.radius**2 - entlang**2
    if querQuadrat < 0:
        return []
    quer = sqrt(querQuadrat)
    richtungInX, richtungInY = wegInX / abstand, wegInY / abstand
    fußInX, fußInY = ersteMitteInX + entlang * richtungInX, ersteMitteInY + entlang * richtungInY
    return [
        (fußInX - seite * quer * richtungInY, fußInY + seite * quer * richtungInX)
        for seite in (1, -1)
    ]


def _kreisMitGerade(kreis: Kreisrand, gerade: Geradenrand) -> list[Punkt]:
    mitteInX, mitteInY = kreis.mitte
    entlang, quer = (mitteInX, mitteInY) if gerade.inX else (mitteInY, mitteInX)
    rest = kreis.radius**2 - (gerade.wert - entlang) ** 2
    if rest < 0:
        return []
    halbe = sqrt(rest)
    if gerade.inX:
        return [(gerade.wert, quer + seite * halbe) for seite in (1, -1)]
    return [(quer + seite * halbe, gerade.wert) for seite in (1, -1)]


def _geradeMitGerade(erste: Geradenrand, zweite: Geradenrand) -> list[Punkt]:
    if erste.inX == zweite.inX:
        return []
    senkrechte, waagerechte = (erste, zweite) if erste.inX else (zweite, erste)
    return [(senkrechte.wert, waagerechte.wert)]


def _schnittpunkte(erster: Rand, zweiter: Rand) -> list[Punkt]:
    match erster, zweiter:
        case Kreisrand(), Kreisrand():
            return _kreisMitKreis(erster, zweiter)
        case Kreisrand(), Geradenrand():
            return _kreisMitGerade(erster, zweiter)
        case Geradenrand(), Kreisrand():
            return _kreisMitGerade(zweiter, erster)
        case Geradenrand(), Geradenrand():
            return _geradeMitGerade(erster, zweiter)


def _zulässig(punkt: Punkt, rand: Rand) -> bool:
    punktInX, punktInY = punkt
    match rand:
        case Kreisrand(mitte=(mitteInX, mitteInY), radius=radius, darin=darin):
            abstand = hypot(punktInX - mitteInX, punktInY - mitteInY)
            return abstand <= radius + _toleranz if darin else abstand >= radius - _toleranz
        case Geradenrand(inX=inX, wert=wert, aufwärts=aufwärts):
            hinter = (punktInX if inX else punktInY) - wert
            return (hinter if aufwärts else -hinter) >= -_toleranz


def _abstandZumUrsprung(rand: Rand) -> float:
    match rand:
        case Kreisrand(mitte=(mitteInX, mitteInY), radius=radius):
            return abs(hypot(mitteInX, mitteInY) - radius)
        case Geradenrand(wert=wert):
            return abs(wert)


def _länge(punkt: Punkt) -> float:
    return hypot(*punkt)


def _gerundet(zahl: float) -> Fraction:
    return Fraction(round(zahl * _nenner), _nenner)


def _umDenKandidaten(kandidat: Punkt) -> Iterable[Weg]:
    kandidatInX, kandidatInY = kandidat
    yield _gerundet(kandidatInX), _gerundet(kandidatInY)
    for abstand in _abständeUmDenKandidaten:
        for richtung in range(_richtungenUmDenKandidaten):
            winkel = 2 * pi * richtung / _richtungenUmDenKandidaten
            yield (
                _gerundet(kandidatInX + abstand * cos(winkel)),
                _gerundet(kandidatInY + abstand * sin(winkel)),
            )


def wegInDieFreieFläche(
    ränder: Collection[Rand], frei: Callable[[Weg], bool], zurück: Weg
) -> Weg | None:
    zurückInX, zurückInY = zurück
    reichweite = hypot(float(zurückInX), float(zurückInY)) + _toleranz
    nahe = [rand for rand in ränder if _abstandZumUrsprung(rand) <= reichweite]
    punkte = [punkt for rand in nahe for punkt in _lotpunkte(rand)]
    for erster, zweiter in combinations(nahe, 2):
        punkte.extend(_schnittpunkte(erster, zweiter))
    kandidaten = [
        punkt
        for punkt in punkte
        if _länge(punkt) <= reichweite and all(_zulässig(punkt, rand) for rand in nahe)
    ]
    kandidaten.sort(key=_länge)
    return next(
        (weg for kandidat in kandidaten for weg in _umDenKandidaten(kandidat) if frei(weg)), None
    )
