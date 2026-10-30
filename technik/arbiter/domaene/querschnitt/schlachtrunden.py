from collections.abc import Mapping
from enum import Enum
from itertools import pairwise

from arbiter.domaene.missionsvorbereitung.ausgangslage import Ausgangslage
from arbiter.domaene.phasen import einheitVon
from arbiter.domaene.phasen.aufstellen import Aufstellung
from arbiter.domaene.phasen.aufstellen.auswahl import Auswahl
from arbiter.domaene.phasen.aufstellen.reihenfolge import gegnerVon
from arbiter.domaene.phasen.bewegung import Bewegungsphase, StellenMitGründen
from arbiter.domaene.querschnitt.kohaerenz import einheitInKohärenz
from arbiter.domaene.querschnitt.uebergehen import Protokoll
from arbiter.domaene.sperre import Grund, Sperre
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

    def stellenBeimLoslassen(self, modell: Modell, stelle: Stelle) -> Mapping[Modell, Stelle]:
        neue, gründe = self._stellenMitGründen(modell, stelle)
        if gründe:
            raise Sperre(*gründe)
        return neue

    def modellLoslassen(
        self, modell: Modell, stelle: Stelle, übergehen: frozenset[Grund] = frozenset()
    ) -> None:
        neue, gründe = self._stellenMitGründen(modell, stelle)
        sperre = Sperre(*gründe, übergehbar=True) if gründe else None
        if sperre and not (sperre.übergehbar and gründe <= übergehen):
            raise sperre
        self._stellen.update(neue)
        if gründe and self._amZug is not None:
            einheit = einheitVon(self._beideSpieler, modell)
            self._protokoll.eintragen(einheit, self._amZug, frozenset(gründe))

    def _stellenMitGründen(self, modell: Modell, stelle: Stelle) -> StellenMitGründen:
        spieler = self._amZug
        if self._phase is not Phase.bewegungsphase or spieler is None:
            return {}, set()
        if modell not in spieler.armee.modelle:
            return {}, set()
        einheit = einheitVon(self._beideSpieler, modell)
        ebene = self._auswahl.ebene(einheit, modell, self._stellen)
        return self._bewegungsphase.stellenMitGründenNachDemZiehen(
            ebene, modell, stelle, self._stellen, spieler.armee.modelle
        )

    def modellAnklicken(self, modell: Modell) -> None:
        if self.gesetzt(modell):
            self._auswahl.modellAnklicken(einheitVon(self._beideSpieler, modell), modell)

    def ausgewählt(self, einheit: Einheit) -> bool:
        return self._auswahl.ausgewählt(einheit)

    def ganzeEinheitIstEbene(self, einheit: Einheit) -> bool:
        return self._auswahl.ganzeEinheitIstEbene(einheit)

    def modellIstEbene(self, modell: Modell) -> bool:
        return self._auswahl.modellIstEbene(modell)

    def modellAusgewählt(self, modell: Modell) -> bool:
        return self._auswahl.modellAusgewählt(modell)

    def auswählen(self, einheit: Einheit) -> None:
        self._auswahl.auswählen(einheit)

    def karteAnklicken(self, _stelle: Stelle) -> None:
        self._auswahl.auswahlAufheben()

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
