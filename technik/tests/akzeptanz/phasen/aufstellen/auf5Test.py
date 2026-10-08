"""AUF-5 · Auswählen am Bildschirm."""

import re

import pytest
from playwright.sync_api import expect

from tests.akzeptanz.bildschirm import (
    ausgewählteEinheiten,
    ausgewählteModelle,
    einheitenKarteVon,
    elementeDerSeite,
    strichVon,
    umrissVon,
)
from tests.akzeptanz.handgriffe import einheitAufstellen, modelleSetzen

ausgewähltGekennzeichnet = re.compile(r"\bausgewählt\b")
anzahlGesetzterModelle = 3


def stellenDerModelle(gesetzte) -> frozenset[tuple[float, float]]:
    return frozenset((float(stelle.x), float(stelle.y)) for _, stelle in gesetzte)


def klickenUndWarten(seite, spielername: str, einheitenname: str) -> None:
    """Klickt die Karte der Einheit an und wartet, bis die Seite ihre Auswahl zeigt."""
    karte = einheitenKarteVon(seite, spielername, einheitenname)
    war = ausgewählteEinheiten(seite)
    karte.click()
    if einheitenname in war:
        expect(karte).not_to_have_class(ausgewähltGekennzeichnet)
    else:
        expect(karte).to_have_class(ausgewähltGekennzeichnet)


@pytest.mark.parametrize(
    ("spielername", "einheitenname"),
    [
        ("Spieler 1", "Boyz"),
        ("Spieler 1", "Warboss"),
        ("Spieler 2", "Necron Warriors"),
        ("Spieler 2", "Overlord"),
    ],
    ids=[
        "boyzAnDerReihe",
        "warbossAnDerReihe",
        "necronWarriorsNichtAnDerReihe",
        "overlordNichtAnDerReihe",
    ],
)
def testAuf5_3EinKlickAufEineNichtAusgewählteEinheitMachtSieAusgewählt(
    bildschirm, aufstellungNachDerZonenwahl, spielername, einheitenname
):
    seite = bildschirm.seiteZu(aufstellungNachDerZonenwahl)

    klickenUndWarten(seite, spielername, einheitenname)

    assert ausgewählteEinheiten(seite) == {einheitenname}


def testAuf5_3EinKlickAufEineNichtAusgewählteEinheitLässtDieAndereDesSpielersAusgewählt(
    bildschirm, aufstellungNachDerZonenwahl
):
    seite = bildschirm.seiteZu(aufstellungNachDerZonenwahl)
    klickenUndWarten(seite, "Spieler 1", "Boyz")

    klickenUndWarten(seite, "Spieler 1", "Warboss")

    assert ausgewählteEinheiten(seite) == {"Boyz", "Warboss"}


def testAuf5_3EinKlickAufEineEinheitDesAnderenSpielersLässtDieAusgewählteDesErstenAusgewählt(
    bildschirm, aufstellungNachDerZonenwahl
):
    seite = bildschirm.seiteZu(aufstellungNachDerZonenwahl)
    klickenUndWarten(seite, "Spieler 1", "Boyz")

    klickenUndWarten(seite, "Spieler 2", "Necron Warriors")

    assert ausgewählteEinheiten(seite) == {"Boyz", "Necron Warriors"}


@pytest.mark.parametrize(
    ("spielername", "einheitenname"),
    [("Spieler 1", "Boyz"), ("Spieler 2", "Necron Warriors")],
    ids=["einheitDesSpielersAnDerReihe", "einheitDesSpielersNichtAnDerReihe"],
)
def testAuf5_4EinKlickAufEineAusgewählteEinheitMachtSieNichtAusgewählt(
    bildschirm, aufstellungNachDerZonenwahl, spielername, einheitenname
):
    seite = bildschirm.seiteZu(aufstellungNachDerZonenwahl)
    klickenUndWarten(seite, spielername, einheitenname)

    klickenUndWarten(seite, spielername, einheitenname)

    assert ausgewählteEinheiten(seite) == frozenset()


