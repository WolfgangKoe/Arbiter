"""Backlog-structure gate (INV-5): the B-NNN table/details split stays consistent.

docs/goals/backlog.md (98-Zeilen-Prioritaetstabelle) and docs/goals/backlog_details.md
(ausfuehrliche Begruendung je Item) are two halves of one artefact — a table row
whose anchor points nowhere, or a details section nobody links to, silently loses
the reason an item exists (S151-Restrukturierung). Pairs with test_doc_health.py
(line-budget pattern from CLAUDE.md) and test_correlation.py.
"""

from __future__ import annotations

import re
from pathlib import Path

_ROOT = Path(__file__).resolve().parents[2]
_BACKLOG = _ROOT / "docs" / "goals" / "backlog.md"
_DETAILS = _ROOT / "docs" / "goals" / "backlog_details.md"

# Doku-Decke-Muster wie test_doc_health.py (BRIEFING_MAX_LINES): harte Grenze weit
# ueber dem Ist-Stand (161 Zeilen S151), damit die Tabelle wachsen kann, bevor der
# Test rot wird.
BACKLOG_MAX_LINES = 200

_VALID_STATUSES = {
    "ToDo",
    "In Progress",
    "Review",
    "UI-Verifikation",
    "Blocked",
}

_STATUS_GLYPHS = ("\U0001f532", "\U0001f7e1", "\U0001f7e2")  # 🔲 🟡 🟢

_ID_RE = re.compile(r"\bB-\d{3}\b")
_TABLE_ROW_RE = re.compile(
    r"^\|\s*\[(?P<id>B-\d{3})\]\(backlog_details\.md#(?P<slug>[a-z0-9-]+)\)\s*\|"
    r"\s*(?P<status>[^|]+?)\s*\|"
)
_DETAILS_HEADING_RE = re.compile(r"^##\s+(?P<heading>B-\d{3}\s+.*)$")


def _github_slug(heading: str) -> str:
    """Reimplements GitHub's heading-to-anchor rule: lowercase, strip everything
    that is not alphanumeric/space/hyphen, spaces -> hyphens (no de-duplication of
    consecutive hyphens — GitHub does not collapse them either)."""
    slug = heading.lower()
    slug = re.sub(r"[^\w\s-]", "", slug)
    return slug.replace(" ", "-")


def _table_rows() -> list[tuple[str, str, str]]:
    lines = _BACKLOG.read_text(encoding="utf-8").splitlines()
    rows = []
    for line in lines:
        match = _TABLE_ROW_RE.match(line)
        if match:
            rows.append((match["id"], match["slug"], match["status"]))
    return rows


def _details_sections() -> list[tuple[str, str]]:
    """Returns (id, slug) pairs, one per '## B-NNN ...' heading in backlog_details.md."""
    sections = []
    for line in _DETAILS.read_text(encoding="utf-8").splitlines():
        match = _DETAILS_HEADING_RE.match(line)
        if match:
            heading = match["heading"]
            item_id = _ID_RE.search(heading).group(0)  # type: ignore[union-attr]
            sections.append((item_id, _github_slug(heading)))
    return sections


def test_backlog_within_line_budget() -> None:
    lines = _BACKLOG.read_text(encoding="utf-8").splitlines()
    assert len(lines) <= BACKLOG_MAX_LINES, (
        f"backlog.md hat {len(lines)} Zeilen (Decke {BACKLOG_MAX_LINES}). "
        "Muster wie BRIEFING_MAX_LINES in test_doc_health.py: erledigte Items nach "
        "backlog_archive.md verschieben, statt die Decke zu erhoehen."
    )


def test_every_table_id_has_exactly_one_details_section() -> None:
    table_ids = [item_id for item_id, _slug, _status in _table_rows()]
    details_ids = [item_id for item_id, _slug in _details_sections()]

    table_id_set = set(table_ids)
    details_id_set = set(details_ids)

    duplicates = sorted({i for i in details_ids if details_ids.count(i) > 1})
    missing_details = sorted(table_id_set - details_id_set)
    orphaned_details = sorted(details_id_set - table_id_set)

    assert not duplicates, f"IDs mit mehr als einem Details-Anker: {duplicates}"
    assert (
        not missing_details
    ), f"IDs in backlog.md ohne ## B-NNN Anker in backlog_details.md: {missing_details}"
    assert not orphaned_details, (
        "Details-Abschnitte ohne Tabellenzeile in backlog.md (verwaist — gehoeren "
        f"vermutlich nach backlog_archive.md): {orphaned_details}"
    )


def test_every_table_link_points_to_an_existing_details_slug() -> None:
    details_slugs = {slug for _item_id, slug in _details_sections()}
    broken = sorted(
        f"{item_id} -> #{slug}"
        for item_id, slug, _status in _table_rows()
        if slug not in details_slugs
    )
    assert not broken, (
        "Tabellen-Links in backlog.md ohne passenden Slug in backlog_details.md "
        f"(GitHub-Slug-Regel gebrochen oder Anker verschoben): {broken}"
    )


def test_backlog_status_column_uses_known_vocabulary() -> None:
    offenders = sorted(
        f"{item_id}: {status!r}"
        for item_id, _slug, status in _table_rows()
        if status not in _VALID_STATUSES
    )
    assert not offenders, (
        f"Status-Werte ausserhalb von {sorted(_VALID_STATUSES)} "
        f"('Done' ist verboten — erledigt gehoert ins Archiv): {offenders}"
    )


def test_backlog_has_no_status_glyphs() -> None:
    text = _BACKLOG.read_text(encoding="utf-8")
    found = [glyph for glyph in _STATUS_GLYPHS if glyph in text]
    assert not found, (
        f"Verbotene Status-Glyphen in backlog.md gefunden: {found} — Status gehoert "
        "ausschliesslich in die Status-Spalte als Text (s. Legende)."
    )
