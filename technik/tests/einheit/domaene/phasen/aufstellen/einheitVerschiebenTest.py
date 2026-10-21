from fractions import Fraction

from arbiter.domaene.phasen.aufstellen.einheitVerschieben import hineingerückt, verschobeneStellen
from arbiter.domaene.spielobjekte import Modell, Stelle

zone = (Fraction(0), Fraction(44))


def stelleAn(inX: int, inY: int) -> Stelle:
    return Stelle(x=Fraction(inX), y=Fraction(inY))


def testDieGruppeFolgtDemWegDesGezogenenUndDasGezogeneStehtAmZiel(zehnZoll):
    gezogenes, zweites = Modell(base=zehnZoll), Modell(base=zehnZoll)
    gruppe = {gezogenes: stelleAn(10, 10), zweites: stelleAn(10, 20)}

    verschoben = verschobeneStellen(gruppe, gezogenes, stelleAn(13, 6))

    assert verschoben == {gezogenes: stelleAn(13, 6), zweites: stelleAn(13, 16)}


def testEinNochNichtGesetztesModellBewegtDieGruppeNicht(zehnZoll):
    gesetztes, neues = Modell(base=zehnZoll), Modell(base=zehnZoll)
    gruppe = {gesetztes: stelleAn(10, 10)}

    assert verschobeneStellen(gruppe, neues, stelleAn(13, 6)) == {neues: stelleAn(13, 6)}


def testEineGruppeInDerZoneBleibtStehen(zehnZoll):
    modell = Modell(base=zehnZoll)

    assert hineingerückt({modell: stelleAn(20, 20)}, (zone, zone)) == {modell: stelleAn(20, 20)}


def testEineGruppeVorDerZoneRücktGemeinsamHinein(zehnZoll):
    erstes, zweites = Modell(base=zehnZoll), Modell(base=zehnZoll)
    stellen = {erstes: stelleAn(2, 20), zweites: stelleAn(2, 30)}

    assert hineingerückt(stellen, (zone, zone)) == {
        erstes: stelleAn(5, 20),
        zweites: stelleAn(5, 30),
    }


def testEineGruppeHinterDerZoneRücktGemeinsamHinein(zehnZoll):
    erstes, zweites = Modell(base=zehnZoll), Modell(base=zehnZoll)
    stellen = {erstes: stelleAn(42, 20), zweites: stelleAn(42, 30)}

    assert hineingerückt(stellen, (zone, zone)) == {
        erstes: stelleAn(39, 20),
        zweites: stelleAn(39, 30),
    }
