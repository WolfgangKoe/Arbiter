"""Hook `SubagentStart`: zählt jeden Rollenlauf mit Zyklus und Phase, als Kennzahl im Stand."""

import json
import sys
from datetime import UTC, datetime
from pathlib import Path

from agenten import projektordner
from stand import lage, protokoll


def zähle(eingabe: dict, wurzel: Path) -> None:
    if not eingabe.get("agent_type"):
        return
    zyklusNummer, phase, _ = lage(wurzel)
    # Warum: In `.git/` erzeugt das Protokoll keine Änderung im Arbeitsbaum.
    datei = protokoll(wurzel)
    datei.parent.mkdir(parents=True, exist_ok=True)
    eintrag = {
        "zeit": datetime.now(UTC).isoformat(timespec="seconds"),
        "phase": f"Zyklus {zyklusNummer} · {phase}",
        "rolle": eingabe["agent_type"],
    }
    with datei.open("a", encoding="utf-8") as ziel:
        ziel.write(json.dumps(eintrag, ensure_ascii=False) + "\n")


if __name__ == "__main__":
    zähle(json.load(sys.stdin), projektordner())
