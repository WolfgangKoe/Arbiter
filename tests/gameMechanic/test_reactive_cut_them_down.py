"""Plan 015 — Cut Them Down reactive window (Fall Back declaration).

Covers movementPhase.py's `pending_fall_back` marker: set the moment a unit
declares Retreat (core_rules.txt Z. 773-778 — this app has no separate
movement-execution step, so "before any models are moved" collapses to
"immediately on declaration"), and consumed by `_render_pending_cut_them_down`,
which renders the reactive box in the ENEMY's column (`player: inactive` in
the shared stratagems.yaml). As of S139 B12b the marker is NOT cleared on Use
(no `on_resolved` callback): window-consuming GOs get the same anchor treatment
as every other GO — the box keeps rendering ("used" at its own anchor,
"used_elsewhere" anywhere else) instead of vanishing the instant it is spent.
`_reset_phase_state()` clears `pending_fall_back` at the phase boundary, so the
window still never outlives the phase.

S139 E7: `_render_pending_cut_them_down` takes a single `faction` (the column
it is being rendered from) instead of `(first, second)` — a pre-existing
layout bug had `render_active` call it once, outside `st.columns()`, so the
box spanned/sat below both player columns instead of living in the affected
player's own column. Now called once per column, from inside that column's
`with colN:` block; it renders nothing when `faction` is the retreating side
itself (see `test_no_render_in_retreating_players_own_column`).
"""

from __future__ import annotations

import sys
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import MagicMock

_st_mock = MagicMock()
sys.modules["streamlit"] = _st_mock
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

import gameMechanic.movementPhase as mp  # noqa: E402


class FakeSessionState(dict):
    """Dict with attribute access — mirrors streamlit's session_state API."""

    def __getattr__(self, name):  # type: ignore[no-untyped-def]
        try:
            return self[name]
        except KeyError as exc:
            raise AttributeError(name) from exc

    def __setattr__(self, name, value):  # type: ignore[no-untyped-def]
        self[name] = value


# ---------------------------------------------------------------------------
# Retreat click opens the window
# ---------------------------------------------------------------------------


def test_retreat_click_sets_pending_fall_back_marker(monkeypatch) -> None:
    """Clicking "Retreat" for a unit in melee opens the Cut Them Down window."""
    unit = SimpleNamespace(name_en="Necron Warriors", get_triggered_effect=lambda *a, **kw: None)
    unit_state = {
        "in_reserve": False,
        "in_melee": True,
        "movement_choice": None,
        "turn_flags": {},
    }
    session = FakeSessionState(round=3, pending_fall_back=None)
    mp.st.session_state = session
    mp.st.button = lambda label, key=None, **kw: key == "mv_Necrons_u1_retreated"
    mp.st.rerun = MagicMock()
    monkeypatch.setattr(mp, "set_movement_status", lambda uid, faction, value: None)
    monkeypatch.setattr(mp, "log_action", lambda *a, **kw: None)

    mp._active_movement("Necrons", "u1", unit, unit_state, {})

    assert session.pending_fall_back == {"faction": "Necrons", "uid": "u1"}
    mp.st.rerun.assert_called_once()


def test_move_click_does_not_set_pending_fall_back_marker(monkeypatch) -> None:
    """A non-Retreat movement choice must not open the reactive window."""
    unit = SimpleNamespace(name_en="Necron Warriors", get_triggered_effect=lambda *a, **kw: None)
    unit_state = {
        "in_reserve": False,
        "in_melee": False,
        "movement_choice": None,
        "turn_flags": {},
    }
    session = FakeSessionState(round=3, pending_fall_back=None)
    mp.st.session_state = session
    mp.st.button = lambda label, key=None, **kw: key == "mv_Necrons_u1_moved"
    mp.st.rerun = MagicMock()
    monkeypatch.setattr(mp, "set_movement_status", lambda uid, faction, value: None)
    monkeypatch.setattr(mp, "log_action", lambda *a, **kw: None)

    mp._active_movement("Necrons", "u1", unit, unit_state, {})

    assert session.pending_fall_back is None


