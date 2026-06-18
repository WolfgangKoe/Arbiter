"""Tests für die reine Aggregations-Logik von tools/token_report.py.

tools/ ist nicht in der Coverage-Messung (``--cov=src``); diese Tests sind das
fachliche Sicherheitsnetz für den Parser und die Summenbildung.
"""

from __future__ import annotations

import json

from tools.token_report import (
    SessionMeta,
    UsageRecord,
    parse_first_timestamp,
    parse_usage_lines,
    render_markdown,
    session_label,
    summarize,
    tier_for_model,
)


def _assistant_line(model: str, **usage: int) -> str:
    return json.dumps(
        {
            "type": "assistant",
            "message": {"model": model, "usage": usage},
        }
    )


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
    assert records[0].output_tokens == 5


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


def test_summarize_splits_main_and_subagent_per_session():
    records = [
        UsageRecord("s1", "main", "claude-opus-4-8", 100, 0, 0, 0),
        UsageRecord("s1", "subagent", "claude-haiku-4-5", 30, 0, 0, 0),
        UsageRecord("s2", "main", "claude-opus-4-8", 50, 0, 0, 0),
    ]
    summary = summarize(records)

    assert summary["by_session"]["s1"]["main"].total == 100
    assert summary["by_session"]["s1"]["subagent"].total == 30
    assert summary["by_session"]["s2"]["subagent"].total == 0
    assert summary["by_tier"]["Opus"].total == 150
    assert summary["by_tier"]["Haiku"].total == 30
    assert summary["grand_total"].total == 180
    assert summary["grand_total"].count == 3


def test_render_markdown_shows_subagent_share_and_labelled_total():
    records = [
        UsageRecord("session-aaaa", "main", "claude-opus-4-8", 75, 0, 0, 0),
        UsageRecord("session-aaaa", "subagent", "claude-sonnet-4-6", 25, 0, 0, 0),
    ]
    md = render_markdown(summarize(records), generated_at="2026-06-18 00:00 UTC")

    assert "Token-Report" in md
    assert "25.0 %" in md  # Subagent-Anteil 25/100
    assert "session-" in md  # gekürzte Session-ID als Fallback-Label (keine Zeit)
    assert "Σ (alle Sessions)" in md  # Summe klar beschriftet
    assert "Opus" in md and "Sonnet" in md


def test_session_label_uses_date_when_timestamp_present():
    label = session_label("abcdef1234", "2026-06-18T18:53:21.000Z")
    assert label == "2026-06-18 18:53 · abcdef12"


def test_session_label_falls_back_to_short_id_without_timestamp():
    assert session_label("abcdef1234", None) == "abcdef12"
    assert session_label("abcdef1234", "kaputt") == "abcdef12"


def test_parse_first_timestamp_returns_first_seen():
    lines = [
        "",
        "not json",
        '{"type": "user", "timestamp": "2026-06-18T10:00:00Z"}',
        '{"type": "assistant", "timestamp": "2026-06-18T11:00:00Z"}',
    ]
    assert parse_first_timestamp(lines) == "2026-06-18T10:00:00Z"


def test_render_markdown_orders_newest_session_first():
    records = [
        UsageRecord("old-sess", "main", "claude-opus-4-8", 10, 0, 0, 0),
        UsageRecord("new-sess", "main", "claude-opus-4-8", 10, 0, 0, 0),
    ]
    meta = {
        "old-sess": SessionMeta("2026-06-01T09:00:00Z", []),
        "new-sess": SessionMeta("2026-06-18T09:00:00Z", []),
    }
    md = render_markdown(summarize(records), generated_at="x", meta=meta)
    assert md.index("2026-06-18") < md.index("2026-06-01")


def test_render_markdown_lists_subagents_with_task():
    records = [UsageRecord("s1", "main", "claude-opus-4-8", 10, 0, 0, 0)]
    meta = {"s1": SessionMeta(None, [("Explore", "Suche Aufrufer von foo()")])}
    md = render_markdown(summarize(records), generated_at="x", meta=meta)

    assert "Subagenten — wer wurde wofür gestartet" in md
    assert "Explore" in md
    assert "Suche Aufrufer von foo()" in md


def test_render_markdown_includes_tier_pie_diagram():
    records = [UsageRecord("s1", "main", "claude-opus-4-8", 100, 0, 0, 0)]
    md = render_markdown(summarize(records), generated_at="x")
    assert "```mermaid" in md
    assert "pie showData" in md
    assert '"Opus" : 100' in md


def test_render_markdown_escapes_angle_bracket_labels():
    records = [UsageRecord("s1", "main", "<synthetic>", 0, 0, 0, 0)]
    md = render_markdown(summarize(records), generated_at="2026-06-18 00:00 UTC")

    assert "&lt;synthetic&gt;" in md
    assert "<synthetic>" not in md  # roher Tag würde im Renderer verschwinden
