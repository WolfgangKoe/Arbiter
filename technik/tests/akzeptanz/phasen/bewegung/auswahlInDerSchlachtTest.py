"""BEW-7 · Auswahl in der Schlacht."""

from fractions import Fraction
from http import HTTPStatus

from playwright.sync_api import expect

from tests.akzeptanz.auswahl import ausgewählteModelle
from tests.akzeptanz.bildschirm import seiteDerSchlachtMitEingabe
from tests.akzeptanz.dienst import (
    ausgewählteModelleIm,
    modellAnklicken,
    modellebenenIm,
    stelleImSpielstand,
)
from tests.akzeptanz.handgriffe import modellebeneWählen, versetzt
from tests.akzeptanz.schlacht import jetzigeStellen, stellenDerEinheitAlsZahlen
from tests.akzeptanz.ziehen import (
    klickenMit,
    liegtEinPixelGenauAn,
    mitMausUndFinger,
    modellZiehen,
    punktAufDemSpielfeld,
)

dreiZollNachOsten = (Fraction(3), Fraction(0))


def testBew7_1EinKlickAufEinModellDerAusgewähltenEinheitMachtSeineModellebeneZuIhrerEbene(
    schlachtInDerBewegungsphase, einheitJederSeite
):
    angeklickt, *_ = einheitJederSeite.modelle
    schlachtInDerBewegungsphase.auswählen(einheitJederSeite)

    schlachtInDerBewegungsphase.modellAnklicken(angeklickt)

    assert schlachtInDerBewegungsphase.istModellebene(angeklickt)
    assert not schlachtInDerBewegungsphase.hatEinheitenebene(einheitJederSeite)


def testBew7_1MitDerModellebeneEinesAnderenModellsWirdDieDesAngeklicktenZurEbene(
    schlachtNachDerWahlDesErstenZugs, boyz
):
    erstes, zweites, *_ = boyz.modelle
    modellebeneWählen(schlachtNachDerWahlDesErstenZugs, boyz, erstes)

    schlachtNachDerWahlDesErstenZugs.modellAnklicken(zweites)

    assert schlachtNachDerWahlDesErstenZugs.istModellebene(zweites)
    assert not schlachtNachDerWahlDesErstenZugs.istModellebene(erstes)
    assert schlachtNachDerWahlDesErstenZugs.ausgewählt(boyz)


def testBew7_1DerDienstNenntNachDemZweitenKlickDieModellebeneDesModells(
    dienstDerSchlacht, beendeteAufstellung, schlachtInDerBewegungsphase, einheitJederSeite
):
    angeklickt, *_ = einheitJederSeite.modelle
    modellAnklicken(dienstDerSchlacht, beendeteAufstellung, einheitJederSeite, angeklickt)

    antwort = modellAnklicken(dienstDerSchlacht, beendeteAufstellung, einheitJederSeite, angeklickt)

    stelle = stelleImSpielstand(schlachtInDerBewegungsphase.stelle(angeklickt))
    assert antwort.status_code == HTTPStatus.OK
    assert modellebenenIm(antwort.get_json()) == {stelle}


def testBew7_2EinKlickAufDasModellDerModellebeneMachtDieEinheitenebeneZurEbene(
    schlachtInDerBewegungsphase, einheitJederSeite
):
    angeklickt, *_ = einheitJederSeite.modelle
    modellebeneWählen(schlachtInDerBewegungsphase, einheitJederSeite, angeklickt)
    assert schlachtInDerBewegungsphase.istModellebene(angeklickt)

    schlachtInDerBewegungsphase.modellAnklicken(angeklickt)

    assert schlachtInDerBewegungsphase.ausgewählt(einheitJederSeite)
    assert schlachtInDerBewegungsphase.hatEinheitenebene(einheitJederSeite)


