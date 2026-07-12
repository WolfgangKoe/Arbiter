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


def test_ork_faction_keyword_filtered_despite_case_and_plural_mismatch() -> None:
    """S138 root cause: real Ork data carries the singular uppercase keyword
    "ORK" while unit.faction is "Orks" (Title Case, plural) — the naive
    ``kw != unit.faction`` check never matched, leaking the faction keyword
    into the card. Case+plural folding must filter it out."""
    unit = _make_unit(["ORK", "BAD MOONS", "INFANTRY", "MOB", "CORE", "BOYZ"], faction="Orks")
    _st_mock.session_state = {}
    html = _keywords_html(unit)
    assert ">ORK<" not in html
    assert ">BAD MOONS<" in html
    assert ">CORE<" in html
    assert ">BOYZ<" in html


def test_necron_faction_keyword_still_filtered_after_folding() -> None:
    """Regression guard: the fold must not break the previously-working case
    (NECRONS keyword vs. Necrons faction, exact plural match already)."""
    unit = _make_unit(["NECRONS", "NEPHREKH", "INFANTRY", "CORE"], faction="Necrons")
    _st_mock.session_state = {}
    html = _keywords_html(unit)
    assert ">NECRONS<" not in html
    assert ">NEPHREKH<" in html


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
    cast: bool = False,
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
            "cast": cast,
        },
        "in_melee": in_melee,
        "in_reserve": in_reserve,
        "active_buffs": (
            [{"ability_id": "mwbd", "badge_label": "MWBD", "effect_type": "buff_roll"}]
            if mwbd
            else []
        ),
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


# ---------------------------------------------------------------------------
# State/buff group separator — <br> only when BOTH groups are non-empty (S137)
# ---------------------------------------------------------------------------


def test_separator_between_state_and_buff_groups() -> None:
    html = _state_badges_html(_state(movement_choice="moved", mwbd=True))
    assert "MOVED" in html
    assert "MWBD" in html
    assert html.count("<br>") == 1
    # State group comes first, buff group after the separator
    assert html.index("MOVED") < html.index("<br>") < html.index("MWBD")


def test_no_separator_when_only_state_group() -> None:
    html = _state_badges_html(_state(movement_choice="moved", shot=True))
    assert "<br>" not in html


def test_no_separator_when_only_buff_group() -> None:
    html = _state_badges_html(_state(mwbd=True))
    assert "<br>" not in html


def test_caller_buff_badge_without_active_buffs_gets_separator() -> None:
    """Army-ability/protocol badges passed by the caller are buff badges:
    they belong behind the separator even when active_buffs is empty."""
    from uiLayout.unitCard import _badge

    html = _state_badges_html(
        _state(movement_choice="moved"),
        extra_buff_badges=[_badge("ARMY ABILITY", variant="buff")],
    )
    assert html.count("<br>") == 1
    assert html.index("MOVED") < html.index("<br>") < html.index("ARMY ABILITY")


def test_caller_buff_badge_without_state_group_has_no_separator() -> None:
    from uiLayout.unitCard import _badge

    html = _state_badges_html(
        _state(),
        extra_buff_badges=[_badge("ARMY ABILITY", variant="buff")],
    )
    assert "ARMY ABILITY" in html
    assert "<br>" not in html


# ---------------------------------------------------------------------------
# CAST badge — turn_flags["cast"] (psychicPhase Smite) renders in the state
# group with the --arb-blue family colours (S137 decision, design_colors.md §2)
# ---------------------------------------------------------------------------


def test_cast_flag_renders_cast_badge_with_blue_family_colors() -> None:
    html = _state_badges_html(_state(cast=True))
    assert "CAST" in html
    assert "#93c5fd" in html
    assert "#1e3a8a" in html


def test_cast_badge_belongs_to_state_group() -> None:
    html = _state_badges_html(_state(cast=True, mwbd=True))
    # CAST is a state badge → it stands before the group separator
    assert html.index("CAST") < html.index("<br>") < html.index("MWBD")


def test_no_cast_badge_without_cast_flag() -> None:
    html = _state_badges_html(_state(shot=True))
    assert "CAST" not in html


# ---------------------------------------------------------------------------
# _TARGET_PHASES — #PSI regression (S129): the psychic phase must offer the
# inactive player's unit cards as Smite target selectors. Without "psychic"
# here no enemy card is clickable, selected_targets stays empty and the Smite
# damage button can never appear.
# ---------------------------------------------------------------------------


def test_psychic_phase_offers_enemy_cards_as_smite_target_selectors() -> None:
    from uiLayout.unitCard import _TARGET_PHASES

    assert "psychic" in _TARGET_PHASES


def test_target_phases_keep_the_existing_attack_phases() -> None:
    from uiLayout.unitCard import _TARGET_PHASES

    assert {"shooting", "charge", "fight"} <= _TARGET_PHASES


# ---------------------------------------------------------------------------
# _self_select_eligible — Bugfix A regression (S143): the inactive player must
# be able to self-select their own unit in the Morale phase (e.g. to pick the
# unit an Insane Bravery `player: both` stratagem applies to). Before the fix
# the inactive player's own-unit cards fell through to the target-selector
# branch, which only offers a button in `_TARGET_PHASES` — Morale is not one
# of those, so no button (and no `selected_unit`) was ever offered.
# ---------------------------------------------------------------------------


def test_inactive_player_can_self_select_in_morale_phase() -> None:
    from uiLayout.unitCard import _self_select_eligible

    assert _self_select_eligible("morale", is_active=False) is True


def test_active_player_can_always_self_select() -> None:
    from uiLayout.unitCard import _self_select_eligible

    assert _self_select_eligible("shooting", is_active=True) is True
    assert _self_select_eligible("morale", is_active=True) is True


def test_inactive_player_still_cannot_self_select_in_turn_based_phases() -> None:
    from uiLayout.unitCard import _self_select_eligible

    assert _self_select_eligible("shooting", is_active=False) is False
    assert _self_select_eligible("charge", is_active=False) is False
    assert _self_select_eligible("fight", is_active=False) is False
