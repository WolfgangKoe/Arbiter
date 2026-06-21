"""Tests für die reine Aggregations-/Render-Logik von tools/token_report.py (v3).

tools/ ist nicht in der Coverage-Messung (``--cov=src``); diese Tests sind das
fachliche Sicherheitsnetz für Parser, Summenbildung und die theme-sicheren Balken.
"""

from __future__ import annotations

import json

from tools.token_report import (
    CONTEXT_LIMIT,
    Bucket,
    SessionMeta,
    Subagent,
    UsageRecord,
    _context_status,
    _render_subagent_corridor,
    _subagent_peak_context,
    bar,
    generate_hints,
    load_session_archive,
    load_subagent_archive,
    merge_session_into_archive,
    model_mix_bar,
    parse_first_timestamp,
    parse_first_user_task,
    parse_usage_lines,
    read_subagents,
    render_markdown,
    render_session_archive_md,
    save_session_archive,
    session_label,
    summarize,
    tier_for_model,
    trend,
)


def _assistant_line(model: str, **usage: int) -> str:
    return json.dumps({"type": "assistant", "message": {"model": model, "usage": usage}})


def _record(session, role, model, inp=0, cc=0, cr=0, out=0) -> UsageRecord:
    return UsageRecord(session, role, model, inp, cc, cr, out)


# --- Parser -------------------------------------------------------------- #


def test_tier_for_model_maps_known_prefixes_and_falls_back():
    assert tier_for_model("claude-opus-4-8") == "Opus"
    assert tier_for_model("claude-sonnet-4-6") == "Sonnet"
    assert tier_for_model("claude-haiku-4-5-20251001") == "Haiku"
    assert tier_for_model(None) == "unbekannt"
    assert tier_for_model("some-future-model") == "some-future-model"


def test_parse_usage_lines_sums_all_four_token_kinds():
    line = _assistant_line(
        "claude-opus-4-8",
        input_tokens=10,
        cache_creation_input_tokens=100,
        cache_read_input_tokens=1000,
        output_tokens=5,
    )
    records = parse_usage_lines([line], session="s1", role="main")
    assert len(records) == 1
    assert records[0].total == 1115
    assert records[0].context == 1110  # input + cache_read + cache_creation (ohne Output)


def test_parse_usage_lines_skips_non_assistant_and_broken_lines():
    lines = [
        '{"type": "user", "message": {"content": "hi"}}',
        "not json at all",
        "",
        '{"type": "assistant", "message": {"model": "claude-opus-4-8"}}',  # kein usage
        _assistant_line("claude-opus-4-8", input_tokens=7, output_tokens=3),
    ]
    records = parse_usage_lines(lines, session="s1", role="main")
    assert len(records) == 1
    assert records[0].total == 10


def test_parse_first_timestamp_returns_first_seen():
    lines = [
        "",
        "not json",
        '{"type": "user", "timestamp": "2026-06-18T10:00:00Z"}',
        '{"type": "assistant", "timestamp": "2026-06-18T11:00:00Z"}',
    ]
    assert parse_first_timestamp(lines) == "2026-06-18T10:00:00Z"


def test_parse_first_user_task_skips_wrapper_lines():
    lines = [
        json.dumps({"type": "user", "message": {"content": "<command-name>/model</command-name>"}}),
        json.dumps({"type": "user", "message": {"content": "<local-command-stdout>x</...>"}}),
        json.dumps({"type": "user", "isMeta": True, "message": {"content": "echte Aufgabe?"}}),
        json.dumps({"type": "user", "message": {"content": "Baue den Token-Report v3"}}),
    ]
    assert parse_first_user_task(lines) == "Baue den Token-Report v3"


def test_parse_first_user_task_truncates_and_returns_none_when_only_wrappers():
    long_task = "x " * 200
    assert parse_first_user_task(
        [json.dumps({"type": "user", "message": {"content": long_task}})]
    ).endswith("…")
    assert (
        parse_first_user_task(
            [json.dumps({"type": "user", "message": {"content": "<system-reminder>r</...>"}})]
        )
        is None
    )


def test_read_subagents_reads_task_and_model_tier(tmp_path):
    sub_dir = tmp_path / "subagents"
    sub_dir.mkdir()
    (sub_dir / "agent-1.meta.json").write_text(
        json.dumps({"agentType": "Explore", "description": "Audit YAML"})
    )
    (sub_dir / "agent-1.jsonl").write_text(
        _assistant_line("claude-sonnet-4-6", input_tokens=50_000, output_tokens=1)
    )

    subagents = read_subagents(sub_dir)
    assert len(subagents) == 1
    sub = subagents[0]
    assert sub.agent_type == "Explore"
    assert sub.description == "Audit YAML"
    assert sub.tier == "Sonnet"
    assert sub.peak_context == 50_000


