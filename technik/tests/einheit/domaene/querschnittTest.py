from fractions import Fraction

from arbiter.domaene.querschnitt import baseÜberdeckt
from arbiter.domaene.spielobjekte import Base, Modell, Stelle

# Regel: 254 mm sind 10″, der Durchmesser 254 mm hat den Radius 5″
zehnZoll = Base(durchmesser=254)
ursprung = Stelle(x=Fraction(0), y=Fraction(0))


def testEineBaseAufEinerAnderenBaseIstÜberdeckt():
    anderes = Modell(base=zehnZoll)

    assert baseÜberdeckt(Modell(base=zehnZoll), ursprung, {anderes: ursprung})


def testBerührendeBasesSindNichtÜberdeckt():
    anderes = Modell(base=zehnZoll)

    assert not baseÜberdeckt(
        Modell(base=zehnZoll), ursprung, {anderes: Stelle(x=Fraction(10), y=Fraction(0))}
    )


def testDasModellÜberdecktSichNichtSelbst():
    modell = Modell(base=zehnZoll)

    assert not baseÜberdeckt(modell, ursprung, {modell: ursprung})
