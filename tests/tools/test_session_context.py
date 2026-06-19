"""Tiering of the Kontext-Korridor gauge (UserPromptSubmit hook)."""

from tools.session_context import (
    STOP_THRESHOLD,
    WARN_THRESHOLD,
    gauge_message,
)


def test_below_warn_shows_neutral_gauge():
    msg = gauge_message(35_000)
    assert msg.startswith("Session context: ~35k")
    assert "⚠️" not in msg and "⛔" not in msg


def test_at_warn_threshold_escalates_to_warning():
    msg = gauge_message(WARN_THRESHOLD)
    assert msg.startswith("⚠️")
    assert "Korridor" in msg


def test_between_warn_and_stop_stays_warning():
    msg = gauge_message(130_000)
    assert msg.startswith("⚠️")


def test_at_stop_threshold_emits_stop_directive():
    msg = gauge_message(STOP_THRESHOLD)
    assert msg.startswith("⛔")
    assert "Wind-down" in msg


def test_far_above_stop_still_stops():
    msg = gauge_message(148_000)
    assert msg.startswith("⛔")
