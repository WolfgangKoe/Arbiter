from collections.abc import Collection, Iterable, Mapping
from fractions import Fraction
from functools import partial

from arbiter.domaene import messen
from arbiter.domaene.phasen.aufstellen.anhaltenAufDemWeg import (
    AnteilBisZumAnhalten,
    Stellen,
    Weiterrücken,
    gleiten,
    zuvorGezeigt,
)
from arbiter.domaene.phasen.bewegung.anhaltenAnDerBewegungsweite import (
    anteilBisZurBewegungsweite,
)
from arbiter.domaene.phasen.bewegung.anhaltenVorDerGrenze import (
    anteilBisZurNahkampfreichweite,
    anteilBisZurSpielfeldkante,
)
from arbiter.domaene.phasen.bewegung.beenden import gründeGegenDasBeenden
from arbiter.domaene.phasen.bewegung.grenzkreise import (
    Einhüllende,
    grenzeDerBewegung,
    grenzenDerWürfe,
    kleinsterWurfAn,
    möglicheWürfe,
)
from arbiter.domaene.phasen.bewegung.normaleBewegung import gründeBeimZiehen
from arbiter.domaene.phasen.bewegung.uebergehenBeimZiehen import (
    Angebot,
    Anteile,
    Übergangen,
    gründeBeimÜbergehen,
)
from arbiter.domaene.querschnitt.setzen import Gezeigt
from arbiter.domaene.sperre import Grund
from arbiter.domaene.spielobjekte import Einheit, Modell, Spielfeld, Stelle, einheitDes

StellenMitGründen = tuple[Gezeigt, set[Grund]]


