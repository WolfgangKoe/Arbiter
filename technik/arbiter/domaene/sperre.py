from enum import Enum


class Grund(Enum):
    nichtWählbar = "nicht wählbar"
    nichtInAufstellung = "nicht in Aufstellung"
    einheitBegonnen = "Einheit begonnen"
    nichtGanzInDerZone = "nicht ganz in der Zone"
    baseÜberdeckt = "Base überdeckt"
    nahkampfreichweite = "Nahkampfreichweite"


class Sperre(Exception):
    def __init__(self, *gründe: Grund) -> None:
        super().__init__(", ".join(sorted(grund.value for grund in gründe)))
        self.gründe = frozenset(gründe)
