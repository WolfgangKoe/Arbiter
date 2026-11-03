from collections.abc import Mapping

from arbiter.domaene import messen
from arbiter.domaene.spielobjekte import Modell, Stelle


def angehalten(
    stellen: Mapping[Modell, Stelle], neue: Mapping[Modell, Stelle], gezogenes: Modell
) -> dict[Modell, Stelle]:
    weg = messen.wegZwischen(stellen[gezogenes], neue[gezogenes])
    bewegte = [(modell.base, stellen[modell]) for modell in neue]
    ruhende = [(modell.base, stelle) for modell, stelle in stellen.items() if modell not in neue]
    anteil = messen.anteilBisZurBerührung(bewegte, ruhende, weg)
    kurz = messen.teilDesWegs(weg, anteil)
    return {modell: messen.verschoben(stellen[modell], kurz) for modell in neue}
