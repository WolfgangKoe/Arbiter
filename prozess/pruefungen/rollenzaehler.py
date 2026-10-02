"""Hook `SubagentStart`: zählt jeden Rollenlauf mit Zyklus und Phase, für das Budget im Stand.

Das Protokoll liegt in `.git/arbiter/`, damit es keine Änderung im Arbeitsbaum erzeugt.
"""

from __future__ import annotations

import json
import sys
from datetime import datetime, timezone

from agenten import projektordner
from stand import lage, protokoll


def zaehle(eingabe: dict, wurzel) -> None:
    if not eingabe.get("agent_type"):
        return
    n, phase, _ = lage(wurzel)
    datei = protokoll(wurzel)
    datei.parent.mkdir(parents=True, exist_ok=True)
    eintrag = {
        "zeit": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "phase": f"Zyklus {n} · {phase}",
        "rolle": eingabe["agent_type"],
    }
    with datei.open("a", encoding="utf-8") as ziel:
        ziel.write(json.dumps(eintrag, ensure_ascii=False) + "\n")


if __name__ == "__main__":
    zaehle(json.load(sys.stdin), projektordner())
