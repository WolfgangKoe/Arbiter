"""Hook (PreToolUse, Write und Edit): `erledigt` setzt nur der Absender des Anliegens.

Die Rolle (`agent_type`) muss der Absender im Kopf sein. Ohne `agent_type` schreibt der
Stakeholder selbst; dann greift die Sperre nicht. Was eine Rolle per Bash ändert, erfasst
der Hook nicht ([Anliegen 34](../../handoff/anliegen/34-erledigtNurDurchDenAbsender.md)).
"""

import json
import sys
from pathlib import Path

from agenten import projektordner
from anliegen import kopfAusText


def neuerInhalt(werkzeug: str, eingabe: dict, bisher: str) -> str | None:
    if werkzeug == "Write":
        return eingabe.get("content")
    if werkzeug == "Edit":
        alt, neu = eingabe.get("old_string"), eingabe.get("new_string")
        if alt is None or neu is None:
            return None
        return bisher.replace(alt, neu) if eingabe.get("replace_all") else bisher.replace(alt, neu, 1)
    return None


def entscheide(eingabe: dict, wurzel: Path) -> dict | None:
    rolle = eingabe.get("agent_type")
    werkzeug = eingabe.get("tool_name")
    angaben = eingabe.get("tool_input") or {}
    if not rolle or werkzeug not in ("Write", "Edit") or not angaben.get("file_path"):
        return None
    ziel = Path(angaben["file_path"])
    ziel = ziel if ziel.is_absolute() else wurzel / ziel
    ziel = ziel.resolve()
    if ziel.parent != (wurzel / "handoff" / "anliegen").resolve() or ziel.suffix != ".md":
        return None
    bisher = ziel.read_text(encoding="utf-8") if ziel.is_file() else ""
    danach = neuerInhalt(werkzeug, angaben, bisher)
    neu = kopfAusText(danach, ziel) if danach is not None else None
    if neu is None or neu.status != "erledigt" or neu.absender.lower() == rolle.lower():
        return None
    alt = kopfAusText(bisher, ziel)
    if alt is not None and alt.status == "erledigt":
        return None
    return {
        "hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "permissionDecision": "deny",
            "permissionDecisionReason": (
                f"Statusrecht: {ziel.name} setzt auf `erledigt` nur der Absender "
                f"({neu.absender}), nicht {rolle}. Setze `angenommen`, `abgelehnt` oder `beantwortet`."
            ),
        }
    }


if __name__ == "__main__":
    antwort = entscheide(json.load(sys.stdin), projektordner())
    if antwort:
        print(json.dumps(antwort, ensure_ascii=False))
    sys.exit(0)
