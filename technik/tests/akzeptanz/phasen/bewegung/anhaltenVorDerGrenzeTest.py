"""BEW-6 · Anhalten an der Kante und vor der Nahkampfreichweite."""

from fractions import Fraction
from http import HTTPStatus

import pytest

from arbiter.domaene.spielobjekte import Stelle
from tests.akzeptanz.bildschirm import seiteDerSchlachtMitEingabe, sperrmeldungenDerSeite
from tests.akzeptanz.dienst import (
    modellLoslassen,
    stelleBeimLoslassenAbfragen,
    stellenDerAbfrage,
    stellenDerEinheitIm,
)
from tests.akzeptanz.handgriffe import versetzt, wegVon
from tests.akzeptanz.schlacht import (
    abstandImQuadrat,
    abständeZuDenSpielfeldkanten,
    aufeinanderZuZiehen,
    außerhalbDerNahkampfreichweite,
    bewegungsweite,
    hältAnDerBewegungsweite,
    hältAnDerSpielfeldkante,
    hältVorDerNahkampfreichweite,
    jetzigeStellen,
    liegtAufDerGeradenVon,
    stellenAlsZahlen,
    stellenVersetzt,
    summeDerRadien,
    zurBewegungsphaseDesNächstenZugs,
)
from tests.akzeptanz.ziehen import haltenUndLosslassen, mitMausUndFinger

nichts = Fraction(0)
dreiZoll = Fraction(3)
halberZoll = Fraction(1, 2)
zweiZoll = Fraction(2)
dreiZollNachWesten = (-dreiZoll, nichts)
zehnZollNachWesten = (Fraction(-10), nichts)
dreiZollNachSüden = (nichts, dreiZoll)
vierZollNachNorden = (nichts, Fraction(-4))
jeZweiZollNachOstenUndSüden = (zweiZoll, zweiZoll)
flachZurWestkante = (Fraction(-3, 2), Fraction(12))


schrägÜberDieKante = (Fraction(-5), Fraction(2))
geradeÜberDieKante = (-zweiZoll, dreiZoll)
jenseitsDerKanteNebenDemOverlord = (-zweiZoll, Fraction(-1))


def überDerSpielfeldkante(stelle: Stelle, modell) -> bool:
    return min(abständeZuDenSpielfeldkanten(stelle, modell)) < 0


@pytest.fixture(params=["westen", "norden", "osten"])
def zugÜberEineSpielfeldkante(request, boyz, warboss, necronWarriors):
    if request.param == "osten":
        schlacht = request.getfixturevalue("schlachtInDerBewegungsphaseDesZweitenSpielers")
        *_, modell = necronWarriors.modelle
        return schlacht, modell, versetzt(schlacht.stelle(modell), (dreiZoll, nichts))
    schlacht = request.getfixturevalue("schlachtInDerBewegungsphase")
    if request.param == "westen":
        *_, modell = boyz.modelle
        return schlacht, modell, versetzt(schlacht.stelle(modell), dreiZollNachWesten)
    (modell,) = warboss.modelle
    schlacht.modellLoslassen(modell, versetzt(schlacht.stelle(modell), dreiZollNachSüden))
    return schlacht, modell, versetzt(schlacht.stelle(modell), vierZollNachNorden)


def blockSüdlichDerNordkante(schlacht, boyz):
    schlacht.auswählen(boyz)
    erstes, *_, gezogenes = boyz.modelle
    schlacht.modellLoslassen(gezogenes, versetzt(schlacht.stelle(gezogenes), dreiZollNachSüden))
    return erstes, gezogenes, jetzigeStellen(schlacht, boyz)


def vorDenOverlord(schlacht, warboss, overlord, abstand: Fraction):
    (modell,) = warboss.modelle
    (modellDesAnderenSpielers,) = overlord.modelle
    aufeinanderZuZiehen(schlacht, modell, modellDesAnderenSpielers, abstand)
    return modell, modellDesAnderenSpielers


def nebenDemOverlordAnDerKante(schlacht, warboss, overlord, versatz):
    modell, modellDesAnderenSpielers = vorDenOverlord(schlacht, warboss, overlord, dreiZoll)
    stelleDesAnderen = schlacht.stelle(modellDesAnderenSpielers)
    schlacht.modellLoslassen(modell, versetzt(stelleDesAnderen, versatz))
    zurBewegungsphaseDesNächstenZugs(schlacht)
    zurBewegungsphaseDesNächstenZugs(schlacht)
    return modell, modellDesAnderenSpielers, stelleDesAnderen


def testBew6_1ZiehtEinModellÜberDieSpielfeldkanteHältArbiterEsDavorAn(zugÜberEineSpielfeldkante):
    schlacht, modell, ziel = zugÜberEineSpielfeldkante
    davor = schlacht.stelle(modell)

    schlacht.modellLoslassen(modell, ziel)

    danach = schlacht.stelle(modell)
    assert hältAnDerSpielfeldkante(danach, modell)
    assert liegtAufDerGeradenVon(davor, ziel, danach)


