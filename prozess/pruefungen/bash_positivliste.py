"""Hook: Der Koordinator führt nur Befehle aus der Positivliste aus; Rollen nutzen git nur lesend.

Berechtigungsregeln reichen nicht: Ohne Write hat ein Agent in der Probe per
`echo > datei` geschrieben. Für den Koordinator sind Verkettung, Umleitung und
Befehlsersetzung gesperrt. Committen ist allein Sache des Koordinators; in Zyklus 1 hatten
Planer und Architekt selbst committet.
"""

from __future__ import annotations

import json
import shlex
import sys
from pathlib import Path

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

GIT_LESEND = (
    "status", "log", "diff", "show", "grep", "ls-files", "ls-tree", "blame",
    "rev-parse", "shortlog", "cat-file", "describe",
)
GIT_OPTIONEN_MIT_WERT = ("-C", "-c", "--git-dir", "--work-tree")


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


def git_unterbefehle(befehl: str) -> list[str]:
    """Die Unterbefehle aller git-Aufrufe, auch in verketteten Befehlen."""
    zerleger = shlex.shlex(befehl.replace("\n", " ; "), posix=True, punctuation_chars=True)
    zerleger.whitespace_split = True
    try:
        teile = list(zerleger)
    except ValueError:
        return ["(nicht lesbar)"] if "git" in befehl else []
    unterbefehle = []
    for i, teil in enumerate(teile):
        if Path(teil).name != "git" or (i and not set(teile[i - 1]) <= OPERATOR_ZEICHEN):
            continue
        j = i + 1
        while j < len(teile) and teile[j].startswith("-"):
            j += 2 if teile[j] in GIT_OPTIONEN_MIT_WERT else 1
        unterbefehle.append(teile[j] if j < len(teile) else "")
    return unterbefehle


def ablehnen(grund: str) -> dict:
    return {
        "hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "permissionDecision": "deny",
            "permissionDecisionReason": grund,
        }
    }


def entscheide(eingabe: dict) -> dict | None:
    rolle = eingabe.get("agent_type")
    if not rolle or eingabe.get("tool_name") != "Bash":
        return None
    befehl = (eingabe.get("tool_input") or {}).get("command", "")
    if rolle == GEPRUEFTE_ROLLE:
        if ist_erlaubt(befehl):
            return None
        return ablehnen(
            "Bash-Positivliste des Koordinators: nur "
            + ", ".join(ERLAUBT)
            + "; ohne Verkettung und Umleitung. Andere Arbeit beauftragst du bei einer Rolle."
        )
    schreibend = [u for u in git_unterbefehle(befehl) if u not in GIT_LESEND]
    if not schreibend:
        return None
    return ablehnen(
        f"git {schreibend[0]} ist dem Koordinator vorbehalten; Rollen nutzen git nur lesend "
        f"({', '.join(GIT_LESEND)}). Lösche Dateien mit rm, committet wird vom Koordinator."
    )


if __name__ == "__main__":
    antwort = entscheide(json.load(sys.stdin))
    if antwort:
        print(json.dumps(antwort, ensure_ascii=False))
