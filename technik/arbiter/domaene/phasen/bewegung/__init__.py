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
from arbiter.domaene.phasen.bewegung.grenzkreise import (
    Einhüllende,
    grenzeDerBewegung,
    grenzenDerWürfe,
    kleinsterWurfAn,
    möglicheWürfe,
)
from arbiter.domaene.phasen.bewegung.sperrenBeimZiehen import gründeBeimZiehen
from arbiter.domaene.sperre import Grund
from arbiter.domaene.spielobjekte import Einheit, Modell, Spielfeld, Stelle

StellenMitGründen = tuple[dict[Modell, Stelle], set[Grund]]


class Bewegungsphase:
    def __init__(self, stellen: Mapping[Modell, Stelle], spielfeld: Spielfeld) -> None:
        self._spielfeld = spielfeld
        self._stellenZuBeginn = dict(stellen)
        self._wartendeEinheiten: set[Einheit] = set()
        self._vorrückwürfe: dict[Einheit, int] = {}

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
        return next(
            (wurf for einheit, wurf in self._vorrückwürfe.items() if gezogenes in einheit.modelle),
            0,
        )

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
            anteilBisZurBewegungsweite(
                ebene, weg, self._stellenZuBeginn, self._vorrückwurfDes(gezogenes)
            ),
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
