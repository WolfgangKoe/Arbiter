#!/usr/bin/env python3
"""Token-/„Wer leistete was"-Report — Operating-Model Phase B.

Führt den Token-Verbrauch der Haupt-Session (Orchestrator/Opus) und der
Subagenten (Sonnet/Haiku) **getrennt** zusammen, wie CLAUDE.md es verlangt.
Quelle sind die Claude-Code-Transcripts unter
``~/.claude/projects/<slug>/``:

* Haupt-Chain   : ``<slug>/<session>.jsonl``           (``isSidechain: false``)
* Subagenten    : ``<slug>/<session>/subagents/*.jsonl`` (``isSidechain: true``)

Aufruf::

    python tools/token_report.py            # Report aller Sessions nach stdout
    python tools/token_report.py --session <id>
    python tools/token_report.py --write    # docs/metrics/overview.md aktualisieren

Token-Maß je Eintrag = ``input + cache_creation + cache_read + output`` —
konsistent mit der Korridor-Definition in CLAUDE.md.
"""

from __future__ import annotations

import argparse
import json
from collections import defaultdict
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path

# Mapping von Modell-ID-Präfix auf das Tier-Label des Operating Models.
_MODEL_TIERS: tuple[tuple[str, str], ...] = (
    ("claude-opus", "Opus"),
    ("claude-sonnet", "Sonnet"),
    ("claude-haiku", "Haiku"),
    ("claude-fable", "Fable"),
)


def tier_for_model(model: str | None) -> str:
    """Ordnet eine Modell-ID dem Tier-Label zu (Fallback: die ID selbst)."""
    if not model:
        return "unbekannt"
    for prefix, label in _MODEL_TIERS:
        if model.startswith(prefix):
            return label
    return model


@dataclass(frozen=True)
class UsageRecord:
    """Ein assistant-Antwort-Eintrag mit seinem Token-Verbrauch."""

    session: str
    role: str  # "main" | "subagent"
    model: str
    input_tokens: int
    cache_creation: int
    cache_read: int
    output_tokens: int

    @property
    def total(self) -> int:
        return self.input_tokens + self.cache_creation + self.cache_read + self.output_tokens


def parse_usage_lines(lines: list[str], *, session: str, role: str) -> list[UsageRecord]:
    """Extrahiert UsageRecords aus den JSONL-Zeilen eines Transcripts.

    Reine Funktion (keine I/O) — Zeilen ohne assistant-``usage`` werden
    übersprungen, kaputte JSON-Zeilen ignoriert.
    """
    records: list[UsageRecord] = []
    for line in lines:
        line = line.strip()
        if not line:
            continue
        try:
            entry = json.loads(line)
        except json.JSONDecodeError:
            continue
        if entry.get("type") != "assistant":
            continue
        message = entry.get("message") or {}
        usage = message.get("usage")
        if not usage:
            continue
        records.append(
            UsageRecord(
                session=session,
                role=role,
                model=message.get("model") or "unbekannt",
                input_tokens=int(usage.get("input_tokens", 0)),
                cache_creation=int(usage.get("cache_creation_input_tokens", 0)),
                cache_read=int(usage.get("cache_read_input_tokens", 0)),
                output_tokens=int(usage.get("output_tokens", 0)),
            )
        )
    return records


def project_dir_for(cwd: Path) -> Path:
    """Leitet das Claude-Projekt-Transcript-Verzeichnis aus dem cwd ab."""
    slug = str(cwd).replace("/", "-")
    return Path.home() / ".claude" / "projects" / slug


def collect_records(project_dir: Path, *, session_filter: str | None = None) -> list[UsageRecord]:
    """Liest alle Haupt- und Subagent-Transcripts eines Projekts."""
    records: list[UsageRecord] = []
    for main_file in sorted(project_dir.glob("*.jsonl")):
        session = main_file.stem
        if session_filter and session != session_filter:
            continue
        records.extend(
            parse_usage_lines(
                main_file.read_text(encoding="utf-8").splitlines(),
                session=session,
                role="main",
            )
        )
        subagents_dir = project_dir / session / "subagents"
        for sub_file in sorted(subagents_dir.glob("*.jsonl")):
            records.extend(
                parse_usage_lines(
                    sub_file.read_text(encoding="utf-8").splitlines(),
                    session=session,
                    role="subagent",
                )
            )
    return records


@dataclass(frozen=True)
class Bucket:
    """Aggregierte Summe einer Gruppe von UsageRecords."""

    total: int
    output: int
    count: int


def _sum(records: list[UsageRecord]) -> Bucket:
    return Bucket(
        total=sum(r.total for r in records),
        output=sum(r.output_tokens for r in records),
        count=len(records),
    )


