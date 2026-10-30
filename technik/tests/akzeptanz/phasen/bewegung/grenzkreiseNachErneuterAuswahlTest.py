"""BEW-15 · Grenzkreise nach erneuter Auswahl."""

import pytest

from tests.akzeptanz.grenzen import (
    ganzeEinheitAuswählen,
    grenzeDerBewegung,
    grenzenDerEinheit,
    zweiZollZurMitte,
)
from tests.akzeptanz.schlacht import mitteDesSpielfelds


def aufDieLeereKarteKlicken(schlacht, _andereEinheit) -> None:
    schlacht.karteAnklicken(mitteDesSpielfelds)


def einModellDerAnderenAnklicken(schlacht, andereEinheit) -> None:
    modellDerAnderen, *_ = andereEinheit.modelle
    schlacht.modellAnklicken(modellDerAnderen)


abwahlen = {
    "leereKarte": aufDieLeereKarteKlicken,
    "modellDerAnderenEinheit": einModellDerAnderenAnklicken,
}


@pytest.mark.parametrize("abwahl", list(abwahlen), ids=list(abwahlen))
def testBew15_1NachErneuterAuswahlZeigtDieKarteDieEinhüllendeUmDieStellenZuBeginnDerPhase(
    einheitAmZug, abwahl
):
    schlacht, einheit, andereEinheit, _ = einheitAmZug
    stellen = ganzeEinheitAuswählen(schlacht, einheit)
    erstes, *_ = einheit.modelle
    schlacht.modellLoslassen(erstes, zweiZollZurMitte(stellen[erstes]))
    abwahlen[abwahl](schlacht, andereEinheit)
    ganzeEinheitAuswählen(schlacht, andereEinheit)
    (modellDerAnderen, *_) = andereEinheit.modelle
    schlacht.modellLoslassen(modellDerAnderen, zweiZollZurMitte(schlacht.stelle(modellDerAnderen)))

    schlacht.modellAnklicken(erstes)

    assert schlacht.stelle(erstes) != stellen[erstes]
    assert grenzenDerEinheit(schlacht, einheit) == {grenzeDerBewegung(stellen)}
