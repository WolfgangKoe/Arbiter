from fractions import Fraction

import pytest

from arbiter.domaene.phasen.aufstellen.auswahl import Auswahl
from arbiter.domaene.spielobjekte import Stelle
from tests.akzeptanz.handgriffe import spielerMit


@pytest.fixture
def spieler():
    return spielerMit(2, 1)


@pytest.fixture
def auswahl():
    return Auswahl()


def anklicken(auswahl, spieler, modell, gesetzt=None):
    gesetzteModelle = spieler.armee.modelle if gesetzt is None else gesetzt
    stellen = {gesetztes: Stelle(x=Fraction(0), y=Fraction(0)) for gesetztes in gesetzteModelle}
    auswahl.modellAnklicken((spieler, spielerMit(1)), modell, stellen)


def einheitenUndModelle(spieler):
    ersteEinheit, zweiteEinheit = spieler.armee.einheiten
    erstesModell, zweitesModell = ersteEinheit.modelle
    return ersteEinheit, zweiteEinheit, erstesModell, zweitesModell


def testOhneAuswahlGibtEsKeineEbeneUndKeinModellIstAusgewählt(auswahl, spieler):
    ersteEinheit, _, erstesModell, _ = einheitenUndModelle(spieler)

    assert not auswahl.hatEinheitenebene(ersteEinheit)
    assert not auswahl.modellAusgewählt(erstesModell)


def testEineAusgewählteEinheitIstSelbstDieEbeneUndAlleModelleSindAusgewählt(auswahl, spieler):
    ersteEinheit, _, erstesModell, zweitesModell = einheitenUndModelle(spieler)

    auswahl.auswählen(ersteEinheit)

    assert auswahl.hatEinheitenebene(ersteEinheit)
    assert auswahl.modellAusgewählt(erstesModell)
    assert auswahl.modellAusgewählt(zweitesModell)


def testDieEbeneEinesModellsMachtNurDiesesModellAusgewählt(auswahl, spieler):
    ersteEinheit, _, erstesModell, zweitesModell = einheitenUndModelle(spieler)
    auswahl.auswählen(ersteEinheit)

    anklicken(auswahl, spieler, erstesModell)

    assert auswahl.istModellebene(erstesModell)
    assert auswahl.modellAusgewählt(erstesModell)
    assert not auswahl.modellAusgewählt(zweitesModell)


def testNurDieAusgewählteEinheitOhneModellebeneHatDieEinheitenebene(auswahl, spieler):
    ersteEinheit, zweiteEinheit, erstesModell, _ = einheitenUndModelle(spieler)
    ohneAuswahl = auswahl.hatEinheitenebene(ersteEinheit)
    auswahl.auswählen(ersteEinheit)
    ganz = auswahl.hatEinheitenebene(ersteEinheit)
    anderer = auswahl.hatEinheitenebene(zweiteEinheit)

    anklicken(auswahl, spieler, erstesModell)

    assert not ohneAuswahl
    assert ganz
    assert not anderer
    assert not auswahl.hatEinheitenebene(ersteEinheit)


def testNurDasGewählteModellIstEbene(auswahl, spieler):
    ersteEinheit, _, erstesModell, zweitesModell = einheitenUndModelle(spieler)
    auswahl.auswählen(ersteEinheit)
    ohneEbene = auswahl.istModellebene(erstesModell)

    anklicken(auswahl, spieler, erstesModell)

    assert not ohneEbene
    assert auswahl.istModellebene(erstesModell)
    assert not auswahl.istModellebene(zweitesModell)


def testDasEbeneModellErneutAnklickenKehrtZurEinheitZurück(auswahl, spieler):
    ersteEinheit, _, erstesModell, _ = einheitenUndModelle(spieler)
    auswahl.auswählen(ersteEinheit)
    anklicken(auswahl, spieler, erstesModell)

    anklicken(auswahl, spieler, erstesModell)

    assert auswahl.hatEinheitenebene(ersteEinheit)


def testEinAnderesModellAnklickenWechseltDieEbene(auswahl, spieler):
    ersteEinheit, _, erstesModell, zweitesModell = einheitenUndModelle(spieler)
    auswahl.auswählen(ersteEinheit)
    anklicken(auswahl, spieler, erstesModell)

    anklicken(auswahl, spieler, zweitesModell)

    assert auswahl.istModellebene(zweitesModell)
    assert not auswahl.istModellebene(erstesModell)


def testEinModellEinerNichtAusgewähltenEinheitAnklickenWähltDieEinheitAus(auswahl, spieler):
    ersteEinheit, zweiteEinheit, erstesModell, _ = einheitenUndModelle(spieler)
    auswahl.auswählen(zweiteEinheit)

    anklicken(auswahl, spieler, erstesModell)

    assert auswahl.hatEinheitenebene(ersteEinheit)
    assert not auswahl.ausgewählt(zweiteEinheit)


def testEineNeueAuswahlSetztDieEbeneZurück(auswahl, spieler):
    ersteEinheit, zweiteEinheit, erstesModell, _ = einheitenUndModelle(spieler)
    auswahl.auswählen(ersteEinheit)
    anklicken(auswahl, spieler, erstesModell)

    auswahl.auswählen(zweiteEinheit)
    auswahl.auswählen(ersteEinheit)

    assert auswahl.hatEinheitenebene(ersteEinheit)


def testDieselbeEinheitErneutAuswählenBehältDieEbene(auswahl, spieler):
    ersteEinheit, _, erstesModell, _ = einheitenUndModelle(spieler)
    auswahl.auswählen(ersteEinheit)
    anklicken(auswahl, spieler, erstesModell)

    auswahl.auswählen(ersteEinheit)

    assert auswahl.istModellebene(erstesModell)


def testEinUngesetztesModellAnklickenÄndertNichts(auswahl, spieler):
    ersteEinheit, _, erstesModell, _ = einheitenUndModelle(spieler)
    auswahl.auswählen(ersteEinheit)

    anklicken(auswahl, spieler, erstesModell, gesetzt=())

    assert auswahl.hatEinheitenebene(ersteEinheit)


def testEinModellKeinesSpielersAnklickenWirftEinenFehler(auswahl, spieler):
    (fremdes,) = spielerMit(1).armee.modelle

    with pytest.raises(ValueError):
        anklicken(auswahl, spieler, fremdes, gesetzt=(fremdes,))
