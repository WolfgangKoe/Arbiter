from fractions import Fraction

from arbiter.domaene.phasen.aufstellen.anhaltenAnEinerBase import angehalten
from arbiter.domaene.spielobjekte import Stelle
from tests.einheit.modelle import modellMit


def stelleAn(inX: int, inY: int) -> Stelle:
    return Stelle(x=Fraction(inX), y=Fraction(inY))


def testEinGezogenesModellHältVorDerFremdenBaseAn(zehnZoll):
    gezogenes, ruhendes = modellMit(zehnZoll), modellMit(zehnZoll)
    stellen = {gezogenes: stelleAn(0, 0), ruhendes: stelleAn(25, 0)}
    neue = {gezogenes: stelleAn(20, 0)}

    assert angehalten(stellen, neue, gezogenes) == {gezogenes: stelleAn(15, 0)}


def testEinNichtGesetztesGezogenesModellWirdNichtAngehaltenAuchAufEinerFremdenBase(zehnZoll):
    gezogenes, ruhendes = modellMit(zehnZoll), modellMit(zehnZoll)
    stellen = {ruhendes: stelleAn(20, 20)}
    neue = {gezogenes: stelleAn(20, 20)}

    assert angehalten(stellen, neue, gezogenes) == neue
