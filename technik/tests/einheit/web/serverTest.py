import pytest

from arbiter.web.server import AdresseBelegt, adresseMitPort, serverStarten
from tests.akzeptanz.handgriffe import aufstellungVon, spielerMit


@pytest.fixture
def aufstellung():
    return aufstellungVon(spielerMit(1), spielerMit(1))


def testDieAdresseNenntDenPortDesServers(aufstellung):
    server = serverStarten(aufstellung)

    assert server.adresse.startswith("http://127.0.0.1:")
    assert server.adresse == adresseMitPort(int(server.adresse.split(":")[-1].rstrip("/")))
    server.beenden()


def testEinBelegterPortIstEineBelegteAdresse(aufstellung):
    ersterServer = serverStarten(aufstellung)
    belegterPort = int(ersterServer.adresse.split(":")[-1].rstrip("/"))

    with pytest.raises(AdresseBelegt) as fehler:
        serverStarten(aufstellung, belegterPort)

    assert fehler.value.adresse == adresseMitPort(belegterPort)
    ersterServer.beenden()
