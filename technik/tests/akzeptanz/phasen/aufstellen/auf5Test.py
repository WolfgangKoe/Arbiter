"""AUF-5 · Auswählen am Bildschirm."""

from collections.abc import Callable
from http import HTTPStatus
from typing import NamedTuple

import pytest
from playwright.sync_api import expect

from tests.akzeptanz.bildschirm import (
    ausgewählteEinheiten,
    ausgewählteModelle,
    ausgewähltGekennzeichnet,
    einheitenKarteVon,
    elementeDerSeite,
    klickenUndWarten,
    spielerAnDerReihe,
    strichVon,
    umrissVon,
)
from tests.akzeptanz.dienst import (
    abwählen,
    ausgewählteEinheitenIm,
    ausgewählteModelleIm,
    auswählen,
    dienstFür,
    einheitenDerAblagen,
    spielstandDesVertrags,
    spielstandVon,
)
from tests.akzeptanz.handgriffe import anzahlGesetzterModelle, einheitAufstellen, modelleSetzen


def stellenDerModelle(gesetzte) -> frozenset[tuple[float, float]]:
    return frozenset((float(stelle.x), float(stelle.y)) for _, stelle in gesetzte)


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
    assert "Spieler 1" in spielerAnDerReihe(seite).text_content()


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
    aufstellungNachDerZonenwahl.auswählen(boyz)
    einheitAufstellen(aufstellungNachDerZonenwahl, boyz)

    seite = bildschirm.seiteZu(aufstellungNachDerZonenwahl)

    assert ausgewählteModelle(seite) == frozenset()
    assert len(elementeDerSeite(seite, ".karte .modell")) == len(boyz.modelle)


def testAuf5_10DieAndereAusgewählteEinheitBleibtNachDemAufstellenAusgewählt(
    bildschirm, aufstellungNachDerZonenwahl, boyz, warboss
):
    aufstellungNachDerZonenwahl.auswählen(boyz)
    aufstellungNachDerZonenwahl.auswählen(warboss)
    einheitAufstellen(aufstellungNachDerZonenwahl, boyz)

    seite = bildschirm.seiteZu(aufstellungNachDerZonenwahl)

    assert ausgewählteEinheiten(seite) == {"Warboss"}
    assert ausgewählteModelle(seite) == frozenset()


def testAuf5_6DieSeiteKennzeichnetImBeispielDesVertragsDieAusgewähltenEinheiten(
    bildschirm, ausgangsaufstellung
):
    spielstand = spielstandDesVertrags()

    seite = bildschirm.seiteMitSpielstand(ausgangsaufstellung, spielstand)

    assert ausgewählteEinheiten(seite) == ausgewählteEinheitenIm(spielstand)


def testAuf5_7DieSeiteZeichnetImBeispielDesVertragsDieAusgewähltenModelleAusgewählt(
    bildschirm, ausgangsaufstellung
):
    spielstand = spielstandDesVertrags()

    seite = bildschirm.seiteMitSpielstand(ausgangsaufstellung, spielstand)

    assert ausgewählteModelle(seite) == ausgewählteModelleIm(spielstand)


@pytest.mark.parametrize(
    "einheitenname",
    ["Boyz", "Warboss", "Necron Warriors", "Overlord"],
    ids=["boyz", "warboss", "necronWarriors", "overlord"],
)
def testAuf5_3DerDienstMachtEineNichtAusgewählteEinheitAusgewählt(dienst, einheitenname):
    antwort = auswählen(dienst, einheitenname)

    assert antwort.status_code == HTTPStatus.OK
    assert ausgewählteEinheitenIm(antwort.get_json()) == {einheitenname}
    assert ausgewählteEinheitenIm(spielstandVon(dienst)) == {einheitenname}


def testAuf5_3DerDienstLässtDieAndereAusgewählteEinheitDesSpielersAusgewählt(dienst):
    auswählen(dienst, "Boyz")

    antwort = auswählen(dienst, "Warboss")

    assert antwort.status_code == HTTPStatus.OK
    assert ausgewählteEinheitenIm(antwort.get_json()) == {"Boyz", "Warboss"}


