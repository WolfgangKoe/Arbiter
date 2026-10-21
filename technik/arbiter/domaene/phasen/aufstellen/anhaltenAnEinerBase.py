"""Das Anhalten beim Ziehen an der ersten Base, an die ein Modell oder der Block stößt (AUF-26)."""

from collections.abc import Mapping

from arbiter.domaene import messen
from arbiter.domaene.spielobjekte import Modell, Stelle


def angehalten(
    stellen: Mapping[Modell, Stelle], neue: Mapping[Modell, Stelle], gezogenes: Modell
) -> dict[Modell, Stelle]:
    """Die neuen Stellen, der gemeinsame Weg gekürzt bis keine Base eine andere überdeckt."""
    davor = stellen.get(gezogenes)
    if davor is None:
        return dict(neue)
    ziel = neue[gezogenes]
    weg = messen.wegZwischen(davor, ziel)
    bewegte = [(modell.base, stellen[modell]) for modell in neue]
    # Regel: AUF-26.2 und 26.3, die Modelle des Blocks halten einander nicht an
    ruhende = [(modell.base, stelle) for modell, stelle in stellen.items() if modell not in neue]
    anteil = messen.anteilBisZurBerührung(bewegte, ruhende, weg)
    kurz = messen.teilDesWegs(weg, anteil)
    return {modell: messen.verschoben(stellen[modell], kurz) for modell in neue}
