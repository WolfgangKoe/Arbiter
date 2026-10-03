from dataclasses import dataclass, field


@dataclass(eq=False)
class Modell:
    gesetzt: bool = False


@dataclass(eq=False)
class Einheit:
    modelle: list[Modell]
    aufgestellt: bool = False

    @property
    def begonnen(self) -> bool:
        return any(modell.gesetzt for modell in self.modelle)


@dataclass(eq=False)
class Armee:
    einheiten: list[Einheit] = field(default_factory=list)

    @property
    def hatEinheitenZumAufstellen(self) -> bool:
        return any(not einheit.aufgestellt for einheit in self.einheiten)


@dataclass(eq=False)
class Spieler:
    armee: Armee
