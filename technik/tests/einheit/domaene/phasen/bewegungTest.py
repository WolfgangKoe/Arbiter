from fractions import Fraction

from arbiter.domaene.phasen.bewegung import Bewegungsphase
from arbiter.domaene.sperre import Grund
from arbiter.domaene.spielobjekte import Einheit, Spielfeld, Stelle
from tests.einheit.modelle import bewegungsweiteDerTestmodelle, modellMit

spielfeld = Spielfeld(seitenlängen=(Fraction(60), Fraction(44)))
imInnerenDesSpielfelds = 10


def stelleAn(inX: int, inY: int) -> Stelle:
    return Stelle(
        x=Fraction(inX + imInnerenDesSpielfelds), y=Fraction(inY + imInnerenDesSpielfelds)
    )


def testDasZiehenGibtDieNeuenStellenDerEbeneZurück(zehnZoll):
    modell = modellMit(zehnZoll)
    stellen = {modell: stelleAn(0, 0)}

    neue, gründe = Bewegungsphase(stellen, spielfeld).stellenMitGründenNachDemZiehen(
        stellen, modell, stelleAn(4, 0), stellen, {}
    )

    assert neue == {modell: stelleAn(4, 0)}
    assert gründe == set()


def testDieBewegungsweiteZähltVomBeginnDerBewegungsphase(zehnZoll):
    modell = modellMit(zehnZoll)
    beginn = {modell: stelleAn(0, 0)}
    jetzt = {modell: stelleAn(3, 0)}

    neue, _ = Bewegungsphase(beginn, spielfeld).stellenMitGründenNachDemZiehen(
        jetzt, modell, stelleAn(9, 0), jetzt, {}
    )

    assert neue == {modell: stelleAn(int(bewegungsweiteDerTestmodelle), 0)}


def testDerVorrückwurfEinerEinheitGiltNichtFürDasModellEinerAnderenEinheit(zehnZoll):
    vorgerücktesModell = modellMit(zehnZoll)
    normalesModell = modellMit(zehnZoll)
    vorgerückt = Einheit("Vorgerückt", (vorgerücktesModell,))
    stellen = {vorgerücktesModell: stelleAn(0, 20), normalesModell: stelleAn(0, 0)}
    bewegungsphase = Bewegungsphase(stellen, spielfeld)
    bewegungsphase.vorrückenBeginnen(vorgerückt)
    assert bewegungsphase.vorrückwurfNehmen(vorgerückt, vorgerückt.modelle, stelleAn(0, 32))

    neue, _ = bewegungsphase.stellenMitGründenNachDemZiehen(
        {normalesModell: stelleAn(0, 0)}, normalesModell, stelleAn(9, 0), stellen, {}
    )

    assert neue == {normalesModell: stelleAn(int(bewegungsweiteDerTestmodelle), 0)}


def testEineEinheitDieNichtVorrückteWirdVorrückenAngeboten():
    einheit = Einheit("Testeinheit", ())
    bewegungsphase = Bewegungsphase({}, spielfeld)

    assert bewegungsphase.vorrückenAngeboten(einheit)
    assert not bewegungsphase.vorrückenZurücknehmenAngeboten(einheit)


def testNachDemBeginnWartetDieEinheitAufIhrenVorrückwurf():
    einheit = Einheit("Testeinheit", ())
    bewegungsphase = Bewegungsphase({}, spielfeld)

    bewegungsphase.vorrückenBeginnen(einheit)

    assert bewegungsphase.wartetAufVorrückwurf(einheit)
    assert not bewegungsphase.vorgerückt(einheit)
    assert bewegungsphase.vorrückenZurücknehmenAngeboten(einheit)


def testDasZurücknehmenMachtDieWartendeEinheitWiederFrei():
    einheit = Einheit("Testeinheit", ())
    bewegungsphase = Bewegungsphase({}, spielfeld)
    bewegungsphase.vorrückenBeginnen(einheit)

    bewegungsphase.vorrückenZurücknehmen(einheit)

    assert bewegungsphase.vorrückenAngeboten(einheit)
    assert bewegungsphase.vorrückwurf(einheit) is None


def testNachDemZiehenBisÜberDieBewegungsweiteHinausWirdDasÜbergehenAngeboten(zehnZoll):
    modell = modellMit(zehnZoll)
    stellen = {modell: stelleAn(0, 0)}
    bewegungsphase = Bewegungsphase(stellen, spielfeld)

    bewegungsphase.angebotNachDemZiehen(stellen, modell, stelleAn(9, 0), {})

    assert bewegungsphase.übergehenAngeboten


def testNachDemZiehenInnerhalbDerBewegungsweiteWirdKeinÜbergehenAngeboten(zehnZoll):
    modell = modellMit(zehnZoll)
    stellen = {modell: stelleAn(0, 0)}
    bewegungsphase = Bewegungsphase(stellen, spielfeld)

    bewegungsphase.angebotNachDemZiehen(stellen, modell, stelleAn(4, 0), {})

    assert not bewegungsphase.übergehenAngeboten


def testOhneAngebotIstNichtsÜbergangen(zehnZoll):
    modell = modellMit(zehnZoll)
    stellen = {modell: stelleAn(0, 0)}

    assert Bewegungsphase(stellen, spielfeld).übergangen(stellen, {}) is None


def testDasÜbergehenSetztDasModellAmPunktDesZiehensUndNenntDenGrundDesAnhaltens(zehnZoll):
    modell = modellMit(zehnZoll)
    stellen = {modell: stelleAn(0, 0)}
    bewegungsphase = Bewegungsphase(stellen, spielfeld)
    bewegungsphase.angebotNachDemZiehen(stellen, modell, stelleAn(9, 0), {})

    übergangen = bewegungsphase.übergangen(stellen, {})

    assert übergangen is not None
    assert übergangen.stellen == {modell: stelleAn(9, 0)}
    assert übergangen.gründe == set()
    assert übergangen.angehalten == {Grund.bewegungsweite}
    assert übergangen.gezogenes == modell


def testDasBeendenDesAngebotsNimmtDasÜbergehenZurück(zehnZoll):
    modell = modellMit(zehnZoll)
    stellen = {modell: stelleAn(0, 0)}
    bewegungsphase = Bewegungsphase(stellen, spielfeld)
    bewegungsphase.angebotNachDemZiehen(stellen, modell, stelleAn(9, 0), {})

    bewegungsphase.angebotBeenden()

    assert not bewegungsphase.übergehenAngeboten
    assert bewegungsphase.übergangen(stellen, {}) is None
