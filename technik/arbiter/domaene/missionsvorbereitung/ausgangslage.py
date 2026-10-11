"""Die Ausgangslage der Mission: Armeen, Spielfeld und Aufstellungszonen (MIV-1)."""

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
    """Modelle je Reihe und der Abstand benachbarter Bases in Zoll (AUF-8.5)."""

    reihen: tuple[int, ...]
    abstand: Fraction


@dataclass(frozen=True, eq=False)
class Ausgangslage:
    ersterSpieler: Spieler
    zweiterSpieler: Spieler
    spielfeld: Spielfeld
    tiefen: Mapping[Aufstellungszone, Fraction]
    formationen: Mapping[str, Formation]

    def __post_init__(self) -> None:
        if self.ersterSpieler is self.zweiterSpieler:
            raise ValueError("Die Aufstellung braucht zwei verschiedene Spieler")
        if _teilenSichArmeeOderModell(self.ersterSpieler, self.zweiterSpieler):
            raise ValueError("Die Spieler brauchen verschiedene Armeen ohne gemeinsames Modell")

    def grenzenDerZone(self, zone: Aufstellungszone) -> Grenzen:
        """Die Fläche der Zone als Grenzen in x und in y, die Form von `messen.ganzIn`."""
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
