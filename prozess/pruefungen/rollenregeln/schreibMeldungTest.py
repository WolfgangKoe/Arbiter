import json
from pathlib import Path

from rollenregeln.schreibBilanz import meldungsOrdner
from rollenregeln.schreibMeldung import entscheide


def meldungAblegen(wurzel: Path, agentId: str, text: str) -> None:
    meldungsOrdner(wurzel).mkdir(parents=True, exist_ok=True)
    (meldungsOrdner(wurzel) / f"{agentId}.txt").write_text(text, encoding="utf-8")


def testDerKoordinatorBekommtDieMeldungAlsKontextZumWerkzeugaufrufUndNurEinmal(tmp_path):
    meldungAblegen(tmp_path, "a1", "Schreibgrenze verletzt: probe.")
    daten = {"hook_event_name": "PostToolUse", "tool_name": "Read", "agent_type": "koordinator"}

    antwort = entscheide(daten, tmp_path)

    assert antwort["hookSpecificOutput"]["hookEventName"] == "PostToolUse"
    assert "Schreibgrenze verletzt: probe." in antwort["hookSpecificOutput"]["additionalContext"]
    assert entscheide(daten, tmp_path) is None


def testEineRolleBekommtDieMeldungEinerAnderenNicht(tmp_path):
    meldungAblegen(tmp_path, "a1", "Schreibgrenze verletzt: probe.")
    daten = {"hook_event_name": "PostToolUse", "agent_id": "a2", "agent_type": "probe"}
    assert entscheide(daten, tmp_path) is None
    assert (meldungsOrdner(tmp_path) / "a1.txt").exists()


def testOhneMeldungBleibtDerHookStill(tmp_path):
    assert entscheide(json.loads('{"hook_event_name": "PostToolUse"}'), tmp_path) is None
