"""Die Schlacht: wer am Zug ist, in welcher Schlachtrunde und Phase (QUE-9, QUE-10)."""

from collections.abc import Mapping
from enum import Enum
from itertools import pairwise

from arbiter.domaene.missionsvorbereitung.ausgangslage import Ausgangslage
from arbiter.domaene.phasen.aufstellen import Aufstellung
from arbiter.domaene.phasen.aufstellen.auswahl import Auswahl
from arbiter.domaene.phasen.aufstellen.beenden import gesetzteModelle
from arbiter.domaene.phasen.aufstellen.einheitVerschieben import verschobeneStellen
from arbiter.domaene.phasen.aufstellen.reihenfolge import einheitVon
from arbiter.domaene.phasen.bewegung.anhaltenAnDerBewegungsweite import (
    anDerBewegungsweiteAngehalten,
)
from arbiter.domaene.phasen.bewegung.beenden import gründeGegenDasBeenden
from arbiter.domaene.phasen.bewegung.sperrenBeimZiehen import gründeBeimZiehen
from arbiter.domaene.querschnitt.kohaerenz import inKohärenz
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
    """Übernimmt die Stellen der beendeten Aufstellung und führt durch Züge und Phasen."""

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
        self._stellenZuBeginn = dict(self._stellen)
        self._auswahl = Auswahl()
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
            gründe = gründeGegenDasBeenden(spieler.armee.einheiten, self._stellen)
            if gründe:
                raise Sperre(*gründe)
        nächste = _nächstePhase.get(self._phase)
        if nächste is not None:
            self._phase = nächste
            if nächste is Phase.bewegungsphase:
                self._stellenZuBeginn = dict(self._stellen)
            return
        self._phase = Phase.kommandophase
        self._zugBeenden()

    def gesetzt(self, modell: Modell) -> bool:
        return modell in self._stellen

    def stelle(self, modell: Modell) -> Stelle | None:
        return self._stellen.get(modell)

    def inKohärenz(self, einheit: Einheit) -> bool:
        return inKohärenz(gesetzteModelle(einheit, self._stellen))

    def stellenBeimLoslassen(self, modell: Modell, stelle: Stelle) -> Mapping[Modell, Stelle]:
        """Die Stellen, an die `modellLoslassen` die Modelle setzen würde (QUE-10.5)."""
        spieler = self._amZug
        if self._phase is not Phase.bewegungsphase or spieler is None:
            return {}
        if modell not in spieler.armee.modelle:
            return {}
        einheit = einheitVon(self._beideSpieler, modell)
        ebene = self._ebeneVon(einheit, modell)
        verschoben = verschobeneStellen(ebene, modell, stelle)
        neue = anDerBewegungsweiteAngehalten(ebene, verschoben, self._stellenZuBeginn)
        fremde = {anderes: ort for anderes, ort in self._stellen.items() if anderes not in neue}
        gründe = gründeBeimZiehen(ebene, neue, fremde, spieler.armee.modelle)
        if gründe:
            raise Sperre(*gründe)
        return neue

    def modellLoslassen(self, modell: Modell, stelle: Stelle) -> None:
        self._stellen.update(self.stellenBeimLoslassen(modell, stelle))

    def modellAnklicken(self, modell: Modell) -> None:
        if self.gesetzt(modell):
            self._auswahl.auswählen(einheitVon(self._beideSpieler, modell))

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

    def _ebeneVon(self, einheit: Einheit, modell: Modell) -> dict[Modell, Stelle]:
        """Die Stellen der Modelle, die Ziehen bewegt: die ganze Einheit oder das eine Modell."""
        if self.ganzeEinheitIstEbene(einheit):
            return gesetzteModelle(einheit, self._stellen)
        return {modell: self._stellen[modell]}

    def _zugBeenden(self) -> None:
        if self._amZug is self._ersterZug:
            ersterSpieler, zweiterSpieler = self._beideSpieler
            self._amZug = zweiterSpieler if self._ersterZug is ersterSpieler else ersterSpieler
            return
        if self._schlachtrunde == self._ausgangslage.letzteSchlachtrunde:
            self._amZug = None
            self._beendet = True
            return
        self._schlachtrunde += 1
        self._amZug = self._ersterZug
