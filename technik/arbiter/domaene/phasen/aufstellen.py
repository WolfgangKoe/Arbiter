"""Die Phase Aufstellen: Wahlen, Setzen der Modelle und Auswählen der Einheiten (AUF)."""

from collections.abc import Callable, Collection, Mapping
from fractions import Fraction
from typing import ClassVar

from arbiter.domaene import messen
from arbiter.domaene.missionsvorbereitung.ausgangslage import Aufstellungszone, Ausgangslage
from arbiter.domaene.querschnitt import baseÜberdeckt, inKohärenz
from arbiter.domaene.sperre import Grund, Sperre
from arbiter.domaene.spielobjekte import Einheit, Modell, Spieler, Stelle

# Regel: Nahkampfreichweite ist ein Abstand von höchstens 1″ (domaene/glossar.md)
_nahkampfreichweite = Fraction(1)


# Regel: Nahkampfreichweite (core_rules.txt:447)
def inNahkampfreichweite(
    modell: Modell, stelle: Stelle, stellen: Mapping[Modell, Stelle], eigene: Collection[Modell]
) -> bool:
    return any(
        anderes not in eigene
        and messen.abstandHöchstens(
            modell.base, stelle, anderes.base, andereStelle, _nahkampfreichweite
        )
        for anderes, andereStelle in stellen.items()
    )


