"""QUE-3 · Bedienung."""

import pytest

from arbiter.domaene.sperre import Grund
from tests.akzeptanz.auswahl import (
    ausgewählteEinheiten,
    ausgewählteModelle,
    klickenUndWarten,
    tippenUndWarten,
)
from tests.akzeptanz.bildschirm import (
    gesperrteModelle,
    gründeAlsText,
    inhaltDerSeite,
    neuLaden,
    seiteMitEingabe,
    sperrmeldungWarten,
)
from tests.akzeptanz.dienst import auswählen, dienstFür, spielstandVon
from tests.akzeptanz.handgriffe import (
    anzahlGesetzterModelle,
    einheitAufstellen,
    modelleSetzen,
    nachDerWahlDerAufstellungszone,
    stelleDesErstenModells,
    stelleInDerZoneVon,
    stellenDerEinheit,
)
from tests.akzeptanz.ziehen import (
    liegtEinPixelGenauAn,
    modellAufDieAblageZiehen,
    modellZiehen,
)

mitMausUndFinger = pytest.mark.parametrize("eingabe", ["maus", "finger"])
gründeAufDemModellDesAnderen = {
    Grund.baseÜberdeckt,
    Grund.nahkampfreichweite,
    Grund.nichtGanzInDerZone,
}


def einModellAufDemModellDesAnderenSpielers(aufstellung, ersterSpieler, zweiterSpieler):
    """Das erste Modell des ersten Spielers ist gesperrt, mit allen drei Gründen."""
    nachDerWahlDerAufstellungszone(aufstellung, gewinner=ersterSpieler)
    einheitDesAnderen, _ = zweiterSpieler.armee.einheiten
    einheit, _ = ersterSpieler.armee.einheiten
    modell, _ = einheit.modelle
    einheitAufstellen(aufstellung, einheitDesAnderen)
    aufstellung.modellSetzen(modell, stelleDesErstenModells(aufstellung, ersterSpieler, einheit))
    (_, stelleDesAnderen), _ = stellenDerEinheit(aufstellung, zweiterSpieler, einheitDesAnderen)
    aufstellung.modellLoslassen(modell, stelleDesAnderen)
    return modell


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


def testQue3_2DerDienstLiefertAufJedeWeitereAnfrageDenselbenSpielstandWieDavor(
    dienst, aufstellungNachDerZonenwahl, boyz
):
    modelleSetzen(aufstellungNachDerZonenwahl, boyz, anzahlGesetzterModelle)
    davor = auswählen(dienst, "Boyz").get_json()

    danach = spielstandVon(dienst)

    assert danach == davor
    assert spielstandVon(dienst) == davor


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


@mitMausUndFinger
def testQue3_4EinModellAufDieKarteZiehenUndLoslassenSetztEsAnDieStelleDesLoslassens(
    bildschirm, aufstellungNachDerZonenwahl, boyzSetzen, spielerEins, eingabe
):
    _, (zweitesModell, stelleDavor) = boyzSetzen(2)
    ziel = stelleInDerZoneVon(aufstellungNachDerZonenwahl, spielerEins, 6, 40)
    seite = seiteMitEingabe(bildschirm, aufstellungNachDerZonenwahl, eingabe)

    modellZiehen(seite, stelleDavor, ziel, eingabe)

    assert aufstellungNachDerZonenwahl.gesetzt(zweitesModell)
    assert liegtEinPixelGenauAn(seite, aufstellungNachDerZonenwahl.stelle(zweitesModell), ziel)


@mitMausUndFinger
def testQue3_4EinModellAufDieAblageZiehenUndLoslassenLässtJedesModellWoEsWar(
    bildschirm, aufstellungNachDerZonenwahl, boyzSetzen, eingabe
):
    (erstesModell, ersteStelle), (zweitesModell, stelleDavor) = boyzSetzen(2)
    seite = seiteMitEingabe(bildschirm, aufstellungNachDerZonenwahl, eingabe)

    modellAufDieAblageZiehen(seite, stelleDavor, "Spieler 1", eingabe)

    assert aufstellungNachDerZonenwahl.stelle(zweitesModell) == stelleDavor
    assert aufstellungNachDerZonenwahl.stelle(erstesModell) == ersteStelle


@pytest.mark.parametrize("erneut", ["neuLaden", "adresseErneutÖffnen"])
def testQue3_5EinGesperrtesModellIstNachDemErneutenÖffnenWeiterGesperrtMitJedemGrund(
    bildschirm, aufstellung, ersterSpieler, zweiterSpieler, erneut
):
    gesperrtesModell = einModellAufDemModellDesAnderenSpielers(
        aufstellung, ersterSpieler, zweiterSpieler
    )
    davor = bildschirm.seiteZu(aufstellung)
    gründeDavor = sperrmeldungWarten(davor, gründeAufDemModellDesAnderen)
    gesperrtDavor = gesperrteModelle(davor)

    if erneut == "neuLaden":
        neuLaden(davor)
        danach = davor
    else:
        danach = bildschirm.seiteBei(davor.url)

    assert sperrmeldungWarten(danach, gründeAufDemModellDesAnderen) == gründeDavor
    assert gründeDavor == gründeAlsText(gründeAufDemModellDesAnderen)
    assert gesperrteModelle(danach) == gesperrtDavor
    assert len(gesperrtDavor) == 1
    assert aufstellung.gesperrt(gesperrtesModell)


def testQue3_5DerDienstMeldetEinGesperrtesModellAufJedeWeitereAnfrageWieDavor(
    aufstellung, ersterSpieler, zweiterSpieler
):
    gesperrtesModell = einModellAufDemModellDesAnderenSpielers(
        aufstellung, ersterSpieler, zweiterSpieler
    )
    dienst = dienstFür(aufstellung)
    davor = spielstandVon(dienst)

    danach = spielstandVon(dienst)

    gesperrte = [modell for modell in danach["modelle"] if modell["gesperrt"]]
    assert len(gesperrte) == 1
    assert danach["gründeDerGesperrten"] == davor["gründeDerGesperrten"]
    assert set(danach["gründeDerGesperrten"]) == gründeAlsText(gründeAufDemModellDesAnderen)
    assert danach == davor
    assert aufstellung.gesperrt(gesperrtesModell)
