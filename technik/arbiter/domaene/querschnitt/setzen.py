from collections.abc import Collection, Mapping
from fractions import Fraction

from arbiter.domaene import messen
from arbiter.domaene.sperre import Grund
from arbiter.domaene.spielobjekte import Einheit, Modell, Stelle

nahkampfreichweite = Fraction(1)


def gesetzteModelle(einheit: Einheit, stellen: Mapping[Modell, Stelle]) -> dict[Modell, Stelle]:
    return {modell: stellen[modell] for modell in einheit.modelle if modell in stellen}


def baseÜberdeckt(modell: Modell, stelle: Stelle, stellen: Mapping[Modell, Stelle]) -> bool:
    return any(
        messen.überdecken(modell.base, stelle, anderes.base, andereStelle)
        for anderes, andereStelle in stellen.items()
        if anderes is not modell
    )


def inNahkampfreichweite(
    modell: Modell, stelle: Stelle, stellen: Mapping[Modell, Stelle], eigene: Collection[Modell]
) -> bool:
    return any(
        anderes not in eigene
        and messen.abstandHöchstens(
            modell.base, stelle, anderes.base, andereStelle, nahkampfreichweite
        )
        for anderes, andereStelle in stellen.items()
    )


def befundeDesSetzens(
    modell: Modell,
    stelle: Stelle,
    stellen: Mapping[Modell, Stelle],
    eigene: Collection[Modell],
) -> dict[Grund, bool]:
    return {
        Grund.baseÜberdeckt: baseÜberdeckt(modell, stelle, stellen),
        Grund.nahkampfreichweite: inNahkampfreichweite(modell, stelle, stellen, eigene),
    }