def testBew6_1BeiDerEinheitenebeneHältDerBlockAnSobaldEinesDieKanteErreicht(
    schlachtInDerBewegungsphase, boyz
):
    erstes, gezogenes, davor = blockSüdlichDerNordkante(schlachtInDerBewegungsphase, boyz)
    ziel = versetzt(davor[gezogenes], vierZollNachNorden)

    schlachtInDerBewegungsphase.modellLoslassen(gezogenes, ziel)

    danach = jetzigeStellen(schlachtInDerBewegungsphase, boyz)
    assert hältAnDerSpielfeldkante(danach[erstes], erstes)
    assert liegtAufDerGeradenVon(davor[gezogenes], ziel, danach[gezogenes])
    assert danach == stellenVersetzt(davor, wegVon(davor[gezogenes], danach[gezogenes]))


def testBew6_1DerDienstHältAnDerKanteAnUndAntwortetOhneGrund(
    dienstDerSchlacht, beendeteAufstellung, schlachtInDerBewegungsphase, boyz
):
    *_, modell = boyz.modelle
    ziel = versetzt(schlachtInDerBewegungsphase.stelle(modell), dreiZollNachWesten)

    antwort = modellLoslassen(dienstDerSchlacht, beendeteAufstellung, boyz, modell, ziel)

    assert antwort.status_code == HTTPStatus.OK
    assert "gründe" not in antwort.get_json()
    assert hältAnDerSpielfeldkante(schlachtInDerBewegungsphase.stelle(modell), modell)


def testBew6_2ZiehtEinModellInDieNahkampfreichweiteDesAnderenSpielersHältArbiterEsDavorAn(
    schlachtInDerBewegungsphase, warboss, overlord
):
    (modell,) = warboss.modelle
    (modellDesAnderenSpielers,) = overlord.modelle
    radien = summeDerRadien(modell, modellDesAnderenSpielers)
    aufeinanderZuZiehen(schlachtInDerBewegungsphase, modell, modellDesAnderenSpielers, dreiZoll)
    davor = schlachtInDerBewegungsphase.stelle(modell)
    stelleDesAnderen = schlachtInDerBewegungsphase.stelle(modellDesAnderenSpielers)
    ziel = Stelle(x=stelleDesAnderen.x - radien - halberZoll, y=davor.y)
    assert abstandImQuadrat(davor, ziel) <= bewegungsweite("Warboss", "Warboss") ** 2
    assert not außerhalbDerNahkampfreichweite(
        ziel, modell, stelleDesAnderen, modellDesAnderenSpielers
    )

    schlachtInDerBewegungsphase.modellLoslassen(modell, ziel)

    danach = schlachtInDerBewegungsphase.stelle(modell)
    assert hältVorDerNahkampfreichweite(danach, modell, stelleDesAnderen, modellDesAnderenSpielers)
    assert liegtAufDerGeradenVon(davor, ziel, danach)


def testBew6_2BeiDerEinheitenebeneHältDerBlockAnBevorEinesInDerNahkampfreichweiteIst(
    schlachtInDerBewegungsphase, boyz, overlord
):
    (modellDesAnderenSpielers,) = overlord.modelle
    vorderstes, *_, gezogenes = boyz.modelle
    schlachtInDerBewegungsphase.auswählen(boyz)
    schlachtInDerBewegungsphase.modellLoslassen(
        vorderstes,
        versetzt(schlachtInDerBewegungsphase.stelle(vorderstes), jeZweiZollNachOstenUndSüden),
    )
    zurBewegungsphaseDesNächstenZugs(schlachtInDerBewegungsphase)
    zurBewegungsphaseDesNächstenZugs(schlachtInDerBewegungsphase)
    aufeinanderZuZiehen(schlachtInDerBewegungsphase, vorderstes, modellDesAnderenSpielers, dreiZoll)
    davor = jetzigeStellen(schlachtInDerBewegungsphase, boyz)
    stelleDesAnderen = schlachtInDerBewegungsphase.stelle(modellDesAnderenSpielers)
    ziel = versetzt(davor[gezogenes], (Fraction(4), nichts))

    schlachtInDerBewegungsphase.modellLoslassen(gezogenes, ziel)

    danach = jetzigeStellen(schlachtInDerBewegungsphase, boyz)
    assert danach == stellenVersetzt(davor, wegVon(davor[gezogenes], danach[gezogenes]))
    assert liegtAufDerGeradenVon(davor[gezogenes], ziel, danach[gezogenes])
    assert hältVorDerNahkampfreichweite(
        danach[vorderstes], vorderstes, stelleDesAnderen, modellDesAnderenSpielers
    )
    assert [
        modell
        for modell, stelle in danach.items()
        if not außerhalbDerNahkampfreichweite(
            stelle, modell, stelleDesAnderen, modellDesAnderenSpielers
        )
    ] == []


