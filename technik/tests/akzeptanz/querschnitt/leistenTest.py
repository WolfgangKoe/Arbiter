"""QUE-6 · Leisten."""

import pytest
from playwright.sync_api import Locator, Page, expect

from tests.akzeptanz.bildschirm import griffVon, leisteVon
from tests.akzeptanz.handgriffe import versetzt
from tests.akzeptanz.schlacht import anhaltenUndÜbergehen, zehnZollNachOsten


def linksDesSpielfelds(leiste: dict, spielfeld: dict) -> bool:
    return leiste["x"] + leiste["width"] <= spielfeld["x"]


def rechtsDesSpielfelds(leiste: dict, spielfeld: dict) -> bool:
    return leiste["x"] >= spielfeld["x"] + spielfeld["width"]


def unterDemSpielfeld(leiste: dict, spielfeld: dict) -> bool:
    return leiste["y"] >= spielfeld["y"] + spielfeld["height"]


lageJeLeiste = pytest.mark.parametrize(
    ("leistenname", "lage"),
    [
        ("Armeeliste Spieler 1", linksDesSpielfelds),
        ("Armeeliste Spieler 2", rechtsDesSpielfelds),
        ("Protokoll", unterDemSpielfeld),
    ],
    ids=["links", "rechts", "unten"],
)

inhaltJeLeiste = {
    "Armeeliste Spieler 1": (".armeeKarte", "Spieler 1"),
    "Armeeliste Spieler 2": (".armeeKarte", "Spieler 2"),
    "Protokoll": (".protokollEintrag", "Warboss"),
}

jedeLeiste = pytest.mark.parametrize(
    "leistenname", list(inhaltJeLeiste), ids=["links", "rechts", "unten"]
)

jedeArmeeliste = pytest.mark.parametrize(
    "leistenname", ["Armeeliste Spieler 1", "Armeeliste Spieler 2"], ids=["links", "rechts"]
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


def warbossÜbergehen(schlacht, warboss) -> None:
    (boss,) = warboss.modelle
    anhaltenUndÜbergehen(schlacht, boss, versetzt(schlacht.stelle(boss), zehnZollNachOsten))


@pytest.fixture
def seiteMitProtokoll(
    bildschirm, beendeteAufstellung, schlachtInDerBewegungsphase, warboss
) -> Page:
    warbossÜbergehen(schlachtInDerBewegungsphase, warboss)
    return bildschirm.seiteZuSchlacht(beendeteAufstellung, schlachtInDerBewegungsphase)


@pytest.fixture
def seiteZumTippen(bildschirm, beendeteAufstellung, schlachtInDerBewegungsphase, warboss) -> Page:
    warbossÜbergehen(schlachtInDerBewegungsphase, warboss)
    return bildschirm.seiteZuSchlacht(
        beendeteAufstellung, schlachtInDerBewegungsphase, berührbar=True
    )


@lageJeLeiste
def testQue6_1JedeLeisteStehtAnIhrerSeiteDesSpielfelds(
    bildschirm, aufstellungNachDerZonenwahl, leistenname, lage
):
    seite = bildschirm.seiteZu(aufstellungNachDerZonenwahl)

    leiste = leisteVon(seite, leistenname).bounding_box()
    spielfeld = seite.locator("svg.spielfeld").bounding_box()

    assert lage(leiste, spielfeld)


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


@jedeArmeeliste
def testQue6_2NachDemStartZeigtJedeArmeelisteIhrenInhalt(
    adresseDesBefehls, bildschirm, leistenname
):
    seite = bildschirm.seiteBei(adresseDesBefehls)

    inhalt = inhaltVon(seite, leistenname)

    expect(inhalt).to_be_visible()


@jedeLeiste
def testQue6_3EinKlickAufDenGriffEinerNichtEingefahrenenLeisteFährtSieEin(
    seiteMitProtokoll, leistenname
):
    istNichtEingefahren(seiteMitProtokoll, leistenname)

    griffVon(seiteMitProtokoll, leistenname).click()

    istEingefahren(seiteMitProtokoll, leistenname)


@jedeLeiste
def testQue6_4EinKlickAufDenGriffEinerEingefahrenenLeisteFährtSieNichtMehrEin(
    seiteMitProtokoll, leistenname
):
    griffVon(seiteMitProtokoll, leistenname).click()
    istEingefahren(seiteMitProtokoll, leistenname)

    griffVon(seiteMitProtokoll, leistenname).click()

    istNichtEingefahren(seiteMitProtokoll, leistenname)


@jedeLeiste
def testQue6_5EinTippenAufDenGriffEinerNichtEingefahrenenLeisteWirktWieEinKlick(
    seiteZumTippen, leistenname
):
    istNichtEingefahren(seiteZumTippen, leistenname)

    griffVon(seiteZumTippen, leistenname).tap()

    istEingefahren(seiteZumTippen, leistenname)


@jedeLeiste
def testQue6_5EinTippenAufDenGriffEinerEingefahrenenLeisteWirktWieEinKlick(
    seiteZumTippen, leistenname
):
    griffVon(seiteZumTippen, leistenname).tap()
    istEingefahren(seiteZumTippen, leistenname)

    griffVon(seiteZumTippen, leistenname).tap()

    istNichtEingefahren(seiteZumTippen, leistenname)