def testAuf5_3DerDienstLässtDieAusgewählteEinheitDesAnderenSpielersAusgewählt(dienst):
    auswählen(dienst, "Boyz")

    antwort = auswählen(dienst, "Necron Warriors")

    assert antwort.status_code == HTTPStatus.OK
    assert ausgewählteEinheitenIm(antwort.get_json()) == {"Boyz", "Necron Warriors"}


@pytest.mark.parametrize(
    "einheitenname", ["Boyz", "Necron Warriors"], ids=["boyz", "necronWarriors"]
)
def testAuf5_4DerDienstMachtEineAusgewählteEinheitNichtAusgewählt(dienst, einheitenname):
    auswählen(dienst, einheitenname)

    antwort = abwählen(dienst, einheitenname)

    assert antwort.status_code == HTTPStatus.OK
    assert ausgewählteEinheitenIm(antwort.get_json()) == frozenset()
    assert ausgewählteEinheitenIm(spielstandVon(dienst)) == frozenset()


def testAuf5_4DerDienstLässtDieAndereAusgewählteEinheitAusgewählt(dienst):
    auswählen(dienst, "Boyz")
    auswählen(dienst, "Warboss")

    antwort = abwählen(dienst, "Boyz")

    assert antwort.status_code == HTTPStatus.OK
    assert ausgewählteEinheitenIm(antwort.get_json()) == {"Warboss"}


def testAuf5_6DerSpielstandKennzeichnetDieAusgewählteEinheitUnabhängigVonDerEinheitInAufstellung(
    dienst, aufstellungNachDerZonenwahl, boyz
):
    modelleSetzen(aufstellungNachDerZonenwahl, boyz, 1)

    antwort = auswählen(dienst, "Warboss")

    einheiten = einheitenDerAblagen(antwort.get_json())
    assert einheiten["Warboss"]["ausgewählt"] is True
    assert einheiten["Warboss"]["inAufstellung"] is False
    assert einheiten["Boyz"]["ausgewählt"] is False
    assert einheiten["Boyz"]["inAufstellung"] is True


def testAuf5_6DerSpielstandKennzeichnetDieEinheitInAufstellungAuchWennSieAusgewähltIst(
    dienst, aufstellungNachDerZonenwahl, boyz
):
    modelleSetzen(aufstellungNachDerZonenwahl, boyz, 1)

    antwort = auswählen(dienst, "Boyz")

    einheit = einheitenDerAblagen(antwort.get_json())["Boyz"]
    assert einheit["ausgewählt"] is True
    assert einheit["inAufstellung"] is True


def testAuf5_7DerSpielstandKennzeichnetJedesGesetzteModellDerAusgewähltenEinheit(
    dienst, aufstellungNachDerZonenwahl, boyz
):
    gesetzte = modelleSetzen(aufstellungNachDerZonenwahl, boyz, anzahlGesetzterModelle)

    antwort = auswählen(dienst, "Boyz")

    spielstand = antwort.get_json()
    assert ausgewählteModelleIm(spielstand) == stellenDerModelle(gesetzte)
    assert len(spielstand["modelle"]) == anzahlGesetzterModelle


def testAuf5_7DerSpielstandKennzeichnetNurDieGesetztenModelleDerAusgewähltenEinheit(
    dienst, aufstellungNachDerZonenwahl, boyz, necronWarriors
):
    einheitAufstellen(aufstellungNachDerZonenwahl, boyz)
    gesetzteDerNecrons = modelleSetzen(aufstellungNachDerZonenwahl, necronWarriors, 2)

    antwort = auswählen(dienst, "Necron Warriors")

    spielstand = antwort.get_json()
    assert ausgewählteModelleIm(spielstand) == stellenDerModelle(gesetzteDerNecrons)
    assert len(spielstand["modelle"]) == len(boyz.modelle) + 2


def testAuf5_7DerSpielstandKennzeichnetKeinModellEinerNichtAusgewähltenEinheit(
    dienst, aufstellungNachDerZonenwahl, boyz
):
    modelleSetzen(aufstellungNachDerZonenwahl, boyz, anzahlGesetzterModelle)

    antwort = auswählen(dienst, "Warboss")

    spielstand = antwort.get_json()
    assert ausgewählteModelleIm(spielstand) == frozenset()
    assert len(spielstand["modelle"]) == anzahlGesetzterModelle


