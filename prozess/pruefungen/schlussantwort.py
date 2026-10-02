"""Hook `PreToolUse` auf `SubagentHandback`: Schlussantworten nennen nur Status und Pfade.

Inhalte gehören nach `handoff/`, nicht in den Kontext des Koordinators. In Zyklus 1 kamen
Schlussantworten bis 17.000 Zeichen; der Kontext des Koordinators lief voll. In VS Code kommt
der Bericht über `SubagentHandback`, headless als letzte Nachricht; dort prüft `SubagentStop`.
"""

from __future__ import annotations

import json
import sys

HOECHSTLAENGE = 800


def grund(laenge: int) -> str:
    return (
        f"Schlussantwort hat {laenge} Zeichen, höchstens {HOECHSTLAENGE}. Inhalte, Fragen und "
        "Empfehlungen gehören in eine Datei in handoff/; hier nur Status und Pfade."
    )


def entscheide(eingabe: dict) -> dict | None:
    if not eingabe.get("agent_type"):
        return None
    if eingabe.get("hook_event_name") == "SubagentStop":
        bericht = eingabe.get("last_assistant_message") or ""
        if len(bericht) <= HOECHSTLAENGE or eingabe.get("stop_hook_active"):
            return None
        return {"decision": "block", "reason": grund(len(bericht))}
    if eingabe.get("tool_name") != "SubagentHandback":
        return None
    bericht = (eingabe.get("tool_input") or {}).get("message", "")
    if len(bericht) <= HOECHSTLAENGE:
        return None
    return {
        "hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "permissionDecision": "deny",
            "permissionDecisionReason": grund(len(bericht)),
        }
    }


if __name__ == "__main__":
    antwort = entscheide(json.load(sys.stdin))
    if antwort:
        print(json.dumps(antwort, ensure_ascii=False))
