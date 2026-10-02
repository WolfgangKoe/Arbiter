"""Hook: Eine Rolle schreibt nur in ihren Schreibpfaden.

Write/Edit werden vorab gesperrt (`PreToolUse`). Was eine Rolle per Bash ändert, meldet
`SubagentStop` dem Koordinator, verglichen mit dem git-Stand bei `SubagentStart`. Beim
Start erfährt die Rolle ihre Schreibpfade, denn den Kopf ihrer Definition sieht sie nicht.
Ohne `agent_type` arbeitet der Stakeholder selbst; dann greift die Grenze nicht.
"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

from agenten import darf_schreiben, projektordner, schreibpfade

SCHREIBWERKZEUGE = ("Write", "Edit", "NotebookEdit")


def geaenderte_pfade(wurzel: Path) -> set[str]:
    ausgabe = subprocess.run(
        ["git", "status", "--porcelain", "--untracked-files=all"],
        cwd=wurzel,
        capture_output=True,
        text=True,
        check=False,
    ).stdout
    return {zeile[3:].split(" -> ")[-1] for zeile in ausgabe.splitlines() if zeile}


def stand_datei(wurzel: Path, agent_id: str) -> Path:
    return wurzel / ".git" / "arbiter-schreibgrenze" / f"{agent_id}.txt"


def vor_dem_schreiben(eingabe: dict, wurzel: Path) -> dict | None:
    rolle = eingabe.get("agent_type")
    if not rolle or eingabe.get("tool_name") not in SCHREIBWERKZEUGE:
        return None
    werkzeug = eingabe.get("tool_input") or {}
    ziel = Path(werkzeug.get("file_path") or werkzeug.get("notebook_path") or "")
    ziel = (wurzel / ziel).resolve() if not ziel.is_absolute() else ziel.resolve()
    if ziel.is_relative_to(wurzel):
        relativ = ziel.relative_to(wurzel).as_posix()
        if darf_schreiben(relativ, schreibpfade(rolle, wurzel)):
            return None
    else:
        relativ = str(ziel)
    return {
        "hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "permissionDecision": "deny",
            "permissionDecisionReason": f"Schreibgrenze: {rolle} darf {relativ} nicht "
            "schreiben. Kritik an fremden Artefakten wird ein Anliegen.",
        }
    }


def beim_start(eingabe: dict, wurzel: Path) -> dict:
    datei = stand_datei(wurzel, eingabe["agent_id"])
    datei.parent.mkdir(parents=True, exist_ok=True)
    datei.write_text("\n".join(sorted(geaenderte_pfade(wurzel))), encoding="utf-8")
    muster = schreibpfade(eingabe.get("agent_type") or "", wurzel)
    return {
        "hookSpecificOutput": {
            "hookEventName": "SubagentStart",
            "additionalContext": "Deine Schreibpfade: "
            + (", ".join(muster) if muster else "keine, du schreibst nichts"),
        }
    }


def beim_ende(eingabe: dict, wurzel: Path) -> dict | None:
    datei = stand_datei(wurzel, eingabe["agent_id"])
    vorher = set(datei.read_text(encoding="utf-8").splitlines()) if datei.exists() else set()
    datei.unlink(missing_ok=True)
    muster = schreibpfade(eingabe["agent_type"], wurzel)
    verstoesse = sorted(
        p for p in geaenderte_pfade(wurzel) - vorher if not darf_schreiben(p, muster)
    )
    if not verstoesse:
        return None
    return {
        "hookSpecificOutput": {
            "hookEventName": "SubagentStop",
            "additionalContext": f"Schreibgrenze verletzt: {eingabe['agent_type']} hat "
            f"außerhalb seiner Schreibpfade geändert: {', '.join(verstoesse)}. "
            "Nicht committen, dem Stakeholder melden.",
        }
    }


def entscheide(eingabe: dict, wurzel: Path) -> dict | None:
    ereignis = eingabe.get("hook_event_name")
    if ereignis == "PreToolUse":
        return vor_dem_schreiben(eingabe, wurzel)
    if ereignis == "SubagentStart" and eingabe.get("agent_id"):
        return beim_start(eingabe, wurzel)
    if ereignis == "SubagentStop" and eingabe.get("agent_id"):
        return beim_ende(eingabe, wurzel)
    return None


if __name__ == "__main__":
    antwort = entscheide(json.load(sys.stdin), projektordner())
    if antwort:
        print(json.dumps(antwort, ensure_ascii=False))
