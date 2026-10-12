"""AUF-16 · Loslassen ohne Ziel."""

from http import HTTPStatus

import pytest

from arbiter.domaene.sperre import Grund
from tests.akzeptanz.bildschirm import (
    ablageVon,
    amKopfDerSeite,
    aufDieHandlungWarten,
    einheitenKarteVon,
    gründeAlsText,
    inhaltDerSeite,
    knopfDerSeite,
    mitDerMausZiehen,
    mitteVon,
    punktAufDerKarte,
    sperrmeldungenDerSeite,
    sperrmeldungWarten,
    ziehenOhneAnfrage,
)
from tests.akzeptanz.dienst import einheitAufAblageLoslassen, spielstandVon
from tests.akzeptanz.handgriffe import (
    einheitAufstellen,
    modelleSetzen,
    nachDerWahlDerAufstellungszone,
    sperrgründe,
    stelleInDerZoneVon,
    stellenAllerModelle,
    stellenDerEinheit,
)


@pytest.mark.parametrize("einheitenwahl", ["inAufstellung", "aufgestellt", "desAnderenSpielers"])
def testAuf16_1EineEinheitMitAllenGesetztenModellenStehtNachDemLoslassenWieDavor(
    aufstellungNachDerZonenwahl, boyz, necronWarriors, spielerEins, einheitenwahl
):
    modelleSetzen(aufstellungNachDerZonenwahl, boyz, len(boyz.modelle))
    if einheitenwahl == "aufgestellt":
        aufstellungNachDerZonenwahl.aufstellenDerEinheitBeenden()
    if einheitenwahl == "desAnderenSpielers":
        aufstellungNachDerZonenwahl.aufstellenDerEinheitBeenden()
        einheitAufstellen(aufstellungNachDerZonenwahl, necronWarriors)
    einheit = necronWarriors if einheitenwahl == "desAnderenSpielers" else boyz
    davor = stellenAllerModelle(aufstellungNachDerZonenwahl)
    irgendwo = stelleInDerZoneVon(aufstellungNachDerZonenwahl, spielerEins, 8, 50)

    aufstellungNachDerZonenwahl.einheitLoslassen(einheit, irgendwo)

    assert stellenAllerModelle(aufstellungNachDerZonenwahl) == davor


@pytest.mark.parametrize("gezogenes", ["einheit", "modell"])
def testAuf16_2EineEinheitOderEinModellNebenKarteUndAblagenStehtNachDemLoslassenWieDavor(
    bildschirm, aufstellungNachDerZonenwahl, boyzSetzen, gezogenes
):
    (_, stelleDesModells), *_ = boyzSetzen(3)
    seite = bildschirm.seiteZu(aufstellungNachDerZonenwahl)
    davor = stellenAllerModelle(aufstellungNachDerZonenwahl)
    seiteDavor = inhaltDerSeite(seite)
    if gezogenes == "einheit":
        start = mitteVon(einheitenKarteVon(seite, "Spieler 1", "Boyz"))
    else:
        start = punktAufDerKarte(seite, stelleDesModells)

    anfragen = ziehenOhneAnfrage(seite, start, amKopfDerSeite(seite))

    assert anfragen == []
    assert stellenAllerModelle(aufstellungNachDerZonenwahl) == davor
    assert sperrmeldungenDerSeite(seite) == []
    assert inhaltDerSeite(seite) == seiteDavor


def testAuf16_3EinGesetztesModellAufDerAblageDesAnderenSpielersIstNichtWählbar(
    aufstellung, ersterSpieler, zweiterSpieler
):
    nachDerWahlDerAufstellungszone(aufstellung, gewinner=ersterSpieler)
    einheit, _ = zweiterSpieler.armee.einheiten
    (modell, stelle), _ = stellenDerEinheit(aufstellung, zweiterSpieler, einheit)
    aufstellung.modellSetzen(modell, stelle)

    gründe = sperrgründe(aufstellung.modellZurücklegen, modell, ersterSpieler)

    assert gründe == {Grund.nichtWählbar}
    assert aufstellung.stelle(modell) == stelle
    assert aufstellung.einheitInAufstellung is einheit


