"""Regression tests: fight_current_player changes must trigger st.rerun().

Bug: app.py renders the left army column before the fight phase handler runs.
A silent fight_current_player switch left that column with stale buttons —
selecting a unit then needed two clicks (the first click hit a stale target
button and added the own unit to selected_targets).
"""

import sys
from pathlib import Path
from unittest.mock import MagicMock

sys.modules.setdefault("streamlit", MagicMock())
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

import gameMechanic.fightPhase as fp  # noqa: E402


class FakeSessionState(dict):
    """Dict with attribute access — mirrors streamlit's session_state API."""

    def __getattr__(self, name):  # type: ignore[no-untyped-def]
        try:
            return self[name]
        except KeyError as exc:
            raise AttributeError(name) from exc

    def __setattr__(self, name, value):  # type: ignore[no-untyped-def]
        self[name] = value


def _unit_state(*, fought: bool = False, in_melee: bool = True, charged: bool = False) -> dict:
    return {
        "destroyed": False,
        "in_melee": in_melee,
        "in_reserve": False,
        "turn_flags": {"fought": fought, "charged": charged},
    }


def _setup(monkeypatch, *, a_state: dict, b_state: dict, current: str, selected) -> None:  # type: ignore[no-untyped-def]
    monkeypatch.setattr(fp, "units_key_for", lambda player: f"{player}_units")
    monkeypatch.setattr(fp, "lookup", lambda faction, uid: (None, a_state))
    fp.st.session_state = FakeSessionState(
        fight_current_player=current,
        selected_unit=selected,
        selected_targets=[],
        A_units={"u1": a_state},
        B_units={"u2": b_state},
    )
    fp.st.rerun = MagicMock()


def test_no_advance_while_resolution_active(monkeypatch) -> None:  # type: ignore[no-untyped-def]
    """The fought flag is set on the first Apply Damage — the turn must not pass
    until the resolution is finished (All done — Continue)."""
    a_state = _unit_state(fought=True)
    b_state = _unit_state()
    _setup(monkeypatch, a_state=a_state, b_state=b_state, current="A", selected=("A", "u1"))
    fp.st.session_state.attack_declaration = {"active": True, "entries": []}

    fp._advance_fight_turn_if_needed("A", "B")

    assert fp.st.session_state.fight_current_player == "A"
    assert fp.st.session_state.selected_unit == ("A", "u1")
    fp.st.rerun.assert_not_called()


def test_switch_after_fought_triggers_rerun(monkeypatch) -> None:  # type: ignore[no-untyped-def]
    a_state = _unit_state(fought=True)
    b_state = _unit_state()
    _setup(monkeypatch, a_state=a_state, b_state=b_state, current="A", selected=("A", "u1"))

    fp._advance_fight_turn_if_needed("A", "B")

    assert fp.st.session_state.fight_current_player == "B"
    assert fp.st.session_state.selected_unit is None
    fp.st.rerun.assert_called_once()


def test_auto_skip_to_other_player_triggers_rerun(monkeypatch) -> None:  # type: ignore[no-untyped-def]
    a_state = _unit_state(fought=True)  # A has no eligible units left
    b_state = _unit_state()
    _setup(monkeypatch, a_state=a_state, b_state=b_state, current="A", selected=None)

    fp._advance_fight_turn_if_needed("A", "B")

    assert fp.st.session_state.fight_current_player == "B"
    fp.st.rerun.assert_called_once()


def test_advanced_unit_in_melee_is_eligible_and_receives_turn(monkeypatch) -> None:  # type: ignore[no-untyped-def]
    """P20: ADVANCED blocks charge/shoot but NOT fighting (RAW). A unit that was
    heroically intervened into (or advanced and got engaged) must be eligible,
    and the fight turn must pass to its player."""
    scarabs = {
        "destroyed": False,
        "in_melee": True,
        "in_reserve": False,
        "movement_choice": "advanced",
        "turn_flags": {"fought": False, "charged": False, "advanced": True},
    }
    fought_char = _unit_state(fought=True)
    _setup(monkeypatch, a_state=fought_char, b_state=scarabs, current="A", selected=("A", "u1"))

    assert fp.can_fight(scarabs) is True
    assert fp.can_fight_now(scarabs, "A", "B") is True

    fp._advance_fight_turn_if_needed("A", "B")
    assert fp.st.session_state.fight_current_player == "B"


def test_no_change_means_no_rerun(monkeypatch) -> None:  # type: ignore[no-untyped-def]
    a_state = _unit_state()
    b_state = _unit_state()
    _setup(monkeypatch, a_state=a_state, b_state=b_state, current="A", selected=("A", "u1"))

    fp._advance_fight_turn_if_needed("A", "B")

    assert fp.st.session_state.fight_current_player == "A"
    fp.st.rerun.assert_not_called()


def test_none_current_player_returns_without_rerun(monkeypatch) -> None:  # type: ignore[no-untyped-def]
    a_state = _unit_state()
    b_state = _unit_state()
    _setup(monkeypatch, a_state=a_state, b_state=b_state, current=None, selected=None)

    fp._advance_fight_turn_if_needed("A", "B")

    assert fp.st.session_state.fight_current_player is None
    fp.st.rerun.assert_not_called()
