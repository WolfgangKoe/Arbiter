import os
import select
import subprocess
import sys
from pathlib import Path
from typing import NamedTuple

import pytest
from playwright.sync_api import Browser, sync_playwright

from arbiter.domaene.missionsvorbereitung.ausgangslage import Aufstellungszone, Ausgangslage
from arbiter.domaene.phasen.aufstellen import Aufstellung
from arbiter.domaene.querschnitt.schlachtrunden import Schlacht
from arbiter.domaene.spielobjekte import Einheit, Modell, Spieler, Stelle
from arbiter.katalog.ausgangslage import ausgangslageLaden
from tests.akzeptanz.anhalten import stelleAn
from tests.akzeptanz.bildschirm import Bildschirm
from tests.akzeptanz.dienst import dienstFür, dienstFürSchlacht, stellenDesVertrags
from tests.akzeptanz.grenzen import EinheitAmZug
from tests.akzeptanz.handgriffe import (
    Platz,
    abstandDerReihen,
    alleEinheitenAufstellen,
    aufstellungVon,
    einheitAufstellen,
    modelleAnStellenSetzen,
    modelleSetzen,
    radiusInZoll,
    spielerMit,
    tiefeDerErstenReihe,
    versetzt,
)
from tests.akzeptanz.schlacht import (
    ZugÜberDieBewegungsweite,
    zehnZollNachOsten,
    zehnZollNachWesten,
)

_technik = Path(__file__).parents[2]
_sekundenBisZurAdresse = 15
_freierPort = 0


class Ende(NamedTuple):
    ausgabe: str
    fehlerausgabe: str
    code: int


class Befehl:
    def __init__(self) -> None:
        self._prozesse: list[subprocess.Popen] = []

    def starten(self) -> str:
        prozess = self._prozessStarten(_freierPort, subprocess.DEVNULL)
        bereit, _, _ = select.select([prozess.stdout], [], [], _sekundenBisZurAdresse)
        return prozess.stdout.readline().strip() if bereit else ""

    def startenBisZumEnde(self, port: int) -> Ende:
        prozess = self._prozessStarten(port, subprocess.PIPE)
        try:
            ausgabe, fehlerausgabe = prozess.communicate(timeout=_sekundenBisZurAdresse)
        except subprocess.TimeoutExpired:
            prozess.terminate()
            ausgabe, fehlerausgabe = prozess.communicate()
        return Ende(ausgabe, fehlerausgabe, prozess.returncode)

    def _prozessStarten(self, port: int, fehlerausgabe: int) -> subprocess.Popen:
        umgebung = {name: wert for name, wert in os.environ.items() if name != "PYTHONUNBUFFERED"}
        umgebung["PYTHONPATH"] = str(_technik)
        prozess = subprocess.Popen(
            [sys.executable, "-m", "arbiter", "--port", str(port)],
            stdout=subprocess.PIPE,
            stderr=fehlerausgabe,
            text=True,
            env=umgebung,
        )
        self._prozesse.append(prozess)
        return prozess

    def beenden(self) -> None:
        for prozess in self._prozesse:
            prozess.terminate()
            prozess.wait(timeout=10)


@pytest.fixture
def befehl():
    befehl = Befehl()
    yield befehl
    befehl.beenden()


@pytest.fixture
def adresseDesBefehls(befehl: Befehl) -> str:
    return befehl.starten()


@pytest.fixture
def ausgangslage() -> Ausgangslage:
    return ausgangslageLaden()


@pytest.fixture
def ersterSpieler() -> Spieler:
    return spielerMit(2, 1)


@pytest.fixture
def zweiterSpieler() -> Spieler:
    return spielerMit(2, 1)


@pytest.fixture
def aufstellung(ersterSpieler: Spieler, zweiterSpieler: Spieler) -> Aufstellung:
    return aufstellungVon(ersterSpieler, zweiterSpieler)


@pytest.fixture(params=list(Aufstellungszone), ids=[zone.name for zone in Aufstellungszone])
def zone(request) -> Aufstellungszone:
    return request.param


@pytest.fixture
def platz(zone: Aufstellungszone) -> Platz:
    return Platz(zone)


@pytest.fixture
def ersteEinheitDesSpielersAnDerReihe(
    aufstellung: Aufstellung, ersterSpieler: Spieler, zweiterSpieler: Spieler, zone
) -> Einheit:
    andereZone = next(kandidat for kandidat in Aufstellungszone if kandidat is not zone)
    aufstellung.gewinnerWählen(zweiterSpieler)
    aufstellung.aufstellungszoneWählen(andereZone)
    ersteEinheit, _ = ersterSpieler.armee.einheiten
    return ersteEinheit


