from fractions import Fraction

from arbiter.domaene.querschnitt import Formation, baseÜberdeckt, inKohärenz
from arbiter.domaene.spielobjekte import Base, Modell, Stelle

# Regel: 254 mm sind 10″, der Durchmesser 254 mm hat den Radius 5″
zehnZoll = Base(durchmesser=254)
ursprung = Stelle(x=Fraction(0), y=Fraction(0))
weitesFeld = (Fraction(-1000), Fraction(1000))


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


def testZweiModelleMitZweiZollZwischenDenBasesStehenInKohärenz():
    stellen = {
        Modell(base=zehnZoll): ursprung,
        Modell(base=zehnZoll): Stelle(x=Fraction(12), y=Fraction(0)),
    }

    assert inKohärenz(stellen)


def testZweiModelleMitMehrAlsZweiZollZwischenDenBasesStehenNichtInKohärenz():
    stellen = {
        Modell(base=zehnZoll): ursprung,
        Modell(base=zehnZoll): Stelle(x=Fraction(13), y=Fraction(0)),
    }

    assert not inKohärenz(stellen)


def testEineFormationStelltEineReiheMittigBaseAnBaseAuf():
    formation = Formation(reihen=(2,), abstand=Fraction(0))
    mitte = Stelle(x=Fraction(20), y=Fraction(20))

    stellen = formation.stellen(zehnZoll, mitte, weitesFeld, weitesFeld)

    assert stellen == [
        Stelle(x=Fraction(20), y=Fraction(15)),
        Stelle(x=Fraction(20), y=Fraction(25)),
    ]


def testEineFormationRücktInDieGrenzen():
    formation = Formation(reihen=(2,), abstand=Fraction(0))
    mitte = Stelle(x=Fraction(20), y=Fraction(20))
    nurBisAchtzehn = (Fraction(0), Fraction(18))

    stellen = formation.stellen(zehnZoll, mitte, weitesFeld, nurBisAchtzehn)

    assert stellen == [
        Stelle(x=Fraction(20), y=Fraction(3)),
        Stelle(x=Fraction(20), y=Fraction(13)),
    ]


def testEineFormationSetztDieNächsteReiheEinenSchrittDahinter():
    formation = Formation(reihen=(1, 1), abstand=Fraction(0))
    mitte = Stelle(x=Fraction(20), y=Fraction(20))

    stellen = formation.stellen(zehnZoll, mitte, weitesFeld, weitesFeld)

    assert stellen == [
        Stelle(x=Fraction(15), y=Fraction(20)),
        Stelle(x=Fraction(25), y=Fraction(20)),
    ]
