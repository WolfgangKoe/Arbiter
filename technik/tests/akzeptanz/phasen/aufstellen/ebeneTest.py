"""AUF-20 · Ganze Einheit oder ein Modell."""

from http import HTTPStatus

import pytest
from playwright.sync_api import expect

from tests.akzeptanz.auswahl import (
    ausgewählteEinheiten,
    ausgewählteModelle,
    auswählenMit,
)
from tests.akzeptanz.bildschirm import (
    aufDieHandlungWarten,
    seiteDerSchlachtMitEingabe,
    seiteMitEingabe,
)
from tests.akzeptanz.dienst import (
    ausgewählteEinheitenIm,
    ausgewählteModelleIm,
    auswählen,
    ebenenIm,
    karteAnklicken,
    modellAnklicken,
    modellLoslassen,
    spielstandVon,
    stelleImSpielstand,
    stellenDerEinheitIm,
)
from tests.akzeptanz.handgriffe import modellZurEbeneMachen, stelleInDerZoneVon
from tests.akzeptanz.schlacht import stellenDerEinheitAlsZahlen
from tests.akzeptanz.ziehen import (
    klickenMit,
    liegtEinPixelGenauAn,
    mitMausUndFinger,
    modellZiehen,
    punktAufDerKarte,
)

mitteDerZone = 4
längsDerZone = 30
nummerDesGezogenen = 1


def nichtAuswählen(aufstellung, einheit, modell): ...


@pytest.fixture(
    params=[nichtAuswählen, modellZurEbeneMachen], ids=["nichtAusgewählt", "ebeneIstEinModell"]
)
def dreiBoyzNachDerVorgeschichte(request, aufstellungNachDerZonenwahl, boyz, boyzSetzen):
    gesetzte = boyzSetzen(3)
    [(gezogenes, _), *_] = gesetzte
    request.param(aufstellungNachDerZonenwahl, boyz, gezogenes)
    return gesetzte


def testAuf20_2DieEbeneEinerAusgewähltenEinheitIstDieGanzeEinheit(
    aufstellungNachDerZonenwahl, boyz
):
    aufstellungNachDerZonenwahl.auswählen(boyz)

    assert aufstellungNachDerZonenwahl.ganzeEinheitIstEbene(boyz)


def testAuf20_2WiederAusgewähltIstDieEbeneDieGanzeEinheitAuchNachEinemModell(
    aufstellungNachDerZonenwahl, boyzSetzen, boyz, warboss
):
    [(modell, _), *_] = boyzSetzen(3)
    modellZurEbeneMachen(aufstellungNachDerZonenwahl, boyz, modell)
    aufstellungNachDerZonenwahl.auswählen(warboss)

    aufstellungNachDerZonenwahl.auswählen(boyz)

    assert aufstellungNachDerZonenwahl.ganzeEinheitIstEbene(boyz)


def testAuf20_2DerDienstKennzeichnetNachDemWiederAuswählenKeinModellAlsEbene(
    dienst, aufstellungNachDerZonenwahl, boyzSetzen, boyz
):
    [(modell, _), *_] = boyzSetzen(3)
    auswählen(dienst, "Boyz")
    mitEbene = modellAnklicken(dienst, aufstellungNachDerZonenwahl, boyz, modell)
    auswählen(dienst, "Warboss")

    antwort = auswählen(dienst, "Boyz")

    assert len(ebenenIm(mitEbene.get_json())) == 1
    assert ausgewählteEinheitenIm(antwort.get_json()) == {"Boyz"}
    assert ebenenIm(antwort.get_json()) == frozenset()


@mitMausUndFinger
def testAuf20_2DieSeiteKennzeichnetNachDemAuswählenAlleGesetztenModelleDerEinheit(
    bildschirm, aufstellungNachDerZonenwahl, boyzSetzen, boyz, eingabe
):
    gesetzte = boyzSetzen(3)
    [(modell, _), *_] = gesetzte
    modellZurEbeneMachen(aufstellungNachDerZonenwahl, boyz, modell)
    aufstellungNachDerZonenwahl.abwählen(boyz)
    seite = seiteMitEingabe(bildschirm, aufstellungNachDerZonenwahl, eingabe)

    auswählenMit[eingabe](seite, "Spieler 1", "Boyz")

    expect(seite.locator(".karte .modell.ausgewählt")).to_have_count(len(gesetzte))
    assert ausgewählteModelle(seite) == frozenset(
        stelleImSpielstand(stelle) for _, stelle in gesetzte
    )


