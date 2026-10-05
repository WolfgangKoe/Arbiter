"""AUF-4 · Anzeige der Aufstellung."""

from dataclasses import dataclass

import pytest

from arbiter.domaene.phasen.aufstellen import Aufstellung, Aufstellungszone, grenzenInXDerZone
from arbiter.domaene.spielobjekte import Spieler


@dataclass(frozen=True)
class Gewinnerwahl:
    gewinner: Spieler
    nameDesGewinners: str
    nameDesAnderen: str


@pytest.fixture(
    params=[("Spieler 1", "Spieler 2"), ("Spieler 2", "Spieler 1")],
    ids=["spielerEinsGewinnt", "spielerZweiGewinnt"],
)
def gewinnerwahl(request, spielerEins, spielerZwei) -> Gewinnerwahl:
    nameDesGewinners, nameDesAnderen = request.param
    gewinner = spielerEins if nameDesGewinners == "Spieler 1" else spielerZwei
    return Gewinnerwahl(gewinner, nameDesGewinners, nameDesAnderen)


@pytest.fixture(params=list(Aufstellungszone), ids=["ersteZone", "zweiteZone"])
def zoneDesGewinners(request) -> Aufstellungszone:
    return request.param


@pytest.fixture
def gewählteAufstellung(ausgangsaufstellung, gewinnerwahl, zoneDesGewinners):
    ausgangsaufstellung.gewinnerWählen(gewinnerwahl.gewinner)
    ausgangsaufstellung.aufstellungszoneWählen(zoneDesGewinners)
    return ausgangsaufstellung


@pytest.fixture(params=["ausgangslage", "nachDerGewinnerwahl", "nachDerAufstellung"])
def aufstellungOhneJemandAnDerReihe(
    request, ausgangsaufstellung, spielerEins, spielerZwei, einheitenAufstellen
):
    if request.param != "ausgangslage":
        ausgangsaufstellung.gewinnerWählen(spielerEins)
    if request.param == "nachDerAufstellung":
        ausgangsaufstellung.aufstellungszoneWählen(Aufstellungszone.zweite)
        alleEinheiten = len(spielerEins.armee.einheiten) + len(spielerZwei.armee.einheiten)
        einheitenAufstellen(ausgangsaufstellung, alleEinheiten)
    return ausgangsaufstellung


@pytest.fixture(params=["nachDerZonenwahl", "nachDemBeenden"])
def aufstellungOhneEinheitInAufstellung(request, aufstellungNachDerZonenwahl, einheitenAufstellen):
    if request.param == "nachDemBeenden":
        einheitenAufstellen(aufstellungNachDerZonenwahl, 1)
    return aufstellungNachDerZonenwahl


def testAuf4_2DieAblageDesSpielersDerErstenArmeeHeißtSpieler1(bildschirm, ausgangsaufstellung):
    seite = bildschirm.seiteZu(ausgangsaufstellung)

    ablage = bildschirm.ablageVon(seite, "Spieler 1")

    assert ablage.count() == 1
    assert ablage.locator(".einheitenKarte", has_text="Boyz").count() == 1
    assert ablage.locator(".einheitenKarte", has_text="Warboss").count() == 1


def testAuf4_2DieAblageDesSpielersDerZweitenArmeeHeißtSpieler2(bildschirm, ausgangsaufstellung):
    seite = bildschirm.seiteZu(ausgangsaufstellung)

    ablage = bildschirm.ablageVon(seite, "Spieler 2")

    assert ablage.count() == 1
    assert ablage.locator(".einheitenKarte", has_text="Necron Warriors").count() == 1
    assert ablage.locator(".einheitenKarte", has_text="Overlord").count() == 1


