"""Die Gründe gegen eine Stelle beim Setzen und Loslassen eines Modells (AUF-3, D4)."""

from collections.abc import Collection, Mapping

from arbiter.domaene import messen
from arbiter.domaene.missionsvorbereitung.ausgangslage import Grenzen
from arbiter.domaene.querschnitt import befundeDesSetzens
from arbiter.domaene.sperre import Grund
from arbiter.domaene.spielobjekte import Modell, Stelle


def gründeGegenDieStelle(
    modell: Modell,
    stelle: Stelle,
    stellen: Mapping[Modell, Stelle],
    eigene: Collection[Modell],
    zone: Grenzen,
) -> set[Grund]:
    """Die Gründe gegen die Stelle; `eigene` sind die Modelle des Spielers an der Reihe."""
    befunde = {
        **befundeDesSetzens(modell, stelle, stellen, eigene),
        Grund.nichtGanzInDerZone: not messen.ganzIn(modell.base, stelle, *zone),
    }
    return {grund for grund, trifft in befunde.items() if trifft}
