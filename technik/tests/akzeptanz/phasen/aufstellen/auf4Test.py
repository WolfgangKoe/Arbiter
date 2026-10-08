"""AUF-4 · Anzeige der Aufstellung."""

from dataclasses import dataclass

import pytest

from arbiter.domaene.phasen.aufstellen import Aufstellung, Aufstellungszone
from arbiter.domaene.spielobjekte import Spieler
from tests.akzeptanz.bildschirm import ablageVon, elementeDerSeite, modellfarben
from tests.akzeptanz.handgriffe import alleEinheitenAufstellen, einheitenAufstellen, modelleSetzen


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


@pytest.fixture(params=["ausgangslage", "nachDerGewinnerwahl"])
def aufstellungVorDerZonenwahl(request, ausgangslage, spielerEins) -> Aufstellung:
    aufstellung = Aufstellung(ausgangslage)
    if request.param == "nachDerGewinnerwahl":
        aufstellung.gewinnerWählen(spielerEins)
    return aufstellung


@pytest.fixture
def aufstellungNachDerAufstellung(aufstellungNachDerZonenwahl) -> Aufstellung:
    alleEinheitenAufstellen(aufstellungNachDerZonenwahl)
    return aufstellungNachDerZonenwahl


@pytest.fixture(params=["nachDerZonenwahl", "nachDemBeenden"])
def aufstellungOhneEinheitInAufstellung(request, aufstellungNachDerZonenwahl):
    if request.param == "nachDemBeenden":
        einheitenAufstellen(aufstellungNachDerZonenwahl, 1)
    return aufstellungNachDerZonenwahl


def testAuf4_2DieAblageDesSpielersDerErstenArmeeHeißtSpieler1(bildschirm, ausgangsaufstellung):
    seite = bildschirm.seiteZu(ausgangsaufstellung)

    ablage = ablageVon(seite, "Spieler 1")

    assert ablage.count() == 1
    assert ablage.locator(".einheitenKarte", has_text="Boyz").count() == 1
    assert ablage.locator(".einheitenKarte", has_text="Warboss").count() == 1


def testAuf4_2DieAblageDesSpielersDerZweitenArmeeHeißtSpieler2(bildschirm, ausgangsaufstellung):
    seite = bildschirm.seiteZu(ausgangsaufstellung)

    ablage = ablageVon(seite, "Spieler 2")

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

    ablage = ablageVon(seite, spielername)

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

    karte = ablageVon(seite, "Spieler 1").locator(".einheitenKarte", has_text="Boyz")
    assert karte.locator(".einheitenKartenModelle").text_content() == nichtGesetzt


def testAuf4_3SindAlleModelleGesetztZeigtDieAblageDieEinheitOhneAnzahl(
    bildschirm, aufstellungNachDerZonenwahl, boyzSetzen
):
    boyzSetzen(10)

    seite = bildschirm.seiteZu(aufstellungNachDerZonenwahl)

    karte = ablageVon(seite, "Spieler 1").locator(".einheitenKarte", has_text="Boyz")
    assert karte.count() == 1
    assert karte.locator(".einheitenKartenModelle").count() == 0


def testAuf4_3DieAblageZeigtKeineAufgestellteEinheit(
    bildschirm, aufstellungNachDerZonenwahl, spielerZwei
):
    einheitenAufstellen(aufstellungNachDerZonenwahl, 1)

    seite = bildschirm.seiteZu(aufstellungNachDerZonenwahl)

    ablageEins = ablageVon(seite, "Spieler 1")
    ablageZwei = ablageVon(seite, "Spieler 2")
    assert ablageEins.locator(".einheitenKarte").count() == 1
    assert ablageEins.locator(".einheitenKarte", has_text="Warboss").count() == 1
    assert ablageZwei.locator(".einheitenKarte").count() == len(spielerZwei.armee.einheiten)


def testAuf4_3HatEinSpielerAlleEinheitenAufgestelltBleibtSeineAblageLeerUndNenntIhn(
    bildschirm, aufstellungNachDerZonenwahl
):
    alleEinheitenAufstellen(aufstellungNachDerZonenwahl)

    seite = bildschirm.seiteZu(aufstellungNachDerZonenwahl)

    for spielername in ("Spieler 1", "Spieler 2"):
        ablage = ablageVon(seite, spielername)
        assert ablage.count() == 1
        assert ablage.locator(".einheitenKarte").count() == 0


def kopfzeilenTexte(seite) -> str:
    kopfzeilen = elementeDerSeite(seite, ".kopfzeileSpieler")
    return " ".join(kopfzeile.text for kopfzeile in kopfzeilen)


def testAuf4_4VorDerZonenwahlZeigtArbiterKeinenAnDerReihe(bildschirm, aufstellungVorDerZonenwahl):
    seite = bildschirm.seiteZu(aufstellungVorDerZonenwahl)

    texte = kopfzeilenTexte(seite)

    assert "Spieler 1" in texte
    assert "Spieler 2" in texte
    assert seite.locator(".kopfzeileAnDerReihe").count() == 0


