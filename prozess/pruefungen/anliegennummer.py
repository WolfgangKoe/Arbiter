"""Hook (PreToolUse, Write): Eine neue Anliegen-Datei trägt eine noch nie vergebene Nummer."""

import json
import sys
from pathlib import Path

from agenten import projektordner
from anliegen import nummerAusDateiname, nächsteFreieNummer, vergebeneNummern


def entscheide(eingabe: dict, wurzel: Path) -> dict | None:
    angaben = eingabe.get("tool_input") or {}
    if eingabe.get("tool_name") != "Write" or not angaben.get("file_path"):
        return None
    ziel = Path(angaben["file_path"])
    ziel = (ziel if ziel.is_absolute() else wurzel / ziel).resolve()
    if ziel.parent != (wurzel / "handoff" / "anliegen").resolve() or ziel.suffix != ".md":
        return None
    nummer = nummerAusDateiname(ziel.name)
    if ziel.is_file() or nummer is None or nummer not in vergebeneNummern(wurzel):
        return None
    return {
        "hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "permissionDecision": "deny",
            "permissionDecisionReason": (
                f"Die Nummer {nummer} ist vergeben. Die nächste freie ist "
                f"{nächsteFreieNummer(wurzel)}: Kopf und Dateiname ändern, neu schreiben."
            ),
        }
    }


if __name__ == "__main__":
    antwort = entscheide(json.load(sys.stdin), projektordner())
    if antwort:
        print(json.dumps(antwort, ensure_ascii=False))
    sys.exit(0)
