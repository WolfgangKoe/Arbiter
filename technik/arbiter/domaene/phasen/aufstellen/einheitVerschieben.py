"""Das Verschieben einer Einheit als Block und das Hineinrücken in die Zone (AUF-21, AUF-26.1)."""

from collections.abc import Mapping

from arbiter.domaene import messen
from arbiter.domaene.missionsvorbereitung.ausgangslage import Grenzen
from arbiter.domaene.spielobjekte import Modell, Stelle


def verschobeneStellen(
    gruppe: Mapping[Modell, Stelle], gezogenes: Modell, ziel: Stelle
) -> dict[Modell, Stelle]:
    """Jedes Modell der Gruppe um den Weg des gezogenen; das gezogene steht am Ziel."""
    davor = gruppe.get(gezogenes)
    if davor is None:
        return {gezogenes: ziel}
    weg = messen.wegZwischen(davor, ziel)
    verschobene = {modell: messen.verschoben(stelle, weg) for modell, stelle in gruppe.items()}
    return {**verschobene, gezogenes: ziel}


def hineingerückt(stellen: Mapping[Modell, Stelle], zone: Grenzen) -> dict[Modell, Stelle]:
    """Alle gemeinsam auf kürzestem Weg in die Zone, bis jede Base ganz darin liegt."""
    grenzenInX, grenzenInY = zone
    rückung = messen.rückungInDieFläche(
        ((modell.base, stelle) for modell, stelle in stellen.items()), grenzenInX, grenzenInY
    )
    return {modell: messen.verschoben(stelle, rückung) for modell, stelle in stellen.items()}