def summarize(records: list[UsageRecord]) -> dict:
    """Verdichtet UsageRecords zu Session- und Tier-Summen (reine Funktion)."""
    by_session: dict[str, dict[str, Bucket]] = {}
    by_tier: dict[str, Bucket] = {}

    sessions: dict[str, dict[str, list[UsageRecord]]] = defaultdict(
        lambda: {"main": [], "subagent": []}
    )
    tiers: dict[str, list[UsageRecord]] = defaultdict(list)
    for record in records:
        sessions[record.session][record.role].append(record)
        tiers[tier_for_model(record.model)].append(record)

    for session, by_role in sessions.items():
        by_session[session] = {
            "main": _sum(by_role["main"]),
            "subagent": _sum(by_role["subagent"]),
        }
    for tier, tier_records in tiers.items():
        by_tier[tier] = _sum(tier_records)

    return {
        "by_session": by_session,
        "by_tier": by_tier,
        "grand_total": _sum(records),
    }


def _fmt(value: int) -> str:
    """1234567 -> '1,234,567' (Tausender-Trenner für Lesbarkeit)."""
    return f"{value:,}"


def _escape_label(label: str) -> str:
    """Macht Tier-Labels Markdown-sicher (z. B. ``<synthetic>``)."""
    return label.replace("<", "&lt;").replace(">", "&gt;")


def render_markdown(summary: dict, *, generated_at: str) -> str:
    """Rendert die Zusammenfassung als Markdown-Report (Leitstand-Feld 4)."""
    lines: list[str] = [
        "# Token-Report — Wer leistete was",
        "",
        "<!-- Generiert von tools/token_report.py — nicht von Hand pflegen. -->",
        f"Stand: {generated_at}",
        "",
        "Haupt-Session (Orchestrator) und Subagenten **getrennt** ausgewiesen.",
        "Token-Maß = input + cache_creation + cache_read + output.",
        "",
        "## Summe je Modell-Tier",
        "",
        "| Tier | Antworten | Output-Token | Gesamt-Token |",
        "|---|---:|---:|---:|",
    ]
    for tier in sorted(summary["by_tier"], key=lambda t: -summary["by_tier"][t].total):
        bucket = summary["by_tier"][tier]
        lines.append(
            f"| {_escape_label(tier)} | {_fmt(bucket.count)} | {_fmt(bucket.output)} "
            f"| {_fmt(bucket.total)} |"
        )
    grand = summary["grand_total"]
    lines.append(
        f"| **Σ** | **{_fmt(grand.count)}** | **{_fmt(grand.output)}** "
        f"| **{_fmt(grand.total)}** |"
    )

    lines += [
        "",
        "## Je Session — Haupt vs. Subagent",
        "",
        "| Session | Haupt (gesamt) | Subagent (gesamt) | Subagent-Anteil |",
        "|---|---:|---:|---:|",
    ]
    for session in sorted(summary["by_session"]):
        roles = summary["by_session"][session]
        main_total = roles["main"].total
        sub_total = roles["subagent"].total
        combined = main_total + sub_total
        share = f"{sub_total / combined * 100:.1f} %" if combined else "—"
        lines.append(f"| `{session[:8]}` | {_fmt(main_total)} | {_fmt(sub_total)} " f"| {share} |")
    lines.append("")
    return "\n".join(lines)


_OUTPUT_DOC = Path("docs/metrics/overview.md")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--session", help="Nur diese Session-ID auswerten (Default: alle).")
    parser.add_argument(
        "--write",
        action="store_true",
        help=f"Report nach {_OUTPUT_DOC} schreiben (sonst stdout).",
    )
    parser.add_argument(
        "--project-dir",
        type=Path,
        help="Transcript-Verzeichnis überschreiben (Default: aus cwd abgeleitet).",
    )
    args = parser.parse_args(argv)

    project_dir = args.project_dir or project_dir_for(Path.cwd())
    if not project_dir.is_dir():
        parser.error(f"Transcript-Verzeichnis nicht gefunden: {project_dir}")

    records = collect_records(project_dir, session_filter=args.session)
    summary = summarize(records)
    generated_at = datetime.now(UTC).strftime("%Y-%m-%d %H:%M UTC")
    report = render_markdown(summary, generated_at=generated_at)

    if args.write:
        _OUTPUT_DOC.parent.mkdir(parents=True, exist_ok=True)
        _OUTPUT_DOC.write_text(report + "\n", encoding="utf-8")
        print(f"Report geschrieben: {_OUTPUT_DOC}")
    else:
        print(report)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
