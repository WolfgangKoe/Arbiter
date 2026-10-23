"""AUF-23 · Einheit zurücklegen."""

from http import HTTPStatus

import pytest
from playwright.sync_api import expect

from tests.akzeptanz.auswahl import ausgewählteEinheiten
from tests.akzeptanz.bildschirm import (
    aufDieHandlungWarten,
    beendenKnopf,
    knopfDerSeite,
    zurücklegenKnopf,
)
from tests.akzeptanz.dienst import (
    auswählen,
    modellAlsEbene,
    spielstandDesVertrags,
    spielstandVon,
    zurückgelegtDesVertrags,
    zurücklegen,
)
from tests.akzeptanz.handgriffe import einheitAufstellen, modelleSetzen, stellenAllerModelle

zurücklegenAdresse = "**/api/zur%C3%BCcklegen"
anzahlGesetzter = 3


def ohneAuswahl(aufstellung, einheit, _modell):
    """Die Einheit bleibt, wie sie ist: nicht ausgewählt."""


def ausgewählt(aufstellung, einheit, _modell):
    aufstellung.auswählen(einheit)


def einModellAlsEbene(aufstellung, einheit, modell):
    aufstellung.auswählen(einheit)
    aufstellung.ebeneWählen(modell)


mitJederEbene = pytest.mark.parametrize(
    "ebeneWählen",
    [ohneAuswahl, ausgewählt, einModellAlsEbene],
    ids=["nichtAusgewählt", "ganzeEinheit", "einModell"],
)

mitAusgewählterEinheit = pytest.mark.parametrize(
    "ebeneWählen",
    [ausgewählt, einModellAlsEbene],
    ids=["ganzeEinheit", "einModell"],
)


def gesetzteStellen(aufstellung):
    """Die gesetzten Modelle, die die Karte zeigen muss."""
    return [stelle for stelle in stellenAllerModelle(aufstellung).values() if stelle is not None]


def keineEinheitInAufstellung(aufstellung, einheit):
    """Die Zonenwahl ist getroffen, kein Modell ist gesetzt."""


def eineEinheitAufgestellt(aufstellung, einheit):
    einheitAufstellen(aufstellung, einheit)


ohneEinheitInAufstellung = pytest.mark.parametrize(
    "vorgeschichte",
    [keineEinheitInAufstellung, eineEinheitAufgestellt],
    ids=["keinModellGesetzt", "eineEinheitAufgestellt"],
)


@pytest.fixture
def boyzMitEbene(aufstellungNachDerZonenwahl, boyz, boyzSetzen, ebeneWählen):
    """Drei gesetzte Boyz; die Ebene und die Auswahl legt der Test fest."""
    [(erstes, _), *_] = boyzSetzen(anzahlGesetzter)
    ebeneWählen(aufstellungNachDerZonenwahl, boyz, erstes)
    return boyz


@mitJederEbene
def testAuf23_1ZurücklegenNimmtAlleGesetztenModelleDerEinheitInAufstellungVonDerKarte(
    aufstellungNachDerZonenwahl, spielerEins, boyzMitEbene
):
    aufstellungNachDerZonenwahl.zurücklegen()

    assert not any(aufstellungNachDerZonenwahl.gesetzt(modell) for modell in boyzMitEbene.modelle)
    assert aufstellungNachDerZonenwahl.einheitInAufstellung is None
    assert aufstellungNachDerZonenwahl.anDerReihe is spielerEins


@mitJederEbene
def testAuf23_1DerDienstNimmtAlleGesetztenModelleDerEinheitInAufstellungVonDerKarte(
    dienst, aufstellungNachDerZonenwahl, spielerEins, boyzMitEbene
):
    antwort = zurücklegen(dienst)

    spielstand = antwort.get_json()
    assert antwort.status_code == HTTPStatus.OK
    assert spielstand["modelle"] == []
    assert spielstand["einheitInAufstellung"] is None
    assert not any(aufstellungNachDerZonenwahl.gesetzt(modell) for modell in boyzMitEbene.modelle)
    assert aufstellungNachDerZonenwahl.anDerReihe is spielerEins


def testAuf23_1ZurücklegenLässtDieAufgestelltenEinheitenAufDerKarte(
    aufstellungMitModellenBeiderSpieler, spielerEins, warboss
):
    aufstellung = aufstellungMitModellenBeiderSpieler
    stellenDavor = stellenAllerModelle(aufstellung)
    modelleSetzen(aufstellung, warboss, 1)

    aufstellung.zurücklegen()

    assert stellenAllerModelle(aufstellung) == stellenDavor
    assert aufstellung.einheitInAufstellung is None
    assert aufstellung.anDerReihe is spielerEins


