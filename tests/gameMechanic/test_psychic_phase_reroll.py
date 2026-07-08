"""S130 — Command Re-Roll wiring for the Psychic Phase (manifest + Deny the Witch).

`_render_psi_result` / `_render_undo_deny_button` call render_inline_command_reroll
(uiLayout._common) at the exact spots where the manifest roll or the Deny the
Witch roll is still "the last roll" (core_rules.txt Z. 3124-3130) — gated so a
LATER roll (a deny attempt superseding the manifest) or an already-applied
Perils consequence correctly suppresses the offer.

These tests spy on render_inline_command_reroll rather than simulating full
widget interaction — its own visibility/spend contract is covered end-to-end
with real stratagem data in tests/uiLayout/test_common.py. Here the contract
under test is: WHEN psychicPhase calls it (faction/phase/gating), and whether
its on_reroll callback correctly reopens the state.
"""

from __future__ import annotations

import sys
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import MagicMock

sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

import gameMechanic.psychicPhase as pp  # noqa: E402


class _SS(dict):
    """Minimal session-state stand-in (attribute + key access)."""

    def __getattr__(self, name):  # type: ignore[no-untyped-def]
        try:
            return self[name]
        except KeyError as exc:
            raise AttributeError(name) from exc

    def __setattr__(self, name, value):  # type: ignore[no-untyped-def]
        self[name] = value


def _quiet_widgets(monkeypatch) -> None:  # type: ignore[no-untyped-def]
    monkeypatch.setattr(pp.st, "markdown", lambda *a, **kw: None)
    monkeypatch.setattr(pp.st, "caption", lambda *a, **kw: None)
    monkeypatch.setattr(pp.st, "error", lambda *a, **kw: None)
    monkeypatch.setattr(pp.st, "warning", lambda *a, **kw: None)
    monkeypatch.setattr(pp.st, "success", lambda *a, **kw: None)
    monkeypatch.setattr(pp.st, "number_input", lambda *a, **kw: 2)
    monkeypatch.setattr(pp.st, "button", lambda *a, **kw: False)


def _base_psi(**overrides):  # type: ignore[no-untyped-def]
    psi = {
        "faction": "Necrons",
        "uid": "cryptek#1",
        "roll": 7,
        "manifested": True,
        "perils": False,
        "perils_applied": False,
        "denied": None,
        "deny_roll": None,
        "deny_faction": None,
    }
    psi.update(overrides)
    return psi


def _state():  # type: ignore[no-untyped-def]
    return {"round": 2, "first_player": "Necrons", "second_player": "Orks"}


# ---------------------------------------------------------------------------
# Manifest roll — offered only while it is still "the last roll"
# ---------------------------------------------------------------------------


def test_manifest_reroll_offered_when_failed(monkeypatch) -> None:
    _quiet_widgets(monkeypatch)
    pp.st.session_state = _SS(selected_targets=[])
    spy = MagicMock()
    monkeypatch.setattr(pp, "render_inline_command_reroll", spy)
    unit = SimpleNamespace(name_en="Cryptek")

    pp._render_psi_result("Necrons", "cryptek#1", unit, _base_psi(manifested=False), _state())

    spy.assert_called_once()
    call = spy.call_args
    assert call.args[0] == "Necrons"
    assert call.args[1] == "psychic"
    assert call.kwargs["reopen_key"] == "psi_manifest_cryptek#1"


def test_manifest_reroll_offered_while_waiting_for_deny(monkeypatch) -> None:
    _quiet_widgets(monkeypatch)
    pp.st.session_state = _SS(selected_targets=[])
    spy = MagicMock()
    monkeypatch.setattr(pp, "render_inline_command_reroll", spy)
    unit = SimpleNamespace(name_en="Cryptek")
    psi = _base_psi(denied=None, deny_faction=None)

    pp._render_psi_result("Necrons", "cryptek#1", unit, psi, _state())

    spy.assert_called_once()


def test_manifest_reroll_offered_when_no_deny_possible(monkeypatch) -> None:
    _quiet_widgets(monkeypatch)
    pp.st.session_state = _SS(selected_targets=[])
    spy = MagicMock()
    monkeypatch.setattr(pp, "render_inline_command_reroll", spy)
    unit = SimpleNamespace(name_en="Cryptek")
    psi = _base_psi(denied=False, deny_faction=None)

    pp._render_psi_result("Necrons", "cryptek#1", unit, psi, _state())

    spy.assert_called_once()


def test_manifest_reroll_not_offered_once_denied(monkeypatch) -> None:
    """A deny roll is a LATER roll — the manifest is no longer "the last roll"."""
    _quiet_widgets(monkeypatch)
    pp.st.session_state = _SS(selected_targets=[])
    spy = MagicMock()
    monkeypatch.setattr(pp, "render_inline_command_reroll", spy)
    unit = SimpleNamespace(name_en="Cryptek")
    psi = _base_psi(denied=True, deny_roll=9, deny_faction="Orks")

    pp._render_psi_result("Necrons", "cryptek#1", unit, psi, _state())

    spy.assert_not_called()


