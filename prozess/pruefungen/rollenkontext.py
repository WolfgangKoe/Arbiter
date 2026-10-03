"""Hook `SubagentStart`: Die Rolle bekommt Stand und die Ordner-CLAUDE.md ihrer Perspektive."""

import json
import sys
from pathlib import Path

from agenten import projektordner, schreibpfade
from stand import stand

perspektiven = ("domaene", "technik", "prozess")


def perspektive(rolle: str, wurzel: Path) -> str | None:
    muster = schreibpfade(rolle, wurzel)
    oberster = muster[0].split("/")[0] if muster else None
    return oberster if oberster in perspektiven else None


def kontext(rolle: str, wurzel: Path) -> str:
    teile = [stand(wurzel)]
    ordner = perspektive(rolle, wurzel)
    datei = wurzel / ordner / "CLAUDE.md" if ordner else None
    if datei and datei.is_file():
        teile.append(f"{ordner}/CLAUDE.md:\n" + datei.read_text(encoding="utf-8"))
    return "\n\n".join(teile)


if __name__ == "__main__":
    eingabe = json.load(sys.stdin)
    if eingabe.get("agent_type"):
        print(
            json.dumps(
                {
                    "hookSpecificOutput": {
                        "hookEventName": "SubagentStart",
                        "additionalContext": kontext(eingabe["agent_type"], projektordner()),
                    }
                },
                ensure_ascii=False,
            )
        )
