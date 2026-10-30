"""Das Setzen eines Modells (QUE-1), was mehrere Regeln über Stellen brauchen."""

from collections.abc import Collection, Mapping
from fractions import Fraction

from arbiter.domaene import messen
from arbiter.domaene.sperre import Grund
from arbiter.domaene.spielobjekte import Modell, Stelle

_nahkampfreichweite = Fraction(1)


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
            modell.base, stelle, anderes.base, andereStelle, _nahkampfreichweite
        )
        for anderes, andereStelle in stellen.items()
    )


def befundeDesSetzens(
    modell: Modell,
    stelle: Stelle,
    stellen: Mapping[Modell, Stelle],
    eigene: Collection[Modell],
) -> dict[Grund, bool]:
    """Je Grund nach QUE-1, ob er gegen die Stelle gilt; `eigene` sind die Modelle am Zug."""
    return {
        Grund.baseÜberdeckt: baseÜberdeckt(modell, stelle, stellen),
        Grund.nahkampfreichweite: inNahkampfreichweite(modell, stelle, stellen, eigene),
    }
