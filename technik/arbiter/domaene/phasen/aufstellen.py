"""Die Phase Aufstellen: Wahlen, Setzen der Modelle und Auswählen der Einheiten (AUF)."""

from collections.abc import Callable, Collection, Mapping
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

    def __post_init__(self) -> None:
        if self.ersterSpieler is self.zweiterSpieler:
            raise ValueError("Die Aufstellung braucht zwei verschiedene Spieler")
        if _teilenSichArmeeOderModell(self.ersterSpieler, self.zweiterSpieler):
            raise ValueError("Die Spieler brauchen verschiedene Armeen ohne gemeinsames Modell")

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


# Regel: Nahkampfreichweite, ein Gegner höchstens 1″ entfernt (core_rules.txt:450)
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
    """Der Schiedsrichter der Phase: Abfragen, dann AUF-1, AUF-7 und AUF-3, AUF-5."""

    def __init__(self, ausgangslage: Ausgangslage) -> None:
        self._ausgangslage = ausgangslage
        self._spieler = (ausgangslage.ersterSpieler, ausgangslage.zweiterSpieler)
        self._gewinner: Spieler | None = None
        self._einheitInAufstellung: Einheit | None = None
        self._anDerReihe: Spieler | None = None
        self._zonen: dict[Spieler, Aufstellungszone] = {}
        self._stellen: dict[Modell, Stelle] = {}
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
        einheit = self._einheitVon(modell)
        # Regel: AUF-7.2 und AUF-7.3 sperren vor jeder Prüfung der Stelle (AUF-3.8)
        if self.aufgestellt(einheit) or not self._gehörtDemSpielerAnDerReihe(einheit):
            raise Sperre(Grund.nichtWählbar)
        if self._einheitInAufstellung not in (None, einheit):
            raise Sperre(Grund.einheitBegonnen)
        gründe = self._gründeGegenDieStelle(modell, stelle)
        if gründe:
            raise Sperre(*gründe)
        self._stellen[modell] = stelle
        self._einheitInAufstellung = einheit

    def aufstellenDerEinheitBeenden(self) -> None:
        einheit = self._einheitInAufstellung
        if einheit is None:
            raise Sperre(Grund.nichtInAufstellung)
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

    def _inNahkampfreichweiteVonGegnern(self, modell: Modell, stelle: Stelle) -> bool:
        eigene = self._spielerAnDerReihe.armee.modelle
        return inNahkampfreichweite(modell, stelle, self._stellen, eigene)

    _prüfungen: ClassVar[dict[Grund, Callable[["Aufstellung", Modell, Stelle], bool]]] = {
        Grund.nichtGanzInDerZone: _nichtGanzInDerZone,
        Grund.baseÜberdeckt: _baseÜberdeckt,
        Grund.nahkampfreichweite: _inNahkampfreichweiteVonGegnern,
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