def testAuf5_7DerSpielstandKennzeichnetNachAbwahlDerEinheitKeinModellMehr(
    dienst, aufstellungNachDerZonenwahl, boyz
):
    modelleSetzen(aufstellungNachDerZonenwahl, boyz, anzahlGesetzterModelle)
    auswählen(dienst, "Boyz")

    antwort = abwählen(dienst, "Boyz")

    assert ausgewählteModelleIm(antwort.get_json()) == frozenset()


class Auswahlfall(NamedTuple):
    einheitenname: str
    gesetzteModelle: int
    anfrage: Callable


@pytest.mark.parametrize(
    "fall",
    [
        Auswahlfall("Boyz", 0, auswählen),
        Auswahlfall("Boyz", 0, abwählen),
        Auswahlfall("Warboss", 1, auswählen),
        Auswahlfall("Warboss", 1, abwählen),
        Auswahlfall("Necron Warriors", 1, auswählen),
        Auswahlfall("Necron Warriors", 1, abwählen),
    ],
    ids=[
        "boyzOhneGesetztesModellAuswählen",
        "boyzOhneGesetztesModellAbwählen",
        "warbossBeiBoyzInAufstellungAuswählen",
        "warbossBeiBoyzInAufstellungAbwählen",
        "necronWarriorsNichtAnDerReiheAuswählen",
        "necronWarriorsNichtAnDerReiheAbwählen",
    ],
)
def testAuf5_8DerDienstÄndertBeiAuswählenUndAbwählenNurDieAuswahl(
    dienst, aufstellungNachDerZonenwahl, spielerEins, boyz, fall
):
    gesetzte = modelleSetzen(aufstellungNachDerZonenwahl, boyz, fall.gesetzteModelle)
    erwartetInAufstellung = boyz if gesetzte else None
    if fall.anfrage is abwählen:
        auswählen(dienst, fall.einheitenname)

    antwort = fall.anfrage(dienst, fall.einheitenname)

    assert antwort.status_code == HTTPStatus.OK
    assert aufstellungNachDerZonenwahl.anDerReihe is spielerEins
    assert aufstellungNachDerZonenwahl.einheitInAufstellung is erwartetInAufstellung
    for modell in spielerEins.armee.modelle:
        assert aufstellungNachDerZonenwahl.stelle(modell) == dict(gesetzte).get(modell)


def testAuf5_9DerSpielstandNachDemStartKenntKeineAusgewählteEinheit(ausgangsaufstellung):
    spielstand = spielstandVon(dienstFür(ausgangsaufstellung))

    assert einheitenDerAblagen(spielstand)
    assert ausgewählteEinheitenIm(spielstand) == frozenset()
    assert ausgewählteModelleIm(spielstand) == frozenset()


def testAuf5_10DerSpielstandKenntEineAufgestellteEinheitNichtMehrAlsAusgewählt(
    dienst, aufstellungNachDerZonenwahl, boyz
):
    auswählen(dienst, "Boyz")
    einheitAufstellen(aufstellungNachDerZonenwahl, boyz)

    spielstand = spielstandVon(dienst)

    assert not aufstellungNachDerZonenwahl.ausgewählt(boyz)
    assert ausgewählteEinheitenIm(spielstand) == frozenset()
    assert ausgewählteModelleIm(spielstand) == frozenset()
    assert len(spielstand["modelle"]) == len(boyz.modelle)


def testAuf5_10DerSpielstandBehältDieAndereAusgewählteEinheitNachDemAufstellenAusgewählt(
    dienst, aufstellungNachDerZonenwahl, boyz
):
    auswählen(dienst, "Boyz")
    auswählen(dienst, "Warboss")
    einheitAufstellen(aufstellungNachDerZonenwahl, boyz)

    spielstand = spielstandVon(dienst)

    assert ausgewählteEinheitenIm(spielstand) == {"Warboss"}
    assert ausgewählteModelleIm(spielstand) == frozenset()


def testAuf5_6DieAntwortDesDienstesAufDieAuswahlGleichtDemBeispielDesVertrags(dienstDesBeispiels):
    auswählen(dienstDesBeispiels, "Warboss")

    antwort = auswählen(dienstDesBeispiels, "Necron Warriors")

    assert antwort.get_json() == spielstandDesVertrags()
    assert spielstandVon(dienstDesBeispiels) == spielstandDesVertrags()
