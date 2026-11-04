from enum import Enum


class Grund(Enum):
    nichtWählbar = "nicht wählbar"
    nichtInAufstellung = "nicht in Aufstellung"
    einheitBegonnen = "Einheit begonnen"
    keineKohärenz = "keine Kohärenz"
    nichtGanzInDerZone = "nicht ganz in der Zone"
    baseÜberdeckt = "Base überdeckt"
    bewegungsweite = "Bewegungsweite"
    nahkampfreichweite = "Nahkampfreichweite"


class Sperre(Exception):
    def __init__(self, grund: Grund, *weitere: Grund) -> None:
        gründe = (grund, *weitere)
        super().__init__(", ".join(sorted(einzelner.value for einzelner in gründe)))
        self.gründe = frozenset(gründe)
