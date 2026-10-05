"""Startet den Werkzeug-Server in einem eigenen Thread (web.md, W2)."""

from threading import Thread

from werkzeug.serving import make_server

from arbiter.domaene.phasen.aufstellen import Aufstellung
from arbiter.web.anwendung import anwendungFür

_gerät = "127.0.0.1"
_freierPort = 0


class Server:
    def __init__(self, aufstellung: Aufstellung) -> None:
        self._server = make_server(_gerät, _freierPort, anwendungFür(aufstellung))
        self._thread = Thread(target=self._server.serve_forever, daemon=True)
        self.adresse = f"http://{_gerät}:{self._server.port}/"

    def starten(self) -> None:
        self._thread.start()

    def warten(self) -> None:
        self._thread.join()

    def beenden(self) -> None:
        self._server.shutdown()
        self._server.server_close()
        self._thread.join()


def serverStarten(aufstellung: Aufstellung) -> Server:
    server = Server(aufstellung)
    server.starten()
    return server
