from http import HTTPStatus

import pytest

from arbiter.domaene.missionsvorbereitung.ausgangslage import Aufstellungszone
from arbiter.web.anwendung import anwendungFür
from tests.akzeptanz.handgriffe import alleEinheitenAufstellen, aufstellungVon, spielerMit

pfadDerAuswahl = "/api/spieler/{}/einheiten/{}/ausgewählt"


@pytest.fixture
def aufstellung():
    return aufstellungVon(spielerMit(1, 1), spielerMit(1, 1))


@pytest.mark.parametrize(("spielernummer", "einheitennummer"), [(0, 1), (3, 1), (1, 0), (1, 3)])
@pytest.mark.parametrize("methode", ["put", "delete"])
def testEinPfadOhneEinheitInDerAblageIstNichtGefunden(
    aufstellung, spielernummer, einheitennummer, methode
):
    dienst = anwendungFür(aufstellung).test_client()

    antwort = getattr(dienst, methode)(pfadDerAuswahl.format(spielernummer, einheitennummer))

    assert antwort.status_code == HTTPStatus.NOT_FOUND


def testEineAufgestellteEinheitIstNichtMehrInDerAblageUndNichtGefunden(aufstellung):
    aufstellung.gewinnerWählen(aufstellung.ausgangslage.ersterSpieler)
    aufstellung.aufstellungszoneWählen(Aufstellungszone.erste)
    alleEinheitenAufstellen(aufstellung)
    dienst = anwendungFür(aufstellung).test_client()

    antwort = dienst.put(pfadDerAuswahl.format(1, 1))

    assert antwort.status_code == HTTPStatus.NOT_FOUND


pfadDesModells = "/api/spieler/{}/einheiten/{}/modelle/{}/stelle"
eineStelle = {"x": 3, "y": 20}


@pytest.mark.parametrize(
    ("spielernummer", "einheitennummer", "modellnummer"), [(3, 1, 1), (1, 3, 1), (1, 1, 3)]
)
@pytest.mark.parametrize("methode", ["put", "delete"])
def testEinModellOhneKennungIstNichtGefunden(
    aufstellung, spielernummer, einheitennummer, modellnummer, methode
):
    dienst = anwendungFür(aufstellung).test_client()
    pfad = pfadDesModells.format(spielernummer, einheitennummer, modellnummer)

    antwort = getattr(dienst, methode)(pfad, json=eineStelle)

    assert antwort.status_code == HTTPStatus.NOT_FOUND


@pytest.mark.parametrize("körper", [None, {}, {"x": 3}, {"x": "3", "y": 2}, {"x": True, "y": 2}])
def testEinModellOhneZahlenFürXUndYIstEineFehlerhafteAnfrage(aufstellung, körper):
    dienst = anwendungFür(aufstellung).test_client()

    antwort = dienst.put(pfadDesModells.format(1, 1, 1), json=körper)

    assert antwort.status_code == HTTPStatus.BAD_REQUEST


@pytest.mark.parametrize("zahl", ["NaN", "Infinity", "-Infinity"])
def testEineStelleMitUnendlicherOderUnbestimmterZahlIstEineFehlerhafteAnfrage(aufstellung, zahl):
    dienst = anwendungFür(aufstellung).test_client()

    antwort = dienst.put(
        "/api/karteAnklicken", data=f'{{"x": {zahl}, "y": 2}}', content_type="application/json"
    )

    assert antwort.status_code == HTTPStatus.BAD_REQUEST


def testEineSehrGroßeGanzeZahlIstEineFehlerhafteAnfrageUndLässtDenSpielstandLesbar(aufstellung):
    aufstellung.gewinnerWählen(aufstellung.ausgangslage.ersterSpieler)
    aufstellung.aufstellungszoneWählen(Aufstellungszone.erste)
    dienst = anwendungFür(aufstellung).test_client()
    dienst.put(pfadDerAuswahl.format(2, 1))
    groß = "1" + "0" * 400

    antwort = dienst.put(
        pfadDesModells.format(2, 1, 1),
        data=f'{{"x": 3, "y": {groß}}}',
        content_type="application/json",
    )

    assert antwort.status_code == HTTPStatus.BAD_REQUEST
    assert dienst.get("/api/spielstand").status_code == HTTPStatus.OK


def testEinModellOhneAblageZumZurücklegenIstEineFehlerhafteAnfrage(aufstellung):
    dienst = anwendungFür(aufstellung).test_client()

    antwort = dienst.delete(pfadDesModells.format(1, 1, 1))

    assert antwort.status_code == HTTPStatus.BAD_REQUEST


def testEinModellAufDieAblageEinesUnbekanntenSpielersIstNichtGefunden(aufstellung):
    dienst = anwendungFür(aufstellung).test_client()

    antwort = dienst.delete(pfadDesModells.format(1, 1, 1) + "?ablage=3")

    assert antwort.status_code == HTTPStatus.NOT_FOUND


def testEinKlickAufDieKarteOhneZahlenFürXUndYIstEineFehlerhafteAnfrage(aufstellung):
    dienst = anwendungFür(aufstellung).test_client()

    antwort = dienst.put("/api/karteAnklicken", json={"y": 2})

    assert antwort.status_code == HTTPStatus.BAD_REQUEST


def testEinFremderHostBekommtBadRequest(aufstellung):
    dienst = anwendungFür(aufstellung).test_client()

    antwort = dienst.get("/api/spielstand", headers={"Host": "fremd.example"})

    assert antwort.status_code == HTTPStatus.BAD_REQUEST
