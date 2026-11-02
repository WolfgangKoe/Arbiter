"""BEW-25 · Weiterziehen nach dem Übergehen."""

from fractions import Fraction
from http import HTTPStatus

import pytest

from tests.akzeptanz.dienst import modellLoslassen
from tests.akzeptanz.handgriffe import radiusInZoll, versetzt
from tests.akzeptanz.schlacht import (
    anhaltenUndÜbergehen,
    aufeinanderZuZiehen,
    bewegungsweite,
    jetzigeStellen,
    zehnZollNachOsten,
)

nichts = Fraction(0)
halberZoll = Fraction(1, 2)
zweiZollNachOsten = (Fraction(2), nichts)
zweiZollNachWesten = (Fraction(-2), nichts)
einZollNachSüden = (nichts, Fraction(1))


def übergangenVorDemOverlord(schlacht, warboss, overlord, abstand: Fraction, weg: Fraction):
    (boss,) = warboss.modelle
    (modellDesAnderenSpielers,) = overlord.modelle
    aufeinanderZuZiehen(schlacht, boss, modellDesAnderenSpielers, abstand)
    anhaltenUndÜbergehen(schlacht, boss, versetzt(schlacht.stelle(boss), (weg, nichts)))
    return boss


@pytest.mark.parametrize(
    ("abstand", "weg"),
    [(Fraction(12), Fraction(8)), (Fraction(3), Fraction(5, 2)), (Fraction(7), Fraction(13, 2))],
    ids=["überDerBewegungsweite", "inDerNahkampfreichweite", "beide"],
)
def testBew25_1ZiehtEinÜbergangenesModellWeiterHältArbiterEsAnDerVorigenStelleAn(
    schlachtInDerBewegungsphase, warboss, overlord, abstand, weg
):
    boss = übergangenVorDemOverlord(schlachtInDerBewegungsphase, warboss, overlord, abstand, weg)
    vorige = schlachtInDerBewegungsphase.stelle(boss)

    schlachtInDerBewegungsphase.modellLoslassen(boss, versetzt(vorige, zweiZollNachWesten))

    assert schlachtInDerBewegungsphase.stelle(boss) == vorige
    assert schlachtInDerBewegungsphase.gemeinsamÜbergehenAngeboten is True


@pytest.mark.parametrize(
    "weg",
    [zweiZollNachOsten, zweiZollNachWesten, (Fraction(-10), nichts)],
    ids=["weiter", "zurück", "zurückZumStart"],
)
def testBew25_1ÜberDerBewegungsweiteHältArbiterInJedeRichtungAnDerVorigenStelleAn(
    schlachtInDerBewegungsphase, warboss, weg
):
    (boss,) = warboss.modelle
    ziel = versetzt(schlachtInDerBewegungsphase.stelle(boss), zehnZollNachOsten)
    anhaltenUndÜbergehen(schlachtInDerBewegungsphase, boss, ziel)

    schlachtInDerBewegungsphase.modellLoslassen(boss, versetzt(ziel, weg))

    assert schlachtInDerBewegungsphase.stelle(boss) == ziel


def testBew25_1IstDieGanzeEinheitEbeneHältDerBlockAnWennEinesÜberDerBewegungsweiteSteht(
    schlachtInDerBewegungsphase, boyz
):
    erster, *_, letzter = boyz.modelle
    anhaltenUndÜbergehen(
        schlachtInDerBewegungsphase,
        letzter,
        versetzt(schlachtInDerBewegungsphase.stelle(letzter), zehnZollNachOsten),
    )
    schlachtInDerBewegungsphase.auswählen(boyz)
    davor = jetzigeStellen(schlachtInDerBewegungsphase, boyz)

    schlachtInDerBewegungsphase.modellLoslassen(erster, versetzt(davor[erster], einZollNachSüden))

    assert jetzigeStellen(schlachtInDerBewegungsphase, boyz) == davor


def testBew25_1EinAnderesModellZiehtNachDemÜbergehenOhneAnzuhalten(
    schlachtInDerBewegungsphase, warboss, boyz
):
    (boss,) = warboss.modelle
    anhaltenUndÜbergehen(
        schlachtInDerBewegungsphase,
        boss,
        versetzt(schlachtInDerBewegungsphase.stelle(boss), zehnZollNachOsten),
    )
    *_, letzter = boyz.modelle
    ziel = versetzt(schlachtInDerBewegungsphase.stelle(letzter), einZollNachSüden)

    schlachtInDerBewegungsphase.modellLoslassen(letzter, ziel)

    assert schlachtInDerBewegungsphase.stelle(letzter) == ziel
    assert schlachtInDerBewegungsphase.gemeinsamÜbergehenAngeboten is False


def nachDemÜbergehenVorgerücktMit(schlacht, warboss, wurf: int):
    (boss,) = warboss.modelle
    start = schlacht.stelle(boss)
    ziel = versetzt(start, zehnZollNachOsten)
    anhaltenUndÜbergehen(schlacht, boss, ziel)
    schlacht.auswählen(warboss)
    schlacht.vorrücken()
    imKreisDesWurfs = bewegungsweite("Warboss", "Warboss") + radiusInZoll(boss) + wurf - halberZoll
    schlacht.karteAnklicken(versetzt(start, (nichts, imKreisDesWurfs)))
    return boss, ziel


def testBew25_1NachDemVorrückwurfHältArbiterÜberBewegungsweitePlusWurfAn(
    schlachtInDerBewegungsphase, warboss
):
    boss, vorige = nachDemÜbergehenVorgerücktMit(schlachtInDerBewegungsphase, warboss, 1)

    schlachtInDerBewegungsphase.modellLoslassen(boss, versetzt(vorige, zweiZollNachWesten))

    assert schlachtInDerBewegungsphase.stelle(boss) == vorige


def testBew25_1NachDemVorrückwurfZiehtEsInnerhalbVonBewegungsweitePlusWurfWeiter(
    schlachtInDerBewegungsphase, warboss
):
    boss, vorige = nachDemÜbergehenVorgerücktMit(schlachtInDerBewegungsphase, warboss, 6)
    ziel = versetzt(vorige, zweiZollNachWesten)

    schlachtInDerBewegungsphase.modellLoslassen(boss, ziel)

    assert schlachtInDerBewegungsphase.stelle(boss) == ziel


def testBew25_1DerDienstHältAnDerVorigenStelleAnUndNenntDasAngebot(
    dienstDerSchlacht, beendeteAufstellung, schlachtInDerBewegungsphase, warboss
):
    (boss,) = warboss.modelle
    vorige = versetzt(schlachtInDerBewegungsphase.stelle(boss), zehnZollNachOsten)
    anhaltenUndÜbergehen(schlachtInDerBewegungsphase, boss, vorige)

    antwort = modellLoslassen(
        dienstDerSchlacht, beendeteAufstellung, warboss, boss, versetzt(vorige, zweiZollNachOsten)
    )

    assert antwort.status_code == HTTPStatus.OK
    assert antwort.get_json()["schlacht"]["gemeinsamÜbergehen"] == {"angeboten": True}
    assert schlachtInDerBewegungsphase.stelle(boss) == vorige
