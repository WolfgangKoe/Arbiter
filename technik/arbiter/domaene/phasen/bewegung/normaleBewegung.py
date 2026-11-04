from collections.abc import Collection, Mapping

from arbiter.domaene.querschnitt.setzen import befundeDesSetzens
from arbiter.domaene.sperre import Grund
from arbiter.domaene.spielobjekte import Modell, Stelle


def gründeBeimZiehen(
    vorige: Mapping[Modell, Stelle],
    neue: Mapping[Modell, Stelle],
    fremde: Mapping[Modell, Stelle],
    eigene: Collection[Modell],
) -> set[Grund]:
    gründe: set[Grund] = set()
    for modell, stelle in neue.items():
        if stelle == vorige[modell]:
            continue
        befunde = befundeDesSetzens(modell, stelle, fremde, eigene)
        gründe |= {grund for grund, trifft in befunde.items() if trifft}
    return gründe
