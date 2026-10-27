"""BEW-1 · Normale Bewegung."""

from fractions import Fraction
from http import HTTPStatus

from arbiter.domaene.sperre import Grund
from tests.akzeptanz.bildschirm import (
    kreiseDerKarte,
    seiteDerSchlachtMitEingabe,
    sperrmeldungenDerSeite,
)
from tests.akzeptanz.dienst import (
    modellLoslassen,
    spielstandVon,
    stelleBeimLoslassenAbfragen,
    stellenDerAbfrage,
    stellenDerEinheitIm,
)
from tests.akzeptanz.handgriffe import versetzt
from tests.akzeptanz.schlacht import (
    bewegungsweite,
    einModellAusDerKohärenzZiehen,
    hältAnDerBewegungsweite,
    jetzigeStellen,
    schrägOhneHindernis,
    stellenAlsZahlen,
    stellenVersetzt,
)
from tests.akzeptanz.ziehen import (
    halten,
    haltenUndLosslassen,
    hältAnDerBewegungsweiteAufEinenPixelGenau,
    mitMausUndFinger,
)

nichts = Fraction(0)
einigeZoll = (Fraction(3), nichts)
ausDerZoneHinaus = (Fraction(9, 2), nichts)
nachNorden = (nichts, Fraction(3))
überDieHälfteDerBewegungsweite = Fraction(3, 5)


def zuWeitNachOsten(einheitenname: str) -> tuple[Fraction, Fraction]:
    return bewegungsweite(einheitenname) + 1, nichts


def testBew1_5DasModellStehtDanachAnDerStelleDesLoslassens(schlachtInDerBewegungsphase, warboss):
    (modell,) = warboss.modelle
    ziel = versetzt(schlachtInDerBewegungsphase.stelle(modell), einigeZoll)

    schlachtInDerBewegungsphase.modellLoslassen(modell, ziel)

    assert schlachtInDerBewegungsphase.stelle(modell) == ziel


def testBew1_5IstDieGanzeEinheitEbeneRücktJedesModellUmDieselbeStreckeVor(
    schlachtInDerBewegungsphase, boyz
):
    schlachtInDerBewegungsphase.auswählen(boyz)
    gezogenes, *_ = boyz.modelle
    davor = jetzigeStellen(schlachtInDerBewegungsphase, boyz)
    ziel = versetzt(davor[gezogenes], schrägOhneHindernis)

    schlachtInDerBewegungsphase.modellLoslassen(gezogenes, ziel)

    assert jetzigeStellen(schlachtInDerBewegungsphase, boyz) == stellenVersetzt(
        davor, schrägOhneHindernis
    )


def testBew1_5IstDieEinheitNichtAusgewähltStehenDieAnderenModelleWieDavor(
    schlachtInDerBewegungsphase, boyz
):
    *übrige, gezogenes = boyz.modelle
    davor = jetzigeStellen(schlachtInDerBewegungsphase, boyz)
    ziel = versetzt(davor[gezogenes], (Fraction(2), nichts))

    schlachtInDerBewegungsphase.modellLoslassen(gezogenes, ziel)

    assert schlachtInDerBewegungsphase.stelle(gezogenes) == ziel
    assert all(schlachtInDerBewegungsphase.stelle(modell) == davor[modell] for modell in übrige)


def testBew1_5ArbiterRücktDasModellNichtInDieAufstellungszone(schlachtInDerBewegungsphase, warboss):
    (modell,) = warboss.modelle
    ziel = versetzt(schlachtInDerBewegungsphase.stelle(modell), ausDerZoneHinaus)

    schlachtInDerBewegungsphase.modellLoslassen(modell, ziel)

    assert schlachtInDerBewegungsphase.stelle(modell) == ziel


def testBew1_5FehlendeKohärenzSperrtBeimLoslassenNicht(schlachtInDerBewegungsphase, boyz):
    einModellAusDerKohärenzZiehen(schlachtInDerBewegungsphase, boyz)

    assert not schlachtInDerBewegungsphase.inKohärenz(boyz)


def testBew1_6EineSchonGezogeneEinheitLässtSichNachEinerAnderenAuchLängerAlsDieBewegungsweiteZiehen(
    schlachtInDerBewegungsphase, warboss, boyz
):
    (modellDesWarboss,) = warboss.modelle
    *_, letztesModellDerBoyz = boyz.modelle
    start = schlachtInDerBewegungsphase.stelle(modellDesWarboss)
    mehrAlsDieHälfte = (bewegungsweite("Warboss") * überDieHälfteDerBewegungsweite, nichts)
    schlachtInDerBewegungsphase.modellLoslassen(modellDesWarboss, versetzt(start, mehrAlsDieHälfte))
    stelleDerBoyz = schlachtInDerBewegungsphase.stelle(letztesModellDerBoyz)
    schlachtInDerBewegungsphase.modellLoslassen(
        letztesModellDerBoyz, versetzt(stelleDerBoyz, nachNorden)
    )

    schlachtInDerBewegungsphase.modellLoslassen(modellDesWarboss, start)

    assert schlachtInDerBewegungsphase.stelle(modellDesWarboss) == start


