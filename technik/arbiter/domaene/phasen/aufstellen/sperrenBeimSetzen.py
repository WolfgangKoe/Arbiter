"""Die Gründe gegen eine Stelle beim Setzen und Loslassen eines Modells (AUF-3, D4)."""

from collections.abc import Collection, Mapping
from fractions import Fraction

from arbiter.domaene import messen
from arbiter.domaene.querschnitt import baseÜberdeckt
from arbiter.domaene.sperre import Grund
from arbiter.domaene.spielobjekte import Modell, Stelle

Grenzen = tuple[tuple[Fraction, Fraction], tuple[Fraction, Fraction]]

# Regel: Nahkampfreichweite ist ein Abstand von höchstens 1″ (domaene/glossar.md)
_nahkampfreichweite = Fraction(1)


# Regel: Nahkampfreichweite (core_rules.txt:447)
def inNahkampfreichweite(
    modell: Modell, stelle: Stelle, stellen: Mapping[Modell, Stelle], eigene: Collection[Modell]
) -> bool:
    return any(
        anderes not in eigene
        and messen.abstandHöchstens(
            modell.base, stelle, anderes.base, andereStelle, _nahkampfreichweite
        )
        for anderes, andereStelle in stellen.items()
    )


def gründeGegenDieStelle(
    modell: Modell,
    stelle: Stelle,
    stellen: Mapping[Modell, Stelle],
    eigene: Collection[Modell],
    zone: Grenzen,
) -> set[Grund]:
    """Die Gründe gegen die Stelle; `eigene` sind die Modelle des Spielers an der Reihe."""
    gegeben = {
        Grund.nichtGanzInDerZone: not messen.ganzIn(modell.base, stelle, *zone),
        Grund.baseÜberdeckt: baseÜberdeckt(modell, stelle, stellen),
        # Regel: Aufstellen nicht in Nahkampfreichweite (core_rules.txt:450)
        Grund.nahkampfreichweite: inNahkampfreichweite(modell, stelle, stellen, eigene),
    }
    return {grund for grund, trifft in gegeben.items() if trifft}
