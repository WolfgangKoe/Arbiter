"""Acceptance: Subfaction- & Faktion-Badge (Finding #1).

Pins AC-SUBFACTION-01..05 from docs/spec/acceptance/index.md. The badge is
always rendered — a chosen value, a visible 'No <Label>' placeholder, or a
visible 'No Subfaction' error; never empty.

NOTE on imports: this module deliberately imports ``gameState`` *lazily* (inside
the tests), not at module top. The tests in tests/gameMechanic/ install per-file
mocks for ``streamlit`` and rely on ``gameState``/``unitMutations`` sharing the
mock that the first importer binds. Since tests/acceptance/ is collected first, a
top-level import here would make this module that first importer and split the
binding, breaking those tests. Deferring the import lets the gameMechanic modules
bind it (during collection) before any test runs.
"""

from __future__ import annotations

import sys
from pathlib import Path
from unittest.mock import MagicMock

import pytest

sys.modules.setdefault("streamlit", MagicMock())
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))

from tests.acceptance._acceptance import acceptance  # noqa: E402


class _S(dict):
    def __getattr__(self, key: str):
        try:
            return self[key]
        except KeyError:
            raise AttributeError(key)

    def __setattr__(self, key: str, value: object) -> None:
        self[key] = value


def _gs():
    import gameMechanic.gameState as gs  # noqa: PLC0415

    return gs


@pytest.fixture(autouse=True)
def _isolate_session_state():
    """Don't leak our dict-based session_state into other modules sharing the
    streamlit mock — restore an ambient MagicMock after each test."""
    yield
    _gs().st.session_state = MagicMock()


def _session(faction_dir: str, subfaction: str | None) -> None:
    _gs().st.session_state = _S(
        first_player="P1",
        second_player="P2",
        p1_faction_dir=faction_dir,
        p2_faction_dir="orks",
        p1_subfaction=subfaction,
        p2_subfaction=None,
    )


@acceptance("AC-SUBFACTION-01")
def test_necron_dynasty_set_shows_titlecased_value() -> None:
    _session("necrons", "szarekhan")
    badge = _gs().subfaction_badge_for("P1")
    assert badge.state == "set"
    assert badge.text == "Szarekhan"


@acceptance("AC-SUBFACTION-02")
def test_ork_clan_set_resolves_via_generic_field() -> None:
    _session("orks", "bad_moons")
    badge = _gs().subfaction_badge_for("P1")
    assert badge.state == "set"
    assert badge.text == "Bad Moons"


@acceptance("AC-SUBFACTION-03")
def test_valid_roster_without_choice_shows_visible_placeholder() -> None:
    _session("necrons", None)
    badge = _gs().subfaction_badge_for("P1")
    assert badge.state == "missing"
    assert badge.text == "No Dynasty"


@acceptance("AC-SUBFACTION-04")
def test_faction_without_subfaction_field_shows_error_badge() -> None:
    _session("faction_without_binding", "anything")
    badge = _gs().subfaction_badge_for("P1")
    assert badge.state == "error"
    assert badge.text == "No Subfaction"


@acceptance("AC-SUBFACTION-05")
def test_faction_badge_uses_faction_name_not_roster_title() -> None:
    _session("necrons", "szarekhan")
    assert _gs().faction_display_name_for("P1") == "Necrons"
