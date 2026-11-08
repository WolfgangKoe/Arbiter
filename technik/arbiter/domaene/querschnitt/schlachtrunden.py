from enum import Enum
from itertools import pairwise

from arbiter.domaene.missionsvorbereitung.ausgangslage import Ausgangslage
from arbiter.domaene.phasen import einheitVon, gegnerVon
from arbiter.domaene.phasen.aufstellen import Aufstellung
from arbiter.domaene.phasen.aufstellen.anhaltenAufDemWeg import Weiterrücken
from arbiter.domaene.phasen.aufstellen.auswahl import Auswahl
from arbiter.domaene.phasen.bewegung import Bewegungsphase, Gezogen, StellenMitGründen
from arbiter.domaene.phasen.bewegung.grenzkreise import (
    Einhüllende,
    grenzenDerNahkampfreichweite,
)
from arbiter.domaene.querschnitt.kohaerenz import einheitInKohärenz
from arbiter.domaene.querschnitt.setzen import Gezeigt
from arbiter.domaene.querschnitt.uebergehen import Protokoll
from arbiter.domaene.sperre import Sperre
from arbiter.domaene.spielobjekte import Einheit, Modell, Spieler, Stelle


class Phase(Enum):
    kommandophase = "Kommandophase"
    bewegungsphase = "Bewegungsphase"
    psiphase = "Psiphase"
    schussphase = "Schussphase"
    angriffsphase = "Angriffsphase"
    nahkampfphase = "Nahkampfphase"
    moralphase = "Moralphase"


_nächstePhase = dict(pairwise(Phase))
_ersteSchlachtrunde = 1


