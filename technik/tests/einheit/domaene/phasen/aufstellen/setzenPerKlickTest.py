from fractions import Fraction

from arbiter.domaene.missionsvorbereitung.ausgangslage import Formation
from arbiter.domaene.phasen.aufstellen.setzenPerKlick import stellenDerFormation
from arbiter.domaene.spielobjekte import Base, Stelle

# Regel: 254 mm sind 10″, der Durchmesser 254 mm hat den Radius 5″
zehnZoll = Base(durchmesser=254)
weitesFeld = (Fraction(-1000), Fraction(1000))


def testEineFormationStelltEineReiheMittigBaseAnBaseAuf():
    formation = Formation(reihen=(2,), abstand=Fraction(0))
    mitte = Stelle(x=Fraction(20), y=Fraction(20))

    stellen = stellenDerFormation(formation, zehnZoll, mitte, weitesFeld, weitesFeld)

    assert stellen == [
        Stelle(x=Fraction(20), y=Fraction(15)),
        Stelle(x=Fraction(20), y=Fraction(25)),
    ]


def testEineFormationRücktInDieGrenzen():
    formation = Formation(reihen=(2,), abstand=Fraction(0))
    mitte = Stelle(x=Fraction(20), y=Fraction(20))
    nurBisAchtzehn = (Fraction(0), Fraction(18))

    stellen = stellenDerFormation(formation, zehnZoll, mitte, weitesFeld, nurBisAchtzehn)

    assert stellen == [
        Stelle(x=Fraction(20), y=Fraction(3)),
        Stelle(x=Fraction(20), y=Fraction(13)),
    ]


def testEineFormationSetztDieNächsteReiheEinenSchrittDahinter():
    formation = Formation(reihen=(1, 1), abstand=Fraction(0))
    mitte = Stelle(x=Fraction(20), y=Fraction(20))

    stellen = stellenDerFormation(formation, zehnZoll, mitte, weitesFeld, weitesFeld)

    assert stellen == [
        Stelle(x=Fraction(15), y=Fraction(20)),
        Stelle(x=Fraction(25), y=Fraction(20)),
    ]
