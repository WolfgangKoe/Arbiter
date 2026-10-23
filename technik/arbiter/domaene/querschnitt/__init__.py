"""Die Überdeckung der Bases (QUE-1), was mehrere Regeln über Stellen brauchen."""

from collections.abc import Mapping

from arbiter.domaene import messen
from arbiter.domaene.spielobjekte import Modell, Stelle


def baseÜberdeckt(modell: Modell, stelle: Stelle, stellen: Mapping[Modell, Stelle]) -> bool:
    return any(
        messen.überdecken(modell.base, stelle, anderes.base, andereStelle)
        for anderes, andereStelle in stellen.items()
        if anderes is not modell
    )
