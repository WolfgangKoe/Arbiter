from fractions import Fraction

from arbiter.domaene.querschnitt import baseÜberdeckt
from arbiter.domaene.spielobjekte import Stelle
from tests.einheit.modelle import testmodell

ursprung = Stelle(x=Fraction(0), y=Fraction(0))


def testEineBaseAufEinerAnderenBaseIstÜberdeckt(zehnZoll):
    anderes = testmodell(zehnZoll)

    assert baseÜberdeckt(testmodell(zehnZoll), ursprung, {anderes: ursprung})


def testBerührendeBasesSindNichtÜberdeckt(zehnZoll):
    anderes = testmodell(zehnZoll)

    assert not baseÜberdeckt(
        testmodell(zehnZoll), ursprung, {anderes: Stelle(x=Fraction(10), y=Fraction(0))}
    )


def testDasModellÜberdecktSichNichtSelbst(zehnZoll):
    modell = testmodell(zehnZoll)

    assert not baseÜberdeckt(modell, ursprung, {modell: ursprung})
