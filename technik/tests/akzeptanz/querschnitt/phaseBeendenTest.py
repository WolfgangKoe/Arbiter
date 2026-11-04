"""QUE-11 · Phase beenden nur im Zug."""

import pytest
from playwright.sync_api import expect

from tests.akzeptanz.bildschirm import knopfDerSeite, phaseBeendenKnopf, spielerAmZug
from tests.akzeptanz.schlacht import (
    letzteSchlachtrunde,
    phaseBeendenBis,
    phasenEinesZugs,
    zügeBeenden,
)

ersterZugKnopf = "Erster Zug"


@pytest.mark.parametrize("phase", phasenEinesZugs, ids=[phase.name for phase in phasenEinesZugs])
def testQue11_1IstEinSpielerAmZugZeigtDieSeitePhaseBeenden(
    bildschirm, beendeteAufstellung, schlacht, spielerMitDemErstenZug, phase
):
    schlacht.ersterZugWählen(spielerMitDemErstenZug)
    phaseBeendenBis(schlacht, phase)

    seite = bildschirm.seiteZuSchlacht(beendeteAufstellung, schlacht)

    expect(spielerAmZug(seite)).to_have_count(1)
    expect(knopfDerSeite(seite, phaseBeendenKnopf)).to_have_count(1)


def testQue11_1VorDemErstenZugZeigtDieSeiteKeinPhaseBeenden(
    bildschirm, beendeteAufstellung, schlacht
):
    seite = bildschirm.seiteZuSchlacht(beendeteAufstellung, schlacht)

    expect(knopfDerSeite(seite, ersterZugKnopf)).to_have_count(2)
    expect(knopfDerSeite(seite, phaseBeendenKnopf)).to_have_count(0)


def testQue11_1InDerAufstellungZeigtDieSeiteKeinPhaseBeenden(bildschirm, ausgangsaufstellung):
    seite = bildschirm.seiteZu(ausgangsaufstellung)

    expect(seite.locator(".karte")).to_have_count(1)
    expect(knopfDerSeite(seite, phaseBeendenKnopf)).to_have_count(0)


def testQue11_1NachDemEndeDerSchlachtZeigtDieSeiteKeinPhaseBeenden(
    bildschirm, beendeteAufstellung, schlacht, spielerMitDemErstenZug
):
    schlacht.ersterZugWählen(spielerMitDemErstenZug)
    zügeBeenden(schlacht, 2 * letzteSchlachtrunde())

    seite = bildschirm.seiteZuSchlacht(beendeteAufstellung, schlacht)

    expect(seite.locator(".kopfzeileSchlachtBeendet")).to_have_count(1)
    expect(knopfDerSeite(seite, phaseBeendenKnopf)).to_have_count(0)
