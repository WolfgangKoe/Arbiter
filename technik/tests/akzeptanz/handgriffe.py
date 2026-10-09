"""Handgriffe der Akzeptanztests: Armeen bauen, Stellen berechnen, aufstellen."""

from dataclasses import replace
from fractions import Fraction

import pytest

from arbiter.domaene.phasen.aufstellen import Aufstellung, Aufstellungszone
from arbiter.domaene.sperre import Grund, Sperre
from arbiter.domaene.spielobjekte import Armee, Base, Einheit, Modell, Spieler, Stelle
from arbiter.katalog.ausgangslage import ausgangslageLaden
from tests.akzeptanz.dienst import spielstandDesVertrags

# Regel: 1 Zoll sind 25,4 mm (domaene/glossar.md, Durchmesser)
millimeterJeZoll = Fraction(254, 10)


# Warum: Lage der Zonen, Ursprung und Achsen der Stelle stehen in technik/architektur.md, S1
breiteDesSpielfelds = 44
längeDerSpielfeldkante = 60
tiefeDerZone = 9
abstandDerReihen = Fraction(5, 2)
tiefeDerErstenReihe = Fraction(3, 2)
durchmesserDerTestmodelle = 32
anzahlGesetzterModelle = 3


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
        # Warum: Schon ein Millionstel Zoll entscheidet, damit Grenzfälle ohne Toleranz gelten.
        self.millionstel = Fraction(1, 1_000_000)
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


def modelleAnDenStellenDesVertragsSetzen(aufstellung: Aufstellung, einheit: Einheit) -> None:
    """Setzt die ersten Modelle der Einheit an die Stellen der Modelle im Beispiel des Vertrags."""
    stellen = [
        Stelle(x=Fraction(str(modell["x"])), y=Fraction(str(modell["y"])))
        for modell in spielstandDesVertrags()["modelle"]
    ]
    for modell, stelle in zip(einheit.modelle, stellen, strict=False):
        aufstellung.modellSetzen(modell, stelle)
