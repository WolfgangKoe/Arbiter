from collections.abc import Collection, Mapping

from arbiter.domaene import messen
from arbiter.domaene.missionsvorbereitung.ausgangslage import Grenzen
from arbiter.domaene.querschnitt.setzen import befundeDesSetzens
from arbiter.domaene.sperre import Grund
from arbiter.domaene.spielobjekte import Modell, Stelle


def gründeGegenDieStelle(
    modell: Modell,
    stelle: Stelle,
    stellen: Mapping[Modell, Stelle],
    eigene: Collection[Modell],
    zone: Grenzen,
) -> set[Grund]:
    befunde = {
        **befundeDesSetzens(modell, stelle, stellen, eigene),
        Grund.nichtGanzInDerZone: not messen.ganzIn(modell.base, stelle, *zone),
    }
    return {grund for grund, trifft in befunde.items() if trifft}
