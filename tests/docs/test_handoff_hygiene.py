"""Handoff hygiene gate (INV-5): docs/handoff stays a small, current mailbox.

Every handoff file declares its lifecycle status in line 1, and DONE files
must not linger: insights get merged into backlog/spec, then the file is
deleted (DoD Punkt 7). Guards against the S116-S118 drift where finished
handoffs accumulated and triggered a redundant follow-up session (S120).
Convention: docs/handoff/README.md.
"""

from __future__ import annotations

from pathlib import Path

_ROOT = Path(__file__).resolve().parents[2]
_HANDOFF_DIR = _ROOT / "docs" / "handoff"

_VALID_MARKERS = ("NEEDS-DECISION", "ANSWERED", "DONE")


def _handoff_files() -> list[Path]:
    return sorted(p for p in _HANDOFF_DIR.glob("*.md") if p.name != "README.md")


def _first_line(path: Path) -> str:
    lines = path.read_text(encoding="utf-8").splitlines()
    return lines[0] if lines else ""


def test_every_handoff_file_declares_a_valid_status_marker() -> None:
    offenders = [
        f"{path.name}: {_first_line(path)!r}"
        for path in _handoff_files()
        if not _first_line(path).startswith("STATUS:")
        or not any(marker in _first_line(path) for marker in _VALID_MARKERS)
    ]
    assert not offenders, (
        "Handoff-Dateien ohne gueltigen Status-Marker in Zeile 1 "
        f"(erwartet 'STATUS:' + {'/'.join(_VALID_MARKERS)}, "
        "s. docs/handoff/README.md): " + "; ".join(offenders)
    )


def test_no_done_handoff_lingers() -> None:
    done = [
        path.name
        for path in _handoff_files()
        if _first_line(path).startswith("STATUS:") and "DONE" in _first_line(path)
    ]
    assert not done, (
        "DONE-Handoffs gemaess Lifecycle loeschen, Erkenntnisse vorher in "
        f"Backlog/Spec ueberfuehren — DoD Punkt 7: {done}"
    )
