"""Tests für die reine Aggregations-Logik von tools/token_report.py.

tools/ ist nicht in der Coverage-Messung (``--cov=src``); diese Tests sind das
fachliche Sicherheitsnetz für den Parser und die Summenbildung.
"""

from __future__ import annotations

import json

from tools.token_report import (
    UsageRecord,
    parse_usage_lines,
    render_markdown,
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


def test_render_markdown_shows_subagent_share_and_totals():
    records = [
        UsageRecord("session-aaaa", "main", "claude-opus-4-8", 75, 0, 0, 0),
        UsageRecord("session-aaaa", "subagent", "claude-sonnet-4-6", 25, 0, 0, 0),
    ]
    md = render_markdown(summarize(records), generated_at="2026-06-18 00:00 UTC")

    assert "Token-Report" in md
    assert "25.0 %" in md  # Subagent-Anteil 25/100
    assert "`session-`" in md  # Session-ID auf 8 Zeichen gekürzt
    assert "Opus" in md and "Sonnet" in md


def test_render_markdown_escapes_angle_bracket_labels():
    records = [UsageRecord("s1", "main", "<synthetic>", 0, 0, 0, 0)]
    md = render_markdown(summarize(records), generated_at="2026-06-18 00:00 UTC")

    assert "&lt;synthetic&gt;" in md
    assert "<synthetic>" not in md  # roher Tag würde im Renderer verschwinden
