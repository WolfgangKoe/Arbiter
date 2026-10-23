"""AUF-25 · Modell per Klick auswählen."""

from http import HTTPStatus
from urllib.parse import urlparse

import pytest
from playwright.sync_api import expect

from tests.akzeptanz.auswahl import ausgewählteEinheiten, ausgewählteModelle
from tests.akzeptanz.bildschirm import seiteMitEingabe
from tests.akzeptanz.dienst import (
    auswählen,
    ebeneDesVertrags,
    ebenenIm,
    einheitAlsEbene,
    modellAlsEbene,
    spielstandDesVertrags,
    spielstandVon,
    stelleImSpielstand,
    stellenDerEinheitIm,
    stellenDesVertrags,
)
from tests.akzeptanz.handgriffe import stelleInDerZoneDesSpielersAnDerReihe, stelleInDerZoneVon
from tests.akzeptanz.ziehen import (
    aufDieEbeneWarten,
    klickenMit,
    liegtEinPixelGenauAn,
    mitDerMausKlicken,
    mitMausUndFinger,
    modellZiehen,
    punktAufDerKarte,
)


def zustandOhneEbene(aufstellung, einheit):
    return (
        aufstellung.ausgewählt(einheit),
        {modell: aufstellung.stelle(modell) for modell in einheit.modelle},
        aufstellung.einheitInAufstellung,
        aufstellung.anDerReihe,
    )


def ganzeEinheitDavor(aufstellung, anderes):
    """Davor ist die Ebene die ganze Einheit."""


def anderesModellDavor(aufstellung, anderes):
    aufstellung.ebeneWählen(anderes)


@pytest.fixture(
    params=[ganzeEinheitDavor, anderesModellDavor], ids=["ganzeEinheit", "anderesModell"]
)
def zweitesBoyzModellOhneEbene(request, aufstellungNachDerZonenwahl, boyzSetzen, boyz):
    """Die Boyz sind ausgewählt; das zweite Modell wird angeklickt."""
    [(erstes, _), (zweites, stelleZweites), _] = boyzSetzen(3)
    aufstellungNachDerZonenwahl.auswählen(boyz)
    request.param(aufstellungNachDerZonenwahl, erstes)
    return zweites, stelleZweites


def testAuf25_1EinKlickAufEinModellMachtEsZurEbeneGleichWasDavorWar(
    aufstellungNachDerZonenwahl, zweitesBoyzModellOhneEbene
):
    zweites, _ = zweitesBoyzModellOhneEbene

    aufstellungNachDerZonenwahl.ebeneWählen(zweites)

    assert aufstellungNachDerZonenwahl.modellIstEbene(zweites)


def testAuf25_1EinKlickAufEinModellNachDemSetzenPerKlickMachtEsZurEbene(
    aufstellungNachDerZonenwahl, spielerEins, boyz
):
    aufstellungNachDerZonenwahl.auswählen(boyz)
    klick = stelleInDerZoneVon(aufstellungNachDerZonenwahl, spielerEins, 4, 30)
    aufstellungNachDerZonenwahl.karteAnklicken(klick)
    *_, letztes = boyz.modelle

    aufstellungNachDerZonenwahl.ebeneWählen(letztes)

    assert aufstellungNachDerZonenwahl.modellIstEbene(letztes)


def testAuf25_1DerDienstGleichtNachDemKlickAufEinModellDemBeispielDesVertrags(
    dienstDesBeispiels, aufstellungDesBeispiels, necronWarriors
):
    auswählen(dienstDesBeispiels, "Necron Warriors")
    _, _, drittes, *_ = necronWarriors.modelle

    antwort = modellAlsEbene(dienstDesBeispiels, aufstellungDesBeispiels, necronWarriors, drittes)

    assert antwort.status_code == HTTPStatus.OK
    assert antwort.get_json() == ebeneDesVertrags()


@mitMausUndFinger
def testAuf25_1DieSeiteSendetBeimKlickAufEinModellOhneEbeneEinPutUndDieEbeneIstDasModell(
    bildschirm, aufstellungNachDerZonenwahl, zweitesBoyzModellOhneEbene, eingabe
):
    zweites, stelleZweites = zweitesBoyzModellOhneEbene
    seite = seiteMitEingabe(bildschirm, aufstellungNachDerZonenwahl, eingabe)

    with aufDieEbeneWarten(seite) as antwort:
        klickenMit[eingabe](seite, punktAufDerKarte(seite, stelleZweites))

    assert antwort.value.request.method == "PUT"
    assert antwort.value.status == HTTPStatus.OK
    assert aufstellungNachDerZonenwahl.modellIstEbene(zweites)


