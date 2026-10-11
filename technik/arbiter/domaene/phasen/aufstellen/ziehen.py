"""Das Ziehen einer Einheit aus der Ablage: ihre Formation (AUF-8.5)."""

from collections.abc import Mapping
from dataclasses import dataclass
from fractions import Fraction
from math import isqrt

from arbiter.domaene import messen
from arbiter.domaene.spielobjekte import Base, Einheit, Modell, Stelle

# Regel: AUF-8.5, die Mittelpunkte benachbarter Reihen liegen auf 1/100″ genau
_hundertstel = 100


@dataclass(frozen=True)
class Formation:
    """Modelle je Reihe und der Abstand benachbarter Bases in Zoll (AUF-8.5)."""

    reihen: tuple[int, ...]
    abstand: Fraction

    def stellen(
        self,
        base: Base,
        mitte: Stelle,
        grenzenInX: tuple[Fraction, Fraction],
        grenzenInY: tuple[Fraction, Fraction],
    ) -> list[Stelle]:
        """Die Stellen mittig an `mitte`, in die Grenzen gerückt, Reihe für Reihe."""
        radius = messen.radiusInZoll(base)
        schritt = 2 * radius + self.abstand
        versätze = self._versätzeDerReihen(schritt)
        mittelpunkt = (versätze[0] + versätze[-1]) / 2
        stellen = [
            Stelle(x=mitte.x + versatz - mittelpunkt, y=mitte.y + lage)
            for versatz, anzahl in zip(versätze, self.reihen, strict=True)
            for lage in _lagenDerReihe(anzahl, schritt)
        ]
        rückungX = _rückung([stelle.x for stelle in stellen], radius, grenzenInX)
        rückungY = _rückung([stelle.y for stelle in stellen], radius, grenzenInY)
        return [Stelle(x=stelle.x + rückungX, y=stelle.y + rückungY) for stelle in stellen]

    def _versätzeDerReihen(self, schritt: Fraction) -> list[Fraction]:
        versätze = [Fraction(0)]
        for vordere, hintere in zip(self.reihen, self.reihen[1:], strict=False):
            versätze.append(versätze[-1] + _reihenabstand(vordere, hintere, schritt))
        return versätze


def stellenDerUngesetzten(
    einheit: Einheit,
    ungesetzte: list[Modell],
    mitte: Stelle,
    formationen: Mapping[str, Formation],
    zone: tuple[tuple[Fraction, Fraction], tuple[Fraction, Fraction]],
) -> dict[Modell, Stelle]:
    """Die Stellen der Ungesetzten beim Loslassen der Einheit an `mitte`."""
    erstes, *_ = ungesetzte
    # Regel: AUF-14.1, der Rest einer Einheit kommt einzeln
    if len(ungesetzte) < len(einheit.modelle):
        return {erstes: mitte}
    stellen = formationen[einheit.name].stellen(erstes.base, mitte, *zone)
    return dict(zip(ungesetzte, stellen, strict=True))


def _reihenabstand(vordere: int, hintere: int, schritt: Fraction) -> Fraction:
    """Der kleinste Abstand auf 1/100″, bei dem jede Base der Nachbarreihe den Schritt hält."""
    nötig = max(
        max(Fraction(0), schritt**2 - (vorn - hinten) ** 2)
        for vorn in _lagenDerReihe(vordere, schritt)
        for hinten in _lagenDerReihe(hintere, schritt)
    )
    hundertstel = _aufgerundeteWurzel(nötig * _hundertstel**2)
    return Fraction(hundertstel, _hundertstel)


def _lagenDerReihe(anzahl: int, schritt: Fraction) -> list[Fraction]:
    """Die Lagen der Bases einer Reihe entlang der Kante, mittig um null."""
    return [(platz - Fraction(anzahl - 1, 2)) * schritt for platz in range(anzahl)]


def _aufgerundeteWurzel(quadrat: Fraction) -> int:
    ganze = isqrt(-(-quadrat.numerator // quadrat.denominator))
    return ganze if ganze**2 >= quadrat else ganze + 1


def _rückung(
    werte: list[Fraction], radius: Fraction, grenzen: tuple[Fraction, Fraction]
) -> Fraction:
    von, bis = grenzen
    vorn = min(werte) - radius
    hinten = max(werte) + radius
    if vorn < von:
        return von - vorn
    if hinten > bis:
        return bis - hinten
    return Fraction(0)
