from fractions import Fraction

import pytest

from arbiter.domaene.phasen.aufstellen import Aufstellungszone
from arbiter.katalog.ausgangslage import ausgangslageAus, ausgangslageLaden

einheitMitDurchmesser = {"Einheit": "Boyz", "durchmesser": [32]}
armeen = [[einheitMitDurchmesser], [einheitMitDurchmesser]]


def onlyWarMitKante(kante: int) -> dict:
    zone = {"Spielfeldkante": kante, "Tiefe": 9}
    return {"Spielfeld": [44, 60], "Aufstellungszone": {"erste": zone, "zweite": zone}}


def testEineSpielfeldkanteAußerhalbDerZweitenSeitenlängeIstEinFehlerBeimLaden():
    with pytest.raises(ValueError):
        ausgangslageAus({"Armee": armeen}, onlyWarMitKante(44))


def testEinDurchmesserMitKommaIstEinFehlerBeimLaden():
    kaputt = [[{"Einheit": "Boyz", "durchmesser": [28.5]}], [einheitMitDurchmesser]]

    with pytest.raises(ValueError):
        ausgangslageAus({"Armee": kaputt}, onlyWarMitKante(60))


def testDieDatenVonOnlyWarLaden():
    assert ausgangslageLaden().spielfeld.seitenlängen == (44, 60)


@pytest.mark.parametrize("durchmesser", [True, 0, -5], ids=["wahrheitswert", "null", "negativ"])
def testEinDurchmesserKeinePositiveGanzeZahlIstEinFehlerBeimLaden(durchmesser):
    kaputt = [[{"Einheit": "Boyz", "durchmesser": [durchmesser]}], [einheitMitDurchmesser]]

    with pytest.raises(ValueError):
        ausgangslageAus({"Armee": kaputt}, onlyWarMitKante(60))


def testEineFehlendeAufstellungszoneIstEinFehlerBeimLaden():
    zone = {"Spielfeldkante": 60, "Tiefe": 9}
    onlyWar = {"Spielfeld": [44, 60], "Aufstellungszone": {"erste": zone}}

    with pytest.raises(ValueError):
        ausgangslageAus({"Armee": armeen}, onlyWar)


def testEineUnbekannteAufstellungszoneIstEinFehlerBeimLaden():
    zone = {"Spielfeldkante": 60, "Tiefe": 9}
    onlyWar = {"Spielfeld": [44, 60], "Aufstellungszone": {"erste": zone, "dritte": zone}}

    with pytest.raises(ValueError):
        ausgangslageAus({"Armee": armeen}, onlyWar)


def testDieTiefenDerAusgangslageLassenSichNichtÄndern():
    tiefen = ausgangslageLaden().tiefen

    with pytest.raises(TypeError):
        tiefen[Aufstellungszone.erste] = Fraction(30)
