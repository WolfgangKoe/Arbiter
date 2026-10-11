"""AUF-8 · Ziehen."""

from fractions import Fraction
from operator import attrgetter

import pytest

from arbiter.domaene import messen
from arbiter.domaene.sperre import Grund
from arbiter.domaene.spielobjekte import Stelle
from tests.akzeptanz.handgriffe import (
    einheitAufstellen,
    nachDerWahlDerAufstellungszone,
    radiusInZoll,
    reihenDerFormation,
    sperrgründe,
    stelleDesErstenModells,
    stelleInDerZoneVon,
    stellenDerEinheit,
)

# Warum: Schon ein Millionstel Zoll entscheidet, damit Grenzfälle ohne Toleranz gelten.
millionstel = Fraction(1, 1_000_000)
abstandInDerFormation = Fraction(3, 2)
mitteDerZone = Stelle(x=Fraction(40), y=Fraction(30))


def gesetzteStellen(aufstellung, einheit) -> list[Stelle]:
    return [aufstellung.stelle(modell) for modell in einheit.modelle if aufstellung.gesetzt(modell)]


def mittelwert(werte: list[Fraction]) -> Fraction:
    return sum(werte) / len(werte)


def reihenNachX(stellen: list[Stelle]) -> list[list[Stelle]]:
    xWerte = sorted({stelle.x for stelle in stellen})
    return [
        sorted((kandidat for kandidat in stellen if kandidat.x == wert), key=attrgetter("y"))
        for wert in xWerte
    ]


def testAuf8_2EinGesetztesModellIstNachDemLoslassenAnDerStelleDesLoslassensGesetzt(
    aufstellung, ersterSpieler, zweiterSpieler
):
    nachDerWahlDerAufstellungszone(aufstellung, gewinner=ersterSpieler)
    einheit, _ = zweiterSpieler.armee.einheiten
    modell, _ = einheit.modelle
    aufstellung.modellSetzen(modell, stelleDesErstenModells(aufstellung, zweiterSpieler, einheit))
    stelleDesLoslassens = stelleInDerZoneVon(aufstellung, zweiterSpieler, 4, 20)

    aufstellung.modellLoslassen(modell, stelleDesLoslassens)

    assert aufstellung.gesetzt(modell)
    assert aufstellung.stelle(modell) == stelleDesLoslassens
    assert not aufstellung.gesperrt(modell)


def testAuf8_3EinGesetztesModellDerEinheitInAufstellungIstNachDemZurücklegenNichtGesetzt(
    aufstellung, ersterSpieler, zweiterSpieler
):
    nachDerWahlDerAufstellungszone(aufstellung, gewinner=ersterSpieler)
    einheit, _ = zweiterSpieler.armee.einheiten
    erstesModell, zweitesModell = einheit.modelle
    (_, ersteStelle), (_, zweiteStelle) = stellenDerEinheit(aufstellung, zweiterSpieler, einheit)
    aufstellung.modellSetzen(erstesModell, ersteStelle)
    aufstellung.modellSetzen(zweitesModell, zweiteStelle)

    aufstellung.modellZurücklegen(zweitesModell, zweiterSpieler)

    assert not aufstellung.gesetzt(zweitesModell)
    assert aufstellung.stelle(zweitesModell) is None
    assert aufstellung.stelle(erstesModell) == ersteStelle


@pytest.mark.parametrize("ablage", ["eigeneAblage", "ablageDesAnderen"])
def testAuf8_4EinModellEinerAufgestelltenEinheitIstAufEinerAblageNichtWählbar(
    aufstellung, ersterSpieler, zweiterSpieler, ablage
):
    nachDerWahlDerAufstellungszone(aufstellung, gewinner=ersterSpieler)
    aufgestellteEinheit, _ = zweiterSpieler.armee.einheiten
    modell, _ = aufgestellteEinheit.modelle
    einheitAufstellen(aufstellung, aufgestellteEinheit)
    stelleDavor = aufstellung.stelle(modell)
    spielerDerAblage = zweiterSpieler if ablage == "eigeneAblage" else ersterSpieler

    gründe = sperrgründe(aufstellung.modellZurücklegen, modell, spielerDerAblage)

    assert gründe == {Grund.nichtWählbar}
    assert aufstellung.stelle(modell) == stelleDavor


def testAuf8_5DieEinheitKommtMitAllenModellenAufDieKarte(aufstellungNachDerZonenwahl, boyz):
    aufstellungNachDerZonenwahl.einheitLoslassen(boyz, mitteDerZone)

    assert len(gesetzteStellen(aufstellungNachDerZonenwahl, boyz)) == len(boyz.modelle)
    assert aufstellungNachDerZonenwahl.einheitInAufstellung is boyz


def testAuf8_5DieReihenDerFormationLiegenParallelZurSpielfeldkanteDerZone(
    aufstellungNachDerZonenwahl, boyz
):
    aufstellungNachDerZonenwahl.einheitLoslassen(boyz, mitteDerZone)

    reihen = reihenNachX(gesetzteStellen(aufstellungNachDerZonenwahl, boyz))
    assert [len(reihe) for reihe in reihen] == reihenDerFormation("Boyz")


