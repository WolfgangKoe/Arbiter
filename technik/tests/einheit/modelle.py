from fractions import Fraction

from arbiter.domaene.spielobjekte import Base, Modell

bewegungsweiteDerTestmodelle = Fraction(5)


def modellMit(base: Base) -> Modell:
    return Modell(modellart="Testmodell", base=base, bewegungsweite=bewegungsweiteDerTestmodelle)