def testAuf25_1DieSeiteAdressiertImBeispielDesVertragsDasAngeklickteModell(
    bildschirm, ausgangsaufstellung
):
    spielstand = spielstandDesVertrags()
    _, _, stelleDesDritten, *_ = stellenDesVertrags(2)
    seite = bildschirm.seiteMitSpielstand(ausgangsaufstellung, spielstand)

    with aufDieEbeneWarten(seite) as antwort:
        mitDerMausKlicken(seite, punktAufDerKarte(seite, stelleDesDritten))

    anfrage = antwort.value.request
    assert (anfrage.method, urlparse(anfrage.url).path) == (
        "PUT",
        "/api/spieler/2/einheiten/1/modelle/3/ebene",
    )


@mitMausUndFinger
def testAuf25_1NachDemZiehenDerEinheitIstDieEbeneDieGanzeEinheit(
    bildschirm, aufstellungNachDerZonenwahl, boyzSetzen, boyz, eingabe
):
    [(_, stelleErstes), *_] = boyzSetzen(3)
    aufstellungNachDerZonenwahl.auswählen(boyz)
    ziel = stelleInDerZoneDesSpielersAnDerReihe(aufstellungNachDerZonenwahl, 4, 20)
    seite = seiteMitEingabe(bildschirm, aufstellungNachDerZonenwahl, eingabe)

    modellZiehen(seite, stelleErstes, ziel, eingabe)

    assert aufstellungNachDerZonenwahl.ganzeEinheitIstEbene(boyz)
    assert aufstellungNachDerZonenwahl.ausgewählt(boyz)


@mitMausUndFinger
def testAuf25_1NachDemZiehenDesModellsDasDieEbeneIstBleibtEsDieEbene(
    bildschirm, aufstellungNachDerZonenwahl, boyzSetzen, boyz, eingabe
):
    [(erstes, stelleErstes), *_] = boyzSetzen(3)
    aufstellungNachDerZonenwahl.auswählen(boyz)
    aufstellungNachDerZonenwahl.ebeneWählen(erstes)
    ziel = stelleInDerZoneDesSpielersAnDerReihe(aufstellungNachDerZonenwahl, 4, 20)
    seite = seiteMitEingabe(bildschirm, aufstellungNachDerZonenwahl, eingabe)

    modellZiehen(seite, stelleErstes, ziel, eingabe)

    assert liegtEinPixelGenauAn(seite, aufstellungNachDerZonenwahl.stelle(erstes), ziel)
    assert aufstellungNachDerZonenwahl.modellIstEbene(erstes)


def testAuf25_2EinKlickAufDasModellDerEbeneMachtWiederDieGanzeEinheitZurEbene(
    aufstellungNachDerZonenwahl, boyzSetzen, boyz
):
    [(erstes, _), *_] = boyzSetzen(3)
    aufstellungNachDerZonenwahl.auswählen(boyz)
    aufstellungNachDerZonenwahl.ebeneWählen(erstes)

    aufstellungNachDerZonenwahl.ebeneAbwählen(erstes)

    assert aufstellungNachDerZonenwahl.ganzeEinheitIstEbene(boyz)


def testAuf25_2EinZweiterKlickAufDasModellMachtDieGanzeEinheitZurEbeneAuchBeiAnderemModell(
    aufstellungNachDerZonenwahl, boyzSetzen, boyz
):
    [(erstes, _), (zweites, _), _] = boyzSetzen(3)
    aufstellungNachDerZonenwahl.auswählen(boyz)
    aufstellungNachDerZonenwahl.ebeneWählen(erstes)
    aufstellungNachDerZonenwahl.ebeneWählen(zweites)

    aufstellungNachDerZonenwahl.ebeneAbwählen(zweites)

    assert aufstellungNachDerZonenwahl.ganzeEinheitIstEbene(boyz)


def testAuf25_2DerDienstGleichtNachDemZweitenKlickDemBeispielVonV1(
    dienstDesBeispiels, aufstellungDesBeispiels, necronWarriors
):
    auswählen(dienstDesBeispiels, "Necron Warriors")
    _, _, drittes, *_ = necronWarriors.modelle
    modellAlsEbene(dienstDesBeispiels, aufstellungDesBeispiels, necronWarriors, drittes)

    antwort = einheitAlsEbene(dienstDesBeispiels, aufstellungDesBeispiels, necronWarriors, drittes)

    assert antwort.status_code == HTTPStatus.OK
    assert antwort.get_json() == spielstandDesVertrags()


