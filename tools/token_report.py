#!/usr/bin/env python3
"""Token-Report — Effizienz statt Menge (Operating-Model Phase B, v3).

Beantwortet die Stakeholder-Frage *"wurden die Token gut ausgegeben, werden wir
besser oder schlechter?"* — nicht bloße Mengen, sondern Effizienz und Trend.
Quelle sind die Claude-Code-Transcripts unter ``~/.claude/projects/<slug>/``:

* Haupt-Chain : ``<slug>/<session>.jsonl``            (Orchestrator, Opus)
* Subagenten  : ``<slug>/<session>/subagents/*.jsonl`` (Sonnet/Haiku, isoliert)

Der Report hat fünf Teile (ADR-0002, leser-orientiert):

1. **Fokus letzte Session** — Aufgabe, Modelle je Rolle, Peak-Kontext vs. 150k,
   Subagent-Anteil, plus ein Zusammensetzungs-Balken (input/cache_creation/
   cache_read/output).
2. **Verlauf (letzte 6 Sessions)** — je Session theme-sichere Unicode-Balken für
   Peak-Kontext, Subagent-Anteil und Modell-Mix, jeweils mit Trend ↑/↓.
3. **Hinweise** — auto-generiert (Korridor-Überschreitung, Subagent-Last, Tiering).
4. **Subagenten** — Session · Modell · Agent · Aufgabe.

Aufruf::

    python tools/token_report.py            # Report aller Sessions nach stdout
    python tools/token_report.py --session <id>
    python tools/token_report.py --write    # docs/metrics/overview.md aktualisieren

Token-Maß je Antwort = ``input + cache_creation + cache_read + output``.
Peak-Kontext je Session = ``max(input + cache_read + cache_creation)`` über die
Haupt-Antworten (das ist das Fenster, das der 150k-Korridor begrenzt).
"""

from __future__ import annotations

import argparse
import json
from collections import defaultdict
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

# Zeitstempel in lokaler Zeit (Europe/Berlin = CET/CEST, DST-korrekt) statt UTC,
# damit die Overview-Zeiten zur Wanduhr des Stakeholders passen (S78).
_LOCAL_TZ = ZoneInfo("Europe/Berlin")

# Kontext-Korridor aus CLAUDE.md — Bezugsgröße für Peak-Kontext und Hinweise.
CONTEXT_LIMIT = 150_000

# Client-seitige Fehler-/Interrupt-Stubs (z. B. „API Error: 529 Overloaded")
# tragen dieses Pseudo-Modell und Null-Usage — kein echter LLM-Call. Sie dürfen
# nicht als Antwort zählen, sonst erscheint eine Geister-Session mit 0k-Peak.
SYNTHETIC_MODEL = "<synthetic>"

# Mapping von Modell-ID-Präfix auf das Tier-Label des Operating Models.
_MODEL_TIERS: tuple[tuple[str, str], ...] = (
    ("claude-opus", "Opus"),
    ("claude-sonnet", "Sonnet"),
    ("claude-haiku", "Haiku"),
    ("claude-fable", "Fable"),
)

# Modell-Mix-Balken: feste Zeichen je Tier (theme-sicher, keine Farb-Legende).
# Opus █ vs. Sonnet · = starker Kontrast für die beiden häufigsten Tiers.
_MIX_CHARS: tuple[tuple[str, str], ...] = (
    ("Opus", "█"),
    ("Sonnet", "·"),
    ("Haiku", "▒"),
)
_MIX_OTHER = "▓"

