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

millimeterJeZoll = Fraction(254, 10)

millionstel = Fraction(1, 1_000_000)


breiteDesSpielfelds = 44
längeDerSpielfeldkante = 60
tiefeDerZone = 9
abstandDerReihen = Fraction(5, 2)
tiefeDerErstenReihe = Fraction(3, 2)
durchmesserDerTestmodelle = 32
bewegungsweiteDerTestmodelle = Fraction(5)
modellartDerTestmodelle = "Testmodell"
anzahlGesetzterModelle = 3

gerade = (1, 0)
schrägOhneWurzel = (Fraction(3, 5), Fraction(4, 5))


def spielerMit(*modellzahlen: int) -> Spieler:
    einheiten = tuple(
        Einheit(
            name=f"Einheit {nummer}",
            modelle=tuple(
                Modell(
                    modellart=modellartDerTestmodelle,
                    base=Base(durchmesser=durchmesserDerTestmodelle),
                    bewegungsweite=bewegungsweiteDerTestmodelle,
                )
                for _ in range(zahl)
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
    ersteHälfte = zone is Aufstellungszone.erste
    breite = Fraction(tiefe) if ersteHälfte else breiteDesSpielfelds - Fraction(tiefe)
    return Stelle(x=breite, y=Fraction(länge))


def stellenDerEinheit(
    aufstellung: Aufstellung, spieler: Spieler, einheit: Einheit
) -> list[tuple[Modell, Stelle]]:
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


def sperreBei(handlung, *argumente, **benannte) -> Sperre:
    with pytest.raises(Sperre) as sperre:
        handlung(*argumente, **benannte)
    return sperre.value


def sperrgründe(handlung, *argumente, **benannte) -> frozenset[Grund]:
    return sperreBei(handlung, *argumente, **benannte).gründe


def durchmesserJeEinheit(spieler: Spieler) -> tuple[tuple[int, ...], ...]:
    return tuple(
        tuple(modell.base.durchmesser for modell in einheit.modelle)
        for einheit in spieler.armee.einheiten
    )


class Platz:
    def __init__(self, zone: Aufstellungszone) -> None:
        self._zone = zone
        testmodell = Modell(
            modellart=modellartDerTestmodelle,
            base=Base(durchmesser=durchmesserDerTestmodelle),
            bewegungsweite=bewegungsweiteDerTestmodelle,
        )
        self.radius = radiusInZoll(testmodell)
        self.millionstel = millionstel
        self.breiteDesSpielfelds = breiteDesSpielfelds
        self.längeDerSpielfeldkante = längeDerSpielfeldkante
        self.tiefeDerZone = tiefeDerZone
        self.tiefeDerErstenReihe = tiefeDerErstenReihe

    def stelle(self, tiefe, länge) -> Stelle:
        return stelleInZone(self._zone, tiefe, länge)

    def stelleBeimAnderenSpieler(self, abstandDerMittelpunkte, richtung) -> Stelle:
        anteilX, anteilY = richtung
        tiefe = (
            self.breiteDesSpielfelds - self.tiefeDerErstenReihe - abstandDerMittelpunkte * anteilX
        )
        return self.stelle(tiefe, 3 * self.radius + abstandDerMittelpunkte * anteilY)


def modelleSetzen(
    aufstellung: Aufstellung, einheit: Einheit, anzahl: int
) -> list[tuple[Modell, Stelle]]:
    spieler = aufstellung.anDerReihe
    gesetzt = stellenDerEinheit(aufstellung, spieler, einheit)[:anzahl]
    for modell, stelle in gesetzt:
        aufstellung.modellSetzen(modell, stelle)
    return gesetzt


def einheitenAufstellen(aufstellung: Aufstellung, anzahl: int) -> None:
    for _ in range(anzahl):
        spieler = aufstellung.anDerReihe
        nächste = next(
            einheit for einheit in spieler.armee.einheiten if not aufstellung.aufgestellt(einheit)
        )
        einheitAufstellen(aufstellung, nächste)


def alleEinheitenAufstellen(aufstellung: Aufstellung) -> None:
    ausgangslage = aufstellung.ausgangslage
    einheitenAufstellen(
        aufstellung,
        len(ausgangslage.ersterSpieler.armee.einheiten)
        + len(ausgangslage.zweiterSpieler.armee.einheiten),
    )


def modelleAnStellenSetzen(
    aufstellung: Aufstellung, einheit: Einheit, stellen: list[Stelle]
) -> list[tuple[Modell, Stelle]]:
    gesetzte = list(zip(einheit.modelle, stellen, strict=False))
    for modell, stelle in gesetzte:
        aufstellung.modellSetzen(modell, stelle)
    return gesetzte


def inZoll(maß: tuple[Fraction | int, int], radius: Fraction) -> Fraction:
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


def gestreckt(weg: tuple[Fraction, Fraction], faktor: Fraction) -> tuple[Fraction, Fraction]:
    wegInX, wegInY = weg
    return wegInX * faktor, wegInY * faktor


def gezogenesUndRest(
    gesetzte: list[tuple[Modell, Stelle]], *, zweitesGezogen: bool
) -> tuple[tuple[Modell, Stelle], tuple[Modell, Stelle]]:
    erstes, zweites = gesetzte
    return (zweites, erstes) if zweitesGezogen else (erstes, zweites)


def erwarteteStelle(
    aufstellung: Aufstellung, radius: Fraction, erwartet: tuple[tuple, tuple]
) -> Stelle:
    tiefe, länge = erwartet
    return stelleInDerZoneDesSpielersAnDerReihe(
        aufstellung, inZoll(tiefe, radius), inZoll(länge, radius)
    )


def stelleInDerZoneVon(
    aufstellung: Aufstellung, spieler: Spieler, tiefe: Fraction | int, länge: Fraction | int
) -> Stelle:
    return stelleInZone(aufstellung.aufstellungszone(spieler), tiefe, länge)


def stelleInDerZoneDesSpielersAnDerReihe(
    aufstellung: Aufstellung, tiefe: Fraction | int, länge: Fraction | int
) -> Stelle:
    return stelleInDerZoneVon(aufstellung, aufstellung.anDerReihe, tiefe, länge)


def stellenAllerModelle(spielstand) -> dict[Modell, Stelle | None]:
    ausgangslage = spielstand.ausgangslage
    spieler = (ausgangslage.ersterSpieler, ausgangslage.zweiterSpieler)
    return {
        modell: spielstand.stelle(modell) for einer in spieler for modell in einer.armee.modelle
    }


def yamlAusDenDaten(*teileDesPfads: str):
    pfad = Path(__file__).parents[3] / "domaene" / "daten" / Path(*teileDesPfads)
    with pfad.open(encoding="utf-8") as datei:
        return yaml.safe_load(datei)


def modellartenImKatalog(eintrag: dict) -> dict:
    datenblätter = yamlAusDenDaten("katalog", eintrag["fraktion"], "datenblaetter.yaml")
    return datenblätter[eintrag["datenblatt"]]["modellarten"]


def profileDerModelle(eintrag: dict) -> list[tuple[str, dict]]:
    modellarten = modellartenImKatalog(eintrag)
    return [
        (modellart, modellarten[modellart])
        for modellart, anzahl in eintrag["modelle"].items()
        for _ in range(anzahl)
    ]


def eintragDerAusgangslage(datenblatt: str) -> dict:
    armeen = yamlAusDenDaten("ausgangslage.yaml")["Armee"]
    einträge = (eintrag for armee in armeen for eintrag in armee)
    return next(eintrag for eintrag in einträge if eintrag["datenblatt"] == datenblatt)


def reihenDerFormation(einheitenname: str) -> list[int]:
    return yamlAusDenDaten("formation.yaml")["formation"][einheitenname]


def modellZurEbeneMachen(spiel, einheit: Einheit, modell: Modell) -> None:
    spiel.auswählen(einheit)
    spiel.modellAnklicken(modell)
    if not spiel.modellIstEbene(modell):
        raise AssertionError("Der Klick machte das Modell nicht zur Ebene")
