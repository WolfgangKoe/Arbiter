"""Die Gründe gegen die Stellen beim Loslassen in der Bewegungsphase (BEW-2, QUE-1)."""

from collections.abc import Collection, Mapping

from arbiter.domaene import messen
from arbiter.domaene.querschnitt import gründeDesSetzens
from arbiter.domaene.sperre import Grund
from arbiter.domaene.spielobjekte import Modell, Stelle


def _überEineBase(
    modell: Modell, vorige: Stelle, neue: Stelle, fremde: Mapping[Modell, Stelle]
) -> bool:
    return any(
        messen.streckeÜberdeckt(modell.base, vorige, neue, anderes.base, ort)
        for anderes, ort in fremde.items()
    )


def gründeBeimZiehen(
    vorige: Mapping[Modell, Stelle],
    neue: Mapping[Modell, Stelle],
    fremde: Mapping[Modell, Stelle],
    eigene: Collection[Modell],
) -> set[Grund]:
    """Die Gründe gegen die neuen Stellen; `fremde` sind alle Modelle, die nicht gezogen werden."""
    gründe: set[Grund] = set()
    for modell, stelle in neue.items():
        gründe |= gründeDesSetzens(modell, stelle, fremde, eigene)
        if _überEineBase(modell, vorige[modell], stelle, fremde):
            gründe.add(Grund.überEineBase)
    return gründe
