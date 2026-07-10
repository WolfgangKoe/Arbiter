"""Regression tests for the First Player block (Stakeholder-Beobachtung B5,
docs/goals/backlog.md §2 / Screenshot docs/handoff/*21-23-28*.png).

Stakeholder wording (fixed, no design question):
- heading → "Roll-Off for First Player"
- selection buttons show only the army name (no "goes first" suffix)
- the "Currently selected: ..." caption is removed entirely

``_render_setup`` is exercised with a mocked ``streamlit`` module, asserting
on the recorded call arguments — there is no rendered-HTML-string test
pattern for uiLayout modules in this codebase (they are coverage-excluded,
see pyproject.toml). The mock is injected per-test via ``monkeypatch`` on the
module attribute (not only via ``sys.modules``), so the tests are independent
of which uiLayout test module imported ``gameActionsArea`` first in the full
suite run.
"""

import sys
from pathlib import Path
from unittest.mock import MagicMock

if "streamlit" not in sys.modules:
    sys.modules["streamlit"] = MagicMock()
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

from uiLayout import gameActionsArea as gaa  # noqa: E402


class _SessionState(dict):
    """Minimal stand-in for st.session_state — supports both ``sst["k"]`` and
    ``sst.k`` access, like the real Streamlit object."""

    def __getattr__(self, name: str) -> object:
        try:
            return self[name]
        except KeyError as exc:
            raise AttributeError(name) from exc

    def __setattr__(self, name: str, value: object) -> None:
        self[name] = value


def _fresh_st_mock() -> MagicMock:
    st_mock = MagicMock()
    st_mock.button.return_value = False
    st_mock.columns.return_value = (MagicMock(), MagicMock())
    st_mock.session_state = _SessionState(
        {
            "player_slots": ("Necrons 1500pts", "Necrons alpha"),
            "first_player": "Necrons 1500pts",
            "second_player": "Necrons alpha",
            "selected_unit": None,
            "round_choice_assignments": {},
        }
    )
    return st_mock


def _run_render_setup(monkeypatch) -> MagicMock:  # type: ignore[no-untyped-def]
    st_mock = _fresh_st_mock()
    monkeypatch.setattr(gaa, "st", st_mock)
    monkeypatch.setattr(gaa, "faction_dir_for", lambda *_: "necrons")
    monkeypatch.setattr(gaa, "load_round_choice_abilities", lambda *_: [])
    gaa._render_setup()
    return st_mock


def test_heading_says_roll_off_for_first_player(monkeypatch) -> None:  # type: ignore[no-untyped-def]
    st_mock = _run_render_setup(monkeypatch)
    markdown_texts = [c.args[0] for c in st_mock.markdown.call_args_list if c.args]
    assert "**Roll-Off for First Player**" in markdown_texts
    assert not any(text == "**First Player**" for text in markdown_texts)


def test_buttons_show_only_army_name(monkeypatch) -> None:  # type: ignore[no-untyped-def]
    st_mock = _run_render_setup(monkeypatch)
    button_labels = [c.args[0] for c in st_mock.button.call_args_list if c.args]
    assert "Necrons 1500pts" in button_labels
    assert "Necrons alpha" in button_labels
    assert not any("goes first" in label for label in button_labels if isinstance(label, str))


def test_currently_selected_caption_removed(monkeypatch) -> None:  # type: ignore[no-untyped-def]
    st_mock = _run_render_setup(monkeypatch)
    caption_texts = [c.args[0] for c in st_mock.caption.call_args_list if c.args]
    assert not any("Currently selected" in text for text in caption_texts if isinstance(text, str))
