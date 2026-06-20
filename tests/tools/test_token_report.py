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
    bar,
    generate_hints,
    model_mix_bar,
    parse_first_timestamp,
    parse_first_user_task,
    parse_usage_lines,
    read_subagents,
    render_markdown,
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
    (sub_dir / "agent-1.jsonl").write_text(_assistant_line("claude-sonnet-4-6", output_tokens=1))

    subagents = read_subagents(sub_dir)
    assert subagents == [Subagent("Explore", "Audit YAML", "Sonnet")]


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
    assert session_label("abcdef1234", "2026-06-18T18:53:21.000Z") == "2026-06-18 18:53 · abcdef12"


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
    assert "## Fokus: letzte Session" in md
    assert "Token-Report v3 bauen" in md  # Aufgabe aus Meta
    assert "## Verlauf (letzte 6 Sessions)" in md
    assert "## Hinweise" in md
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


def test_render_markdown_lists_subagents_with_model_and_task():
    records = [_record("s1", "main", "claude-opus-4-8", inp=10)]
    meta = {"s1": SessionMeta(None, None, [Subagent("Explore", "Suche Aufrufer", "Sonnet")])}
    md = render_markdown(summarize(records), generated_at="x", meta=meta)

    assert "Subagenten — wer wurde wofür gestartet" in md
    assert "| Session | Modell | Agent | Aufgabe |" in md
    assert "Sonnet" in md and "Explore" in md and "Suche Aufrufer" in md


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