def test_subagent_peak_context_returns_none_for_missing_file(tmp_path):
    assert _subagent_peak_context(tmp_path / "no-such.jsonl") is None


def test_subagent_peak_context_returns_max_context(tmp_path):
    jsonl = tmp_path / "agent.jsonl"
    jsonl.write_text(
        "\n".join(
            [
                _assistant_line(
                    "claude-sonnet-4-6", input_tokens=30_000, cache_read_input_tokens=20_000
                ),
                _assistant_line("claude-sonnet-4-6", input_tokens=80_000),
            ]
        )
    )
    # max(30k+20k, 80k) = 80k
    assert _subagent_peak_context(jsonl) == 80_000


def test_context_status_thresholds():
    assert _context_status(None) == "—"
    assert _context_status(0) == "✅"
    assert _context_status(119_999) == "✅"
    assert _context_status(120_000) == "⚠️"
    assert _context_status(149_999) == "⚠️"
    assert _context_status(150_000) == "⛔"
    assert _context_status(200_000) == "⛔"


def test_render_subagent_corridor_no_subagents():
    meta = SessionMeta("2026-06-18T09:00:00Z", "task", [])
    lines = _render_subagent_corridor(meta)
    assert any("keine Subagenten" in line for line in lines)


def test_render_subagent_corridor_shows_peak_bar():
    sub = Subagent("Explore", "Audit YAML", "Sonnet", peak_context=60_000)
    meta = SessionMeta("2026-06-18T09:00:00Z", "task", [sub])
    lines = _render_subagent_corridor(meta)
    combined = "\n".join(lines)
    assert "60k" in combined
    assert "✅" in combined
    assert "Explore" in combined
    assert "150k" in combined  # 150k reference in column header


# --- Aggregation --------------------------------------------------------- #


def test_summarize_splits_roles_tiers_and_peak_context():
    records = [
        _record("s1", "main", "claude-opus-4-8", inp=100, cr=40_000),
        _record("s1", "main", "claude-opus-4-8", inp=200, cr=80_000),  # höherer Kontext
        _record("s1", "subagent", "claude-haiku-4-5", inp=30),
        _record("s2", "main", "claude-opus-4-8", inp=50),
    ]
    summary = summarize(records)
    s1 = summary["sessions"]["s1"]

    assert s1.main.total == 100 + 40_000 + 200 + 80_000
    assert s1.subagent.total == 30
    assert s1.peak_context == 80_200  # max(input + cache_read) der Haupt-Antworten
    assert s1.answers == 2
    assert s1.main_by_tier["Opus"] == 120_300
    assert s1.sub_by_tier["Haiku"] == 30
    assert s1.by_tier == {"Opus": 120_300, "Haiku": 30}
    assert summary["grand_total"].total == 120_380


def test_session_summary_subagent_share_and_over_limit():
    records = [
        _record("s1", "main", "claude-opus-4-8", cr=CONTEXT_LIMIT + 1),  # über Korridor
        _record("s1", "subagent", "claude-sonnet-4-6", inp=CONTEXT_LIMIT + 1),
    ]
    s1 = summarize(records)["sessions"]["s1"]
    assert s1.over_limit == 1
    assert round(s1.subagent_share) == 50


def test_bucket_add_is_componentwise():
    combined = Bucket(1, 2, 3, 4, 1) + Bucket(10, 20, 30, 40, 1)
    assert (combined.input, combined.cache_creation, combined.cache_read, combined.output) == (
        11,
        22,
        33,
        44,
    )
    assert combined.total == 110 and combined.count == 2


# --- Balken / Trend ------------------------------------------------------ #


def test_bar_fills_proportionally_and_clamps():
    assert bar(0, 100, width=10) == "░" * 10
    assert bar(100, 100, width=10) == "█" * 10
    assert bar(50, 100, width=10) == "█████░░░░░"
    assert bar(999, 100, width=10) == "█" * 10  # Clamp bei Überschreitung
    assert bar(5, 0, width=4) == "░░░░"  # maximum 0 -> leer


