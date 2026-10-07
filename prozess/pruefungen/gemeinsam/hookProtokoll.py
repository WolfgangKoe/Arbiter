"""Ein- und Ausgabe der Hooks von Claude Code."""

import json
import sys
from dataclasses import dataclass
from pathlib import Path

# Warum: Nur hier stehen die Feldnamen der Hook-Eingabe; `formregeln/einzelstellen.py` prüft das.
feldnamen = {
    "rolle": "agent_type",
    "werkzeug": "tool_name",
    "ereignis": "hook_event_name",
    "agentId": "agent_id",
    "sitzung": "session_id",
    "transkript": "transcript_path",
    "rollenTranskript": "agent_transcript_path",
    "letzteAntwort": "last_assistant_message",
    "stoppWiederholt": "stop_hook_active",
    "angaben": "tool_input",
}


def feldVon(daten: dict, attribut: str):
    """Der Wert des Feldes der Hook-Eingabe, das zum Attribut von `HookEingabe` gehört."""
    return daten.get(feldnamen[attribut])


@dataclass(frozen=True)
class HookEingabe:
    """Die Felder der Hook-Eingabe von Claude Code; fehlt eines, ist es `None`."""

    rolle: str | None
    werkzeug: str | None
    ereignis: str | None
    agentId: str | None
    sitzung: str | None
    transkript: Path | None
    rollenTranskript: Path | None
    letzteAntwort: str
    stoppWiederholt: bool
    angaben: dict

    @classmethod
    def aus(cls, daten: dict) -> "HookEingabe":
        transkript = feldVon(daten, "transkript")
        rollenTranskript = feldVon(daten, "rollenTranskript")
        return cls(
            rolle=feldVon(daten, "rolle") or None,
            werkzeug=feldVon(daten, "werkzeug"),
            ereignis=feldVon(daten, "ereignis"),
            agentId=feldVon(daten, "agentId") or None,
            sitzung=feldVon(daten, "sitzung"),
            transkript=Path(transkript) if transkript else None,
            rollenTranskript=Path(rollenTranskript) if rollenTranskript else None,
            letzteAntwort=feldVon(daten, "letzteAntwort") or "",
            stoppWiederholt=bool(feldVon(daten, "stoppWiederholt")),
            angaben=feldVon(daten, "angaben") or {},
        )


def eingabeLesen() -> dict:
    return json.load(sys.stdin)


def verweigerung(grund: str) -> dict:
    return {
        "hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "permissionDecision": "deny",
            "permissionDecisionReason": grund,
        }
    }


def zusatzkontext(ereignis: str, text: str) -> dict:
    return {"hookSpecificOutput": {"hookEventName": ereignis, "additionalContext": text}}


def antwortAusgeben(antwort: dict | None) -> None:
    if antwort:
        print(json.dumps(antwort, ensure_ascii=False))
