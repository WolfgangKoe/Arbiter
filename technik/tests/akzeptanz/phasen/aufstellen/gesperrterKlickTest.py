"""AUF-19 · Gesperrter Klick."""

from dataclasses import dataclass
from http import HTTPStatus

import pytest

from arbiter.domaene.sperre import Grund
from arbiter.domaene.spielobjekte import Stelle
from tests.akzeptanz.auswahl import klickenUndWarten
from tests.akzeptanz.bildschirm import (
    aufDieHandlungWarten,
    gründeAlsText,
    knopfDerSeite,
    sperrmeldungWarten,
)
from tests.akzeptanz.dienst import spielfeldAnklicken, spielstandVon
from tests.akzeptanz.handgriffe import (
    modelleSetzen,
    sperrgründe,
    stelleInDerZoneVon,
    stellenAllerModelle,
)
from tests.akzeptanz.ziehen import mitDerMausKlicken, punktAufDemSpielfeld


@dataclass(frozen=True)
class Sperrfall:
    stelle: Stelle
    grund: Grund


@pytest.fixture(
    params=[
        (0, "necronWarriors", Grund.nichtWählbar),
        (1, "warboss", Grund.einheitBegonnen),
    ],
    ids=["einheitDesSpielersNichtAnDerReihe", "andereEinheitBeiBegonnener"],
)
def sperrfall(request, aufstellungNachDerZonenwahl, spielerEins, boyz) -> Sperrfall:
    gesetzteBoyz, ausgewählte, grund = request.param
    modelleSetzen(aufstellungNachDerZonenwahl, boyz, gesetzteBoyz)
    aufstellungNachDerZonenwahl.auswählen(request.getfixturevalue(ausgewählte))
    stelle = stelleInDerZoneVon(aufstellungNachDerZonenwahl, spielerEins, 4, 30)
    return Sperrfall(stelle, grund)


def testAuf19_4EinKlickAufDasSpielfeldSperrtWieDasLoslassenUndSetztKeinModell(
    aufstellungNachDerZonenwahl, sperrfall
):
    davor = stellenAllerModelle(aufstellungNachDerZonenwahl)

    gründe = sperrgründe(aufstellungNachDerZonenwahl.spielfeldAnklicken, sperrfall.stelle)

    assert gründe == {sperrfall.grund}
    assert stellenAllerModelle(aufstellungNachDerZonenwahl) == davor


def testAuf19_4DerDienstAntwortetAufDenKlickMitDemGrundUndDemStandWieDavor(dienst, sperrfall):
    davor = spielstandVon(dienst)

    antwort = spielfeldAnklicken(dienst, sperrfall.stelle)

    assert antwort.status_code == HTTPStatus.CONFLICT
    assert antwort.get_json()["gründe"] == [sperrfall.grund.value]
    assert antwort.get_json()["spielstand"] == davor


def testAuf19_4DieSeiteNenntNachDemKlickAufDasSpielfeldDenGrundUndBietetGemeinsamÜbergehenNichtAn(
    bildschirm, aufstellungNachDerZonenwahl, sperrfall
):
    davor = stellenAllerModelle(aufstellungNachDerZonenwahl)
    seite = bildschirm.seiteZu(aufstellungNachDerZonenwahl)

    with aufDieHandlungWarten(seite):
        mitDerMausKlicken(seite, punktAufDemSpielfeld(seite, sperrfall.stelle))

    genannt = sperrmeldungWarten(seite, {sperrfall.grund})
    assert genannt == gründeAlsText({sperrfall.grund})
    assert knopfDerSeite(seite, "gemeinsam übergehen").count() == 0
    assert stellenAllerModelle(aufstellungNachDerZonenwahl) == davor


def testAuf19_4DieSeiteNenntDenGrundNochNachDemAuswählen(
    bildschirm, aufstellungNachDerZonenwahl, spielerEins, necronWarriors
):
    aufstellungNachDerZonenwahl.auswählen(necronWarriors)
    stelle = stelleInDerZoneVon(aufstellungNachDerZonenwahl, spielerEins, 4, 30)
    seite = bildschirm.seiteZu(aufstellungNachDerZonenwahl)
    with aufDieHandlungWarten(seite):
        mitDerMausKlicken(seite, punktAufDemSpielfeld(seite, stelle))
    sperrmeldungWarten(seite, {Grund.nichtWählbar})

    klickenUndWarten(seite, "Spieler 1", "Boyz")

    assert sperrmeldungWarten(seite, {Grund.nichtWählbar}) == gründeAlsText({Grund.nichtWählbar})


def testAuf19_4DieSeiteNenntDenGrundNichtMehrNachDerNächstenHandlung(
    bildschirm, aufstellungNachDerZonenwahl, spielerEins, necronWarriors
):
    aufstellungNachDerZonenwahl.auswählen(necronWarriors)
    stelle = stelleInDerZoneVon(aufstellungNachDerZonenwahl, spielerEins, 4, 30)
    seite = bildschirm.seiteZu(aufstellungNachDerZonenwahl)
    with aufDieHandlungWarten(seite):
        mitDerMausKlicken(seite, punktAufDemSpielfeld(seite, stelle))
    sperrmeldungWarten(seite, {Grund.nichtWählbar})
    klickenUndWarten(seite, "Spieler 1", "Boyz")

    with aufDieHandlungWarten(seite):
        mitDerMausKlicken(seite, punktAufDemSpielfeld(seite, stelle))

    assert sperrmeldungWarten(seite, set()) == frozenset()
