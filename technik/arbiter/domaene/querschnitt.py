from collections.abc import Mapping

from arbiter.domaene import messen
from arbiter.domaene.spielobjekte import Modell, Stelle


# Regel: QUE-1.2, keine zwei Bases überdecken sich; das Modell selbst zählt nicht (AUF-3.7)
def baseÜberdeckt(modell: Modell, stelle: Stelle, stellen: Mapping[Modell, Stelle]) -> bool:
    return any(
        messen.überdecken(modell.base, stelle, anderes.base, andereStelle)
        for anderes, andereStelle in stellen.items()
        if anderes is not modell
    )
