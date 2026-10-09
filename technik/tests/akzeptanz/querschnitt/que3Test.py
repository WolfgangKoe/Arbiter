"""QUE-3 · Bedienung."""

import pytest

from tests.akzeptanz.bildschirm import (
    ausgewählteEinheiten,
    ausgewählteModelle,
    inhaltDerSeite,
    klickenUndWarten,
    neuLaden,
    tippenUndWarten,
)
from tests.akzeptanz.dienst import auswählen, spielstandVon
from tests.akzeptanz.handgriffe import anzahlGesetzterModelle, modelleSetzen


def kreisAufDerKarte(seite):
    return seite.locator(".karte .modell").first


def testQue3_1EinTippenAufEineKarteInDerAblageMachtDieEinheitAusgewähltWieEinKlick(
    bildschirm, aufstellungNachDerZonenwahl
):
    mitMaus = bildschirm.seiteZu(aufstellungNachDerZonenwahl)
    mitFinger = bildschirm.seiteZu(aufstellungNachDerZonenwahl, berührbar=True)

    klickenUndWarten(mitMaus, "Spieler 2", "Necron Warriors")
    tippenUndWarten(mitFinger, "Spieler 2", "Necron Warriors")

    assert ausgewählteEinheiten(mitFinger) == ausgewählteEinheiten(mitMaus) == {"Necron Warriors"}


def testQue3_1EinTippenAufEineAusgewählteEinheitMachtSieNichtAusgewähltWieEinKlick(
    bildschirm, aufstellungNachDerZonenwahl
):
    mitMaus = bildschirm.seiteZu(aufstellungNachDerZonenwahl)
    mitFinger = bildschirm.seiteZu(aufstellungNachDerZonenwahl, berührbar=True)
    klickenUndWarten(mitMaus, "Spieler 1", "Boyz")
    tippenUndWarten(mitFinger, "Spieler 1", "Boyz")

    klickenUndWarten(mitMaus, "Spieler 1", "Boyz")
    tippenUndWarten(mitFinger, "Spieler 1", "Boyz")

    assert ausgewählteEinheiten(mitFinger) == ausgewählteEinheiten(mitMaus) == frozenset()


def testQue3_1EinTippenAufDieKarteLöstDasselbeAusWieEinKlick(
    bildschirm, aufstellungNachDerZonenwahl, boyz
):
    modelleSetzen(aufstellungNachDerZonenwahl, boyz, anzahlGesetzterModelle)
    mitMaus = bildschirm.seiteZu(aufstellungNachDerZonenwahl)
    mitFinger = bildschirm.seiteZu(aufstellungNachDerZonenwahl, berührbar=True)
    klickenUndWarten(mitMaus, "Spieler 1", "Boyz")
    tippenUndWarten(mitFinger, "Spieler 1", "Boyz")

    kreisAufDerKarte(mitMaus).click()
    kreisAufDerKarte(mitFinger).tap()

    assert inhaltDerSeite(mitFinger) == inhaltDerSeite(mitMaus)
    assert ausgewählteModelle(mitFinger) == ausgewählteModelle(mitMaus)


@pytest.mark.parametrize("erneut", ["neuLaden", "adresseErneutÖffnen"])
def testQue3_2ÖffnetEinSpielerDieAdresseErneutZeigenKarteUndAblagenDasselbeWieDavor(
    bildschirm, aufstellungNachDerZonenwahl, boyz, erneut
):
    modelleSetzen(aufstellungNachDerZonenwahl, boyz, anzahlGesetzterModelle)
    davor = bildschirm.seiteZu(aufstellungNachDerZonenwahl)
    klickenUndWarten(davor, "Spieler 1", "Boyz")

    if erneut == "neuLaden":
        neuLaden(davor)
        danach = davor
    else:
        danach = bildschirm.seiteBei(davor.url)

    assert ausgewählteEinheiten(danach) == {"Boyz"}
    assert len(ausgewählteModelle(danach)) == anzahlGesetzterModelle
    assert inhaltDerSeite(danach) == inhaltDerSeite(davor)


def testQue3_3NachDemNeustartZeigenKarteUndAblagenDieAusgangslageStattDesStandsDavor(
    befehl, bildschirm
):
    adresseDavor = befehl.starten()
    davor = bildschirm.seiteBei(adresseDavor)
    ausgangslageMitWahl = inhaltDerSeite(davor)
    klickenUndWarten(davor, "Spieler 1", "Boyz")
    standDavor = inhaltDerSeite(davor)
    befehl.beenden()

    adresseDanach = befehl.starten()
    danach = bildschirm.seiteBei(adresseDanach)

    assert standDavor != ausgangslageMitWahl
    assert inhaltDerSeite(danach) == ausgangslageMitWahl
    assert ausgewählteEinheiten(danach) == frozenset()


def testQue3_2DerDienstLiefertAufJedeWeitereAnfrageDenselbenSpielstandWieDavor(
    dienst, aufstellungNachDerZonenwahl, boyz
):
    modelleSetzen(aufstellungNachDerZonenwahl, boyz, anzahlGesetzterModelle)
    davor = auswählen(dienst, "Boyz").get_json()

    danach = spielstandVon(dienst)

    assert danach == davor
    assert spielstandVon(dienst) == davor
