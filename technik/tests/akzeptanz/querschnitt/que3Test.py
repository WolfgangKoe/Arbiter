"""QUE-3 · Bedienung."""

import re

import pytest
from playwright.sync_api import expect

from tests.akzeptanz.bildschirm import (
    ausgewählteEinheiten,
    ausgewählteModelle,
    einheitenKarteVon,
    inhaltDerSeite,
)
from tests.akzeptanz.handgriffe import modelleSetzen

ausgewähltGekennzeichnet = re.compile(r"\bausgewählt\b")
anzahlGesetzterModelle = 3


def kreisAufDerKarte(seite):
    return seite.locator(".karte .modell").first


def testQue3_1EinTippenAufEineKarteInDerAblageMachtDieEinheitAusgewähltWieEinKlick(
    bildschirm, aufstellungNachDerZonenwahl
):
    mitMaus = bildschirm.seiteZu(aufstellungNachDerZonenwahl)
    mitFinger = bildschirm.seiteZu(aufstellungNachDerZonenwahl, berührbar=True)

    einheitenKarteVon(mitMaus, "Spieler 2", "Necron Warriors").click()
    einheitenKarteVon(mitFinger, "Spieler 2", "Necron Warriors").tap()

    for seite in (mitMaus, mitFinger):
        expect(einheitenKarteVon(seite, "Spieler 2", "Necron Warriors")).to_have_class(
            ausgewähltGekennzeichnet
        )
    assert ausgewählteEinheiten(mitFinger) == ausgewählteEinheiten(mitMaus)


def testQue3_1EinTippenAufEineAusgewählteEinheitMachtSieNichtAusgewähltWieEinKlick(
    bildschirm, aufstellungNachDerZonenwahl
):
    mitMaus = bildschirm.seiteZu(aufstellungNachDerZonenwahl)
    mitFinger = bildschirm.seiteZu(aufstellungNachDerZonenwahl, berührbar=True)
    einheitenKarteVon(mitMaus, "Spieler 1", "Boyz").click()
    einheitenKarteVon(mitFinger, "Spieler 1", "Boyz").tap()
    expect(einheitenKarteVon(mitMaus, "Spieler 1", "Boyz")).to_have_class(ausgewähltGekennzeichnet)
    expect(einheitenKarteVon(mitFinger, "Spieler 1", "Boyz")).to_have_class(
        ausgewähltGekennzeichnet
    )

    einheitenKarteVon(mitMaus, "Spieler 1", "Boyz").click()
    einheitenKarteVon(mitFinger, "Spieler 1", "Boyz").tap()

    for seite in (mitMaus, mitFinger):
        expect(einheitenKarteVon(seite, "Spieler 1", "Boyz")).not_to_have_class(
            ausgewähltGekennzeichnet
        )
    assert ausgewählteEinheiten(mitFinger) == ausgewählteEinheiten(mitMaus) == frozenset()


def testQue3_1EinTippenAufDieKarteLöstDasselbeAusWieEinKlick(
    bildschirm, aufstellungNachDerZonenwahl, boyz
):
    modelleSetzen(aufstellungNachDerZonenwahl, boyz, anzahlGesetzterModelle)
    mitMaus = bildschirm.seiteZu(aufstellungNachDerZonenwahl)
    mitFinger = bildschirm.seiteZu(aufstellungNachDerZonenwahl, berührbar=True)
    einheitenKarteVon(mitMaus, "Spieler 1", "Boyz").click()
    einheitenKarteVon(mitFinger, "Spieler 1", "Boyz").tap()
    expect(einheitenKarteVon(mitMaus, "Spieler 1", "Boyz")).to_have_class(ausgewähltGekennzeichnet)
    expect(einheitenKarteVon(mitFinger, "Spieler 1", "Boyz")).to_have_class(
        ausgewähltGekennzeichnet
    )

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
    einheitenKarteVon(davor, "Spieler 1", "Boyz").click()
    expect(einheitenKarteVon(davor, "Spieler 1", "Boyz")).to_have_class(ausgewähltGekennzeichnet)

    if erneut == "neuLaden":
        davor.reload()
        davor.wait_for_selector(".karte .spielfeld")
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
    einheitenKarteVon(davor, "Spieler 1", "Boyz").click()
    expect(einheitenKarteVon(davor, "Spieler 1", "Boyz")).to_have_class(ausgewähltGekennzeichnet)
    standDavor = inhaltDerSeite(davor)
    befehl.beenden()

    adresseDanach = befehl.starten()
    danach = bildschirm.seiteBei(adresseDanach)

    assert standDavor != ausgangslageMitWahl
    assert inhaltDerSeite(danach) == ausgangslageMitWahl
    assert ausgewählteEinheiten(danach) == frozenset()
