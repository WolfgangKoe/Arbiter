"""BEW-15 · Grenzkreise nach erneuter Auswahl."""

import pytest

from tests.akzeptanz.grenzen import grenzeDerBewegung, grenzenDerEinheit, zweiZollEntlangDerReihe
from tests.akzeptanz.schlacht import mitteDesSpielfelds
from tests.akzeptanz.vorruecken import ganzeEinheitAuswählen


def aufDasSpielfeldKlickenWoKeinModellSteht(schlacht, _andereEinheit) -> None:
    schlacht.spielfeldAnklicken(mitteDesSpielfelds)


def einModellDerAnderenAnklicken(schlacht, andereEinheit) -> None:
    modellDerAnderen, *_ = andereEinheit.modelle
    schlacht.modellAnklicken(modellDerAnderen)


abwahlen = {
    "spielfeldWoKeinModellSteht": aufDasSpielfeldKlickenWoKeinModellSteht,
    "modellDerAnderenEinheit": einModellDerAnderenAnklicken,
}


@pytest.mark.parametrize("abwahl", list(abwahlen), ids=list(abwahlen))
def testBew15_1NachErneuterAuswahlZeigtDasSpielfeldDieEinhüllendeUmDieStellenZuBeginnDerPhase(
    einheitAmZug, abwahl
):
    schlacht, einheit, andereEinheit, _ = einheitAmZug
    stellen = ganzeEinheitAuswählen(schlacht, einheit)
    erstes, *_ = einheit.modelle
    schlacht.modellLoslassen(erstes, zweiZollEntlangDerReihe(stellen[erstes]))
    abwahlen[abwahl](schlacht, andereEinheit)
    ganzeEinheitAuswählen(schlacht, andereEinheit)
    (modellDerAnderen, *_) = andereEinheit.modelle
    schlacht.modellLoslassen(
        modellDerAnderen, zweiZollEntlangDerReihe(schlacht.stelle(modellDerAnderen))
    )

    schlacht.modellAnklicken(erstes)

    assert schlacht.stelle(erstes) != stellen[erstes]
    assert grenzenDerEinheit(schlacht, einheit) == {grenzeDerBewegung(stellen)}
