from collections.abc import Mapping

from arbiter.domaene import messen
from arbiter.domaene.missionsvorbereitung.ausgangslage import Grenzen
from arbiter.domaene.spielobjekte import Modell, Stelle


def hineingerückt(stellen: Mapping[Modell, Stelle], zone: Grenzen) -> dict[Modell, Stelle]:
    grenzenInX, grenzenInY = zone
    rückung = messen.rückungInDieFläche(
        ((modell.base, stelle) for modell, stelle in stellen.items()), grenzenInX, grenzenInY
    )
    return {modell: messen.verschoben(stelle, rückung) for modell, stelle in stellen.items()}


def verschobeneStellen(
    gruppe: Mapping[Modell, Stelle], gezogenes: Modell, ziel: Stelle
) -> dict[Modell, Stelle]:
    weg = messen.wegZwischen(gruppe[gezogenes], ziel)
    verschobene = {modell: messen.verschoben(stelle, weg) for modell, stelle in gruppe.items()}
    return {**verschobene, gezogenes: ziel}
