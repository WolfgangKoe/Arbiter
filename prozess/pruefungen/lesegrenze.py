"""Hook `PreToolUse` auf `Read`: Der Koordinator liest nur kurze Dateien.

Er leitet weiter und liest keine Inhalte; lange Dokumente lesen die Rollen. In Zyklus 1 las er
zu Beginn die ganze VORGEHEN.md (25.000 Zeichen).
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

from agenten import projektordner

GEPRUEFTE_ROLLE = "koordinator"
HOECHSTLAENGE = 4000


def entscheide(eingabe: dict, wurzel: Path) -> dict | None:
    if eingabe.get("agent_type") != GEPRUEFTE_ROLLE or eingabe.get("tool_name") != "Read":
        return None
    datei = Path((eingabe.get("tool_input") or {}).get("file_path", ""))
    datei = datei if datei.is_absolute() else wurzel / datei
    if not datei.is_file():
        return None
    try:
        laenge = len(datei.read_text(encoding="utf-8"))
    except UnicodeDecodeError:
        return None
    if laenge <= HOECHSTLAENGE:
        return None
    return {
        "hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "permissionDecision": "deny",
            "permissionDecisionReason": f"{datei.name} hat {laenge} Zeichen; du liest höchstens "
            f"{HOECHSTLAENGE}. Nenne der zuständigen Rolle den Pfad, sie liest selbst.",
        }
    }


if __name__ == "__main__":
    antwort = entscheide(json.load(sys.stdin), projektordner())
    if antwort:
        print(json.dumps(antwort, ensure_ascii=False))
