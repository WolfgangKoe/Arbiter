"""Tiering of the Kontext-Korridor gauge (UserPromptSubmit hook).

Schwellen nach Plan 028 Step 1 (O3):
  WARN_THRESHOLD = STOP_THRESHOLD = 135k — erst ab 135k wird eskaliert.
  Unter 135k erscheint nur der neutrale Gauge (kein ⚠️, kein ⛔).
"""

from tools.session_context import (
    STOP_THRESHOLD,
    gauge_message,
)


def test_below_warn_shows_neutral_gauge():
    msg = gauge_message(35_000)
    assert msg.startswith("Session context: ~35k")
    assert "⚠️" not in msg and "⛔" not in msg


# Plan-028-Test: 120k liegt unter der neuen 135k-Schwelle → neutral (kein ⚠️)
def test_gauge_message_below_threshold_is_neutral():
    """120k erzeugt keinen ⚠️ mehr (Schwelle wurde auf 135k angehoben)."""
    msg = gauge_message(120_000)
    assert "⚠️" not in msg and "⛔" not in msg
    assert msg.startswith("Session context: ~120k")


# Plan-028-Test: 135k → ⚠️/⛔ (Eskalation startet erst jetzt)
def test_gauge_message_at_warn_threshold():
    """135k triggert Eskalation (warn_threshold = stop_threshold = 135k)."""
    msg = gauge_message(135_000)
    # STOP_THRESHOLD == WARN_THRESHOLD → der ⛔-Zweig greift zuerst
    assert msg.startswith("⛔")
    assert "Wind-down" in msg


def test_between_warn_and_stop_is_neutral():
    """130k liegt unter 135k → neutraler Gauge (migriert von stays_warning)."""
    msg = gauge_message(130_000)
    assert "⚠️" not in msg and "⛔" not in msg


def test_at_stop_threshold_emits_stop_directive():
    msg = gauge_message(STOP_THRESHOLD)
    assert msg.startswith("⛔")
    assert "Wind-down" in msg


def test_far_above_stop_still_stops():
    msg = gauge_message(148_000)
    assert msg.startswith("⛔")
