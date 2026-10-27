"""BEW-3 · Anhalten an der Bewegungsweite."""

from fractions import Fraction
from http import HTTPStatus

import pytest

from tests.akzeptanz.bildschirm import seiteDerSchlachtMitEingabe, sperrmeldungenDerSeite
from tests.akzeptanz.dienst import modellLoslassen
from tests.akzeptanz.handgriffe import gestreckt, schrägOhneWurzel, versetzt, wegVon
from tests.akzeptanz.schlacht import (
    bewegungsweite,
    hältAnDerBewegungsweite,
    jetzigeStellen,
    liegtAufDerGeradenVon,
    schrägOhneHindernis,
    stellenVersetzt,
    zurBewegungsphaseDerNächstenSchlachtrunde,
)
from tests.akzeptanz.ziehen import mitMausUndFinger, modellZiehen

nichts = Fraction(0)
dreiZoll = Fraction(3)
weiterAlsDieBewegungsweiteDesWarboss = bewegungsweite("Warboss") + 1
weiterAlsDieBewegungsweiteDerBoyz = bewegungsweite("Boyz") + 1

wegeÜberDieBewegungsweite = pytest.mark.parametrize(
    "weg",
    [
        (weiterAlsDieBewegungsweiteDesWarboss, nichts),
        gestreckt(schrägOhneWurzel, weiterAlsDieBewegungsweiteDesWarboss),
    ],
    ids=["nachOsten", "schräg"],
)


def testBew3_1ZiehtEinModellGenauSoWeitWieSeineBewegungsweiteHältArbiterEsNichtAn(
    schlachtInDerBewegungsphase, warboss
):
    (modell,) = warboss.modelle
    ziel = versetzt(schlachtInDerBewegungsphase.stelle(modell), (bewegungsweite("Warboss"), nichts))

    schlachtInDerBewegungsphase.modellLoslassen(modell, ziel)

    assert schlachtInDerBewegungsphase.stelle(modell) == ziel


def testBew3_1ZiehtEinModellSchrägGenauSoWeitWieSeineBewegungsweiteHältArbiterEsNichtAn(
    schlachtInDerBewegungsphase, warboss
):
    (modell,) = warboss.modelle
    ziel = versetzt(
        schlachtInDerBewegungsphase.stelle(modell),
        gestreckt(schrägOhneWurzel, bewegungsweite("Warboss")),
    )

    schlachtInDerBewegungsphase.modellLoslassen(modell, ziel)

    assert schlachtInDerBewegungsphase.stelle(modell) == ziel


def testBew3_1JedesModellHatSeineEigeneBewegungsweite(
    schlachtInDerBewegungsphaseDesZweitenSpielers, overlord
):
    (modell,) = overlord.modelle
    ziel = versetzt(
        schlachtInDerBewegungsphaseDesZweitenSpielers.stelle(modell),
        (-bewegungsweite("Overlord"), nichts),
    )

    schlachtInDerBewegungsphaseDesZweitenSpielers.modellLoslassen(modell, ziel)

    assert schlachtInDerBewegungsphaseDesZweitenSpielers.stelle(modell) == ziel


@wegeÜberDieBewegungsweite
def testBew3_1ZiehtEinModellWeiterAlsDieBewegungsweiteHältArbiterEsAnDerBewegungsweiteAnOhneGrund(
    schlachtInDerBewegungsphase, warboss, weg
):
    (modell,) = warboss.modelle
    davor = schlachtInDerBewegungsphase.stelle(modell)
    ziel = versetzt(davor, weg)

    schlachtInDerBewegungsphase.modellLoslassen(modell, ziel)

    danach = schlachtInDerBewegungsphase.stelle(modell)
    assert hältAnDerBewegungsweite(davor, danach, bewegungsweite("Warboss"))
    assert liegtAufDerGeradenVon(davor, ziel, danach)


def testBew3_1DieDistanzZähltVonDerStelleZuBeginnDerBewegungsphase(
    schlachtInDerBewegungsphase, warboss
):
    (modell,) = warboss.modelle
    start = schlachtInDerBewegungsphase.stelle(modell)
    nachDemErstenZug = versetzt(start, (dreiZoll, nichts))
    schlachtInDerBewegungsphase.modellLoslassen(modell, nachDemErstenZug)
    ziel = versetzt(nachDemErstenZug, (bewegungsweite("Warboss"), nichts))

    schlachtInDerBewegungsphase.modellLoslassen(modell, ziel)

    danach = schlachtInDerBewegungsphase.stelle(modell)
    assert hältAnDerBewegungsweite(start, danach, bewegungsweite("Warboss"))


def testBew3_1DieDistanzBeginntMitJederBewegungsphaseNeu(schlachtInDerBewegungsphase, warboss):
    (modell,) = warboss.modelle
    zugweite = (bewegungsweite("Warboss"), nichts)
    erstesZiel = versetzt(schlachtInDerBewegungsphase.stelle(modell), zugweite)
    schlachtInDerBewegungsphase.modellLoslassen(modell, erstesZiel)
    zurBewegungsphaseDerNächstenSchlachtrunde(schlachtInDerBewegungsphase)
    zweitesZiel = versetzt(erstesZiel, zugweite)

    schlachtInDerBewegungsphase.modellLoslassen(modell, zweitesZiel)

    assert schlachtInDerBewegungsphase.stelle(modell) == zweitesZiel


