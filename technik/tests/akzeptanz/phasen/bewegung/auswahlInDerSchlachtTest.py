"""BEW-7 · Auswahl in der Schlacht."""

from fractions import Fraction
from http import HTTPStatus

from playwright.sync_api import expect

from tests.akzeptanz.auswahl import ausgewählteModelle
from tests.akzeptanz.bildschirm import seiteDerSchlachtMitEingabe
from tests.akzeptanz.dienst import (
    ausgewählteModelleIm,
    ebenenIm,
    modellAnklicken,
    stelleImSpielstand,
)
from tests.akzeptanz.handgriffe import versetzt
from tests.akzeptanz.schlacht import (
    jetzigeStellen,
    modellZurEbeneMachen,
    stellenDerEinheitAlsZahlen,
)
from tests.akzeptanz.ziehen import (
    klickenMit,
    liegtEinPixelGenauAn,
    mitMausUndFinger,
    modellZiehen,
    punktAufDerKarte,
)

dreiZollNachOsten = (Fraction(3), Fraction(0))


def testBew7_1EinKlickAufEinModellDerAusgewähltenEinheitMachtEsZuIhrerEbene(
    schlachtInDerBewegungsphase, einheitJederSeite
):
    angeklickt, *_ = einheitJederSeite.modelle
    schlachtInDerBewegungsphase.auswählen(einheitJederSeite)

    schlachtInDerBewegungsphase.modellAnklicken(angeklickt)

    assert schlachtInDerBewegungsphase.modellIstEbene(angeklickt)
    assert not schlachtInDerBewegungsphase.ganzeEinheitIstEbene(einheitJederSeite)


def testBew7_1IstEinAnderesModellDieEbeneWirdDasAngeklickteZurEbene(
    schlachtInDerKommandophase, boyz
):
    erstes, zweites, *_ = boyz.modelle
    modellZurEbeneMachen(schlachtInDerKommandophase, boyz, erstes)

    schlachtInDerKommandophase.modellAnklicken(zweites)

    assert schlachtInDerKommandophase.modellIstEbene(zweites)
    assert not schlachtInDerKommandophase.modellIstEbene(erstes)
    assert schlachtInDerKommandophase.ausgewählt(boyz)


def testBew7_1DerDienstNenntNachDemZweitenKlickDasModellAlsEbene(
    dienstDerSchlacht, beendeteAufstellung, schlachtInDerBewegungsphase, einheitJederSeite
):
    angeklickt, *_ = einheitJederSeite.modelle
    modellAnklicken(dienstDerSchlacht, beendeteAufstellung, einheitJederSeite, angeklickt)

    antwort = modellAnklicken(dienstDerSchlacht, beendeteAufstellung, einheitJederSeite, angeklickt)

    stelle = stelleImSpielstand(schlachtInDerBewegungsphase.stelle(angeklickt))
    assert antwort.status_code == HTTPStatus.OK
    assert ebenenIm(antwort.get_json()) == {stelle}


def testBew7_2EinKlickAufDasModellDerEbeneMachtDieGanzeEinheitZurEbene(
    schlachtInDerBewegungsphase, einheitJederSeite
):
    angeklickt, *_ = einheitJederSeite.modelle
    modellZurEbeneMachen(schlachtInDerBewegungsphase, einheitJederSeite, angeklickt)
    assert schlachtInDerBewegungsphase.modellIstEbene(angeklickt)

    schlachtInDerBewegungsphase.modellAnklicken(angeklickt)

    assert schlachtInDerBewegungsphase.ausgewählt(einheitJederSeite)
    assert schlachtInDerBewegungsphase.ganzeEinheitIstEbene(einheitJederSeite)


def testBew7_2DerDienstNenntNachDemDrittenKlickKeineEbeneUndAlleModelleAusgewählt(
    dienstDerSchlacht, beendeteAufstellung, schlachtInDerBewegungsphase, boyz
):
    angeklickt, *_ = boyz.modelle
    modellZurEbeneMachen(schlachtInDerBewegungsphase, boyz, angeklickt)
    assert schlachtInDerBewegungsphase.modellIstEbene(angeklickt)

    antwort = modellAnklicken(dienstDerSchlacht, beendeteAufstellung, boyz, angeklickt)

    spielstand = antwort.get_json()
    assert antwort.status_code == HTTPStatus.OK
    assert ebenenIm(spielstand) == frozenset()
    assert ausgewählteModelleIm(spielstand) == stellenDerEinheitAlsZahlen(
        schlachtInDerBewegungsphase, boyz
    )


