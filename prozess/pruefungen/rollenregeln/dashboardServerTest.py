import os
import sys
import threading
import urllib.request
from http import HTTPStatus
from pathlib import Path

import pytest

from rollenregeln.dashboardAnliegenSeiten import stand
from rollenregeln.dashboardServer import Wächter, antworten, quellenStand, serverErzeugen
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


def testFormularLegtDieZügeSofortInsAnliegen(ordner):
    anlegen(ordner)
    antwort = senden(
        ordner, "/anliegen/10", "status=angenommen&antwort_F1=B&kommentar=Hallo&runde="
    )
    assert antwort.status == HTTPStatus.SEE_OTHER and antwort.ort == "/anliegen/10"
    text = (ordner / "handoff" / "anliegen" / "10-titel.md").read_text(encoding="utf-8")
    assert "Runde 1/3 · angenommen" in text and "Antwort: B" in text
    assert text.endswith("Kommentar: Hallo\n")
    assert vorgemerkte(ordner) == []


def testNachDemAbsendenStehtNichtsMehrAlsVorgemerktUndKeinFormularBietetDieAntwortNoch(ordner):
    anlegen(ordner)
    senden(ordner, "/anliegen/10", "status=angenommen&antwort_F1=B")
    assert "vorgemerkt ·" not in holen(ordner, "/").inhalt.decode()
    assert 'name="antwort_F1"' not in holen(ordner, "/anliegen/10").inhalt.decode()


def testWerBeiEinerRückfrageDranIstBekommtAntwortfelderUndDasDashboardNenntDieZügeInKlartext(
    ordner,
):
    anlegen(ordner, richtung=("Stakeholder", "organisationsentwickler"), status="rückfrage")
    assert 'name="antwort_F1"' in holen(ordner, "/anliegen/10").inhalt.decode()
    verworfenVermerken(ordner, Verworfen(Zug(10, "antwort", "A", "F1"), "Passt nicht mehr."))
    text = holen(ordner, "/").inhalt.decode()
    assert "Anliegen 10 · Antwort auf F1: A" in text and "antwort F1" not in text


def testGeänderterCodeFälltAufDamitDerServerSichNeuStartenKann(ordner):
    skript = ordner / "prozess" / "pruefungen" / "rollenregeln" / "probe.py"
    skript.parent.mkdir(parents=True)
    skript.write_text("a = 1\n", encoding="utf-8")
    vorher = quellenStand(ordner)
    assert quellenStand(ordner) == vorher
    skript.write_text("a = 2\n", encoding="utf-8")
    os.utime(skript, ns=(1, 1))
    assert quellenStand(ordner) != vorher


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


def ändern(skript: Path, inhalt: str, zeit: int) -> None:
    skript.write_text(inhalt, encoding="utf-8")
    os.utime(skript, ns=(zeit, zeit))


def testDerServerStürztNichtMitEinemFehlerhaftenPrüfskriptUndLäuftNachDerBesserungWieder(ordner):
    skript = ordner / "prozess" / "pruefungen" / "rollenregeln" / "probe.py"
    skript.parent.mkdir(parents=True)
    ändern(skript, "import time\ntime.sleep(60)\n", 1)
    wächter = Wächter([sys.executable, str(skript)], ordner)
    try:
        wächter.schritt()
        erstes = wächter.kind
        wächter.schritt()
        assert wächter.kind is erstes and wächter.läuft()
        ändern(skript, "def (:\n", 2)
        wächter.schritt()
        assert wächter.kind.wait(timeout=10) != 0
        wächter.schritt()
        assert not wächter.läuft()
        ändern(skript, "import time\ntime.sleep(60)\n", 3)
        wächter.schritt()
        assert wächter.läuft()
    finally:
        wächter.beenden()


def testEinVerschwundenesPrüfskriptBringtDenStandNichtZumAbsturz(ordner):
    skript = ordner / "prozess" / "pruefungen" / "probe.py"
    skript.parent.mkdir(parents=True)
    skript.write_text("a = 1\n", encoding="utf-8")
    (skript.parent / "weg.py").symlink_to(ordner / "nichtDa.py")
    assert quellenStand(ordner) == ((str(skript), skript.stat().st_mtime_ns),)
