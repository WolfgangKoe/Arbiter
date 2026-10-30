from fractions import Fraction

from arbiter.domaene.phasen.bewegung.anhaltenAnDerBewegungsweite import (
    anteilBisZurBewegungsweite,
)
from arbiter.domaene.spielobjekte import Stelle
from tests.einheit.modelle import bewegungsweiteDerTestmodelle, modellMit


def stelleAn(inX: int, inY: int) -> Stelle:
    return Stelle(x=Fraction(inX), y=Fraction(inY))


def testEinWegBisZurBewegungsweiteBleibtUnverkürzt(zehnZoll):
    modell = modellMit(zehnZoll)
    anfang = {modell: stelleAn(0, 0)}

    assert anteilBisZurBewegungsweite(anfang, (Fraction(5), Fraction(0)), anfang) == 1


def testEinWegÜberDieBewegungsweiteHältHöchstensEinHundertstelDavorAn(zehnZoll):
    modell = modellMit(zehnZoll)
    anfang = {modell: stelleAn(0, 0)}
    weg = (Fraction(9), Fraction(0))

    halt = anteilBisZurBewegungsweite(anfang, weg, anfang) * 9

    assert bewegungsweiteDerTestmodelle - Fraction(1, 100) <= halt <= bewegungsweiteDerTestmodelle


def testDieDistanzZähltVomAnfangUndDerBlockHältMitDemWeitestenModellAn(zehnZoll):
    weites, nahes = modellMit(zehnZoll), modellMit(zehnZoll)
    anfang = {weites: stelleAn(0, 0), nahes: stelleAn(0, 10)}
    vorige = {weites: stelleAn(3, 0), nahes: stelleAn(0, 10)}

    halt = 3 + anteilBisZurBewegungsweite(vorige, (Fraction(5), Fraction(0)), anfang) * 5

    assert bewegungsweiteDerTestmodelle - Fraction(1, 100) <= halt <= bewegungsweiteDerTestmodelle
