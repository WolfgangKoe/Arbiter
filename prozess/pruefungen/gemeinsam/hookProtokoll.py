"""Ein- und Ausgabe der Hooks von Claude Code."""

import json
import sys
from dataclasses import dataclass
from pathlib import Path


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
        transkript = daten.get("transcript_path")
        rollenTranskript = daten.get("agent_transcript_path")
        return cls(
            rolle=daten.get("agent_type") or None,
            werkzeug=daten.get("tool_name"),
            ereignis=daten.get("hook_event_name"),
            agentId=daten.get("agent_id") or None,
            sitzung=daten.get("session_id"),
            transkript=Path(transkript) if transkript else None,
            rollenTranskript=Path(rollenTranskript) if rollenTranskript else None,
            letzteAntwort=daten.get("last_assistant_message") or "",
            stoppWiederholt=bool(daten.get("stop_hook_active")),
            angaben=daten.get("tool_input") or {},
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