@mitMausUndFinger
def testAuf25_2DieSeiteSendetBeimKlickAufDasModellDerEbeneEinDeleteUndDieEbeneIstDieEinheit(
    bildschirm, aufstellungNachDerZonenwahl, boyzSetzen, boyz, eingabe
):
    [(erstes, stelleErstes), *_] = boyzSetzen(3)
    aufstellungNachDerZonenwahl.auswählen(boyz)
    aufstellungNachDerZonenwahl.ebeneWählen(erstes)
    seite = seiteMitEingabe(bildschirm, aufstellungNachDerZonenwahl, eingabe)

    with aufDieEbeneWarten(seite) as antwort:
        klickenMit[eingabe](seite, punktAufDerKarte(seite, stelleErstes))

    assert antwort.value.request.method == "DELETE"
    assert antwort.value.status == HTTPStatus.OK
    assert aufstellungNachDerZonenwahl.ganzeEinheitIstEbene(boyz)


@mitMausUndFinger
def testAuf25_2DieSeiteKennzeichnetNachDemKlickAlleGesetztenModelleDerEinheit(
    bildschirm, aufstellungNachDerZonenwahl, boyzSetzen, boyz, eingabe
):
    gesetzte = boyzSetzen(3)
    [(erstes, stelleErstes), *_] = gesetzte
    aufstellungNachDerZonenwahl.auswählen(boyz)
    aufstellungNachDerZonenwahl.ebeneWählen(erstes)
    seite = seiteMitEingabe(bildschirm, aufstellungNachDerZonenwahl, eingabe)

    with aufDieEbeneWarten(seite):
        klickenMit[eingabe](seite, punktAufDerKarte(seite, stelleErstes))

    expect(seite.locator(".karte .modell.ausgewählt")).to_have_count(len(gesetzte))
    assert ausgewählteModelle(seite) == frozenset(
        stelleImSpielstand(stelle) for _, stelle in gesetzte
    )


def testAuf25_2DieSeiteAdressiertImBeispielMitEbeneDasModellDerEbene(
    bildschirm, ausgangsaufstellung
):
    spielstand = ebeneDesVertrags()
    _, _, stelleDesDritten, *_ = stellenDesVertrags(2)
    seite = bildschirm.seiteMitSpielstand(ausgangsaufstellung, spielstand)

    with aufDieEbeneWarten(seite) as antwort:
        mitDerMausKlicken(seite, punktAufDerKarte(seite, stelleDesDritten))

    anfrage = antwort.value.request
    assert (anfrage.method, urlparse(anfrage.url).path) == (
        "DELETE",
        "/api/spieler/2/einheiten/1/modelle/3/ebene",
    )


def testAuf25_3DasWählenDerEbeneÄndertAuswahlModelleEinheitInAufstellungUndReihenfolgeNicht(
    aufstellungNachDerZonenwahl, boyzSetzen, boyz
):
    [(erstes, _), *_] = boyzSetzen(3)
    aufstellungNachDerZonenwahl.auswählen(boyz)
    zustandDavor = zustandOhneEbene(aufstellungNachDerZonenwahl, boyz)

    aufstellungNachDerZonenwahl.ebeneWählen(erstes)

    assert zustandOhneEbene(aufstellungNachDerZonenwahl, boyz) == zustandDavor


def testAuf25_3DasAbwählenDerEbeneÄndertAuswahlModelleEinheitInAufstellungUndReihenfolgeNicht(
    aufstellungNachDerZonenwahl, boyzSetzen, boyz
):
    [(erstes, _), *_] = boyzSetzen(3)
    aufstellungNachDerZonenwahl.auswählen(boyz)
    aufstellungNachDerZonenwahl.ebeneWählen(erstes)
    zustandDavor = zustandOhneEbene(aufstellungNachDerZonenwahl, boyz)

    aufstellungNachDerZonenwahl.ebeneAbwählen(erstes)

    assert zustandOhneEbene(aufstellungNachDerZonenwahl, boyz) == zustandDavor


