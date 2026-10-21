"""Die Phase Aufstellen: Wahlen, Setzen und Auswählen (AUF)."""

from collections.abc import Mapping

from arbiter.domaene.missionsvorbereitung.ausgangslage import (
    Aufstellungszone,
    Ausgangslage,
    Grenzen,
)
from arbiter.domaene.phasen.aufstellen.anhaltenAnEinerBase import angehalten
from arbiter.domaene.phasen.aufstellen.auswahl import Auswahl
from arbiter.domaene.phasen.aufstellen.beenden import gesetzteModelle, gründeGegenDasBeenden
from arbiter.domaene.phasen.aufstellen.einheitInAufstellung import prüfenDassWählbar
from arbiter.domaene.phasen.aufstellen.einheitVerschieben import (
    hineingerückt,
    verschobeneStellen,
)
from arbiter.domaene.phasen.aufstellen.reihenfolge import (
    einheitVon,
    nächsterAnDerReihe,
    zonenVerteilen,
)
from arbiter.domaene.phasen.aufstellen.setzenPerKlick import formationDerEinheit
from arbiter.domaene.phasen.aufstellen.sperrenBeimSetzen import gründeGegenDieStelle
from arbiter.domaene.querschnitt.kohaerenz import inKohärenz
from arbiter.domaene.sperre import Grund, Sperre
from arbiter.domaene.spielobjekte import Einheit, Modell, Spieler, Stelle


