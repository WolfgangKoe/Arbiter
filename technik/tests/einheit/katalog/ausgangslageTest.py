from fractions import Fraction

import pytest

from arbiter.domaene.missionsvorbereitung.ausgangslage import Aufstellungszone
from arbiter.katalog.ausgangslage import ausgangslageAus, ausgangslageLaden
from arbiter.katalog.datenblaetter import Datenblatt, Modellart

modellart = Modellart(bewegungsweite=Fraction(5), durchmesser=32)
datenblätter = {
    "orks": {
        "Boyz": Datenblatt({"Ork Boy": modellart, "Boss Nob": modellart}),
        "Warboss": Datenblatt({"Warboss": modellart}),
        "Flieger": Datenblatt({"Flieger": modellart}, fliegen=True),
    }
}
einheit = {"fraktion": "orks", "datenblatt": "Boyz", "modelle": {"Ork Boy": 1}}
armeenMitBoyz = [[einheit], [einheit]]
formationDerBoyz = {"abstand": 1.5, "formation": {"Boyz": [1]}}


def datenblätterVon(fraktionen: dict):
    def lesen(fraktion: str) -> dict:
        if fraktion not in fraktionen:
            raise ValueError(f"Die Fraktion {fraktion} hat keinen Ordner")
        return fraktionen[fraktion]

    return lesen


def onlyWarMitKante(kante: int) -> dict:
    zone = {"Spielfeldkante": kante, "Tiefe": 9}
    return {
        "Spielfeld": [44, 60],
        "Aufstellungszone": {"erste": zone, "zweite": zone},
        "Schlacht": {"schlachtrunde": 5},
    }


def laden(
    armeen: list,
    formation: dict | None = None,
    onlyWar: dict | None = None,
    fraktionen: dict = datenblätter,
):
    return ausgangslageAus(
        {"Armee": armeen},
        onlyWar or onlyWarMitKante(60),
        formation or formationDerBoyz,
        datenblätterVon(fraktionen),
    )


def testDieModelleEinerEinheitFolgenDenModellartenUndZahlenDerAusgangslage():
    zwei = {"fraktion": "orks", "datenblatt": "Boyz", "modelle": {"Ork Boy": 2, "Boss Nob": 1}}

    ausgangslage = laden([[zwei], [zwei]], {"abstand": 1.5, "formation": {"Boyz": [3]}})

    boyz, *_ = ausgangslage.ersterSpieler.armee.einheiten
    assert boyz.name == "Boyz"
    assert [modell.modellart for modell in boyz.modelle] == ["Ork Boy", "Ork Boy", "Boss Nob"]


def testDieWerteJedesModellsKommenAusSeinerModellart():
    boyz, *_ = laden(armeenMitBoyz).ersterSpieler.armee.einheiten
    modell, *_ = boyz.modelle

    assert (modell.bewegungsweite, modell.base.durchmesser) == (Fraction(5), 32)


def testDieAusgangslageLadenNenntDieEinheitenWieIhreDatenblätter():
    einheiten = ausgangslageLaden().ersterSpieler.armee.einheiten
    (boyz,) = (einheit for einheit in einheiten if einheit.name == "Boyz")

    assert {"Boyz", "Warboss"} <= {einheit.name for einheit in einheiten}
    assert {modell.modellart for modell in boyz.modelle} == {"Ork Boy", "Boss Nob"}


def testDieLetzteSchlachtrundeKommtAusOnlyWar():
    schlachtrunde = 7
    onlyWar = onlyWarMitKante(60) | {"Schlacht": {"schlachtrunde": schlachtrunde}}

    assert laden(armeenMitBoyz, onlyWar=onlyWar).letzteSchlachtrunde == schlachtrunde


