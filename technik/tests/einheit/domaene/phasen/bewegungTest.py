from fractions import Fraction

from arbiter.domaene.phasen.bewegung import Bewegungsphase
from arbiter.domaene.spielobjekte import Spielfeld, Stelle
from tests.einheit.modelle import bewegungsweiteDerTestmodelle, modellMit

spielfeld = Spielfeld(seitenlängen=(Fraction(60), Fraction(44)))
imInnerenDesSpielfelds = 10


def stelleAn(inX: int, inY: int) -> Stelle:
    return Stelle(
        x=Fraction(inX + imInnerenDesSpielfelds), y=Fraction(inY + imInnerenDesSpielfelds)
    )


def testDasZiehenGibtDieNeuenStellenDerEbeneZurück(zehnZoll):
    modell = modellMit(zehnZoll)
    stellen = {modell: stelleAn(0, 0)}

    neue, gründe = Bewegungsphase(stellen, spielfeld).stellenMitGründenNachDemZiehen(
        stellen, modell, stelleAn(4, 0), stellen, {modell}
    )

    assert neue == {modell: stelleAn(4, 0)}
    assert gründe == set()


def testDieBewegungsweiteZähltVomBeginnDerBewegungsphase(zehnZoll):
    modell = modellMit(zehnZoll)
    beginn = {modell: stelleAn(0, 0)}
    jetzt = {modell: stelleAn(3, 0)}

    neue, _ = Bewegungsphase(beginn, spielfeld).stellenMitGründenNachDemZiehen(
        jetzt, modell, stelleAn(9, 0), jetzt, {modell}
    )

    assert neue == {modell: stelleAn(int(bewegungsweiteDerTestmodelle), 0)}