def testBew1_7DieStellenBeimLoslassenSindDieStellenDesEinenModells(
    schlachtInDerBewegungsphase, warboss
):
    (modell,) = warboss.modelle
    ziel = versetzt(schlachtInDerBewegungsphase.stelle(modell), ausDerZoneHinaus)

    stellen = schlachtInDerBewegungsphase.stellenBeimLoslassen(modell, ziel)

    assert stellen == {modell: ziel}


def testBew1_7DieStellenBeimLoslassenSindBeiDerGanzenEinheitDieStellenJedesModells(
    schlachtInDerBewegungsphase, boyz
):
    schlachtInDerBewegungsphase.auswählen(boyz)
    gezogenes, *_ = boyz.modelle
    davor = jetzigeStellen(schlachtInDerBewegungsphase, boyz)
    ziel = versetzt(davor[gezogenes], schrägOhneHindernis)

    stellen = schlachtInDerBewegungsphase.stellenBeimLoslassen(gezogenes, ziel)

    assert stellen == stellenVersetzt(davor, schrägOhneHindernis)


def testBew1_7DieStellenBeimLoslassenÄndernNichtsAmSpielstand(schlachtInDerBewegungsphase, boyz):
    schlachtInDerBewegungsphase.auswählen(boyz)
    gezogenes, *_ = boyz.modelle
    davor = jetzigeStellen(schlachtInDerBewegungsphase, boyz)
    ziel = versetzt(davor[gezogenes], schrägOhneHindernis)

    schlachtInDerBewegungsphase.stellenBeimLoslassen(gezogenes, ziel)

    assert jetzigeStellen(schlachtInDerBewegungsphase, boyz) == davor


def testBew1_7DieStellenBeimLoslassenHaltenWeiterAlsDieBewegungsweiteAnDerBewegungsweiteAn(
    schlachtInDerBewegungsphase, warboss
):
    (modell,) = warboss.modelle
    davor = schlachtInDerBewegungsphase.stelle(modell)
    ziel = versetzt(davor, zuWeitNachOsten("Warboss"))

    stellen = schlachtInDerBewegungsphase.stellenBeimLoslassen(modell, ziel)

    (stelle,) = stellen.values()
    assert hältAnDerBewegungsweite(davor, stelle, bewegungsweite("Warboss"))


def testBew1_7DerDienstNenntBeiDerGanzenEinheitDieStellenJedesModells(
    dienstDerSchlacht, beendeteAufstellung, schlachtInDerBewegungsphase, boyz
):
    schlachtInDerBewegungsphase.auswählen(boyz)
    gezogenes, *_ = boyz.modelle
    davor = jetzigeStellen(schlachtInDerBewegungsphase, boyz)
    ziel = versetzt(davor[gezogenes], schrägOhneHindernis)

    antwort = stelleBeimLoslassenAbfragen(
        dienstDerSchlacht, beendeteAufstellung, boyz, gezogenes, ziel
    )

    erwartet = stellenVersetzt(davor, schrägOhneHindernis)
    assert antwort.status_code == HTTPStatus.OK
    assert stellenDerEinheitIm(antwort.get_json(), "Boyz") == stellenDerAbfrage(boyz, erwartet)
    assert len(antwort.get_json()["modelle"]) == len(boyz.modelle)


def testBew1_7DerDienstNenntOhneEbeneEinheitNurDasGezogeneModell(
    dienstDerSchlacht, beendeteAufstellung, schlachtInDerBewegungsphase, warboss
):
    (modell,) = warboss.modelle
    ziel = versetzt(schlachtInDerBewegungsphase.stelle(modell), einigeZoll)

    antwort = stelleBeimLoslassenAbfragen(
        dienstDerSchlacht, beendeteAufstellung, warboss, modell, ziel
    )

    assert antwort.status_code == HTTPStatus.OK
    assert stellenDerEinheitIm(antwort.get_json(), "Warboss") == stellenDerAbfrage(
        warboss, {modell: ziel}
    )
    assert len(antwort.get_json()["modelle"]) == 1


def testBew1_7DerDienstNenntWeiterAlsDieBewegungsweiteDieStelleDesAnhaltensWieDasLoslassen(
    dienstDerSchlacht, beendeteAufstellung, schlachtInDerBewegungsphase, warboss
):
    (modell,) = warboss.modelle
    ziel = versetzt(schlachtInDerBewegungsphase.stelle(modell), zuWeitNachOsten("Warboss"))
    abfrage = stelleBeimLoslassenAbfragen(
        dienstDerSchlacht, beendeteAufstellung, warboss, modell, ziel
    )

    loslassen = modellLoslassen(dienstDerSchlacht, beendeteAufstellung, warboss, modell, ziel)

    gesetzt = {modell: schlachtInDerBewegungsphase.stelle(modell)}
    assert abfrage.status_code == HTTPStatus.OK
    assert loslassen.status_code == HTTPStatus.OK
    assert stellenDerEinheitIm(abfrage.get_json(), "Warboss") == stellenDerAbfrage(warboss, gesetzt)


