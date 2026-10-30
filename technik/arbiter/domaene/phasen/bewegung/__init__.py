from collections.abc import Collection, Iterable, Mapping

from arbiter.domaene import messen
from arbiter.domaene.phasen.bewegung.anhaltenAnDerBewegungsweite import (
    anteilBisZurBewegungsweite,
)
from arbiter.domaene.phasen.bewegung.anhaltenVorDerGrenze import (
    anteilBisZurNahkampfreichweite,
    anteilBisZurSpielfeldkante,
)
from arbiter.domaene.phasen.bewegung.beenden import gründeGegenDasBeenden
from arbiter.domaene.phasen.bewegung.sperrenBeimZiehen import gründeBeimZiehen
from arbiter.domaene.sperre import Grund
from arbiter.domaene.spielobjekte import Einheit, Modell, Spielfeld, Stelle

StellenMitGründen = tuple[dict[Modell, Stelle], set[Grund]]


class Bewegungsphase:
    def __init__(self, stellen: Mapping[Modell, Stelle], spielfeld: Spielfeld) -> None:
        self._spielfeld = spielfeld
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
        gegner = {anderes: ort for anderes, ort in stellen.items() if anderes not in eigene}
        anteil = min(
            anteilBisZurBewegungsweite(ebene, weg, self._stellenZuBeginn),
            anteilBisZurSpielfeldkante(ebene, weg, self._spielfeld),
            anteilBisZurNahkampfreichweite(ebene, weg, gegner),
        )
        kurz = messen.teilDesWegs(weg, anteil)
        neue = {modell: messen.verschoben(stelle, kurz) for modell, stelle in ebene.items()}
        fremde = {anderes: ort for anderes, ort in stellen.items() if anderes not in neue}
        return neue, gründeBeimZiehen(ebene, neue, fremde, eigene)

    def gründeGegenDasBeenden(
        self, einheiten: Iterable[Einheit], stellen: Mapping[Modell, Stelle]
    ) -> set[Grund]:
        return gründeGegenDasBeenden(einheiten, stellen)
