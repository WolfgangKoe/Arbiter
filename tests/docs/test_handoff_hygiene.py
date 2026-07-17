"""Handoff hygiene gate (INV-5): docs/handoff stays a small, current mailbox.

Every handoff file declares its lifecycle status in line 1, and DONE/ANSWERED
files must not linger: insights get merged into backlog/spec, then the file
is deleted in the same Abschluss (DoD Punkt 7; S156-Retro Maßnahme 7 widened
the guard from DONE-only to both transit markers). Guards against the
S116-S118 drift where finished handoffs accumulated and triggered a
redundant follow-up session (S120). Convention: docs/handoff/README.md.
"""

from __future__ import annotations

from pathlib import Path

_ROOT = Path(__file__).resolve().parents[2]
_HANDOFF_DIR = _ROOT / "docs" / "handoff"

_VALID_MARKERS = (
    # NEEDS-APPROVAL: Planning-Datei der laufenden Session (Plan vorgelegt/freigegeben);
    # wird beim Session-Abschluss auf ANSWERED gesetzt und geloescht (S157).
    "NEEDS-APPROVAL",
    "NEEDS-DECISION",
    "ANSWERED",
    "DONE",
    # STANDING: dauerhafte Datei (Eingangskanal), Inhalt wird ueberfuehrt,
    # die Datei selbst bleibt bestehen (S134-Stakeholder-Entscheid).
    "STANDING",
    # AWAITING-VERIFICATION: wartet auf manuelle Stakeholder-Sichtpruefung eines
    # UI-Effekts (DoD Punkt 6) — keine Entscheidungsfrage, ersetzt die bisherige
    # Fehlnutzung von NEEDS-DECISION dafuer (Retro-M1, S160/S161).
    "AWAITING-VERIFICATION",
)


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


_STALE_MARKERS = ("DONE", "ANSWERED")


def test_no_done_or_answered_handoff_lingers() -> None:
    stale = [
        path.name
        for path in _handoff_files()
        if _first_line(path).startswith("STATUS:")
        and any(marker in _first_line(path) for marker in _STALE_MARKERS)
    ]
    assert not stale, (
        "DONE-/ANSWERED-Handoffs sind Durchgangszustaende — im selben Abschluss "
        "loeschen, Erkenntnisse vorher in Backlog/Spec ueberfuehren "
        f"(DoD Punkt 7, S156-Retro Massnahme 7): {stale}"
    )


def test_awaiting_verification_is_a_valid_marker() -> None:
    assert "AWAITING-VERIFICATION" in _VALID_MARKERS


def test_awaiting_verification_is_not_treated_as_stale() -> None:
    assert "AWAITING-VERIFICATION" not in _STALE_MARKERS
