from collections.abc import Mapping
from dataclasses import dataclass
from enum import Enum
from fractions import Fraction

from arbiter.domaene.spielobjekte import Spieler, Spielfeld

Grenzen = tuple[tuple[Fraction, Fraction], tuple[Fraction, Fraction]]


class Aufstellungszone(Enum):
    erste = 1
    zweite = 2


@dataclass(frozen=True)
class Formation:
    reihen: tuple[int, ...]
    abstand: Fraction


@dataclass(frozen=True, eq=False)
class Ausgangslage:
    ersterSpieler: Spieler
    zweiterSpieler: Spieler
    spielfeld: Spielfeld
    tiefen: Mapping[Aufstellungszone, Fraction]
    formationen: Mapping[str, Formation]
    letzteSchlachtrunde: int

    def __post_init__(self) -> None:
        if _teilenSichArmeeOderModell(self.ersterSpieler, self.zweiterSpieler):
            raise ValueError("Die Spieler brauchen verschiedene Armeen ohne gemeinsames Modell")

    def grenzenDerZone(self, zone: Aufstellungszone) -> Grenzen:
        breite, länge = self.spielfeld.seitenlängen
        return _grenzenInXDerZone(zone, breite, self.tiefen[zone]), (Fraction(0), länge)


def _grenzenInXDerZone(
    zone: Aufstellungszone, breite: Fraction, tiefe: Fraction
) -> tuple[Fraction, Fraction]:
    if zone is Aufstellungszone.erste:
        return Fraction(0), tiefe
    return breite - tiefe, breite


def _teilenSichArmeeOderModell(ersterSpieler: Spieler, zweiterSpieler: Spieler) -> bool:
    return (
        ersterSpieler.armee is zweiterSpieler.armee
        or not ersterSpieler.armee.modelle.isdisjoint(zweiterSpieler.armee.modelle)
    )
