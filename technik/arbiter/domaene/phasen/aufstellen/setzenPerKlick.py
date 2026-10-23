"""Das Setzen einer Einheit per Klick: ihre Formation (AUF-18.2, 18.3)."""

from collections.abc import Mapping
from fractions import Fraction
from itertools import accumulate, pairwise
from math import ceil, isqrt

from arbiter.domaene import messen
from arbiter.domaene.missionsvorbereitung.ausgangslage import Formation, Grenzen
from arbiter.domaene.spielobjekte import Base, Einheit, Modell, Stelle

_hundertstel = 100


def stellenDerFormation(
    formation: Formation,
    base: Base,
    mitte: Stelle,
    grenzenInX: tuple[Fraction, Fraction],
    grenzenInY: tuple[Fraction, Fraction],
) -> list[Stelle]:
    """Die Stellen mittig an `mitte`, in die Grenzen gerückt, Reihe für Reihe."""
    radius = messen.radiusInZoll(base)
    schritt = 2 * radius + formation.abstand
    versätze = _versätzeDerReihen(formation.reihen, schritt)
    stellen = [
        Stelle(x=mitte.x + versatz, y=mitte.y + lage)
        for versatz, anzahl in zip(versätze, formation.reihen, strict=True)
        for lage in _lagenDerReihe(anzahl, schritt)
    ]
    rückung = messen.rückungInDieFläche(
        ((base, stelle) for stelle in stellen), grenzenInX, grenzenInY
    )
    return [messen.verschoben(stelle, rückung) for stelle in stellen]


def formationDerEinheit(
    einheit: Einheit, mitte: Stelle, formationen: Mapping[str, Formation], zone: Grenzen
) -> dict[Modell, Stelle]:
    """Die Stellen aller Modelle der Einheit beim Klick an `mitte`."""
    erstes, *_ = einheit.modelle
    stellen = stellenDerFormation(formationen[einheit.name], erstes.base, mitte, *zone)
    return dict(zip(einheit.modelle, stellen, strict=True))


def _versätzeDerReihen(reihen: tuple[int, ...], schritt: Fraction) -> list[Fraction]:
    """Die Lagen der Reihen quer zu den Reihen, mittig um null."""
    abstände = [_reihenabstand(vordere, hintere, schritt) for vordere, hintere in pairwise(reihen)]
    return list(accumulate(abstände, initial=-sum(abstände, Fraction(0)) / 2))


def _reihenabstand(vordere: int, hintere: int, schritt: Fraction) -> Fraction:
    """Der kleinste Abstand auf 1/100″, bei dem jede Base der Nachbarreihe den Schritt hält."""
    nächster = min(
        abs(vorn - hinten)
        for vorn in _lagenDerReihe(vordere, schritt)
        for hinten in _lagenDerReihe(hintere, schritt)
    )
    hundertstel = _aufgerundeteWurzel((schritt**2 - nächster**2) * _hundertstel**2)
    return Fraction(hundertstel, _hundertstel)


def _lagenDerReihe(anzahl: int, schritt: Fraction) -> list[Fraction]:
    """Die Lagen der Bases einer Reihe entlang der Kante, mittig um null."""
    return [(platz - Fraction(anzahl - 1, 2)) * schritt for platz in range(anzahl)]


def _aufgerundeteWurzel(quadrat: Fraction) -> int:
    ganze = isqrt(ceil(quadrat))
    return ganze if ganze**2 >= quadrat else ganze + 1
