"""Hook: Eine Rolle schreibt nur in ihren Schreibpfaden; manche Pfade sind für alle nur lesbar."""

import json
import subprocess
import sys
from pathlib import Path

from agenten import darfSchreiben, istNurLesbar, nurLesbar, projektordner, schreibpfade

schreibwerkzeuge = ("Write", "Edit", "NotebookEdit")


def geänderteDateien(wurzel: Path) -> set[str]:
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


def standDatei(wurzel: Path, agentId: str) -> Path:
    return wurzel / ".git" / "arbiter-schreibgrenze" / f"{agentId}.txt"


def sperren(grund: str) -> dict:
    return {
        "hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "permissionDecision": "deny",
            "permissionDecisionReason": grund,
        }
    }


def vorDemSchreiben(eingabe: dict, wurzel: Path) -> dict | None:
    rolle = eingabe.get("agent_type")
    if not rolle or eingabe.get("tool_name") not in schreibwerkzeuge:
        return None
    werkzeug = eingabe.get("tool_input") or {}
    ziel = Path(werkzeug.get("file_path") or werkzeug.get("notebook_path") or "")
    ziel = (wurzel / ziel).resolve() if not ziel.is_absolute() else ziel.resolve()
    if ziel.is_relative_to(wurzel):
        relativ = ziel.relative_to(wurzel).as_posix()
        if istNurLesbar(relativ):
            return sperren(
                f"Schreibgrenze: {relativ} ist nur lesbar, für alle Rollen und den Koordinator. "
                "Löschen und ändern tut nur der Stakeholder."
            )
        if darfSchreiben(relativ, schreibpfade(rolle, wurzel)):
            return None
    else:
        relativ = str(ziel)
    return sperren(
        f"Schreibgrenze: {rolle} darf {relativ} nicht schreiben. "
        "Kritik an fremden Artefakten wird ein Anliegen."
    )


def beimStart(eingabe: dict, wurzel: Path) -> dict:
    datei = standDatei(wurzel, eingabe["agent_id"])
    datei.parent.mkdir(parents=True, exist_ok=True)
    zeilen = [f"HEAD {kopf(wurzel)}", *sorted(geänderteDateien(wurzel))]
    datei.write_text("\n".join(zeilen), encoding="utf-8")
    muster = schreibpfade(eingabe.get("agent_type") or "", wurzel)
    return {
        "hookSpecificOutput": {
            "hookEventName": "SubagentStart",
            "additionalContext": "Deine Schreibpfade: "
            + (", ".join(muster) if muster else "keine, du schreibst nichts")
            + f". Für alle nur lesbar: {', '.join(nurLesbar)}.",
        }
    }


def beimEnde(eingabe: dict, wurzel: Path) -> dict | None:
    datei = standDatei(wurzel, eingabe["agent_id"])
    zeilen = datei.read_text(encoding="utf-8").splitlines() if datei.exists() else []
    datei.unlink(missing_ok=True)
    kopfVorher = next(
        (zeile.removeprefix("HEAD ") for zeile in zeilen if zeile.startswith("HEAD ")), None
    )
    vorher = {zeile for zeile in zeilen if not zeile.startswith("HEAD ")}
    rolle = eingabe["agent_type"]
    muster = schreibpfade(rolle, wurzel)
    meldungen = []
    verstöße = sorted(
        pfad
        for pfad in geänderteDateien(wurzel) - vorher
        if istNurLesbar(pfad) or not darfSchreiben(pfad, muster)
    )
    if verstöße:
        meldungen.append(
            f"Schreibgrenze verletzt: {rolle} hat außerhalb seiner Schreibpfade oder in nur "
            f"lesbaren Pfaden geändert: {', '.join(verstöße)}."
        )
    if kopfVorher is not None and kopf(wurzel) != kopfVorher:
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
        return vorDemSchreiben(eingabe, wurzel)
    if ereignis == "SubagentStart" and eingabe.get("agent_id"):
        return beimStart(eingabe, wurzel)
    if ereignis == "SubagentStop" and eingabe.get("agent_id"):
        return beimEnde(eingabe, wurzel)
    return None


if __name__ == "__main__":
    antwort = entscheide(json.load(sys.stdin), projektordner())
    if antwort:
        print(json.dumps(antwort, ensure_ascii=False))
