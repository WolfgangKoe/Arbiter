"""Hook `SessionStart`: leitet den Stand des Zyklus aus `handoff/` ab, eine Zeile.

Plan, Review und Retro tragen in der ersten Zeile `Zyklus <n>`. Kein Briefing.
"""

from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path

from agenten import projektordner

ABFOLGE = (
    ("plan.md", "Plan", "Domänenphase"),
    ("review.md", "Review", "Technikphase"),
    ("retro.md", "Retro", "Prozessphase"),
)


def zyklus(datei: Path) -> int | None:
    if not datei.is_file():
        return None
    erste_zeile = datei.read_text(encoding="utf-8").partition("\n")[0]
    treffer = re.search(r"Zyklus\s+(\d+)", erste_zeile)
    return int(treffer.group(1)) if treffer else None


def phase(handoff: Path) -> str:
    nummern = [zyklus(handoff / name) for name, _, _ in ABFOLGE]
    if nummern[0] is None:
        return "Noch kein Zyklus begonnen → Domänenphase, Plan 1"
    aktuell = nummern[0]
    for (_, artefakt, zustaendige_phase), nummer in zip(ABFOLGE[1:], nummern[1:], strict=True):
        if nummer != aktuell:
            return f"Zyklus {aktuell}: {artefakt} {aktuell} fehlt → {zustaendige_phase}"
    return f"Zyklus {aktuell} abgeschlossen → Domänenphase, Plan {aktuell + 1}"


def offene_anliegen(handoff: Path) -> int:
    ordner = handoff / "anliegen"
    return len(list(ordner.glob("*.md"))) if ordner.is_dir() else 0


def uncommittet(wurzel: Path) -> int:
    ausgabe = subprocess.run(
        ["git", "status", "--porcelain"], cwd=wurzel, capture_output=True, text=True, check=False
    ).stdout
    return len([zeile for zeile in ausgabe.splitlines() if zeile])


def stand(wurzel: Path) -> str:
    handoff = wurzel / "handoff"
    teile = [
        phase(handoff),
        f"{offene_anliegen(handoff)} offene Anliegen",
        f"{uncommittet(wurzel)} uncommittete Dateien",
    ]
    if (wurzel / "VORGEHEN.md").is_file():
        teile.append("Übergang: Aufbau laut VORGEHEN.md, Abschnitt „Einstieg“")
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