def testAuf20_4ZiehenEinesModellsOhneEbeneEinheitLässtDieAnderenModelleStehen(
    aufstellungNachDerZonenwahl, spielerEins, dreiBoyzNachDerVorgeschichte
):
    [(gezogenes, stelleDavor), (zweites, stelleZweites), (drittes, stelleDrittes)] = (
        dreiBoyzNachDerVorgeschichte
    )
    ziel = stelleInDerZoneVon(aufstellungNachDerZonenwahl, spielerEins, 4, 20)

    aufstellungNachDerZonenwahl.modellLoslassen(gezogenes, ziel)

    assert ziel != stelleDavor
    assert aufstellungNachDerZonenwahl.stelle(gezogenes) == ziel
    assert aufstellungNachDerZonenwahl.stelle(zweites) == stelleZweites
    assert aufstellungNachDerZonenwahl.stelle(drittes) == stelleDrittes


def testAuf20_4ZiehenEinesAnderenModellsAlsDerEbeneLässtAuchDieEbeneStehen(
    aufstellungNachDerZonenwahl, spielerEins, boyz, boyzSetzen
):
    [(modellDerEbene, stelleDerEbene), (gezogenes, _), (drittes, stelleDrittes)] = boyzSetzen(3)
    modellZurEbeneMachen(aufstellungNachDerZonenwahl, boyz, modellDerEbene)
    ziel = stelleInDerZoneVon(aufstellungNachDerZonenwahl, spielerEins, 4, 20)

    aufstellungNachDerZonenwahl.modellLoslassen(gezogenes, ziel)

    assert aufstellungNachDerZonenwahl.stelle(gezogenes) == ziel
    assert aufstellungNachDerZonenwahl.stelle(modellDerEbene) == stelleDerEbene
    assert aufstellungNachDerZonenwahl.stelle(drittes) == stelleDrittes


def testAuf20_4DerDienstVerschiebtNurDasGezogeneModell(
    dienst, aufstellungNachDerZonenwahl, boyz, dreiBoyzNachDerVorgeschichte
):
    [(gezogenes, _), *_] = dreiBoyzNachDerVorgeschichte
    davor = stellenDerEinheitIm(spielstandVon(dienst), "Boyz")
    spieler = aufstellungNachDerZonenwahl.anDerReihe
    ziel = stelleInDerZoneVon(aufstellungNachDerZonenwahl, spieler, 4, 20)

    antwort = modellLoslassen(dienst, aufstellungNachDerZonenwahl, boyz, gezogenes, ziel)

    danach = stellenDerEinheitIm(antwort.get_json(), "Boyz")
    übrigeDavor = {
        nummer: stelle for nummer, stelle in davor.items() if nummer != nummerDesGezogenen
    }
    übrigeDanach = {
        nummer: stelle for nummer, stelle in danach.items() if nummer != nummerDesGezogenen
    }
    assert antwort.status_code == HTTPStatus.OK
    assert danach[nummerDesGezogenen] != davor[nummerDesGezogenen]
    assert danach[nummerDesGezogenen] == stelleImSpielstand(ziel)
    assert übrigeDanach == übrigeDavor


@mitMausUndFinger
def testAuf20_4DieSeiteZiehtNurDasGezogeneModell(
    bildschirm, aufstellungNachDerZonenwahl, dreiBoyzNachDerVorgeschichte, eingabe
):
    [(gezogenes, stelleDavor), (zweites, stelleZweites), (drittes, stelleDrittes)] = (
        dreiBoyzNachDerVorgeschichte
    )
    spieler = aufstellungNachDerZonenwahl.anDerReihe
    ziel = stelleInDerZoneVon(aufstellungNachDerZonenwahl, spieler, 4, 20)
    seite = seiteMitEingabe(bildschirm, aufstellungNachDerZonenwahl, eingabe)

    modellZiehen(seite, stelleDavor, ziel, eingabe)

    assert liegtEinPixelGenauAn(seite, aufstellungNachDerZonenwahl.stelle(gezogenes), ziel)
    assert aufstellungNachDerZonenwahl.stelle(zweites) == stelleZweites
    assert aufstellungNachDerZonenwahl.stelle(drittes) == stelleDrittes


def testAuf20_5NachDemSetzenDerFormationBleibtDieEinheitAusgewähltMitIhrerEbene(
    aufstellungNachDerZonenwahl, spielerEins, boyz
):
    aufstellungNachDerZonenwahl.auswählen(boyz)
    klick = stelleInDerZoneVon(aufstellungNachDerZonenwahl, spielerEins, mitteDerZone, längsDerZone)

    aufstellungNachDerZonenwahl.karteAnklicken(klick)

    assert aufstellungNachDerZonenwahl.ausgewählt(boyz)
    assert aufstellungNachDerZonenwahl.ganzeEinheitIstEbene(boyz)
    assert all(aufstellungNachDerZonenwahl.modellAusgewählt(modell) for modell in boyz.modelle)


