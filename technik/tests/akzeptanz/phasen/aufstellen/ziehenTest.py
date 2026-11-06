"""AUF-8 · Ziehen."""

from fractions import Fraction

import pytest
from playwright.sync_api import Browser

from arbiter.domaene.spielobjekte import Stelle
from tests.akzeptanz.auswahl import auswählenMit
from tests.akzeptanz.bildschirm import Bildschirm, seiteDerSchlachtMitEingabe
from tests.akzeptanz.handgriffe import (
    nachDerWahlDerAufstellungszone,
    radiusInZoll,
    stelleDesErstenModells,
    stelleInDerZoneVon,
    stellenAllerModelle,
    versetzt,
)
from tests.akzeptanz.ziehen import (
    Bildpunkt,
    griffAbseitsDerMitte,
    liegtEinPixelGenauAn,
    mitMausUndFinger,
    modellAmPunktZiehen,
    modellZiehen,
    punktAufDerKarte,
    ziehenOhneAnfrage,
    zollJePixel,
    zugschwelleInPixeln,
)

abweichungUnterDerSchwelle = zugschwelleInPixeln - 1
dreiZollNachOsten = (Fraction(3), Fraction(0))


@pytest.fixture
def bildschirmMitGroßemFenster(browser: Browser):
    bildschirm = Bildschirm(browser, fenster={"width": 1920, "height": 1080})
    yield bildschirm
    bildschirm.beenden()


def testAuf8_2EinGesetztesModellIstNachDemLoslassenAnDerStelleDesLoslassensGesetzt(
    aufstellung, ersterSpieler, zweiterSpieler
):
    nachDerWahlDerAufstellungszone(aufstellung, gewinner=ersterSpieler)
    einheit, _ = zweiterSpieler.armee.einheiten
    modell, _ = einheit.modelle
    aufstellung.modellSetzen(modell, stelleDesErstenModells(aufstellung, zweiterSpieler, einheit))
    stelleDesLoslassens = stelleInDerZoneVon(aufstellung, zweiterSpieler, 4, 20)

    aufstellung.modellLoslassen(modell, stelleDesLoslassens)

    assert aufstellung.gesetzt(modell)
    assert aufstellung.stelle(modell) == stelleDesLoslassens


@pytest.mark.parametrize("eingabe", ["maus", "finger"])
def testAuf8_2EinModellWirdUmWenigerAlsSeinenRadiusGezogenUndAnDerStelleDesLoslassensGesetzt(
    bildschirmMitGroßemFenster, aufstellungNachDerZonenwahl, boyzSetzen, eingabe
):
    [(modell, stelleDavor)] = boyzSetzen(1)
    ziel = Stelle(x=stelleDavor.x, y=stelleDavor.y + Fraction(1, 2))
    seite = bildschirmMitGroßemFenster.seiteZu(
        aufstellungNachDerZonenwahl, berührbar=eingabe == "finger"
    )
    zugInPixeln = float(Fraction(1, 2)) / zollJePixel(seite)
    radiusInPixeln = float(radiusInZoll(modell)) / zollJePixel(seite)
    assert zugschwelleInPixeln < zugInPixeln < radiusInPixeln

    modellZiehen(seite, stelleDavor, ziel, eingabe)

    assert liegtEinPixelGenauAn(seite, aufstellungNachDerZonenwahl.stelle(modell), ziel)


@pytest.mark.parametrize("eingabe", ["maus", "finger"])
def testAuf8_2EinModellBleibtBeiWenigerAlsDerZugschwelleAbweichungAnSeinerStelle(
    bildschirm, aufstellungNachDerZonenwahl, boyzSetzen, eingabe
):
    [(_, stelleDavor)] = boyzSetzen(1)
    seite = bildschirm.seiteZu(aufstellungNachDerZonenwahl, berührbar=eingabe == "finger")
    auswählenMit[eingabe](seite, "Spieler 1", "Boyz")
    davor = stellenAllerModelle(aufstellungNachDerZonenwahl)
    start = punktAufDerKarte(seite, stelleDavor)
    ziel = Bildpunkt(
        start.links + abweichungUnterDerSchwelle, start.oben + abweichungUnterDerSchwelle
    )

    anfragen = ziehenOhneAnfrage(seite, start, ziel, eingabe)

    assert [anfrage for anfrage in anfragen if anfrage.url.endswith("/stelle")] == []
    assert stellenAllerModelle(aufstellungNachDerZonenwahl) == davor


@pytest.mark.parametrize("eingabe", ["maus", "finger"])
def testAuf8_7EinModellFolgtDemWegDesZeigersUndNichtDemPunktUnterDemZeiger(
    bildschirmMitGroßemFenster, aufstellungNachDerZonenwahl, boyzSetzen, eingabe
):
    [(modell, stelleDavor)] = boyzSetzen(1)
    seite = bildschirmMitGroßemFenster.seiteZu(
        aufstellungNachDerZonenwahl, berührbar=eingabe == "finger"
    )
    griff = griffAbseitsDerMitte(seite, modell, punktAufDerKarte(seite, stelleDavor))
    wegInPixeln = float(Fraction(1, 2)) / zollJePixel(seite)
    ende = Bildpunkt(griff.links, griff.oben + wegInPixeln)
    erwartet = Stelle(x=stelleDavor.x, y=stelleDavor.y + Fraction(1, 2))

    modellAmPunktZiehen(seite, griff, ende, eingabe)

    assert liegtEinPixelGenauAn(seite, aufstellungNachDerZonenwahl.stelle(modell), erwartet)


@mitMausUndFinger
def testAuf8_7InDerBewegungsphaseFolgtEinModellDemWegDesZeigersUndNichtDemPunktUnterDemZeiger(
    bildschirmMitGroßemFenster, beendeteAufstellung, schlachtInDerBewegungsphase, warboss, eingabe
):
    (modell,) = warboss.modelle
    davor = schlachtInDerBewegungsphase.stelle(modell)
    erwartet = versetzt(davor, dreiZollNachOsten)
    seite = seiteDerSchlachtMitEingabe(
        bildschirmMitGroßemFenster, beendeteAufstellung, schlachtInDerBewegungsphase, eingabe
    )
    mitte = punktAufDerKarte(seite, davor)
    punktDesErwarteten = punktAufDerKarte(seite, erwartet)
    griff = griffAbseitsDerMitte(seite, modell, mitte)
    ende = Bildpunkt(
        griff.links + punktDesErwarteten.links - mitte.links,
        griff.oben + punktDesErwarteten.oben - mitte.oben,
    )

    modellAmPunktZiehen(seite, griff, ende, eingabe)

    assert liegtEinPixelGenauAn(seite, schlachtInDerBewegungsphase.stelle(modell), erwartet)
