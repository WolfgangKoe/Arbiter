from collections.abc import Callable, Mapping
from dataclasses import dataclass
from enum import Enum
from fractions import Fraction
from typing import ClassVar

from arbiter.domaene import messen
from arbiter.domaene.querschnitt import baseÜberdeckt
from arbiter.domaene.sperre import Grund, Sperre
from arbiter.domaene.spielobjekte import Einheit, Modell, Spieler, Spielfeld, Stelle

# Regel: Nahkampfreichweite ist ein Abstand von höchstens 1″ (domaene/glossar.md)
_nahkampfreichweite = Fraction(1)


class Aufstellungszone(Enum):
    erste = 1
    zweite = 2


@dataclass(frozen=True, eq=False)
class Ausgangslage:
    ersterSpieler: Spieler
    zweiterSpieler: Spieler
    spielfeld: Spielfeld
    tiefen: Mapping[Aufstellungszone, Fraction]

    def grenzenDerZone(
        self, zone: Aufstellungszone
    ) -> tuple[tuple[Fraction, Fraction], tuple[Fraction, Fraction]]:
        """Die Fläche der Zone als Grenzen in x und in y, die Form von `messen.ganzIn`."""
        breite, länge = self.spielfeld.seitenlängen
        return _grenzenInXDerZone(zone, breite, self.tiefen[zone]), (Fraction(0), länge)


def _grenzenInXDerZone(
    zone: Aufstellungszone, breite: Fraction, tiefe: Fraction
) -> tuple[Fraction, Fraction]:
    if zone is Aufstellungszone.erste:
        return Fraction(0), tiefe
    return breite - tiefe, breite


def _teilenSichArmeeOderModell(ersterSpieler: Spieler, zweiterSpieler: Spieler) -> bool:
    return (
        ersterSpieler.armee is zweiterSpieler.armee
        or not ersterSpieler.armee.modelle.isdisjoint(zweiterSpieler.armee.modelle)
    )


class Aufstellung:
    def __init__(self, ausgangslage: Ausgangslage) -> None:
        ersterSpieler, zweiterSpieler = ausgangslage.ersterSpieler, ausgangslage.zweiterSpieler
        if ersterSpieler is zweiterSpieler:
            raise ValueError("Die Aufstellung braucht zwei verschiedene Spieler")
        if _teilenSichArmeeOderModell(ersterSpieler, zweiterSpieler):
            raise ValueError("Die Spieler brauchen verschiedene Armeen ohne gemeinsames Modell")
        self._ausgangslage = ausgangslage
        self._spieler = (ersterSpieler, zweiterSpieler)
        self._gewinner: Spieler | None = None
        self._einheitInAufstellung: Einheit | None = None
        self._anDerReihe: Spieler | None = None
        self._zonen: dict[Spieler, Aufstellungszone] = {}
        self._stellen: dict[Modell, Stelle] = {}
        self._aufgestellt: set[Einheit] = set()

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

    def aufgestellt(self, einheit: Einheit) -> bool:
        return einheit in self._aufgestellt

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

    def aufstellungszone(self, spieler: Spieler) -> Aufstellungszone | None:
        if spieler not in self._spieler:
            raise ValueError("Der Spieler gehört nicht zur Aufstellung")
        return self._zonen.get(spieler)

    def einheitInAufstellungWählen(self, einheit: Einheit) -> None:
        if self._anDerReihe is None or self.aufgestellt(einheit):
            raise Sperre(Grund.nichtWählbar)
        if einheit not in self._anDerReihe.armee.einheiten:
            raise Sperre(Grund.nichtWählbar)
        bisherige = self._einheitInAufstellung
        if bisherige is not None and bisherige is not einheit and self._begonnen(bisherige):
            raise Sperre(Grund.einheitBegonnen)
        self._einheitInAufstellung = einheit

    def modellSetzen(self, modell: Modell, stelle: Stelle) -> None:
        einheit = self._einheitInAufstellung
        if einheit is None or modell not in einheit.modelle:
            raise Sperre(Grund.nichtInAufstellung)
        gründe = self._gründeGegenDieStelle(modell, stelle)
        if gründe:
            raise Sperre(*gründe)
        self._stellen[modell] = stelle

    def aufstellenDerEinheitBeenden(self) -> None:
        einheit = self._einheitInAufstellung
        if einheit is None:
            raise Sperre(Grund.nichtInAufstellung)
        spieler = self._spielerAnDerReihe
        self._aufgestellt.add(einheit)
        self._einheitInAufstellung = None
        self._anDerReihe = self._nächsterAnDerReihe(spieler)

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

    def _inNahkampfreichweiteVonGegnern(self, modell: Modell, stelle: Stelle) -> bool:
        spieler = self._spielerAnDerReihe
        eigene = spieler.armee.modelle
        return any(
            anderes not in eigene
            and messen.abstandHöchstens(
                modell.base, stelle, anderes.base, andereStelle, _nahkampfreichweite
            )
            for anderes, andereStelle in self._stellen.items()
        )

    _prüfungen: ClassVar[dict[Grund, Callable[["Aufstellung", Modell, Stelle], bool]]] = {
        Grund.nichtGanzInDerZone: _nichtGanzInDerZone,
        Grund.baseÜberdeckt: _baseÜberdeckt,
        Grund.nahkampfreichweite: _inNahkampfreichweiteVonGegnern,
    }

    def _begonnen(self, einheit: Einheit) -> bool:
        return any(self.gesetzt(modell) for modell in einheit.modelle)

    def _hatEinheitenZumAufstellen(self, spieler: Spieler) -> bool:
        return any(not self.aufgestellt(einheit) for einheit in spieler.armee.einheiten)

    def _gegnerVon(self, spieler: Spieler) -> Spieler:
        return next(andere for andere in self._spieler if andere is not spieler)

    def _nächsterAnDerReihe(self, bisher: Spieler) -> Spieler | None:
        gegner = self._gegnerVon(bisher)
        for kandidat in (gegner, bisher):
            if self._hatEinheitenZumAufstellen(kandidat):
                return kandidat
        return None
