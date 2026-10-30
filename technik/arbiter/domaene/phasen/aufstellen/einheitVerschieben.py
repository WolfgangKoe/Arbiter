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