class Aufstellung:
    """Der Schiedsrichter der Aufstellung: ändert den Stand nur nach Prüfung der Sperren."""

    def __init__(self, ausgangslage: Ausgangslage) -> None:
        self._ausgangslage = ausgangslage
        self._spieler = (ausgangslage.ersterSpieler, ausgangslage.zweiterSpieler)
        self._gewinner: Spieler | None = None
        self._einheitInAufstellung: Einheit | None = None
        self._anDerReihe: Spieler | None = None
        self._zonen: dict[Spieler, Aufstellungszone] = {}
        self._stellen: dict[Modell, Stelle] = {}
        # Warum: je gesperrtem Modell die Stelle, die Gründe, die vorige Stelle und sein Loslassen
        self._gesperrte: dict[
            Modell, tuple[Stelle, frozenset[Grund], Stelle | None, frozenset]
        ] = {}
        self._aufgestellt: set[Einheit] = set()
        self._ausgewählt: set[Einheit] = set()

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
        if modell not in self._gesperrte:
            return None
        stelle, _, _, _ = self._gesperrte[modell]
        return stelle

    def gründeDesGesperrten(self, modell: Modell) -> frozenset[Grund]:
        if modell not in self._gesperrte:
            return frozenset()
        _, gründe, _, _ = self._gesperrte[modell]
        return gründe

    def inKohärenz(self, einheit: Einheit) -> bool:
        gesetzte = {
            modell: self._stellen[modell] for modell in einheit.modelle if modell in self._stellen
        }
        return inKohärenz(gesetzte)

    def aufgestellt(self, einheit: Einheit) -> bool:
        return einheit in self._aufgestellt

    def ausgewählt(self, einheit: Einheit) -> bool:
        return einheit in self._ausgewählt

    def aufstellungszone(self, spieler: Spieler) -> Aufstellungszone | None:
        if spieler not in self._spieler:
            raise ValueError("Der Spieler gehört nicht zur Aufstellung")
        return self._zonen.get(spieler)

    def gewinnerWählen(self, gewinner: Spieler) -> None:
        if gewinner not in self._spieler:
            raise ValueError("Der Gewinner gehört nicht zur Aufstellung")
        if self._gewinner is not None:
            raise Sperre(Grund.nichtWählbar)
        self._gewinner = gewinner

    def aufstellungszoneWählen(self, zone: Aufstellungszone) -> None:
        if self._gewinner is None or self._zonen:
            raise Sperre(Grund.nichtWählbar)
        andere = next(übrige for übrige in Aufstellungszone if übrige is not zone)
        self._zonen = {self._gewinner: zone, self._gegnerVon(self._gewinner): andere}
        self._anDerReihe = self._nächsterAnDerReihe(self._gewinner)

    def _gegnerVon(self, spieler: Spieler) -> Spieler:
        return next(andere for andere in self._spieler if andere is not spieler)

    def _nächsterAnDerReihe(self, bisher: Spieler) -> Spieler | None:
        gegner = self._gegnerVon(bisher)
        for kandidat in (gegner, bisher):
            if self._hatEinheitenZumAufstellen(kandidat):
                return kandidat
        return None

    def _hatEinheitenZumAufstellen(self, spieler: Spieler) -> bool:
        return any(not self.aufgestellt(einheit) for einheit in spieler.armee.einheiten)

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

    def einheitLoslassen(self, einheit: Einheit, stelle: Stelle) -> None:
        ungesetzte = [modell for modell in einheit.modelle if not self.gesetzt(modell)]
        # Regel: AUF-16.1, sind alle Modelle gesetzt, geschieht nichts
        if not ungesetzte:
            return
        erstes, *_ = ungesetzte
        self._wählbareEinheitVon(erstes)
        if len(ungesetzte) < len(einheit.modelle):
            # Regel: AUF-14.1, der Rest einer Einheit kommt einzeln
            stellen = [stelle]
            modelle = [erstes]
        else:
            modelle = ungesetzte
            stellen = self._stellenDerFormation(einheit, stelle)
        gruppe = frozenset(modelle)
        for modell, ort in zip(modelle, stellen, strict=True):
            self._loslassen(modell, einheit, ort, gruppe)

    def modellZurücklegen(self, modell: Modell, spieler: Spieler) -> None:
        self._prüfenDassNichtsGesperrtIst()
        einheit = self._einheitVon(modell)
        # Regel: AUF-8.4 und AUF-16.3, nur in die eigene Ablage, nie aus einer aufgestellten Einheit
        if self.aufgestellt(einheit) or einheit not in spieler.armee.einheiten:
            raise Sperre(Grund.nichtWählbar)
        self._stellen.pop(modell, None)
        self._einheitInAufstellungPrüfen()

    def zurück(self) -> None:
        gesperrte, self._gesperrte = self._gesperrte, {}
        for modell, (_, _, vorige, gruppe) in gesperrte.items():
            if vorige is not None:
                self._stellen[modell] = vorige
                continue
            for aus in gruppe:
                self._stellen.pop(aus, None)
        self._einheitInAufstellungPrüfen()

    def _einheitInAufstellungPrüfen(self) -> None:
        einheit = self._einheitInAufstellung
        if einheit is not None and not any(self.gesetzt(modell) for modell in einheit.modelle):
            self._einheitInAufstellung = None

    def _stellenDerFormation(self, einheit: Einheit, mitte: Stelle) -> list[Stelle]:
        formation = self._ausgangslage.formationen[einheit.name]
        zone = self._zonen[self._spielerAnDerReihe]
        grenzenInX, grenzenInY = self._ausgangslage.grenzenDerZone(zone)
        erstes, *_ = einheit.modelle
        return formation.stellen(erstes.base, mitte, grenzenInX, grenzenInY)

    def _loslassen(
        self, modell: Modell, einheit: Einheit, stelle: Stelle, gruppe: frozenset[Modell]
    ) -> None:
        gründe = self._gründeGegenDieStelle(modell, stelle)
        if not gründe:
            self._stellen[modell] = stelle
            self._einheitInAufstellung = einheit
            return
        vorige = self._stellen.pop(modell, None)
        self._gesperrte[modell] = (stelle, frozenset(gründe), vorige, gruppe)

    def _prüfenDassNichtsGesperrtIst(self) -> None:
        if self._gesperrte:
            raise Sperre(Grund.modellGesperrt)

    def _wählbareEinheitVon(self, modell: Modell) -> Einheit:
        """Die Einheit des Modells, wenn es jetzt dran ist; sonst die Sperre ohne Stelle."""
        self._prüfenDassNichtsGesperrtIst()
        einheit = self._einheitVon(modell)
        # Regel: AUF-7.2 und AUF-7.3 sperren vor jeder Prüfung der Stelle (AUF-3.8)
        if self.aufgestellt(einheit) or not self._gehörtDemSpielerAnDerReihe(einheit):
            raise Sperre(Grund.nichtWählbar)
        if self._einheitInAufstellung not in (None, einheit):
            raise Sperre(Grund.einheitBegonnen)
        return einheit

    def aufstellenDerEinheitBeenden(self) -> None:
        self._prüfenDassNichtsGesperrtIst()
        einheit = self._einheitInAufstellung
        if einheit is None:
            raise Sperre(Grund.nichtInAufstellung)
        gründe = {
            grund for grund, fehlt in self._gründeGegenDasBeenden.items() if fehlt(self, einheit)
        }
        if gründe:
            raise Sperre(*gründe)
        spieler = self._spielerAnDerReihe
        self._aufgestellt.add(einheit)
        self._ausgewählt.discard(einheit)
        self._einheitInAufstellung = None
        self._anDerReihe = self._nächsterAnDerReihe(spieler)

    def _einheitVon(self, modell: Modell) -> Einheit:
        for spieler in self._spieler:
            einheit = spieler.armee.einheitVon(modell)
            if einheit is not None:
                return einheit
        raise ValueError("Das Modell gehört nicht zur Aufstellung")

    def _gehörtDemSpielerAnDerReihe(self, einheit: Einheit) -> bool:
        return self._anDerReihe is not None and einheit in self._anDerReihe.armee.einheiten

    @property
    def _spielerAnDerReihe(self) -> Spieler:
        spieler = self._anDerReihe
        assert spieler is not None  # Warum: Einheit in Aufstellung heißt, jemand ist an der Reihe.
        return spieler

    def _gründeGegenDieStelle(self, modell: Modell, stelle: Stelle) -> set[Grund]:
        return {
            grund for grund, prüfung in self._prüfungen.items() if prüfung(self, modell, stelle)
        }

    def _nichtGanzInDerZone(self, modell: Modell, stelle: Stelle) -> bool:
        spieler = self._spielerAnDerReihe
        grenzen = self._ausgangslage.grenzenDerZone(self._zonen[spieler])
        return not messen.ganzIn(modell.base, stelle, *grenzen)

    def _baseÜberdeckt(self, modell: Modell, stelle: Stelle) -> bool:
        return baseÜberdeckt(modell, stelle, self._stellen)

    # Regel: Aufstellen nicht in Nahkampfreichweite (core_rules.txt:450)
    def _inNahkampfreichweiteVonGegnern(self, modell: Modell, stelle: Stelle) -> bool:
        eigene = self._spielerAnDerReihe.armee.modelle
        return inNahkampfreichweite(modell, stelle, self._stellen, eigene)

    _prüfungen: ClassVar[dict[Grund, Callable[["Aufstellung", Modell, Stelle], bool]]] = {
        Grund.nichtGanzInDerZone: _nichtGanzInDerZone,
        Grund.baseÜberdeckt: _baseÜberdeckt,
        Grund.nahkampfreichweite: _inNahkampfreichweiteVonGegnern,
    }

    def _modelleFehlen(self, einheit: Einheit) -> bool:
        return not all(self.gesetzt(modell) for modell in einheit.modelle)

    def _ohneKohärenz(self, einheit: Einheit) -> bool:
        return not self.inKohärenz(einheit)

    _gründeGegenDasBeenden: ClassVar[dict[Grund, Callable[["Aufstellung", Einheit], bool]]] = {
        Grund.modelleFehlen: _modelleFehlen,
        Grund.keineKohärenz: _ohneKohärenz,
    }

    def auswählen(self, einheit: Einheit) -> None:
        self._prüfenDassZurAufstellung(einheit)
        if einheit in self._aufgestellt:
            raise ValueError("Eine aufgestellte Einheit ist nicht auswählbar")
        self._ausgewählt.add(einheit)

    def abwählen(self, einheit: Einheit) -> None:
        self._prüfenDassZurAufstellung(einheit)
        self._ausgewählt.discard(einheit)

    def _prüfenDassZurAufstellung(self, einheit: Einheit) -> None:
        if not any(einheit in spieler.armee.einheiten for spieler in self._spieler):
            raise ValueError("Die Einheit gehört nicht zur Aufstellung")
