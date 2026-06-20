#!/usr/bin/env python3
"""History-Rotation für den Session-Abschluss (Operating-Model Event 5).

Die fehleranfällige Handarbeit am Session-Ende — den verdichteten Stand als
Einzeiler in die lange ``docs/goals/ziel6.md`` einhängen *und* den alten
„Aktueller Stand"-Block in ``next_session.md`` zurücksetzen, damit der Startprompt
nicht über das 120-Zeilen-Doku-Gate wächst (S68-Befund) — wird hier mechanisch
erledigt. Das *Verdichten* selbst bleibt Urteil (Argument ``--summary``); das Tool
fasst nur die zwei klar abgegrenzten Bereiche an und bricht ab, wenn ein Marker
fehlt, statt still zu verstümmeln.

Aufruf am Session-Ende (Beispiel Abschluss von S69)::

    python tools/rotate_history.py --session 69 \\
        --summary "Vier S67-Nutzerwünsche umgesetzt …"

Danach den ausführlichen neuen Stand von Hand in den frisch zurückgesetzten Block
in ``next_session.md`` schreiben.
"""

from __future__ import annotations

import argparse
import re
import sys
from datetime import date as date_cls
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
ZIEL6 = REPO_ROOT / "docs" / "goals" / "ziel6.md"
NEXT_SESSION = REPO_ROOT / ".claude" / "tasks" / "next_session.md"

STAND_HEADER_PREFIX = "## Aktueller Stand"
NEXT_STEP_MARKER = "### ▶ Nächster Schritt"
_FRUEHERE_RE = re.compile(r"Frühere Sessions \(S(\d+)–S(\d+)\)")
_DEFAULT_RANGE_START = "60"


def append_history_line(ziel6_text: str, session: int, date: str, summary: str) -> str:
    """Hänge eine ``- **S<session> (<date>)** <summary>``-Zeile ans Ende an."""
    line = f"- **S{session} ({date})** {summary.strip()}"
    return f"{ziel6_text.rstrip()}\n{line}\n"


def reset_stand_block(next_session_text: str, session: int, date: str) -> str:
    """Ersetze den ``## Aktueller Stand``-Block durch einen frischen Rumpf.

    Erhält den im alten Block geparsten Bereich-Start der „Frühere Sessions"-Zeile
    und setzt deren Ende auf ``session - 1`` (der gerade archivierten Session). Lässt
    alles ab ``### ▶ Nächster Schritt`` unangetastet.
    """
    lines = next_session_text.splitlines()
    start = _find_line(lines, lambda ln: ln.startswith(STAND_HEADER_PREFIX))
    end = _find_line(lines, lambda ln: ln.startswith(NEXT_STEP_MARKER))
    if start is None:
        raise ValueError(f"Marker fehlt: keine Zeile beginnt mit {STAND_HEADER_PREFIX!r}")
    if end is None:
        raise ValueError(f"Marker fehlt: keine Zeile beginnt mit {NEXT_STEP_MARKER!r}")
    if start >= end:
        raise ValueError("Marker-Reihenfolge ungültig: Stand-Header steht nach Nächster Schritt")

    old_block = "\n".join(lines[start:end])
    range_start = _parse_range_start(old_block)
    fresh_block = (
        f"## Aktueller Stand (nach S{session}, {date})\n"
        "\n"
        "<!-- Neuen Stand hier eintragen: kurze Prosa, was lief / aktueller Zustand. -->\n"
        "\n"
        f"Frühere Sessions (S{range_start}–S{session - 1}): Verlauf in "
        "`docs/goals/ziel6.md` (Session-Historie).\n"
        "\n"
    )
    new_lines = lines[:start] + fresh_block.splitlines() + lines[end:]
    return "\n".join(new_lines) + "\n"


def _find_line(lines: list[str], predicate) -> int | None:
    for index, line in enumerate(lines):
        if predicate(line):
            return index
    return None


def _parse_range_start(block: str) -> str:
    match = _FRUEHERE_RE.search(block)
    return match.group(1) if match else _DEFAULT_RANGE_START


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="History-Rotation für den Session-Abschluss.")
    parser.add_argument(
        "--session", type=int, required=True, help="Nummer der gerade beendeten Session, z. B. 69"
    )
    parser.add_argument(
        "--summary", required=True, help="Verdichteter Einzeiler für die ziel6.md-Historie"
    )
    parser.add_argument(
        "--date", default=date_cls.today().isoformat(), help="Datum (Default: heute)"
    )
    args = parser.parse_args(argv)

    ziel6_text = ZIEL6.read_text(encoding="utf-8")
    next_text = NEXT_SESSION.read_text(encoding="utf-8")

    ZIEL6.write_text(
        append_history_line(ziel6_text, args.session, args.date, args.summary),
        encoding="utf-8",
    )
    NEXT_SESSION.write_text(
        reset_stand_block(next_text, args.session, args.date),
        encoding="utf-8",
    )
    print(f"✓ ziel6.md: S{args.session}-Zeile angehängt.")
    print(
        f"✓ next_session.md: Stand-Block auf nach-S{args.session} zurückgesetzt"
        " — neuen Stand jetzt von Hand eintragen."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
