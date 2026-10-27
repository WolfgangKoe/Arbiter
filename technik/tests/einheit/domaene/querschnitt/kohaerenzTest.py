from fractions import Fraction

from arbiter.domaene.querschnitt.kohaerenz import inKohärenz
from arbiter.domaene.spielobjekte import Stelle
from tests.einheit.modelle import testmodell

ursprung = Stelle(x=Fraction(0), y=Fraction(0))


def testZweiModelleMitZweiZollZwischenDenBasesStehenInKohärenz(zehnZoll):
    stellen = {
        testmodell(zehnZoll): ursprung,
        testmodell(zehnZoll): Stelle(x=Fraction(12), y=Fraction(0)),
    }

    assert inKohärenz(stellen)


def testZweiModelleMitMehrAlsZweiZollZwischenDenBasesStehenNichtInKohärenz(zehnZoll):
    stellen = {
        testmodell(zehnZoll): ursprung,
        testmodell(zehnZoll): Stelle(x=Fraction(13), y=Fraction(0)),
    }

    assert not inKohärenz(stellen)