def testBew6_2ZiehtEinModellAufDerStreckeDurchDieNahkampfreichweiteHältArbiterEsDavorAn(
    schlachtInDerBewegungsphase, warboss, overlord
):
    modell, modellDesAnderenSpielers = vorDenOverlord(
        schlachtInDerBewegungsphase, warboss, overlord, dreiZoll
    )
    stelleDesAnderen = schlachtInDerBewegungsphase.stelle(modellDesAnderenSpielers)
    seitlich = summeDerRadien(modell, modellDesAnderenSpielers) + halberZoll
    davor = versetzt(stelleDesAnderen, (-zweiZoll, seitlich))
    schlachtInDerBewegungsphase.modellLoslassen(modell, davor)
    zurBewegungsphaseDesNächstenZugs(schlachtInDerBewegungsphase)
    zurBewegungsphaseDesNächstenZugs(schlachtInDerBewegungsphase)
    ziel = versetzt(stelleDesAnderen, (zweiZoll, seitlich))
    assert außerhalbDerNahkampfreichweite(ziel, modell, stelleDesAnderen, modellDesAnderenSpielers)

    schlachtInDerBewegungsphase.modellLoslassen(modell, ziel)

    danach = schlachtInDerBewegungsphase.stelle(modell)
    assert hältVorDerNahkampfreichweite(danach, modell, stelleDesAnderen, modellDesAnderenSpielers)
    assert liegtAufDerGeradenVon(davor, ziel, danach)


def testBew6_3LiegtDieKanteVorDerBewegungsweiteHältArbiterAnDerKanteAn(
    schlachtInDerBewegungsphase, boyz
):
    *_, modell = boyz.modelle
    ziel = versetzt(schlachtInDerBewegungsphase.stelle(modell), zehnZollNachWesten)

    schlachtInDerBewegungsphase.modellLoslassen(modell, ziel)

    assert hältAnDerSpielfeldkante(schlachtInDerBewegungsphase.stelle(modell), modell)


def testBew6_3LiegtDieBewegungsweiteVorDerKanteHältArbiterAnDerBewegungsweiteAn(
    schlachtInDerBewegungsphase, boyz
):
    *_, modell = boyz.modelle
    davor = schlachtInDerBewegungsphase.stelle(modell)
    ziel = versetzt(davor, flachZurWestkante)

    schlachtInDerBewegungsphase.modellLoslassen(modell, ziel)

    danach = schlachtInDerBewegungsphase.stelle(modell)
    assert hältAnDerBewegungsweite(davor, danach, bewegungsweite("Boyz", modell.modellart))
    assert liegtAufDerGeradenVon(davor, ziel, danach)


def testBew6_3LiegtDieNahkampfreichweiteVorDerBewegungsweiteHältArbiterDavorAn(
    schlachtInDerBewegungsphase, warboss, overlord
):
    modell, modellDesAnderenSpielers = vorDenOverlord(
        schlachtInDerBewegungsphase, warboss, overlord, dreiZoll
    )
    davor = schlachtInDerBewegungsphase.stelle(modell)
    stelleDesAnderen = schlachtInDerBewegungsphase.stelle(modellDesAnderenSpielers)

    schlachtInDerBewegungsphase.modellLoslassen(modell, versetzt(davor, (Fraction(8), nichts)))

    danach = schlachtInDerBewegungsphase.stelle(modell)
    assert hältVorDerNahkampfreichweite(danach, modell, stelleDesAnderen, modellDesAnderenSpielers)


def testBew6_3LiegtDieBewegungsweiteVorDerNahkampfreichweiteHältArbiterAnDerBewegungsweiteAn(
    schlachtInDerBewegungsphase, warboss, overlord
):
    modell, _ = vorDenOverlord(schlachtInDerBewegungsphase, warboss, overlord, Fraction(7))
    davor = schlachtInDerBewegungsphase.stelle(modell)

    schlachtInDerBewegungsphase.modellLoslassen(modell, versetzt(davor, (Fraction(8), nichts)))

    danach = schlachtInDerBewegungsphase.stelle(modell)
    assert hältAnDerBewegungsweite(davor, danach, bewegungsweite("Warboss", "Warboss"))


