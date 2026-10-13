from fractions import Fraction

import pytest

from arbiter.domaene.missionsvorbereitung.ausgangslage import Aufstellungszone
from arbiter.katalog.ausgangslage import ausgangslageAus, ausgangslageLaden

einheitMitDurchmesser = {"Einheit": "Boyz", "durchmesser": [32]}
armeen = [[einheitMitDurchmesser], [einheitMitDurchmesser]]
formation = {"abstand": 1.5, "formation": {"Boyz": [1]}}


def onlyWarMitKante(kante: int) -> dict:
    zone = {"Spielfeldkante": kante, "Tiefe": 9}
    return {"Spielfeld": [44, 60], "Aufstellungszone": {"erste": zone, "zweite": zone}}


def testEineSpielfeldkanteAußerhalbDerZweitenSeitenlängeIstEinFehlerBeimLaden():
    onlyWar = onlyWarMitKante(44)

    with pytest.raises(ValueError):
        ausgangslageAus({"Armee": armeen}, onlyWar, formation)


def testEinDurchmesserMitKommaIstEinFehlerBeimLaden():
    kaputt = [[{"Einheit": "Boyz", "durchmesser": [28.5]}], [einheitMitDurchmesser]]

    onlyWar = onlyWarMitKante(60)

    with pytest.raises(ValueError):
        ausgangslageAus({"Armee": kaputt}, onlyWar, formation)


def testDieDatenVonOnlyWarLaden():
    assert ausgangslageLaden().spielfeld.seitenlängen == (44, 60)


@pytest.mark.parametrize("durchmesser", [True, 0, -5], ids=["wahrheitswert", "null", "negativ"])
def testEinDurchmesserKeinePositiveGanzeZahlIstEinFehlerBeimLaden(durchmesser):
    kaputt = [[{"Einheit": "Boyz", "durchmesser": [durchmesser]}], [einheitMitDurchmesser]]

    onlyWar = onlyWarMitKante(60)

    with pytest.raises(ValueError):
        ausgangslageAus({"Armee": kaputt}, onlyWar, formation)


def testEineFehlendeAufstellungszoneIstEinFehlerBeimLaden():
    zone = {"Spielfeldkante": 60, "Tiefe": 9}
    onlyWar = {"Spielfeld": [44, 60], "Aufstellungszone": {"erste": zone}}

    with pytest.raises(ValueError):
        ausgangslageAus({"Armee": armeen}, onlyWar, formation)


def testEineUnbekannteAufstellungszoneIstEinFehlerBeimLaden():
    zone = {"Spielfeldkante": 60, "Tiefe": 9}
    onlyWar = {"Spielfeld": [44, 60], "Aufstellungszone": {"erste": zone, "dritte": zone}}

    with pytest.raises(ValueError):
        ausgangslageAus({"Armee": armeen}, onlyWar, formation)


def testEineEinheitOhneFormationIstEinFehlerBeimLaden():
    ohne = {"abstand": 1.5, "formation": {"Warboss": [1]}}
    onlyWar = onlyWarMitKante(60)

    with pytest.raises(ValueError):
        ausgangslageAus({"Armee": armeen}, onlyWar, ohne)


def testReihenMitAndererModellzahlAlsDieEinheitIstEinFehlerBeimLaden():
    falsch = {"abstand": 1.5, "formation": {"Boyz": [2]}}
    onlyWar = onlyWarMitKante(60)

    with pytest.raises(ValueError):
        ausgangslageAus({"Armee": armeen}, onlyWar, falsch)


def testEineEinheitMitVerschiedenenDurchmessernIstEinFehlerBeimLaden():
    gemischt = {"Einheit": "Boyz", "durchmesser": [32, 40]}
    zwei = {"abstand": 1.5, "formation": {"Boyz": [2]}}
    onlyWar = onlyWarMitKante(60)

    with pytest.raises(ValueError):
        ausgangslageAus({"Armee": [[gemischt], [gemischt]]}, onlyWar, zwei)


def testEineReiheOhneModellIstEinFehlerBeimLaden():
    zweiModelle = {"Einheit": "Boyz", "durchmesser": [32, 32]}
    leer = {"abstand": 1.5, "formation": {"Boyz": [2, 0]}}
    onlyWar = onlyWarMitKante(60)

    with pytest.raises(ValueError):
        ausgangslageAus({"Armee": [[zweiModelle], [zweiModelle]]}, onlyWar, leer)


def testEineNegativeReiheIstEinFehlerBeimLaden():
    dreiModelle = {"Einheit": "Boyz", "durchmesser": [32, 32, 32]}
    negativ = {"abstand": 1.5, "formation": {"Boyz": [4, -1]}}
    onlyWar = onlyWarMitKante(60)

    with pytest.raises(ValueError):
        ausgangslageAus({"Armee": [[dreiModelle], [dreiModelle]]}, onlyWar, negativ)


def testDieTiefenDerAusgangslageLassenSichNichtÄndern():
    tiefen = ausgangslageLaden().tiefen

    with pytest.raises(TypeError):
        tiefen[Aufstellungszone.erste] = Fraction(30)
