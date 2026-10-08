"""QUE-2 · Karte."""

from urllib.parse import urlparse

import pytest

from arbiter.domaene.phasen.aufstellen import Aufstellungszone
from tests.akzeptanz.bildschirm import elementeDerSeite, modellfarben
from tests.akzeptanz.handgriffe import einheitenAufstellen, radiusInZoll

_anzahlGesetzterModelle = 3
# Warum: getBoundingClientRect misst Bruchteile von Pixeln; QUE-2.2 bis QUE-2.4 prüfen Zoll exakt
_pixelgenauigkeit = 1e-4


@pytest.fixture(params=[(1400, 500), (500, 1400)], ids=["breitesFenster", "hohesFenster"])
def fenster(request) -> dict[str, int]:
    breite, höhe = request.param
    return {"width": breite, "height": höhe}


def testQue2_1DerBefehlNenntInDerErstenZeileEineAdresseNurFürDasEigeneGerät(adresseDesBefehls):
    # Warum: Zwei Spieler an einem Gerät, darum nur 127.0.0.1 (Architektur, W5)
    adresse = urlparse(adresseDesBefehls)

    assert (adresse.scheme, adresse.hostname) == ("http", "127.0.0.1")
    assert adresse.port is not None


def testQue2_1UnterDerAdresseÖffnetDerBrowserDieKarteMitDemSpielfeld(adresseDesBefehls, bildschirm):
    seite = bildschirm.seiteBei(adresseDesBefehls)

    assert seite.locator(".karte .spielfeld").count() == 1


def testQue2_2DieKarteZeigtDasSpielfeldAlsRechteckMitDenSeitenlängenDerAusgangslage(
    bildschirm, ausgangsaufstellung, ausgangslage
):
    breite, länge = ausgangslage.spielfeld.seitenlängen

    seite = bildschirm.seiteZu(ausgangsaufstellung)

    (spielfeld,) = elementeDerSeite(seite, ".karte .spielfeld")
    assert spielfeld.art == "rect"
    assert spielfeld.zahl("x") == 0
    assert spielfeld.zahl("y") == 0
    assert spielfeld.zahl("width") == float(breite)
    assert spielfeld.zahl("height") == float(länge)


def testQue2_3DieKarteZeigtJedeAufstellungszoneAlsFlächeAnIhrerSpielfeldkante(
    bildschirm, ausgangsaufstellung, ausgangslage
):
    breite, länge = ausgangslage.spielfeld.seitenlängen
    tiefeErste = ausgangslage.tiefen[Aufstellungszone.erste]
    tiefeZweite = ausgangslage.tiefen[Aufstellungszone.zweite]

    seite = bildschirm.seiteZu(ausgangsaufstellung)

    zonen = elementeDerSeite(seite, ".karte .aufstellungszone")
    gezeigt = sorted(
        (zone.zahl("x"), zone.zahl("y"), zone.zahl("width"), zone.zahl("height")) for zone in zonen
    )
    assert gezeigt == [
        (0, 0, float(tiefeErste), float(länge)),
        (float(breite - tiefeZweite), 0, float(tiefeZweite), float(länge)),
    ]


def testQue2_4OhneGesetztesModellZeigtDieKarteKeinenKreis(bildschirm, ausgangsaufstellung):
    seite = bildschirm.seiteZu(ausgangsaufstellung)

    assert elementeDerSeite(seite, ".karte .modell") == ()


def testQue2_4DieKarteZeigtJedesGesetzteModellAlsKreisMitDurchmesserSeinerBaseAnSeinerStelle(
    bildschirm, aufstellungMitModellenBeiderSpieler, ausgangslage
):
    einheitenAufstellen(aufstellungMitModellenBeiderSpieler, 1)
    aufstellung = aufstellungMitModellenBeiderSpieler
    gesetzte = [
        modell
        for modell in ausgangslage.ersterSpieler.armee.modelle
        | ausgangslage.zweiterSpieler.armee.modelle
        if aufstellung.gesetzt(modell)
    ]
    erwartet = sorted(
        (
            float(aufstellung.stelle(modell).x),
            float(aufstellung.stelle(modell).y),
            float(radiusInZoll(modell)),
        )
        for modell in gesetzte
    )

    seite = bildschirm.seiteZu(aufstellung)

    kreise = elementeDerSeite(seite, ".karte .modell")
    gezeigt = sorted((kreis.zahl("cx"), kreis.zahl("cy"), kreis.zahl("r")) for kreis in kreise)
    assert len(gezeigt) == len(gesetzte)
    assert gezeigt == erwartet


