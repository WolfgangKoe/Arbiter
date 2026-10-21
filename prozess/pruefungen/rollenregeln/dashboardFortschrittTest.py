from http import HTTPStatus
from pathlib import Path
from urllib.parse import quote

import pytest

from rollenregeln.dashboardServer import antworten
from rollenregeln.eingang import vorgemerkte
from standregeln.fortschritt import fortschrittSchreiben

kopf = {"Origin": None, "Host": "127.0.0.1:8765"}
planText = (
    "# Plan · Zyklus 1\n\n## Items\n1. [Stellen](../domaene/items/stellen.md)\n\n"
    "## Freigabe\nFreigabe: offen\nKommentar: .\n"
)
zeile = "Implementierer: Tests zu Item stellen grün"


def schreiben(wurzel: Path, pfad: str, text: str) -> Path:
    datei = wurzel / pfad
    datei.parent.mkdir(parents=True, exist_ok=True)
    datei.write_text(text, encoding="utf-8")
    return datei


@pytest.fixture
def plan(tmp_path, gitRepo):
    datei = schreiben(tmp_path, "handoff/plan.md", planText)
    schreiben(tmp_path, "domaene/items/stellen.md", "# Stellen\n")
    for rolle in ("implementierer", "planer"):
        schreiben(tmp_path, f".claude/agents/{rolle}.md", f"---\nname: {rolle}\n---\n")
    gitRepo.festhalten("Freigabe Plan 1")
    fortschrittSchreiben(tmp_path)
    return datei


def senden(ordner, körper: str):
    return antworten(ordner, "POST", "/fortschritt", körper.encode(), kopf)


@pytest.mark.usefixtures("plan")
def testDieSeiteFortschrittZeigtJedeZeileMitHakenUndKommentarfeld(tmp_path):
    text = antworten(tmp_path, "GET", "/fortschritt", b"", kopf).inhalt.decode()
    assert zeile in text and 'name="kommentar"' in text
    assert 'aria-current="page">Fortschritt' in text


def testDerHakenAusDemDashboardStehtSofortImPlan(tmp_path, plan):
    antwort = senden(tmp_path, f"zeile={quote(zeile)}&haken=&haken=x&kommentar=")
    assert antwort.status == HTTPStatus.SEE_OTHER and antwort.ort == "/fortschritt"
    assert f"- [x] {zeile}\n" in plan.read_text(encoding="utf-8")
    assert vorgemerkte(tmp_path) == []


def testEinKommentarAusDemDashboardWirdAnliegenUndZeile(tmp_path, plan):
    senden(tmp_path, f"zeile={quote(zeile)}&haken=&kommentar={quote('Bitte prüfen.')}")
    assert "  Kommentar: Bitte prüfen. (Anliegen 1)\n" in plan.read_text(encoding="utf-8")
    (datei,) = (tmp_path / "handoff/anliegen").glob("*.md")
    text = datei.read_text(encoding="utf-8")
    assert "Von: Stakeholder\nAn: Implementierer" in text


def testFormularVonEinerFremdenSeiteSetztKeinenHaken(tmp_path, plan):
    vorher = plan.read_text(encoding="utf-8")
    fremd = {**kopf, "Origin": "http://böse.example"}
    körper = f"zeile={quote(zeile)}&haken=x".encode()
    antwort = antworten(tmp_path, "POST", "/fortschritt", körper, fremd)
    assert antwort.status == HTTPStatus.FORBIDDEN
    assert plan.read_text(encoding="utf-8") == vorher
