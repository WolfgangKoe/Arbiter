from collections.abc import Collection, Iterable, Mapping
from dataclasses import replace
from fractions import Fraction
from functools import partial

from arbiter.domaene import messen
from arbiter.domaene.phasen.bewegung.anhaltenAnDerBewegungsweite import (
    anteilBisZurBewegungsweite,
)
from arbiter.domaene.phasen.bewegung.anhaltenVorDerGrenze import anteilBisZurSpielfeldkante
from arbiter.domaene.phasen.bewegung.anhaltenVorFremdenBases import Gleiten
from arbiter.domaene.phasen.bewegung.beenden import gründeGegenDasBeenden
from arbiter.domaene.phasen.bewegung.einheitZuruecksetzen import stehtNichtWieZuBeginn
from arbiter.domaene.phasen.bewegung.fliegen import Fliegen
from arbiter.domaene.phasen.bewegung.grenzkreise import (
    Einhüllende,
    grenzeDerBewegung,
    grenzenDerWürfe,
    kleinsterWurfAn,
    möglicheWürfe,
)
from arbiter.domaene.phasen.bewegung.keinVorrueckenAusDerNahkampfreichweite import (
    einModellInNahkampfreichweite,
)
from arbiter.domaene.phasen.bewegung.normaleBewegung import (
    Gezogen,
    Umgebung,
    Weite,
    gründeBeimZiehen,
)
from arbiter.domaene.phasen.bewegung.uebergehenBeimZiehen import (
    Angebot,
    Übergangen,
    gründeBeimÜbergehen,
)
from arbiter.domaene.querschnitt.setzen import Gezeigt
from arbiter.domaene.sperre import Grund
from arbiter.domaene.spielobjekte import Einheit, Modell, Spielfeld, Stelle, einheitDes

StellenMitGründen = tuple[Gezeigt, set[Grund]]


def _fremdeDer(
    ebene: Mapping[Modell, Stelle], stellen: Mapping[Modell, Stelle]
) -> dict[Modell, Stelle]:
    return {anderes: ort for anderes, ort in stellen.items() if anderes not in ebene}


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
        gezogen: Gezogen,
        stellen: Mapping[Modell, Stelle],
        gegner: Mapping[Modell, Stelle],
    ) -> None:
        _, hältAnDerGrenze = self._art(gezogen, stellen, gegner).gezeigt()
        self._angebot = (
            Angebot(frozenset(gezogen.ebene), gezogen.gezogenes, gezogen.ziel, gezogen.fliegen)
            if hältAnDerGrenze
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
        gezogen = Gezogen(ebene, gezogenes, angebot.punkt, fliegen=angebot.fliegen)
        art = self._art(gezogen, stellen, gegner)
        weg = messen.wegZwischen(ebene[gezogenes], angebot.punkt)
        kurz = messen.teilDesWegs(weg, anteilBisZurSpielfeldkante(ebene, weg, self._spielfeld))
        neue = art.übergangen(kurz)
        gegangen = messen.wegZwischen(ebene[gezogenes], neue[gezogenes])
        return Übergangen(
            dict(neue),
            gründeBeimÜbergehen(neue, _fremdeDer(ebene, stellen), stellen.keys() - gegner.keys()),
            art.anteileBeimÜbergehen(gegangen).gründeDesAnhaltens,
            gezogenes,
        )

    def _art(
        self,
        gezogen: Gezogen,
        stellen: Mapping[Modell, Stelle],
        gegner: Mapping[Modell, Stelle],
    ) -> Gleiten | Fliegen:
        umgebung = Umgebung(_fremdeDer(gezogen.ebene, stellen), gegner, self._spielfeld)
        bewegungsweite = partial(
            anteilBisZurBewegungsweite,
            anfang=self._stellenZuBeginn,
            vorrückwurf=self._vorrückwurfDes(gezogen.gezogenes),
        )
        spielfeldkante = partial(anteilBisZurSpielfeldkante, spielfeld=self._spielfeld)
        if gezogen.fliegen:
            mitWeiten = replace(umgebung, weiten=self._weitenDer(gezogen))
            return Fliegen(gezogen, mitWeiten, bewegungsweite, spielfeldkante)
        return Gleiten(gezogen, umgebung, bewegungsweite, spielfeldkante)

    def _weitenDer(self, gezogen: Gezogen) -> dict[Modell, Weite]:
        vorrückwurf = self._vorrückwurfDes(gezogen.gezogenes)
        return {
            modell: Weite(
                self._stellenZuBeginn[modell], Fraction(modell.bewegungsweite + vorrückwurf)
            )
            for modell in gezogen.ebene
        }

    def vorrückenAngeboten(
        self, einheit: Einheit, stellen: Mapping[Modell, Stelle], gegner: Mapping[Modell, Stelle]
    ) -> bool:
        return not self.vorrückenZurücknehmenAngeboten(
            einheit
        ) and not einModellInNahkampfreichweite(einheit, stellen, gegner)

    def vorrückenZurücknehmenAngeboten(self, einheit: Einheit) -> bool:
        return self.wartetAufVorrückwurf(einheit) or self.vorgerückt(einheit)

    def einheitZurücksetzenAngeboten(
        self, einheit: Einheit, stellen: Mapping[Modell, Stelle]
    ) -> bool:
        return not self.vorrückenZurücknehmenAngeboten(einheit) and stehtNichtWieZuBeginn(
            einheit, stellen, self._stellenZuBeginn
        )

    def vorrückenBeginnen(
        self, einheit: Einheit, stellen: Mapping[Modell, Stelle], gegner: Mapping[Modell, Stelle]
    ) -> None:
        if self.vorrückenAngeboten(einheit, stellen, gegner):
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

    def stellenMitGründenNachDemZiehen(
        self,
        gezogen: Gezogen,
        stellen: Mapping[Modell, Stelle],
        gegner: Mapping[Modell, Stelle],
    ) -> StellenMitGründen:
        art = self._art(gezogen, stellen, gegner)
        gezeigt, _ = art.gezeigt()
        return gezeigt, art.gründeBeimZiehen(gezeigt.stellen, stellen.keys() - gegner.keys())

    def stellenMitGründenNachDemLoslassen(
        self,
        gezogen: Gezogen,
        stellen: Mapping[Modell, Stelle],
        gegner: Mapping[Modell, Stelle],
    ) -> StellenMitGründen:
        art = self._art(gezogen, stellen, gegner)
        gezeigt, _ = art.gezeigt()
        gerückt = art.nachDemLoslassen(gezeigt)
        gründe = gründeBeimZiehen(
            gezogen.ebene,
            gerückt.stellen,
            _fremdeDer(gezogen.ebene, stellen),
            stellen.keys() - gegner.keys(),
        )
        return gerückt, gründe

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
