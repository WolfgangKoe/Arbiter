"""Der Befehl `arbiter` (technik/architektur/web.md, W5)."""

from arbiter.domaene.phasen.aufstellen import Aufstellung
from arbiter.katalog.ausgangslage import ausgangslageLaden
from arbiter.web.server import serverStarten


def starten() -> None:
    server = serverStarten(Aufstellung(ausgangslageLaden()))
    print(server.adresse, flush=True)
    server.warten()


if __name__ == "__main__":
    starten()
