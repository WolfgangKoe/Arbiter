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


def test_non_charged_waits_while_charged_pending(monkeypatch) -> None:  # type: ignore[no-untyped-def]
    """R-COMBAT-32 (Charging Units Fight First): a non-charged unit may not fight
    while an enemy charged unit has not yet fought — it must wait its turn. This
    covers the ordering branch of can_fight_now, not just eligibility."""
    non_charged = _unit_state(in_melee=True, charged=False)
    enemy_charged = _unit_state(in_melee=True, charged=True)
    _setup(
        monkeypatch, a_state=non_charged, b_state=enemy_charged, current="A", selected=("A", "u1")
    )

    # The non-charged unit is generally eligible...
    assert fp.can_fight(non_charged) is True
    # ...but must wait while the charged enemy is still pending.
    assert fp.can_fight_now(non_charged, "A", "B") is False
    # The charged unit itself fights first.
    assert fp.can_fight_now(enemy_charged, "A", "B") is True


# ---------------------------------------------------------------------------
# Plan 015 — Counter-Offensive: _enemy_has_fought() + _apply_counter_offensive()
# B-087: renamed from _any_unit_fought() — the gate must check the OPPONENT's
# fought units, not "either side", or the box wrongly offers Counter-Offensive
# right after the reacting player's OWN unit fought (core_rules.txt Z. 3256-3259
# requires "after an enemy unit has fought").
# ---------------------------------------------------------------------------


def test_enemy_has_fought_false_before_any_fight_this_phase(monkeypatch) -> None:  # type: ignore[no-untyped-def]
    a_state = _unit_state(fought=False)
    b_state = _unit_state(fought=False)
    _setup(monkeypatch, a_state=a_state, b_state=b_state, current="A", selected=None)

    assert fp._enemy_has_fought("A", "A", "B") is False


def test_enemy_has_fought_false_when_only_own_side_fought(monkeypatch) -> None:  # type: ignore[no-untyped-def]
    """Regression B-087: A's own unit fought, B's has not — A has no enemy-fought
    trigger yet, so Counter-Offensive must NOT be offered to A."""
    a_state = _unit_state(fought=True)
    b_state = _unit_state(fought=False)
    _setup(monkeypatch, a_state=a_state, b_state=b_state, current="B", selected=None)

    assert fp._enemy_has_fought("A", "A", "B") is False


def test_enemy_has_fought_true_when_opponent_fought(monkeypatch) -> None:  # type: ignore[no-untyped-def]
    """B's unit fought — from A's perspective the enemy has fought, so
    Counter-Offensive becomes available to A."""
    a_state = _unit_state(fought=False)
    b_state = _unit_state(fought=True)
    _setup(monkeypatch, a_state=a_state, b_state=b_state, current="A", selected=None)

    assert fp._enemy_has_fought("A", "A", "B") is True


def test_apply_counter_offensive_reassigns_fight_current_player_and_clears_selection(
    monkeypatch,
) -> None:  # type: ignore[no-untyped-def]
    """Counter-Offensive (core_rules.txt: 'Select one of your own eligible units and
    fight with it next.') lets X cut back in — no extra suppression flag is needed
    because _advance_fight_turn_if_needed only flips away from X once X's selected
    unit has fought, which is not yet true right after this call."""
    monkeypatch.setattr(fp, "units_key_for", lambda player: f"{player}_units")
    monkeypatch.setattr(fp, "lookup", lambda faction, uid: (None, {}))
    fp.st.session_state = FakeSessionState(
        fight_current_player="B",
        selected_unit=("B", "u2"),
        selected_targets=[("B", "u2")],
        # A already fought with u1, but still has a second, not-yet-fought unit
        # eligible to fight via Counter-Offensive.
        A_units={
            "u1": _unit_state(fought=True),
            "u3": _unit_state(fought=False, in_melee=True),
        },
        B_units={"u2": _unit_state(fought=False, in_melee=True)},
    )
    fp.st.rerun = MagicMock()

    fp._apply_counter_offensive("A")

    assert fp.st.session_state.fight_current_player == "A"
    assert fp.st.session_state.selected_unit is None
    assert fp.st.session_state.selected_targets == []

    # The natural alternation logic leaves "A" in place — no immediate flip-back,
    # since A has not (yet) selected+fought its remaining eligible unit ("u3").
    fp.st.rerun.reset_mock()
    fp._advance_fight_turn_if_needed("A", "B")
    assert fp.st.session_state.fight_current_player == "A"
    fp.st.rerun.assert_not_called()
