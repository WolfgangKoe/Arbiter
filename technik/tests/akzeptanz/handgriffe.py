"""Handgriffe der Akzeptanztests: Armeen bauen, Stellen berechnen, aufstellen."""

from dataclasses import replace
from fractions import Fraction
from pathlib import Path

import pytest
import yaml

from arbiter.domaene.missionsvorbereitung.ausgangslage import Aufstellungszone
from arbiter.domaene.phasen.aufstellen import Aufstellung
from arbiter.domaene.sperre import Grund, Sperre
from arbiter.domaene.spielobjekte import Armee, Base, Einheit, Modell, Spieler, Stelle
from arbiter.katalog.ausgangslage import ausgangslageLaden

# Regel: 1 Zoll sind 25,4 mm (domaene/glossar.md, Durchmesser)
millimeterJeZoll = Fraction(254, 10)

# Warum: Schon ein Millionstel Zoll entscheidet, damit Grenzfälle ohne Toleranz gelten.
millionstel = Fraction(1, 1_000_000)


# Warum: Lage der Zonen, Ursprung und Achsen der Stelle stehen in technik/architektur.md, S1
breiteDesSpielfelds = 44
längeDerSpielfeldkante = 60
tiefeDerZone = 9
abstandDerReihen = Fraction(5, 2)
tiefeDerErstenReihe = Fraction(3, 2)
durchmesserDerTestmodelle = 32
anzahlGesetzterModelle = 3

# Regel: Richtung als Anteile von x und y; 3-4-5 hält die Entfernung exakt
gerade = (1, 0)
schräg = (Fraction(3, 5), Fraction(4, 5))


def spielerMit(*modellzahlen: int) -> Spieler:
    """Ein Spieler, dessen Armee je Zahl eine Einheit mit so vielen Modellen hat."""
    einheiten = tuple(
        Einheit(
            name=f"Einheit {nummer}",
            modelle=tuple(
                Modell(base=Base(durchmesser=durchmesserDerTestmodelle)) for _ in range(zahl)
            ),
        )
        for nummer, zahl in enumerate(modellzahlen, start=1)
    )
    return Spieler(armee=Armee(einheiten=einheiten))


def aufstellungVon(ersterSpieler: Spieler, zweiterSpieler: Spieler) -> Aufstellung:
    onlyWar = ausgangslageLaden()
    return Aufstellung(replace(onlyWar, ersterSpieler=ersterSpieler, zweiterSpieler=zweiterSpieler))


def radiusInZoll(modell: Modell) -> Fraction:
    return Fraction(modell.base.durchmesser) / 2 / millimeterJeZoll


def stelleInZone(zone: Aufstellungszone, tiefe: Fraction | int, länge: Fraction | int) -> Stelle:
    """Tiefe von der Spielfeldkante der Zone nach innen, Länge entlang dieser Kante."""
    ersteHälfte = zone is Aufstellungszone.erste
    breite = Fraction(tiefe) if ersteHälfte else breiteDesSpielfelds - Fraction(tiefe)
    return Stelle(x=breite, y=Fraction(länge))


def stellenDerEinheit(
    aufstellung: Aufstellung, spieler: Spieler, einheit: Einheit
) -> list[tuple[Modell, Stelle]]:
    """Die Modelle in einer Reihe, Base an Base, je Einheit eine eigene Reihe in der Zone."""
    zone = aufstellung.aufstellungszone(spieler)
    reihe = spieler.armee.einheiten.index(einheit)
    tiefe = tiefeDerErstenReihe + abstandDerReihen * reihe
    länge = Fraction(0)
    stellen = []
    for modell in einheit.modelle:
        länge += radiusInZoll(modell)
        stellen.append((modell, stelleInZone(zone, tiefe, länge)))
        länge += radiusInZoll(modell)
    return stellen


def stelleDesErstenModells(aufstellung: Aufstellung, spieler: Spieler, einheit: Einheit) -> Stelle:
    (_, stelle), *_ = stellenDerEinheit(aufstellung, spieler, einheit)
    return stelle


def einheitAufstellen(aufstellung: Aufstellung, einheit: Einheit) -> None:
    spieler = aufstellung.anDerReihe
    for modell, stelle in stellenDerEinheit(aufstellung, spieler, einheit):
        aufstellung.modellSetzen(modell, stelle)
    aufstellung.aufstellenDerEinheitBeenden()


def nachDerWahlDerAufstellungszone(aufstellung: Aufstellung, gewinner: Spieler) -> None:
    aufstellung.gewinnerWählen(gewinner)
    aufstellung.aufstellungszoneWählen(Aufstellungszone.erste)


def sperrgründe(handlung, *argumente) -> frozenset[Grund]:
    with pytest.raises(Sperre) as sperre:
        handlung(*argumente)
    return sperre.value.gründe


def durchmesserJeEinheit(spieler: Spieler) -> tuple[tuple[int, ...], ...]:
    return tuple(
        tuple(modell.base.durchmesser for modell in einheit.modelle)
        for einheit in spieler.armee.einheiten
    )


class Platz:
    """Stellen in der Zone des ersten Spielers und die Maße der Testmodelle."""

    def __init__(self, zone: Aufstellungszone) -> None:
        self._zone = zone
        self.radius = radiusInZoll(Modell(base=Base(durchmesser=durchmesserDerTestmodelle)))
        self.millionstel = millionstel
        self.breiteDesSpielfelds = breiteDesSpielfelds
        self.längeDerSpielfeldkante = längeDerSpielfeldkante
        self.tiefeDerZone = tiefeDerZone
        self.tiefeDerErstenReihe = tiefeDerErstenReihe

    def stelle(self, tiefe, länge) -> Stelle:
        return stelleInZone(self._zone, tiefe, länge)

    def stelleBeimAnderenSpieler(self, abstandDerMittelpunkte, richtung) -> Stelle:
        """Eine Stelle, deren Mittelpunkt so weit vom letzten Modell der ersten Einheit liegt."""
        anteilX, anteilY = richtung
        tiefe = (
            self.breiteDesSpielfelds - self.tiefeDerErstenReihe - abstandDerMittelpunkte * anteilX
        )
        return self.stelle(tiefe, 3 * self.radius + abstandDerMittelpunkte * anteilY)


