"""AUF-25 · Modell per Klick auswählen."""

from http import HTTPStatus
from urllib.parse import urlparse

import pytest
from playwright.sync_api import expect

from tests.akzeptanz.auswahl import ausgewählteEinheiten, ausgewählteModelle
from tests.akzeptanz.bildschirm import seiteMitEingabe
from tests.akzeptanz.dienst import (
    auswählen,
    imUmfangDes,
    modellAnklicken,
    modellebeneDesVertrags,
    modellebenenIm,
    spielstandDesVertrags,
    spielstandVon,
    stelleImSpielstand,
    stellenDerEinheitIm,
    stellenDesVertrags,
)
from tests.akzeptanz.handgriffe import (
    modellebeneWählen,
    stelleInDerZoneDesSpielersAnDerReihe,
    stelleInDerZoneVon,
)
from tests.akzeptanz.ziehen import (
    aufDasAnklickenWarten,
    klickenMit,
    liegtEinPixelGenauAn,
    mitDerMausKlicken,
    mitMausUndFinger,
    modellZiehen,
    punktAufDemSpielfeld,
)


def zustandOhneEbene(aufstellung, einheit):
    return (
        aufstellung.ausgewählt(einheit),
        {modell: aufstellung.stelle(modell) for modell in einheit.modelle},
        aufstellung.einheitInAufstellung,
        aufstellung.anDerReihe,
    )


def ganzeEinheitDavor(aufstellung, anderes): ...


def anderesModellDavor(aufstellung, anderes):
    aufstellung.modellAnklicken(anderes)


@pytest.fixture(
    params=[ganzeEinheitDavor, anderesModellDavor], ids=["ganzeEinheit", "anderesModell"]
)
def zweitesBoyzModellOhneModellebene(request, aufstellungNachDerZonenwahl, boyzSetzen, boyz):
    [(erstes, _), (zweites, stelleZweites), _] = boyzSetzen(3)
    aufstellungNachDerZonenwahl.auswählen(boyz)
    request.param(aufstellungNachDerZonenwahl, erstes)
    return zweites, stelleZweites


def testAuf25_1EinKlickAufEinModellMachtSeineModellebeneZurEbeneGleichWasDavorWar(
    aufstellungNachDerZonenwahl, zweitesBoyzModellOhneModellebene
):
    zweites, _ = zweitesBoyzModellOhneModellebene

    aufstellungNachDerZonenwahl.modellAnklicken(zweites)

    assert aufstellungNachDerZonenwahl.istModellebene(zweites)


def testAuf25_1EinKlickAufEinModellNachDemSetzenPerKlickMachtSeineModellebeneZurEbene(
    aufstellungNachDerZonenwahl, spielerEins, boyz
):
    aufstellungNachDerZonenwahl.auswählen(boyz)
    klick = stelleInDerZoneVon(aufstellungNachDerZonenwahl, spielerEins, 4, 30)
    aufstellungNachDerZonenwahl.spielfeldAnklicken(klick)
    *_, letztes = boyz.modelle

    aufstellungNachDerZonenwahl.modellAnklicken(letztes)

    assert aufstellungNachDerZonenwahl.istModellebene(letztes)


def testAuf25_1DerDienstGleichtNachDemKlickAufEinModellDemBeispielDesVertrags(
    dienstDesBeispiels, aufstellungDesBeispiels, necronWarriors
):
    auswählen(dienstDesBeispiels, "Necron Warriors")
    _, _, drittes, *_ = necronWarriors.modelle

    antwort = modellAnklicken(dienstDesBeispiels, aufstellungDesBeispiels, necronWarriors, drittes)

    assert antwort.status_code == HTTPStatus.OK
    beispiel = modellebeneDesVertrags()
    assert imUmfangDes(beispiel, antwort.get_json()) == beispiel


