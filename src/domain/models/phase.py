from dataclasses import dataclass


@dataclass(frozen=True)
class Phase:
    index: int
    name: str


PHASES: list[Phase] = [
    Phase(0, "Befehlsphase"),
    Phase(1, "Bewegungsphase"),
    Phase(2, "Psiphase"),
    Phase(3, "Fernkampfphase"),
    Phase(4, "Angriffphase"),
    Phase(5, "Nahkampfphase"),
    Phase(6, "Moralphase"),
]