class Aufstellung:
    """Der Schiedsrichter: ändert den Stand erst nach der Prüfung."""

    def __init__(self, ausgangslage: Ausgangslage) -> None:
        self._ausgangslage = ausgangslage
        self._spieler = (ausgangslage.ersterSpieler, ausgangslage.zweiterSpieler)
        self._gewinner: Spieler | None = None
        self._einheitInAufstellung: Einheit | None = None
        self._anDerReihe: Spieler | None = None
        self._zonen: dict[Spieler, Aufstellungszone] = {}
        self._stellen: dict[Modell, Stelle] = {}
        self._aufgestellt: set[Einheit] = set()
        self._auswahl = Auswahl(self._spieler, self._aufgestellt)

    @property
    def ausgangslage(self) -> Ausgangslage:
        return self._ausgangslage

    @property
    def gewinner(self) -> Spieler | None:
        return self._gewinner

    @property
    def einheitInAufstellung(self) -> Einheit | None:
        return self._einheitInAufstellung

    @property
    def anDerReihe(self) -> Spieler | None:
        return self._anDerReihe

    @property
    def beendet(self) -> bool:
        return bool(self._zonen) and self._anDerReihe is None

    def gesetzt(self, modell: Modell) -> bool:
        return modell in self._stellen

    def stelle(self, modell: Modell) -> Stelle | None:
        return self._stellen.get(modell)

    def inKohärenz(self, einheit: Einheit) -> bool:
        return inKohärenz(gesetzteModelle(einheit, self._stellen))

    def aufgestellt(self, einheit: Einheit) -> bool:
        return einheit in self._aufgestellt

    def ausgewählt(self, einheit: Einheit) -> bool:
        return self._auswahl.ausgewählt(einheit)

    def ebene(self, einheit: Einheit) -> Einheit | Modell | None:
        return self._auswahl.ebene(einheit)

    def modellAusgewählt(self, modell: Modell) -> bool:
        return self._auswahl.modellAusgewählt(modell)

    def aufstellungszone(self, spieler: Spieler) -> Aufstellungszone | None:
        if spieler not in self._spieler:
            raise ValueError("Der Spieler ist unbekannt")
        return self._zonen.get(spieler)

    def gewinnerWählen(self, gewinner: Spieler) -> None:
        if gewinner not in self._spieler:
            raise ValueError("Der Gewinner ist kein Spieler")
        if self._gewinner is not None:
            raise Sperre(Grund.nichtWählbar)
        self._gewinner = gewinner

    def aufstellungszoneWählen(self, zone: Aufstellungszone) -> None:
        if self._gewinner is None or self._zonen:
            raise Sperre(Grund.nichtWählbar)
        self._zonen = zonenVerteilen(self._spieler, self._gewinner, zone)
        self._anDerReihe = nächsterAnDerReihe(self._spieler, self._gewinner, self._aufgestellt)

    def modellSetzen(self, modell: Modell, stelle: Stelle) -> None:
        einheit = self._wählbareEinheitVon(modell)
        gründe = self._gründeGegenDieStelle(modell, stelle, self._stellen)
        if gründe:
            raise Sperre(*gründe)
        self._stellen[modell] = stelle
        self._einheitInAufstellung = einheit

    def modellLoslassen(self, modell: Modell, stelle: Stelle) -> None:
        stellen = self.stellenBeimLoslassen(modell, stelle)
        self._loslassen(einheitVon(self._spieler, modell), stellen)

    def stellenBeimLoslassen(self, modell: Modell, stelle: Stelle) -> dict[Modell, Stelle]:
        """Die Stellen, an die `modellLoslassen` die Modelle setzen würde (V10)."""
        einheit = self._wählbareEinheitVon(modell)
        verschoben = self._verschobeneStellen(einheit, modell, stelle)
        hinein = hineingerückt(verschoben, self._zoneAnDerReihe())
        return angehalten(self._stellen, hinein, modell)

    def _verschobeneStellen(
        self, einheit: Einheit, modell: Modell, stelle: Stelle
    ) -> dict[Modell, Stelle]:
        # Regel: AUF-21.1 verschiebt den Block der Einheit, AUF-20.4 nur das gezogene Modell
        if self.ebene(einheit) is not einheit:
            return {modell: stelle}
        return verschobeneStellen(gesetzteModelle(einheit, self._stellen), modell, stelle)

    def karteAnklicken(self, stelle: Stelle) -> None:
        einheit = self._auswahl.einheit
        if einheit is None:
            return
        self._prüfenDassDran(einheit)
        # Regel: AUF-18.2 setzt die Formation, AUF-18.5 mit gesetzten Modellen nichts
        if any(self.gesetzt(modell) for modell in einheit.modelle):
            return
        formationen = self._ausgangslage.formationen
        orte = formationDerEinheit(einheit, stelle, formationen, self._zoneAnDerReihe())
        self._loslassen(einheit, orte)

    def modellAufAblageLoslassen(self, modell: Modell, ablage: Spieler) -> None:
        einheit = einheitVon(self._spieler, modell)
        # Regel: AUF-8.4 und AUF-16.3 sperren, AUF-16.6 auf der eigenen Ablage geschieht nichts
        if einheit in self._aufgestellt or einheit not in ablage.armee.einheiten:
            raise Sperre(Grund.nichtWählbar)

    def zurück(self) -> None:
        # Regel: AUF-17.1, eine Sperre setzt kein Modell, also gibt es nichts zurückzunehmen
        return

    def _loslassen(self, einheit: Einheit, neue: Mapping[Modell, Stelle]) -> None:
        # Regel: AUF-24.2, die Modelle des Loslassens sperren einander nicht
        anderswo = {modell: ort for modell, ort in self._stellen.items() if modell not in neue}
        gründe: set[Grund] = set()
        for modell, ort in neue.items():
            gründe |= self._gründeGegenDieStelle(modell, ort, anderswo)
        if gründe:
            raise Sperre(*gründe)
        self._stellen.update(neue)
        self._einheitInAufstellung = einheit

    def _prüfenDassDran(self, einheit: Einheit) -> None:
        prüfenDassWählbar(einheit, self._aufgestellt, self._anDerReihe, self._einheitInAufstellung)

    def _wählbareEinheitVon(self, modell: Modell) -> Einheit:
        einheit = einheitVon(self._spieler, modell)
        self._prüfenDassDran(einheit)
        return einheit

    def aufstellenDerEinheitBeenden(self) -> None:
        einheit = self._einheitInAufstellung
        if einheit is None:
            raise Sperre(Grund.nichtInAufstellung)
        gründe = gründeGegenDasBeenden(einheit, self._stellen)
        if gründe:
            raise Sperre(*gründe)
        bisher = self._spielerAnDerReihe
        self._aufgestellt.add(einheit)
        self._auswahl.abwählen(einheit)
        self._einheitInAufstellung = None
        self._anDerReihe = nächsterAnDerReihe(self._spieler, bisher, self._aufgestellt)

    @property
    def _spielerAnDerReihe(self) -> Spieler:
        spieler = self._anDerReihe
        assert spieler is not None  # Warum: Mit einer Einheit in Aufstellung ist jemand dran
        return spieler

    def _zoneAnDerReihe(self) -> Grenzen:
        return self._ausgangslage.grenzenDerZone(self._zonen[self._spielerAnDerReihe])

    def _gründeGegenDieStelle(
        self, modell: Modell, stelle: Stelle, stellen: Mapping[Modell, Stelle]
    ) -> set[Grund]:
        eigene = self._spielerAnDerReihe.armee.modelle
        return gründeGegenDieStelle(modell, stelle, stellen, eigene, self._zoneAnDerReihe())

    def auswählen(self, einheit: Einheit) -> None:
        self._auswahl.auswählen(einheit)

    def ebeneWählen(self, modell: Modell) -> None:
        self._auswahl.ebeneWählen(modell)

    def ebeneAbwählen(self, modell: Modell) -> None:
        self._auswahl.ebeneAbwählen(modell)

    def abwählen(self, einheit: Einheit) -> None:
        self._auswahl.abwählen(einheit)