def modelleSetzen(
    aufstellung: Aufstellung, einheit: Einheit, anzahl: int
) -> list[tuple[Modell, Stelle]]:
    """Setzt die ersten Modelle der Reihe der Einheit, ohne das Aufstellen zu beenden."""
    spieler = aufstellung.anDerReihe
    gesetzt = stellenDerEinheit(aufstellung, spieler, einheit)[:anzahl]
    for modell, stelle in gesetzt:
        aufstellung.modellSetzen(modell, stelle)
    return gesetzt


def einheitenAufstellen(aufstellung: Aufstellung, anzahl: int) -> None:
    """Der jeweils an der Reihe ist, stellt seine nächste Einheit auf, so oft wie verlangt."""
    for _ in range(anzahl):
        spieler = aufstellung.anDerReihe
        nächste = next(
            einheit for einheit in spieler.armee.einheiten if not aufstellung.aufgestellt(einheit)
        )
        einheitAufstellen(aufstellung, nächste)


def alleEinheitenAufstellen(aufstellung: Aufstellung) -> None:
    """Beide Spieler stellen alle Einheiten ihrer Armee auf."""
    ausgangslage = aufstellung.ausgangslage
    einheitenAufstellen(
        aufstellung,
        len(ausgangslage.ersterSpieler.armee.einheiten)
        + len(ausgangslage.zweiterSpieler.armee.einheiten),
    )


def modelleAnStellenSetzen(
    aufstellung: Aufstellung, einheit: Einheit, stellen: list[Stelle]
) -> None:
    """Setzt die ersten Modelle der Einheit an die Stellen, ein Modell je Stelle."""
    for modell, stelle in zip(einheit.modelle, stellen, strict=False):
        aufstellung.modellSetzen(modell, stelle)


def inZoll(maß: tuple[int, int], radius: Fraction) -> Fraction:
    """Ganze Zoll plus ein Vielfaches des Radius."""
    zoll, radien = maß
    return zoll + radien * radius


welchesGezogenWird = pytest.mark.parametrize(
    "zweitesGezogen", [False, True], ids=["erstesGezogen", "zweitesGezogen"]
)


def wegVon(davor: Stelle, ziel: Stelle) -> tuple[Fraction, Fraction]:
    return ziel.x - davor.x, ziel.y - davor.y


def versetzt(stelle: Stelle, weg: tuple[Fraction, Fraction]) -> Stelle:
    wegInX, wegInY = weg
    return Stelle(x=stelle.x + wegInX, y=stelle.y + wegInY)


def gezogenesUndRest(
    gesetzte: list[tuple[Modell, Stelle]], *, zweitesGezogen: bool
) -> tuple[tuple[Modell, Stelle], tuple[Modell, Stelle]]:
    """Von zwei gesetzten Modellen das gezogene zuerst, das mitgezogene danach."""
    erstes, zweites = gesetzte
    return (zweites, erstes) if zweitesGezogen else (erstes, zweites)


def stelleInDerZoneVon(
    aufstellung: Aufstellung, spieler: Spieler, tiefe: Fraction | int, länge: Fraction | int
) -> Stelle:
    return stelleInZone(aufstellung.aufstellungszone(spieler), tiefe, länge)


def stelleInDerZoneDesSpielersAnDerReihe(
    aufstellung: Aufstellung, tiefe: Fraction | int, länge: Fraction | int
) -> Stelle:
    return stelleInDerZoneVon(aufstellung, aufstellung.anDerReihe, tiefe, länge)


def stellenAllerModelle(aufstellung: Aufstellung) -> dict[Modell, Stelle | None]:
    ausgangslage = aufstellung.ausgangslage
    spieler = (ausgangslage.ersterSpieler, ausgangslage.zweiterSpieler)
    return {
        modell: aufstellung.stelle(modell) for einer in spieler for modell in einer.armee.modelle
    }


def einGesperrtesModell(
    aufstellung: Aufstellung, spieler: Spieler
) -> tuple[Modell, Modell, Stelle]:
    """Das zweite Modell der ersten Einheit, auf das erste gezogen (AUF-8.2), ist gesperrt."""
    ersteEinheit, _ = spieler.armee.einheiten
    gesetztesModell, gesperrtesModell = ersteEinheit.modelle
    stelle = stelleInDerZoneVon(aufstellung, spieler, tiefeDerErstenReihe, 3)
    nebenan = stelleInDerZoneVon(aufstellung, spieler, tiefeDerErstenReihe, 6)
    aufstellung.modellSetzen(gesetztesModell, stelle)
    aufstellung.modellSetzen(gesperrtesModell, nebenan)
    aufstellung.modellLoslassen(gesperrtesModell, stelle)
    return gesetztesModell, gesperrtesModell, stelle


def reihenDerFormation(einheitenname: str) -> list[int]:
    """Die Modelle je Reihe aus `formation.yaml`, nicht kopiert."""
    pfad = Path(__file__).parents[3] / "domaene" / "daten" / "formation.yaml"
    with pfad.open(encoding="utf-8") as datei:
        return yaml.safe_load(datei)["formation"][einheitenname]
