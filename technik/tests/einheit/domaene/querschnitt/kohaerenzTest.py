from fractions import Fraction

from arbiter.domaene.querschnitt.kohaerenz import inKohärenz
from arbiter.domaene.spielobjekte import Modell, Stelle

ursprung = Stelle(x=Fraction(0), y=Fraction(0))


def testZweiModelleMitZweiZollZwischenDenBasesStehenInKohärenz(zehnZoll):
    stellen = {
        Modell(base=zehnZoll): ursprung,
        Modell(base=zehnZoll): Stelle(x=Fraction(12), y=Fraction(0)),
    }

    assert inKohärenz(stellen)


def testZweiModelleMitMehrAlsZweiZollZwischenDenBasesStehenNichtInKohärenz(zehnZoll):
    stellen = {
        Modell(base=zehnZoll): ursprung,
        Modell(base=zehnZoll): Stelle(x=Fraction(13), y=Fraction(0)),
    }

    assert not inKohärenz(stellen)
