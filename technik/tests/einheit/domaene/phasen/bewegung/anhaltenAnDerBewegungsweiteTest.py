from fractions import Fraction

from arbiter.domaene.phasen.bewegung.anhaltenAnDerBewegungsweite import (
    anDerBewegungsweiteAngehalten,
)
from arbiter.domaene.spielobjekte import Stelle
from tests.einheit.modelle import bewegungsweiteDerTestmodelle, testmodell


def stelleAn(inX: int, inY: int) -> Stelle:
    return Stelle(x=Fraction(inX), y=Fraction(inY))


def testEinWegBisZurBewegungsweiteBleibtUnverkürzt(zehnZoll):
    modell = testmodell(zehnZoll)
    neue = {modell: stelleAn(5, 0)}

    assert (
        anDerBewegungsweiteAngehalten({modell: stelleAn(0, 0)}, neue, {modell: stelleAn(0, 0)})
        == neue
    )


def testEinWegÜberDieBewegungsweiteHältHöchstensEinHundertstelDavorAn(zehnZoll):
    modell = testmodell(zehnZoll)
    anfang = {modell: stelleAn(0, 0)}

    (halt,) = anDerBewegungsweiteAngehalten(anfang, {modell: stelleAn(9, 0)}, anfang).values()

    assert bewegungsweiteDerTestmodelle - Fraction(1, 100) <= halt.x <= bewegungsweiteDerTestmodelle


def testDieDistanzZähltVomAnfangUndDerBlockHältMitDemWeitestenModellAn(zehnZoll):
    weites, nahes = testmodell(zehnZoll), testmodell(zehnZoll)
    anfang = {weites: stelleAn(0, 0), nahes: stelleAn(0, 10)}
    vorige = {weites: stelleAn(3, 0), nahes: stelleAn(0, 10)}
    neue = {weites: stelleAn(8, 0), nahes: stelleAn(5, 10)}

    halt = anDerBewegungsweiteAngehalten(vorige, neue, anfang)

    assert Fraction(49, 10) <= halt[weites].x <= bewegungsweiteDerTestmodelle
    assert halt[nahes].x == halt[weites].x - 3
