import errno
import socket

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


def testEinAndererFehlerBeimBindenWirdWeitergegeben(aufstellung, monkeypatch):
    def verweigern(*_):
        raise OSError(errno.EACCES, "Zugriff verweigert")

    monkeypatch.setattr(socket, "create_server", verweigern)

    with pytest.raises(OSError) as fehler:
        serverStarten(aufstellung)

    assert fehler.value.errno == errno.EACCES


def testEinBelegterPortIstEineBelegteAdresse(server, aufstellung):
    with pytest.raises(AdresseBelegt) as fehler:
        serverStarten(aufstellung, server.port)

    assert fehler.value.adresse == adresseMitPort(server.port)
