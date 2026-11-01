import json
import os
from pathlib import Path

import pytest

umgebungsvariable = "ARBITER_FRONTENDMESSUNG"
_sitzungen: dict = {}


def _seiteStarten(seite) -> None:
    sitzung = seite.context.new_cdp_session(seite)
    sitzung.send("Profiler.enable")
    sitzung.send("Profiler.startPreciseCoverage", {"callCount": True, "detailed": True})
    _sitzungen[seite] = sitzung


def _seiteAbholen(seite, ziel: Path) -> None:
    sitzung = _sitzungen.pop(seite, None)
    if sitzung is None or seite.is_closed():
        return
    ergebnis = sitzung.send("Profiler.takePreciseCoverage")["result"]
    with ziel.open("a", encoding="utf-8") as datei:
        datei.write(json.dumps(ergebnis) + "\n")


@pytest.fixture(autouse=True, scope="session")
def frontendMessen():
    ziel = os.environ.get(umgebungsvariable)
    if not ziel:
        yield
        return
    from playwright.sync_api import BrowserContext  # noqa: PLC0415

    neueSeite = BrowserContext.new_page
    schließen = BrowserContext.close

    def seiteMitMessung(kontext, *argumente, **schlüssel):
        seite = neueSeite(kontext, *argumente, **schlüssel)
        _seiteStarten(seite)
        return seite

    def schließenMitAbholen(kontext, *argumente, **schlüssel):
        for seite in kontext.pages:
            _seiteAbholen(seite, Path(ziel))
        return schließen(kontext, *argumente, **schlüssel)

    BrowserContext.new_page = seiteMitMessung
    BrowserContext.close = schließenMitAbholen
    yield
    BrowserContext.new_page = neueSeite
    BrowserContext.close = schließen
