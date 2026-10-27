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
    spielstandVon,
    stelleBeimLoslassenAbfragen,
    stelleImSpielstand,
    stellenDerAbfrage,
    stellenDerEinheitIm,
)
from tests.akzeptanz.handgriffe import millionstel, sperrgründe, versetzt
from tests.akzeptanz.schlacht import (
    bewegungsweite,
    jetzigeStellen,
    ostenUndNorden,
    schrägOhneHindernis,
    stellenAlsZahlen,
    stellenVersetzt,
)
from tests.akzeptanz.ziehen import (
    Abfragen,
    aufDieAntwortenWarten,
    halten,
    haltenUndLosslassen,
    mitMausUndFinger,
    punktAufDerKarte,
)

nichts = Fraction(0)
einigeZoll = (Fraction(3), nichts)
ausDerZoneHinaus = (Fraction(9, 2), nichts)
fünfZoll = Fraction(5)


def testBew1_1DasGezogeneModellMachtSeineEinheitZurEinheitInBewegung(
    schlachtInDerBewegungsphase, warboss
):
    (modell,) = warboss.modelle
    ziel = versetzt(schlachtInDerBewegungsphase.stelle(modell), einigeZoll)

    schlachtInDerBewegungsphase.modellLoslassen(modell, ziel)

    assert schlachtInDerBewegungsphase.einheitInBewegung is warboss


def testBew1_1DasModellStehtDanachAnDerStelleDesLoslassens(schlachtInDerBewegungsphase, warboss):
    (modell,) = warboss.modelle
    ziel = versetzt(schlachtInDerBewegungsphase.stelle(modell), einigeZoll)

    schlachtInDerBewegungsphase.modellLoslassen(modell, ziel)

    assert schlachtInDerBewegungsphase.stelle(modell) == ziel


