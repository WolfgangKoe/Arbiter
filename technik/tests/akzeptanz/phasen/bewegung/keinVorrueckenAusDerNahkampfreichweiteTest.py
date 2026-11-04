"""BEW-22 · Kein Vorrücken aus der Nahkampfreichweite."""

from fractions import Fraction

import pytest
from playwright.sync_api import expect

from tests.akzeptanz.bildschirm import knopfDerSeite, seiteDerSchlachtMitEingabe
from tests.akzeptanz.dienst import spielstandVon
from tests.akzeptanz.handgriffe import versetzt
from tests.akzeptanz.schlacht import (
    anhaltenUndÜbergehen,
    außerhalbDerNahkampfreichweite,
    warbossNebenDenBoyZiehen,
    zurBewegungsphaseDesNächstenZugs,
)
from tests.akzeptanz.vorruecken import ebenen, mitJederEbene

vorrückenKnopf = "Vorrücken"
nichts = Fraction(0)
zweiZollNachOsten = (Fraction(2), nichts)
fünfZollNachOsten = (Fraction(5), nichts)


def boyzNachOstenZiehen(schlacht, boyz):
    erster, *_ = boyz.modelle
    schlacht.auswählen(boyz)
    schlacht.modellLoslassen(erster, versetzt(schlacht.stelle(erster), fünfZollNachOsten))


def overlordZiehen(schlacht, lord, weg):
    ziel = versetzt(schlacht.stelle(lord), weg)
    schlacht.modellLoslassen(lord, ziel)
    assert schlacht.stelle(lord) == ziel, "Der Overlord steht nicht, wo der Test ihn braucht"


@pytest.fixture
def einBoyInDerNahkampfreichweite(schlachtInDerBewegungsphase, boyz, overlord):
    schlacht = schlachtInDerBewegungsphase
    erster, zweiter, *_ = boyz.modelle
    (lord,) = overlord.modelle
    aufDieHöheDesZweitenBoys = (Fraction(-5), schlacht.stelle(zweiter).y - schlacht.stelle(lord).y)
    wegeDesOverlords = (
        aufDieHöheDesZweitenBoys,
        (Fraction(-6), nichts),
        (Fraction(-11, 2), nichts),
    )
    for weg in wegeDesOverlords:
        boyzNachOstenZiehen(schlacht, boyz)
        zurBewegungsphaseDesNächstenZugs(schlacht)
        overlordZiehen(schlacht, lord, weg)
        zurBewegungsphaseDesNächstenZugs(schlacht)
    schlacht.auswählen(boyz)
    anhaltenUndÜbergehen(schlacht, erster, versetzt(schlacht.stelle(erster), fünfZollNachOsten))
    stelleDesOverlords = schlacht.stelle(lord)
    außerhalb = {
        boy
        for boy in boyz.modelle
        if außerhalbDerNahkampfreichweite(schlacht.stelle(boy), boy, stelleDesOverlords, lord)
    }
    assert set(boyz.modelle) - außerhalb == {zweiter}, "Nicht nur der zweite Boy ist in Reichweite"
    return schlacht, boyz


@mitJederEbene
def testBew22_1InDerNahkampfreichweiteBietetArbiterVorrückenNichtAn(inDerNahkampfreichweite, ebene):
    schlacht, einheit = inDerNahkampfreichweite
    ebenen[ebene](schlacht, einheit)

    assert not schlacht.vorrückenAngeboten


@mitJederEbene
def testBew22_1IstNurEinModellInDerNahkampfreichweiteBietetArbiterVorrückenNichtAn(
    einBoyInDerNahkampfreichweite, ebene
):
    schlacht, boyz = einBoyInDerNahkampfreichweite
    ebenen[ebene](schlacht, boyz)

    assert not schlacht.vorrückenAngeboten


def testBew22_1EineAndereEinheitAußerhalbDerNahkampfreichweiteDarfVorrücken(
    inDerNahkampfreichweite, spielerEins, boyz, necronWarriors
):
    schlacht, _ = inDerNahkampfreichweite
    andereEinheit = boyz if schlacht.amZug is spielerEins else necronWarriors
    schlacht.auswählen(andereEinheit)

    assert schlacht.vorrückenAngeboten


def testBew22_1NebenEinemModellDesselbenSpielersBietetArbiterVorrückenAn(
    schlachtInDerBewegungsphase, warboss, boyz
):
    _, boy, *_ = boyz.modelle
    (boss,) = warboss.modelle
    stelleDesWarboss = warbossNebenDenBoyZiehen(
        schlachtInDerBewegungsphase, warboss, boy, zweiZollNachOsten
    )
    stelleDesBoys = schlachtInDerBewegungsphase.stelle(boy)
    außerhalb = außerhalbDerNahkampfreichweite(stelleDesWarboss, boss, stelleDesBoys, boy)
    assert not außerhalb, "Der Warboss steht nicht in Nahkampfreichweite des Boys"
    schlachtInDerBewegungsphase.auswählen(warboss)

    assert schlachtInDerBewegungsphase.vorrückenAngeboten


def testBew22_1DerDienstNenntInDerNahkampfreichweiteVorrückenNichtAngeboten(
    dienstDerSchlacht, inDerNahkampfreichweite
):
    schlacht, einheit = inDerNahkampfreichweite
    schlacht.auswählen(einheit)

    spielstand = spielstandVon(dienstDerSchlacht)

    assert spielstand["schlacht"]["vorrücken"] == {"angeboten": False, "zurücknehmen": False}


def testBew22_1DieSeiteZeigtInDerNahkampfreichweiteKeinenKnopfVorrücken(
    bildschirm, beendeteAufstellung, inDerNahkampfreichweite
):
    schlacht, einheit = inDerNahkampfreichweite
    schlacht.auswählen(einheit)

    seite = seiteDerSchlachtMitEingabe(bildschirm, beendeteAufstellung, schlacht, "maus")

    expect(knopfDerSeite(seite, "Phase beenden")).to_have_count(1)
    expect(knopfDerSeite(seite, vorrückenKnopf)).to_have_count(0)