@pytest.mark.parametrize(
    ("spielername", "modelleJeEinheit"),
    [
        ("Spieler 1", {"Boyz": "10", "Warboss": "1"}),
        ("Spieler 2", {"Necron Warriors": "10", "Overlord": "1"}),
    ],
    ids=["ablageVonSpielerEins", "ablageVonSpielerZwei"],
)
def testAuf4_3DieAblageZeigtJedeEinheitMitDerAnzahlIhrerNichtGesetztenModelle(
    bildschirm, ausgangsaufstellung, spielername, modelleJeEinheit
):
    seite = bildschirm.seiteZu(ausgangsaufstellung)

    ablage = bildschirm.ablageVon(seite, spielername)

    karten = ablage.locator(".einheitenKarte")
    anzahlen = {
        name: karten.filter(has_text=name).locator(".einheitenKartenModelle").text_content()
        for name in modelleJeEinheit
    }
    assert karten.count() == len(modelleJeEinheit)
    assert anzahlen == modelleJeEinheit


@pytest.mark.parametrize(
    ("gesetzt", "nichtGesetzt"), [(3, "7"), (9, "1")], ids=["dreiGesetzt", "neunGesetzt"]
)
def testAuf4_3DieAblageZähltNurDieNichtGesetztenModelleDerEinheit(
    bildschirm, aufstellungNachDerZonenwahl, boyzSetzen, gesetzt, nichtGesetzt
):
    boyzSetzen(gesetzt)

    seite = bildschirm.seiteZu(aufstellungNachDerZonenwahl)

    karte = bildschirm.ablageVon(seite, "Spieler 1").locator(".einheitenKarte", has_text="Boyz")
    assert karte.locator(".einheitenKartenModelle").text_content() == nichtGesetzt


def testAuf4_3SindAlleModelleGesetztZeigtDieAblageDieEinheitOhneAnzahl(
    bildschirm, aufstellungNachDerZonenwahl, boyzSetzen
):
    boyzSetzen(10)

    seite = bildschirm.seiteZu(aufstellungNachDerZonenwahl)

    karte = bildschirm.ablageVon(seite, "Spieler 1").locator(".einheitenKarte", has_text="Boyz")
    assert karte.count() == 1
    assert karte.locator(".einheitenKartenModelle").count() == 0


def testAuf4_3DieAblageZeigtKeineAufgestellteEinheit(
    bildschirm, aufstellungNachDerZonenwahl, spielerZwei, einheitenAufstellen
):
    einheitenAufstellen(aufstellungNachDerZonenwahl, 1)

    seite = bildschirm.seiteZu(aufstellungNachDerZonenwahl)

    ablageEins = bildschirm.ablageVon(seite, "Spieler 1")
    ablageZwei = bildschirm.ablageVon(seite, "Spieler 2")
    assert ablageEins.locator(".einheitenKarte").count() == 1
    assert ablageEins.locator(".einheitenKarte", has_text="Warboss").count() == 1
    assert ablageZwei.locator(".einheitenKarte").count() == len(spielerZwei.armee.einheiten)


def testAuf4_4SolangeKeinerAnDerReiheIstZeigtArbiterKeinen(
    bildschirm, aufstellungOhneJemandAnDerReihe
):
    seite = bildschirm.seiteZu(aufstellungOhneJemandAnDerReihe)

    kopfzeilen = bildschirm.elementeDerSeite(seite, ".kopfzeileSpieler")
    texte = " ".join(kopfzeile.text for kopfzeile in kopfzeilen)
    assert "Spieler 1" in texte
    assert "Spieler 2" in texte
    assert seite.locator(".kopfzeileAnDerReihe").count() == 0


def testAuf4_4ArbiterZeigtDenSpielerAnDerReihe(bildschirm, ausgangsaufstellung, gewinnerwahl):
    ausgangsaufstellung.gewinnerWählen(gewinnerwahl.gewinner)
    ausgangsaufstellung.aufstellungszoneWählen(Aufstellungszone.erste)

    seite = bildschirm.seiteZu(ausgangsaufstellung)

    markierte = seite.locator(".kopfzeileSpieler").filter(has=seite.locator(".kopfzeileAnDerReihe"))
    assert markierte.count() == 1
    assert gewinnerwahl.nameDesAnderen in markierte.text_content()
    assert seite.locator(".kopfzeileAnDerReihe").text_content() == "an der Reihe"


