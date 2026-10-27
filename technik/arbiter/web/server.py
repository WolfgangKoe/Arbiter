"""Startet den Werkzeug-Server in einem eigenen Thread (web.md, W2)."""

import errno
import socket
from threading import Thread

from werkzeug.serving import make_server

from arbiter.domaene.phasen.aufstellen import Aufstellung
from arbiter.domaene.querschnitt.schlachtrunden import Schlacht
from arbiter.web.anwendung import anwendungFür

_gerät = "127.0.0.1"
_freierPort = 0


class AdresseBelegt(Exception):
    def __init__(self, adresse: str) -> None:
        super().__init__(adresse)
        self.adresse = adresse


def adresseMitPort(port: int) -> str:
    return f"http://{_gerät}:{port}/"


class Server:
    def __init__(self, aufstellung: Aufstellung, port: int, schlacht: Schlacht | None) -> None:
        anwendung = anwendungFür(aufstellung, schlacht)
        with _verbindungBinden(port) as verbindung:
            self._server = make_server(_gerät, port, anwendung, fd=verbindung.fileno())
        self._thread = Thread(target=self._server.serve_forever, daemon=True)

    @property
    def port(self) -> int:
        return self._server.port

    @property
    def adresse(self) -> str:
        return adresseMitPort(self.port)

    def starten(self) -> None:
        self._thread.start()

    def warten(self) -> None:
        self._thread.join()

    def beenden(self) -> None:
        self._server.shutdown()
        self._server.server_close()
        self._thread.join()


def serverStarten(
    aufstellung: Aufstellung, port: int = _freierPort, *, schlacht: Schlacht | None = None
) -> Server:
    server = Server(aufstellung, port, schlacht)
    server.starten()
    return server


def _verbindungBinden(port: int) -> socket.socket:
    """Bindet den Socket selbst, damit eine belegte Adresse als `AdresseBelegt` ankommt."""
    try:
        return socket.create_server((_gerät, port))
    except OSError as fehler:
        if fehler.errno == errno.EADDRINUSE:
            raise AdresseBelegt(adresseMitPort(port)) from fehler
        raise
