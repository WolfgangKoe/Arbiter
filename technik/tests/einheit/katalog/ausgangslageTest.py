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
    onlyWar = onlyWarMitKante(44)

    with pytest.raises(ValueError):
        ausgangslageAus({"Armee": armeen}, onlyWar)


def testEinDurchmesserMitKommaIstEinFehlerBeimLaden():
    kaputt = [[{"Einheit": "Boyz", "durchmesser": [28.5]}], [einheitMitDurchmesser]]

    onlyWar = onlyWarMitKante(60)

    with pytest.raises(ValueError):
        ausgangslageAus({"Armee": kaputt}, onlyWar)


def testDieDatenVonOnlyWarLaden():
    assert ausgangslageLaden().spielfeld.seitenlängen == (44, 60)


@pytest.mark.parametrize("durchmesser", [True, 0, -5], ids=["wahrheitswert", "null", "negativ"])
def testEinDurchmesserKeinePositiveGanzeZahlIstEinFehlerBeimLaden(durchmesser):
    kaputt = [[{"Einheit": "Boyz", "durchmesser": [durchmesser]}], [einheitMitDurchmesser]]

    onlyWar = onlyWarMitKante(60)

    with pytest.raises(ValueError):
        ausgangslageAus({"Armee": kaputt}, onlyWar)


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
