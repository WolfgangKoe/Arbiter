"""BEW-10 · Modelle des anderen Spielers."""

from fractions import Fraction
from http import HTTPStatus

import pytest

from tests.akzeptanz.bildschirm import seiteDerSchlachtMitEingabe, sperrmeldungenDerSeite
from tests.akzeptanz.dienst import modellLoslassen
from tests.akzeptanz.handgriffe import stellenAllerModelle, versetzt
from tests.akzeptanz.ziehen import mitMausUndFinger, modellZiehen

dreiZollNachWesten = (Fraction(-3), Fraction(0))
dreiZollNachOsten = (Fraction(3), Fraction(0))


@pytest.fixture(params=["spielerEinsAmZug", "spielerZweiAmZug"])
def zugAnEinemFremdenModell(request, boyz, necronWarriors):
    schlachtUndEinheit = {
        "spielerEinsAmZug": ("schlachtInDerBewegungsphase", necronWarriors, dreiZollNachWesten),
        "spielerZweiAmZug": (
            "schlachtInDerBewegungsphaseDesZweitenSpielers",
            boyz,
            dreiZollNachOsten,
        ),
    }
    fixture, einheit, weg = schlachtUndEinheit[request.param]
    schlacht = request.getfixturevalue(fixture)
    *_, modell = einheit.modelle
    return schlacht, einheit, modell, versetzt(schlacht.stelle(modell), weg)


@pytest.mark.parametrize("ausgewählt", [False, True], ids=["ohneAuswahl", "einheitAusgewählt"])
def testBew10_1EinModellDesAnderenSpielersBleibtBeimLoslassenStehenOhneGrund(
    zugAnEinemFremdenModell, ausgewählt
):
    schlacht, einheit, modell, ziel = zugAnEinemFremdenModell
    if ausgewählt:
        schlacht.auswählen(einheit)
    davor = stellenAllerModelle(schlacht)

    schlacht.modellLoslassen(modell, ziel)

    assert stellenAllerModelle(schlacht) == davor


def testBew10_1DerDienstAntwortetBeimModellDesAnderenSpielersOhneGrundUndÄndertNichts(
    dienstDerSchlacht, beendeteAufstellung, schlachtInDerBewegungsphase, necronWarriors
):
    *_, modell = necronWarriors.modelle
    ziel = versetzt(schlachtInDerBewegungsphase.stelle(modell), dreiZollNachWesten)
    davor = stellenAllerModelle(schlachtInDerBewegungsphase)

    antwort = modellLoslassen(dienstDerSchlacht, beendeteAufstellung, necronWarriors, modell, ziel)

    assert antwort.status_code == HTTPStatus.OK
    assert "gründe" not in antwort.get_json()
    assert stellenAllerModelle(schlachtInDerBewegungsphase) == davor


@mitMausUndFinger
def testBew10_1DieSeiteLässtEinModellDesAnderenSpielersStehenOhneSperrmeldung(
    bildschirm, beendeteAufstellung, schlachtInDerBewegungsphase, necronWarriors, eingabe
):
    *_, modell = necronWarriors.modelle
    stelle = schlachtInDerBewegungsphase.stelle(modell)
    davor = stellenAllerModelle(schlachtInDerBewegungsphase)
    seite = seiteDerSchlachtMitEingabe(
        bildschirm, beendeteAufstellung, schlachtInDerBewegungsphase, eingabe
    )

    modellZiehen(seite, stelle, versetzt(stelle, dreiZollNachWesten), eingabe)

    assert stellenAllerModelle(schlachtInDerBewegungsphase) == davor
    assert sperrmeldungenDerSeite(seite) == []