@pytest.mark.parametrize(
    ("versatz", "hältAnDerKante"),
    [(schrägÜberDieKante, True), (geradeÜberDieKante, False)],
    ids=["kanteVorDerNahkampfreichweite", "nahkampfreichweiteVorDerKante"],
)
def testBew6_3LiegenKanteUndNahkampfreichweiteAufDemWegHältArbiterAnDerErstenAn(
    schlachtInDerBewegungsphase, warboss, overlord, versatz, hältAnDerKante
):
    modell, modellDesAnderenSpielers, stelleDesAnderen = nebenDemOverlordAnDerKante(
        schlachtInDerBewegungsphase, warboss, overlord, versatz
    )
    davor = schlachtInDerBewegungsphase.stelle(modell)
    ziel = versetzt(stelleDesAnderen, jenseitsDerKanteNebenDemOverlord)
    assert abstandImQuadrat(davor, ziel) <= bewegungsweite("Warboss", "Warboss") ** 2
    assert überDerSpielfeldkante(ziel, modell)
    assert not außerhalbDerNahkampfreichweite(
        ziel, modell, stelleDesAnderen, modellDesAnderenSpielers
    )

    schlachtInDerBewegungsphase.modellLoslassen(modell, ziel)

    danach = schlachtInDerBewegungsphase.stelle(modell)
    assert liegtAufDerGeradenVon(davor, ziel, danach)
    assert hältAnDerSpielfeldkante(danach, modell) is hältAnDerKante
    assert (
        hältVorDerNahkampfreichweite(danach, modell, stelleDesAnderen, modellDesAnderenSpielers)
        is not hältAnDerKante
    )


def testBew6_4DieStellenBeimLoslassenHaltenDenBlockAnDerKanteAn(schlachtInDerBewegungsphase, boyz):
    erstes, gezogenes, davor = blockSüdlichDerNordkante(schlachtInDerBewegungsphase, boyz)
    ziel = versetzt(davor[gezogenes], vierZollNachNorden)

    stellen = schlachtInDerBewegungsphase.stellenBeimLoslassen(gezogenes, ziel).stellen

    assert hältAnDerSpielfeldkante(stellen[erstes], erstes)
    assert stellen == stellenVersetzt(davor, wegVon(davor[gezogenes], stellen[gezogenes]))


def testBew6_4DieStellenBeimLoslassenHaltenVorDerNahkampfreichweiteAn(
    schlachtInDerBewegungsphase, warboss, overlord
):
    modell, modellDesAnderenSpielers = vorDenOverlord(
        schlachtInDerBewegungsphase, warboss, overlord, dreiZoll
    )
    davor = schlachtInDerBewegungsphase.stelle(modell)
    stelleDesAnderen = schlachtInDerBewegungsphase.stelle(modellDesAnderenSpielers)

    stellen = schlachtInDerBewegungsphase.stellenBeimLoslassen(
        modell, versetzt(davor, (Fraction(8), nichts))
    ).stellen

    assert hältVorDerNahkampfreichweite(
        stellen[modell], modell, stelleDesAnderen, modellDesAnderenSpielers
    )


def testBew6_4DerDienstNenntAnDerKanteDieStelleDesAnhaltensWieDasLoslassen(
    dienstDerSchlacht, beendeteAufstellung, schlachtInDerBewegungsphase, boyz
):
    *_, modell = boyz.modelle
    ziel = versetzt(schlachtInDerBewegungsphase.stelle(modell), zehnZollNachWesten)
    abfrage = stelleBeimLoslassenAbfragen(
        dienstDerSchlacht, beendeteAufstellung, boyz, modell, ziel
    )

    loslassen = modellLoslassen(dienstDerSchlacht, beendeteAufstellung, boyz, modell, ziel)

    gesetzt = {modell: schlachtInDerBewegungsphase.stelle(modell)}
    assert abfrage.status_code == HTTPStatus.OK
    assert loslassen.status_code == HTTPStatus.OK
    assert stellenDerEinheitIm(abfrage.get_json(), "Boyz") == stellenDerAbfrage(boyz, gesetzt)
    assert hältAnDerSpielfeldkante(schlachtInDerBewegungsphase.stelle(modell), modell)


@mitMausUndFinger
def testBew6_4DasSpielfeldZeigtBeimHaltenDenBlockDortWoErAnDerKanteAnhält(
    bildschirm, beendeteAufstellung, schlachtInDerBewegungsphase, boyz, eingabe
):
    erstes, gezogenes, davor = blockSüdlichDerNordkante(schlachtInDerBewegungsphase, boyz)
    seite = seiteDerSchlachtMitEingabe(
        bildschirm, beendeteAufstellung, schlachtInDerBewegungsphase, eingabe
    )

    gezeigt = haltenUndLosslassen(
        seite, davor[gezogenes], versetzt(davor[gezogenes], vierZollNachNorden), eingabe
    )

    assert gezeigt == stellenAlsZahlen(schlachtInDerBewegungsphase)
    assert sperrmeldungenDerSeite(seite) == []
    assert hältAnDerSpielfeldkante(schlachtInDerBewegungsphase.stelle(erstes), erstes)
