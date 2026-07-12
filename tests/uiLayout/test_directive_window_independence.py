"""Regression: the main directive and the extra directive are chosen independently.

Bug (Plan 031): a single ``directive_pending`` flag per player gated BOTH the main
directive's selection window and the extra directive's window. Choosing one closed
the other, so a player with two real choices (round-assigned protocol + extra
protocol with a real directive choice) lost the second choice and its effect.

Rule basis — Wahapedia faction_overview.txt Z. 568 + Z. 579: both the main and the
extra directive are selected "at the start of each battle round", independently. The
fix gates each window on (directive_pending AND that directive's own key is None), so
the two windows open and close independently. These tests pin that independence.
"""

import sys
from pathlib import Path
from unittest.mock import MagicMock

_st_mock = MagicMock()
sys.modules["streamlit"] = _st_mock
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

import uiLayout.armyCard as _army  # noqa: E402
from gameMechanic.gameState import round_choice_state_key  # noqa: E402
from uiLayout.armyCard import _directive_window_open  # noqa: E402


class _S(dict):
    def __getattr__(self, key: str):  # type: ignore[override]
        try:
            return self[key]
        except KeyError:
            raise AttributeError(key)

    def __setattr__(self, key: str, value: object) -> None:
        self[key] = value


def _install(session: "_S") -> None:
    _army.st.session_state = session


def _round_start_session(player: str = "P1") -> _S:
    """Session as it is right after a round-start reset: window open, nothing chosen."""
    session = _S()
    session[round_choice_state_key(player, "directive_pending")] = True
    session[round_choice_state_key(player, "directive")] = None
    session[round_choice_state_key(player, "extra_directive")] = None
    return session


def test_both_windows_open_at_round_start() -> None:
    session = _round_start_session()
    _install(session)
    assert _directive_window_open("P1", "directive") is True
    assert _directive_window_open("P1", "extra_directive") is True


def test_choosing_main_directive_keeps_extra_window_open() -> None:
    """The core regression: picking the main directive must NOT close the extra window."""
    session = _round_start_session()
    session[round_choice_state_key("P1", "directive")] = "primary"
    _install(session)

    # Main window now closed (own choice made), extra window still open.
    assert _directive_window_open("P1", "directive") is False
    assert _directive_window_open("P1", "extra_directive") is True


def test_choosing_extra_directive_keeps_main_window_open() -> None:
    """Symmetric: picking the extra directive must NOT close the main window."""
    session = _round_start_session()
    session[round_choice_state_key("P1", "extra_directive")] = "secondary"
    _install(session)

    assert _directive_window_open("P1", "extra_directive") is False
    assert _directive_window_open("P1", "directive") is True


def test_both_directives_can_be_set_and_stay_set() -> None:
    """Player with two real choices: both get set and both persist independently."""
    session = _round_start_session()
    _install(session)

    # Choose main, then extra — neither write disturbs the other key.
    session[round_choice_state_key("P1", "directive")] = "primary"
    session[round_choice_state_key("P1", "extra_directive")] = "secondary"

    assert session[round_choice_state_key("P1", "directive")] == "primary"
    assert session[round_choice_state_key("P1", "extra_directive")] == "secondary"
    # Both windows are now closed (each by its own choice), no reopen mid-round.
    assert _directive_window_open("P1", "directive") is False
    assert _directive_window_open("P1", "extra_directive") is False


def test_window_closed_when_pending_false_even_if_unchosen() -> None:
    """Outside the round-start window (pending False) no window is open."""
    session = _S()
    session[round_choice_state_key("P1", "directive_pending")] = False
    session[round_choice_state_key("P1", "directive")] = None
    session[round_choice_state_key("P1", "extra_directive")] = None
    _install(session)

    assert _directive_window_open("P1", "directive") is False
    assert _directive_window_open("P1", "extra_directive") is False
