from fractions import Fraction

from arbiter.domaene.phasen.bewegung.anhaltenVorDerGrenze import (
    anteilBisZurNahkampfreichweite,
    anteilBisZurSpielfeldkante,
)
from arbiter.domaene.spielobjekte import Spielfeld, Stelle
from tests.einheit.modelle import modellMit

grenze = 11
spielfeld = Spielfeld(seitenlängen=(Fraction(60), Fraction(44)))


def stelleAn(inX: int, inY: int) -> Stelle:
    return Stelle(x=Fraction(inX), y=Fraction(inY))


def testEinWegImSpielfeldBleibtUnverkürzt(zehnZoll):
    modell = modellMit(zehnZoll)

    anteil = anteilBisZurSpielfeldkante(
        {modell: stelleAn(10, 10)}, (Fraction(5), Fraction(0)), spielfeld
    )

    assert anteil == 1


def testEinWegAusDemSpielfeldHältHöchstensEinHundertstelVorDerKanteAn(zehnZoll):
    modell = modellMit(zehnZoll)

    anteil = anteilBisZurSpielfeldkante(
        {modell: stelleAn(10, 10)}, (Fraction(-20), Fraction(0)), spielfeld
    )

    abstandZurKante = 10 - Fraction(5) - 20 * anteil
    assert 0 <= abstandZurKante <= Fraction(1, 100)


def testEinWegZuEinemGegnerHältVorDerNahkampfreichweiteAn(zehnZoll):
    modell, gegner = modellMit(zehnZoll), modellMit(zehnZoll)

    anteil = anteilBisZurNahkampfreichweite(
        {modell: stelleAn(0, 0)}, (Fraction(20), Fraction(0)), {gegner: stelleAn(20, 0)}
    )

    abstandDerMittelpunkte = 20 - 20 * anteil
    assert grenze < abstandDerMittelpunkte <= grenze + Fraction(1, 100)
