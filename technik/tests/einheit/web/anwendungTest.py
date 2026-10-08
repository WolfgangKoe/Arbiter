from http import HTTPStatus

import pytest

from arbiter.web.anwendung import anwendungFür
from tests.akzeptanz.handgriffe import alleEinheitenAufstellen, aufstellungVon, spielerMit

pfadDerAuswahl = "/api/spieler/{}/einheiten/{}/ausgewählt"


@pytest.fixture
def aufstellung():
    return aufstellungVon(spielerMit(1, 1), spielerMit(1, 1))


@pytest.mark.parametrize(("spielernummer", "einheitennummer"), [(0, 1), (3, 1), (1, 0), (1, 3)])
@pytest.mark.parametrize("methode", ["put", "delete"])
def testEinePfadOhneEinheitInDerAblageIstNichtGefunden(
    aufstellung, spielernummer, einheitennummer, methode
):
    dienst = anwendungFür(aufstellung).test_client()

    antwort = getattr(dienst, methode)(pfadDerAuswahl.format(spielernummer, einheitennummer))

    assert antwort.status_code == HTTPStatus.NOT_FOUND


def testEineAufgestellteEinheitIstNichtMehrInDerAblageUndNichtGefunden(aufstellung):
    aufstellung.gewinnerWählen(aufstellung.ausgangslage.ersterSpieler)
    aufstellung.aufstellungszoneWählen(next(iter(aufstellung.ausgangslage.tiefen)))
    alleEinheitenAufstellen(aufstellung)
    dienst = anwendungFür(aufstellung).test_client()

    antwort = dienst.put(pfadDerAuswahl.format(1, 1))

    assert antwort.status_code == HTTPStatus.NOT_FOUND


def testEinFremderHostBekommtBadRequest(aufstellung):
    dienst = anwendungFür(aufstellung).test_client()

    antwort = dienst.get("/api/spielstand", headers={"Host": "fremd.example"})

    assert antwort.status_code == HTTPStatus.BAD_REQUEST
