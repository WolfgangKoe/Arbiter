from enum import Enum

from arbiter.domaene.sperre import Grund, Sperre
from arbiter.domaene.spielobjekte import Einheit, Modell, Spieler


class Aufstellungszone(Enum):
    nord = "nord"
    süd = "süd"


class Aufstellung:
    def __init__(self, ersterSpieler: Spieler, zweiterSpieler: Spieler) -> None:
        self.spieler = (ersterSpieler, zweiterSpieler)
        self.gewinner: Spieler | None = None
        self.einheitInAufstellung: Einheit | None = None
        self.anDerReihe: Spieler | None = None
        self.beendet = False
        self._zoneDesGewinners: Aufstellungszone | None = None

    def gewinnerWählen(self, gewinner: Spieler) -> None:
        if self.gewinner is not None:
            raise Sperre(Grund.nichtWählbar)
        self.gewinner = gewinner

    def aufstellungszoneWählen(self, zone: Aufstellungszone) -> None:
        if self.gewinner is None or self._zoneDesGewinners is not None:
            raise Sperre(Grund.nichtWählbar)
        self._zoneDesGewinners = zone
        self.anDerReihe = self._gegnerVon(self.gewinner)

    def aufstellungszone(self, spieler: Spieler) -> Aufstellungszone | None:
        if self._zoneDesGewinners is None:
            return None
        if spieler is self.gewinner:
            return self._zoneDesGewinners
        return next(zone for zone in Aufstellungszone if zone is not self._zoneDesGewinners)

    def einheitInAufstellungWählen(self, einheit: Einheit) -> None:
        if self.anDerReihe is None or einheit.aufgestellt:
            raise Sperre(Grund.nichtWählbar)
        if einheit not in self.anDerReihe.armee.einheiten:
            raise Sperre(Grund.nichtWählbar)
        if self.einheitInAufstellung is not None and self.einheitInAufstellung.begonnen:
            raise Sperre(Grund.einheitBegonnen)
        self.einheitInAufstellung = einheit

    def modellSetzen(self, modell: Modell) -> None:
        einheit = self.einheitInAufstellung
        if einheit is None or modell not in einheit.modelle:
            raise Sperre(Grund.nichtInAufstellung)
        modell.gesetzt = True

    def aufstellenDerEinheitBeenden(self) -> None:
        if self.einheitInAufstellung is None or self.anDerReihe is None:
            raise Sperre(Grund.nichtInAufstellung)
        self.einheitInAufstellung.aufgestellt = True
        self.einheitInAufstellung = None
        self.anDerReihe = self._nächsterAnDerReihe(self.anDerReihe)
        self.beendet = self.anDerReihe is None

    def _gegnerVon(self, spieler: Spieler) -> Spieler:
        return next(andere for andere in self.spieler if andere is not spieler)

    def _nächsterAnDerReihe(self, bisher: Spieler) -> Spieler | None:
        gegner = self._gegnerVon(bisher)
        for kandidat in (gegner, bisher):
            if kandidat.armee.hatEinheitenZumAufstellen:
                return kandidat
        return None
