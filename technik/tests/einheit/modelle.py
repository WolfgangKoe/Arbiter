"""Testmodelle der Einheitstests: eine Base und die Bewegungsweite 5 Zoll."""

from fractions import Fraction

from arbiter.domaene.spielobjekte import Base, Modell

bewegungsweiteDerTestmodelle = Fraction(5)


def testmodell(base: Base) -> Modell:
    return Modell(base=base, bewegungsweite=bewegungsweiteDerTestmodelle)


testmodell.__test__ = False
