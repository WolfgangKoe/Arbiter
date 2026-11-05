from collections.abc import Callable, Collection, Iterable, Mapping
from dataclasses import dataclass
from fractions import Fraction
from functools import partial

from arbiter.domaene import messen
from arbiter.domaene.phasen.aufstellen.anhaltenAufDemWeg import (
    AnteilBisZumAnhalten,
    Stellen,
    Weiterrücken,
    gleiten,
    umFremdeGleiten,
    zuvorGezeigt,
    überdecktFremde,
)
from arbiter.domaene.phasen.bewegung.anhaltenAnDerBewegungsweite import (
    anteilBisZurBewegungsweite,
)
from arbiter.domaene.phasen.bewegung.anhaltenVorDerGrenze import (
    anteilBisZurNahkampfreichweite,
    anteilBisZurSpielfeldkante,
)
from arbiter.domaene.phasen.bewegung.beenden import gründeGegenDasBeenden
from arbiter.domaene.phasen.bewegung.einheitZuruecksetzen import stehtNichtWieZuBeginn
from arbiter.domaene.phasen.bewegung.fliegen import (
    Umgebung,
    Weite,
    nachFremdenBasesGerückt,
)
from arbiter.domaene.phasen.bewegung.fliegen import (
    anteilBisZurNahkampfreichweite as anteilBisZurNahkampfreichweiteDesFliegers,
)
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


@dataclass(frozen=True)
class Gezogen:
    ebene: Mapping[Modell, Stelle]
    gezogenes: Modell
    ziel: Stelle
    weiter: Weiterrücken | None = None
    fliegen: bool = False


type EndeDerStrecke = Callable[[Fraction, Fraction], Fraction]


def _nurSpielfeldkante(_bewegungsweite: Fraction, spielfeldkante: Fraction) -> Fraction:
    return spielfeldkante


def _verschobenUm(stellen: Mapping[Modell, Stelle], weg: messen.Weg) -> dict[Modell, Stelle]:
    return {modell: messen.verschoben(stelle, weg) for modell, stelle in stellen.items()}


