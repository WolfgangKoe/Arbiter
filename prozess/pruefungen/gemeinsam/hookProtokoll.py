"""Ein- und Ausgabe der Hooks von Claude Code."""

import json
import sys


def eingabeLesen() -> dict:
    return json.load(sys.stdin)


def werkzeugAngaben(eingabe: dict) -> dict:
    return eingabe.get("tool_input") or {}


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