@pytest.fixture
def einheitNachDemAnderenSpieler(
    aufstellung: Aufstellung, ersterSpieler: Spieler, zweiterSpieler: Spieler, zone
) -> Einheit:
    andereZone = next(kandidat for kandidat in Aufstellungszone if kandidat is not zone)
    ersteEinheit, zweiteEinheit = ersterSpieler.armee.einheiten
    einheitDesAnderenSpielers, _ = zweiterSpieler.armee.einheiten
    aufstellung.gewinnerWählen(zweiterSpieler)
    aufstellung.aufstellungszoneWählen(andereZone)
    einheitAufstellen(aufstellung, ersteEinheit)
    einheitAufstellen(aufstellung, einheitDesAnderenSpielers)
    return zweiteEinheit


@pytest.fixture
def spielerEins(ausgangslage: Ausgangslage) -> Spieler:
    return ausgangslage.ersterSpieler


@pytest.fixture
def spielerZwei(ausgangslage: Ausgangslage) -> Spieler:
    return ausgangslage.zweiterSpieler


def _einheitMitDemNamen(spieler: Spieler, name: str) -> Einheit:
    (einheit,) = (einheit for einheit in spieler.armee.einheiten if einheit.name == name)
    return einheit


@pytest.fixture
def boyz(spielerEins: Spieler) -> Einheit:
    return _einheitMitDemNamen(spielerEins, "Boyz")


@pytest.fixture
def warboss(spielerEins: Spieler) -> Einheit:
    return _einheitMitDemNamen(spielerEins, "Warboss")


@pytest.fixture
def necronWarriors(spielerZwei: Spieler) -> Einheit:
    return _einheitMitDemNamen(spielerZwei, "Necron Warriors")


@pytest.fixture
def overlord(spielerZwei: Spieler) -> Einheit:
    return _einheitMitDemNamen(spielerZwei, "Overlord")


@pytest.fixture
def ausgangsaufstellung(ausgangslage: Ausgangslage) -> Aufstellung:
    return Aufstellung(ausgangslage)


@pytest.fixture
def aufstellungNachDerZonenwahl(
    ausgangsaufstellung: Aufstellung, spielerZwei: Spieler
) -> Aufstellung:
    ausgangsaufstellung.gewinnerWählen(spielerZwei)
    ausgangsaufstellung.aufstellungszoneWählen(Aufstellungszone.erste)
    return ausgangsaufstellung


@pytest.fixture
def aufstellungDesBeispiels(
    ausgangsaufstellung: Aufstellung, spielerEins: Spieler, necronWarriors: Einheit
) -> Aufstellung:
    ausgangsaufstellung.gewinnerWählen(spielerEins)
    ausgangsaufstellung.aufstellungszoneWählen(Aufstellungszone.erste)
    modelleAnStellenSetzen(ausgangsaufstellung, necronWarriors, stellenDesVertrags(2))
    return ausgangsaufstellung


@pytest.fixture
def aufstellungMitModellenBeiderSpieler(
    aufstellungNachDerZonenwahl: Aufstellung, boyz: Einheit, necronWarriors: Einheit
) -> Aufstellung:
    einheitAufstellen(aufstellungNachDerZonenwahl, boyz)
    einheitAufstellen(aufstellungNachDerZonenwahl, necronWarriors)
    return aufstellungNachDerZonenwahl


@pytest.fixture(scope="session")
def browser():
    with sync_playwright() as playwright:
        chromium = playwright.chromium.launch()
        yield chromium
        chromium.close()


@pytest.fixture
def bildschirm(browser: Browser):
    bildschirm = Bildschirm(browser)
    yield bildschirm
    bildschirm.beenden()


@pytest.fixture
def boyzSetzen(aufstellungNachDerZonenwahl, boyz):
    def setzen(anzahl: int) -> list[tuple[Modell, Stelle]]:
        return modelleSetzen(aufstellungNachDerZonenwahl, boyz, anzahl)

    return setzen


@pytest.fixture
def warriorsVorDemOverlord(
    aufstellungNachDerZonenwahl, boyz, overlord, warboss, necronWarriors
) -> tuple[list[tuple[Modell, Stelle]], Stelle]:
    for einheit in (boyz, overlord, warboss):
        einheitAufstellen(aufstellungNachDerZonenwahl, einheit)
    gesetzte = modelleSetzen(aufstellungNachDerZonenwahl, necronWarriors, 3)
    (gezogenes, _), *_ = gesetzte
    zielAmOverlord = stelleAn(
        aufstellungNachDerZonenwahl,
        (tiefeDerErstenReihe + abstandDerReihen, 2 * radiusInZoll(gezogenes)),
    )
    return gesetzte, zielAmOverlord