def testAuf20_5DerDienstLässtNachDemSetzenDieEinheitAusgewähltOhneModellAlsEbene(
    dienst, aufstellungNachDerZonenwahl, spielerEins, boyz
):
    auswählen(dienst, "Boyz")
    klick = stelleInDerZoneVon(aufstellungNachDerZonenwahl, spielerEins, mitteDerZone, längsDerZone)

    antwort = karteAnklicken(dienst, klick)

    spielstand = antwort.get_json()
    assert antwort.status_code == HTTPStatus.OK
    assert ausgewählteEinheitenIm(spielstand) == {"Boyz"}
    assert len(ausgewählteModelleIm(spielstand)) == len(boyz.modelle)
    assert ebenenIm(spielstand) == frozenset()


@mitMausUndFinger
def testAuf20_5DieSeiteZeigtNachDemSetzenDieEinheitUndAlleIhreModelleAusgewählt(
    bildschirm, aufstellungNachDerZonenwahl, spielerEins, boyz, eingabe
):
    seite = seiteMitEingabe(bildschirm, aufstellungNachDerZonenwahl, eingabe)
    auswählenMit[eingabe](seite, "Spieler 1", "Boyz")
    klick = stelleInDerZoneVon(aufstellungNachDerZonenwahl, spielerEins, mitteDerZone, längsDerZone)

    with aufDieHandlungWarten(seite):
        klickenMit[eingabe](seite, punktAufDerKarte(seite, klick))

    expect(seite.locator(".karte .modell.ausgewählt")).to_have_count(len(boyz.modelle))
    assert ausgewählteEinheiten(seite) == {"Boyz"}


def testAuf20_6EinKlickAufEinModellWähltSeineEinheitMitDerGanzenEinheitAlsEbene(
    schlachtInDerBewegungsphase, einheitJederSeite
):
    angeklickt, *_ = einheitJederSeite.modelle

    schlachtInDerBewegungsphase.modellAnklicken(angeklickt)

    assert schlachtInDerBewegungsphase.ausgewählt(einheitJederSeite)
    assert schlachtInDerBewegungsphase.ganzeEinheitIstEbene(einheitJederSeite)


def testAuf20_6EinKlickAufEinModellWähltKeineAndereEinheit(
    schlachtInDerBewegungsphase, boyz, warboss
):
    schlachtInDerBewegungsphase.auswählen(warboss)
    angeklickt, *_ = boyz.modelle

    schlachtInDerBewegungsphase.modellAnklicken(angeklickt)

    assert schlachtInDerBewegungsphase.ausgewählt(boyz)
    assert not schlachtInDerBewegungsphase.ausgewählt(warboss)


def testAuf20_6EinKlickAufEinGesetztesModellInDerAufstellungWähltDieGanzeEinheit(
    aufstellungNachDerZonenwahl, boyzSetzen, boyz
):
    [(angeklickt, _), *_] = boyzSetzen(3)

    aufstellungNachDerZonenwahl.modellAnklicken(angeklickt)

    assert aufstellungNachDerZonenwahl.ausgewählt(boyz)
    assert aufstellungNachDerZonenwahl.ganzeEinheitIstEbene(boyz)


def testAuf20_6EinKlickAufEinGesetztesModellInDerAufstellungWähltKeineAndereEinheit(
    aufstellungNachDerZonenwahl, boyzSetzen, boyz, warboss
):
    [(angeklickt, _), *_] = boyzSetzen(3)
    aufstellungNachDerZonenwahl.auswählen(warboss)

    aufstellungNachDerZonenwahl.modellAnklicken(angeklickt)

    assert aufstellungNachDerZonenwahl.ausgewählt(boyz)
    assert not aufstellungNachDerZonenwahl.ausgewählt(warboss)


@pytest.fixture(
    params=["boyz", "necronWarriors"],
    ids=["einheitDesSpielersAnDerReihe", "einheitDesAnderenSpielers"],
)
def aufgestellteEinheitJederSeite(request):
    return request.getfixturevalue(request.param)


def testAuf20_6EinKlickInDerAufstellungWähltDieGanzeEinheitGleichWerAnDerReiheIst(
    aufstellungMitModellenBeiderSpieler, aufgestellteEinheitJederSeite
):
    angeklickt, *_ = aufgestellteEinheitJederSeite.modelle

    aufstellungMitModellenBeiderSpieler.modellAnklicken(angeklickt)

    assert aufstellungMitModellenBeiderSpieler.ausgewählt(aufgestellteEinheitJederSeite)
    assert aufstellungMitModellenBeiderSpieler.ganzeEinheitIstEbene(aufgestellteEinheitJederSeite)


