import pytest

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