def testBew3_1IstDieGanzeEinheitEbeneHältDerBlockAnDerBewegungsweiteAn(
    schlachtInDerBewegungsphase, boyz
):
    schlachtInDerBewegungsphase.auswählen(boyz)
    gezogenes, *_ = boyz.modelle
    davor = jetzigeStellen(schlachtInDerBewegungsphase, boyz)
    weg = gestreckt(schrägOhneHindernis, bewegungsweite("Boyz"))
    ziel = versetzt(davor[gezogenes], weg)

    schlachtInDerBewegungsphase.modellLoslassen(gezogenes, ziel)

    danach = jetzigeStellen(schlachtInDerBewegungsphase, boyz)
    gesetzterWeg = wegVon(davor[gezogenes], danach[gezogenes])
    assert hältAnDerBewegungsweite(davor[gezogenes], danach[gezogenes], bewegungsweite("Boyz"))
    assert liegtAufDerGeradenVon(davor[gezogenes], ziel, danach[gezogenes])
    assert danach == stellenVersetzt(davor, gesetzterWeg)


def testBew3_1DasModellMitDerWeitestenDistanzBestimmtDenHaltepunktDesBlocks(
    schlachtInDerBewegungsphase, boyz
):
    *_, weitesModell = boyz.modelle
    startDesWeitenModells = schlachtInDerBewegungsphase.stelle(weitesModell)
    schlachtInDerBewegungsphase.modellLoslassen(
        weitesModell, versetzt(startDesWeitenModells, (nichts, dreiZoll))
    )
    schlachtInDerBewegungsphase.auswählen(boyz)
    gezogenes, *_ = boyz.modelle
    davor = jetzigeStellen(schlachtInDerBewegungsphase, boyz)
    weg = gestreckt(schrägOhneHindernis, bewegungsweite("Boyz"))

    schlachtInDerBewegungsphase.modellLoslassen(gezogenes, versetzt(davor[gezogenes], weg))

    danach = jetzigeStellen(schlachtInDerBewegungsphase, boyz)
    gesetzterWeg = wegVon(davor[gezogenes], danach[gezogenes])
    assert hältAnDerBewegungsweite(
        startDesWeitenModells, danach[weitesModell], bewegungsweite("Boyz")
    )
    assert danach == stellenVersetzt(davor, gesetzterWeg)


def testBew3_1HältArbiterAnDerBewegungsweiteAnPrüftEsÜberEineBaseNurAnDerAngehaltenenStelle(
    schlachtInDerBewegungsphase, boyz, warboss
):
    (modellDesWarboss,) = warboss.modelle
    gezogenes, *_ = boyz.modelle
    stelleDesWarboss = schlachtInDerBewegungsphase.stelle(modellDesWarboss)
    schlachtInDerBewegungsphase.modellLoslassen(
        modellDesWarboss, versetzt(stelleDesWarboss, (bewegungsweite("Warboss"), nichts))
    )
    davor = schlachtInDerBewegungsphase.stelle(gezogenes)
    ziel = versetzt(davor, (weiterAlsDieBewegungsweiteDerBoyz, nichts))

    schlachtInDerBewegungsphase.modellLoslassen(gezogenes, ziel)

    danach = schlachtInDerBewegungsphase.stelle(gezogenes)
    assert hältAnDerBewegungsweite(davor, danach, bewegungsweite("Boyz"))


def testBew3_1DerDienstHältWeiterAlsDieBewegungsweiteAnDerBewegungsweiteAnUndAntwortetOhneGrund(
    dienstDerSchlacht, beendeteAufstellung, schlachtInDerBewegungsphase, warboss
):
    (modell,) = warboss.modelle
    davor = schlachtInDerBewegungsphase.stelle(modell)
    ziel = versetzt(davor, (weiterAlsDieBewegungsweiteDesWarboss, nichts))

    antwort = modellLoslassen(dienstDerSchlacht, beendeteAufstellung, warboss, modell, ziel)

    assert antwort.status_code == HTTPStatus.OK
    assert "gründe" not in antwort.get_json()
    danach = schlachtInDerBewegungsphase.stelle(modell)
    assert hältAnDerBewegungsweite(davor, danach, bewegungsweite("Warboss"))


@mitMausUndFinger
def testBew3_1DieSeiteHältWeiterAlsDieBewegungsweiteAnDerBewegungsweiteAnOhneSperrmeldung(
    bildschirm, beendeteAufstellung, schlachtInDerBewegungsphase, warboss, eingabe
):
    (modell,) = warboss.modelle
    davor = schlachtInDerBewegungsphase.stelle(modell)
    seite = seiteDerSchlachtMitEingabe(
        bildschirm, beendeteAufstellung, schlachtInDerBewegungsphase, eingabe
    )
    ziel = versetzt(davor, (weiterAlsDieBewegungsweiteDesWarboss, nichts))

    modellZiehen(seite, davor, ziel, eingabe)

    assert sperrmeldungenDerSeite(seite) == []
    danach = schlachtInDerBewegungsphase.stelle(modell)
    assert hältAnDerBewegungsweite(davor, danach, bewegungsweite("Warboss"))
