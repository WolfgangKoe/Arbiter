from fractions import Fraction

from arbiter.domaene.phasen.aufstellen.anhaltenAufDemWeg import (
    Weiterrücken,
    gleiten,
    keinAnhaltenAufDemWeg,
    zuvorGezeigt,
)
from tests.einheit.modelle import modellMit, stelleAn


def wegVon(inX: int, inY: int) -> tuple[Fraction, Fraction]:
    return Fraction(inX), Fraction(inY)


def testEinGezogenesModellHältVorDerFremdenBaseAn(zehnZoll):
    gezogenes, ruhendes = modellMit(zehnZoll), modellMit(zehnZoll)

    geglitten = gleiten(
        {gezogenes: stelleAn(0, 0)},
        wegVon(20, 0),
        {ruhendes: stelleAn(25, 0)},
        keinAnhaltenAufDemWeg,
        angehaltenAufDemWeg=False,
    )

    assert geglitten.stellen == {gezogenes: stelleAn(15, 0)}
    assert geglitten.angehaltenAufDemWeg


def testAmFreienZielZeigtEsDasZielOhneAnhalten(zehnZoll):
    gezogenes, ruhendes = modellMit(zehnZoll), modellMit(zehnZoll)

    geglitten = gleiten(
        {gezogenes: stelleAn(0, 0)},
        wegVon(20, 0),
        {ruhendes: stelleAn(10, 0)},
        keinAnhaltenAufDemWeg,
        angehaltenAufDemWeg=False,
    )

    assert geglitten.stellen == {gezogenes: stelleAn(20, 0)}
    assert not geglitten.angehaltenAufDemWeg


def testEineBaseDieSchonZuvorÜberdecktWurdeHältNichtAuf(zehnZoll):
    gezogenes, ruhendes = modellMit(zehnZoll), modellMit(zehnZoll)

    geglitten = gleiten(
        {gezogenes: stelleAn(0, 0)},
        wegVon(20, 0),
        {ruhendes: stelleAn(5, 0)},
        keinAnhaltenAufDemWeg,
        angehaltenAufDemWeg=False,
    )

    assert geglitten.stellen == {gezogenes: stelleAn(20, 0)}


def testDerFreieWaagrechteTeilGiltVorDerGeradenStrecke(zehnZoll):
    gezogenes, ruhendes = modellMit(zehnZoll), modellMit(zehnZoll)

    geglitten = gleiten(
        {gezogenes: stelleAn(0, 0)},
        wegVon(10, 10),
        {ruhendes: stelleAn(10, 10)},
        keinAnhaltenAufDemWeg,
        angehaltenAufDemWeg=False,
    )

    assert geglitten.stellen == {gezogenes: stelleAn(10, 0)}
    assert geglitten.angehaltenAufDemWeg


def testNachDemAnhaltenHältEsAbZuvorAnDemHaken(zehnZoll):
    gezogenes = modellMit(zehnZoll)

    def aufDieHälfte(*_):
        return Fraction(1, 2)

    geglitten = gleiten(
        {gezogenes: stelleAn(0, 0)}, wegVon(20, 0), {}, aufDieHälfte, angehaltenAufDemWeg=True
    )

    assert geglitten.stellen == {gezogenes: stelleAn(10, 0)}
    assert geglitten.angehaltenAufDemWeg


def testZuvorGezeigtRücktAlleModelleUmDenWegDesGezogenen(zehnZoll):
    gezogenes, anderes = modellMit(zehnZoll), modellMit(zehnZoll)
    vor = {gezogenes: stelleAn(0, 0), anderes: stelleAn(0, 30)}

    zuvor = zuvorGezeigt(vor, gezogenes, Weiterrücken(stelleAn(5, 7), angehaltenAufDemWeg=False))

    assert zuvor == {gezogenes: stelleAn(5, 7), anderes: stelleAn(5, 37)}


def testZuvorGezeigtOhneZuvorIstDieStelleVorDemZiehen(zehnZoll):
    gezogenes = modellMit(zehnZoll)
    vor = {gezogenes: stelleAn(3, 4)}

    assert zuvorGezeigt(vor, gezogenes, Weiterrücken(None, angehaltenAufDemWeg=False)) == vor