class Bewegungsphase:
    def __init__(self, stellen: Mapping[Modell, Stelle], spielfeld: Spielfeld) -> None:
        self._spielfeld = spielfeld
        self._stellenZuBeginn = dict(stellen)
        self._wartendeEinheiten: set[Einheit] = set()
        self._vorrückwürfe: dict[Einheit, int] = {}
        self._angebot: Angebot | None = None

    @property
    def übergehenAngeboten(self) -> bool:
        return self._angebot is not None

    def angebotBeenden(self) -> None:
        self._angebot = None

    def angebotNachDemZiehen(
        self,
        ebene: Mapping[Modell, Stelle],
        gezogenes: Modell,
        ziel: Stelle,
        gegner: Mapping[Modell, Stelle],
    ) -> None:
        weg = messen.wegZwischen(ebene[gezogenes], ziel)
        anteile = self._anteile(ebene, gezogenes, weg, gegner)
        self._angebot = (
            Angebot(frozenset(ebene), gezogenes, ziel)
            if anteile.hältAnDerBewegungsweiteOderNahkampfreichweite
            else None
        )

    def übergangen(
        self, stellen: Mapping[Modell, Stelle], gegner: Mapping[Modell, Stelle]
    ) -> Übergangen | None:
        angebot = self._angebot
        if angebot is None:
            return None
        ebene = {modell: stellen[modell] for modell in angebot.ebene}
        gezogenes = angebot.gezogenes
        weg = messen.wegZwischen(ebene[gezogenes], angebot.punkt)
        kurz = messen.teilDesWegs(weg, anteilBisZurSpielfeldkante(ebene, weg, self._spielfeld))
        fremde = {anderes: ort for anderes, ort in stellen.items() if anderes not in ebene}
        anDerSpielfeldkante = partial(anteilBisZurSpielfeldkante, spielfeld=self._spielfeld)
        neue = gleiten(ebene, kurz, fremde, anDerSpielfeldkante, angehaltenAufDemWeg=False).stellen
        eigene = stellen.keys() - gegner.keys()
        gegangen = messen.wegZwischen(ebene[gezogenes], neue[gezogenes])
        anteile = self._anteile(ebene, gezogenes, gegangen, gegner)
        return Übergangen(
            neue,
            gründeBeimÜbergehen(neue, fremde, eigene),
            anteile.gründeDesAnhaltens,
            gezogenes,
        )

    def _anteile(
        self,
        ebene: Mapping[Modell, Stelle],
        gezogenes: Modell,
        weg: messen.Weg,
        gegner: Mapping[Modell, Stelle],
    ) -> Anteile:
        return Anteile(
            anteilBisZurBewegungsweite(
                ebene, weg, self._stellenZuBeginn, self._vorrückwurfDes(gezogenes)
            ),
            anteilBisZurSpielfeldkante(ebene, weg, self._spielfeld),
            anteilBisZurNahkampfreichweite(ebene, weg, gegner),
        )

    def vorrückenAngeboten(self, einheit: Einheit) -> bool:
        return not self.vorrückenZurücknehmenAngeboten(einheit)

    def vorrückenZurücknehmenAngeboten(self, einheit: Einheit) -> bool:
        return self.wartetAufVorrückwurf(einheit) or self.vorgerückt(einheit)

    def vorrückenBeginnen(self, einheit: Einheit) -> None:
        if self.vorrückenAngeboten(einheit):
            self._wartendeEinheiten.add(einheit)

    def vorrückenZurücknehmen(self, einheit: Einheit) -> None:
        self._wartendeEinheiten.discard(einheit)
        self._vorrückwürfe.pop(einheit, None)

    def wartetAufVorrückwurf(self, einheit: Einheit) -> bool:
        return einheit in self._wartendeEinheiten

    def vorgerückt(self, einheit: Einheit) -> bool:
        return einheit in self._vorrückwürfe

    def vorrückwurf(self, einheit: Einheit) -> int | None:
        return self._vorrückwürfe.get(einheit)

    def _vorrückwurfDes(self, gezogenes: Modell) -> int:
        einheit = einheitDes(gezogenes, self._vorrückwürfe)
        return self._vorrückwürfe[einheit] if einheit else 0

    def stellenMitGründenNachDemZiehen(  # noqa: PLR0913
        self,
        ebene: Mapping[Modell, Stelle],
        gezogenes: Modell,
        ziel: Stelle,
        stellen: Mapping[Modell, Stelle],
        gegner: Mapping[Modell, Stelle],
        weiter: Weiterrücken | None = None,
    ) -> StellenMitGründen:
        weiter = weiter or Weiterrücken(None, angehaltenAufDemWeg=False)
        zuvor = zuvorGezeigt(ebene, gezogenes, weiter)
        fremde = {anderes: ort for anderes, ort in stellen.items() if anderes not in ebene}
        geglitten = gleiten(
            zuvor,
            messen.wegZwischen(zuvor[gezogenes], ziel),
            fremde,
            self._anteilBisZumAnhalten(gezogenes, gegner),
            angehaltenAufDemWeg=weiter.angehaltenAufDemWeg,
        )
        stellenNachV16 = self._anHöchstensBisZumAnhalten(ebene, gezogenes, ziel, gegner)
        gezeigt = Gezeigt(
            geglitten.stellen if geglitten.angehaltenAufDemWeg else stellenNachV16,
            geglitten.angehaltenAufDemWeg,
        )
        eigene = stellen.keys() - gegner.keys()
        return gezeigt, gründeBeimZiehen(ebene, gezeigt.stellen, fremde, eigene)

    def _anHöchstensBisZumAnhalten(
        self,
        ebene: Mapping[Modell, Stelle],
        gezogenes: Modell,
        ziel: Stelle,
        gegner: Mapping[Modell, Stelle],
    ) -> dict[Modell, Stelle]:
        weg = messen.wegZwischen(ebene[gezogenes], ziel)
        kurz = messen.teilDesWegs(weg, min(self._anteile(ebene, gezogenes, weg, gegner)))
        return {modell: messen.verschoben(stelle, kurz) for modell, stelle in ebene.items()}

    def _anteilBisZumAnhalten(
        self, gezogenes: Modell, gegner: Mapping[Modell, Stelle]
    ) -> AnteilBisZumAnhalten:
        def anteil(vorige: Stellen, weg: messen.Weg) -> Fraction:
            return min(self._anteile(vorige, gezogenes, weg, gegner))

        return anteil

    def gründeGegenDasBeenden(
        self, einheiten: Iterable[Einheit], stellen: Mapping[Modell, Stelle]
    ) -> set[Grund]:
        return gründeGegenDasBeenden(einheiten, stellen)

    def stellenZuBeginnDer(self, einheit: Einheit) -> dict[Modell, Stelle]:
        return self._stellenZuBeginnDer(einheit.modelle)

    def grenzenDerEbene(
        self, einheit: Einheit, ebene: Collection[Modell]
    ) -> tuple[Einhüllende, ...]:
        stellen = self._stellenZuBeginnDer(ebene)
        return (grenzeDerBewegung(einheit, stellen), *self._grenzenDerWürfe(einheit, stellen))

    def vorrückwurfNehmen(
        self, einheit: Einheit, ebene: Collection[Modell], stelle: Stelle
    ) -> bool:
        if not self.wartetAufVorrückwurf(einheit):
            return False
        stellen = self._stellenZuBeginnDer(ebene)
        wurf = kleinsterWurfAn(
            stelle,
            grenzeDerBewegung(einheit, stellen),
            self._grenzenDerWürfe(einheit, stellen),
        )
        if wurf is None:
            return False
        self._wartendeEinheiten.discard(einheit)
        self._vorrückwürfe[einheit] = wurf
        return True

    def _stellenZuBeginnDer(self, modelle: Iterable[Modell]) -> dict[Modell, Stelle]:
        return {
            modell: self._stellenZuBeginn[modell]
            for modell in modelle
            if modell in self._stellenZuBeginn
        }

    def _grenzenDerWürfe(
        self, einheit: Einheit, stellen: Mapping[Modell, Stelle]
    ) -> tuple[Einhüllende, ...]:
        if self.wartetAufVorrückwurf(einheit):
            return grenzenDerWürfe(einheit, stellen, möglicheWürfe, wählbar=True)
        wurf = self.vorrückwurf(einheit)
        if wurf is None:
            return ()
        return grenzenDerWürfe(einheit, stellen, [wurf], wählbar=False)