def testAuf4_4NachAufstellenDerEinheitZeigtArbiterDenAnderenSpielerAnDerReihe(
    bildschirm, ausgangsaufstellung, gewinnerwahl, einheitenAufstellen
):
    ausgangsaufstellung.gewinnerWählen(gewinnerwahl.gewinner)
    ausgangsaufstellung.aufstellungszoneWählen(Aufstellungszone.erste)
    einheitenAufstellen(ausgangsaufstellung, 1)

    seite = bildschirm.seiteZu(ausgangsaufstellung)

    markierte = seite.locator(".kopfzeileSpieler").filter(has=seite.locator(".kopfzeileAnDerReihe"))
    assert markierte.count() == 1
    assert gewinnerwahl.nameDesGewinners in markierte.text_content()


@pytest.mark.parametrize("gesetzt", [0, 3, 10], ids=["keinGesetzt", "dreiGesetzt", "alleGesetzt"])
def testAuf4_5DieEinheitInAufstellungIstInDerAblageGekennzeichnet(
    bildschirm, aufstellungNachDerZonenwahl, boyz, modelleSetzen, gesetzt
):
    modelleSetzen(aufstellungNachDerZonenwahl, boyz, gesetzt)

    seite = bildschirm.seiteZu(aufstellungNachDerZonenwahl)

    ablage = bildschirm.ablageVon(seite, "Spieler 1")
    abzeichen = seite.locator(".einheitenKartenAbzeichen")
    assert abzeichen.count() == 1
    assert abzeichen.text_content() == "in Aufstellung"
    assert (
        ablage.locator(".einheitenKarte", has_text="Boyz")
        .locator(".einheitenKartenAbzeichen")
        .count()
        == 1
    )


def testAuf4_5DieEinheitInAufstellungDesZweitenSpielersIstInSeinerAblageGekennzeichnet(
    bildschirm, aufstellungNachDerZonenwahl, necronWarriors, einheitenAufstellen, modelleSetzen
):
    einheitenAufstellen(aufstellungNachDerZonenwahl, 1)
    modelleSetzen(aufstellungNachDerZonenwahl, necronWarriors, 0)

    seite = bildschirm.seiteZu(aufstellungNachDerZonenwahl)

    ablageEins = bildschirm.ablageVon(seite, "Spieler 1")
    ablageZwei = bildschirm.ablageVon(seite, "Spieler 2")
    assert ablageEins.locator(".einheitenKartenAbzeichen").count() == 0
    assert ablageZwei.locator(".einheitenKartenAbzeichen").count() == 1
    assert (
        ablageZwei.locator(".einheitenKarte", has_text="Necron Warriors")
        .locator(".einheitenKartenAbzeichen")
        .count()
        == 1
    )


def testAuf4_5MitDerWahlEinerAnderenEinheitWandertDieKennzeichnung(
    bildschirm, aufstellungNachDerZonenwahl, boyz, warboss, modelleSetzen
):
    modelleSetzen(aufstellungNachDerZonenwahl, boyz, 0)
    modelleSetzen(aufstellungNachDerZonenwahl, warboss, 0)

    seite = bildschirm.seiteZu(aufstellungNachDerZonenwahl)

    ablage = bildschirm.ablageVon(seite, "Spieler 1")
    abzeichen = ablage.locator(".einheitenKartenAbzeichen")
    assert abzeichen.count() == 1
    assert (
        ablage.locator(".einheitenKarte", has_text="Warboss")
        .locator(".einheitenKartenAbzeichen")
        .count()
        == 1
    )


def testAuf4_5OhneEinheitInAufstellungKennzeichnetDieAblageKeine(
    bildschirm, aufstellungOhneEinheitInAufstellung
):
    seite = bildschirm.seiteZu(aufstellungOhneEinheitInAufstellung)

    assert seite.locator(".einheitenKarte").count() > 0
    assert seite.locator(".einheitenKartenAbzeichen").count() == 0


