from fractions import Fraction

from arbiter.domaene.messen import (
    abstandHöchstens,
    anteilBisZurBerührung,
    ganzIn,
    rückungInDieFläche,
    streckeÜberdeckt,
    teilDesWegs,
    verschoben,
    wegZwischen,
    überdecken,
)
from arbiter.domaene.spielobjekte import Stelle

ursprung = Stelle(x=Fraction(0), y=Fraction(0))


def testZweiBasesImAbstandDerRadienBerührenSichUndÜberdeckenSichNicht(zehnZoll):
    berührend = Stelle(x=Fraction(10), y=Fraction(0))

    assert not überdecken(zehnZoll, ursprung, zehnZoll, berührend)


def testZweiBasesKnappInnerhalbDerRadienÜberdeckenSich(zehnZoll):
    knapp = Stelle(x=Fraction(10) - Fraction(1, 1_000_000), y=Fraction(0))

    assert überdecken(zehnZoll, ursprung, zehnZoll, knapp)


def testDerAbstandIstHöchstensEinZollWennDieRänderEinenZollAuseinanderLiegen(zehnZoll):
    einZollAbstand = Stelle(x=Fraction(11), y=Fraction(0))

    assert abstandHöchstens(zehnZoll, ursprung, zehnZoll, einZollAbstand, Fraction(1))


def testDerAbstandIstNichtHöchstensEinZollWennDieRänderWeiterAuseinanderLiegen(zehnZoll):
    weiter = Stelle(x=Fraction(11) + Fraction(1, 1_000_000), y=Fraction(0))

    assert not abstandHöchstens(zehnZoll, ursprung, zehnZoll, weiter, Fraction(1))


def testDieBaseLiegtGanzInDenGrenzenWennIhrRandDieFlächeBerührt(zehnZoll):
    grenzenInX, grenzenInY = (Fraction(-5), Fraction(5)), (Fraction(0), Fraction(10))

    assert ganzIn(zehnZoll, Stelle(x=Fraction(0), y=Fraction(5)), grenzenInX, grenzenInY)


def testDieBaseLiegtNichtGanzInDenGrenzenWennSieEinMillionstelHinausragt(zehnZoll):
    grenzenInX, grenzenInY = (Fraction(-5), Fraction(5)), (Fraction(0), Fraction(10))
    verschobeneStelle = Stelle(x=Fraction(1, 1_000_000), y=Fraction(5))

    assert not ganzIn(zehnZoll, verschobeneStelle, grenzenInX, grenzenInY)


def testEineStelleFolgtDemWeg():
    stelle = Stelle(x=Fraction(2), y=Fraction(3))

    assert verschoben(stelle, (Fraction(5), Fraction(-4))) == Stelle(x=Fraction(7), y=Fraction(-1))


def testDerWegZwischenZweiStellenFührtVonDerErstenZurZweiten():
    davor = Stelle(x=Fraction(2), y=Fraction(3))
    danach = Stelle(x=Fraction(7), y=Fraction(-1))

    weg = wegZwischen(davor, danach)

    assert weg == (Fraction(5), Fraction(-4))
    assert verschoben(davor, weg) == danach


def testEinTeilDesWegsSkaliertBeideRichtungen():
    assert teilDesWegs((Fraction(8), Fraction(-4)), Fraction(1, 4)) == (Fraction(2), Fraction(-1))


def testEineBaseInDerFlächeBrauchtKeineRückung(zehnZoll):
    grenzenInX, grenzenInY = (Fraction(0), Fraction(20)), (Fraction(0), Fraction(20))
    mitte = Stelle(x=Fraction(10), y=Fraction(10))

    assert rückungInDieFläche([(zehnZoll, mitte)], grenzenInX, grenzenInY) == (0, 0)


def testZweiBasesRückenGemeinsamUmDasÜberstehendeDerVorderstenHinein(zehnZoll):
    grenzenInX, grenzenInY = (Fraction(0), Fraction(20)), (Fraction(0), Fraction(20))
    bases = [
        (zehnZoll, Stelle(x=Fraction(2), y=Fraction(10))),
        (zehnZoll, Stelle(x=Fraction(8), y=Fraction(17))),
    ]

    assert rückungInDieFläche(bases, grenzenInX, grenzenInY) == (3, -2)


def testEinZuBreiterBlockRücktNurAnDieUntereKante(zehnZoll):
    grenzenInX, grenzenInY = (Fraction(0), Fraction(20)), (Fraction(0), Fraction(20))
    bases = [
        (zehnZoll, Stelle(x=Fraction(2), y=Fraction(10))),
        (zehnZoll, Stelle(x=Fraction(22), y=Fraction(10))),
    ]

    assert rückungInDieFläche(bases, grenzenInX, grenzenInY) == (3, 0)


def testEineBaseÜberDerObergrenzeRücktInXAnDieObergrenze(zehnZoll):
    grenzenInX, grenzenInY = (Fraction(0), Fraction(20)), (Fraction(0), Fraction(20))
    bases = [(zehnZoll, Stelle(x=Fraction(18), y=Fraction(10)))]

    assert rückungInDieFläche(bases, grenzenInX, grenzenInY) == (-3, 0)


def testEineBaseUnterDerUntergrenzeRücktInYAnDieUntergrenze(zehnZoll):
    grenzenInX, grenzenInY = (Fraction(0), Fraction(20)), (Fraction(0), Fraction(20))
    bases = [(zehnZoll, Stelle(x=Fraction(10), y=Fraction(2)))]

    assert rückungInDieFläche(bases, grenzenInX, grenzenInY) == (0, 3)


