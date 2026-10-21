import re
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
faktZeile = "Reviewer: Review geschrieben"


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


def startseite(ordner) -> str:
    return antworten(ordner, "GET", "/", b"", kopf).inhalt.decode()


@pytest.mark.usefixtures("plan")
def testDieStartseiteZeigtJedeZeileMitHakenUndDasKommentarfeldNurInDetails(tmp_path):
    text = startseite(tmp_path)
    assert zeile in text and 'name="haken" value="x"' in text
    felder = text.count('name="kommentar"')
    assert felder > 0
    assert felder == len(re.findall(r"<details>(?:(?!</details>).)*name=\"kommentar\"", text))


@pytest.mark.usefixtures("plan")
def testDieReiterSindAnliegenUndTokenbericht(tmp_path):
    reiter = re.search(r'<nav class="reiter">(.*?)</nav>', startseite(tmp_path)).group(1)
    assert re.findall(r">([^<]+)</a>", reiter) == ["Anliegen", "Tokenbericht"]
    assert antworten(tmp_path, "GET", "/fortschritt", b"", kopf).status == HTTPStatus.NOT_FOUND


@pytest.mark.usefixtures("plan")
def testDerHakenGiltMitDemKlickOhneKnopf(tmp_path):
    text = startseite(tmp_path)
    assert 'onchange="this.form.submit()"' in text
    assert "Abschicken" not in text


def testEinGesetzterHakenIstGesperrtUndEinKommentarEntferntIhnNicht(tmp_path, plan):
    senden(tmp_path, f"zeile={quote(zeile)}&haken=x")
    seite = startseite(tmp_path)
    assert '<span class="haken" role="img" aria-label="abgehakt">✓</span>' in seite
    assert 'type="checkbox"' not in seite.split(f"<summary>{zeile}")[0].rsplit("<li>", 1)[-1]
    senden(tmp_path, f"zeile={quote(zeile)}&haken=&kommentar={quote('Noch eins.')}")
    assert f"- [x] {zeile}\n" in plan.read_text(encoding="utf-8")


def testEineZeileMitNochFehlendemFaktIstGesperrtUndDerServerSetztSieNicht(tmp_path, plan):
    vorher = plan.read_text(encoding="utf-8")
    seite = startseite(tmp_path)
    vorDerZeile = seite.split(f"<summary>{faktZeile}")[0].rsplit("<li>", 1)[-1]
    assert 'name="haken" value="x" disabled' in vorDerZeile
    senden(tmp_path, f"zeile={quote(faktZeile)}&haken=x")
    assert plan.read_text(encoding="utf-8") == vorher


def testEinHindernisStehtUnterDerZeileMitLinkAufDasAnliegen(tmp_path, plan):
    text = plan.read_text(encoding="utf-8").replace(
        f"- [ ] {zeile}\n", f"- [ ] {zeile}\n  Hindernis: Fehlt <b> (Anliegen 77)\n"
    )
    plan.write_text(text, encoding="utf-8")
    seite = startseite(tmp_path)
    assert '<a href="/anliegen/77">Anliegen 77</a>' in seite
    assert "Fehlt &lt;b&gt;" in seite


def testDerHakenAusDemDashboardStehtSofortImPlan(tmp_path, plan):
    antwort = senden(tmp_path, f"zeile={quote(zeile)}&haken=&haken=x&kommentar=")
    assert antwort.status == HTTPStatus.SEE_OTHER and antwort.ort == "/"
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
