"""AUF-8 · Ziehen."""

from fractions import Fraction

import pytest

from arbiter.domaene.spielobjekte import Stelle
from tests.akzeptanz.auswahl import auswählenMit
from tests.akzeptanz.handgriffe import (
    nachDerWahlDerAufstellungszone,
    radiusInZoll,
    stelleDesErstenModells,
    stelleInDerZoneVon,
    stellenAllerModelle,
)
from tests.akzeptanz.ziehen import (
    Bildpunkt,
    liegtEinPixelGenauAn,
    modellAmPunktZiehen,
    modellZiehen,
    punktAufDerKarte,
    ziehenOhneAnfrage,
    zollJePixel,
)

zugschwelleInPixeln = 4
abweichungUnterDerSchwelle = zugschwelleInPixeln - 1


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
    bildschirm, aufstellungNachDerZonenwahl, boyzSetzen, eingabe
):
    [(modell, stelleDavor)] = boyzSetzen(1)
    ziel = Stelle(x=stelleDavor.x, y=stelleDavor.y + Fraction(1, 2))
    seite = bildschirm.seiteZu(aufstellungNachDerZonenwahl, berührbar=eingabe == "finger")
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
    bildschirm, aufstellungNachDerZonenwahl, boyzSetzen, eingabe
):
    [(modell, stelleDavor)] = boyzSetzen(1)
    seite = bildschirm.seiteZu(aufstellungNachDerZonenwahl, berührbar=eingabe == "finger")
    mitte = punktAufDerKarte(seite, stelleDavor)
    radiusInPixeln = float(radiusInZoll(modell)) / zollJePixel(seite)
    versatzDesGriffsInPixeln = radiusInPixeln * 0.8
    griff = Bildpunkt(mitte.links + versatzDesGriffsInPixeln, mitte.oben)
    wegInPixeln = float(Fraction(1, 2)) / zollJePixel(seite)
    ende = Bildpunkt(griff.links, griff.oben + wegInPixeln)
    erwartet = Stelle(x=stelleDavor.x, y=stelleDavor.y + Fraction(1, 2))
    assert versatzDesGriffsInPixeln > zugschwelleInPixeln

    modellAmPunktZiehen(seite, griff, ende, eingabe)

    assert liegtEinPixelGenauAn(seite, aufstellungNachDerZonenwahl.stelle(modell), erwartet)
