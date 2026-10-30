from fractions import Fraction

from arbiter.domaene.phasen.bewegung.anhaltenAnDerBewegungsweite import (
    anDerBewegungsweiteAngehalten,
)
from arbiter.domaene.spielobjekte import Stelle
from tests.einheit.modelle import bewegungsweiteDerTestmodelle, modellMit


def stelleAn(inX: int, inY: int) -> Stelle:
    return Stelle(x=Fraction(inX), y=Fraction(inY))


def testEinWegBisZurBewegungsweiteBleibtUnverkürzt(zehnZoll):
    modell = modellMit(zehnZoll)
    anfang = {modell: stelleAn(0, 0)}

    assert anDerBewegungsweiteAngehalten(anfang, (Fraction(5), Fraction(0)), anfang) == {
        modell: stelleAn(5, 0)
    }


def testEinWegÜberDieBewegungsweiteHältHöchstensEinHundertstelDavorAn(zehnZoll):
    modell = modellMit(zehnZoll)
    anfang = {modell: stelleAn(0, 0)}

    (halt,) = anDerBewegungsweiteAngehalten(anfang, (Fraction(9), Fraction(0)), anfang).values()

    assert bewegungsweiteDerTestmodelle - Fraction(1, 100) <= halt.x <= bewegungsweiteDerTestmodelle


def testDieDistanzZähltVomAnfangUndDerBlockHältMitDemWeitestenModellAn(zehnZoll):
    weites, nahes = modellMit(zehnZoll), modellMit(zehnZoll)
    anfang = {weites: stelleAn(0, 0), nahes: stelleAn(0, 10)}
    vorige = {weites: stelleAn(3, 0), nahes: stelleAn(0, 10)}

    halt = anDerBewegungsweiteAngehalten(vorige, (Fraction(5), Fraction(0)), anfang)

    assert bewegungsweiteDerTestmodelle - Fraction(1, 100) <= halt[weites].x
    assert halt[weites].x <= bewegungsweiteDerTestmodelle
    assert halt[nahes].x == halt[weites].x - 3
