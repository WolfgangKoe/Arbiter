from fractions import Fraction
from math import hypot

from arbiter.domaene import messen
from arbiter.domaene.phasen.bewegung.fliegen import (
    Umgebung,
    Weite,
    anteilBisZurNahkampfreichweite,
    nachFremdenBasesGerückt,
)
from arbiter.domaene.spielobjekte import Spielfeld, Stelle
from tests.einheit.modelle import modellMit

breite, länge = Fraction(60), Fraction(44)
spielfeld = Spielfeld(seitenlängen=(breite, länge))
hundertstel = Fraction(1, 100)
nachLinks = (Fraction(-15), Fraction(0))
fremderOrt = Stelle(x=Fraction(10), y=Fraction(10))
übersFremdeOrt = Stelle(x=Fraction(11), y=Fraction(10))
weglänge = 30
kürzesterRückwegAnDerKante = 91**0.5


def stelleAn(inX: int, inY: int) -> Stelle:
    return Stelle(x=Fraction(inX), y=Fraction(inY))


def abstand(erste: Stelle, zweite: Stelle) -> float:
    return hypot(float(erste.x - zweite.x), float(erste.y - zweite.y))


def abstandLiegtEinHundertstelÜber(mindestens: float, gerückt: Stelle) -> bool:
    return mindestens <= abstand(gerückt, übersFremdeOrt) <= mindestens + float(hundertstel)


def wegNachRechts(zoll: int) -> messen.Weg:
    return Fraction(zoll), Fraction(0)


def testOhneModellInNahkampfreichweiteAmEndeHältNichtsAn(zehnZoll):
    modell, gegner = modellMit(zehnZoll), modellMit(zehnZoll)
    vorige, gegnerOrt = {modell: stelleAn(0, 0)}, {gegner: stelleAn(20, 0)}

    anteil = anteilBisZurNahkampfreichweite(vorige, wegNachRechts(50), gegnerOrt, Fraction(1))

    assert anteil == 1


def testEndetDerWegInDerNahkampfreichweiteHältErAnDerLetztenStelleDavorAn(zehnZoll):
    modell, gegner = modellMit(zehnZoll), modellMit(zehnZoll)
    vorige, gegnerOrt = {modell: stelleAn(0, 0)}, {gegner: stelleAn(20, 0)}
    erstesDarin = 9

    anteil = anteilBisZurNahkampfreichweite(vorige, wegNachRechts(weglänge), gegnerOrt, Fraction(1))

    assert erstesDarin - hundertstel <= weglänge * anteil < erstesDarin


def testDasEndeVorDemWegendeBestimmtDieNahkampfreichweiteAmEnde(zehnZoll):
    modell, gegner = modellMit(zehnZoll), modellMit(zehnZoll)
    vorige, gegnerOrt = {modell: stelleAn(0, 0)}, {gegner: stelleAn(20, 0)}
    erstesDarin = 9

    anteil = anteilBisZurNahkampfreichweite(vorige, wegNachRechts(50), gegnerOrt, Fraction(1, 2))

    assert erstesDarin - hundertstel <= 50 * anteil < erstesDarin


def testOhneÜberdeckungBleibenDieStellenUnverändert(zehnZoll):
    modell, fremder = modellMit(zehnZoll), modellMit(zehnZoll)
    gesetzt = {modell: stelleAn(30, 10)}
    umgebung = Umgebung({fremder: fremderOrt}, {}, spielfeld)

    assert nachFremdenBasesGerückt(gesetzt, nachLinks, umgebung) is gesetzt


def testEineÜberdeckteBaseRücktAnDenNächstenFreienPunktAmRandDerFremden(zehnZoll):
    modell, fremder = modellMit(zehnZoll), modellMit(zehnZoll)
    umgebung = Umgebung({fremder: fremderOrt}, {}, spielfeld)

    gerückt = nachFremdenBasesGerückt({modell: übersFremdeOrt}, nachLinks, umgebung)

    stelle = gerückt[modell]
    assert not messen.überdecken(modell.base, stelle, fremder.base, fremderOrt)
    assert abstandLiegtEinHundertstelÜber(9, stelle)


def testEinGegnerHältDieNahkampfreichweiteVonDerBaseFern(zehnZoll):
    modell, gegner = modellMit(zehnZoll), modellMit(zehnZoll)
    umgebung = Umgebung({gegner: fremderOrt}, {gegner: fremderOrt}, spielfeld)

    gerückt = nachFremdenBasesGerückt({modell: übersFremdeOrt}, nachLinks, umgebung)

    stelle = gerückt[modell]
    assert not messen.abstandHöchstens(modell.base, stelle, gegner.base, fremderOrt, Fraction(1))
    assert abstandLiegtEinHundertstelÜber(10, stelle)


def testAnDerSpielfeldkanteRücktDieBaseGanzInsSpielfeldHinein(zehnZoll):
    modell, fremder = modellMit(zehnZoll), modellMit(zehnZoll)
    fremderAmRand, amRand = stelleAn(50, 22), stelleAn(51, 22)
    umgebung = Umgebung({fremder: fremderAmRand}, {}, spielfeld)

    gerückt = nachFremdenBasesGerückt({modell: amRand}, nachLinks, umgebung)

    stelle = gerückt[modell]
    assert messen.ganzIn(modell.base, stelle, (Fraction(0), breite), (Fraction(0), länge))
    assert not messen.überdecken(modell.base, stelle, fremder.base, fremderAmRand)
    rückweg = abstand(stelle, amRand)
    assert kürzesterRückwegAnDerKante <= rückweg <= kürzesterRückwegAnDerKante + float(hundertstel)


def testDieBewegungsweiteBegrenztDieDistanzDerGerücktenBase(zehnZoll):
    modell, fremder = modellMit(zehnZoll), modellMit(zehnZoll)
    weiten = {modell: Weite(stelleAn(14, 10), Fraction(6))}
    umgebung = Umgebung({fremder: fremderOrt}, {}, spielfeld, weiten)

    gerückt = nachFremdenBasesGerückt({modell: übersFremdeOrt}, nachLinks, umgebung)

    assert gerückt == {modell: stelleAn(20, 10)}


def testGibtEsKeinenFreienPunktInDerBewegungsweiteBleibenDieStellenUnverändert(zehnZoll):
    modell, fremder = modellMit(zehnZoll), modellMit(zehnZoll)
    gesetzt = {modell: übersFremdeOrt}
    weiten = {modell: Weite(stelleAn(14, 10), Fraction(5))}
    umgebung = Umgebung({fremder: fremderOrt}, {}, spielfeld, weiten)

    assert nachFremdenBasesGerückt(gesetzt, nachLinks, umgebung) is gesetzt


def testMehrereBasesRückenGemeinsamUmDenselbenWeg(zehnZoll):
    erstes, zweites, fremder = (modellMit(zehnZoll) for _ in range(3))
    gesetzt = {erstes: übersFremdeOrt, zweites: stelleAn(11, 30)}
    umgebung = Umgebung({fremder: fremderOrt}, {}, spielfeld)

    gerückt = nachFremdenBasesGerückt(gesetzt, nachLinks, umgebung)

    wegErstes = messen.wegZwischen(gesetzt[erstes], gerückt[erstes])
    assert messen.wegZwischen(gesetzt[zweites], gerückt[zweites]) == wegErstes
    assert wegErstes != (0, 0)