def testAuf25_3DerDienstLässtBeimWählenDerEbeneArmeelistenStellenUndReiheGleich(
    dienst, aufstellungNachDerZonenwahl, boyzSetzen, boyz
):
    [(erstes, _), *_] = boyzSetzen(3)
    auswählen(dienst, "Boyz")
    davor = spielstandVon(dienst)

    antwort = modellAlsEbene(dienst, aufstellungNachDerZonenwahl, boyz, erstes)

    danach = antwort.get_json()
    assert antwort.status_code == HTTPStatus.OK
    assert danach["spieler"] == davor["spieler"]
    assert stellenDerEinheitIm(danach, "Boyz") == stellenDerEinheitIm(davor, "Boyz")
    assert len(danach["modelle"]) == len(davor["modelle"])


@mitMausUndFinger
def testAuf25_3DieSeiteLässtBeimKlickAufEinModellDieEinheitAusgewähltUndDieModelleStehen(
    bildschirm, aufstellungNachDerZonenwahl, boyzSetzen, boyz, eingabe
):
    [(erstes, stelleErstes), *_] = boyzSetzen(3)
    aufstellungNachDerZonenwahl.auswählen(boyz)
    zustandDavor = zustandOhneEbene(aufstellungNachDerZonenwahl, boyz)
    seite = seiteMitEingabe(bildschirm, aufstellungNachDerZonenwahl, eingabe)

    with aufDieEbeneWarten(seite):
        klickenMit[eingabe](seite, punktAufDerKarte(seite, stelleErstes))

    expect(seite.locator(".karte .modell.ausgewählt")).to_have_count(1)
    assert ausgewählteEinheiten(seite) == {"Boyz"}
    assert zustandOhneEbene(aufstellungNachDerZonenwahl, boyz) == zustandDavor
    assert aufstellungNachDerZonenwahl.modellIstEbene(erstes)


def testAuf25_4IstDieEbeneEinModellIstNurDiesesModellAusgewählt(
    aufstellungNachDerZonenwahl, boyzSetzen, boyz
):
    [(erstes, _), (zweites, _), (drittes, _)] = boyzSetzen(3)
    aufstellungNachDerZonenwahl.auswählen(boyz)

    aufstellungNachDerZonenwahl.ebeneWählen(zweites)

    assert not aufstellungNachDerZonenwahl.modellAusgewählt(erstes)
    assert aufstellungNachDerZonenwahl.modellAusgewählt(zweites)
    assert not aufstellungNachDerZonenwahl.modellAusgewählt(drittes)


def testAuf25_4DerDienstKennzeichnetNurDasModellDerEbene(
    dienstDesBeispiels, aufstellungDesBeispiels, necronWarriors
):
    auswählen(dienstDesBeispiels, "Necron Warriors")
    _, _, drittes, *_ = necronWarriors.modelle

    antwort = modellAlsEbene(dienstDesBeispiels, aufstellungDesBeispiels, necronWarriors, drittes)

    stelleDesDritten = aufstellungDesBeispiels.stelle(drittes)
    assert ebenenIm(antwort.get_json()) == {stelleImSpielstand(stelleDesDritten)}


def testAuf25_4DieKarteKennzeichnetImBeispielDesVertragsNurDasModellDerEbene(
    bildschirm, ausgangsaufstellung
):
    spielstand = ebeneDesVertrags()
    _, _, stelleDesDritten, *_ = stellenDesVertrags(2)

    seite = bildschirm.seiteMitSpielstand(ausgangsaufstellung, spielstand)

    assert ausgewählteModelle(seite) == {stelleImSpielstand(stelleDesDritten)}
    assert ebenenIm(spielstand) == {stelleImSpielstand(stelleDesDritten)}


@mitMausUndFinger
def testAuf25_4DieKarteKennzeichnetNachDemKlickNurDasAngeklickteModell(
    bildschirm, aufstellungNachDerZonenwahl, boyzSetzen, boyz, eingabe
):
    [_, (_, stelleZweites), _] = boyzSetzen(3)
    aufstellungNachDerZonenwahl.auswählen(boyz)
    seite = seiteMitEingabe(bildschirm, aufstellungNachDerZonenwahl, eingabe)

    with aufDieEbeneWarten(seite):
        klickenMit[eingabe](seite, punktAufDerKarte(seite, stelleZweites))

    expect(seite.locator(".karte .modell.ausgewählt")).to_have_count(1)
    assert ausgewählteModelle(seite) == {stelleImSpielstand(stelleZweites)}