def testEineSchonÜberdeckendeBaseHältDenWegAmAnfangAnAuchWennSieSichEntfernt(zehnZoll):
    überdeckt = Stelle(x=Fraction(-999, 100), y=Fraction(0))
    amEnde = Stelle(x=Fraction(25), y=Fraction(0))
    weg = (Fraction(20), Fraction(0))

    anteil = anteilBisZurBerührung(
        [(zehnZoll, ursprung)], [(zehnZoll, überdeckt), (zehnZoll, amEnde)], weg
    )

    assert anteil == 0


def testDerWegBisZurBerührungEndetAufDemRasterHöchstensEinHundertstelVorIhr(zehnZoll):
    ort = Stelle(x=Fraction(25), y=Fraction(0))
    weg = (Fraction(20), Fraction(0))

    anteil = anteilBisZurBerührung([(zehnZoll, ursprung)], [(zehnZoll, ort)], weg)

    halt = verschoben(ursprung, teilDesWegs(weg, anteil))
    assert halt == Stelle(x=Fraction(15), y=Fraction(0))
    assert not überdecken(zehnZoll, halt, zehnZoll, ort)
    assert abstandHöchstens(zehnZoll, halt, zehnZoll, ort, Fraction(1, 100))


def testDerWegHältAufDemHundertstelRasterUndNichtAufEinemFeineren(zehnZoll):
    ort = Stelle(x=Fraction(10995, 1000), y=Fraction(0))

    anteil = anteilBisZurBerührung(
        [(zehnZoll, ursprung)], [(zehnZoll, ort)], (Fraction(2), Fraction(0))
    )

    halt = verschoben(ursprung, teilDesWegs((Fraction(2), Fraction(0)), anteil))
    assert halt == Stelle(x=Fraction(99, 100), y=Fraction(0))


def testDerWegHältAuchBeiEinemBloßenStreifenAmEndeVorDerBerührung(zehnZoll):
    streifend = Stelle(x=Fraction(199998, 10000), y=Fraction(99999975, 10000000))
    ruhend = [(zehnZoll, streifend)]
    weg = (Fraction(20), Fraction(0))

    anteil = anteilBisZurBerührung([(zehnZoll, ursprung)], ruhend, weg)

    halt = verschoben(ursprung, teilDesWegs(weg, anteil))
    assert not überdecken(zehnZoll, halt, zehnZoll, streifend)
    assert abstandHöchstens(zehnZoll, halt, zehnZoll, streifend, Fraction(1, 100))


def testDerWegHältVorDerBaseDieErUnterwegsNurStreiftWennErInEinerZweitenEndet(zehnZoll):
    gestreift = Stelle(x=Fraction(200060, 10000), y=Fraction(99999988, 10000000))
    ende = Stelle(x=Fraction(40), y=Fraction(0))
    ruhend = [(zehnZoll, gestreift), (zehnZoll, ende)]
    weg = (Fraction(40), Fraction(0))

    anteil = anteilBisZurBerührung([(zehnZoll, ursprung)], ruhend, weg)

    halt = verschoben(ursprung, teilDesWegs(weg, anteil))
    assert not überdecken(zehnZoll, halt, zehnZoll, gestreift)
    assert abstandHöchstens(zehnZoll, halt, zehnZoll, gestreift, Fraction(1, 100))


def testEinWegDerLängeNullIstGanzAuchWennDieBaseSchonÜberdeckt(zehnZoll):
    ruhend = [(zehnZoll, Stelle(x=Fraction(5), y=Fraction(0)))]

    anteil = anteilBisZurBerührung([(zehnZoll, ursprung)], ruhend, (Fraction(0), Fraction(0)))

    assert anteil == 1


def testEinWegUnterEinemRasterschrittInEineBerührteBaseBleibtLeer(zehnZoll):
    ruhend = [(zehnZoll, Stelle(x=Fraction(10), y=Fraction(0)))]

    anteil = anteilBisZurBerührung([(zehnZoll, ursprung)], ruhend, (Fraction(1, 200), Fraction(0)))

    assert anteil == 0


def testDerWegIstGanzWennDasEndeFreiIstAuchWennErEineBaseKreuzt(zehnZoll):
    ruhend = [(zehnZoll, Stelle(x=Fraction(15), y=Fraction(0)))]

    anteil = anteilBisZurBerührung([(zehnZoll, ursprung)], ruhend, (Fraction(40), Fraction(0)))

    assert anteil == 1


def testDerWegBleibtLeerWennDieBaseSchonAnDerBaseSteht(zehnZoll):
    ruhend = [(zehnZoll, Stelle(x=Fraction(10), y=Fraction(0)))]

    anteil = anteilBisZurBerührung([(zehnZoll, ursprung)], ruhend, (Fraction(5), Fraction(0)))

    assert anteil == 0


def testEineStreckeÜberdecktEineBaseAmWegAuchWennEndeUndAnfangFreiSind(zehnZoll):
    hindernis = Stelle(x=Fraction(15), y=Fraction(0))
    ende = Stelle(x=Fraction(30), y=Fraction(0))

    assert streckeÜberdeckt(zehnZoll, ursprung, ende, zehnZoll, hindernis)


def testEineStreckeNebenDerBaseÜberdecktSieNicht(zehnZoll):
    hindernis = Stelle(x=Fraction(15), y=Fraction(10))
    ende = Stelle(x=Fraction(30), y=Fraction(0))

    assert not streckeÜberdeckt(zehnZoll, ursprung, ende, zehnZoll, hindernis)
