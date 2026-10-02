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


def kopf(wurzel: Path) -> str:
    return subprocess.run(
        ["git", "rev-parse", "HEAD"], cwd=wurzel, capture_output=True, text=True, check=False
    ).stdout.strip()


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
    zeilen = [f"HEAD {kopf(wurzel)}", *sorted(geaenderte_pfade(wurzel))]
    datei.write_text("\n".join(zeilen), encoding="utf-8")
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
    zeilen = datei.read_text(encoding="utf-8").splitlines() if datei.exists() else []
    datei.unlink(missing_ok=True)
    kopf_vorher = next((z.removeprefix("HEAD ") for z in zeilen if z.startswith("HEAD ")), None)
    vorher = {z for z in zeilen if not z.startswith("HEAD ")}
    rolle = eingabe["agent_type"]
    muster = schreibpfade(rolle, wurzel)
    meldungen = []
    verstoesse = sorted(
        p for p in geaenderte_pfade(wurzel) - vorher if not darf_schreiben(p, muster)
    )
    if verstoesse:
        meldungen.append(
            f"Schreibgrenze verletzt: {rolle} hat außerhalb seiner Schreibpfade geändert: "
            f"{', '.join(verstoesse)}."
        )
    if kopf_vorher is not None and kopf(wurzel) != kopf_vorher:
        meldungen.append(
            f"Während {rolle} lief, kam ein Commit hinzu. Hast du ihn nicht selbst gemacht, "
            f"hat {rolle} committet; das ist dem Koordinator vorbehalten."
        )
    if not meldungen:
        return None
    return {
        "hookSpecificOutput": {
            "hookEventName": "SubagentStop",
            "additionalContext": " ".join(meldungen) + " Nicht committen, dem Stakeholder melden.",
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