def testAuf5_4EinKlickAufEineAusgewählteEinheitLässtDieAndereAusgewählteEinheitAusgewählt(
    bildschirm, aufstellungNachDerZonenwahl
):
    seite = bildschirm.seiteZu(aufstellungNachDerZonenwahl)
    klickenUndWarten(seite, "Spieler 1", "Boyz")
    klickenUndWarten(seite, "Spieler 1", "Warboss")

    klickenUndWarten(seite, "Spieler 1", "Boyz")

    assert ausgewählteEinheiten(seite) == {"Warboss"}


@pytest.mark.parametrize(
    ("spielername", "einheitenname"),
    [("Spieler 1", "Warboss"), ("Spieler 2", "Necron Warriors")],
    ids=["ablageVonSpielerEins", "ablageVonSpielerZwei"],
)
def testAuf5_6DieAblageKennzeichnetJedeAusgewählteEinheit(
    bildschirm, aufstellungNachDerZonenwahl, spielername, einheitenname
):
    seite = bildschirm.seiteZu(aufstellungNachDerZonenwahl)

    klickenUndWarten(seite, spielername, einheitenname)

    karte = einheitenKarteVon(seite, spielername, einheitenname)
    assert karte.count() == 1
    expect(karte).to_have_class(ausgewähltGekennzeichnet)


def testAuf5_6DieKennzeichnungDerAusgewähltenEinheitUnterscheidetSichVonDerEinheitInAufstellung(
    bildschirm, aufstellungNachDerZonenwahl, boyz
):
    modelleSetzen(aufstellungNachDerZonenwahl, boyz, 1)
    seite = bildschirm.seiteZu(aufstellungNachDerZonenwahl)

    klickenUndWarten(seite, "Spieler 1", "Warboss")

    ausgewählte = einheitenKarteVon(seite, "Spieler 1", "Warboss")
    inAufstellung = einheitenKarteVon(seite, "Spieler 1", "Boyz")
    assert ausgewählte.locator(".einheitenKartenAbzeichen").count() == 0
    assert inAufstellung.locator(".einheitenKartenAbzeichen").count() == 1
    expect(inAufstellung).not_to_have_class(ausgewähltGekennzeichnet)
    assert umrissVon(ausgewählte) != umrissVon(inAufstellung)


def testAuf5_6DieEinheitInAufstellungKannZugleichAusgewähltSeinUndZeigtBeides(
    bildschirm, aufstellungNachDerZonenwahl, boyz
):
    modelleSetzen(aufstellungNachDerZonenwahl, boyz, 1)
    seite = bildschirm.seiteZu(aufstellungNachDerZonenwahl)

    klickenUndWarten(seite, "Spieler 1", "Boyz")

    karte = einheitenKarteVon(seite, "Spieler 1", "Boyz")
    expect(karte).to_have_class(ausgewähltGekennzeichnet)
    assert karte.locator(".einheitenKartenAbzeichen").count() == 1


def testAuf5_7DieKarteKennzeichnetJedesGesetzteModellDerAusgewähltenEinheit(
    bildschirm, aufstellungNachDerZonenwahl, boyz
):
    gesetzte = modelleSetzen(aufstellungNachDerZonenwahl, boyz, anzahlGesetzterModelle)
    seite = bildschirm.seiteZu(aufstellungNachDerZonenwahl)

    klickenUndWarten(seite, "Spieler 1", "Boyz")

    assert ausgewählteModelle(seite) == stellenDerModelle(gesetzte)