def test_model_mix_bar_segments_by_tier_share():
    mix = model_mix_bar({"Opus": 6, "Sonnet": 3, "Haiku": 3}, width=12)
    assert len(mix) == 12
    assert mix.count("█") == 6 and mix.count("·") == 3 and mix.count("▒") == 3
    assert model_mix_bar({}, width=4) == "▓▓▓▓"


def test_trend_compares_to_previous():
    assert trend(10, 5) == "↑"
    assert trend(5, 10) == "↓"
    assert trend(5, 5) == "→"
    assert trend(5, None) == "—"


# --- Hinweise ------------------------------------------------------------ #


def test_generate_hints_warns_on_corridor_breach():
    summary = summarize([_record("s1", "main", "claude-opus-4-8", cr=CONTEXT_LIMIT + 1)])
    hints = generate_hints(summary["sessions"]["s1"])
    assert any("150k-Korridor" in h and "über" in h for h in hints)


def test_generate_hints_praises_subagent_offloading():
    records = [
        _record("s1", "main", "claude-opus-4-8", inp=100),
        _record("s1", "subagent", "claude-sonnet-4-6", inp=900),
    ]
    hints = generate_hints(summarize(records)["sessions"]["s1"])
    assert any("Subagenten" in h for h in hints)
    assert any("Tiering" in h for h in hints)


# --- Render -------------------------------------------------------------- #


def test_session_label_uses_date_when_timestamp_present():
    # UTC-Zeitstempel werden in lokaler Zeit (Europe/Berlin) gezeigt: 18:53Z → 20:53 CEST (S78).
    assert session_label("abcdef1234", "2026-06-18T18:53:21.000Z") == "2026-06-18 20:53 · abcdef12"


def test_session_label_falls_back_to_short_id_without_timestamp():
    assert session_label("abcdef1234", None) == "abcdef12"
    assert session_label("abcdef1234", "kaputt") == "abcdef12"


def test_render_markdown_has_v3_sections_and_no_pie():
    records = [
        _record("new", "main", "claude-opus-4-8", inp=100, cr=50_000, out=20),
        _record("new", "subagent", "claude-sonnet-4-6", inp=40),
        _record("old", "main", "claude-opus-4-8", inp=10),
    ]
    meta = {
        "new": SessionMeta("2026-06-18T09:00:00Z", "Token-Report v3 bauen", []),
        "old": SessionMeta("2026-06-01T09:00:00Z", "Vorgänger", []),
    }
    md = render_markdown(summarize(records), generated_at="x", meta=meta)

    assert "Effizienz statt Menge" in md
    assert "## Jüngste Session" in md  # Plan-023: Heading umbenannt
    assert "Token-Report v3 bauen" in md  # Aufgabe aus Meta
    assert "## Verlauf (letzte 6 Sessions)" in md
    assert "## (Retro-)Hinweise" in md  # Plan-023: Heading umbenannt
    assert "Peak-Kontext" in md
    assert "150k" in md
    assert "pie showData" not in md  # All-Time-Torte entfernt (Akzeptanz f)


def test_render_markdown_orders_newest_session_first():
    records = [
        _record("old-sess", "main", "claude-opus-4-8", inp=10),
        _record("new-sess", "main", "claude-opus-4-8", inp=10),
    ]
    meta = {
        "old-sess": SessionMeta("2026-06-01T09:00:00Z", None, []),
        "new-sess": SessionMeta("2026-06-18T09:00:00Z", None, []),
    }
    md = render_markdown(summarize(records), generated_at="x", meta=meta)
    # Fokus zeigt die jüngste Session voll, Verlauf beide im Kurzformat (MM-DD) jüngste zuerst.
    assert "2026-06-18" in md  # jüngste als Fokus
    assert md.index("06-18") < md.index("06-01")


def test_render_markdown_corridor_shows_subagent():
    """Der 150k-Korridor-Abschnitt zeigt Subagenten der jüngsten Session."""
    records = [_record("s1", "main", "claude-opus-4-8", inp=10)]
    sub = Subagent("Explore", "Suche Aufrufer", "Sonnet", peak_context=40_000)
    meta = {"s1": SessionMeta(None, None, [sub])}
    md = render_markdown(summarize(records), generated_at="x", meta=meta)

    assert "150k-Korridor für Subagenten" in md  # Plan-023: Heading
    assert "Explore" in md and "Suche Aufrufer" in md


