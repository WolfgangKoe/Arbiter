from fractions import Fraction

from arbiter.domaene.querschnitt.setzen import baseÜberdeckt
from arbiter.domaene.spielobjekte import Stelle
from tests.einheit.modelle import modellMit

ursprung = Stelle(x=Fraction(0), y=Fraction(0))


def testEineBaseAufEinerAnderenBaseIstÜberdeckt(zehnZoll):
    anderes = modellMit(zehnZoll)

    assert baseÜberdeckt(modellMit(zehnZoll), ursprung, {anderes: ursprung})


def testBerührendeBasesSindNichtÜberdeckt(zehnZoll):
    anderes = modellMit(zehnZoll)

    assert not baseÜberdeckt(
        modellMit(zehnZoll), ursprung, {anderes: Stelle(x=Fraction(10), y=Fraction(0))}
    )


def testDasModellÜberdecktSichNichtSelbst(zehnZoll):
    modell = modellMit(zehnZoll)

    assert not baseÜberdeckt(modell, ursprung, {modell: ursprung})