def testBew7_3IstEinModellDieEbeneSetztDasLoslassenNurDieses(schlachtInDerBewegungsphase, boyz):
    *_, gezogenes = boyz.modelle
    modellZurEbeneMachen(schlachtInDerBewegungsphase, boyz, gezogenes)
    davor = jetzigeStellen(schlachtInDerBewegungsphase, boyz)
    ziel = versetzt(davor[gezogenes], dreiZollNachOsten)

    schlachtInDerBewegungsphase.modellLoslassen(gezogenes, ziel)

    erwartet = {**davor, gezogenes: ziel}
    assert jetzigeStellen(schlachtInDerBewegungsphase, boyz) == erwartet


@mitMausUndFinger
def testBew7_3DieSeiteZiehtBeiEinemModellAlsEbeneNurDieses(
    bildschirm, beendeteAufstellung, schlachtInDerBewegungsphase, boyz, eingabe
):
    *übrige, gezogenes = boyz.modelle
    modellZurEbeneMachen(schlachtInDerBewegungsphase, boyz, gezogenes)
    davor = jetzigeStellen(schlachtInDerBewegungsphase, boyz)
    ziel = versetzt(davor[gezogenes], dreiZollNachOsten)
    seite = seiteDerSchlachtMitEingabe(
        bildschirm, beendeteAufstellung, schlachtInDerBewegungsphase, eingabe
    )

    modellZiehen(seite, davor[gezogenes], ziel, eingabe)

    danach = jetzigeStellen(schlachtInDerBewegungsphase, boyz)
    assert liegtEinPixelGenauAn(seite, danach[gezogenes], ziel)
    assert {modell: danach[modell] for modell in übrige} == {
        modell: davor[modell] for modell in übrige
    }


def testBew7_4IstEinModellDieEbeneIstNurDiesesAusgewählt(schlachtInDerBewegungsphase, boyz):
    angeklickt, *andere = boyz.modelle
    schlachtInDerBewegungsphase.auswählen(boyz)

    schlachtInDerBewegungsphase.modellAnklicken(angeklickt)

    assert schlachtInDerBewegungsphase.modellAusgewählt(angeklickt)
    assert [
        modell for modell in andere if schlachtInDerBewegungsphase.modellAusgewählt(modell)
    ] == []


def testBew7_4DerDienstKennzeichnetNurDasModellDerEbene(
    dienstDerSchlacht, beendeteAufstellung, schlachtInDerBewegungsphase, necronWarriors
):
    angeklickt, *_ = necronWarriors.modelle
    schlachtInDerBewegungsphase.auswählen(necronWarriors)

    antwort = modellAnklicken(dienstDerSchlacht, beendeteAufstellung, necronWarriors, angeklickt)

    stelle = stelleImSpielstand(schlachtInDerBewegungsphase.stelle(angeklickt))
    assert ausgewählteModelleIm(antwort.get_json()) == {stelle}
    assert ebenenIm(antwort.get_json()) == {stelle}


@mitMausUndFinger
def testBew7_4DieKarteKennzeichnetNachDemKlickNurDasAngeklickteModell(
    bildschirm, beendeteAufstellung, schlachtInDerBewegungsphase, boyz, eingabe
):
    *_, angeklickt = boyz.modelle
    schlachtInDerBewegungsphase.auswählen(boyz)
    stelle = schlachtInDerBewegungsphase.stelle(angeklickt)
    seite = seiteDerSchlachtMitEingabe(
        bildschirm, beendeteAufstellung, schlachtInDerBewegungsphase, eingabe
    )

    klickenMit[eingabe](seite, punktAufDerKarte(seite, stelle))

    expect(seite.locator(".karte .modell.ausgewählt")).to_have_count(1)
    assert ausgewählteModelle(seite) == {stelleImSpielstand(stelle)}
