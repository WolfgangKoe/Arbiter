from fractions import Fraction

import pytest

from arbiter.domaene.spielobjekte import Armee, Base, Einheit, Modell, Stelle


def testDieArmeeNenntDieEinheitEinesModells():
    modell = Modell(base=Base(durchmesser=32))
    einheit = Einheit(name="Einheit", modelle=(modell,))
    armee = Armee(einheiten=(Einheit(name="Andere", modelle=()), einheit))

    assert armee.einheitVon(modell) is einheit


def testDieArmeeKenntEinFremdesModellNicht():
    armee = Armee(einheiten=(Einheit(name="Einheit", modelle=()),))

    assert armee.einheitVon(Modell(base=Base(durchmesser=32))) is None


@pytest.mark.parametrize("zahl", [20, 20.0])
def testEineStelleAusEinerUngenauenZahlIstEinFehler(zahl):
    null = Fraction(0)

    with pytest.raises(TypeError):
        Stelle(x=zahl, y=null)
    with pytest.raises(TypeError):
        Stelle(x=null, y=zahl)