def testAuf5_7DieKarteKennzeichnetNurDieGesetztenModelleDerAusgewähltenEinheit(
    bildschirm, aufstellungNachDerZonenwahl, boyz, necronWarriors
):
    einheitAufstellen(aufstellungNachDerZonenwahl, boyz)
    gesetzteDerNecrons = modelleSetzen(aufstellungNachDerZonenwahl, necronWarriors, 2)
    seite = bildschirm.seiteZu(aufstellungNachDerZonenwahl)

    klickenUndWarten(seite, "Spieler 2", "Necron Warriors")

    assert ausgewählteModelle(seite) == stellenDerModelle(gesetzteDerNecrons)
    assert len(elementeDerSeite(seite, ".karte .modell")) == len(boyz.modelle) + 2


def testAuf5_7DieKarteKennzeichnetKeinModellEinerNichtAusgewähltenEinheit(
    bildschirm, aufstellungNachDerZonenwahl, boyz
):
    modelleSetzen(aufstellungNachDerZonenwahl, boyz, anzahlGesetzterModelle)
    seite = bildschirm.seiteZu(aufstellungNachDerZonenwahl)

    klickenUndWarten(seite, "Spieler 1", "Warboss")

    assert ausgewählteModelle(seite) == frozenset()
    assert len(elementeDerSeite(seite, ".karte .modell")) == anzahlGesetzterModelle


def testAuf5_7DieKarteKennzeichnetNachAbwahlDerEinheitKeinModellMehr(
    bildschirm, aufstellungNachDerZonenwahl, boyz
):
    modelleSetzen(aufstellungNachDerZonenwahl, boyz, anzahlGesetzterModelle)
    seite = bildschirm.seiteZu(aufstellungNachDerZonenwahl)
    klickenUndWarten(seite, "Spieler 1", "Boyz")

    klickenUndWarten(seite, "Spieler 1", "Boyz")

    assert ausgewählteModelle(seite) == frozenset()


def testAuf5_7DieKarteZeichnetDenKreisEinesAusgewähltenModellsAndersAlsEinenNichtAusgewählten(
    bildschirm, aufstellungNachDerZonenwahl, boyz, necronWarriors
):
    einheitAufstellen(aufstellungNachDerZonenwahl, boyz)
    modelleSetzen(aufstellungNachDerZonenwahl, necronWarriors, 2)
    seite = bildschirm.seiteZu(aufstellungNachDerZonenwahl)

    klickenUndWarten(seite, "Spieler 2", "Necron Warriors")

    ausgewähltesModell = seite.locator(".karte .modell.ausgewählt").first
    nichtAusgewähltesModell = seite.locator(".karte .modell:not(.ausgewählt)").first
    assert strichVon(ausgewähltesModell) != strichVon(nichtAusgewähltesModell)


@pytest.mark.parametrize("vorherAusgewählt", [False, True], ids=["auswählen", "abwählen"])
def testAuf5_8EinKlickÄndertWederDenSpielerAnDerReiheNochDieEinheitInAufstellungNochEinModell(
    bildschirm, aufstellungNachDerZonenwahl, spielerEins, boyz, vorherAusgewählt
):
    gesetzte = modelleSetzen(aufstellungNachDerZonenwahl, boyz, anzahlGesetzterModelle)
    seite = bildschirm.seiteZu(aufstellungNachDerZonenwahl)
    if vorherAusgewählt:
        klickenUndWarten(seite, "Spieler 2", "Necron Warriors")

    klickenUndWarten(seite, "Spieler 2", "Necron Warriors")

    assert aufstellungNachDerZonenwahl.anDerReihe is spielerEins
    assert aufstellungNachDerZonenwahl.einheitInAufstellung is boyz
    for modell in spielerEins.armee.modelle:
        erwartet = dict(gesetzte).get(modell)
        assert aufstellungNachDerZonenwahl.stelle(modell) == erwartet
    markierte = seite.locator(".kopfzeileSpieler").filter(has=seite.locator(".kopfzeileAnDerReihe"))
    assert "Spieler 1" in markierte.text_content()


