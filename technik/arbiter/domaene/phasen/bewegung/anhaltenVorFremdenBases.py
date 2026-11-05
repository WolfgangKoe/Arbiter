from collections.abc import Collection
from fractions import Fraction

from arbiter.domaene import messen
from arbiter.domaene.phasen.aufstellen.anhaltenAufDemWeg import (
    Weiterrücken,
    gleiten,
    umFremdeGleiten,
    zuvorGezeigt,
    überdecktFremde,
)
from arbiter.domaene.phasen.bewegung.anhaltenVorDerGrenze import anteilBisZurNahkampfreichweite
from arbiter.domaene.phasen.bewegung.normaleBewegung import (
    AnteilAufDemWeg,
    Gezogen,
    Stellen,
    Umgebung,
    gründeBeimZiehen,
    verschobenUm,
)
from arbiter.domaene.phasen.bewegung.uebergehenBeimZiehen import Anteile
from arbiter.domaene.querschnitt.setzen import Gezeigt
from arbiter.domaene.sperre import Grund
from arbiter.domaene.spielobjekte import Modell, Stelle


class Gleiten:
    def __init__(
        self,
        gezogen: Gezogen,
        umgebung: Umgebung,
        bewegungsweite: AnteilAufDemWeg,
        spielfeldkante: AnteilAufDemWeg,
    ) -> None:
        self._gezogen = gezogen
        self._umgebung = umgebung
        self._bewegungsweite = bewegungsweite
        self._spielfeldkante = spielfeldkante

    def gezeigt(self) -> tuple[Gezeigt, bool]:
        ebene, gezogenes = self._gezogen.ebene, self._gezogen.gezogenes
        weiter = self._gezogen.weiter or Weiterrücken(None, angehaltenAufDemWeg=False)
        zuvor = zuvorGezeigt(ebene, gezogenes, weiter)
        weg = messen.wegZwischen(ebene[gezogenes], self._gezogen.ziel)
        anteile = self._anteile(ebene, weg)
        halt = verschobenUm(ebene, messen.teilDesWegs(weg, min(anteile)))
        hältAnDerGrenze = anteile.hältAnDerBewegungsweiteOderNahkampfreichweite
        if weiter.angehaltenAufDemWeg:
            halt, nahkampfreichweiteHält = self._gekürztAnDerNahkampfreichweite(zuvor, halt)
            hältAnDerGrenze = hältAnDerGrenze or nahkampfreichweiteHält
        if not überdecktFremde(zuvor, halt, self._umgebung.fremde):
            return Gezeigt(halt, weiter.angehaltenAufDemWeg), hältAnDerGrenze
        return self._umFremdeGeglitten(zuvor)

    def _gekürztAnDerNahkampfreichweite(
        self, zuvor: Stellen, halt: Stellen
    ) -> tuple[dict[Modell, Stelle], bool]:
        gezogenes = self._gezogen.gezogenes
        weg = messen.wegZwischen(zuvor[gezogenes], halt[gezogenes])
        anteil = anteilBisZurNahkampfreichweite(zuvor, weg, self._umgebung.gegner)
        return verschobenUm(zuvor, messen.teilDesWegs(weg, anteil)), anteil < 1

    def _umFremdeGeglitten(self, zuvor: Stellen) -> tuple[Gezeigt, bool]:
        gezogenes = self._gezogen.gezogenes
        wegAbZuvor = messen.wegZwischen(zuvor[gezogenes], self._gezogen.ziel)
        geglitten = umFremdeGleiten(
            zuvor, wegAbZuvor, self._umgebung.fremde, self._anteilBisZumAnhalten
        )
        anteileAbZuvor = self._anteile(zuvor, wegAbZuvor)
        stelleDesAnteils = messen.verschoben(
            zuvor[gezogenes], messen.teilDesWegs(wegAbZuvor, min(anteileAbZuvor))
        )
        hältAnDerGrenze = (
            anteileAbZuvor.hältAnDerBewegungsweiteOderNahkampfreichweite
            and geglitten.stellen[gezogenes] == stelleDesAnteils
        )
        return Gezeigt(geglitten.stellen, geglitten.angehaltenAufDemWeg), hältAnDerGrenze

    def _anteilBisZumAnhalten(self, vorige: Stellen, weg: messen.Weg) -> Fraction:
        return min(self._anteile(vorige, weg))

    def _anteile(self, ebene: Stellen, weg: messen.Weg) -> Anteile:
        return Anteile(
            self._bewegungsweite(ebene, weg),
            self._spielfeldkante(ebene, weg),
            anteilBisZurNahkampfreichweite(ebene, weg, self._umgebung.gegner),
        )

    def gründeBeimZiehen(self, gesetzt: Stellen, eigene: Collection[Modell]) -> set[Grund]:
        return gründeBeimZiehen(self._gezogen.ebene, gesetzt, self._umgebung.fremde, eigene)

    def nachDemLoslassen(self, gezeigt: Gezeigt) -> Gezeigt:
        return gezeigt

    def übergangen(self, kurz: messen.Weg) -> Stellen:
        return gleiten(
            self._gezogen.ebene,
            kurz,
            self._umgebung.fremde,
            self._spielfeldkante,
            angehaltenAufDemWeg=False,
        ).stellen

    def anteileBeimÜbergehen(self, weg: messen.Weg) -> Anteile:
        return self._anteile(self._gezogen.ebene, weg)