def testAuf23_1DerDienstLässtDieAufgestelltenEinheitenAufDerKarte(
    dienst, aufstellungMitModellenBeiderSpieler, warboss
):
    modelleDavor = spielstandVon(dienst)["modelle"]
    modelleSetzen(aufstellungMitModellenBeiderSpieler, warboss, 1)

    antwort = zurücklegen(dienst)

    assert antwort.status_code == HTTPStatus.OK
    assert antwort.get_json()["modelle"] == modelleDavor


def testAuf23_1DerDienstZeigtNachDemZurücklegenDasBeispielImVertrag(dienstDesBeispiels):
    auswählen(dienstDesBeispiels, "Necron Warriors")

    antwort = zurücklegen(dienstDesBeispiels)

    assert antwort.status_code == HTTPStatus.OK
    assert antwort.get_json() == zurückgelegtDesVertrags()


@mitJederEbene
def testAuf23_1EinKlickAufEinheitZurücklegenNimmtDieEinheitInAufstellungVonDerKarte(
    bildschirm, aufstellungNachDerZonenwahl, spielerEins, boyzMitEbene
):
    seite = bildschirm.seiteZu(aufstellungNachDerZonenwahl)
    knopf = knopfDerSeite(seite, zurücklegenKnopf)

    with aufDieHandlungWarten(seite):
        knopf.click()

    expect(seite.locator(".karte .modell")).to_have_count(0)
    assert not any(aufstellungNachDerZonenwahl.gesetzt(modell) for modell in boyzMitEbene.modelle)
    assert aufstellungNachDerZonenwahl.anDerReihe is spielerEins


def testAuf23_1EinKlickAufEinheitZurücklegenLässtDieAufgestelltenEinheitenAufDerKarte(
    bildschirm, aufstellungMitModellenBeiderSpieler, warboss
):
    aufstellung = aufstellungMitModellenBeiderSpieler
    anzahlAufgestellter = len(gesetzteStellen(aufstellung))
    modelleSetzen(aufstellung, warboss, 1)
    seite = bildschirm.seiteZu(aufstellung)
    knopf = knopfDerSeite(seite, zurücklegenKnopf)

    with aufDieHandlungWarten(seite):
        knopf.click()

    expect(seite.locator(".karte .modell")).to_have_count(anzahlAufgestellter)


def testAuf23_1DieSeiteLeertDieKarteMitDerAntwortImBeispiel(bildschirm, ausgangsaufstellung):
    antworten = {zurücklegenAdresse: zurückgelegtDesVertrags()}
    seite = bildschirm.seiteMitSpielstand(ausgangsaufstellung, spielstandDesVertrags(), antworten)
    knopf = knopfDerSeite(seite, zurücklegenKnopf)

    with aufDieHandlungWarten(seite):
        knopf.click()

    expect(seite.locator(".karte .modell")).to_have_count(0)


@mitAusgewählterEinheit
def testAuf23_3EineAusgewählteEinheitBleibtNachDemZurücklegenAusgewähltMitDerGanzenEinheitAlsEbene(
    aufstellungNachDerZonenwahl, boyzMitEbene
):
    aufstellungNachDerZonenwahl.zurücklegen()

    assert aufstellungNachDerZonenwahl.ausgewählt(boyzMitEbene)
    assert aufstellungNachDerZonenwahl.ganzeEinheitIstEbene(boyzMitEbene)
    assert not any(
        aufstellungNachDerZonenwahl.modellIstEbene(modell) for modell in boyzMitEbene.modelle
    )


def testAuf23_3MitEinemModellAlsEbeneLässtDerDienstDieEinheitMitDerGanzenEinheitAlsEbeneAusgewählt(
    dienstDesBeispiels, aufstellungDesBeispiels, necronWarriors
):
    auswählen(dienstDesBeispiels, "Necron Warriors")
    _, _, drittes, *_ = necronWarriors.modelle
    modellAlsEbene(dienstDesBeispiels, aufstellungDesBeispiels, necronWarriors, drittes)

    antwort = zurücklegen(dienstDesBeispiels)

    assert antwort.status_code == HTTPStatus.OK
    assert antwort.get_json() == zurückgelegtDesVertrags()
    assert aufstellungDesBeispiels.ganzeEinheitIstEbene(necronWarriors)


def testAuf23_3DieSeiteZeigtDieEinheitMitDerAntwortImBeispielAusgewählt(
    bildschirm, ausgangsaufstellung
):
    antworten = {zurücklegenAdresse: zurückgelegtDesVertrags()}
    seite = bildschirm.seiteMitSpielstand(ausgangsaufstellung, spielstandDesVertrags(), antworten)
    knopf = knopfDerSeite(seite, zurücklegenKnopf)

    with aufDieHandlungWarten(seite):
        knopf.click()

    expect(seite.locator(".karte .modell")).to_have_count(0)
    assert ausgewählteEinheiten(seite) == {"Necron Warriors"}


