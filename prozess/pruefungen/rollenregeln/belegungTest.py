import json

import pytest

from rollenregeln.belegung import (
    belegungAusTranskript,
    eigenesTranskript,
    entscheide,
    freigabedatei,
)

nutzung = {
    "input_tokens": 5,
    "cache_creation_input_tokens": 1_000,
    "cache_read_input_tokens": 99_000,
}
summeDerNutzung = 100_005
jüngsteBelegung = 80_000


def transkript(ordner, name, *belegungen):
    datei = ordner / name
    zeilen = [
        json.dumps({"message": {"usage": {"cache_read_input_tokens": belegung}}})
        for belegung in belegungen
    ]
    datei.write_text("\n".join(zeilen) + "\n", encoding="utf-8")
    return datei


def werkzeug(ereignis, datei, *, rolle="planer", agentId="a1", werkzeugname="Bash"):
    eingabe = {
        "hook_event_name": ereignis,
        "agent_type": rolle,
        "tool_name": werkzeugname,
        "transcript_path": str(datei),
        "agent_transcript_path": str(datei),
    }
    if agentId:
        eingabe["agent_id"] = agentId
    return eingabe


@pytest.fixture
def wurzel(tmp_path):
    (tmp_path / ".git").mkdir()
    return tmp_path


def testBelegungIstEingabeUndCacheOhneAusgabe(tmp_path):
    datei = tmp_path / "lauf.jsonl"
    datei.write_text(json.dumps({"message": {"usage": {**nutzung, "output_tokens": 7}}}) + "\n")
    assert belegungAusTranskript(datei) == summeDerNutzung


def testGemessenWirdDieJüngsteBrauchbareAnfrage(tmp_path):
    datei = transkript(tmp_path, "lauf.jsonl", 10_000, 80_000)
    with datei.open("a", encoding="utf-8") as ziel:
        fehler = {"isApiErrorMessage": True, "message": {"usage": {"input_tokens": 1}}}
        ziel.write(json.dumps(fehler) + "\n")
        ziel.write("kein json\n")
    assert belegungAusTranskript(datei) == jüngsteBelegung


def testFehlendesTranskriptHatKeineBelegung(tmp_path):
    assert belegungAusTranskript(tmp_path / "gibtEsNicht.jsonl") is None


def testRollenMessenIhrEigenesTranskriptNichtDasDesKoordinators(tmp_path):
    sitzung = tmp_path / "sitzung1"
    (sitzung / "subagents").mkdir(parents=True)
    eigenes = transkript(sitzung / "subagents", "agent-a1.jsonl", 42)
    eingabe = {
        "agent_id": "a1",
        "session_id": "sitzung1",
        "transcript_path": str(tmp_path / "sitzung1.jsonl"),
    }
    assert eigenesTranskript(eingabe) == eigenes


def testUnterDerWarnschwelleKommtKeineMeldung(wurzel):
    datei = transkript(wurzel, "lauf.jsonl", 119_999)
    assert entscheide(werkzeug("PostToolUse", datei), wurzel) is None


def testAbDerWarnschwelleKommtEineMeldungEinmalJeLauf(wurzel):
    datei = transkript(wurzel, "lauf.jsonl", 120_000)
    antwort = entscheide(werkzeug("PostToolUse", datei), wurzel)
    text = antwort["hookSpecificOutput"]["additionalContext"]
    assert "120.000 Token" in text
    assert "nichts Neues" in text
    assert entscheide(werkzeug("PostToolUse", datei), wurzel) is None


def testDerKoordinatorBekommtDieEmpfehlungFürEinenNeuenChat(wurzel):
    datei = transkript(wurzel, "lauf.jsonl", 130_000)
    antwort = entscheide(werkzeug("PostToolUse", datei, rolle="koordinator", agentId=None), wurzel)
    assert "neuen Chat" in antwort["hookSpecificOutput"]["additionalContext"]


def testUnterDerSperrschwelleLäuftJedesWerkzeug(wurzel):
    datei = transkript(wurzel, "lauf.jsonl", 149_999)
    assert entscheide(werkzeug("PreToolUse", datei), wurzel) is None


def testAbDerSperrschwelleSperrtAllesAußerSchreibenUndSchlussantwort(wurzel):
    datei = transkript(wurzel, "lauf.jsonl", 150_000)
    sperre = entscheide(werkzeug("PreToolUse", datei), wurzel)
    assert sperre["hookSpecificOutput"]["permissionDecision"] == "deny"
    for erlaubt in ("Write", "Edit", "SubagentHandback"):
        assert entscheide(werkzeug("PreToolUse", datei, werkzeugname=erlaubt), wurzel) is None


def testBeimKoordinatorEntscheidetDerStakeholder(wurzel):
    datei = transkript(wurzel, "lauf.jsonl", 150_000)
    eingabe = werkzeug("PreToolUse", datei, rolle="koordinator", agentId=None)
    grund = entscheide(eingabe, wurzel)["hookSpecificOutput"]["permissionDecisionReason"]
    assert "Stakeholder entscheidet" in grund


def testDerStakeholderGibtMitHöhererGrenzeFrei(wurzel):
    datei = transkript(wurzel, "lauf.jsonl", 160_000)
    eingabe = werkzeug("PreToolUse", datei, rolle="koordinator", agentId=None)
    assert entscheide(eingabe, wurzel) is not None
    freigabedatei(wurzel).parent.mkdir(parents=True, exist_ok=True)
    freigabedatei(wurzel).write_text("200000", encoding="utf-8")
    assert entscheide(eingabe, wurzel) is None


def testOhneRolleMisstDerHookNicht(wurzel):
    datei = transkript(wurzel, "lauf.jsonl", 500_000)
    assert entscheide(werkzeug("PreToolUse", datei, rolle=None), wurzel) is None


def testEinUnlesbaresTranskriptSperrtNie(wurzel):
    eingabe = werkzeug("PreToolUse", wurzel / "gibtEsNicht.jsonl")
    assert entscheide(eingabe, wurzel) is None