def testBew7_2DerDienstNenntNachDemDrittenKlickKeineModellebeneUndAlleModelleAusgewählt(
    dienstDerSchlacht, beendeteAufstellung, schlachtInDerBewegungsphase, boyz
):
    angeklickt, *_ = boyz.modelle
    modellebeneWählen(schlachtInDerBewegungsphase, boyz, angeklickt)
    assert schlachtInDerBewegungsphase.istModellebene(angeklickt)

    antwort = modellAnklicken(dienstDerSchlacht, beendeteAufstellung, boyz, angeklickt)

    spielstand = antwort.get_json()
    assert antwort.status_code == HTTPStatus.OK
    assert modellebenenIm(spielstand) == frozenset()
    assert ausgewählteModelleIm(spielstand) == stellenDerEinheitAlsZahlen(
        schlachtInDerBewegungsphase, boyz
    )


def testBew7_3MitDerModellebeneEinesModellsSetztDasLoslassenNurDieses(
    schlachtInDerBewegungsphase, boyz
):
    *_, gezogenes = boyz.modelle
    modellebeneWählen(schlachtInDerBewegungsphase, boyz, gezogenes)
    davor = jetzigeStellen(schlachtInDerBewegungsphase, boyz)
    ziel = versetzt(davor[gezogenes], dreiZollNachOsten)

    schlachtInDerBewegungsphase.modellLoslassen(gezogenes, ziel)

    erwartet = {**davor, gezogenes: ziel}
    assert jetzigeStellen(schlachtInDerBewegungsphase, boyz) == erwartet


@mitMausUndFinger
def testBew7_3DieSeiteZiehtBeiEinerModellebeneNurDieses(
    bildschirm, beendeteAufstellung, schlachtInDerBewegungsphase, boyz, eingabe
):
    *übrige, gezogenes = boyz.modelle
    modellebeneWählen(schlachtInDerBewegungsphase, boyz, gezogenes)
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


def testBew7_4MitDerModellebeneEinesModellsIstNurDiesesAusgewählt(
    schlachtInDerBewegungsphase, boyz
):
    angeklickt, *andere = boyz.modelle
    schlachtInDerBewegungsphase.auswählen(boyz)

    schlachtInDerBewegungsphase.modellAnklicken(angeklickt)

    assert schlachtInDerBewegungsphase.modellAusgewählt(angeklickt)
    assert [
        modell for modell in andere if schlachtInDerBewegungsphase.modellAusgewählt(modell)
    ] == []


def testBew7_4DerDienstKennzeichnetNurDasModellDerModellebene(
    dienstDerSchlacht, beendeteAufstellung, schlachtInDerBewegungsphase, necronWarriors
):
    angeklickt, *_ = necronWarriors.modelle
    schlachtInDerBewegungsphase.auswählen(necronWarriors)

    antwort = modellAnklicken(dienstDerSchlacht, beendeteAufstellung, necronWarriors, angeklickt)

    stelle = stelleImSpielstand(schlachtInDerBewegungsphase.stelle(angeklickt))
    assert ausgewählteModelleIm(antwort.get_json()) == {stelle}
    assert modellebenenIm(antwort.get_json()) == {stelle}


@mitMausUndFinger
def testBew7_4DasSpielfeldKennzeichnetNachDemKlickNurDasAngeklickteModell(
    bildschirm, beendeteAufstellung, schlachtInDerBewegungsphase, boyz, eingabe
):
    *_, angeklickt = boyz.modelle
    schlachtInDerBewegungsphase.auswählen(boyz)
    stelle = schlachtInDerBewegungsphase.stelle(angeklickt)
    seite = seiteDerSchlachtMitEingabe(
        bildschirm, beendeteAufstellung, schlachtInDerBewegungsphase, eingabe
    )

    klickenMit[eingabe](seite, punktAufDemSpielfeld(seite, stelle))

    expect(seite.locator(".spielfeld .modell.ausgewählt")).to_have_count(1)
    assert ausgewählteModelle(seite) == {stelleImSpielstand(stelle)}
