#!/usr/bin/env python3
"""PreToolUse hook: hard Freigabe-Gate for Edit/Write/NotebookEdit.

The operating model's "Freigabe vor Umsetzung" rule was prose Claude had to
remember; this turns it into a harness-enforced trigger. A PreToolUse hook
cannot read whether the stakeholder said "ja" in chat, so approval is expressed
*physically*: the marker file ``.claude/.freigabe``.

* Marker present  -> allow the edit (exit 0).
* Marker absent   -> deny the edit (exit 2 + reason on stderr), which blocks the
                     tool call and feeds the reason back to Claude.

A SessionStart hook removes the marker each session, so the gate re-arms every
session instead of decaying into "always open". The stakeholder re-grants with
``touch .claude/.freigabe`` after a plan is approved.

Known gap: only Edit/Write/NotebookEdit are gated. File writes via Bash
(``>``, ``sed -i`` ...) are out of scope by design — gating all Bash would block
reads and pytest.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

MARKER = Path(__file__).resolve().parent.parent / ".claude" / ".freigabe"

DENY_REASON = (
    "🔒 Freigabe-Gate aktiv: kein freigegebener Plan. Zeige dem Stakeholder "
    "Plan + betroffene Dateien und warte auf Freigabe. Freigabe erfolgt "
    "physisch mit `touch .claude/.freigabe` (re-armt automatisch bei "
    "Session-Start). NICHT selbst den Marker setzen."
)


def is_allowed(marker: Path) -> bool:
    """Edits are allowed exactly while the Freigabe marker exists."""
    return marker.exists()


def main() -> None:
    # Never break the harness on malformed input — fail open is unsafe for a
    # gate, so fail *closed* would block everything; instead, on parse failure
    # we allow, because a broken gate must not wedge the session. The marker
    # check below is the actual enforcement path.
    try:
        json.load(sys.stdin)  # consume payload; matcher already scoped the tool
    except Exception:
        return
    if is_allowed(MARKER):
        return
    print(DENY_REASON, file=sys.stderr)
    sys.exit(2)


if __name__ == "__main__":
    main()
