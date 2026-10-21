"""AUF-8 · Ziehen."""

from fractions import Fraction

import pytest

from arbiter.domaene.sperre import Grund
from arbiter.domaene.spielobjekte import Stelle
from tests.akzeptanz.handgriffe import (
    einheitAufstellen,
    nachDerWahlDerAufstellungszone,
    radiusInZoll,
    sperrgründe,
    stelleDesErstenModells,
    stelleInDerZoneVon,
    stellenAllerModelle,
)
from tests.akzeptanz.ziehen import (
    Bildpunkt,
    liegtEinPixelGenauAn,
    modellZiehen,
    punktAufDerKarte,
    ziehenOhneAnfrage,
    zollJePixel,
)

# Regel: Architektur V8, ab dieser Abweichung beginnt ein Zug
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
    davor = stellenAllerModelle(aufstellungNachDerZonenwahl)
    start = punktAufDerKarte(seite, stelleDavor)
    ziel = Bildpunkt(
        start.links + abweichungUnterDerSchwelle, start.oben + abweichungUnterDerSchwelle
    )

    anfragen = ziehenOhneAnfrage(seite, start, ziel, eingabe)

    assert anfragen == []
    assert stellenAllerModelle(aufstellungNachDerZonenwahl) == davor


@pytest.mark.parametrize("ablage", ["eigeneAblage", "ablageDesAnderen"])
def testAuf8_4EinModellEinerAufgestelltenEinheitIstAufEinerAblageNichtWählbar(
    aufstellung, ersterSpieler, zweiterSpieler, ablage
):
    nachDerWahlDerAufstellungszone(aufstellung, gewinner=ersterSpieler)
    aufgestellteEinheit, _ = zweiterSpieler.armee.einheiten
    modell, _ = aufgestellteEinheit.modelle
    einheitAufstellen(aufstellung, aufgestellteEinheit)
    stelleDavor = aufstellung.stelle(modell)
    spielerDerAblage = zweiterSpieler if ablage == "eigeneAblage" else ersterSpieler

    gründe = sperrgründe(aufstellung.modellAufAblageLoslassen, modell, spielerDerAblage)

    assert gründe == {Grund.nichtWählbar}
    assert aufstellung.stelle(modell) == stelleDavor
