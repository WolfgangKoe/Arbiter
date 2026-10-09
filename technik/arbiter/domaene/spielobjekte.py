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
    name: str
    modelle: tuple[Modell, ...]


@dataclass(frozen=True, eq=False)
class Armee:
    einheiten: tuple[Einheit, ...] = ()

    @property
    def modelle(self) -> frozenset[Modell]:
        return frozenset(modell for einheit in self.einheiten for modell in einheit.modelle)

    def einheitVon(self, modell: Modell) -> Einheit | None:
        """Die Einheit der Armee, zu der das Modell gehört, sonst None."""
        return next((einheit for einheit in self.einheiten if modell in einheit.modelle), None)


@dataclass(frozen=True, eq=False)
class Spieler:
    armee: Armee