@mitMausUndFinger
def testAuf25_1DieSeiteSendetBeimKlickAufEinModellOhneModellebeneEinPutUndDieEbeneIstSeineModellebene(  # noqa: E501
    bildschirm, aufstellungNachDerZonenwahl, zweitesBoyzModellOhneModellebene, eingabe
):
    zweites, stelleZweites = zweitesBoyzModellOhneModellebene
    seite = seiteMitEingabe(bildschirm, aufstellungNachDerZonenwahl, eingabe)

    with aufDasAnklickenWarten(seite) as antwort:
        klickenMit[eingabe](seite, punktAufDemSpielfeld(seite, stelleZweites))

    assert antwort.value.request.method == "PUT"
    assert antwort.value.status == HTTPStatus.OK
    assert aufstellungNachDerZonenwahl.istModellebene(zweites)


def testAuf25_1DieSeiteAdressiertImBeispielDesVertragsDasAngeklickteModell(
    bildschirm, ausgangsaufstellung
):
    spielstand = spielstandDesVertrags()
    _, _, stelleDesDritten, *_ = stellenDesVertrags(2)
    seite = bildschirm.seiteMitSpielstand(ausgangsaufstellung, spielstand)

    with aufDasAnklickenWarten(seite) as antwort:
        mitDerMausKlicken(seite, punktAufDemSpielfeld(seite, stelleDesDritten))

    anfrage = antwort.value.request
    assert (anfrage.method, urlparse(anfrage.url).path) == (
        "PUT",
        "/api/spieler/2/einheiten/1/modelle/3/anklicken",
    )


@mitMausUndFinger
def testAuf25_1NachDemZiehenDerEinheitIstDieEbeneDieEinheitenebene(
    bildschirm, aufstellungNachDerZonenwahl, boyzSetzen, boyz, eingabe
):
    [(_, stelleErstes), *_] = boyzSetzen(3)
    aufstellungNachDerZonenwahl.auswählen(boyz)
    ziel = stelleInDerZoneDesSpielersAnDerReihe(aufstellungNachDerZonenwahl, 4, 20)
    seite = seiteMitEingabe(bildschirm, aufstellungNachDerZonenwahl, eingabe)

    modellZiehen(seite, stelleErstes, ziel, eingabe)

    assert aufstellungNachDerZonenwahl.hatEinheitenebene(boyz)
    assert aufstellungNachDerZonenwahl.ausgewählt(boyz)


@mitMausUndFinger
def testAuf25_1NachDemZiehenDesModellsDerModellebeneBleibtSieDieEbene(
    bildschirm, aufstellungNachDerZonenwahl, boyzSetzen, boyz, eingabe
):
    [(erstes, stelleErstes), *_] = boyzSetzen(3)
    modellebeneWählen(aufstellungNachDerZonenwahl, boyz, erstes)
    ziel = stelleInDerZoneDesSpielersAnDerReihe(aufstellungNachDerZonenwahl, 4, 20)
    seite = seiteMitEingabe(bildschirm, aufstellungNachDerZonenwahl, eingabe)

    modellZiehen(seite, stelleErstes, ziel, eingabe)

    assert liegtEinPixelGenauAn(seite, aufstellungNachDerZonenwahl.stelle(erstes), ziel)
    assert aufstellungNachDerZonenwahl.istModellebene(erstes)


def testAuf25_2EinKlickAufDasModellDerModellebeneMachtWiederDieEinheitenebeneZurEbene(
    aufstellungNachDerZonenwahl, boyzSetzen, boyz
):
    [(erstes, _), *_] = boyzSetzen(3)
    modellebeneWählen(aufstellungNachDerZonenwahl, boyz, erstes)

    aufstellungNachDerZonenwahl.modellAnklicken(erstes)

    assert aufstellungNachDerZonenwahl.hatEinheitenebene(boyz)


def testAuf25_2EinZweiterKlickAufDasModellMachtDieEinheitenebeneZurEbeneAuchBeiAnderemModell(
    aufstellungNachDerZonenwahl, boyzSetzen, boyz
):
    [(erstes, _), (zweites, _), _] = boyzSetzen(3)
    modellebeneWählen(aufstellungNachDerZonenwahl, boyz, erstes)
    aufstellungNachDerZonenwahl.modellAnklicken(zweites)

    aufstellungNachDerZonenwahl.modellAnklicken(zweites)

    assert aufstellungNachDerZonenwahl.hatEinheitenebene(boyz)


