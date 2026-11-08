"""BEW-19 · Einheit als Ganzes ziehen."""

from fractions import Fraction

from tests.akzeptanz.handgriffe import radiusInZoll, versetzt
from tests.akzeptanz.schlacht import jetzigeStellen, stellenVersetzt


def testBew19_1BeiDerEinheitenebeneSperrtKeinModellDasModellDerselbenEinheitAnDerVorigenStelle(
    schlachtInDerBewegungsphase, boyz
):
    schlachtInDerBewegungsphase.auswählen(boyz)
    gezogenes, *_ = boyz.modelle
    davor = jetzigeStellen(schlachtInDerBewegungsphase, boyz)
    wenigerAlsDerDurchmesser = (Fraction(0), radiusInZoll(gezogenes))
    ziel = versetzt(davor[gezogenes], wenigerAlsDerDurchmesser)

    schlachtInDerBewegungsphase.modellLoslassen(gezogenes, ziel)

    assert jetzigeStellen(schlachtInDerBewegungsphase, boyz) == stellenVersetzt(
        davor, wenigerAlsDerDurchmesser
    )
