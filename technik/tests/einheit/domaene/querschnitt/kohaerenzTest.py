from fractions import Fraction

from arbiter.domaene.querschnitt.kohaerenz import inKohärenz
from arbiter.domaene.spielobjekte import Stelle
from tests.einheit.modelle import modellMit

ursprung = Stelle(x=Fraction(0), y=Fraction(0))


def testZweiModelleMitZweiZollZwischenDenBasesStehenInKohärenz(zehnZoll):
    stellen = {
        modellMit(zehnZoll): ursprung,
        modellMit(zehnZoll): Stelle(x=Fraction(12), y=Fraction(0)),
    }

    assert inKohärenz(stellen)


def testZweiModelleMitMehrAlsZweiZollZwischenDenBasesStehenNichtInKohärenz(zehnZoll):
    stellen = {
        modellMit(zehnZoll): ursprung,
        modellMit(zehnZoll): Stelle(x=Fraction(13), y=Fraction(0)),
    }

    assert not inKohärenz(stellen)
