from arbiter.domaene.spielobjekte import Armee, Base, Einheit, Modell


def testDieArmeeNenntDieEinheitEinesModells():
    modell = Modell(base=Base(durchmesser=32))
    einheit = Einheit(name="Einheit", modelle=(modell,))
    armee = Armee(einheiten=(Einheit(name="Andere", modelle=()), einheit))

    assert armee.einheitVon(modell) is einheit


def testDieArmeeKenntEinFremdesModellNicht():
    armee = Armee(einheiten=(Einheit(name="Einheit", modelle=()),))

    assert armee.einheitVon(Modell(base=Base(durchmesser=32))) is None