class Schlacht:
    def __init__(self, aufstellung: Aufstellung) -> None:
        ausgangslage = aufstellung.ausgangslage
        self._ausgangslage = ausgangslage
        self._beideSpieler = (ausgangslage.ersterSpieler, ausgangslage.zweiterSpieler)
        self._stellen = {
            modell: stelle
            for spieler in self._beideSpieler
            for modell in spieler.armee.modelle
            if (stelle := aufstellung.stelle(modell))
        }
        self._bewegungsphase = Bewegungsphase(self._stellen, ausgangslage.spielfeld)
        self._auswahl = Auswahl()
        self._protokoll = Protokoll()
        self._ersterZug: Spieler | None = None
        self._amZug: Spieler | None = None
        self._schlachtrunde = _ersteSchlachtrunde
        self._phase = Phase.kommandophase
        self._beendet = False

    @property
    def ausgangslage(self) -> Ausgangslage:
        return self._ausgangslage

    @property
    def ersterZug(self) -> Spieler | None:
        return self._ersterZug

    @property
    def amZug(self) -> Spieler | None:
        return self._amZug

    @property
    def schlachtrunde(self) -> int:
        return self._schlachtrunde

    @property
    def phase(self) -> Phase:
        return self._phase

    @property
    def protokoll(self) -> Protokoll:
        return self._protokoll

    @property
    def beendet(self) -> bool:
        return self._beendet

    def ersterZugWählen(self, spieler: Spieler) -> None:
        if self._ersterZug is not None:
            return
        self._ersterZug = spieler
        self._amZug = spieler

    def phaseBeenden(self) -> None:
        spieler = self._amZug
        if spieler is None:
            return
        if self._phase is Phase.bewegungsphase:
            gründe = self._bewegungsphase.gründeGegenDasBeenden(
                spieler.armee.einheiten, self._stellen
            )
            if gründe:
                raise Sperre(*gründe)
        self._bewegungsphase.angebotBeenden()
        nächste = _nächstePhase.get(self._phase)
        if nächste is not None:
            self._phase = nächste
            if nächste is Phase.bewegungsphase:
                self._bewegungsphase = Bewegungsphase(self._stellen, self._ausgangslage.spielfeld)
            return
        self._phase = Phase.kommandophase
        self._zugBeenden()

    def gesetzt(self, modell: Modell) -> bool:
        return modell in self._stellen

    def stelle(self, modell: Modell) -> Stelle | None:
        return self._stellen.get(modell)

    def inKohärenz(self, einheit: Einheit) -> bool:
        return einheitInKohärenz(einheit, self._stellen)

    def stellenBeimLoslassen(
        self, modell: Modell, stelle: Stelle, weiter: Weiterrücken | None = None
    ) -> Gezeigt:
        gezeigt, gründe = self._stellenMitGründen(modell, stelle, weiter)
        if gründe:
            raise Sperre(*gründe)
        return gezeigt

    def modellLoslassen(
        self, modell: Modell, stelle: Stelle, weiter: Weiterrücken | None = None
    ) -> None:
        gezeigt, gründe = self._stellenMitGründen(modell, stelle, weiter, losgelassen=True)
        if gründe:
            raise Sperre(*gründe)
        self._bewegungsphase.angebotBeenden()
        if gezeigt.stellen:
            self._bewegungsphase.angebotNachDemZiehen(
                self._gezogen(modell, stelle, weiter), self._stellen, self._stellenDesGegners()
            )
        self._stellen.update(gezeigt.stellen)

    @property
    def gemeinsamÜbergehenAngeboten(self) -> bool:
        return self._bewegungsphase.übergehenAngeboten

    def gemeinsamÜbergehen(self) -> None:
        spieler = self._amZug
        übergangen = self._bewegungsphase.übergangen(self._stellen, self._stellenDesGegners())
        if übergangen is None or spieler is None:
            return
        if übergangen.gründe:
            raise Sperre(*übergangen.gründe)
        self._stellen.update(übergangen.stellen)
        self._bewegungsphase.angebotBeenden()
        einheit = einheitVon(self._beideSpieler, übergangen.gezogenes)
        self._protokoll.eintragen(einheit, spieler, übergangen.angehalten)

    def _ziehtDerSpielerAmZug(self, modell: Modell) -> bool:
        spieler = self._amZug
        return (
            self._phase is Phase.bewegungsphase
            and spieler is not None
            and modell in spieler.armee.modelle
        )

    def _ebeneDes(self, modell: Modell) -> dict[Modell, Stelle]:
        einheit = einheitVon(self._beideSpieler, modell)
        return self._auswahl.ebene(einheit, modell, self._stellen)

    def _stellenDesGegners(self) -> dict[Modell, Stelle]:
        spieler = self._amZug
        return {
            anderes: ort
            for anderes, ort in self._stellen.items()
            if spieler is None or anderes not in spieler.armee.modelle
        }

    def _gezogen(self, modell: Modell, stelle: Stelle, weiter: Weiterrücken | None) -> Gezogen:
        einheit = einheitVon(self._beideSpieler, modell)
        return Gezogen(self._ebeneDes(modell), modell, stelle, weiter, einheit.fliegen)

    def _stellenMitGründen(
        self,
        modell: Modell,
        stelle: Stelle,
        weiter: Weiterrücken | None,
        *,
        losgelassen: bool = False,
    ) -> StellenMitGründen:
        if not self._ziehtDerSpielerAmZug(modell):
            return Gezeigt({}, angehaltenAufDemWeg=False), set()
        gezogen = self._gezogen(modell, stelle, weiter)
        berechnen = (
            self._bewegungsphase.stellenMitGründenNachDemLoslassen
            if losgelassen
            else self._bewegungsphase.stellenMitGründenNachDemZiehen
        )
        return berechnen(gezogen, self._stellen, self._stellenDesGegners())

    def modellAnklicken(self, modell: Modell) -> None:
        self._auswahl.modellAnklicken(self._beideSpieler, modell, self._stellen)

    def ausgewählt(self, einheit: Einheit) -> bool:
        return self._auswahl.ausgewählt(einheit)

    def hatEinheitenebene(self, einheit: Einheit) -> bool:
        return self._auswahl.hatEinheitenebene(einheit)

    def istModellebene(self, modell: Modell) -> bool:
        return self._auswahl.istModellebene(modell)

    def modellAusgewählt(self, modell: Modell) -> bool:
        return self._auswahl.modellAusgewählt(modell)

    def auswählen(self, einheit: Einheit) -> None:
        self._auswahl.auswählen(einheit)

    def spielfeldAnklicken(self, stelle: Stelle) -> None:
        self._bewegungsphase.angebotBeenden()
        einheit = self._ausgewählteEinheitAmZug()
        if einheit is not None:
            ebene = self._auswahl.ebeneDerAuswahl(self._stellen)
            if self._bewegungsphase.vorrückwurfNehmen(einheit, ebene, stelle):
                return
        self._auswahl.auswahlAufheben()

    @property
    def grenzen(self) -> tuple[Einhüllende, ...]:
        einheit = self._ausgewählteEinheitAmZug()
        if einheit is None:
            return ()
        ebene = self._auswahl.ebeneDerAuswahl(self._stellen)
        gegner = gegnerVon(self._beideSpieler, self._amZug)
        return (
            *self._bewegungsphase.grenzenDerEbene(einheit, ebene),
            *grenzenDerNahkampfreichweite(gegner.armee.einheiten, self._stellen),
        )

    @property
    def vorrückenAngeboten(self) -> bool:
        einheit = self._ausgewählteEinheitAmZug()
        return einheit is not None and self._bewegungsphase.vorrückenAngeboten(
            einheit, self._stellen, self._stellenDesGegners()
        )

    @property
    def vorrückenZurücknehmenAngeboten(self) -> bool:
        einheit = self._ausgewählteEinheitAmZug()
        return einheit is not None and self._bewegungsphase.vorrückenZurücknehmenAngeboten(einheit)

    @property
    def einheitZurücksetzenAngeboten(self) -> bool:
        einheit = self._ausgewählteEinheitAmZug()
        return einheit is not None and self._bewegungsphase.einheitZurücksetzenAngeboten(
            einheit, self._stellen
        )

    def wartetAufVorrückwurf(self, einheit: Einheit) -> bool:
        return self._bewegungsphase.wartetAufVorrückwurf(einheit)

    def vorgerückt(self, einheit: Einheit) -> bool:
        return self._bewegungsphase.vorgerückt(einheit)

    def vorrückwurf(self, einheit: Einheit) -> int | None:
        return self._bewegungsphase.vorrückwurf(einheit)

    def vorrücken(self) -> None:
        self._bewegungsphase.angebotBeenden()
        einheit = self._ausgewählteEinheitAmZug()
        if einheit is None:
            return
        self._bewegungsphase.vorrückenBeginnen(einheit, self._stellen, self._stellenDesGegners())

    def vorrückenZurücknehmen(self) -> None:
        self._bewegungsphase.angebotBeenden()
        einheit = self._ausgewählteEinheitAmZug()
        if einheit is None or not self._bewegungsphase.vorrückenZurücknehmenAngeboten(einheit):
            return
        self._bewegungsphase.vorrückenZurücknehmen(einheit)
        self._stellen.update(self._bewegungsphase.stellenZuBeginnDer(einheit))

    def einheitZurücksetzen(self) -> None:
        self._bewegungsphase.angebotBeenden()
        einheit = self._ausgewählteEinheitAmZug()
        if einheit is None or not self._bewegungsphase.einheitZurücksetzenAngeboten(
            einheit, self._stellen
        ):
            return
        self._stellen.update(self._bewegungsphase.stellenZuBeginnDer(einheit))

    def _ausgewählteEinheitAmZug(self) -> Einheit | None:
        spieler = self._amZug
        einheit = self._auswahl.einheit
        if self._phase is not Phase.bewegungsphase or spieler is None or einheit is None:
            return None
        return einheit if einheit in spieler.armee.einheiten else None

    def _zugBeenden(self) -> None:
        if self._amZug is self._ersterZug:
            self._amZug = gegnerVon(self._beideSpieler, self._ersterZug)
            return
        if self._schlachtrunde == self._ausgangslage.letzteSchlachtrunde:
            self._amZug = None
            self._beendet = True
            return
        self._schlachtrunde += 1
        self._amZug = self._ersterZug