def testAuf20_6DerDienstWähltBeimAnklickenEinesModellsInDerSchlachtDieGanzeEinheitAlsEbene(
    dienstDerSchlacht, beendeteAufstellung, schlachtInDerBewegungsphase, einheitJederSeite
):
    angeklickt, *_ = einheitJederSeite.modelle

    antwort = modellAnklicken(dienstDerSchlacht, beendeteAufstellung, einheitJederSeite, angeklickt)

    spielstand = antwort.get_json()
    assert antwort.status_code == HTTPStatus.OK
    assert ausgewählteModelleIm(spielstand) == stellenDerEinheitAlsZahlen(
        schlachtInDerBewegungsphase, einheitJederSeite
    )
    assert ebenenIm(spielstand) == frozenset()


def testAuf20_6DerDienstWähltBeimAnklickenEinesModellsKeineAndereEinheit(
    dienstDerSchlacht, beendeteAufstellung, schlachtInDerBewegungsphase, boyz, warboss
):
    schlachtInDerBewegungsphase.auswählen(warboss)
    angeklickt, *_ = boyz.modelle

    antwort = modellAnklicken(dienstDerSchlacht, beendeteAufstellung, boyz, angeklickt)

    assert antwort.status_code == HTTPStatus.OK
    assert ausgewählteModelleIm(antwort.get_json()) == stellenDerEinheitAlsZahlen(
        schlachtInDerBewegungsphase, boyz
    )


def testAuf20_6DerDienstWähltBeimAnklickenEinesGesetztenModellsInDerAufstellungDieGanzeEinheit(
    dienst, aufstellungNachDerZonenwahl, boyzSetzen, boyz
):
    gesetzte = boyzSetzen(3)
    [(angeklickt, _), *_] = gesetzte

    antwort = modellAnklicken(dienst, aufstellungNachDerZonenwahl, boyz, angeklickt)

    spielstand = antwort.get_json()
    assert antwort.status_code == HTTPStatus.OK
    assert ausgewählteEinheitenIm(spielstand) == {"Boyz"}
    assert ausgewählteModelleIm(spielstand) == {
        stelleImSpielstand(stelle) for _, stelle in gesetzte
    }
    assert ebenenIm(spielstand) == frozenset()


def testAuf20_6DerDienstWähltBeimAnklickenEinesGesetztenModellsInDerAufstellungKeineAndereEinheit(
    dienst, aufstellungNachDerZonenwahl, boyzSetzen, boyz
):
    gesetzte = boyzSetzen(3)
    [(angeklickt, _), *_] = gesetzte
    auswählen(dienst, "Warboss")

    antwort = modellAnklicken(dienst, aufstellungNachDerZonenwahl, boyz, angeklickt)

    spielstand = antwort.get_json()
    assert antwort.status_code == HTTPStatus.OK
    assert ausgewählteEinheitenIm(spielstand) == {"Boyz"}
    assert ausgewählteModelleIm(spielstand) == {
        stelleImSpielstand(stelle) for _, stelle in gesetzte
    }


@mitMausUndFinger
def testAuf20_6DieSeiteKennzeichnetNachDemKlickAufEinModellInDerSchlachtAlleModelleDerEinheit(
    bildschirm, beendeteAufstellung, schlachtInDerBewegungsphase, einheitJederSeite, eingabe
):
    angeklickt, *_ = einheitJederSeite.modelle
    stelle = schlachtInDerBewegungsphase.stelle(angeklickt)
    seite = seiteDerSchlachtMitEingabe(
        bildschirm, beendeteAufstellung, schlachtInDerBewegungsphase, eingabe
    )

    klickenMit[eingabe](seite, punktAufDerKarte(seite, stelle))

    expect(seite.locator(".karte .modell.ausgewählt")).to_have_count(len(einheitJederSeite.modelle))
    assert ausgewählteModelle(seite) == stellenDerEinheitAlsZahlen(
        schlachtInDerBewegungsphase, einheitJederSeite
    )


@mitMausUndFinger
def testAuf20_6DieSeiteKennzeichnetNachDemKlickAufEinModellInDerAufstellungDieGanzeEinheit(
    bildschirm, aufstellungNachDerZonenwahl, boyzSetzen, eingabe
):
    gesetzte = boyzSetzen(3)
    [(_, stelle), *_] = gesetzte
    seite = seiteMitEingabe(bildschirm, aufstellungNachDerZonenwahl, eingabe)

    klickenMit[eingabe](seite, punktAufDerKarte(seite, stelle))

    expect(seite.locator(".karte .modell.ausgewählt")).to_have_count(len(gesetzte))
    assert ausgewählteEinheiten(seite) == {"Boyz"}
    assert ausgewählteModelle(seite) == {stelleImSpielstand(stelle) for _, stelle in gesetzte}
