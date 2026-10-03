from fractions import Fraction

from arbiter.domaene.messen import abstandHöchstens, ganzIn, überdecken
from arbiter.domaene.spielobjekte import Base, Stelle

# Regel: 254 mm sind 10″, der Durchmesser 254 mm hat den Radius 5″
zehnZoll = Base(durchmesser=254)
ursprung = Stelle(x=Fraction(0), y=Fraction(0))


def testZweiBasesImAbstandDerRadienBerührenSichUndÜberdeckenSichNicht():
    berührend = Stelle(x=Fraction(10), y=Fraction(0))

    assert not überdecken(zehnZoll, ursprung, zehnZoll, berührend)


def testZweiBasesKnappInnerhalbDerRadienÜberdeckenSich():
    knapp = Stelle(x=Fraction(10) - Fraction(1, 1_000_000), y=Fraction(0))

    assert überdecken(zehnZoll, ursprung, zehnZoll, knapp)


def testDerAbstandIstHöchstensEinZollWennDieRänderEinenZollAuseinanderLiegen():
    einZollAbstand = Stelle(x=Fraction(11), y=Fraction(0))

    assert abstandHöchstens(zehnZoll, ursprung, zehnZoll, einZollAbstand, Fraction(1))


def testDerAbstandIstNichtHöchstensEinZollWennDieRänderWeiterAuseinanderLiegen():
    weiter = Stelle(x=Fraction(11) + Fraction(1, 1_000_000), y=Fraction(0))

    assert not abstandHöchstens(zehnZoll, ursprung, zehnZoll, weiter, Fraction(1))


def testDieBaseLiegtGanzInDenGrenzenWennIhrRandDieFlächeBerührt():
    grenzen, länge = (Fraction(-5), Fraction(5)), Fraction(10)

    assert ganzIn(zehnZoll, Stelle(x=Fraction(0), y=Fraction(5)), grenzen, länge)


def testDieBaseLiegtNichtGanzInDenGrenzenWennSieEinMillionstelHinausragt():
    grenzen, länge = (Fraction(-5), Fraction(5)), Fraction(10)
    verschoben = Stelle(x=Fraction(1, 1_000_000), y=Fraction(5))

    assert not ganzIn(zehnZoll, verschoben, grenzen, länge)