def testAuf4_6NachDerWahlZeigtDieKarteJedeZoneInDerFarbeDerModelleIhresSpielers(
    bildschirm, gewählteAufstellung, ausgangslage, einheitenAufstellen
):
    breite, _ = ausgangslage.spielfeld.seitenlängen
    einheitenAufstellen(gewählteAufstellung, 2)

    seite = bildschirm.seiteZu(gewählteAufstellung)

    zonen = bildschirm.elementeDerSeite(seite, ".karte .aufstellungszone")
    farbeJeZone = {zone.zahl("x"): zone.fill for zone in zonen}
    for spieler in (ausgangslage.ersterSpieler, ausgangslage.zweiterSpieler):
        zone = gewählteAufstellung.aufstellungszone(spieler)
        zoneBeginnt, _ = grenzenInXDerZone(zone, breite, ausgangslage.tiefen[zone])
        (farbeDerModelle,) = bildschirm.modellfarben(seite, gewählteAufstellung, spieler)
        assert farbeJeZone[float(zoneBeginnt)] == farbeDerModelle


@pytest.mark.parametrize(
    "gewinnerGewählt", [False, True], ids=["ausgangslage", "nachDerGewinnerwahl"]
)
def testAuf4_6VorDerWahlZeigtDieKarteKeineZoneInDerFarbeEinesSpielers(
    bildschirm, ausgangslage, aufstellungMitModellenBeiderSpieler, gewinnerGewählt
):
    spielerEins, spielerZwei = ausgangslage.ersterSpieler, ausgangslage.zweiterSpieler
    vorDerWahl = Aufstellung(ausgangslage)
    if gewinnerGewählt:
        vorDerWahl.gewinnerWählen(spielerEins)
    seiteMitModellen = bildschirm.seiteZu(aufstellungMitModellenBeiderSpieler)
    farbenDerModelle = bildschirm.modellfarben(
        seiteMitModellen, aufstellungMitModellenBeiderSpieler, spielerEins
    ) | bildschirm.modellfarben(seiteMitModellen, aufstellungMitModellenBeiderSpieler, spielerZwei)

    seite = bildschirm.seiteZu(vorDerWahl)

    zonen = bildschirm.elementeDerSeite(seite, ".karte .aufstellungszone")
    farbenDerZonen = {zone.fill for zone in zonen}
    assert len(zonen) == len(Aufstellungszone)
    assert farbenDerZonen.isdisjoint(farbenDerModelle)


def testAuf4_7DieAblageNenntIhrenSpielerInDerFarbeSeinerModelle(
    bildschirm, aufstellungMitModellenBeiderSpieler, spielerEins, spielerZwei
):
    seite = bildschirm.seiteZu(aufstellungMitModellenBeiderSpieler)

    namen = bildschirm.elementeDerSeite(seite, ".armeeKartenName")

    farbeJeName = {name.text: {name.farbe} for name in namen}
    farbenEins = bildschirm.modellfarben(seite, aufstellungMitModellenBeiderSpieler, spielerEins)
    farbenZwei = bildschirm.modellfarben(seite, aufstellungMitModellenBeiderSpieler, spielerZwei)
    assert farbeJeName == {"Spieler 1": farbenEins, "Spieler 2": farbenZwei}


def testAuf4_3HatEinSpielerAlleEinheitenAufgestelltBleibtSeineAblageLeerUndNenntIhn(
    bildschirm, aufstellungNachDerZonenwahl, spielerEins, spielerZwei, einheitenAufstellen
):
    alleEinheiten = len(spielerEins.armee.einheiten) + len(spielerZwei.armee.einheiten)
    einheitenAufstellen(aufstellungNachDerZonenwahl, alleEinheiten)

    seite = bildschirm.seiteZu(aufstellungNachDerZonenwahl)

    for spielername in ("Spieler 1", "Spieler 2"):
        ablage = bildschirm.ablageVon(seite, spielername)
        assert ablage.count() == 1
        assert ablage.locator(".einheitenKarte").count() == 0