def testAuf5_8EinKlickAufEineEinheitOhneGesetztesModellMachtSieNichtZurEinheitInAufstellung(
    bildschirm, aufstellungNachDerZonenwahl, spielerEins
):
    seite = bildschirm.seiteZu(aufstellungNachDerZonenwahl)

    klickenUndWarten(seite, "Spieler 1", "Boyz")

    aufstellung = aufstellungNachDerZonenwahl
    gesetzteModelle = [
        modell for modell in spielerEins.armee.modelle if aufstellung.gesetzt(modell)
    ]
    assert gesetzteModelle == []
    assert aufstellung.einheitInAufstellung is None
    assert aufstellung.anDerReihe is spielerEins
    assert elementeDerSeite(seite, ".karte .modell") == ()


def testAuf5_8EinKlickAufEineAndereEinheitLässtDieEinheitInAufstellungUndIhreModelle(
    bildschirm, aufstellungNachDerZonenwahl, spielerEins, boyz
):
    gesetzte = modelleSetzen(aufstellungNachDerZonenwahl, boyz, 1)
    seite = bildschirm.seiteZu(aufstellungNachDerZonenwahl)

    klickenUndWarten(seite, "Spieler 1", "Warboss")

    aufstellung = aufstellungNachDerZonenwahl
    assert aufstellung.einheitInAufstellung is boyz
    assert aufstellung.anDerReihe is spielerEins
    for modell in spielerEins.armee.modelle:
        assert aufstellung.stelle(modell) == dict(gesetzte).get(modell)


def testAuf5_8EinKlickAufDieAblageDesSpielersNichtAnDerReiheLässtSeineModelleUngesetzt(
    bildschirm, aufstellungNachDerZonenwahl, spielerZwei
):
    seite = bildschirm.seiteZu(aufstellungNachDerZonenwahl)

    klickenUndWarten(seite, "Spieler 2", "Necron Warriors")

    aufstellung = aufstellungNachDerZonenwahl
    gesetzteModelle = [
        modell for modell in spielerZwei.armee.modelle if aufstellung.gesetzt(modell)
    ]
    assert gesetzteModelle == []
    assert aufstellungNachDerZonenwahl.einheitInAufstellung is None
    assert elementeDerSeite(seite, ".karte .modell") == ()


def testAuf5_9NachDemStartIstKeineEinheitAusgewählt(adresseDesBefehls, bildschirm):
    seite = bildschirm.seiteBei(adresseDesBefehls)

    assert seite.locator(".einheitenKarte").count() > 0
    assert seite.locator(".ausgewählt").count() == 0


def testAuf5_10WirdEineAusgewählteEinheitAufgestelltIstSieNichtMehrAusgewählt(
    bildschirm, aufstellungNachDerZonenwahl, boyz
):
    seite = bildschirm.seiteZu(aufstellungNachDerZonenwahl)
    klickenUndWarten(seite, "Spieler 1", "Boyz")
    einheitAufstellen(aufstellungNachDerZonenwahl, boyz)

    seite.reload()
    seite.wait_for_selector(".karte .spielfeld")

    assert ausgewählteModelle(seite) == frozenset()
    assert len(elementeDerSeite(seite, ".karte .modell")) == len(boyz.modelle)


def testAuf5_10DieAndereAusgewählteEinheitBleibtNachDemAufstellenAusgewählt(
    bildschirm, aufstellungNachDerZonenwahl, boyz
):
    seite = bildschirm.seiteZu(aufstellungNachDerZonenwahl)
    klickenUndWarten(seite, "Spieler 1", "Boyz")
    klickenUndWarten(seite, "Spieler 1", "Warboss")
    einheitAufstellen(aufstellungNachDerZonenwahl, boyz)

    seite.reload()
    seite.wait_for_selector(".karte .spielfeld")

    assert ausgewählteEinheiten(seite) == {"Warboss"}
    assert ausgewählteModelle(seite) == frozenset()