@pytest.mark.parametrize("gesetzt", [0, 3], ids=["keinModellGesetzt", "dreiModelleGesetzt"])
def testAuf16_4EineEinheitAufDerAblageIhresSpielersStehtNachDemLoslassenWieDavor(
    bildschirm, aufstellungNachDerZonenwahl, boyzSetzen, gesetzt
):
    boyzSetzen(gesetzt)
    seite = bildschirm.seiteZu(aufstellungNachDerZonenwahl)
    davor = stellenAllerModelle(aufstellungNachDerZonenwahl)
    einheitInAufstellungDavor = aufstellungNachDerZonenwahl.einheitInAufstellung
    start = mitteVon(einheitenKarteVon(seite, "Spieler 1", "Boyz"))
    ziel = mitteVon(ablageVon(seite, "Spieler 1").locator(".armeeKartenName"))

    ziehenOhneAnfrage(seite, start, ziel)

    assert stellenAllerModelle(aufstellungNachDerZonenwahl) == davor
    assert aufstellungNachDerZonenwahl.einheitInAufstellung is einheitInAufstellungDavor
    assert sperrmeldungenDerSeite(seite) == []


@pytest.mark.parametrize("gesetzt", [0, 3], ids=["keinModellGesetzt", "dreiModelleGesetzt"])
def testAuf16_5EineEinheitAufDerAblageDesAnderenSpielersIstNichtWählbar(
    aufstellungNachDerZonenwahl, boyz, boyzSetzen, spielerZwei, gesetzt
):
    boyzSetzen(gesetzt)
    davor = stellenAllerModelle(aufstellungNachDerZonenwahl)
    einheitInAufstellungDavor = aufstellungNachDerZonenwahl.einheitInAufstellung

    gründe = sperrgründe(aufstellungNachDerZonenwahl.einheitAufAblageLoslassen, boyz, spielerZwei)

    assert gründe == {Grund.nichtWählbar}
    assert stellenAllerModelle(aufstellungNachDerZonenwahl) == davor
    assert aufstellungNachDerZonenwahl.einheitInAufstellung is einheitInAufstellungDavor


def testAuf16_5EineEinheitAufDerAblageDesSpielersAnDerReiheIstNichtWählbar(
    aufstellungNachDerZonenwahl, necronWarriors, spielerEins
):
    davor = stellenAllerModelle(aufstellungNachDerZonenwahl)
    einheitInAufstellungDavor = aufstellungNachDerZonenwahl.einheitInAufstellung

    gründe = sperrgründe(
        aufstellungNachDerZonenwahl.einheitAufAblageLoslassen, necronWarriors, spielerEins
    )

    assert gründe == {Grund.nichtWählbar}
    assert stellenAllerModelle(aufstellungNachDerZonenwahl) == davor
    assert aufstellungNachDerZonenwahl.einheitInAufstellung is einheitInAufstellungDavor


@pytest.mark.parametrize(
    ("einheitenname", "spielernummer"),
    [("boyz", 2), ("necronWarriors", 1)],
    ids=["boyzAufAblageVonSpielerZwei", "necronWarriorsAufAblageVonSpielerEins"],
)
def testAuf16_5DerDienstSperrtEineEinheitAufDerAblageDesAnderenSpielersMitNichtWählbar(
    dienst, aufstellungNachDerZonenwahl, request, einheitenname, spielernummer
):
    einheit = request.getfixturevalue(einheitenname)
    davor = spielstandVon(dienst)

    antwort = einheitAufAblageLoslassen(dienst, aufstellungNachDerZonenwahl, einheit, spielernummer)

    assert antwort.status_code == HTTPStatus.CONFLICT
    assert antwort.get_json() == {"gründe": [Grund.nichtWählbar.value], "spielstand": davor}


def testAuf16_5DieSeiteNenntBeiEinerEinheitAufDerAblageDesAnderenSpielersDenGrund(
    bildschirm, aufstellungNachDerZonenwahl
):
    seite = bildschirm.seiteZu(aufstellungNachDerZonenwahl)
    davor = stellenAllerModelle(aufstellungNachDerZonenwahl)
    start = mitteVon(einheitenKarteVon(seite, "Spieler 1", "Boyz"))
    ziel = mitteVon(ablageVon(seite, "Spieler 2").locator(".armeeKartenName"))

    with aufDieHandlungWarten(seite) as antwort:
        mitDerMausZiehen(seite, start, ziel)
    genannt = sperrmeldungWarten(seite, {Grund.nichtWählbar})

    assert antwort.value.status == HTTPStatus.CONFLICT
    assert genannt == gründeAlsText({Grund.nichtWählbar})
    assert knopfDerSeite(seite, "gemeinsam übergehen").count() == 0
    assert stellenAllerModelle(aufstellungNachDerZonenwahl) == davor
