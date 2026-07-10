"""Tests for gameActionsArea — setup-phase datasheet stat row.

Regression coverage for Stakeholder-Beobachtung 4 (docs/handoff/
Stakeholder_Beobachtungen.md): the movement value rendered with a doubled
inch mark (``6""``) and the stat column order did not follow the 9E
datasheet convention.
"""

import sys
from pathlib import Path
from unittest.mock import MagicMock

_st_mock = MagicMock()
_st_mock.session_state = {}
sys.modules["streamlit"] = _st_mock
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

from gameObjects.unit import Unit  # noqa: E402
from uiLayout.gameActionsArea import _datasheet_stat_row  # noqa: E402


def _make_unit(**overrides: object) -> Unit:
    defaults: dict = {
        "id": "test.unit",
        "name_en": "Test Unit",
        "name_de": "Test",
        "faction": "Necrons",
        "subfaction": None,
        "battlefield_role": ["Troops"],
        "keywords": ["Necrons", "Infantry"],
        "wounds": 5,
        "models_min": 1,
        "models_max": 1,
        "power_level": 6,
        "move": '6"',
        "bs": "2+",
        "ws": "2+",
        "strength": 5,
        "toughness": 5,
        "attacks": 4,
        "save": 3,
        "invuln_save": 4,
        "leadership": 10,
        "oc": 1,
        "fnp": None,
    }
    defaults.update(overrides)
    return Unit(**defaults)


# ---------------------------------------------------------------------------
# Defect 1 — doubled inch mark on the Move value (Beobachtung 4)
# ---------------------------------------------------------------------------


def test_move_value_has_single_inch_mark() -> None:
    unit = _make_unit(move='6"')
    stats = dict(_datasheet_stat_row(unit))
    assert stats["M"] == '6"'
    assert stats["M"] != '6""'


# ---------------------------------------------------------------------------
# Defect 2 — stat order must follow the 9E datasheet convention
# M WS BS S T W A Ld Sv (core_rules.txt, "4. Profiles"), app-specific ++/OC
# appended at the end.
# ---------------------------------------------------------------------------


def test_stat_row_follows_9e_datasheet_order() -> None:
    unit = _make_unit()
    labels = [lbl for lbl, _ in _datasheet_stat_row(unit)]
    assert labels == ["M", "WS", "BS", "S", "T", "W", "A", "Ld", "Sv", "++", "OC"]


def test_stat_row_values_match_unit_characteristics() -> None:
    unit = _make_unit(
        move='8"', ws="3+", bs="4+", strength=6, toughness=7, wounds=8, attacks=2, leadership=9
    )
    stats = dict(_datasheet_stat_row(unit))
    assert stats["M"] == '8"'
    assert stats["WS"] == "3+"
    assert stats["BS"] == "4+"
    assert stats["S"] == "6"
    assert stats["T"] == "7"
    assert stats["W"] == "8"
    assert stats["A"] == "2"
    assert stats["Ld"] == "9"
    assert stats["Sv"] == f"{unit.save}+"


def test_stat_row_handles_missing_attacks_and_leadership() -> None:
    unit = _make_unit(attacks=None, leadership=None, invuln_save=None)
    stats = dict(_datasheet_stat_row(unit))
    assert stats["A"] == "—"
    assert stats["Ld"] == "—"
    assert stats["++"] == "—"