def testBew1_7DerDienstVerändertBeimAbfragenNichtsAmSpielstand(
    dienstDerSchlacht, beendeteAufstellung, schlachtInDerBewegungsphase, boyz
):
    schlachtInDerBewegungsphase.auswählen(boyz)
    gezogenes, *_ = boyz.modelle
    ziel = versetzt(schlachtInDerBewegungsphase.stelle(gezogenes), schrägOhneHindernis)
    spielstandDavor = spielstandVon(dienstDerSchlacht)

    stelleBeimLoslassenAbfragen(dienstDerSchlacht, beendeteAufstellung, boyz, gezogenes, ziel)

    assert spielstandVon(dienstDerSchlacht) == spielstandDavor


def testBew1_7DerDienstAntwortetBeiEinerSperreWieBeimLoslassenMitDemGrundUndDemStandWieDavor(
    dienstDerSchlacht, beendeteAufstellung, schlachtInDerBewegungsphase, boyz
):
    gezogenes, *_ = boyz.modelle
    ziel = versetzt(schlachtInDerBewegungsphase.stelle(gezogenes), (Fraction(5), nichts))
    spielstandDavor = spielstandVon(dienstDerSchlacht)

    antwort = stelleBeimLoslassenAbfragen(
        dienstDerSchlacht, beendeteAufstellung, boyz, gezogenes, ziel
    )

    assert antwort.status_code == HTTPStatus.CONFLICT
    assert antwort.get_json()["gründe"] == [Grund.überEineBase.value]
    assert antwort.get_json()["spielstand"] == spielstandDavor


@mitMausUndFinger
def testBew1_7DieKarteZeigtBeimHaltenJedesModellDerEinheitDortWoEsBeimLoslassenStehtOhneSperre(
    bildschirm, beendeteAufstellung, schlachtInDerBewegungsphase, boyz, eingabe
):
    schlachtInDerBewegungsphase.auswählen(boyz)
    gezogenes, *_ = boyz.modelle
    davor = schlachtInDerBewegungsphase.stelle(gezogenes)
    ziel = versetzt(davor, schrägOhneHindernis)
    seite = seiteDerSchlachtMitEingabe(
        bildschirm, beendeteAufstellung, schlachtInDerBewegungsphase, eingabe
    )

    gezeigt = haltenUndLosslassen(seite, davor, ziel, eingabe)

    assert gezeigt == stellenAlsZahlen(schlachtInDerBewegungsphase)
    assert sperrmeldungenDerSeite(seite) == []


@mitMausUndFinger
def testBew1_7DieKarteZeigtBeimHaltenNurDasGezogeneModellDortWoEsBeimLoslassenStehtOhneSperre(
    bildschirm, beendeteAufstellung, schlachtInDerBewegungsphase, warboss, eingabe
):
    (modell,) = warboss.modelle
    davor = schlachtInDerBewegungsphase.stelle(modell)
    ziel = versetzt(davor, einigeZoll)
    seite = seiteDerSchlachtMitEingabe(
        bildschirm, beendeteAufstellung, schlachtInDerBewegungsphase, eingabe
    )

    gezeigt = haltenUndLosslassen(seite, davor, ziel, eingabe)

    assert gezeigt == stellenAlsZahlen(schlachtInDerBewegungsphase)
    assert sperrmeldungenDerSeite(seite) == []


@mitMausUndFinger
def testBew1_7DieKarteZeigtWeiterAlsDieBewegungsweiteDasModellAnDerBewegungsweiteOhneSperrmeldung(
    bildschirm, beendeteAufstellung, schlachtInDerBewegungsphase, warboss, eingabe
):
    (modell,) = warboss.modelle
    davor = schlachtInDerBewegungsphase.stelle(modell)
    zuWeit = versetzt(davor, zuWeitNachOsten("Warboss"))
    seite = seiteDerSchlachtMitEingabe(
        bildschirm, beendeteAufstellung, schlachtInDerBewegungsphase, eingabe
    )
    kreiseDavor = kreiseDerKarte(seite)

    halten(seite, davor, zuWeit, eingabe)

    (gezeigt,) = kreiseDerKarte(seite) - kreiseDavor
    assert hältAnDerBewegungsweiteAufEinenPixelGenau(
        seite, davor, gezeigt, bewegungsweite("Warboss")
    )
    assert sperrmeldungenDerSeite(seite) == []