def testQue2_4DieKarteZeigtKeinNichtGesetztesModell(
    bildschirm, aufstellungNachDerZonenwahl, boyzSetzen
):
    gesetzte = boyzSetzen(_anzahlGesetzterModelle)
    erwartet = sorted(
        (float(stelle.x), float(stelle.y), float(radiusInZoll(modell)))
        for modell, stelle in gesetzte
    )

    seite = bildschirm.seiteZu(aufstellungNachDerZonenwahl)

    kreise = elementeDerSeite(seite, ".karte .modell")
    gezeigt = sorted((kreis.zahl("cx"), kreis.zahl("cy"), kreis.zahl("r")) for kreis in kreise)
    assert gezeigt == erwartet
    assert len(gezeigt) == _anzahlGesetzterModelle


def testQue2_5EinZollIstInBeidenAchsenDerKarteGleichLang(bildschirm, ausgangsaufstellung, fenster):
    seite = bildschirm.seiteZu(ausgangsaufstellung)

    seite.set_viewport_size(fenster)

    matrix = seite.locator(".karte").evaluate(
        "karte => { const m = karte.getScreenCTM(); return {a: m.a, b: m.b, c: m.c, d: m.d} }"
    )
    assert matrix["a"] == matrix["d"]
    assert matrix["b"] == 0
    assert matrix["c"] == 0


def testQue2_5DieSeitenlängenDesSpielfeldsHabenAufDerKarteDenselbenMaßstab(
    bildschirm, ausgangsaufstellung, ausgangslage, fenster
):
    breite, länge = ausgangslage.spielfeld.seitenlängen
    seite = bildschirm.seiteZu(ausgangsaufstellung)

    seite.set_viewport_size(fenster)

    (spielfeld,) = elementeDerSeite(seite, ".karte .spielfeld")
    pixelJeZoll = spielfeld.breiteInPixeln / float(breite)
    assert spielfeld.höheInPixeln / float(länge) == pytest.approx(
        pixelJeZoll, rel=_pixelgenauigkeit
    )


def testQue2_5DieTiefeDerAufstellungszonenHatAufDerKarteDenselbenMaßstab(
    bildschirm, ausgangsaufstellung, ausgangslage, fenster
):
    breite, _ = ausgangslage.spielfeld.seitenlängen
    tiefe = ausgangslage.tiefen[Aufstellungszone.erste]
    seite = bildschirm.seiteZu(ausgangsaufstellung)

    seite.set_viewport_size(fenster)

    (spielfeld,) = elementeDerSeite(seite, ".karte .spielfeld")
    zonen = elementeDerSeite(seite, ".karte .aufstellungszone")
    zone = next(zone for zone in zonen if zone.zahl("x") == 0)
    pixelJeZoll = spielfeld.breiteInPixeln / float(breite)
    assert zone.breiteInPixeln / float(tiefe) == pytest.approx(pixelJeZoll, rel=_pixelgenauigkeit)


def testQue2_5DerDurchmesserDerBaseHatAufDerKarteDenselbenMaßstab(
    bildschirm, einGesetztesModell, ausgangslage, fenster
):
    aufstellung, modell = einGesetztesModell
    breite, _ = ausgangslage.spielfeld.seitenlängen
    seite = bildschirm.seiteZu(aufstellung)

    seite.set_viewport_size(fenster)

    (spielfeld,) = elementeDerSeite(seite, ".karte .spielfeld")
    (kreis,) = elementeDerSeite(seite, ".karte .modell")
    pixelJeZoll = spielfeld.breiteInPixeln / float(breite)
    durchmesser = float(2 * radiusInZoll(modell))
    assert kreis.breiteInPixeln / durchmesser == pytest.approx(pixelJeZoll, rel=_pixelgenauigkeit)


def testQue2_6DieModelleEinesSpielersHabenAufDerKarteEineFarbe(
    bildschirm, aufstellungMitModellenBeiderSpieler, spielerEins, spielerZwei
):
    seite = bildschirm.seiteZu(aufstellungMitModellenBeiderSpieler)

    farbenEins = modellfarben(seite, aufstellungMitModellenBeiderSpieler, spielerEins)
    farbenZwei = modellfarben(seite, aufstellungMitModellenBeiderSpieler, spielerZwei)

    assert len(farbenEins) == 1
    assert len(farbenZwei) == 1


def testQue2_6DieModelleDerZweiSpielerHabenAufDerKarteVerschiedeneFarben(
    bildschirm, aufstellungMitModellenBeiderSpieler, spielerEins, spielerZwei
):
    seite = bildschirm.seiteZu(aufstellungMitModellenBeiderSpieler)

    farbenEins = modellfarben(seite, aufstellungMitModellenBeiderSpieler, spielerEins)
    farbenZwei = modellfarben(seite, aufstellungMitModellenBeiderSpieler, spielerZwei)

    assert farbenEins.isdisjoint(farbenZwei)