def test_render_markdown_applies_session_note_link():
    records = [_record("s1", "main", "claude-opus-4-8", inp=10)]
    meta = {"s1": SessionMeta("2026-06-18T09:00:00Z", "Aufgabe", [])}
    md = render_markdown(
        summarize(records), generated_at="x", meta=meta, notes={"s1": "../goals/backlog.md#v3"}
    )
    assert "([Backlog](../goals/backlog.md#v3))" in md


def test_render_markdown_escapes_angle_bracket_task():
    records = [_record("s1", "main", "claude-opus-4-8", inp=10)]
    meta = {"s1": SessionMeta(None, "<synthetic>", [])}
    md = render_markdown(summarize(records), generated_at="x", meta=meta)
    assert "&lt;synthetic&gt;" in md
    assert "<synthetic>" not in md


def test_render_markdown_handles_empty_summary():
    md = render_markdown(summarize([]), generated_at="x", meta={})
    assert "Keine Session-Daten" in md


# --- Subagent-Archiv ----------------------------------------------------- #


def test_merge_session_into_archive_is_idempotent():
    """Dieselbe Session zweimal einfügen ergibt genau einen Eintrag."""
    sub = Subagent("Explore", "Audit YAML", "Sonnet", peak_context=60_000)
    archive: dict = {}
    archive = merge_session_into_archive(archive, "sess-A", [sub], "2026-06-20T10:00:00Z")
    archive = merge_session_into_archive(archive, "sess-A", [sub], "2026-06-20T10:00:00Z")

    assert list(archive.keys()) == ["sess-A"]
    entry = archive["sess-A"]
    assert len(entry["subagents"]) == 1
    assert entry["subagents"][0]["description"] == "Audit YAML"
    assert entry["subagents"][0]["peak_context"] == 60_000


def test_merge_session_into_archive_accumulates_distinct_sessions():
    """Zwei verschiedene Sessions werden beide behalten."""
    sub_a = Subagent("Explore", "Task A", "Sonnet", peak_context=40_000)
    sub_b = Subagent("general-purpose", "Task B", "Opus", peak_context=80_000)
    archive: dict = {}
    archive = merge_session_into_archive(archive, "sess-A", [sub_a], "2026-06-19T09:00:00Z")
    archive = merge_session_into_archive(archive, "sess-B", [sub_b], "2026-06-20T09:00:00Z")

    assert set(archive.keys()) == {"sess-A", "sess-B"}
    assert archive["sess-A"]["subagents"][0]["description"] == "Task A"
    assert archive["sess-B"]["subagents"][0]["description"] == "Task B"


def test_merge_session_into_archive_skips_sessions_without_subagents():
    """Sessions ohne Subagenten werden nicht archiviert."""
    archive = merge_session_into_archive({}, "sess-empty", [], "2026-06-20T10:00:00Z")
    assert "sess-empty" not in archive


def test_load_subagent_archive_returns_empty_for_missing_file(tmp_path):
    assert load_subagent_archive(tmp_path / "no-such.json") == {}


def test_save_and_load_session_archive_round_trips(tmp_path):
    archive_path = tmp_path / "metrics" / "session_archive.json"
    sub = Subagent("Explore", "Round-trip test", "Haiku", peak_context=30_000)
    archive = merge_session_into_archive({}, "sess-rt", [sub], "2026-06-20T12:00:00Z")

    save_session_archive(archive_path, archive)
    loaded = load_session_archive(archive_path)

    assert loaded == archive
    assert loaded["sess-rt"]["subagents"][0]["tier"] == "Haiku"
    assert loaded["sess-rt"]["subagents"][0]["peak_context"] == 30_000


# --- Plan-023-Tests -------------------------------------------------------- #


def test_overview_has_no_wide_subagent_table():
    """„## Subagenten — wer wurde wofür gestartet" darf nicht in overview erscheinen."""
    records = [_record("s1", "main", "claude-opus-4-8", inp=10)]
    sub = Subagent("Explore", "Some task", "Sonnet", peak_context=40_000)
    meta = {"s1": SessionMeta("2026-06-20T09:00:00Z", "task", [sub])}
    md = render_markdown(summarize(records), generated_at="x", meta=meta)
    assert "## Subagenten — wer wurde wofür gestartet" not in md


