"""Der Befehl `arbiter` (technik/architektur/web.md, W5)."""

from arbiter.domaene.phasen.aufstellen import Aufstellung, Aufstellungszone
from arbiter.katalog.ausgangslage import ausgangslageLaden
from arbiter.web.server import serverStarten


def aufstellungNachDemStart() -> Aufstellung:
    # Regel: AUF-6.1, vorläufig: Spieler 1 ist Gewinner und hat die erste Zone gewählt
    ausgangslage = ausgangslageLaden()
    aufstellung = Aufstellung(ausgangslage)
    aufstellung.gewinnerWählen(ausgangslage.ersterSpieler)
    aufstellung.aufstellungszoneWählen(Aufstellungszone.erste)
    return aufstellung


def starten() -> None:
    server = serverStarten(aufstellungNachDemStart())
    print(server.adresse, flush=True)
    try:
        server.warten()
    except KeyboardInterrupt:
        # Warum: Strg+C beendet den Befehl ohne Traceback
        server.beenden()


if __name__ == "__main__":
    starten()
