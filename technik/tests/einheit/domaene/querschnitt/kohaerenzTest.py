from fractions import Fraction

from arbiter.domaene.querschnitt.kohaerenz import inKohärenz
from arbiter.domaene.spielobjekte import Base, Modell, Stelle

# Regel: 254 mm sind 10″, der Durchmesser 254 mm hat den Radius 5″
zehnZoll = Base(durchmesser=254)
ursprung = Stelle(x=Fraction(0), y=Fraction(0))


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