# Wrapper-Tags, die keine echte Nutzer-Aufgabe sind (Slash-Kommandos, IDE-Kontext).
_WRAPPER_TAGS: tuple[str, ...] = (
    "local-command-caveat",
    "command-name",
    "command-message",
    "command-args",
    "command-stdout",
    "ide_selection",
    "ide_opened_file",
    "system-reminder",
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

    @property
    def context(self) -> int:
        """Belegtes Kontextfenster dieser Antwort (ohne neuen Output)."""
        return self.input_tokens + self.cache_read + self.cache_creation


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
        if message.get("model") == SYNTHETIC_MODEL:
            continue
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


def parse_first_timestamp(lines: list[str]) -> str | None:
    """Liefert den ``timestamp`` des ersten Eintrags (Session-Startzeit)."""
    for line in lines:
        line = line.strip()
        if not line:
            continue
        try:
            entry = json.loads(line)
        except json.JSONDecodeError:
            continue
        timestamp = entry.get("timestamp")
        if timestamp:
            return timestamp
    return None


def _user_text(entry: dict) -> str:
    """Reiner Text einer user-Nachricht (verbindet text-Blöcke, ignoriert Tools)."""
    content = (entry.get("message") or {}).get("content")
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        return " ".join(
            block.get("text", "")
            for block in content
            if isinstance(block, dict) and block.get("type") == "text"
        )
    return ""


def _is_wrapper(text: str) -> bool:
    """Erkennt Slash-Kommando-/IDE-/System-Wrapper statt echter Nutzer-Eingabe."""
    return text.startswith("<") and any(tag in text[:40] for tag in _WRAPPER_TAGS)


def parse_first_user_task(lines: list[str], *, max_len: int = 120) -> str | None:
    """Die erste echte Nutzer-Aufgabe einer Session (Wrapper-Zeilen übersprungen)."""
    for line in lines:
        line = line.strip()
        if not line:
            continue
        try:
            entry = json.loads(line)
        except json.JSONDecodeError:
            continue
        if entry.get("type") != "user" or entry.get("isMeta"):
            continue
        text = _user_text(entry).strip()
        if not text or _is_wrapper(text):
            continue
        text = " ".join(text.split())
        return text if len(text) <= max_len else text[: max_len - 1].rstrip() + "…"
    return None


@dataclass(frozen=True)
class Subagent:
    """Ein gestarteter Subagent: Typ, Aufgabe, Modell-Tier und Peak-Kontext."""

    agent_type: str
    description: str
    tier: str
    peak_context: int | None = None


def _first_model(jsonl_path: Path) -> str | None:
    """Modell-ID aus der ersten assistant-Antwort eines Transcripts."""
    if not jsonl_path.is_file():
        return None
    for line in jsonl_path.read_text(encoding="utf-8").splitlines():
        try:
            entry = json.loads(line)
        except json.JSONDecodeError:
            continue
        if entry.get("type") == "assistant":
            model = (entry.get("message") or {}).get("model")
            if model:
                return model
    return None


def _subagent_peak_context(jsonl_path: Path) -> int | None:
    """Peak-Kontext aus einem Subagenten-Transcript (None wenn fehlend/unlesbar)."""
    if not jsonl_path.is_file():
        return None
    try:
        lines = jsonl_path.read_text(encoding="utf-8").splitlines()
    except OSError:
        return None
    records = parse_usage_lines(lines, session="", role="subagent")
    if not records:
        return None
    return max(r.context for r in records)


def read_subagents(subagents_dir: Path) -> list[Subagent]:
    """Liest (Typ, Aufgabe, Tier, Peak-Kontext) je Subagent aus ``*.meta.json`` + ``*.jsonl``."""
    subagents: list[Subagent] = []
    if not subagents_dir.is_dir():
        return subagents
    for meta_file in sorted(subagents_dir.glob("*.meta.json")):
        try:
            data = json.loads(meta_file.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            continue
        jsonl_path = meta_file.with_suffix("").with_suffix(".jsonl")
        subagents.append(
            Subagent(
                agent_type=data.get("agentType") or "?",
                description=data.get("description") or "",
                tier=tier_for_model(_first_model(jsonl_path)),
                peak_context=_subagent_peak_context(jsonl_path),
            )
        )
    return subagents


@dataclass(frozen=True)
class SessionMeta:
    """Lesbare Begleitdaten einer Session (Startzeit, Aufgabe, Subagenten)."""

    started_at: str | None
    task: str | None
    subagents: list[Subagent]


def collect_project(
    project_dir: Path, *, session_filter: str | None = None
) -> tuple[list[UsageRecord], dict[str, SessionMeta]]:
    """Liest Records + Metadaten aller Sessions eines Projekts."""
    records: list[UsageRecord] = []
    meta: dict[str, SessionMeta] = {}
    for main_file in sorted(project_dir.glob("*.jsonl")):
        session = main_file.stem
        if session_filter and session != session_filter:
            continue
        main_lines = main_file.read_text(encoding="utf-8").splitlines()
        records.extend(parse_usage_lines(main_lines, session=session, role="main"))
        subagents_dir = project_dir / session / "subagents"
        for sub_file in sorted(subagents_dir.glob("*.jsonl")):
            records.extend(
                parse_usage_lines(
                    sub_file.read_text(encoding="utf-8").splitlines(),
                    session=session,
                    role="subagent",
                )
            )
        meta[session] = SessionMeta(
            started_at=parse_first_timestamp(main_lines),
            task=parse_first_user_task(main_lines),
            subagents=read_subagents(subagents_dir),
        )
    return records, meta


@dataclass(frozen=True)
class Bucket:
    """Aggregierte Token-Zusammensetzung einer Gruppe von UsageRecords."""

    input: int = 0
    cache_creation: int = 0
    cache_read: int = 0
    output: int = 0
    count: int = 0

    @property
    def total(self) -> int:
        return self.input + self.cache_creation + self.cache_read + self.output

    def __add__(self, other: Bucket) -> Bucket:
        return Bucket(
            input=self.input + other.input,
            cache_creation=self.cache_creation + other.cache_creation,
            cache_read=self.cache_read + other.cache_read,
            output=self.output + other.output,
            count=self.count + other.count,
        )


def _sum(records: list[UsageRecord]) -> Bucket:
    return Bucket(
        input=sum(r.input_tokens for r in records),
        cache_creation=sum(r.cache_creation for r in records),
        cache_read=sum(r.cache_read for r in records),
        output=sum(r.output_tokens for r in records),
        count=len(records),
    )


def _tier_totals(records: list[UsageRecord]) -> dict[str, int]:
    totals: dict[str, int] = defaultdict(int)
    for record in records:
        totals[tier_for_model(record.model)] += record.total
    return dict(totals)


@dataclass(frozen=True)
class SessionSummary:
    """Verdichtete Effizienz-Kennzahlen einer Session (reine Aggregation)."""

    session: str
    main: Bucket
    subagent: Bucket
    main_by_tier: dict[str, int] = field(default_factory=dict)
    sub_by_tier: dict[str, int] = field(default_factory=dict)
    peak_context: int = 0
    answers: int = 0
    over_limit: int = 0

    @property
    def combined(self) -> Bucket:
        return self.main + self.subagent

    @property
    def subagent_share(self) -> float:
        total = self.combined.total
        return self.subagent.total / total * 100 if total else 0.0

    @property
    def by_tier(self) -> dict[str, int]:
        merged: dict[str, int] = dict(self.main_by_tier)
        for tier, value in self.sub_by_tier.items():
            merged[tier] = merged.get(tier, 0) + value
        return merged


def summarize(records: list[UsageRecord]) -> dict:
    """Verdichtet UsageRecords je Session zu Effizienz-Kennzahlen (reine Funktion)."""
    sessions: dict[str, dict[str, list[UsageRecord]]] = defaultdict(
        lambda: {"main": [], "subagent": []}
    )
    for record in records:
        sessions[record.session][record.role].append(record)

    by_session: dict[str, SessionSummary] = {}
    for session, by_role in sessions.items():
        main_records = by_role["main"]
        contexts = [r.context for r in main_records]
        by_session[session] = SessionSummary(
            session=session,
            main=_sum(main_records),
            subagent=_sum(by_role["subagent"]),
            main_by_tier=_tier_totals(main_records),
            sub_by_tier=_tier_totals(by_role["subagent"]),
            peak_context=max(contexts, default=0),
            answers=len(main_records),
            over_limit=sum(1 for c in contexts if c > CONTEXT_LIMIT),
        )

    return {
        "sessions": by_session,
        "grand_total": _sum(records),
    }


# --------------------------------------------------------------------------- #
# Formatierung                                                                 #
# --------------------------------------------------------------------------- #


def _fmt(value: int) -> str:
    """1234567 -> '1,234,567' (Tausender-Trenner für Lesbarkeit)."""
    return f"{value:,}"


def _k(value: int) -> str:
    """132456 -> '132k' (kompaktes Balken-Label)."""
    return f"{round(value / 1000)}k"


def _escape_label(label: str) -> str:
    """Macht Labels Markdown-sicher (z. B. ``<synthetic>``)."""
    return label.replace("<", "&lt;").replace(">", "&gt;")


def _cell(text: str) -> str:
    """Sanitisiert freien Text für eine Tabellenzelle (kein Pipe/Umbruch)."""
    return _escape_label(text).replace("|", "\\|").replace("\n", " ").strip()


def bar(value: int, maximum: int, *, width: int = 12, fill: str = "█", empty: str = "░") -> str:
    """Theme-sicherer Unicode-Balken: gefüllter Anteil ``value/maximum``."""
    if maximum <= 0:
        return empty * width
    filled = max(0, min(width, round(value / maximum * width)))
    return fill * filled + empty * (width - filled)


def model_mix_bar(by_tier: dict[str, int], *, width: int = 12) -> str:
    """Segmentierter Balken nach Tier-Anteil (█ Opus · · Sonnet · ▒ Haiku · ▓ Rest)."""
    total = sum(by_tier.values())
    if total <= 0:
        return _MIX_OTHER * width
    known = [tier for tier, _ in _MIX_CHARS if by_tier.get(tier)]
    others = [tier for tier in by_tier if tier not in dict(_MIX_CHARS) and by_tier[tier]]
    order = known + others
    char = dict(_MIX_CHARS)

    raw = {tier: by_tier[tier] / total * width for tier in order}
    widths = {tier: int(raw[tier]) for tier in order}
    remainder = width - sum(widths.values())
    for tier in sorted(order, key=lambda t: raw[t] - widths[t], reverse=True)[:remainder]:
        widths[tier] += 1
    return "".join(char.get(tier, _MIX_OTHER) * widths[tier] for tier in order)


def trend(current: float | None, previous: float | None, *, tolerance: float = 0.0) -> str:
    """↑/↓/→ gegenüber der davorliegenden Session (— ohne Vergleichswert)."""
    if current is None or previous is None:
        return "—"
    if current > previous + tolerance:
        return "↑"
    if current < previous - tolerance:
        return "↓"
    return "→"


def session_label(session_id: str, started_at: str | None) -> str:
    """Lesbares Label: Datum + Uhrzeit, sonst die gekürzte Session-ID."""
    short = session_id[:8]
    if not started_at:
        return short
    try:
        when = datetime.fromisoformat(started_at.replace("Z", "+00:00")).astimezone(_LOCAL_TZ)
    except ValueError:
        return short
    return f"{when:%Y-%m-%d %H:%M} · {short}"


def _short_label(session_id: str, started_at: str | None) -> str:
    """Kompaktes Label für die Verlaufstabelle (MM-TT HH:MM · Kurz-ID)."""
    short = session_id[:4]
    if not started_at:
        return short
    try:
        when = datetime.fromisoformat(started_at.replace("Z", "+00:00")).astimezone(_LOCAL_TZ)
    except ValueError:
        return short
    return f"{when:%m-%d %H:%M} {short}"


def _sessions_newest_first(summary: dict, meta: dict[str, SessionMeta]) -> list[str]:
    """Session-IDs nach Startzeit absteigend (jüngste zuerst); ohne Zeit ans Ende."""
    return sorted(
        summary["sessions"],
        key=lambda s: (meta.get(s, _EMPTY_META).started_at or "", s),
        reverse=True,
    )


_EMPTY_META = SessionMeta(None, None, [])


def generate_hints(session: SessionSummary) -> list[str]:
    """Auto-Hinweise zur jüngsten Session (Korridor, Subagent-Last, Tiering)."""
    hints: list[str] = []

    if session.over_limit:
        hints.append(
            f"⚠️ {session.over_limit} von {session.answers} Antworten lagen über dem "
            f"150k-Korridor — Session früher schneiden."
        )
    elif session.peak_context > 0.9 * CONTEXT_LIMIT:
        hints.append(
            f"⚠️ Peak-Kontext {_k(session.peak_context)} nahe am 150k-Korridor (>90 %) — "
            f"geordnet beenden und frisch starten."
        )
    else:
        hints.append(f"✅ Peak-Kontext {_k(session.peak_context)} blieb im 150k-Korridor.")

    share = session.subagent_share
    if share >= 30:
        hints.append(
            f"✅ {share:.0f}% der Token liefen über Subagenten — das Hauptfenster blieb schlank."
        )
    elif session.subagent.total == 0 and session.peak_context > 0.5 * CONTEXT_LIMIT:
        hints.append(
            "💡 Große Session ohne Subagent — mechanische Fleißarbeit ließe sich an "
            "Sonnet/Haiku auslagern (CLAUDE.md, Tiering)."
        )

    low_tier = sum(v for t, v in session.by_tier.items() if t in ("Sonnet", "Haiku"))
    if low_tier:
        hints.append(
            f"✅ {_fmt(low_tier)} Token auf günstigeren Tiers (Sonnet/Haiku) — gutes Tiering."
        )
    return hints


def _render_focus(session: SessionSummary, meta: SessionMeta, *, link: str | None) -> list[str]:
    """Abschnitt 'Jüngste Session' — nur Stats-Block (kein Balken-Block)."""
    label = session_label(session.session, meta.started_at)
    task = meta.task or "—"
    if link:
        task = f"{task} ([Backlog]({link}))"
    main_tiers = ", ".join(sorted(session.main_by_tier)) or "—"
    sub_tiers = ", ".join(sorted(session.sub_by_tier)) or "—"
    combined = session.combined

    return [
        "## Jüngste Session",
        "",
        f"**{_escape_label(label)}**",
        "",
        f"- **Aufgabe:** {_cell(task)}",
        f"- **Modelle:** Haupt {main_tiers} · Subagent {sub_tiers}",
        f"- **Tokens gesamt:** {_fmt(combined.total)} "
        f"(Haupt {_fmt(session.main.total)} · Subagent {_fmt(session.subagent.total)}, "
        f"Anteil {session.subagent_share:.0f} %)",
        f"- **Peak-Kontext:** {bar(session.peak_context, CONTEXT_LIMIT)} "
        f"{_k(session.peak_context)} / 150k",
        f"- **cache_read:** {_fmt(combined.cache_read)} · **Output:** {_fmt(combined.output)}",
        "",
    ]


def _render_composition(session: SessionSummary) -> list[str]:
    """Abschnitt 'Zusammensetzung der Antworten' — Balken-Block + Legende."""
    combined = session.combined
    parts = (
        ("input", combined.input),
        ("cache_creation", combined.cache_creation),
        ("cache_read", combined.cache_read),
        ("output", combined.output),
    )
    peak = max((value for _, value in parts), default=0)
    total = combined.total or 1

    lines: list[str] = [
        "## Zusammensetzung der Antworten",
        "",
        "```text",
    ]
    for name, value in parts:
        share = value / total * 100
        lines.append(
            f"{name:<15}▕{bar(value, peak, width=24, empty='░')}▏ {share:>4.0f}%  {_fmt(value)}"
        )
    lines += [
        "```",
        "",
        "**Legende & Zielwerte:**",
        "",
        "- **input** — neue, ungecachte Tokens → niedrig halten.",
        "- **cache_creation** — erstmals gecacht (einmalig teurer) → moderat, unvermeidbar "
        "bei neuem Kontext.",
        "- **cache_read** — aus warmem Cache gelesen (günstig) → **hoher Anteil = gut** "
        "(Kontext bleibt warm, Cache-TTL ~5 Min).",
        "- **output** — generierte Tokens; **kein Selbstzweck — Qualität vor Menge.** Ein "
        "höherer Output-Anteil *relativ zu* cache_read kann Ziele schneller erreichen, "
        "*sofern das Ergebnis trägt*; viel cache_read bei wenig substanziellem Output = "
        'Reibung, "Mist"-Output ist schädlich, nicht gut.',
        "",
        "**Zielbild:** hoher cache_read-Anteil + niedriger input-Anteil = effizientes "
        "Arbeiten; Output bewusst gegen Qualität gewichtet (nicht maximieren). Viele "
        "Cache-Misses (hoher input nach Pausen > 5 Min) sind ein Warnsignal.",
        "",
    ]
    return lines


def _render_history(ordered: list[str], summary: dict, meta: dict[str, SessionMeta]) -> list[str]:
    """Abschnitt "Verlauf"" — Balken + Trend je Session (älteste als Vergleich)."""
    sessions = summary["sessions"]
    # Trend braucht die jeweils ältere Session — über die volle Liste rechnen.
    peak = {s: sessions[s].peak_context for s in ordered}
    share = {s: sessions[s].subagent_share for s in ordered}

    lines = [
        "## Verlauf (letzte 6 Sessions)",
        "",
        "Jüngste zuerst. Balken theme-sicher (Unicode); Trend ↑/↓ ggü. der älteren Session.",
        "Modell-Mix: `█` Opus · `·` Sonnet · `▒` Haiku · `▓` sonstige.",
        "",
        "```text",
        f"{'Session':<17} {'Peak-Kontext':<22} {'Subagent':<14} {'Modell-Mix':<12}",
        f"{'-' * 17} {'-' * 22} {'-' * 14} {'-' * 12}",
    ]
    for index, session in enumerate(ordered[:6]):
        summ = sessions[session]
        older = ordered[index + 1] if index + 1 < len(ordered) else None
        peak_trend = trend(peak[session], peak[older] if older else None)
        share_trend = trend(share[session], share[older] if older else None)
        label = _short_label(session, meta.get(session, _EMPTY_META).started_at)
        peak_col = (
            f"{bar(summ.peak_context, CONTEXT_LIMIT)} {_k(summ.peak_context):>4} {peak_trend}"
        )
        share_bar = bar(round(summ.subagent_share), 100, width=6)
        share_col = f"{share_bar} {summ.subagent_share:>3.0f}% {share_trend}"
        mix_col = model_mix_bar(summ.by_tier)
        lines.append(f"{label:<17} {peak_col:<22} {share_col:<14} {mix_col:<12}")
    lines += ["```", ""]
    return lines


def _render_hints(session: SessionSummary) -> list[str]:
    lines = ["## (Retro-)Hinweise", "", "_Auto-generiert zur jüngsten Session._", ""]
    lines += [f"- {hint}" for hint in generate_hints(session)]
    lines.append("")
    return lines


def _context_status(peak: int | None) -> str:
    """✅/⚠️/⛔ je nach Peak-Kontext im 150k-Korridor (— wenn unbekannt)."""
    if peak is None:
        return "—"
    if peak >= CONTEXT_LIMIT:
        return "⛔"
    if peak >= round(0.8 * CONTEXT_LIMIT):
        return "⚠️"
    return "✅"


def _render_subagent_corridor(latest_meta: SessionMeta) -> list[str]:
    """Abschnitt "150k-Korridor für Subagenten" für die jüngste Session."""
    lines = [
        "## 150k-Korridor für Subagenten",
        "",
        "_Peak-Kontext je Subagent der letzten Session (selbe Metrik wie Haupt-Peak)._",
        "",
    ]
    if not latest_meta.subagents:
        lines += ["_keine Subagenten in der letzten Session._", ""]
        return lines
    lines.append("```text")
    lines.append(f"{'#':<3} {'Agent / Aufgabe':<35} {'Peak-Kontext / 150k':<20} {'Status'}")
    lines.append(f"{'-' * 3} {'-' * 35} {'-' * 20} {'-' * 6}")
    for index, sub in enumerate(latest_meta.subagents, start=1):
        label = f"{sub.agent_type}: {sub.description}"
        if len(label) > 35:
            label = label[:34] + "…"
        if sub.peak_context is None:
            peak_col = "—"
            status = "—"
        else:
            peak_col = f"{bar(sub.peak_context, CONTEXT_LIMIT)} {_k(sub.peak_context):>4}"
            status = _context_status(sub.peak_context)
        lines.append(f"{index:<3} {label:<35} {peak_col:<20} {status}")
    lines += ["```", ""]
    return lines


def render_markdown(
    summary: dict,
    *,
    generated_at: str,
    meta: dict[str, SessionMeta] | None = None,
    notes: dict[str, str] | None = None,
    subagent_archive: dict | None = None,  # unused in overview; kept for API compat
) -> str:
    """Rendert den Effizienz-Report als Markdown (ADR-0002, leser-orientiert).

    Reihenfolge (Plan 023):
      Header → Verlauf → Jüngste Session → (Retro-)Hinweise → 150k-Korridor →
      Zusammensetzung der Antworten → Vergangene Sessions (Link) → Σ-Zeile.
    """
    meta = meta or {}
    notes = notes or {}
    grand = summary["grand_total"]
    lines: list[str] = [
        "# Token-Report — Effizienz statt Menge",
        "",
        "<!-- Generiert von tools/token_report.py — nicht von Hand pflegen. -->",
        f"Stand: {generated_at}",
        "",
        "Beantwortet: *wurden die Token gut ausgegeben, werden wir besser oder schlechter?*",
        "Korridor: **150k** Kontext-Token je Antwort (CLAUDE.md). "
        "Token-Maß = input + cache_creation + cache_read + output.",
        "",
    ]

    ordered = _sessions_newest_first(summary, meta)
    if not ordered:
        lines += ["_Keine Session-Daten gefunden._", ""]
        return "\n".join(lines)

    focus = ordered[0]
    focus_meta = meta.get(focus, _EMPTY_META)
    focus_summary = summary["sessions"][focus]

    lines += _render_history(ordered, summary, meta)
    lines += _render_focus(focus_summary, focus_meta, link=notes.get(focus))
    lines += _render_hints(focus_summary)
    lines += _render_subagent_corridor(focus_meta)
    lines += _render_composition(focus_summary)
    lines += [
        "## Vergangene Sessions",
        "",
        "→ vollständige Historie: [session_archive.md](session_archive.md)",
        "",
    ]
    lines += [
        "---",
        "",
        f"Σ über {len(ordered)} Sessions: {_fmt(grand.total)} Token "
        f"({_fmt(grand.count)} Antworten).",
        "",
    ]
    return "\n".join(lines)


# --------------------------------------------------------------------------- #
# Subagent-Archiv (je Session, akkumulierend)                                  #
# --------------------------------------------------------------------------- #


def _migrate_old_list_entry(value: list) -> dict:
    """Hebt einen alten Listen-Eintrag ``[{...}, ...]`` in das neue Dict-Schema."""
    started_at = value[0].get("started_at") if value else None
    return {
        "started_at": started_at,
        "task": None,
        "peak_context": None,
        "subagent_share": None,
        "by_tier": {},
        "subagents": value,
    }


def load_session_archive(path: Path) -> dict[str, dict]:
    """Lädt das persistente Session-Archiv aus ``path`` (leer, wenn Datei fehlt).

    Neues Schema: ``{session_id: {"started_at": ..., "task": ..., "peak_context": int|null,
    "subagent_share": float|null, "by_tier": {...}, "subagents": [...]}}``.

    Rückwärtskompatibilität: Einträge im alten Listen-Format (``value`` ist ``list``)
    werden on-the-fly in das neue Dict-Schema gehoben — keine Daten gehen verloren.
    """
    if not path.is_file():
        return {}
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return {}
    if not isinstance(data, dict):
        return {}
    result: dict[str, dict] = {}
    for sid, value in data.items():
        if isinstance(value, list):
            result[sid] = _migrate_old_list_entry(value)
        elif isinstance(value, dict):
            result[sid] = value
    return result


# Kept for backward compatibility with tests and callers that reference the old name.
def load_subagent_archive(path: Path) -> dict:
    """Alias für ``load_session_archive`` (rückwärtskompatibel)."""
    return load_session_archive(path)


def _subagents_to_records(subagents: list[Subagent], started_at: str | None) -> list[dict]:
    """Konvertiert ``Subagent``-Objekte in archivierbare Dicts."""
    return [
        {
            "agent_type": sub.agent_type,
            "description": sub.description,
            "tier": sub.tier,
            "peak_context": sub.peak_context,
            "started_at": started_at,
        }
        for sub in subagents
    ]


def merge_session_into_archive(
    archive: dict[str, dict],
    session_id: str,
    subagents: list[Subagent],
    started_at: str | None,
    *,
    task: str | None = None,
    peak_context: int | None = None,
    subagent_share: float | None = None,
    by_tier: dict[str, int] | None = None,
) -> dict[str, dict]:
    """Fügt eine Session in das Archiv ein (Upsert, idempotent).

    Speichert das volle Session-Dict (started_at, task, peak_context, subagent_share,
    by_tier, subagents). Mehrfacher Aufruf mit derselben ``session_id`` überschreibt
    den Eintrag — keine Duplikate.
    Sessions ohne Subagenten werden nicht archiviert.
    """
    updated = dict(archive)
    if subagents:
        updated[session_id] = {
            "started_at": started_at,
            "task": task,
            "peak_context": peak_context,
            "subagent_share": subagent_share,
            "by_tier": by_tier or {},
            "subagents": _subagents_to_records(subagents, started_at),
        }
    return updated


def save_session_archive(path: Path, archive: dict[str, dict]) -> None:
    """Schreibt das Session-Archiv als JSON nach ``path``."""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(archive, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


# Kept for backward compatibility with tests and callers that reference the old name.
def save_subagent_archive(path: Path, archive: dict) -> None:
    """Alias für ``save_session_archive`` (rückwärtskompatibel)."""
    save_session_archive(path, archive)


def _archive_subagents(entry: dict | list) -> list[dict]:
    """Gibt die Subagenten-Liste aus einem Archiv-Eintrag zurück (neues und altes Schema)."""
    if isinstance(entry, list):
        return entry
    return entry.get("subagents") or []


def _archive_started_at(entry: dict | list, sid: str) -> str | None:
    """Gibt started_at aus einem Archiv-Eintrag zurück (neues und altes Schema)."""
    if isinstance(entry, list):
        return entry[0].get("started_at") if entry else None
    return entry.get("started_at")


def render_session_archive_md(archive: dict[str, dict | list], *, generated_at: str) -> str:
    """Rendert das vollständige Session-Archiv als Markdown (session_archive.md).

    Struktur je Session: Hauptzeile (Label · Peak-Balken · Subagent-Anteil · Modell-Mix)
    + Subzeilen je Subagent (SA_N· Peak-Balken + Status + Aufgabe).
    Sessions durch ``---``-Trenner getrennt, jüngste zuerst.
    Fehlende Hauptzeilen-Werte (aus migrierten Alt-Sessions) → ``—``/leere Balken.
    """

    def _entry_started_at(entry: dict | list, sid: str) -> str | None:
        return _archive_started_at(entry, sid)

    def _entry_subs(entry: dict | list) -> list[dict]:
        return _archive_subagents(entry)

    ordered = sorted(
        archive.keys(),
        key=lambda sid: (_entry_started_at(archive[sid], sid) or "", sid),
        reverse=True,
    )

    header_lines = [
        "# Session-Archiv",
        "",
        "<!-- Generiert von tools/token_report.py — nicht von Hand pflegen. -->",
        f"Stand: {generated_at}",
        "",
        "Jüngste zuerst. Akkumuliert über alle Sessions (dedup je Session-ID).",
        "Modell-Mix: `█` Opus · `·` Sonnet · `▒` Haiku · `▓` sonstige.",
        "",
        "```text",
        f"{'Session':<17} {'Peak-Kontext':<22} {'Subagent':<14} {'Modell-Mix':<12}",
        f"{'-' * 17} {'-' * 22} {'-' * 14} {'-' * 12}",
    ]

    body_lines: list[str] = []
    for index, sid in enumerate(ordered):
        entry = archive[sid]
        is_new_schema = isinstance(entry, dict)

        started_at = _entry_started_at(entry, sid)
        label = _short_label(sid, started_at)

        # Hauptzeilen-Felder aus dem neuen Schema; Migration liefert None für fehlende Werte.
        peak = entry.get("peak_context") if is_new_schema else None
        share = entry.get("subagent_share") if is_new_schema else None
        by_tier: dict[str, int] = (entry.get("by_tier") or {}) if is_new_schema else {}

        peak_col: str
        if peak is not None:
            status = _context_status(peak)
            peak_col = f"{bar(peak, CONTEXT_LIMIT)} {_k(peak):>4} {status}"
        else:
            peak_col = "—"

        share_col: str
        if share is not None:
            share_bar = bar(round(share), 100, width=6)
            share_col = f"{share_bar} {share:>3.0f}%"
        else:
            share_col = "—"

        mix_col = model_mix_bar(by_tier) if by_tier else "—"

        body_lines.append(f"{label:<17} {peak_col:<22} {share_col:<14} {mix_col:<12}")

        # Subzeilen je Subagent.
        for sa_index, rec in enumerate(_entry_subs(entry), start=1):
            sa_peak = rec.get("peak_context")
            sa_desc = (rec.get("description") or "").strip()
            if len(sa_desc) > 35:
                sa_desc = sa_desc[:34] + "…"
            if sa_peak is not None:
                sa_peak_col = (
                    f"{bar(sa_peak, CONTEXT_LIMIT)} {_k(sa_peak):>4} {_context_status(sa_peak)}"
                )
            else:
                sa_peak_col = "—"
            body_lines.append(f"{'':9}SA_{sa_index}·  {sa_peak_col:<22} {sa_desc}")

        body_lines.append(f"{'-' * 17} {'-' * 22} {'-' * 14} {'-' * 12}")

    all_lines = header_lines + body_lines + ["```", ""]
    return "\n".join(all_lines)


# --------------------------------------------------------------------------- #
# I/O                                                                          #
# --------------------------------------------------------------------------- #

_OUTPUT_DOC = Path("docs/metrics/overview.md")
_ARCHIVE_MD = Path("docs/metrics/session_archive.md")
_NOTES_FILE = Path("docs/metrics/session_notes.yaml")
_OLD_ARCHIVE_FILE = Path("docs/metrics/subagent_archive.json")
_ARCHIVE_FILE = Path("docs/metrics/session_archive.json")


def load_session_notes(path: Path) -> dict[str, str]:
    """Optionale ``<session-id>: link``-Zuordnung (leer, wenn Datei fehlt)."""
    if not path.is_file():
        return {}
    try:
        import yaml

        data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    except Exception:
        return {}
    if not isinstance(data, dict):
        return {}
    return {str(key): str(value) for key, value in data.items() if value}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--session", help="Nur diese Session-ID auswerten (Default: alle).")
    parser.add_argument(
        "--write",
        action="store_true",
        help=f"Report nach {_OUTPUT_DOC} und {_ARCHIVE_MD} schreiben (sonst stdout).",
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

    records, meta = collect_project(project_dir, session_filter=args.session)
    summary = summarize(records)
    generated_at = datetime.now(_LOCAL_TZ).strftime("%Y-%m-%d %H:%M %Z")

    # Session-Archiv: laden (neue Datei; einmalige Migration aus Altdatei wenn nötig).
    if _ARCHIVE_FILE.is_file():
        archive = load_session_archive(_ARCHIVE_FILE)
    elif _OLD_ARCHIVE_FILE.is_file():
        # Einmalige Migration: altes subagent_archive.json ins neue Schema heben.
        archive = load_session_archive(_OLD_ARCHIVE_FILE)
    else:
        archive = {}

    # Aktuelle Sessions in das Archiv mergen (Upsert, idempotent je session_id).
    sessions_summary = summary["sessions"]
    for session_id, session_meta in meta.items():
        session_summ = sessions_summary.get(session_id)
        archive = merge_session_into_archive(
            archive,
            session_id,
            session_meta.subagents,
            session_meta.started_at,
            task=session_meta.task,
            peak_context=session_summ.peak_context if session_summ else None,
            subagent_share=session_summ.subagent_share if session_summ else None,
            by_tier=session_summ.by_tier if session_summ else None,
        )

    report = render_markdown(
        summary,
        generated_at=generated_at,
        meta=meta,
        notes=load_session_notes(_NOTES_FILE),
    )

    if args.write:
        _OUTPUT_DOC.parent.mkdir(parents=True, exist_ok=True)
        _OUTPUT_DOC.write_text(report + "\n", encoding="utf-8")
        print(f"Report geschrieben: {_OUTPUT_DOC}")

        save_session_archive(_ARCHIVE_FILE, archive)

        archive_md = render_session_archive_md(archive, generated_at=generated_at)
        _ARCHIVE_MD.write_text(archive_md + "\n", encoding="utf-8")
        print(f"Archiv geschrieben: {_ARCHIVE_MD}")
    else:
        print(report)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
