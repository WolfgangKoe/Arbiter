"""QUE-6 · Leisten."""

import pytest
from playwright.sync_api import Locator, Page, expect

from tests.akzeptanz.bildschirm import griffVon, leisteVon
from tests.akzeptanz.schlacht import boyÜberDenWarbossÜbergehen


def linksDerKarte(leiste: dict, karte: dict) -> bool:
    return leiste["x"] + leiste["width"] <= karte["x"]


def rechtsDerKarte(leiste: dict, karte: dict) -> bool:
    return leiste["x"] >= karte["x"] + karte["width"]


def unterDerKarte(leiste: dict, karte: dict) -> bool:
    return leiste["y"] >= karte["y"] + karte["height"]


lageJeLeiste = pytest.mark.parametrize(
    ("leistenname", "lage"),
    [
        ("Armeeliste Spieler 1", linksDerKarte),
        ("Armeeliste Spieler 2", rechtsDerKarte),
        ("Protokoll", unterDerKarte),
    ],
    ids=["links", "rechts", "unten"],
)

inhaltJeLeiste = {
    "Armeeliste Spieler 1": (".armeeKarte", "Spieler 1"),
    "Armeeliste Spieler 2": (".armeeKarte", "Spieler 2"),
    "Protokoll": (".protokollEintrag", "Boyz"),
}

jedeLeiste = pytest.mark.parametrize(
    "leistenname", list(inhaltJeLeiste), ids=["links", "rechts", "unten"]
)


def inhaltVon(seite: Page, leistenname: str) -> Locator:
    klasse, text = inhaltJeLeiste[leistenname]
    return leisteVon(seite, leistenname).locator(klasse, has_text=text)


def istEingefahren(seite: Page, leistenname: str) -> None:
    expect(griffVon(seite, leistenname)).to_have_attribute("aria-expanded", "false")
    expect(griffVon(seite, leistenname)).to_be_visible()
    expect(inhaltVon(seite, leistenname)).to_be_hidden()


def istNichtEingefahren(seite: Page, leistenname: str) -> None:
    expect(griffVon(seite, leistenname)).to_have_attribute("aria-expanded", "true")
    expect(inhaltVon(seite, leistenname)).to_be_visible()


@pytest.fixture
def seiteMitProtokoll(bildschirm, beendeteAufstellung, schlachtInDerBewegungsphase, boyz) -> Page:
    boyÜberDenWarbossÜbergehen(schlachtInDerBewegungsphase, boyz)
    return bildschirm.seiteZuSchlacht(beendeteAufstellung, schlachtInDerBewegungsphase)


@pytest.fixture
def seiteZumTippen(bildschirm, beendeteAufstellung, schlachtInDerBewegungsphase, boyz) -> Page:
    boyÜberDenWarbossÜbergehen(schlachtInDerBewegungsphase, boyz)
    return bildschirm.seiteZuSchlacht(
        beendeteAufstellung, schlachtInDerBewegungsphase, berührbar=True
    )


@lageJeLeiste
def testQue6_1JedeLeisteStehtAnIhrerSeiteDerKarte(
    bildschirm, aufstellungNachDerZonenwahl, leistenname, lage
):
    seite = bildschirm.seiteZu(aufstellungNachDerZonenwahl)

    leiste = leisteVon(seite, leistenname).bounding_box()
    karte = seite.locator("svg.karte").bounding_box()

    assert lage(leiste, karte)


@jedeLeiste
def testQue6_1JedeLeisteZeigtIhrenInhalt(seiteMitProtokoll, leistenname):
    klasse, text = inhaltJeLeiste[leistenname]

    inhalt = leisteVon(seiteMitProtokoll, leistenname).locator(klasse)

    expect(inhalt).to_have_count(1)
    expect(inhalt).to_contain_text(text)


@jedeLeiste
def testQue6_2NachDemStartIstKeineLeisteEingefahren(adresseDesBefehls, bildschirm, leistenname):
    seite = bildschirm.seiteBei(adresseDesBefehls)

    griff = griffVon(seite, leistenname)

    expect(leisteVon(seite, leistenname)).to_be_visible()
    expect(griff).to_have_attribute("aria-expanded", "true")


@jedeLeiste
def testQue6_3EinKlickAufDenGriffEinerAusgefahrenenLeisteFährtSieEin(
    seiteMitProtokoll, leistenname
):
    istNichtEingefahren(seiteMitProtokoll, leistenname)

    griffVon(seiteMitProtokoll, leistenname).click()

    istEingefahren(seiteMitProtokoll, leistenname)


@jedeLeiste
def testQue6_4EinKlickAufDenGriffEinerEingefahrenenLeisteFährtSieAus(
    seiteMitProtokoll, leistenname
):
    griffVon(seiteMitProtokoll, leistenname).click()
    istEingefahren(seiteMitProtokoll, leistenname)

    griffVon(seiteMitProtokoll, leistenname).click()

    istNichtEingefahren(seiteMitProtokoll, leistenname)


@jedeLeiste
def testQue6_5EinTippenAufDenGriffFährtDieLeisteEinWieEinKlick(seiteZumTippen, leistenname):
    istNichtEingefahren(seiteZumTippen, leistenname)

    griffVon(seiteZumTippen, leistenname).tap()

    istEingefahren(seiteZumTippen, leistenname)


@jedeLeiste
def testQue6_5EinTippenAufDenGriffFährtDieLeisteAusWieEinKlick(seiteZumTippen, leistenname):
    griffVon(seiteZumTippen, leistenname).tap()
    istEingefahren(seiteZumTippen, leistenname)

    griffVon(seiteZumTippen, leistenname).tap()

    istNichtEingefahren(seiteZumTippen, leistenname)