def testAuf4_4NachDerAufstellungZeigtArbiterKeinenAnDerReihe(
    bildschirm, aufstellungNachDerAufstellung
):
    seite = bildschirm.seiteZu(aufstellungNachDerAufstellung)

    texte = kopfzeilenTexte(seite)

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
    bildschirm, ausgangsaufstellung, gewinnerwahl
):
    ausgangsaufstellung.gewinnerWählen(gewinnerwahl.gewinner)
    ausgangsaufstellung.aufstellungszoneWählen(Aufstellungszone.erste)
    einheitenAufstellen(ausgangsaufstellung, 1)

    seite = bildschirm.seiteZu(ausgangsaufstellung)

    markierte = seite.locator(".kopfzeileSpieler").filter(has=seite.locator(".kopfzeileAnDerReihe"))
    assert markierte.count() == 1
    assert gewinnerwahl.nameDesGewinners in markierte.text_content()


@pytest.mark.parametrize("gesetzt", [1, 3, 10], ids=["einGesetzt", "dreiGesetzt", "alleGesetzt"])
def testAuf4_5DieEinheitInAufstellungIstInDerAblageGekennzeichnet(
    bildschirm, aufstellungNachDerZonenwahl, boyz, gesetzt
):
    modelleSetzen(aufstellungNachDerZonenwahl, boyz, gesetzt)

    seite = bildschirm.seiteZu(aufstellungNachDerZonenwahl)

    ablage = ablageVon(seite, "Spieler 1")
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
    bildschirm, aufstellungNachDerZonenwahl, necronWarriors
):
    einheitenAufstellen(aufstellungNachDerZonenwahl, 1)
    modelleSetzen(aufstellungNachDerZonenwahl, necronWarriors, 1)

    seite = bildschirm.seiteZu(aufstellungNachDerZonenwahl)

    ablageEins = ablageVon(seite, "Spieler 1")
    ablageZwei = ablageVon(seite, "Spieler 2")
    assert ablageEins.locator(".einheitenKartenAbzeichen").count() == 0
    assert ablageZwei.locator(".einheitenKartenAbzeichen").count() == 1
    assert (
        ablageZwei.locator(".einheitenKarte", has_text="Necron Warriors")
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
    bildschirm, gewählteAufstellung, ausgangslage
):
    einheitenAufstellen(gewählteAufstellung, 2)

    seite = bildschirm.seiteZu(gewählteAufstellung)

    zonen = elementeDerSeite(seite, ".karte .aufstellungszone")
    farbeJeZone = {zone.zahl("x"): zone.fill for zone in zonen}
    for spieler in (ausgangslage.ersterSpieler, ausgangslage.zweiterSpieler):
        zone = gewählteAufstellung.aufstellungszone(spieler)
        (zoneBeginnt, _), _ = ausgangslage.grenzenDerZone(zone)
        (farbeDerModelle,) = modellfarben(seite, gewählteAufstellung, spieler)
        assert farbeJeZone[float(zoneBeginnt)] == farbeDerModelle


def testAuf4_6VorDerWahlZeigtDieKarteKeineZoneInDerFarbeEinesSpielers(
    bildschirm,
    aufstellungVorDerZonenwahl,
    aufstellungMitModellenBeiderSpieler,
    spielerEins,
    spielerZwei,
):
    seiteMitModellen = bildschirm.seiteZu(aufstellungMitModellenBeiderSpieler)
    farbenDerModelle = modellfarben(
        seiteMitModellen, aufstellungMitModellenBeiderSpieler, spielerEins
    ) | modellfarben(seiteMitModellen, aufstellungMitModellenBeiderSpieler, spielerZwei)

    seite = bildschirm.seiteZu(aufstellungVorDerZonenwahl)

    zonen = elementeDerSeite(seite, ".karte .aufstellungszone")
    farbenDerZonen = {zone.fill for zone in zonen}
    assert len(zonen) == len(Aufstellungszone)
    assert farbenDerZonen.isdisjoint(farbenDerModelle)


def testAuf4_7DieAblageNenntIhrenSpielerInDerFarbeSeinerModelle(
    bildschirm, aufstellungMitModellenBeiderSpieler, spielerEins, spielerZwei
):
    seite = bildschirm.seiteZu(aufstellungMitModellenBeiderSpieler)

    namen = elementeDerSeite(seite, ".armeeKartenName")

    farbeJeName = {name.text: {name.farbe} for name in namen}
    farbenEins = modellfarben(seite, aufstellungMitModellenBeiderSpieler, spielerEins)
    farbenZwei = modellfarben(seite, aufstellungMitModellenBeiderSpieler, spielerZwei)
    assert farbeJeName == {"Spieler 1": farbenEins, "Spieler 2": farbenZwei}
