from fractions import Fraction

from arbiter.domaene.querschnitt import baseÜberdeckt
from arbiter.domaene.spielobjekte import Modell, Stelle

ursprung = Stelle(x=Fraction(0), y=Fraction(0))


def testEineBaseAufEinerAnderenBaseIstÜberdeckt(zehnZoll):
    anderes = Modell(base=zehnZoll)

    assert baseÜberdeckt(Modell(base=zehnZoll), ursprung, {anderes: ursprung})


def testBerührendeBasesSindNichtÜberdeckt(zehnZoll):
    anderes = Modell(base=zehnZoll)

    assert not baseÜberdeckt(
        Modell(base=zehnZoll), ursprung, {anderes: Stelle(x=Fraction(10), y=Fraction(0))}
    )


def testDasModellÜberdecktSichNichtSelbst(zehnZoll):
    modell = Modell(base=zehnZoll)

    assert not baseÜberdeckt(modell, ursprung, {modell: ursprung})
