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

Exempt: writes under ``docs/handoff/`` (the ADR-0007 mailbox). That directory is
a planning/coordination artifact, not code — the NEEDS-DECISION round-trip that
*produces* the Freigabe happens before any plan is approved, so gating it would
deadlock the very mechanism that grants approval. Code paths stay gated.

Known gap: only Edit/Write/NotebookEdit are gated. File writes via Bash
(``>``, ``sed -i`` ...) are out of scope by design — gating all Bash would block
reads and pytest.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
MARKER = REPO_ROOT / ".claude" / ".freigabe"
HANDOFF_DIR = REPO_ROOT / "docs" / "handoff"

DENY_REASON = (
    "🔒 Freigabe-Gate aktiv: kein freigegebener Plan. Zeige dem Stakeholder "
    "Plan + betroffene Dateien und warte auf Freigabe. Freigabe erfolgt "
    "physisch mit `touch .claude/.freigabe` (re-armt automatisch bei "
    "Session-Start). NICHT selbst den Marker setzen."
)


def is_allowed(marker: Path) -> bool:
    """Edits are allowed exactly while the Freigabe marker exists."""
    return marker.exists()


def is_exempt(file_path: str | None) -> bool:
    """Mailbox writes (``docs/handoff/``) and anything outside the repo bypass
    the gate. The gate protects the repo; scratchpad drafts (e.g. Planner
    output under ``/tmp/claude-*``) are coordination artifacts, not code —
    blocking them forced Plan-Entwürfe inline in den Chat (S130-Retro, M3)."""
    if not file_path:
        return False
    try:
        resolved = Path(file_path).resolve()
    except Exception:
        return False
    if resolved == HANDOFF_DIR or HANDOFF_DIR in resolved.parents:
        return True
    return REPO_ROOT not in resolved.parents and resolved != REPO_ROOT


def main() -> None:
    # Never break the harness on malformed input — fail open is unsafe for a
    # gate, so fail *closed* would block everything; instead, on parse failure
    # we allow, because a broken gate must not wedge the session. The marker
    # check below is the actual enforcement path.
    try:
        payload = json.load(sys.stdin)
    except Exception:
        return
    file_path = (payload.get("tool_input") or {}).get("file_path")
    if is_exempt(file_path):
        return
    if is_allowed(MARKER):
        return
    print(DENY_REASON, file=sys.stderr)
    sys.exit(2)


if __name__ == "__main__":
    main()
