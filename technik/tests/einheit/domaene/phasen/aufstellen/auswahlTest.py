import pytest

from arbiter.domaene.phasen.aufstellen.auswahl import Auswahl
from tests.akzeptanz.handgriffe import spielerMit


@pytest.fixture
def spieler():
    return spielerMit(2, 1)


@pytest.fixture
def auswahl(spieler):
    return Auswahl([spieler], set())


def einheitenUndModelle(spieler):
    ersteEinheit, zweiteEinheit = spieler.armee.einheiten
    erstesModell, zweitesModell = ersteEinheit.modelle
    return ersteEinheit, zweiteEinheit, erstesModell, zweitesModell


def testOhneAuswahlGibtEsKeineEbeneUndKeinModellIstAusgewählt(auswahl, spieler):
    ersteEinheit, _, erstesModell, _ = einheitenUndModelle(spieler)

    assert auswahl.ebene(ersteEinheit) is None
    assert not auswahl.modellAusgewählt(erstesModell)


def testEineAusgewählteEinheitIstSelbstDieEbeneUndAlleModelleSindAusgewählt(auswahl, spieler):
    ersteEinheit, _, erstesModell, zweitesModell = einheitenUndModelle(spieler)

    auswahl.auswählen(ersteEinheit)

    assert auswahl.ebene(ersteEinheit) is ersteEinheit
    assert auswahl.modellAusgewählt(erstesModell)
    assert auswahl.modellAusgewählt(zweitesModell)


def testDieEbeneEinesModellsMachtNurDiesesModellAusgewählt(auswahl, spieler):
    ersteEinheit, _, erstesModell, zweitesModell = einheitenUndModelle(spieler)
    auswahl.auswählen(ersteEinheit)

    auswahl.ebeneWählen(erstesModell)

    assert auswahl.ebene(ersteEinheit) is erstesModell
    assert auswahl.modellAusgewählt(erstesModell)
    assert not auswahl.modellAusgewählt(zweitesModell)


def testDieEbeneAbwählenKehrtZurEinheitZurück(auswahl, spieler):
    ersteEinheit, _, erstesModell, _ = einheitenUndModelle(spieler)
    auswahl.auswählen(ersteEinheit)
    auswahl.ebeneWählen(erstesModell)

    auswahl.ebeneAbwählen(erstesModell)

    assert auswahl.ebene(ersteEinheit) is ersteEinheit


def testEineNeueAuswahlSetztDieEbeneZurück(auswahl, spieler):
    ersteEinheit, zweiteEinheit, erstesModell, _ = einheitenUndModelle(spieler)
    auswahl.auswählen(ersteEinheit)
    auswahl.ebeneWählen(erstesModell)

    auswahl.auswählen(zweiteEinheit)
    auswahl.auswählen(ersteEinheit)

    assert auswahl.ebene(ersteEinheit) is ersteEinheit


def testDieselbeEinheitErneutAuswählenBehältDieEbene(auswahl, spieler):
    ersteEinheit, _, erstesModell, _ = einheitenUndModelle(spieler)
    auswahl.auswählen(ersteEinheit)
    auswahl.ebeneWählen(erstesModell)

    auswahl.auswählen(ersteEinheit)

    assert auswahl.ebene(ersteEinheit) is erstesModell


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
