from collections.abc import Mapping

from arbiter.domaene import messen
from arbiter.domaene.spielobjekte import Einheit, Modell, Spieler, Stelle


def einheitVon(beideSpieler: tuple[Spieler, Spieler], modell: Modell) -> Einheit:
    for spieler in beideSpieler:
        einheit = spieler.armee.einheitVon(modell)
        if einheit is not None:
            return einheit
    raise ValueError("Das Modell gehört nicht zur Aufstellung")


def verschobeneStellen(
    gruppe: Mapping[Modell, Stelle], gezogenes: Modell, ziel: Stelle
) -> dict[Modell, Stelle]:
    davor = gruppe.get(gezogenes)
    if davor is None:
        return {gezogenes: ziel}
    weg = messen.wegZwischen(davor, ziel)
    verschobene = {modell: messen.verschoben(stelle, weg) for modell, stelle in gruppe.items()}
    return {**verschobene, gezogenes: ziel}
