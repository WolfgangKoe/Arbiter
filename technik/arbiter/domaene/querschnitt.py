"""Regeln über die Stellen der Modelle: Überdeckung, Kohärenz, Formation."""

from collections.abc import Mapping
from dataclasses import dataclass
from fractions import Fraction
from math import isqrt

from arbiter.domaene import messen
from arbiter.domaene.spielobjekte import Base, Modell, Stelle

# Regel: QUE-4.2, Kohärenz heißt ein Abstand von höchstens 2″ (core_rules.txt:434)
_kohärenzabstand = Fraction(2)
_größteEinheitMitEinemPartner = 5
# Regel: AUF-8.5, die Mittelpunkte benachbarter Reihen liegen auf 1/100″ genau
_hundertstel = 100


# Regel: QUE-1.2, keine zwei Bases überdecken sich; das Modell selbst zählt nicht (AUF-3.7)
def baseÜberdeckt(modell: Modell, stelle: Stelle, stellen: Mapping[Modell, Stelle]) -> bool:
    return any(
        messen.überdecken(modell.base, stelle, anderes.base, andereStelle)
        for anderes, andereStelle in stellen.items()
        if anderes is not modell
    )


# Regel: QUE-4, die gesetzten Modelle einer Einheit stehen beisammen (core_rules.txt:434)
def inKohärenz(stellen: Mapping[Modell, Stelle]) -> bool:
    if len(stellen) <= 1:
        return True
    partner = {
        modell: {
            anderes
            for anderes, andereStelle in stellen.items()
            if anderes is not modell
            and messen.abstandHöchstens(
                modell.base, stelle, anderes.base, andereStelle, _kohärenzabstand
            )
        }
        for modell, stelle in stellen.items()
    }
    verlangt = 1 if len(stellen) <= _größteEinheitMitEinemPartner else 2
    return all(len(gefundene) >= verlangt for gefundene in partner.values()) and _zusammenhängend(
        partner
    )


def _zusammenhängend(partner: Mapping[Modell, set[Modell]]) -> bool:
    start, *_ = partner
    erreicht = {start}
    offen = [start]
    while offen:
        aktuelles = offen.pop()
        neue = partner[aktuelles] - erreicht
        erreicht |= neue
        offen.extend(neue)
    return len(erreicht) == len(partner)


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
        schritt = 2 * messen.radiusInZoll(base) + self.abstand
        versätze = self._versätzeDerReihen(schritt)
        mittelpunkt = (versätze[0] + versätze[-1]) / 2
        stellen = [
            Stelle(x=mitte.x + versatz - mittelpunkt, y=mitte.y + lage)
            for versatz, anzahl in zip(versätze, self.reihen, strict=True)
            for lage in _lagenDerReihe(anzahl, schritt)
        ]
        radius = messen.radiusInZoll(base)
        rückungX = _rückung([stelle.x for stelle in stellen], radius, grenzenInX)
        rückungY = _rückung([stelle.y for stelle in stellen], radius, grenzenInY)
        return [Stelle(x=stelle.x + rückungX, y=stelle.y + rückungY) for stelle in stellen]

    def _versätzeDerReihen(self, schritt: Fraction) -> list[Fraction]:
        versätze = [Fraction(0)]
        for vordere, hintere in zip(self.reihen, self.reihen[1:], strict=False):
            versätze.append(versätze[-1] + _reihenabstand(vordere, hintere, schritt))
        return versätze


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
