from fractions import Fraction

from arbiter.domaene.spielobjekte import Base, Modell, Stelle

bewegungsweiteDerTestmodelle = Fraction(5)


def modellMit(base: Base) -> Modell:
    return Modell(modellart="Testmodell", base=base, bewegungsweite=bewegungsweiteDerTestmodelle)


def stelleAn(inX: int, inY: int) -> Stelle:
    return Stelle(x=Fraction(inX), y=Fraction(inY))
