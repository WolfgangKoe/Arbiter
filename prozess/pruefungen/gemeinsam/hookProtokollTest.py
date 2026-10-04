import io
import json

from gemeinsam import hookProtokoll


def testDieEingabeKommtAlsJsonVonStdin(monkeypatch):
    monkeypatch.setattr("sys.stdin", io.StringIO('{"tool_name": "Write"}'))
    assert hookProtokoll.eingabeLesen() == {"tool_name": "Write"}


def testEineAntwortWirdAlsJsonAusgegeben(capsys):
    hookProtokoll.antwortAusgeben({"a": "ä"})
    assert json.loads(capsys.readouterr().out) == {"a": "ä"}


def testKeineAntwortGibtNichtsAus(capsys):
    hookProtokoll.antwortAusgeben(None)
    assert capsys.readouterr().out == ""