def testAuf25_2DerDienstGleichtNachDemZweitenKlickDemBeispielVonV1(
    dienstDesBeispiels, aufstellungDesBeispiels, necronWarriors
):
    auswählen(dienstDesBeispiels, "Necron Warriors")
    _, _, drittes, *_ = necronWarriors.modelle
    mitModellebene = modellAnklicken(
        dienstDesBeispiels, aufstellungDesBeispiels, necronWarriors, drittes
    )

    antwort = modellAnklicken(dienstDesBeispiels, aufstellungDesBeispiels, necronWarriors, drittes)

    assert len(modellebenenIm(mitModellebene.get_json())) == 1
    assert antwort.status_code == HTTPStatus.OK
    beispiel = spielstandDesVertrags()
    assert imUmfangDes(beispiel, antwort.get_json()) == beispiel


@mitMausUndFinger
def testAuf25_2DieSeiteSendetBeimKlickAufDasModellDerModellebeneEinPutUndDieEbeneIstDieEinheitenebene(  # noqa: E501
    bildschirm, aufstellungNachDerZonenwahl, boyzSetzen, boyz, eingabe
):
    [(erstes, stelleErstes), *_] = boyzSetzen(3)
    modellebeneWählen(aufstellungNachDerZonenwahl, boyz, erstes)
    seite = seiteMitEingabe(bildschirm, aufstellungNachDerZonenwahl, eingabe)

    with aufDasAnklickenWarten(seite) as antwort:
        klickenMit[eingabe](seite, punktAufDemSpielfeld(seite, stelleErstes))

    assert antwort.value.request.method == "PUT"
    assert antwort.value.status == HTTPStatus.OK
    assert aufstellungNachDerZonenwahl.hatEinheitenebene(boyz)


@mitMausUndFinger
def testAuf25_2DieSeiteKennzeichnetNachDemKlickAlleGesetztenModelleDerEinheit(
    bildschirm, aufstellungNachDerZonenwahl, boyzSetzen, boyz, eingabe
):
    gesetzte = boyzSetzen(3)
    [(erstes, stelleErstes), *_] = gesetzte
    modellebeneWählen(aufstellungNachDerZonenwahl, boyz, erstes)
    seite = seiteMitEingabe(bildschirm, aufstellungNachDerZonenwahl, eingabe)

    with aufDasAnklickenWarten(seite):
        klickenMit[eingabe](seite, punktAufDemSpielfeld(seite, stelleErstes))

    expect(seite.locator(".spielfeld .modell.ausgewählt")).to_have_count(len(gesetzte))
    assert ausgewählteModelle(seite) == frozenset(
        stelleImSpielstand(stelle) for _, stelle in gesetzte
    )


def testAuf25_2DieSeiteAdressiertImBeispielMitModellebeneDasModellDerModellebene(
    bildschirm, ausgangsaufstellung
):
    spielstand = modellebeneDesVertrags()
    _, _, stelleDesDritten, *_ = stellenDesVertrags(2)
    seite = bildschirm.seiteMitSpielstand(ausgangsaufstellung, spielstand)

    with aufDasAnklickenWarten(seite) as antwort:
        mitDerMausKlicken(seite, punktAufDemSpielfeld(seite, stelleDesDritten))

    anfrage = antwort.value.request
    assert (anfrage.method, urlparse(anfrage.url).path) == (
        "PUT",
        "/api/spieler/2/einheiten/1/modelle/3/anklicken",
    )


def testAuf25_3DasWählenDerEbeneÄndertAuswahlModelleEinheitInAufstellungUndReihenfolgeNicht(
    aufstellungNachDerZonenwahl, boyzSetzen, boyz
):
    [(erstes, _), *_] = boyzSetzen(3)
    aufstellungNachDerZonenwahl.auswählen(boyz)
    zustandDavor = zustandOhneEbene(aufstellungNachDerZonenwahl, boyz)

    aufstellungNachDerZonenwahl.modellAnklicken(erstes)

    assert zustandOhneEbene(aufstellungNachDerZonenwahl, boyz) == zustandDavor


