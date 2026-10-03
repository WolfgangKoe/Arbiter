"""Hook (PreToolUse, Write und Edit): `erledigt` setzt nur der Absender des Anliegens."""

import json
import sys
from pathlib import Path

from agenten import projektordner
from anliegen import Anliegen, höchstRunde, kopfAusText

letzteRunde = "Runde 3/3 ist die letzte; setze `eskaliert`, der Stakeholder entscheidet."


def neuerInhalt(werkzeug: str, eingabe: dict, bisher: str) -> str | None:
    if werkzeug == "Write":
        return eingabe.get("content")
    if werkzeug == "Edit":
        alt, neu = eingabe.get("old_string"), eingabe.get("new_string")
        if alt is None or neu is None:
            return None
        anzahl = -1 if eingabe.get("replace_all") else 1
        return bisher.replace(alt, neu, anzahl)
    return None


def entscheide(eingabe: dict, wurzel: Path) -> dict | None:
    # Warum: Ohne `agent_type` spricht die Hauptsitzung, für sie gilt keine Grenze.
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
    alt = kopfAusText(bisher, ziel)
    if neu is None:
        return None
    grund = erledigtVerstoß(alt, neu, rolle) or rundenVerstoß(alt, neu)
    if grund is None:
        return None
    return {
        "hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "permissionDecision": "deny",
            "permissionDecisionReason": f"Statusrecht: {ziel.name} {grund}",
        }
    }


def erledigtVerstoß(alt: Anliegen | None, neu: Anliegen, rolle: str) -> str | None:
    if neu.status != "erledigt" or neu.absender.lower() == rolle.lower():
        return None
    if alt is not None and alt.status == "erledigt":
        return None
    return (
        f"setzt auf `erledigt` nur der Absender ({neu.absender}), nicht {rolle}. "
        "Setze `angenommen`, `abgelehnt` oder `beantwortet`."
    )


def rundenVerstoß(alt: Anliegen | None, neu: Anliegen) -> str | None:
    """Senken der Runde und Ändern von `eskaliert` bleibt dem Stakeholder."""
    if alt is None:
        return None
    if neu.runde < alt.runde:
        return f"senkt die Runde von {alt.runde}/3 auf {neu.runde}/3. {letzteRunde}"
    if alt.status == "eskaliert" and neu.status != "eskaliert":
        return f"ändert `eskaliert` zu `{neu.status}`. Der Stakeholder entscheidet."
    if (
        alt.runde == höchstRunde
        and alt.status == "abgelehnt"
        and neu.status not in ("abgelehnt", "eskaliert", "erledigt")
    ):
        return f"setzt in Runde 3/3 nach `abgelehnt` `{neu.status}`. {letzteRunde}"
    return None


if __name__ == "__main__":
    antwort = entscheide(json.load(sys.stdin), projektordner())
    if antwort:
        print(json.dumps(antwort, ensure_ascii=False))
    sys.exit(0)
