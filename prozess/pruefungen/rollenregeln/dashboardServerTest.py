import threading
import urllib.request
from http import HTTPStatus
from pathlib import Path

import pytest

from rollenregeln.dashboardAnliegenSeiten import stand
from rollenregeln.dashboardServer import antworten, serverErzeugen
from rollenregeln.eingang import Verworfen, Zug, verworfenVermerken, vorgemerkte

kopf = {"Origin": None, "Host": "127.0.0.1:8765"}
vorlage = """# Titel

{nummer} · Fragen · von {absender} → {empfänger} · Runde 1/3 · {status}

**F1 · Eins.** A oder B.
Antwort:
"""


@pytest.fixture
def ordner(tmp_path):
    (tmp_path / "handoff" / "anliegen").mkdir(parents=True)
    return tmp_path


def anlegen(ordner: Path, nummer=10, richtung=("planer", "Stakeholder"), status="offen"):
    absender, empfänger = richtung
    text = vorlage.format(nummer=nummer, absender=absender, empfänger=empfänger, status=status)
    (ordner / "handoff" / "anliegen" / f"{nummer}-titel.md").write_text(text, encoding="utf-8")


def holen(ordner, pfad):
    return antworten(ordner, "GET", pfad, b"", kopf)


def senden(ordner, pfad, körper, **zusatz):
    return antworten(ordner, "POST", pfad, körper.encode(), {**kopf, **zusatz})


def testAnliegenSeiteZähltWasDemStakeholderBleibtUndVerlinktDieEinzelseite(ordner):
    anlegen(ordner, nummer=10)
    anlegen(ordner, nummer=11, richtung=("Stakeholder", "planer"), status="angenommen")
    text = holen(ordner, "/").inhalt.decode()
    assert "Du bist dran: 2" in text
    assert '<a href="/anliegen/10">10</a>' in text


def testTokenberichtZeigtGelbenHinweisBisDerStatusGesetztIst(ordner):
    anlegen(ordner)
    assert 'class="offene-frage"' in holen(ordner, "/tokens").inhalt.decode()
    anlegen(ordner, status="angenommen")
    assert 'class="offene-frage"' not in holen(ordner, "/tokens").inhalt.decode()


def testEinzelseiteHatWegZurückFormularMitStatusAntwortfeldUndKommentar(ordner):
    anlegen(ordner)
    text = holen(ordner, "/anliegen/10").inhalt.decode()
    assert '<a href="/">‹ Dashboard</a>' in text
    assert '<option value="angenommen">' in text and 'name="antwort_F1"' in text
    assert 'name="kommentar"' in text


def testEinzelseiteBietetNurStatusAnDieDerAblaufZulässt(ordner):
    anlegen(ordner, richtung=("planer", "architekt"))
    text = holen(ordner, "/anliegen/10").inhalt.decode()
    assert 'name="status"' not in text and 'name="antwort_F1"' not in text
    assert 'name="kommentar"' in text


def testUnbekanntesAnliegenGibtNichtGefunden(ordner):
    assert holen(ordner, "/anliegen/99").status == HTTPStatus.NOT_FOUND


def testFormularMerktZügeVorUndSchreibtNichtInDieAnliegen(ordner):
    anlegen(ordner)
    vorher = (ordner / "handoff" / "anliegen" / "10-titel.md").read_bytes()
    antwort = senden(
        ordner, "/anliegen/10", "status=angenommen&antwort_F1=B&kommentar=Hallo&runde="
    )
    assert antwort.status == HTTPStatus.SEE_OTHER and antwort.ort == "/anliegen/10"
    assert vorgemerkte(ordner) == [
        Zug(10, "status", "angenommen"),
        Zug(10, "antwort", "B", "F1"),
        Zug(10, "kommentar", "Hallo"),
    ]
    assert (ordner / "handoff" / "anliegen" / "10-titel.md").read_bytes() == vorher
    assert "vorgemerkt" in holen(ordner, "/").inhalt.decode()


def testFormularVonEinerFremdenSeiteWirdAbgewiesen(ordner):
    anlegen(ordner)
    antwort = senden(ordner, "/anliegen/10", "status=angenommen", Origin="http://böse.example")
    assert antwort.status == HTTPStatus.FORBIDDEN and vorgemerkte(ordner) == []


def testVerworfenesStehtAufDerSeiteBisDerStakeholderEsGelesenHat(ordner):
    anlegen(ordner)
    verworfenVermerken(ordner, Verworfen(Zug(10, "status", "erledigt"), "Passt nicht mehr."))
    assert "Passt nicht mehr." in holen(ordner, "/").inhalt.decode()
    senden(ordner, "/verworfeneLeeren", "")
    assert "Passt nicht mehr." not in holen(ordner, "/").inhalt.decode()


def testTokenberichtTrägtDenReiterZurAnliegenSeite(ordner):
    text = holen(ordner, "/tokens").inhalt.decode()
    assert '<a href="/">Anliegen</a>' in text and 'aria-current="page">Tokenbericht' in text


def testStandÄndertSichMitJederDateiInHandoff(ordner):
    anlegen(ordner)
    vorher = stand(ordner)
    (ordner / "handoff" / "plan.md").write_text("neu", encoding="utf-8")
    assert stand(ordner) != vorher


def testDerServerAntwortetAufEinerEchtenVerbindung(ordner):
    anlegen(ordner)
    server = serverErzeugen(ordner, 0)
    threading.Thread(target=server.handle_request, daemon=True).start()
    port = server.server_address[1]
    with urllib.request.urlopen(f"http://127.0.0.1:{port}/", timeout=5) as antwort:
        assert "Du bist dran: 1" in antwort.read().decode()
    server.server_close()
