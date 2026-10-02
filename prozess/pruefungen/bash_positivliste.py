"""Hook: Der Koordinator führt nur Befehle aus der Positivliste aus.

Berechtigungsregeln reichen nicht: Ohne Write hat ein Agent in der Probe per
`echo > datei` geschrieben. Verkettung, Umleitung und Befehlsersetzung sind gesperrt.
"""

from __future__ import annotations

import json
import shlex
import sys

GEPRUEFTE_ROLLE = "koordinator"

ERLAUBT = (
    "git status",
    "git diff",
    "git log",
    "git show",
    "git add",
    "git commit",
    "git push",
    "git rev-parse",
    "git ls-files",
    "ls",
    "python3 prozess/pruefungen/",
    "python3 -m pytest prozess/pruefungen",
)

OPERATOR_ZEICHEN = set(";&|<>()")


def woerter(befehl: str) -> list[str] | None:
    """Zerlegt wie die Shell; `None`, wenn der Befehl Verkettung oder Umleitung enthält."""
    if "$(" in befehl or "`" in befehl or "\n" in befehl:
        return None
    zerleger = shlex.shlex(befehl, posix=True, punctuation_chars=True)
    zerleger.whitespace_split = True
    try:
        teile = list(zerleger)
    except ValueError:
        return None
    if any(teil and set(teil) <= OPERATOR_ZEICHEN for teil in teile):
        return None
    return teile


def ist_erlaubt(befehl: str) -> bool:
    teile = woerter(befehl)
    if not teile:
        return False
    zeile = " ".join(teile)
    return any(
        zeile.startswith(eintrag)
        if eintrag.endswith("/")
        else zeile == eintrag or zeile.startswith(eintrag + " ")
        for eintrag in ERLAUBT
    )


def entscheide(eingabe: dict) -> dict | None:
    if eingabe.get("agent_type") != GEPRUEFTE_ROLLE or eingabe.get("tool_name") != "Bash":
        return None
    befehl = (eingabe.get("tool_input") or {}).get("command", "")
    if ist_erlaubt(befehl):
        return None
    return {
        "hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "permissionDecision": "deny",
            "permissionDecisionReason": "Bash-Positivliste des Koordinators: nur "
            + ", ".join(ERLAUBT)
            + "; ohne Verkettung und Umleitung. Andere Arbeit beauftragst du bei einer Rolle.",
        }
    }


if __name__ == "__main__":
    antwort = entscheide(json.load(sys.stdin))
    if antwort:
        print(json.dumps(antwort, ensure_ascii=False))
