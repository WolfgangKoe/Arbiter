from fractions import Fraction

from arbiter.domaene.phasen.bewegung import Bewegungsphase
from arbiter.domaene.spielobjekte import Stelle
from tests.einheit.modelle import bewegungsweiteDerTestmodelle, modellMit


def stelleAn(inX: int, inY: int) -> Stelle:
    return Stelle(x=Fraction(inX), y=Fraction(inY))


def testDasZiehenGibtDieNeuenStellenDerEbeneZurück(zehnZoll):
    modell = modellMit(zehnZoll)
    stellen = {modell: stelleAn(0, 0)}

    neue = Bewegungsphase(stellen).stellenNachDemZiehen(
        stellen, modell, stelleAn(4, 0), stellen, {modell}
    )

    assert neue == {modell: stelleAn(4, 0)}


def testDieBewegungsweiteZähltVomBeginnDerBewegungsphase(zehnZoll):
    modell = modellMit(zehnZoll)
    beginn = {modell: stelleAn(0, 0)}
    jetzt = {modell: stelleAn(3, 0)}

    neue = Bewegungsphase(beginn).stellenNachDemZiehen(
        jetzt, modell, stelleAn(9, 0), jetzt, {modell}
    )

    assert neue[modell].x <= bewegungsweiteDerTestmodelle
