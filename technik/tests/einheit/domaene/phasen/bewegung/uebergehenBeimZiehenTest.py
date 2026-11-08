from fractions import Fraction

import pytest

from arbiter.domaene.phasen.bewegung.uebergehenBeimZiehen import Anteile, gründeBeimÜbergehen
from arbiter.domaene.sperre import Grund
from tests.einheit.modelle import modellMit, stelleAn

ganz = Fraction(1)
halb = Fraction(1, 2)
viertel = Fraction(1, 4)


def testKeinAnhaltenFrüherAlsDasEndeDesWegsBietetKeinÜbergehenAn():
    assert not Anteile(ganz, ganz, ganz).hältAnDerBewegungsweiteOderNahkampfreichweite


@pytest.mark.parametrize("anteile", [Anteile(halb, ganz, ganz), Anteile(ganz, ganz, halb)])
def testDasAnhaltenAnDerBewegungsweiteOderNahkampfreichweiteBietetDasÜbergehenAn(anteile):
    assert anteile.hältAnDerBewegungsweiteOderNahkampfreichweite


def testHältDieSpielfeldkanteFrüherAnBietetDasÜbergehenNichtAn():
    assert not Anteile(halb, viertel, ganz).hältAnDerBewegungsweiteOderNahkampfreichweite


def testHältDieSpielfeldkanteGleichFrühAnBietetDasÜbergehenAn():
    assert Anteile(halb, halb, ganz).hältAnDerBewegungsweiteOderNahkampfreichweite


def testDieGründeDesAnhaltensSindDieAnteileUnterEins():
    assert Anteile(halb, viertel, halb).gründeDesAnhaltens == {
        Grund.bewegungsweite,
        Grund.nahkampfreichweite,
    }


def testKeinAnteilUnterEinsGibtKeineGründeDesAnhaltens():
    assert Anteile(ganz, viertel, ganz).gründeDesAnhaltens == frozenset()


def testEinÜberdecktesBaseBeimÜbergehenIstEinGrund(zehnZoll):
    gezogenes, fremdes = modellMit(zehnZoll), modellMit(zehnZoll)

    gründe = gründeBeimÜbergehen(
        {gezogenes: stelleAn(0, 0)}, {fremdes: stelleAn(5, 0)}, {gezogenes}
    )

    assert gründe == {Grund.baseÜberdeckt}


def testDieNahkampfreichweiteIstBeimÜbergehenKeinGrund(zehnZoll):
    gezogenes, gegner = modellMit(zehnZoll), modellMit(zehnZoll)

    gründe = gründeBeimÜbergehen(
        {gezogenes: stelleAn(0, 0)}, {gegner: stelleAn(11, 0)}, {gezogenes}
    )

    assert gründe == set()
