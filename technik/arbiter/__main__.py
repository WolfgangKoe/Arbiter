"""Der Befehl `arbiter` (technik/architektur/web.md, W5)."""

import argparse
import sys
from collections.abc import Sequence

from arbiter.domaene.missionsvorbereitung.ausgangslage import Aufstellungszone
from arbiter.domaene.phasen.aufstellen import Aufstellung
from arbiter.katalog.ausgangslage import ausgangslageLaden
from arbiter.web.server import AdresseBelegt, serverStarten

festerPort = 8040
größterPort = 65535


def _portAngabe(text: str) -> int:
    port = int(text)
    if not 0 <= port <= größterPort:
        raise argparse.ArgumentTypeError(f"{port} liegt nicht zwischen 0 und {größterPort}")
    return port


def portDesBefehls(angaben: Sequence[str]) -> int:
    """Der Port nach `--port`, ohne Angabe der feste (QUE-8.1)."""
    parser = argparse.ArgumentParser(prog="arbiter")
    parser.add_argument("--port", type=_portAngabe, default=festerPort)
    return parser.parse_args(angaben).port


def aufstellungNachDemStart() -> Aufstellung:
    ausgangslage = ausgangslageLaden()
    aufstellung = Aufstellung(ausgangslage)
    aufstellung.gewinnerWählen(ausgangslage.ersterSpieler)
    aufstellung.aufstellungszoneWählen(Aufstellungszone.erste)
    return aufstellung


def starten() -> None:
    port = portDesBefehls(sys.argv[1:])
    try:
        server = serverStarten(aufstellungNachDemStart(), port)
    except AdresseBelegt as belegt:
        meldung = (
            f"Die Adresse {belegt.adresse} ist belegt. Läuft Arbiter schon? "
            "Dann spielt dort weiter oder beendet das andere Fenster mit Strg+C."
        )
        sys.exit(meldung)
    print(server.adresse, flush=True)
    try:
        server.warten()
    except KeyboardInterrupt:
        server.beenden()


if __name__ == "__main__":
    starten()
