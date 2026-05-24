from dataclasses import dataclass


@dataclass(frozen=True)
class Phase:
    index: int
    name: str


PHASES: list[Phase] = [
    Phase(0, "Befehlsphase"),
    Phase(1, "Bewegungsphase"),
    Phase(2, "Psychische Phase"),
    Phase(3, "Schussphase"),
    Phase(4, "Angriffphase"),
    Phase(5, "Kampfphase"),
    Phase(6, "Moralphase"),
]
