from fractions import Fraction

import pytest

from arbiter.domaene.missionsvorbereitung.ausgangslage import Formation
from arbiter.domaene.phasen.aufstellen.setzenPerKlick import (
    formationDerEinheit,
    stellenDerFormation,
)
from arbiter.domaene.spielobjekte import Einheit, Stelle
from tests.einheit.modelle import testmodell

weitesFeld = (Fraction(-1000), Fraction(1000))


def testEineFormationStelltEineReiheMittigBaseAnBaseAuf(zehnZoll):
    formation = Formation(reihen=(2,), abstand=Fraction(0))
    mitte = Stelle(x=Fraction(20), y=Fraction(20))

    stellen = stellenDerFormation(formation, zehnZoll, mitte, weitesFeld, weitesFeld)

    assert stellen == [
        Stelle(x=Fraction(20), y=Fraction(15)),
        Stelle(x=Fraction(20), y=Fraction(25)),
    ]


def testEineFormationAusEinerReiheRechnetExaktMitBruchzahlen(zehnZoll):
    formation = Formation(reihen=(2,), abstand=Fraction(0))
    mitte = Stelle(x=Fraction(1, 3), y=Fraction(20))

    stellen = stellenDerFormation(formation, zehnZoll, mitte, weitesFeld, weitesFeld)

    assert [stelle.x for stelle in stellen] == [Fraction(1, 3), Fraction(1, 3)]


def testEineFormationLässtZwischenDenBasesDenAbstandDerFormation(zehnZoll):
    formation = Formation(reihen=(2,), abstand=Fraction(1))
    mitte = Stelle(x=Fraction(20), y=Fraction(20))

    stellen = stellenDerFormation(formation, zehnZoll, mitte, weitesFeld, weitesFeld)

    assert stellen == [
        Stelle(x=Fraction(20), y=Fraction(29, 2)),
        Stelle(x=Fraction(20), y=Fraction(51, 2)),
    ]


def testEineFormationRücktInDieGrenzen(zehnZoll):
    formation = Formation(reihen=(2,), abstand=Fraction(0))
    mitte = Stelle(x=Fraction(20), y=Fraction(20))
    nurBisAchtzehn = (Fraction(0), Fraction(18))

    stellen = stellenDerFormation(formation, zehnZoll, mitte, weitesFeld, nurBisAchtzehn)

    assert stellen == [
        Stelle(x=Fraction(20), y=Fraction(3)),
        Stelle(x=Fraction(20), y=Fraction(13)),
    ]


def testEineFormationSetztDieNächsteReiheEinenSchrittDahinter(zehnZoll):
    formation = Formation(reihen=(1, 1), abstand=Fraction(0))
    mitte = Stelle(x=Fraction(20), y=Fraction(20))

    stellen = stellenDerFormation(formation, zehnZoll, mitte, weitesFeld, weitesFeld)

    assert stellen == [
        Stelle(x=Fraction(15), y=Fraction(20)),
        Stelle(x=Fraction(25), y=Fraction(20)),
    ]


def testEineVersetzteNächsteReiheStehtAufEinHundertstelGenauAmKleinstenAbstand(zehnZoll):
    formation = Formation(reihen=(2, 1), abstand=Fraction(0))
    mitte = Stelle(x=Fraction(20), y=Fraction(20))
    halberAbstand = Fraction(867, 200)

    stellen = stellenDerFormation(formation, zehnZoll, mitte, weitesFeld, weitesFeld)

    assert stellen == [
        Stelle(x=Fraction(20) - halberAbstand, y=Fraction(15)),
        Stelle(x=Fraction(20) - halberAbstand, y=Fraction(25)),
        Stelle(x=Fraction(20) + halberAbstand, y=Fraction(20)),
    ]


def testEineFormationMitAndererModellzahlAlsDieEinheitIstEineVorbedingungsverletzung(zehnZoll):
    formation = Formation(reihen=(3,), abstand=Fraction(0))
    einheit = Einheit(name="Einheit", modelle=(testmodell(zehnZoll), testmodell(zehnZoll)))
    mitte = Stelle(x=Fraction(20), y=Fraction(20))

    with pytest.raises(ValueError):
        formationDerEinheit(einheit, mitte, {"Einheit": formation}, (weitesFeld, weitesFeld))