@pytest.fixture
def einGesetztesModell(aufstellungNachDerZonenwahl, boyzSetzen) -> tuple[Aufstellung, Modell]:
    [(modell, _)] = boyzSetzen(1)
    return aufstellungNachDerZonenwahl, modell


@pytest.fixture
def dienst(aufstellungNachDerZonenwahl: Aufstellung):
    return dienstFür(aufstellungNachDerZonenwahl)


@pytest.fixture
def dienstDesBeispiels(aufstellungDesBeispiels: Aufstellung):
    return dienstFür(aufstellungDesBeispiels)


@pytest.fixture
def beendeteAufstellung(ausgangsaufstellung: Aufstellung, spielerEins: Spieler) -> Aufstellung:
    ausgangsaufstellung.gewinnerWählen(spielerEins)
    ausgangsaufstellung.aufstellungszoneWählen(Aufstellungszone.erste)
    alleEinheitenAufstellen(ausgangsaufstellung)
    return ausgangsaufstellung


@pytest.fixture
def schlacht(beendeteAufstellung: Aufstellung) -> Schlacht:
    return Schlacht(beendeteAufstellung)


@pytest.fixture
def dienstNachDerAufstellung(beendeteAufstellung: Aufstellung):
    return dienstFür(beendeteAufstellung)


@pytest.fixture
def dienstDerSchlacht(beendeteAufstellung: Aufstellung, schlacht):
    return dienstFürSchlacht(beendeteAufstellung, schlacht)


@pytest.fixture
def schlachtNachDerWahlDesErstenZugs(schlacht, spielerEins: Spieler):
    schlacht.ersterZugWählen(spielerEins)
    return schlacht


@pytest.fixture
def schlachtInDerBewegungsphase(schlachtNachDerWahlDesErstenZugs):
    schlachtNachDerWahlDesErstenZugs.phaseBeenden()
    return schlachtNachDerWahlDesErstenZugs


@pytest.fixture
def schlachtInDerBewegungsphaseDesZweitenSpielers(schlacht, spielerZwei: Spieler):
    schlacht.ersterZugWählen(spielerZwei)
    schlacht.phaseBeenden()
    return schlacht


@pytest.fixture(params=["ersterSpieler", "zweiterSpieler"])
def spielerMitDemErstenZug(request, spielerEins: Spieler, spielerZwei: Spieler) -> Spieler:
    return {"ersterSpieler": spielerEins, "zweiterSpieler": spielerZwei}[request.param]


@pytest.fixture(params=["spielerEins", "spielerZwei"])
def zugÜberDieBewegungsweite(request, schlacht) -> ZugÜberDieBewegungsweite:
    einheitDesSpielers, weg = {
        "spielerEins": ("warboss", zehnZollNachOsten),
        "spielerZwei": ("overlord", zehnZollNachWesten),
    }[request.param]
    spieler = request.getfixturevalue(request.param)
    einheit = request.getfixturevalue(einheitDesSpielers)
    schlacht.ersterZugWählen(spieler)
    schlacht.phaseBeenden()
    (modell,) = einheit.modelle
    ziel = versetzt(schlacht.stelle(modell), weg)
    return ZugÜberDieBewegungsweite(schlacht, spieler, einheit, modell, ziel)


@pytest.fixture(params=["einheitDesSpielersAmZug", "einheitDesAnderenSpielers"])
def einheitJederSeite(request, boyz: Einheit, necronWarriors: Einheit) -> Einheit:
    return {"einheitDesSpielersAmZug": boyz, "einheitDesAnderenSpielers": necronWarriors}[
        request.param
    ]


@pytest.fixture(params=["spielerEins", "spielerZwei"])
def einheitAmZug(request, schlacht) -> EinheitAmZug:
    spieler, einheit, andereEinheit, andererSpieler = (
        request.getfixturevalue(name)
        for name in {
            "spielerEins": ("spielerEins", "boyz", "warboss", "spielerZwei"),
            "spielerZwei": ("spielerZwei", "necronWarriors", "overlord", "spielerEins"),
        }[request.param]
    )
    schlacht.ersterZugWählen(spieler)
    schlacht.phaseBeenden()
    return EinheitAmZug(schlacht, einheit, andereEinheit, andererSpieler)