@mitAusgewählterEinheit
@pytest.mark.usefixtures("boyzMitEbene")
def testAuf23_3DieSeiteZeigtDieEinheitNachDemZurücklegenAusgewählt(
    bildschirm, aufstellungNachDerZonenwahl
):
    seite = bildschirm.seiteZu(aufstellungNachDerZonenwahl)
    knopf = knopfDerSeite(seite, zurücklegenKnopf)

    with aufDieHandlungWarten(seite):
        knopf.click()

    expect(seite.locator(".karte .modell")).to_have_count(0)
    assert ausgewählteEinheiten(seite) == {"Boyz"}


def testAuf23_4MitEinerEinheitInAufstellungBietetDieSeiteEinheitZurücklegenNebenBeendenAn(
    bildschirm, aufstellungNachDerZonenwahl, boyzSetzen
):
    boyzSetzen(1)

    seite = bildschirm.seiteZu(aufstellungNachDerZonenwahl)

    expect(knopfDerSeite(seite, beendenKnopf)).to_have_count(1)
    expect(knopfDerSeite(seite, zurücklegenKnopf)).to_have_count(1)


def testAuf23_4DieSeiteBietetImBeispielMitEinerEinheitInAufstellungBeideKnöpfeAn(
    bildschirm, ausgangsaufstellung
):
    seite = bildschirm.seiteMitSpielstand(ausgangsaufstellung, spielstandDesVertrags())

    expect(knopfDerSeite(seite, beendenKnopf)).to_have_count(1)
    expect(knopfDerSeite(seite, zurücklegenKnopf)).to_have_count(1)


def testAuf23_4DieSeiteBietetImBeispielOhneEinheitInAufstellungNurBeendenAn(
    bildschirm, ausgangsaufstellung
):
    seite = bildschirm.seiteMitSpielstand(ausgangsaufstellung, zurückgelegtDesVertrags())

    expect(knopfDerSeite(seite, beendenKnopf)).to_have_count(1)
    expect(knopfDerSeite(seite, zurücklegenKnopf)).to_have_count(0)


@ohneEinheitInAufstellung
def testAuf23_4OhneEinheitInAufstellungBietetDieSeiteEinheitZurücklegenNichtAn(
    bildschirm, aufstellungNachDerZonenwahl, boyz, vorgeschichte
):
    vorgeschichte(aufstellungNachDerZonenwahl, boyz)

    seite = bildschirm.seiteZu(aufstellungNachDerZonenwahl)

    expect(knopfDerSeite(seite, beendenKnopf)).to_have_count(1)
    expect(knopfDerSeite(seite, zurücklegenKnopf)).to_have_count(0)


def testAuf23_4NachDemZurücklegenBietetDieSeiteEinheitZurücklegenNichtMehrAn(
    bildschirm, aufstellungNachDerZonenwahl, boyzSetzen
):
    boyzSetzen(1)
    seite = bildschirm.seiteZu(aufstellungNachDerZonenwahl)
    knopf = knopfDerSeite(seite, zurücklegenKnopf)

    with aufDieHandlungWarten(seite):
        knopf.click()

    expect(knopfDerSeite(seite, beendenKnopf)).to_have_count(1)
    expect(knopf).to_have_count(0)


@ohneEinheitInAufstellung
def testAuf23_5OhneEinheitInAufstellungÄndertZurücklegenNichtsUndNenntKeinenGrund(
    aufstellungNachDerZonenwahl, boyz, vorgeschichte
):
    vorgeschichte(aufstellungNachDerZonenwahl, boyz)
    stellenDavor = stellenAllerModelle(aufstellungNachDerZonenwahl)
    anDerReihe = aufstellungNachDerZonenwahl.anDerReihe

    aufstellungNachDerZonenwahl.zurücklegen()

    assert stellenAllerModelle(aufstellungNachDerZonenwahl) == stellenDavor
    assert aufstellungNachDerZonenwahl.anDerReihe is anDerReihe
    assert aufstellungNachDerZonenwahl.einheitInAufstellung is None


@ohneEinheitInAufstellung
def testAuf23_5OhneEinheitInAufstellungAntwortetDerDienstMitDemGleichenSpielstand(
    dienst, aufstellungNachDerZonenwahl, boyz, vorgeschichte
):
    vorgeschichte(aufstellungNachDerZonenwahl, boyz)
    spielstandDavor = spielstandVon(dienst)

    antwort = zurücklegen(dienst)

    assert antwort.status_code == HTTPStatus.OK
    assert antwort.get_json() == spielstandDavor
