from dataclasses import dataclass
from enum import Enum
from fractions import Fraction

from arbiter.domaene import messen
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
    # Warum: Tiefe der ersten und der zweiten Aufstellungszone, in der Reihenfolge der Zonen
    tiefen: tuple[Fraction, Fraction]


class Aufstellung:
    def __init__(self, ausgangslage: Ausgangslage) -> None:
        ersterSpieler, zweiterSpieler = ausgangslage.ersterSpieler, ausgangslage.zweiterSpieler
        if ersterSpieler is zweiterSpieler:
            raise ValueError("Die Aufstellung braucht zwei verschiedene Spieler")
        self._ausgangslage = ausgangslage
        self._spieler = (ersterSpieler, zweiterSpieler)
        self._gewinner: Spieler | None = None
        self._einheitInAufstellung: Einheit | None = None
        self._anDerReihe: Spieler | None = None
        self._zoneDesGewinners: Aufstellungszone | None = None
        self._stellen: dict[Modell, Stelle] = {}
        self._aufgestellt: set[Einheit] = set()

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
        return self._zoneDesGewinners is not None and self._anDerReihe is None

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
        if self._gewinner is None or self._zoneDesGewinners is not None:
            raise Sperre(Grund.nichtWählbar)
        self._zoneDesGewinners = zone
        self._anDerReihe = self._nächsterAnDerReihe(self._gewinner)

    def aufstellungszone(self, spieler: Spieler) -> Aufstellungszone | None:
        if spieler not in self._spieler:
            raise ValueError("Der Spieler gehört nicht zur Aufstellung")
        if self._zoneDesGewinners is None:
            return None
        if spieler is self._gewinner:
            return self._zoneDesGewinners
        return next(zone for zone in Aufstellungszone if zone is not self._zoneDesGewinners)

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
        spieler = self._anDerReihe
        if einheit is None:
            raise Sperre(Grund.nichtInAufstellung)
        assert spieler is not None  # Warum: Einheit in Aufstellung heißt, jemand ist an der Reihe.
        self._aufgestellt.add(einheit)
        self._einheitInAufstellung = None
        self._anDerReihe = self._nächsterAnDerReihe(spieler)

    def _gründeGegenDieStelle(self, modell: Modell, stelle: Stelle) -> set[Grund]:
        spieler = self._anDerReihe
        assert spieler is not None  # Warum: Einheit in Aufstellung heißt, jemand ist an der Reihe.
        gründe = set()
        _, länge = self._ausgangslage.spielfeld.seitenlängen
        zone = self.aufstellungszone(spieler)
        assert zone is not None  # Warum: Wer an der Reihe ist, hat die Zone nach der Zonenwahl.
        if not messen.ganzIn(modell.base, stelle, self._grenzenInX(zone), länge):
            gründe.add(Grund.nichtGanzInDerZone)
        for anderes, andereStelle in self._stellen.items():
            if anderes is modell:
                continue
            if messen.überdecken(modell.base, stelle, anderes.base, andereStelle):
                gründe.add(Grund.baseÜberdeckt)
            if anderes not in self._modelleVon(spieler) and messen.abstandHöchstens(
                modell.base, stelle, anderes.base, andereStelle, _nahkampfreichweite
            ):
                gründe.add(Grund.nahkampfreichweite)
        return gründe

    def _modelleVon(self, spieler: Spieler) -> set[Modell]:
        return {modell for einheit in spieler.armee.einheiten for modell in einheit.modelle}

    def _grenzenInX(self, zone: Aufstellungszone) -> tuple[Fraction, Fraction]:
        breite, _ = self._ausgangslage.spielfeld.seitenlängen
        tiefe = self._ausgangslage.tiefen[list(Aufstellungszone).index(zone)]
        if zone is Aufstellungszone.erste:
            return Fraction(0), tiefe
        return breite - tiefe, breite

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
