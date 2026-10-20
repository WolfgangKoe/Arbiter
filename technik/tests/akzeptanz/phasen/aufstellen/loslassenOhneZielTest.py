"""AUF-16 · Loslassen ohne Ziel."""

from http import HTTPStatus

import pytest

from arbiter.domaene.sperre import Grund
from tests.akzeptanz.bildschirm import inhaltDerSeite, sperrmeldungenDerSeite
from tests.akzeptanz.dienst import modellAufAblageLoslassen, spielstandVon
from tests.akzeptanz.handgriffe import (
    nachDerWahlDerAufstellungszone,
    sperrgründe,
    stellenAllerModelle,
    stellenDerEinheit,
)
from tests.akzeptanz.ziehen import (
    amKopfDerSeite,
    modellAufDieAblageZiehen,
    punktAufDerKarte,
    ziehenOhneAnfrage,
)

gesetzteModelle = pytest.mark.parametrize(
    "gesetzt", [1, 3], ids=["einModellGesetzt", "dreiModelleGesetzt"]
)


def testAuf16_3EinGesetztesModellAufDerAblageDesAnderenSpielersIstNichtWählbar(
    aufstellung, ersterSpieler, zweiterSpieler
):
    nachDerWahlDerAufstellungszone(aufstellung, gewinner=ersterSpieler)
    einheit, _ = zweiterSpieler.armee.einheiten
    (modell, stelle), _ = stellenDerEinheit(aufstellung, zweiterSpieler, einheit)
    aufstellung.modellSetzen(modell, stelle)

    gründe = sperrgründe(aufstellung.modellAufAblageLoslassen, modell, ersterSpieler)

    assert gründe == {Grund.nichtWählbar}
    assert aufstellung.stelle(modell) == stelle
    assert aufstellung.einheitInAufstellung is einheit


@gesetzteModelle
def testAuf16_6EinGesetztesModellAufDerAblageSeinesSpielersStehtNachDemLoslassenWieDavor(
    aufstellungNachDerZonenwahl, boyzSetzen, spielerEins, gesetzt
):
    (modell, _), *_ = boyzSetzen(gesetzt)
    davor = stellenAllerModelle(aufstellungNachDerZonenwahl)
    einheitInAufstellungDavor = aufstellungNachDerZonenwahl.einheitInAufstellung

    aufstellungNachDerZonenwahl.modellAufAblageLoslassen(modell, spielerEins)

    assert stellenAllerModelle(aufstellungNachDerZonenwahl) == davor
    assert aufstellungNachDerZonenwahl.einheitInAufstellung is einheitInAufstellungDavor


@gesetzteModelle
def testAuf16_6DerDienstAntwortetBeiEinemModellAufDerEigenenAblageOhneGrundUndÄndertNichts(
    dienst, aufstellungNachDerZonenwahl, boyz, boyzSetzen, gesetzt
):
    (modell, _), *_ = boyzSetzen(gesetzt)
    davor = spielstandVon(dienst)

    antwort = modellAufAblageLoslassen(dienst, aufstellungNachDerZonenwahl, boyz, modell, 1)

    assert antwort.status_code == HTTPStatus.OK
    assert spielstandVon(dienst) == davor


@gesetzteModelle
def testAuf16_6DieSeiteLässtEinModellAufDerEigenenAblageStehenUndNenntKeinenGrund(
    bildschirm, aufstellungNachDerZonenwahl, boyzSetzen, gesetzt
):
    (_, stelleDesModells), *_ = boyzSetzen(gesetzt)
    seite = bildschirm.seiteZu(aufstellungNachDerZonenwahl)
    davor = stellenAllerModelle(aufstellungNachDerZonenwahl)

    antwort = modellAufDieAblageZiehen(seite, stelleDesModells, "Spieler 1")

    assert antwort.status == HTTPStatus.OK
    assert stellenAllerModelle(aufstellungNachDerZonenwahl) == davor
    assert sperrmeldungenDerSeite(seite) == []


@gesetzteModelle
def testAuf16_6EinModellNebenKarteUndAblagenStehtNachDemLoslassenWieDavor(
    bildschirm, aufstellungNachDerZonenwahl, boyzSetzen, gesetzt
):
    (_, stelleDesModells), *_ = boyzSetzen(gesetzt)
    seite = bildschirm.seiteZu(aufstellungNachDerZonenwahl)
    davor = stellenAllerModelle(aufstellungNachDerZonenwahl)
    seiteDavor = inhaltDerSeite(seite)
    start = punktAufDerKarte(seite, stelleDesModells)

    anfragen = ziehenOhneAnfrage(seite, start, amKopfDerSeite(seite))

    assert anfragen == []
    assert stellenAllerModelle(aufstellungNachDerZonenwahl) == davor
    assert sperrmeldungenDerSeite(seite) == []
    assert inhaltDerSeite(seite) == seiteDavor
