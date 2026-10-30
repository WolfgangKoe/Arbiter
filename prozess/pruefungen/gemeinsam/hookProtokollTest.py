import io
import json
import subprocess
import sys
from pathlib import Path

from gemeinsam import hookProtokoll

lauf = Path(__file__).with_name("lauf.py")


def testEineLeereEingabeIstEineEingabeOhneAngaben(monkeypatch):
    monkeypatch.setattr("sys.stdin", io.StringIO(""))
    assert hookProtokoll.eingabeLesen() == {}


def testEinHookOhneEingabeBrichtNichtMitJsonFehlerAb():
    ergebnis = subprocess.run(
        [sys.executable, str(lauf), "anliegenregeln.anliegenLaenge"],
        input="",
        capture_output=True,
        text=True,
        check=False,
    )
    assert ergebnis.returncode == 0, ergebnis.stderr


def testDieEingabeKommtAlsJsonVonStdin(monkeypatch):
    monkeypatch.setattr("sys.stdin", io.StringIO('{"tool_name": "Write"}'))
    assert hookProtokoll.eingabeLesen() == {"tool_name": "Write"}


def testEineAntwortWirdAlsJsonAusgegeben(capsys):
    hookProtokoll.antwortAusgeben({"a": "ä"})
    assert json.loads(capsys.readouterr().out) == {"a": "ä"}


def testKeineAntwortGibtNichtsAus(capsys):
    hookProtokoll.antwortAusgeben(None)
    assert capsys.readouterr().out == ""