def _gekürztAnDerNahkampfreichweite(
    zuvor: Mapping[Modell, Stelle],
    halt: Mapping[Modell, Stelle],
    gezogenes: Modell,
    gegner: Mapping[Modell, Stelle],
) -> tuple[dict[Modell, Stelle], bool]:
    weg = messen.wegZwischen(zuvor[gezogenes], halt[gezogenes])
    anteil = anteilBisZurNahkampfreichweite(zuvor, weg, gegner)
    return _verschobenUm(zuvor, messen.teilDesWegs(weg, anteil)), anteil < 1


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
        _, hältAnDerGrenze = self._gezeigt(gezogen, stellen, gegner)
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
        weg = messen.wegZwischen(ebene[gezogenes], angebot.punkt)
        kurz = messen.teilDesWegs(weg, anteilBisZurSpielfeldkante(ebene, weg, self._spielfeld))
        fremde = {anderes: ort for anderes, ort in stellen.items() if anderes not in ebene}
        eigene = stellen.keys() - gegner.keys()
        if angebot.fliegen:
            gesetzt = _verschobenUm(ebene, kurz)
            zurück = messen.wegZwischen(gesetzt[gezogenes], ebene[gezogenes])
            neue = self._nachFremdenBasesGerückt(gesetzt, zurück, fremde, gegner, {})
        else:
            anDerSpielfeldkante = partial(anteilBisZurSpielfeldkante, spielfeld=self._spielfeld)
            neue = gleiten(
                ebene, kurz, fremde, anDerSpielfeldkante, angehaltenAufDemWeg=False
            ).stellen
        gegangen = messen.wegZwischen(ebene[gezogenes], neue[gezogenes])
        anteile = self._anteile(
            ebene,
            gezogenes,
            gegangen,
            gegner,
            endeDerStrecke=_nurSpielfeldkante if angebot.fliegen else None,
        )
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
        *,
        endeDerStrecke: EndeDerStrecke | None = None,
    ) -> Anteile:
        bewegungsweite = anteilBisZurBewegungsweite(
            ebene, weg, self._stellenZuBeginn, self._vorrückwurfDes(gezogenes)
        )
        spielfeldkante = anteilBisZurSpielfeldkante(ebene, weg, self._spielfeld)
        if endeDerStrecke:
            nahkampfreichweite = anteilBisZurNahkampfreichweiteDesFliegers(
                ebene, weg, gegner, endeDerStrecke(bewegungsweite, spielfeldkante)
            )
        else:
            nahkampfreichweite = anteilBisZurNahkampfreichweite(ebene, weg, gegner)
        return Anteile(bewegungsweite, spielfeldkante, nahkampfreichweite)

    def _nachFremdenBasesGerückt(
        self,
        gesetzt: Mapping[Modell, Stelle],
        zurück: messen.Weg,
        fremde: Mapping[Modell, Stelle],
        gegner: Mapping[Modell, Stelle],
        weiten: Mapping[Modell, Weite],
    ) -> Mapping[Modell, Stelle]:
        umgebung = Umgebung(fremde, gegner, self._spielfeld, weiten)
        return nachFremdenBasesGerückt(gesetzt, zurück, umgebung)

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
        gezeigt, _ = self._gezeigt(gezogen, stellen, gegner)
        return gezeigt, self._gründe(gezogen, gezeigt.stellen, stellen, gegner)

    def stellenMitGründenNachDemLoslassen(
        self,
        gezogen: Gezogen,
        stellen: Mapping[Modell, Stelle],
        gegner: Mapping[Modell, Stelle],
    ) -> StellenMitGründen:
        gezeigt, gründe = self.stellenMitGründenNachDemZiehen(gezogen, stellen, gegner)
        if not gezogen.fliegen:
            return gezeigt, gründe
        ebene = gezogen.ebene
        fremde = {anderes: ort for anderes, ort in stellen.items() if anderes not in ebene}
        vorrückwurf = self._vorrückwurfDes(gezogen.gezogenes)
        weiten = {
            modell: Weite(
                self._stellenZuBeginn[modell], Fraction(modell.bewegungsweite + vorrückwurf)
            )
            for modell in ebene
        }
        zurück = messen.wegZwischen(gezeigt.stellen[gezogen.gezogenes], ebene[gezogen.gezogenes])
        gerückt = self._nachFremdenBasesGerückt(gezeigt.stellen, zurück, fremde, gegner, weiten)
        gründeNachDemRücken = self._gründe(gezogen, gerückt, stellen, gegner, mitBaseÜberdeckt=True)
        return Gezeigt(dict(gerückt), angehaltenAufDemWeg=False), gründeNachDemRücken

    def _gründe(
        self,
        gezogen: Gezogen,
        gesetzt: Mapping[Modell, Stelle],
        stellen: Mapping[Modell, Stelle],
        gegner: Mapping[Modell, Stelle],
        *,
        mitBaseÜberdeckt: bool = False,
    ) -> set[Grund]:
        fremde = {anderes: ort for anderes, ort in stellen.items() if anderes not in gezogen.ebene}
        eigene = stellen.keys() - gegner.keys()
        gründe = gründeBeimZiehen(gezogen.ebene, gesetzt, fremde, eigene)
        if gezogen.fliegen and not mitBaseÜberdeckt:
            return gründe - {Grund.baseÜberdeckt}
        return gründe

    def _gezeigtBeimFliegen(
        self, gezogen: Gezogen, gegner: Mapping[Modell, Stelle]
    ) -> tuple[Gezeigt, bool]:
        ebene, gezogenes = gezogen.ebene, gezogen.gezogenes
        weg = messen.wegZwischen(ebene[gezogenes], gezogen.ziel)
        anteile = self._anteile(ebene, gezogenes, weg, gegner, endeDerStrecke=min)
        halt = _verschobenUm(ebene, messen.teilDesWegs(weg, min(anteile)))
        hält = anteile.hältAnDerBewegungsweiteOderNahkampfreichweite
        return Gezeigt(halt, angehaltenAufDemWeg=False), hält

    def _gezeigt(
        self,
        gezogen: Gezogen,
        stellen: Mapping[Modell, Stelle],
        gegner: Mapping[Modell, Stelle],
    ) -> tuple[Gezeigt, bool]:
        if gezogen.fliegen:
            return self._gezeigtBeimFliegen(gezogen, gegner)
        ebene, gezogenes, ziel = gezogen.ebene, gezogen.gezogenes, gezogen.ziel
        weiter = gezogen.weiter or Weiterrücken(None, angehaltenAufDemWeg=False)
        zuvor = zuvorGezeigt(ebene, gezogenes, weiter)
        fremde = {anderes: ort for anderes, ort in stellen.items() if anderes not in ebene}
        start = ebene
        weg = messen.wegZwischen(start[gezogenes], ziel)
        anteile = self._anteile(start, gezogenes, weg, gegner)
        halt = _verschobenUm(start, messen.teilDesWegs(weg, min(anteile)))
        hältAnDerGrenze = anteile.hältAnDerBewegungsweiteOderNahkampfreichweite
        if weiter.angehaltenAufDemWeg:
            halt, nahkampfreichweiteHält = _gekürztAnDerNahkampfreichweite(
                zuvor, halt, gezogenes, gegner
            )
            hältAnDerGrenze = hältAnDerGrenze or nahkampfreichweiteHält
        if not überdecktFremde(zuvor, halt, fremde):
            return Gezeigt(halt, weiter.angehaltenAufDemWeg), hältAnDerGrenze
        wegAbZuvor = messen.wegZwischen(zuvor[gezogenes], ziel)
        geglitten = umFremdeGleiten(
            zuvor, wegAbZuvor, fremde, self._anteilBisZumAnhalten(gezogenes, gegner)
        )
        anteileAbZuvor = self._anteile(zuvor, gezogenes, wegAbZuvor, gegner)
        stelleDesAnteils = messen.verschoben(
            zuvor[gezogenes], messen.teilDesWegs(wegAbZuvor, min(anteileAbZuvor))
        )
        hältAnDerGrenze = (
            anteileAbZuvor.hältAnDerBewegungsweiteOderNahkampfreichweite
            and geglitten.stellen[gezogenes] == stelleDesAnteils
        )
        return Gezeigt(geglitten.stellen, geglitten.angehaltenAufDemWeg), hältAnDerGrenze

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
