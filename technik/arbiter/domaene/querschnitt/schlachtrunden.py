"""Die Schlacht: wer am Zug ist, in welcher Schlachtrunde und Phase (QUE-9, QUE-10)."""

from collections.abc import Mapping
from enum import Enum

from arbiter.domaene.missionsvorbereitung.ausgangslage import Ausgangslage
from arbiter.domaene.phasen.aufstellen import Aufstellung
from arbiter.domaene.phasen.aufstellen.auswahl import Auswahl
from arbiter.domaene.spielobjekte import Einheit, Modell, Spieler, Stelle


class Phase(Enum):
    kommandophase = "Kommandophase"
    bewegungsphase = "Bewegungsphase"
    psiphase = "Psiphase"
    schussphase = "Schussphase"
    angriffsphase = "Angriffsphase"
    nahkampfphase = "Nahkampfphase"
    moralphase = "Moralphase"


_phasen = tuple(Phase)
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
        if self._amZug is None:
            return
        if self._phase is not _phasen[-1]:
            self._phase = _phasen[_phasen.index(self._phase) + 1]
            return
        self._phase = _phasen[0]
        self._zugBeenden()

    def gesetzt(self, modell: Modell) -> bool:
        return modell in self._stellen

    def stelle(self, modell: Modell) -> Stelle | None:
        return self._stellen.get(modell)

    def stellenBeimLoslassen(self, modell: Modell, stelle: Stelle) -> Mapping[Modell, Stelle]:
        """Außerhalb der Bewegungsphase bewegt sich kein Modell (QUE-10.5)."""
        del modell, stelle
        return {}

    def modellLoslassen(self, modell: Modell, stelle: Stelle) -> None:
        """Außerhalb der Bewegungsphase ändert Loslassen nichts (QUE-10.5)."""
        del modell, stelle

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

    def abwählen(self, einheit: Einheit) -> None:
        self._auswahl.abwählen(einheit)

    def ebeneWählen(self, modell: Modell) -> None:
        self._auswahl.ebeneWählen(modell)

    def ebeneAbwählen(self, modell: Modell) -> None:
        self._auswahl.ebeneAbwählen(modell)

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
