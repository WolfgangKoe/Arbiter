from collections.abc import Collection, Iterable, Mapping

from arbiter.domaene import messen
from arbiter.domaene.phasen.bewegung.anhaltenAnDerBewegungsweite import (
    anDerBewegungsweiteAngehalten,
)
from arbiter.domaene.phasen.bewegung.beenden import gründeGegenDasBeenden
from arbiter.domaene.phasen.bewegung.sperrenBeimZiehen import gründeBeimZiehen
from arbiter.domaene.sperre import Grund
from arbiter.domaene.spielobjekte import Einheit, Modell, Stelle

StellenMitGründen = tuple[dict[Modell, Stelle], set[Grund]]


class Bewegungsphase:
    def __init__(self, stellen: Mapping[Modell, Stelle]) -> None:
        self._stellenZuBeginn = dict(stellen)

    def stellenMitGründenNachDemZiehen(
        self,
        ebene: Mapping[Modell, Stelle],
        gezogenes: Modell,
        ziel: Stelle,
        stellen: Mapping[Modell, Stelle],
        eigene: Collection[Modell],
    ) -> StellenMitGründen:
        weg = messen.wegZwischen(ebene[gezogenes], ziel)
        neue = anDerBewegungsweiteAngehalten(ebene, weg, self._stellenZuBeginn)
        fremde = {anderes: ort for anderes, ort in stellen.items() if anderes not in neue}
        return neue, gründeBeimZiehen(ebene, neue, fremde, eigene)

    def gründeGegenDasBeenden(
        self, einheiten: Iterable[Einheit], stellen: Mapping[Modell, Stelle]
    ) -> set[Grund]:
        return gründeGegenDasBeenden(einheiten, stellen)
