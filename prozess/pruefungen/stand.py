"""Hook `SessionStart`: Stand in einer Zeile, mit dem nächsten Schritt. Kein Briefing.

Jede Phase ist eine feste Folge von Artefakten; der Stand nennt das erste, das fehlt.
Übergänge: Domäne → Technik mit dem Commit `Freigabe Plan <n>`, Technik → Prozess mit
Review n, Prozess → Domäne mit `Freigabe Retro <n>`. Der Trigger für die Technik ist früh:
Ein Plan mit einem einzigen Item aus der ersten fertigen Anforderung genügt.
Die aktuelle Etappe ist die nach Namen erste Datei `domaene/etappen/*.md` (`# Etappe <n> · …`).
"""

from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path

from agenten import projektordner

BUDGET = {"Domänenphase": 8, "Technikphase": 10, "Prozessphase": 5}


def git(wurzel: Path, *argumente: str) -> str:
    return subprocess.run(
        ["git", *argumente], cwd=wurzel, capture_output=True, text=True, check=False
    ).stdout


def freigabe_commit(wurzel: Path, gegenstand: str, nummer: int) -> str | None:
    """Der Commit mit der Betreffzeile `Freigabe <gegenstand> <nummer>`, sonst `None`."""
    for zeile in git(wurzel, "log", "--format=%H %s").splitlines():
        kennung, _, betreff = zeile.partition(" ")
        if betreff == f"Freigabe {gegenstand} {nummer}":
            return kennung
    return None


def zyklus(datei: Path) -> int | None:
    if not datei.is_file():
        return None
    erste_zeile = datei.read_text(encoding="utf-8").partition("\n")[0]
    treffer = re.search(r"Zyklus\s+(\d+)", erste_zeile)
    return int(treffer.group(1)) if treffer else None


def aktuelle_etappe(wurzel: Path) -> tuple[int, str] | None:
    dateien = sorted((wurzel / "domaene" / "etappen").glob("*.md"))
    if not dateien:
        return None
    for zeile in dateien[0].read_text(encoding="utf-8").splitlines():
        treffer = re.match(r"# (Etappe\s+(\d+).*)", zeile)
        if treffer:
            return int(treffer.group(2)), treffer.group(1).strip()
    return None


def gibt_anforderungen(wurzel: Path) -> bool:
    return any(
        zeile.startswith("### ")
        for datei in (wurzel / "domaene" / "anforderungen").rglob("*.md")
        for zeile in datei.read_text(encoding="utf-8").splitlines()
    )


def akzeptanztests_seit(wurzel: Path, kennung: str) -> bool:
    pfad = "technik/tests/akzeptanz"
    return bool(git(wurzel, "log", "--format=%H", f"{kennung}..HEAD", "--", pfad))


def domaenenphase(wurzel: Path, n: int) -> str:
    etappe = aktuelle_etappe(wurzel)
    if etappe is None:
        return "Planer: Etappen aus dem Ziel ableiten"
    nummer, _ = etappe
    if freigabe_commit(wurzel, "Etappe", nummer) is None:
        return f"Etappe {nummer} wartet auf Kritik (Architekt) und Freigabe"
    if not gibt_anforderungen(wurzel):
        return f"Anforderungsautor: erste Anforderung zu Etappe {nummer}"
    return f"Planer: Plan {n} mit den Items, die bereit sind (eins genügt, höchstens drei)"


def lage(wurzel: Path) -> tuple[int, str, str]:
    """Zyklus, Phase und nächster Schritt aus den Artefakten in `handoff/` und git."""
    handoff = wurzel / "handoff"
    plan, review, retro = (zyklus(handoff / f"{name}.md") for name in ("plan", "review", "retro"))
    if plan is None:
        return 1, "Domänenphase", domaenenphase(wurzel, 1)
    freigabe_plan = freigabe_commit(wurzel, "Plan", plan)
    if freigabe_plan is None:
        return plan, "Domänenphase", f"Plan {plan} wartet auf Kritik (Architekt) und Freigabe"
    if review != plan:
        if not akzeptanztests_seit(wurzel, freigabe_plan):
            return plan, "Technikphase", f"Testautor: Akzeptanztests zu den Items von Plan {plan}"
        return plan, "Technikphase", f"Implementierer, dann Reviewer: Tests grün, Review {plan}"
    if retro != plan:
        return plan, "Prozessphase", f"Organisationsentwickler: Retro {plan}"
    if freigabe_commit(wurzel, "Retro", plan) is None:
        return plan, "Prozessphase", f"Retro {plan} wartet auf Kritik und Freigabe"
    return plan + 1, "Domänenphase", domaenenphase(wurzel, plan + 1)


def protokoll(wurzel: Path) -> Path:
    return wurzel / ".git" / "arbiter" / "rollenlaeufe.jsonl"


def rollenlaeufe(wurzel: Path, schluessel: str) -> int:
    datei = protokoll(wurzel)
    if not datei.is_file():
        return 0
    return sum(
        json.loads(zeile).get("phase") == schluessel
        for zeile in datei.read_text(encoding="utf-8").splitlines()
        if zeile.strip()
    )


def budget(wurzel: Path, n: int, phase: str) -> str:
    laeufe, grenze = rollenlaeufe(wurzel, f"Zyklus {n} · {phase}"), BUDGET[phase]
    if laeufe > grenze:
        return (
            f"über Budget ({laeufe}/{grenze} Rollenläufe) → Stakeholder: freigeben, kürzen "
            "oder verlängern"
        )
    return f"Budget {laeufe}/{grenze} Rollenläufe"


def stand(wurzel: Path) -> str:
    n, phase, schritt = lage(wurzel)
    etappe = aktuelle_etappe(wurzel)
    ordner = wurzel / "handoff" / "anliegen"
    anliegen = len(list(ordner.glob("*.md"))) if ordner.is_dir() else 0
    uncommittet = len([z for z in git(wurzel, "status", "--porcelain").splitlines() if z])
    teile = [
        etappe[1] if etappe else "Keine Etappe",
        f"Zyklus {n}, {phase}",
        f"Nächster Schritt: {schritt}",
        budget(wurzel, n, phase),
        f"{anliegen} offene Anliegen",
        f"{uncommittet} uncommittete Dateien",
    ]
    return "Stand: " + " · ".join(teile)


if __name__ == "__main__":
    json.load(sys.stdin)
    print(
        json.dumps(
            {
                "hookSpecificOutput": {
                    "hookEventName": "SessionStart",
                    "additionalContext": stand(projektordner()),
                }
            },
            ensure_ascii=False,
        )
    )