def testBew1_1IstDieGanzeEinheitEbeneRücktJedesModellUmDieselbeStreckeVor(
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


def testBew1_1IstDieEinheitNichtAusgewähltStehenDieAnderenModelleWieDavor(
    schlachtInDerBewegungsphase, boyz
):
    *übrige, gezogenes = boyz.modelle
    davor = jetzigeStellen(schlachtInDerBewegungsphase, boyz)
    ziel = versetzt(davor[gezogenes], (Fraction(2), nichts))

    schlachtInDerBewegungsphase.modellLoslassen(gezogenes, ziel)

    assert schlachtInDerBewegungsphase.stelle(gezogenes) == ziel
    assert all(schlachtInDerBewegungsphase.stelle(modell) == davor[modell] for modell in übrige)


def testBew1_1ArbiterRücktDasModellNichtInDieAufstellungszone(schlachtInDerBewegungsphase, warboss):
    (modell,) = warboss.modelle
    ziel = versetzt(schlachtInDerBewegungsphase.stelle(modell), ausDerZoneHinaus)

    schlachtInDerBewegungsphase.modellLoslassen(modell, ziel)

    assert schlachtInDerBewegungsphase.stelle(modell) == ziel


def testBew1_1FehlendeKohärenzSperrtBeimLoslassenNicht(schlachtInDerBewegungsphase, boyz):
    *_, gezogenes = boyz.modelle
    ziel = versetzt(schlachtInDerBewegungsphase.stelle(gezogenes), (fünfZoll, nichts))

    schlachtInDerBewegungsphase.modellLoslassen(gezogenes, ziel)

    assert schlachtInDerBewegungsphase.einheitInBewegung is boyz
    assert not schlachtInDerBewegungsphase.inKohärenz(boyz)


def testBew1_2OhneKohärenzSperrtBewegungDerEinheitBeendenMitDemGrundKeineKohärenz(
    schlachtInDerBewegungsphase, boyz
):
    *_, gezogenes = boyz.modelle
    ziel = versetzt(schlachtInDerBewegungsphase.stelle(gezogenes), (fünfZoll, nichts))
    schlachtInDerBewegungsphase.modellLoslassen(gezogenes, ziel)
    davor = jetzigeStellen(schlachtInDerBewegungsphase, boyz)

    gründe = sperrgründe(schlachtInDerBewegungsphase.bewegungDerEinheitBeenden)

    assert gründe == {Grund.keineKohärenz}
    assert schlachtInDerBewegungsphase.einheitInBewegung is boyz
    assert jetzigeStellen(schlachtInDerBewegungsphase, boyz) == davor


def testBew1_3GelingtDasBeendenGibtEsKeineEinheitInBewegung(schlachtInDerBewegungsphase, warboss):
    (modell,) = warboss.modelle
    ziel = versetzt(schlachtInDerBewegungsphase.stelle(modell), einigeZoll)
    schlachtInDerBewegungsphase.modellLoslassen(modell, ziel)

    schlachtInDerBewegungsphase.bewegungDerEinheitBeenden()

    assert schlachtInDerBewegungsphase.einheitInBewegung is None


def testBew1_3GelingtDasBeendenEinerGanzenEinheitInKohärenzGibtEsKeineEinheitInBewegung(
    schlachtInDerBewegungsphase, boyz
):
    schlachtInDerBewegungsphase.auswählen(boyz)
    gezogenes, *_ = boyz.modelle
    ziel = versetzt(schlachtInDerBewegungsphase.stelle(gezogenes), ostenUndNorden)
    schlachtInDerBewegungsphase.modellLoslassen(gezogenes, ziel)

    schlachtInDerBewegungsphase.bewegungDerEinheitBeenden()

    assert schlachtInDerBewegungsphase.einheitInBewegung is None


def testBew1_4DieStellenBeimLoslassenSindDieStellenDesEinenModells(
    schlachtInDerBewegungsphase, warboss
):
    (modell,) = warboss.modelle
    ziel = versetzt(schlachtInDerBewegungsphase.stelle(modell), ausDerZoneHinaus)

    stellen = schlachtInDerBewegungsphase.stellenBeimLoslassen(modell, ziel)

    assert stellen == {modell: ziel}


def testBew1_4DieStellenBeimLoslassenSindBeiDerGanzenEinheitDieStellenJedesModells(
    schlachtInDerBewegungsphase, boyz
):
    schlachtInDerBewegungsphase.auswählen(boyz)
    gezogenes, *_ = boyz.modelle
    davor = jetzigeStellen(schlachtInDerBewegungsphase, boyz)
    ziel = versetzt(davor[gezogenes], schrägOhneHindernis)

    stellen = schlachtInDerBewegungsphase.stellenBeimLoslassen(gezogenes, ziel)

    assert stellen == stellenVersetzt(davor, schrägOhneHindernis)


def testBew1_4DieStellenBeimLoslassenÄndernNichtsAmSpielstand(schlachtInDerBewegungsphase, boyz):
    schlachtInDerBewegungsphase.auswählen(boyz)
    gezogenes, *_ = boyz.modelle
    davor = jetzigeStellen(schlachtInDerBewegungsphase, boyz)
    ziel = versetzt(davor[gezogenes], schrägOhneHindernis)

    schlachtInDerBewegungsphase.stellenBeimLoslassen(gezogenes, ziel)

    assert jetzigeStellen(schlachtInDerBewegungsphase, boyz) == davor
    assert schlachtInDerBewegungsphase.einheitInBewegung is None


def testBew1_4DerDienstNenntBeiDerGanzenEinheitDieStellenJedesModells(
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


def testBew1_4DerDienstNenntOhneEbeneEinheitNurDasGezogeneModell(
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


def testBew1_4DerDienstVerändertBeimAbfragenNichtsAmSpielstand(
    dienstDerSchlacht, beendeteAufstellung, schlachtInDerBewegungsphase, boyz
):
    schlachtInDerBewegungsphase.auswählen(boyz)
    gezogenes, *_ = boyz.modelle
    ziel = versetzt(schlachtInDerBewegungsphase.stelle(gezogenes), schrägOhneHindernis)
    spielstandDavor = spielstandVon(dienstDerSchlacht)

    stelleBeimLoslassenAbfragen(dienstDerSchlacht, beendeteAufstellung, boyz, gezogenes, ziel)

    assert spielstandVon(dienstDerSchlacht) == spielstandDavor


def testBew1_4DerDienstAntwortetBeiEinerSperreWieBeimLoslassenMitDemGrundUndDemStandWieDavor(
    dienstDerSchlacht, beendeteAufstellung, schlachtInDerBewegungsphase, warboss
):
    (modell,) = warboss.modelle
    weg = (bewegungsweite("Warboss") + millionstel, nichts)
    ziel = versetzt(schlachtInDerBewegungsphase.stelle(modell), weg)
    spielstandDavor = spielstandVon(dienstDerSchlacht)

    antwort = stelleBeimLoslassenAbfragen(
        dienstDerSchlacht, beendeteAufstellung, warboss, modell, ziel
    )

    assert antwort.status_code == HTTPStatus.CONFLICT
    assert antwort.get_json()["gründe"] == [Grund.weiterAlsB.value]
    assert antwort.get_json()["spielstand"] == spielstandDavor


@mitMausUndFinger
def testBew1_4DieKarteZeigtBeimHaltenJedesModellDerEinheitDortWoEsBeimLoslassenStehtOhneSperre(
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
def testBew1_4DieKarteZeigtBeimHaltenNurDasGezogeneModellDortWoEsBeimLoslassenStehtOhneSperre(
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
def testBew1_4DieKarteZeigtBeimHaltenWeiterAlsBDieLetzteStelleOhneSperreOhneSperrmeldung(
    bildschirm, beendeteAufstellung, schlachtInDerBewegungsphase, warboss, eingabe
):
    (modell,) = warboss.modelle
    davor = schlachtInDerBewegungsphase.stelle(modell)
    erlaubt = versetzt(davor, einigeZoll)
    zuWeit = versetzt(davor, (bewegungsweite("Warboss") + 1, nichts))
    seite = seiteDerSchlachtMitEingabe(
        bildschirm, beendeteAufstellung, schlachtInDerBewegungsphase, eingabe
    )
    zeiger = halten(seite, davor, erlaubt, eingabe)
    gezeigtBeiErlaubt = kreiseDerKarte(seite)
    abfragen = Abfragen(seite)

    zeiger.bewegen(punktAufDerKarte(seite, zuWeit))
    aufDieAntwortenWarten(seite, abfragen)

    assert stelleImSpielstand(davor) not in gezeigtBeiErlaubt
    assert kreiseDerKarte(seite) == gezeigtBeiErlaubt
    assert sperrmeldungenDerSeite(seite) == []
