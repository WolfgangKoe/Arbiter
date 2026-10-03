from dataclasses import dataclass
from fractions import Fraction


@dataclass(frozen=True)
class Base:
    """Rund; der Durchmesser in mm."""

    durchmesser: int


@dataclass(frozen=True)
class Stelle:
    """Mittelpunkt einer Base in Zoll (technik/architektur.md, S1)."""

    x: Fraction
    y: Fraction


@dataclass(frozen=True)
class Spielfeld:
    seitenlängen: tuple[Fraction, Fraction]


@dataclass(frozen=True, eq=False)
class Modell:
    base: Base


@dataclass(frozen=True, eq=False)
class Einheit:
    modelle: tuple[Modell, ...]


@dataclass(frozen=True, eq=False)
class Armee:
    einheiten: tuple[Einheit, ...] = ()


@dataclass(frozen=True, eq=False)
class Spieler:
    armee: Armee
