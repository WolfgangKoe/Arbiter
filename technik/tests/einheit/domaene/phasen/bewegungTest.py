from fractions import Fraction

from arbiter.domaene.phasen.bewegung import Bewegungsphase
from arbiter.domaene.spielobjekte import Einheit, Spielfeld, Stelle
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
        Einheit("Testeinheit", (modell,)),
        stellen, modell, stelleAn(4, 0), stellen, {modell}
    )

    assert neue == {modell: stelleAn(4, 0)}
    assert gründe == set()


def testDieBewegungsweiteZähltVomBeginnDerBewegungsphase(zehnZoll):
    modell = modellMit(zehnZoll)
    beginn = {modell: stelleAn(0, 0)}
    jetzt = {modell: stelleAn(3, 0)}

    neue, _ = Bewegungsphase(beginn, spielfeld).stellenMitGründenNachDemZiehen(
        Einheit("Testeinheit", (modell,)),
        jetzt, modell, stelleAn(9, 0), jetzt, {modell}
    )

    assert neue == {modell: stelleAn(int(bewegungsweiteDerTestmodelle), 0)}


def testEineEinheitDieNichtVorrückteWirdVorrückenAngeboten():
    einheit = Einheit("Testeinheit", ())
    bewegungsphase = Bewegungsphase({}, spielfeld)

    assert bewegungsphase.vorrückenAngeboten(einheit)
    assert not bewegungsphase.vorrückenZurücknehmenAngeboten(einheit)


def testNachDemBeginnWartetDieEinheitAufIhrenVorrückwurf():
    einheit = Einheit("Testeinheit", ())
    bewegungsphase = Bewegungsphase({}, spielfeld)

    bewegungsphase.vorrückenBeginnen(einheit)

    assert bewegungsphase.wartetAufVorrückwurf(einheit)
    assert not bewegungsphase.vorgerückt(einheit)
    assert bewegungsphase.vorrückenZurücknehmenAngeboten(einheit)


def testDasZurücknehmenMachtDieWartendeEinheitWiederFrei():
    einheit = Einheit("Testeinheit", ())
    bewegungsphase = Bewegungsphase({}, spielfeld)
    bewegungsphase.vorrückenBeginnen(einheit)

    bewegungsphase.vorrückenZurücknehmen(einheit)

    assert bewegungsphase.vorrückenAngeboten(einheit)
    assert bewegungsphase.vorrückwurf(einheit) is None
