from fractions import Fraction

from arbiter.domaene.phasen.bewegung.grenzkreise import (
    Grenzkreis,
    enthält,
    grenzeDerBewegung,
    grenzenDerWürfe,
    kleinsterWurfAn,
    möglicheWürfe,
)
from arbiter.domaene.spielobjekte import Einheit, Stelle
from tests.einheit.modelle import bewegungsweiteDerTestmodelle, modellMit

dreiAugen = 3
mitte = Stelle(x=Fraction(20), y=Fraction(20))


def stelleUnterDerMitte(abstand: Fraction) -> Stelle:
    return Stelle(x=mitte.x, y=mitte.y + abstand)


def testDerGrenzkreisReichtEineBewegungsweiteUndEinenRadiusWeit(zehnZoll):
    modell = modellMit(zehnZoll)
    einheit = Einheit("Testeinheit", (modell,))

    grenze = grenzeDerBewegung(einheit, {modell: mitte})

    assert grenze.kreise == (Grenzkreis(mitte, bewegungsweiteDerTestmodelle + Fraction(5, 1)),)


def testEinKreisEnthältAuchSeinenRand():
    kreis = Grenzkreis(mitte, Fraction(5))

    assert enthält([kreis], stelleUnterDerMitte(Fraction(5)))
    assert not enthält([kreis], stelleUnterDerMitte(Fraction(51, 10)))


def testDerKleinsteWurfIstDerKleinsteRing(zehnZoll):
    modell = modellMit(zehnZoll)
    einheit = Einheit("Testeinheit", (modell,))
    ebene = {modell: mitte}
    bewegung = grenzeDerBewegung(einheit, ebene)
    würfe = grenzenDerWürfe(einheit, ebene, möglicheWürfe, wählbar=True)
    weite = bewegungsweiteDerTestmodelle + Fraction(5)

    imDrittenRing = stelleUnterDerMitte(weite + Fraction(5, 2))

    assert kleinsterWurfAn(imDrittenRing, bewegung, würfe) == dreiAugen
    assert kleinsterWurfAn(stelleUnterDerMitte(weite), bewegung, würfe) is None
    assert kleinsterWurfAn(stelleUnterDerMitte(weite + 7), bewegung, würfe) is None