def testAuf25_3DasAbwählenDerEbeneÄndertAuswahlModelleEinheitInAufstellungUndReihenfolgeNicht(
    aufstellungNachDerZonenwahl, boyzSetzen, boyz
):
    [(erstes, _), *_] = boyzSetzen(3)
    modellebeneWählen(aufstellungNachDerZonenwahl, boyz, erstes)
    zustandDavor = zustandOhneEbene(aufstellungNachDerZonenwahl, boyz)

    aufstellungNachDerZonenwahl.modellAnklicken(erstes)

    assert zustandOhneEbene(aufstellungNachDerZonenwahl, boyz) == zustandDavor


def testAuf25_3DerDienstLässtBeimWählenDerEbeneArmeelistenStellenUndReiheGleich(
    dienst, aufstellungNachDerZonenwahl, boyzSetzen, boyz
):
    [(erstes, _), *_] = boyzSetzen(3)
    auswählen(dienst, "Boyz")
    davor = spielstandVon(dienst)

    antwort = modellAnklicken(dienst, aufstellungNachDerZonenwahl, boyz, erstes)

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

    with aufDasAnklickenWarten(seite):
        klickenMit[eingabe](seite, punktAufDemSpielfeld(seite, stelleErstes))

    expect(seite.locator(".spielfeld .modell.ausgewählt")).to_have_count(1)
    assert ausgewählteEinheiten(seite) == {"Boyz"}
    assert zustandOhneEbene(aufstellungNachDerZonenwahl, boyz) == zustandDavor
    assert aufstellungNachDerZonenwahl.istModellebene(erstes)


def testAuf25_4IstDieEbeneEineModellebeneIstNurDiesesModellAusgewählt(
    aufstellungNachDerZonenwahl, boyzSetzen, boyz
):
    [(erstes, _), (zweites, _), (drittes, _)] = boyzSetzen(3)
    aufstellungNachDerZonenwahl.auswählen(boyz)

    aufstellungNachDerZonenwahl.modellAnklicken(zweites)

    assert not aufstellungNachDerZonenwahl.modellAusgewählt(erstes)
    assert aufstellungNachDerZonenwahl.modellAusgewählt(zweites)
    assert not aufstellungNachDerZonenwahl.modellAusgewählt(drittes)


def testAuf25_4DerDienstKennzeichnetNurDasModellDerModellebene(
    dienstDesBeispiels, aufstellungDesBeispiels, necronWarriors
):
    auswählen(dienstDesBeispiels, "Necron Warriors")
    _, _, drittes, *_ = necronWarriors.modelle

    antwort = modellAnklicken(dienstDesBeispiels, aufstellungDesBeispiels, necronWarriors, drittes)

    stelleDesDritten = aufstellungDesBeispiels.stelle(drittes)
    assert modellebenenIm(antwort.get_json()) == {stelleImSpielstand(stelleDesDritten)}


def testAuf25_4DasSpielfeldKennzeichnetImBeispielDesVertragsNurDasModellDerModellebene(
    bildschirm, ausgangsaufstellung
):
    spielstand = modellebeneDesVertrags()
    _, _, stelleDesDritten, *_ = stellenDesVertrags(2)

    seite = bildschirm.seiteMitSpielstand(ausgangsaufstellung, spielstand)

    assert ausgewählteModelle(seite) == {stelleImSpielstand(stelleDesDritten)}
    assert modellebenenIm(spielstand) == {stelleImSpielstand(stelleDesDritten)}


@mitMausUndFinger
def testAuf25_4DasSpielfeldKennzeichnetNachDemKlickNurDasAngeklickteModell(
    bildschirm, aufstellungNachDerZonenwahl, boyzSetzen, boyz, eingabe
):
    [_, (_, stelleZweites), _] = boyzSetzen(3)
    aufstellungNachDerZonenwahl.auswählen(boyz)
    seite = seiteMitEingabe(bildschirm, aufstellungNachDerZonenwahl, eingabe)

    with aufDasAnklickenWarten(seite):
        klickenMit[eingabe](seite, punktAufDemSpielfeld(seite, stelleZweites))

    expect(seite.locator(".spielfeld .modell.ausgewählt")).to_have_count(1)
    assert ausgewählteModelle(seite) == {stelleImSpielstand(stelleZweites)}