# ---------------------------------------------------------------------------
# _render_pending_cut_them_down() — consumes the marker in the enemy's column
# ---------------------------------------------------------------------------


def test_no_marker_renders_nothing(monkeypatch) -> None:
    session = FakeSessionState(pending_fall_back=None)
    mp.st.session_state = session
    spy = MagicMock()
    monkeypatch.setattr(mp, "render_reactive_stratagem_box", spy)

    mp._render_pending_cut_them_down("Orks")

    spy.assert_not_called()


def test_marker_renders_box_for_enemy_of_retreating_faction(monkeypatch) -> None:
    """player: inactive → the box belongs to the OTHER faction, not the mover."""
    session = FakeSessionState(pending_fall_back={"faction": "Necrons", "uid": "u1"})
    mp.st.session_state = session
    warriors = SimpleNamespace(name_en="Necron Warriors")
    monkeypatch.setattr(mp, "lookup", lambda faction, uid: (warriors, {}))
    spy = MagicMock()
    monkeypatch.setattr(mp, "render_reactive_stratagem_box", spy)

    mp._render_pending_cut_them_down("Orks")

    spy.assert_called_once()
    call_kwargs = spy.call_args
    assert call_kwargs.args[0] == "Orks"  # enemy of the retreating faction
    assert call_kwargs.kwargs["phase"] == "movement"
    assert call_kwargs.kwargs["event"] == "on_declaration"
    assert call_kwargs.kwargs["decline_key"] == "u1"


def test_no_render_in_retreating_players_own_column(monkeypatch) -> None:
    """S139 E7 layout fix: called from the RETREATING player's own column, this
    must render nothing — the card belongs only in the enemy's column, never
    in both (regression for the pre-fix full-width/outside-columns bug)."""
    session = FakeSessionState(pending_fall_back={"faction": "Necrons", "uid": "u1"})
    mp.st.session_state = session
    warriors = SimpleNamespace(name_en="Necron Warriors")
    monkeypatch.setattr(mp, "lookup", lambda faction, uid: (warriors, {}))
    spy = MagicMock()
    monkeypatch.setattr(mp, "render_reactive_stratagem_box", spy)

    mp._render_pending_cut_them_down("Necrons")

    spy.assert_not_called()


def test_use_does_not_clear_marker_box_keeps_rendering(monkeypatch) -> None:
    """S139 B12b: the box no longer passes an `on_resolved` callback, so a Use
    does NOT clear `pending_fall_back` — the card stays visible ("used" at its
    own anchor, "used_elsewhere" elsewhere) for the rest of the phase, exactly
    like every non-window-consuming GO (S137/S138 concept §F3). The marker is
    cleared only at the phase boundary (`_reset_phase_state`)."""
    session = FakeSessionState(pending_fall_back={"faction": "Necrons", "uid": "u1"})
    mp.st.session_state = session
    warriors = SimpleNamespace(name_en="Necron Warriors")
    monkeypatch.setattr(mp, "lookup", lambda faction, uid: (warriors, {}))

    captured = {}

    def _fake_render(*args, **kwargs):  # type: ignore[no-untyped-def]
        captured["kwargs"] = kwargs

    monkeypatch.setattr(mp, "render_reactive_stratagem_box", _fake_render)

    mp._render_pending_cut_them_down("Orks")

    assert "on_resolved" not in captured["kwargs"]
    assert session.pending_fall_back == {"faction": "Necrons", "uid": "u1"}


def test_marker_for_unknown_unit_clears_itself(monkeypatch) -> None:
    """A stale marker pointing at a uid that no longer resolves is discarded."""
    session = FakeSessionState(pending_fall_back={"faction": "Necrons", "uid": "gone"})
    mp.st.session_state = session

    def _raise(*a, **kw):  # type: ignore[no-untyped-def]
        raise KeyError("gone")

    monkeypatch.setattr(mp, "lookup", _raise)
    spy = MagicMock()
    monkeypatch.setattr(mp, "render_reactive_stratagem_box", spy)

    mp._render_pending_cut_them_down("Orks")

    assert session.pending_fall_back is None
    spy.assert_not_called()