def testAuf8_5BenachbarteBasesEinerReiheHabenDenAbstandEinsKommaFünfZoll(
    aufstellungNachDerZonenwahl, boyz
):
    modell, *_ = boyz.modelle
    aufstellungNachDerZonenwahl.einheitLoslassen(boyz, mitteDerZone)

    reihen = reihenNachX(gesetzteStellen(aufstellungNachDerZonenwahl, boyz))
    paare = [
        (links, rechts) for reihe in reihen for links, rechts in zip(reihe, reihe[1:], strict=False)
    ]
    base = modell.base
    genau = [
        messen.abstandHöchstens(base, linker, base, rechter, abstandInDerFormation)
        for linker, rechter in paare
    ]
    nicht = [
        messen.abstandHöchstens(base, linker, base, rechter, abstandInDerFormation - millionstel)
        for linker, rechter in paare
    ]
    assert all(genau)
    assert not any(nicht)


def testAuf8_5SchrägBenachbarteBasesHabenMindestensEinsKommaFünfZollBeiReihenAufEinHundertstelGenau(
    aufstellungNachDerZonenwahl, boyz
):
    modell, *_ = boyz.modelle
    aufstellungNachDerZonenwahl.einheitLoslassen(boyz, mitteDerZone)

    reihen = reihenNachX(gesetzteStellen(aufstellungNachDerZonenwahl, boyz))
    paareJeNachbarreihen = [
        [(links, rechts) for links in vordere for rechts in hintere]
        for vordere, hintere in zip(reihen, reihen[1:], strict=False)
    ]
    base = modell.base
    unterschritten = [
        messen.abstandHöchstens(base, links, base, rechts, abstandInDerFormation - millionstel)
        for paare in paareJeNachbarreihen
        for links, rechts in paare
    ]
    zuWeit = [
        not any(
            messen.abstandHöchstens(
                base, links, base, rechts, abstandInDerFormation + Fraction(1, 100)
            )
            for links, rechts in paare
        )
        for paare in paareJeNachbarreihen
    ]
    reihenabstände = [
        hintere[0].x - vordere[0].x for vordere, hintere in zip(reihen, reihen[1:], strict=False)
    ]
    assert not any(unterschritten)
    assert not any(zuWeit)
    assert all((abstand * 100).denominator == 1 for abstand in reihenabstände)


def testAuf8_5DieFormationLiegtMittigAnDerStelleDesLoslassens(aufstellungNachDerZonenwahl, boyz):
    aufstellungNachDerZonenwahl.einheitLoslassen(boyz, mitteDerZone)

    stellen = gesetzteStellen(aufstellungNachDerZonenwahl, boyz)
    assert mittelwert([stelle.x for stelle in stellen]) == mitteDerZone.x
    assert mittelwert([stelle.y for stelle in stellen]) == mitteDerZone.y


def testAuf8_5EineEinheitAusEinemModellStehtAnDerStelleDesLoslassens(
    aufstellungNachDerZonenwahl, warboss
):
    aufstellungNachDerZonenwahl.einheitLoslassen(warboss, mitteDerZone)

    assert gesetzteStellen(aufstellungNachDerZonenwahl, warboss) == [mitteDerZone]


@pytest.mark.parametrize(
    ("stelle", "ändertSich"),
    [
        (Stelle(x=Fraction(44), y=Fraction(30)), "x"),
        (Stelle(x=Fraction(20), y=Fraction(30)), "x"),
        (Stelle(x=Fraction(40), y=Fraction(0)), "y"),
        (Stelle(x=Fraction(40), y=Fraction(60)), "y"),
    ],
    ids=["überDieSpielfeldkante", "zurSpielfeldmitteHin", "überDieKurzeKanteAmAnfang", "amEnde"],
)
def testAuf8_6RagtDieFormationAusDerZoneRücktSieAufKürzestemWegHinein(
    aufstellungNachDerZonenwahl, boyz, stelle, ändertSich
):
    aufstellungNachDerZonenwahl.einheitLoslassen(boyz, stelle)

    stellen = gesetzteStellen(aufstellungNachDerZonenwahl, boyz)
    grenzen = aufstellungNachDerZonenwahl.ausgangslage.grenzenDerZone(
        aufstellungNachDerZonenwahl.aufstellungszone(aufstellungNachDerZonenwahl.anDerReihe)
    )
    erstesModell, *_ = boyz.modelle
    radius = radiusInZoll(erstesModell)
    assert all(
        messen.ganzIn(modell.base, ort, *grenzen)
        for modell, ort in zip(boyz.modelle, stellen, strict=True)
    )
    unveränderteAchse = stelle.y if ändertSich == "x" else stelle.x
    mittlereAchse = mittelwert([ort.y if ändertSich == "x" else ort.x for ort in stellen])
    assert mittlereAchse == unveränderteAchse
    # Warum: Auf kürzestem Weg heißt, eine Base berührt danach die Grenze der Zone
    ränder = [
        rand
        for ort in stellen
        for rand in (ort.x - radius, ort.x + radius, ort.y - radius, ort.y + radius)
    ]
    grenzwerte = {*grenzen[0], *grenzen[1]}
    assert grenzwerte & set(ränder)