def test_manifest_reroll_not_offered_after_deny_failed(monkeypatch) -> None:
    _quiet_widgets(monkeypatch)
    pp.st.session_state = _SS(selected_targets=[])
    spy = MagicMock()
    monkeypatch.setattr(pp, "render_inline_command_reroll", spy)
    unit = SimpleNamespace(name_en="Cryptek")
    psi = _base_psi(denied=False, deny_roll=5, deny_faction="Orks")

    pp._render_psi_result("Necrons", "cryptek#1", unit, psi, _state())

    spy.assert_not_called()


def test_manifest_reroll_offered_during_perils_pending(monkeypatch) -> None:
    _quiet_widgets(monkeypatch)
    pp.st.session_state = _SS(selected_targets=[])
    spy = MagicMock()
    monkeypatch.setattr(pp, "render_inline_command_reroll", spy)
    unit = SimpleNamespace(name_en="Cryptek")
    psi = _base_psi(roll=12, perils=True, perils_applied=False, manifested=True)

    pp._render_psi_result("Necrons", "cryptek#1", unit, psi, _state())

    spy.assert_called_once()


def test_manifest_reroll_not_offered_after_perils_applied(monkeypatch) -> None:
    """Perils mortal wounds already landed — a real consequence this app
    cannot cleanly undo, so the offer stops appearing once it lands."""
    _quiet_widgets(monkeypatch)
    pp.st.session_state = _SS(selected_targets=[])
    spy = MagicMock()
    monkeypatch.setattr(pp, "render_inline_command_reroll", spy)
    unit = SimpleNamespace(name_en="Cryptek")
    psi = _base_psi(roll=2, perils=True, perils_applied=True, manifested=False)

    pp._render_psi_result("Necrons", "cryptek#1", unit, psi, _state())

    spy.assert_not_called()


def test_manifest_reroll_on_reroll_resets_active_power(monkeypatch) -> None:
    _quiet_widgets(monkeypatch)
    session = _SS(selected_targets=[], psychic_denies_used={})
    pp.st.session_state = session
    captured = {}

    def _fake_reroll(faction, phase, *, reopen_key, on_reroll):  # type: ignore[no-untyped-def]
        captured["on_reroll"] = on_reroll

    monkeypatch.setattr(pp, "render_inline_command_reroll", _fake_reroll)
    unit = SimpleNamespace(name_en="Cryptek")
    psi = _base_psi(manifested=False)
    session.psi_result = psi

    pp._render_psi_result("Necrons", "cryptek#1", unit, psi, _state())
    captured["on_reroll"]()

    assert session.psi_result is None


# ---------------------------------------------------------------------------
# Deny the Witch roll — offered only for an actual roll, never a Skip
# ---------------------------------------------------------------------------


def test_deny_reroll_offered_when_deny_roll_was_made(monkeypatch) -> None:
    _quiet_widgets(monkeypatch)
    pp.st.session_state = _SS()
    spy = MagicMock()
    monkeypatch.setattr(pp, "render_inline_command_reroll", spy)
    psi = _base_psi(denied=True, deny_roll=9, deny_faction="Orks")

    pp._render_undo_deny_button("Orks", psi, {"Orks": True})

    spy.assert_called_once()
    call = spy.call_args
    assert call.args[0] == "Orks"
    assert call.args[1] == "psychic"


def test_deny_reroll_not_offered_when_deny_was_skipped(monkeypatch) -> None:
    _quiet_widgets(monkeypatch)
    pp.st.session_state = _SS()
    spy = MagicMock()
    monkeypatch.setattr(pp, "render_inline_command_reroll", spy)
    psi = _base_psi(denied=False, deny_roll=None, deny_faction="Orks")

    pp._render_undo_deny_button("Orks", psi, {"Orks": True})

    spy.assert_not_called()


def test_deny_reroll_on_reroll_reopens_and_refunds_budget(monkeypatch) -> None:
    _quiet_widgets(monkeypatch)
    pp.st.session_state = _SS()
    captured = {}

    def _fake_reroll(faction, phase, *, reopen_key, on_reroll):  # type: ignore[no-untyped-def]
        captured["on_reroll"] = on_reroll

    monkeypatch.setattr(pp, "render_inline_command_reroll", _fake_reroll)
    psi = _base_psi(denied=True, deny_roll=9, deny_faction="Orks")
    denies_used = {"Orks": True}

    pp._render_undo_deny_button("Orks", psi, denies_used)
    captured["on_reroll"]()

    assert pp.st.session_state.psi_result["denied"] is None
    assert pp.st.session_state.psi_result["deny_roll"] is None
    assert pp.st.session_state.psychic_denies_used == {}
