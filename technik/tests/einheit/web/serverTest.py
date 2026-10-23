import pytest

from arbiter.web.server import AdresseBelegt, adresseMitPort, serverStarten
from tests.akzeptanz.handgriffe import aufstellungVon, spielerMit


@pytest.fixture
def aufstellung():
    return aufstellungVon(spielerMit(1), spielerMit(1))


@pytest.fixture
def server(aufstellung):
    laufenderServer = serverStarten(aufstellung)
    yield laufenderServer
    laufenderServer.beenden()


def testDerServerLauschtAufDemFreienPortDesRechners(server):
    assert server.port > 0
    assert server.adresse == adresseMitPort(server.port)


def testEinBelegterPortIstEineBelegteAdresse(server, aufstellung):
    with pytest.raises(AdresseBelegt) as fehler:
        serverStarten(aufstellung, server.port)

    assert fehler.value.adresse == adresseMitPort(server.port)