@pytest.mark.parametrize(
    "kaputt",
    [
        {"fraktion": "elfen", "datenblatt": "Boyz", "modelle": {"Ork Boy": 1}},
        {"fraktion": "orks", "datenblatt": "Grots", "modelle": {"Ork Boy": 1}},
        {"fraktion": "orks", "datenblatt": "Boyz", "modelle": {"Grot": 1}},
        {"fraktion": "orks", "datenblatt": "Boyz", "modelle": {"Ork Boy": 0}},
        {"fraktion": "orks", "datenblatt": "Boyz", "modelle": {"Ork Boy": 1.5}},
        {"fraktion": "orks", "datenblatt": "Boyz", "modelle": {"Ork Boy": True}},
        {"fraktion": "orks", "datenblatt": "Boyz", "modelle": {}},
        {"fraktion": "orks", "datenblatt": "Boyz"},
        {"fraktion": "orks", "datenblatt": "Boyz", "modelle": {"Ork Boy": 1}, "oc": 2},
    ],
    ids=[
        "fraktionOhneOrdner",
        "datenblattUnbekannt",
        "modellartUnbekannt",
        "zahlNull",
        "zahlMitKomma",
        "zahlWahrheitswert",
        "keineModellart",
        "schlüsselFehlt",
        "schlüsselUnbekannt",
    ],
)
def testEinFehlerhafterEintragEinerEinheitIstEinFehlerBeimLaden(kaputt):
    with pytest.raises(ValueError):
        laden([[kaputt], [einheit]])


def testEineSpielfeldkanteAußerhalbDerZweitenSeitenlängeIstEinFehlerBeimLaden():
    onlyWar = onlyWarMitKante(44)

    with pytest.raises(ValueError):
        laden(armeenMitBoyz, onlyWar=onlyWar)


def testDieDatenVonOnlyWarLaden():
    assert ausgangslageLaden().spielfeld.seitenlängen == (44, 60)


def testEineFehlendeAufstellungszoneIstEinFehlerBeimLaden():
    zone = {"Spielfeldkante": 60, "Tiefe": 9}
    onlyWar = {"Spielfeld": [44, 60], "Aufstellungszone": {"erste": zone}}

    with pytest.raises(ValueError):
        laden(armeenMitBoyz, onlyWar=onlyWar)


def testEineUnbekannteAufstellungszoneIstEinFehlerBeimLaden():
    zone = {"Spielfeldkante": 60, "Tiefe": 9}
    onlyWar = {"Spielfeld": [44, 60], "Aufstellungszone": {"erste": zone, "dritte": zone}}

    with pytest.raises(ValueError):
        laden(armeenMitBoyz, onlyWar=onlyWar)


def testEineEinheitOhneFormationIstEinFehlerBeimLaden():
    with pytest.raises(ValueError):
        laden(armeenMitBoyz, {"abstand": 1.5, "formation": {"Warboss": [1]}})


def testReihenMitAndererModellzahlAlsDieEinheitIstEinFehlerBeimLaden():
    with pytest.raises(ValueError):
        laden(armeenMitBoyz, {"abstand": 1.5, "formation": {"Boyz": [2]}})


def testEineEinheitMitVerschiedenenDurchmessernIstEinFehlerBeimLaden():
    breit = Modellart(bewegungsweite=Fraction(5), durchmesser=40)
    gemischt = {"orks": {"Boyz": Datenblatt({"Ork Boy": modellart, "Boss Nob": breit})}}
    zwei = {"fraktion": "orks", "datenblatt": "Boyz", "modelle": {"Ork Boy": 1, "Boss Nob": 1}}

    with pytest.raises(ValueError):
        laden([[zwei], [zwei]], {"abstand": 1.5, "formation": {"Boyz": [2]}}, fraktionen=gemischt)


def testDieEinheitÜbernimmtFliegenIhresDatenblatts():
    flieger = {"fraktion": "orks", "datenblatt": "Flieger", "modelle": {"Flieger": 1}}
    formation = {"abstand": 1.5, "formation": {"Boyz": [1], "Flieger": [1]}}

    ausgangslage = laden([[einheit, flieger], [einheit]], formation)

    boyz, fliegerEinheit = ausgangslage.ersterSpieler.armee.einheiten
    assert (boyz.fliegen, fliegerEinheit.fliegen) == (False, True)


@pytest.mark.parametrize("reihen", [[1, 0], [2, -1]], ids=["leereReihe", "negativeReihe"])
def testEineReiheKeineZahlÜberNullIstEinFehlerBeimLaden(reihen):
    with pytest.raises(ValueError):
        laden(armeenMitBoyz, {"abstand": 1.5, "formation": {"Boyz": reihen}})


def testDieTiefenDerAusgangslageLassenSichNichtÄndern():
    tiefen = ausgangslageLaden().tiefen

    with pytest.raises(TypeError):
        tiefen[Aufstellungszone.erste] = Fraction(30)
