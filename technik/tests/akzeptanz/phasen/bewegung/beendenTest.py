"""BEW-4 · Bewegungsphase beenden."""

from http import HTTPStatus

from arbiter.domaene.querschnitt.schlachtrunden import Phase
from arbiter.domaene.sperre import Grund
from tests.akzeptanz.bildschirm import gründeAlsText, knopfDerSeite, sperrmeldungWarten
from tests.akzeptanz.dienst import phaseBeenden, spielstandVon
from tests.akzeptanz.handgriffe import sperrgründe
from tests.akzeptanz.schlacht import einModellAusDerKohärenzZiehen, jetzigeStellen

phaseBeendenKnopf = "Phase beenden"


def testBew4_1OhneKohärenzSperrtPhaseBeendenMitDemGrundKeineKohärenz(
    schlachtInDerBewegungsphase, boyz
):
    einModellAusDerKohärenzZiehen(schlachtInDerBewegungsphase, boyz)

    gründe = sperrgründe(schlachtInDerBewegungsphase.phaseBeenden)

    assert gründe == {Grund.keineKohärenz}


def testBew4_1NachDerSperreBleibtDiePhaseUndStehtJedesModellWieDavor(
    schlachtInDerBewegungsphase, boyz, spielerEins
):
    einModellAusDerKohärenzZiehen(schlachtInDerBewegungsphase, boyz)
    davor = jetzigeStellen(schlachtInDerBewegungsphase, boyz)

    sperrgründe(schlachtInDerBewegungsphase.phaseBeenden)

    assert schlachtInDerBewegungsphase.phase is Phase.bewegungsphase
    assert schlachtInDerBewegungsphase.amZug is spielerEins
    assert jetzigeStellen(schlachtInDerBewegungsphase, boyz) == davor


def testBew4_1DerDienstSperrtMitDemGrundKeineKohärenzUndLässtDenStandWieDavor(
    dienstDerSchlacht, schlachtInDerBewegungsphase, boyz
):
    einModellAusDerKohärenzZiehen(schlachtInDerBewegungsphase, boyz)
    spielstandDavor = spielstandVon(dienstDerSchlacht)

    antwort = phaseBeenden(dienstDerSchlacht, 1, 1, Phase.bewegungsphase)

    assert antwort.status_code == HTTPStatus.CONFLICT
    assert antwort.get_json()["gründe"] == [Grund.keineKohärenz.value]
    assert antwort.get_json()["spielstand"] == spielstandDavor
    assert schlachtInDerBewegungsphase.phase is Phase.bewegungsphase


def testBew4_1DieSeiteNenntBeimKlickAufPhaseBeendenDenGrundKeineKohärenz(
    bildschirm, beendeteAufstellung, schlachtInDerBewegungsphase, boyz
):
    einModellAusDerKohärenzZiehen(schlachtInDerBewegungsphase, boyz)
    seite = bildschirm.seiteZuSchlacht(beendeteAufstellung, schlachtInDerBewegungsphase)

    knopfDerSeite(seite, phaseBeendenKnopf).click()

    assert sperrmeldungWarten(seite, {Grund.keineKohärenz}) == gründeAlsText({Grund.keineKohärenz})
    assert schlachtInDerBewegungsphase.phase is Phase.bewegungsphase
