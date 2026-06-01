"""Tests for unitCard — keyword filtering, highlighting, and badge logic."""

import sys
from pathlib import Path
from unittest.mock import MagicMock

_st_mock = MagicMock()
_st_mock.session_state = {}
sys.modules["streamlit"] = _st_mock
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

from gameObjects.unit import Unit  # noqa: E402
from uiLayout.unitCard import _keywords_html, _state_badges_html  # noqa: E402


def _make_unit(keywords: list[str], faction: str = "Necrons") -> Unit:
    return Unit(
        id="test.unit",
        name_en="Test Unit",
        name_de="Test",
        faction=faction,
        subfaction="Nephrekh",
        battlefield_role=["Troops"],
        keywords=keywords,
        wounds=1,
        models_min=1,
        models_max=5,
        power_level=3,
        move='6"',
        bs="3+",
        ws="3+",
        strength=4,
        toughness=4,
        attacks=1,
        save=4,
        invuln_save=None,
        leadership=10,
        oc=2,
        fnp=None,
    )


# ---------------------------------------------------------------------------
# Keyword filtering — main faction keyword excluded
# ---------------------------------------------------------------------------


def test_faction_keyword_excluded_from_display() -> None:
    unit = _make_unit(["Necrons", "Nephrekh", "Infantry", "Core"])
    _st_mock.session_state = {}
    html = _keywords_html(unit)
    assert "Necrons" not in html
    assert "Nephrekh" in html
    assert "Infantry" in html
    assert "Core" in html


def test_subfaction_keyword_shown() -> None:
    unit = _make_unit(["Orks", "Bad Moons", "Infantry"], faction="Orks")
    _st_mock.session_state = {}
    html = _keywords_html(unit)
    assert "Orks" not in html
    assert "Bad Moons" in html
    assert "Infantry" in html


def test_no_keywords_returns_empty() -> None:
    unit = _make_unit(["Necrons"], faction="Necrons")
    _st_mock.session_state = {}
    html = _keywords_html(unit)
    assert html == ""


# ---------------------------------------------------------------------------
# Keyword highlighting — all-or-nothing
# ---------------------------------------------------------------------------


def test_highlight_all_keywords_when_unit_qualifies() -> None:
    unit = _make_unit(["Necrons", "Nephrekh", "Infantry", "Core"])
    _st_mock.session_state = {"highlight_keywords": ["Core", "Infantry"]}
    html = _keywords_html(unit)
    # Each highlighted chip has bg #3a2e10 exactly once — two highlighted keywords → count == 2
    assert html.count("#3a2e10") == 2


def test_no_highlight_when_unit_missing_one_keyword() -> None:
    unit = _make_unit(["Necrons", "Nephrekh", "Infantry"])
    _st_mock.session_state = {"highlight_keywords": ["Core", "Infantry"]}
    html = _keywords_html(unit)
    # Unit lacks "Core" → all-or-nothing: no highlights
    assert "#f5d080" not in html


def test_no_highlight_when_highlight_keywords_empty() -> None:
    unit = _make_unit(["Necrons", "Nephrekh", "Infantry", "Core"])
    _st_mock.session_state = {"highlight_keywords": []}
    html = _keywords_html(unit)
    assert "#f5d080" not in html


def test_highlight_single_keyword_qualifies() -> None:
    unit = _make_unit(["Necrons", "Nephrekh", "Core"])
    _st_mock.session_state = {"highlight_keywords": ["Core"]}
    html = _keywords_html(unit)
    assert "#f5d080" in html


def test_highlight_main_faction_keyword_not_shown_even_if_required() -> None:
    """Even if highlight_keywords includes the main faction keyword, it's not rendered."""
    unit = _make_unit(["Necrons", "Nephrekh", "Core"])
    _st_mock.session_state = {"highlight_keywords": ["Necrons", "Core"]}
    html = _keywords_html(unit)
    # "Necrons" is the main faction keyword — filtered out, never in html
    assert "Necrons" not in html


# ---------------------------------------------------------------------------
# State badges — regression guard for layout change (badges still render)
# ---------------------------------------------------------------------------


def _state(
    movement_choice: str | None = None,
    charged: bool = False,
    shot: bool = False,
    fought: bool = False,
    in_melee: bool = False,
    in_reserve: bool = False,
    mwbd: bool = False,
) -> dict:
    return {
        "movement_choice": movement_choice,
        "turn_flags": {
            "advanced": movement_choice == "advanced",
            "retreated": movement_choice == "retreated",
            "charged": charged,
            "shot": shot,
            "fought": fought,
        },
        "in_melee": in_melee,
        "in_reserve": in_reserve,
        "my_will_be_done_active": mwbd,
    }


def test_state_badges_moved() -> None:
    html = _state_badges_html(_state(movement_choice="moved"))
    assert "MOVED" in html


def test_state_badges_mwbd_shown() -> None:
    html = _state_badges_html(_state(mwbd=True))
    assert "MWBD" in html


def test_state_badges_empty_state_returns_empty() -> None:
    html = _state_badges_html(_state())
    assert html == ""
