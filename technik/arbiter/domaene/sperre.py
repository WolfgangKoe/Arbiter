from enum import Enum


class Grund(Enum):
    nichtWählbar = "nicht wählbar"
    nichtInAufstellung = "nicht in Aufstellung"
    einheitBegonnen = "Einheit begonnen"


class Sperre(Exception):
    def __init__(self, grund: Grund) -> None:
        super().__init__(grund.value)
        self.grund = grund
