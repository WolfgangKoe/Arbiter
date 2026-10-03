from dataclasses import dataclass


@dataclass(frozen=True, eq=False)
class Modell:
    pass


@dataclass(frozen=True, eq=False)
class Einheit:
    modelle: tuple[Modell, ...]


@dataclass(frozen=True, eq=False)
class Armee:
    einheiten: tuple[Einheit, ...] = ()


@dataclass(frozen=True, eq=False)
class Spieler:
    armee: Armee
