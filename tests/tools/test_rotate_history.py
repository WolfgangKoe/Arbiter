"""History-Rotation am Session-Abschluss (tools/rotate_history.py)."""

import pytest

from tools.rotate_history import append_history_line, reset_stand_block

_NEXT_SESSION_SAMPLE = """# Startprompt — Nächste Session

## Aktueller Stand (nach S68, 2026-06-20)

Alter Stand-Text, der beim Reset verschwinden soll.

Frühere Sessions (S60–S67): Verlauf in `docs/metrics/session_archive.md` (Session-Historie).

### ▶ Nächster Schritt — frei wählbar
1. Etwas, das erhalten bleiben muss.

## Gate-Netz
- bleibt ebenfalls erhalten.
"""


def test_append_adds_formatted_line_at_end():
    text = "## Session-Historie\n\n- **S67 (2026-06-20)** vorher.\n"
    result = append_history_line(text, 68, "2026-06-21", "neue Zusammenfassung")
    assert result.endswith("- **S68 (2026-06-21)** neue Zusammenfassung\n")


def test_append_preserves_existing_content():
    text = "- **S67 (2026-06-20)** vorher.\n"
    result = append_history_line(text, 68, "2026-06-21", "neu")
    assert "- **S67 (2026-06-20)** vorher." in result


def test_append_strips_summary_whitespace_and_single_trailing_newline():
    result = append_history_line("- **S67** x.\n\n\n", 68, "2026-06-21", "  neu  ")
    assert result.endswith("** neu\n")
    assert not result.endswith("\n\n")


def test_reset_replaces_old_stand_prose():
    result = reset_stand_block(_NEXT_SESSION_SAMPLE, 69, "2026-06-21")
    assert "Alter Stand-Text" not in result
    assert "## Aktueller Stand (nach S69, 2026-06-21)" in result


def test_reset_bumps_fruehere_range_end_to_prior_session_and_keeps_start():
    result = reset_stand_block(_NEXT_SESSION_SAMPLE, 69, "2026-06-21")
    assert "Frühere Sessions (S60–S68):" in result


def test_reset_keeps_everything_from_next_step_onward():
    result = reset_stand_block(_NEXT_SESSION_SAMPLE, 69, "2026-06-21")
    assert "### ▶ Nächster Schritt — frei wählbar" in result
    assert "Etwas, das erhalten bleiben muss." in result
    assert "## Gate-Netz" in result
    assert "bleibt ebenfalls erhalten." in result


def test_reset_raises_when_stand_header_missing():
    with pytest.raises(ValueError, match="Aktueller Stand"):
        reset_stand_block("# Titel\n\n### ▶ Nächster Schritt\n- x\n", 69, "2026-06-21")


def test_reset_raises_when_next_step_marker_missing():
    with pytest.raises(ValueError, match="Nächster Schritt"):
        reset_stand_block("## Aktueller Stand (nach S68, x)\n\nProsa.\n", 69, "2026-06-21")


def test_reset_defaults_range_start_when_no_fruehere_line():
    text = (
        "## Aktueller Stand (nach S68, x)\n\nProsa ohne Frühere-Zeile.\n\n"
        "### ▶ Nächster Schritt\n- x\n"
    )
    result = reset_stand_block(text, 69, "2026-06-21")
    assert "Frühere Sessions (S60–S68):" in result