def test_overview_section_order():
    """Verlauf < Jüngste < (Retro-)Hinweise < 150k-Korridor < Zusammensetzung < Vergangene."""
    records = [_record("s1", "main", "claude-opus-4-8", inp=100, cr=50_000)]
    meta = {"s1": SessionMeta("2026-06-20T09:00:00Z", "task", [])}
    md = render_markdown(summarize(records), generated_at="x", meta=meta)

    headings = [
        "## Verlauf",
        "## Jüngste Session",
        "## (Retro-)Hinweise",
        "## 150k-Korridor für Subagenten",
        "## Zusammensetzung der Antworten",
        "## Vergangene Sessions",
    ]
    positions = [md.index(h) for h in headings]
    assert positions == sorted(positions), f"Falsche Reihenfolge: {positions}"


def test_overview_links_to_session_archive():
    """overview.md muss einen Link auf session_archive.md enthalten."""
    records = [_record("s1", "main", "claude-opus-4-8", inp=10)]
    meta = {"s1": SessionMeta("2026-06-20T09:00:00Z", "task", [])}
    md = render_markdown(summarize(records), generated_at="x", meta=meta)
    assert "session_archive.md" in md


def test_composition_section_present():
    """„## Zusammensetzung der Antworten" mit allen 4 Balken-Labels."""
    records = [_record("s1", "main", "claude-opus-4-8", inp=100, cc=200, cr=1000, out=50)]
    meta = {"s1": SessionMeta("2026-06-20T09:00:00Z", "task", [])}
    md = render_markdown(summarize(records), generated_at="x", meta=meta)

    assert "## Zusammensetzung der Antworten" in md
    for label in ("input", "cache_creation", "cache_read", "output"):
        assert label in md, f"Balken-Label fehlt: {label}"


def test_session_archive_md_has_main_and_sa_rows():
    """render_session_archive_md: Hauptzeile + SA_1-Subzeile vorhanden."""
    archive = {
        "sess1": {
            "started_at": "2026-06-20T11:42:00Z",
            "task": "some task",
            "peak_context": 131_000,
            "subagent_share": 30.0,
            "by_tier": {"Opus": 8_000_000, "Sonnet": 3_000_000},
            "subagents": [
                {
                    "agent_type": "general-purpose",
                    "description": "Fix setup-phase arch",
                    "tier": "Sonnet",
                    "peak_context": 30_000,
                    "started_at": "2026-06-20T11:42:00Z",
                }
            ],
        }
    }
    md = render_session_archive_md(archive, generated_at="2026-06-20 12:00 UTC")

    assert "# Session-Archiv" in md
    # Hauptzeile: label enthält Datum aus started_at
    assert "06-20" in md
    # Subzeile
    assert "SA_1" in md
    assert "Fix setup-phase arch" in md


def test_merge_session_idempotent():
    """Zweimal dieselbe session_id mergen → genau 1 Eintrag, keine Duplikat-Subagenten."""
    sub = Subagent("general-purpose", "Task X", "Sonnet", peak_context=50_000)
    archive: dict = {}
    archive = merge_session_into_archive(
        archive,
        "sid-1",
        [sub],
        "2026-06-20T10:00:00Z",
        task="Task X",
        peak_context=100_000,
        subagent_share=30.0,
        by_tier={"Opus": 70_000, "Sonnet": 30_000},
    )
    archive = merge_session_into_archive(
        archive,
        "sid-1",
        [sub],
        "2026-06-20T10:00:00Z",
        task="Task X",
        peak_context=100_000,
        subagent_share=30.0,
        by_tier={"Opus": 70_000, "Sonnet": 30_000},
    )

    assert list(archive.keys()) == ["sid-1"]
    assert len(archive["sid-1"]["subagents"]) == 1


def test_load_archive_migrates_old_list_schema(tmp_path):
    """Altes {sid: [...]} Format wird on-the-fly in neues Dict-Schema migriert."""
    old_data = {
        "old-sess": [
            {
                "agent_type": "Explore",
                "description": "Old sub",
                "tier": "Sonnet",
                "peak_context": 40_000,
                "started_at": "2026-06-01T09:00:00Z",
            }
        ]
    }
    archive_path = tmp_path / "subagent_archive.json"
    archive_path.write_text(json.dumps(old_data), encoding="utf-8")

    loaded = load_session_archive(archive_path)

    assert "old-sess" in loaded
    entry = loaded["old-sess"]
    assert isinstance(entry, dict), "Migration muss ein Dict zurückgeben"
    assert "subagents" in entry
    assert len(entry["subagents"]) == 1
    assert entry["subagents"][0]["description"] == "Old sub"
    assert entry["started_at"] == "2026-06-01T09:00:00Z"
    assert entry["peak_context"] is None  # kein Wert im alten Format
