from collections.abc import Mapping

from arbiter.domaene.querschnitt.setzen import gesetzteModelle, inNahkampfreichweite
from arbiter.domaene.spielobjekte import Einheit, Modell, Stelle


def einModellInNahkampfreichweite(
    einheit: Einheit, stellen: Mapping[Modell, Stelle], gegner: Mapping[Modell, Stelle]
) -> bool:
    return any(
        inNahkampfreichweite(modell, stelle, gegner, eigene=())
        for modell, stelle in gesetzteModelle(einheit, stellen).items()
    )
