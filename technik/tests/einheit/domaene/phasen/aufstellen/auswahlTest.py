import pytest

from arbiter.domaene.phasen.aufstellen.auswahl import Auswahl
from tests.akzeptanz.handgriffe import spielerMit


@pytest.fixture
def spieler():
    return spielerMit(2, 1)


@pytest.fixture
def auswahl():
    return Auswahl()


def einheitenUndModelle(spieler):
    ersteEinheit, zweiteEinheit = spieler.armee.einheiten
    erstesModell, zweitesModell = ersteEinheit.modelle
    return ersteEinheit, zweiteEinheit, erstesModell, zweitesModell


def testOhneAuswahlGibtEsKeineEbeneUndKeinModellIstAusgewählt(auswahl, spieler):
    ersteEinheit, _, erstesModell, _ = einheitenUndModelle(spieler)

    assert not auswahl.ganzeEinheitIstEbene(ersteEinheit)
    assert not auswahl.modellAusgewählt(erstesModell)


def testEineAusgewählteEinheitIstSelbstDieEbeneUndAlleModelleSindAusgewählt(auswahl, spieler):
    ersteEinheit, _, erstesModell, zweitesModell = einheitenUndModelle(spieler)

    auswahl.auswählen(ersteEinheit)

    assert auswahl.ganzeEinheitIstEbene(ersteEinheit)
    assert auswahl.modellAusgewählt(erstesModell)
    assert auswahl.modellAusgewählt(zweitesModell)


def testDieEbeneEinesModellsMachtNurDiesesModellAusgewählt(auswahl, spieler):
    ersteEinheit, _, erstesModell, zweitesModell = einheitenUndModelle(spieler)
    auswahl.auswählen(ersteEinheit)

    auswahl.ebeneWählen(erstesModell)

    assert auswahl.modellIstEbene(erstesModell)
    assert auswahl.modellAusgewählt(erstesModell)
    assert not auswahl.modellAusgewählt(zweitesModell)


def testNurDieAusgewählteEinheitOhneModellAlsEbeneIstGanzDieEbene(auswahl, spieler):
    ersteEinheit, zweiteEinheit, erstesModell, _ = einheitenUndModelle(spieler)
    ohneAuswahl = auswahl.ganzeEinheitIstEbene(ersteEinheit)
    auswahl.auswählen(ersteEinheit)
    ganz = auswahl.ganzeEinheitIstEbene(ersteEinheit)
    anderer = auswahl.ganzeEinheitIstEbene(zweiteEinheit)

    auswahl.ebeneWählen(erstesModell)

    assert not ohneAuswahl
    assert ganz
    assert not anderer
    assert not auswahl.ganzeEinheitIstEbene(ersteEinheit)


def testNurDasGewählteModellIstEbene(auswahl, spieler):
    ersteEinheit, _, erstesModell, zweitesModell = einheitenUndModelle(spieler)
    auswahl.auswählen(ersteEinheit)
    ohneEbene = auswahl.modellIstEbene(erstesModell)

    auswahl.ebeneWählen(erstesModell)

    assert not ohneEbene
    assert auswahl.modellIstEbene(erstesModell)
    assert not auswahl.modellIstEbene(zweitesModell)


def testDieEbeneAbwählenKehrtZurEinheitZurück(auswahl, spieler):
    ersteEinheit, _, erstesModell, _ = einheitenUndModelle(spieler)
    auswahl.auswählen(ersteEinheit)
    auswahl.ebeneWählen(erstesModell)

    auswahl.ebeneAbwählen(erstesModell)

    assert auswahl.ganzeEinheitIstEbene(ersteEinheit)


def testEineNeueAuswahlSetztDieEbeneZurück(auswahl, spieler):
    ersteEinheit, zweiteEinheit, erstesModell, _ = einheitenUndModelle(spieler)
    auswahl.auswählen(ersteEinheit)
    auswahl.ebeneWählen(erstesModell)

    auswahl.auswählen(zweiteEinheit)
    auswahl.auswählen(ersteEinheit)

    assert auswahl.ganzeEinheitIstEbene(ersteEinheit)


def testDieselbeEinheitErneutAuswählenBehältDieEbene(auswahl, spieler):
    ersteEinheit, _, erstesModell, _ = einheitenUndModelle(spieler)
    auswahl.auswählen(ersteEinheit)
    auswahl.ebeneWählen(erstesModell)

    auswahl.auswählen(ersteEinheit)

    assert auswahl.modellIstEbene(erstesModell)


def testEinModellEinerNichtAusgewähltenEinheitKannNichtAbgewähltWerden(auswahl, spieler):
    ersteEinheit, zweiteEinheit, erstesModell, _ = einheitenUndModelle(spieler)
    auswahl.auswählen(zweiteEinheit)

    with pytest.raises(ValueError):
        auswahl.ebeneAbwählen(erstesModell)


def testEinModellEinerNichtAusgewähltenEinheitKannNichtDieEbeneSein(auswahl, spieler):
    ersteEinheit, zweiteEinheit, erstesModell, _ = einheitenUndModelle(spieler)
    auswahl.auswählen(zweiteEinheit)

    with pytest.raises(ValueError):
        auswahl.ebeneWählen(erstesModell)
