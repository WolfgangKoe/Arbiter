"""Die Phase Aufstellen: Wahlen, Setzen und Auswählen (AUF)."""

from arbiter.domaene.missionsvorbereitung.ausgangslage import (
    Aufstellungszone,
    Ausgangslage,
    Grenzen,
)
from arbiter.domaene.phasen.aufstellen.auswahl import Auswahl
from arbiter.domaene.phasen.aufstellen.beenden import gesetzteModelle, gründeGegenDasBeenden
from arbiter.domaene.phasen.aufstellen.einheitInAufstellung import (
    einheitInAufstellungNach,
    prüfenDassWählbar,
)
from arbiter.domaene.phasen.aufstellen.gesperrtesModell import Gesperrtes, zurücknehmen
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
        self._gesperrte: dict[Modell, Gesperrtes] = {}
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

    def gesperrt(self, modell: Modell) -> bool:
        return modell in self._gesperrte

    def stelleDesGesperrten(self, modell: Modell) -> Stelle | None:
        gesperrtes = self._gesperrte.get(modell)
        return gesperrtes.stelle if gesperrtes else None

    def gründeDesGesperrten(self, modell: Modell) -> frozenset[Grund]:
        gesperrtes = self._gesperrte.get(modell)
        return gesperrtes.gründe if gesperrtes else frozenset()

    def inKohärenz(self, einheit: Einheit) -> bool:
        return inKohärenz(gesetzteModelle(einheit, self._stellen))

    def aufgestellt(self, einheit: Einheit) -> bool:
        return einheit in self._aufgestellt

    def ausgewählt(self, einheit: Einheit) -> bool:
        return self._auswahl.ausgewählt(einheit)

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
        gründe = self._gründeGegenDieStelle(modell, stelle)
        if gründe:
            raise Sperre(*gründe)
        self._stellen[modell] = stelle
        self._einheitInAufstellung = einheit

    def modellLoslassen(self, modell: Modell, stelle: Stelle) -> None:
        einheit = self._wählbareEinheitVon(modell)
        self._loslassen(modell, einheit, stelle, frozenset({modell}))

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
        for modell, ort in orte.items():
            self._loslassen(modell, einheit, ort, frozenset(orte))

    def modellAufAblageLoslassen(self, modell: Modell, ablage: Spieler) -> None:
        self._prüfenDassNichtsGesperrtIst()
        einheit = einheitVon(self._spieler, modell)
        # Regel: AUF-8.4 und AUF-16.3 sperren, AUF-16.6 auf der eigenen Ablage geschieht nichts
        if einheit in self._aufgestellt or einheit not in ablage.armee.einheiten:
            raise Sperre(Grund.nichtWählbar)

    def zurück(self) -> None:
        zurücknehmen(self._gesperrte, self._stellen)
        self._gesperrte = {}
        self._einheitInAufstellungPrüfen()

    def _einheitInAufstellungPrüfen(self) -> None:
        self._einheitInAufstellung = einheitInAufstellungNach(
            self._einheitInAufstellung, self._stellen
        )

    def _loslassen(
        self, modell: Modell, einheit: Einheit, stelle: Stelle, gruppe: frozenset[Modell]
    ) -> None:
        gründe = self._gründeGegenDieStelle(modell, stelle)
        if not gründe:
            self._stellen[modell] = stelle
            self._einheitInAufstellung = einheit
            return
        vorige = self._stellen.pop(modell, None)
        self._gesperrte[modell] = Gesperrtes(stelle, frozenset(gründe), vorige, gruppe)

    def _prüfenDassNichtsGesperrtIst(self) -> None:
        if self._gesperrte:
            raise Sperre(Grund.modellGesperrt)

    def _prüfenDassDran(self, einheit: Einheit) -> None:
        self._prüfenDassNichtsGesperrtIst()
        prüfenDassWählbar(einheit, self._aufgestellt, self._anDerReihe, self._einheitInAufstellung)

    def _wählbareEinheitVon(self, modell: Modell) -> Einheit:
        einheit = einheitVon(self._spieler, modell)
        self._prüfenDassDran(einheit)
        return einheit

    def aufstellenDerEinheitBeenden(self) -> None:
        self._prüfenDassNichtsGesperrtIst()
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

    def _gründeGegenDieStelle(self, modell: Modell, stelle: Stelle) -> set[Grund]:
        eigene = self._spielerAnDerReihe.armee.modelle
        return gründeGegenDieStelle(modell, stelle, self._stellen, eigene, self._zoneAnDerReihe())

    def auswählen(self, einheit: Einheit) -> None:
        self._auswahl.auswählen(einheit)

    def abwählen(self, einheit: Einheit) -> None:
        self._auswahl.abwählen(einheit)
