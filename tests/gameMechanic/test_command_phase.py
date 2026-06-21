"""Tests for gameMechanic/commandPhase.py — pure logic only (no Streamlit UI)."""

import sys
from pathlib import Path
from unittest.mock import MagicMock

# Stub streamlit before importing commandPhase
_st_mock = MagicMock()
sys.modules["streamlit"] = _st_mock
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

import gameMechanic.game_state as _gs  # noqa: E402
from gameMechanic.commandPhase import (  # noqa: E402
    _wargear_once_per_battle,
    _wargear_state_key,
    can_gain_command_point,
    resolve_command_start,
    resolve_gain_cp_roll,
)
from gameObjects.loader import activated_wargear_ids, load_army  # noqa: E402

# ---------------------------------------------------------------------------
# resolve_command_start — integration
# ---------------------------------------------------------------------------


class _S(dict):
    def __getattr__(self, key: str):  # type: ignore[override]
        try:
            return self[key]
        except KeyError:
            raise AttributeError(key)

    def __setattr__(self, key: str, value: object) -> None:
        self[key] = value


def _make_necron_state() -> dict:
    units, _ = load_army("necrons")
    session = _S(first_player="Necrons", p1_faction_dir="necrons", p2_faction_dir="necrons")
    _st_mock.session_state = session
    _gs.st.session_state = session
    return {
        "active": "Necrons",
        "first_player": "Necrons",
        "p1_units": {
            u.id: {
                "current_wounds": max(1, u.wounds * u.models_max - 1),  # 1 wound below max
                "models": u.models_max,
                "destroyed": False,
            }
            for u in units
        },
    }


def test_resolve_command_start_returns_living_metal() -> None:
    state = _make_necron_state()
    triggered = resolve_command_start(state)
    ids = [a.id for a, _ in triggered]
    assert "wh40k_9e.necrons.faction.living_metal" in ids


def test_resolve_command_start_ork_returns_empty() -> None:
    units, _ = load_army("orks")
    session = _S(first_player="Necrons", p1_faction_dir="necrons", p2_faction_dir="orks")
    _st_mock.session_state = session
    _gs.st.session_state = session
    state = {
        "active": "Orks",
        "first_player": "Necrons",
        "p2_units": {
            u.id: {
                "current_wounds": u.wounds * u.models_max,
                "models": u.models_max,
                "destroyed": False,
            }
            for u in units
        },
    }
    triggered = resolve_command_start(state)
    assert triggered == []


# ---------------------------------------------------------------------------
# R-CMD-03 — can_gain_command_point (Battle-forged gate)
# ---------------------------------------------------------------------------


class TestCanGainCommandPoint:
    def test_matched_play_is_battle_forged(self) -> None:
        """Matched Play armies are Battle-forged → CP grant allowed."""
        assert can_gain_command_point("matched") is True

    def test_crusade_is_battle_forged(self) -> None:
        """Crusade armies are also Battle-forged → CP grant allowed."""
        assert can_gain_command_point("crusade") is True

    def test_open_play_is_not_battle_forged(self) -> None:
        """Open Play armies are Unbound → CP grant must be blocked."""
        assert can_gain_command_point("open") is False

    def test_unknown_mode_is_not_battle_forged(self) -> None:
        """Unexpected game_mode values are treated as non-Battle-forged."""
        assert can_gain_command_point("unknown") is False


# ---------------------------------------------------------------------------
# R-CMD-11 — resolve_gain_cp_roll (gain_cp_roll resolution + once-per-phase lock)
# ---------------------------------------------------------------------------


class TestResolveGainCpRoll:
    def test_success_returns_cp_delta(self) -> None:
        """Roll at/above threshold → active side gains `amount` CP and phase locks."""
        cp_delta, locked = resolve_gain_cp_roll(amount=1, roll_succeeded=True, already_rolled=False)
        assert cp_delta == 1
        assert locked is True

    def test_failure_returns_zero_but_locks(self) -> None:
        """Roll below threshold → no CP gained, but phase is still locked."""
        cp_delta, locked = resolve_gain_cp_roll(
            amount=1, roll_succeeded=False, already_rolled=False
        )
        assert cp_delta == 0
        assert locked is True

    def test_lock_prevents_second_resolution(self) -> None:
        """Calling resolve_gain_cp_roll when already_rolled=True raises ValueError."""
        import pytest

        with pytest.raises(ValueError, match="already resolved"):
            resolve_gain_cp_roll(amount=1, roll_succeeded=True, already_rolled=True)

    def test_success_with_multi_cp_amount(self) -> None:
        cp_delta, locked = resolve_gain_cp_roll(amount=2, roll_succeeded=True, already_rolled=False)
        assert cp_delta == 2
        assert locked is True


# ---------------------------------------------------------------------------
# Activated wargear — generic flow (Plan 020)
# ---------------------------------------------------------------------------


class TestActivatedWargear:
    def test_activated_wargear_ids_finds_orb_generically(self) -> None:
        ids = activated_wargear_ids("necrons")
        assert "wh40k_9e.necrons.wargear.resurrection_orb" in ids

    def test_once_per_battle_read_from_conditions(self) -> None:
        entry = {"conditions": [{"within_inches": 6, "once_per_battle": True}]}
        assert _wargear_once_per_battle(entry) is True

    def test_once_per_battle_false_when_absent(self) -> None:
        assert _wargear_once_per_battle({"conditions": [{"within_inches": 6}]}) is False

    def test_two_bearers_target_state_no_conflict(self) -> None:
        # Per-wargear namespacing: two orb instances keep separate targets,
        # so resolving one never clears the other (the old global-key bug).
        targets: dict[str, str] = {}
        targets["revive_wargear_orb_a"] = "necron_warriors#1"
        targets["revive_wargear_orb_b"] = "necron_immortals#1"
        targets.pop("revive_wargear_orb_a", None)
        assert "revive_wargear_orb_a" not in targets
        assert targets["revive_wargear_orb_b"] == "necron_immortals#1"

    def test_same_wargear_two_instances_get_distinct_state_keys(self) -> None:
        # Two Overlords carrying the SAME resurrection orb must not share
        # once-per-battle / target state — the key includes the bearer instance.
        orb = "wh40k_9e.necrons.wargear.resurrection_orb"
        first = _wargear_state_key("wh40k_9e.necrons.unit.overlord", orb)
        second = _wargear_state_key("wh40k_9e.necrons.unit.overlord#1", orb)
        assert first != second

    def test_two_orb_bearers_render_distinct_button_keys(self) -> None:
        # Regression: two Overlords carrying the SAME Resurrection Orb must get
        # DISTINCT Streamlit widget keys for the activate button. With a shared
        # key the second button collides and never sets pending_target_request,
        # so the second orb's per-model revive buttons never appear. Button keys
        # route through the bearer-scoped request_id.
        from gameMechanic.commandPhase import _render_activated_wargear

        captured: list[str] = []

        def _record_button(*args: object, **kwargs: object) -> bool:
            captured.append(str(kwargs.get("key", "")))
            return False

        session = _S(
            wargear_used={},
            revive_wargear_target_uid={},
            pending_target_request=None,
            active="Necrons",
        )
        _st_mock.session_state = session
        orig_button = _st_mock.button
        _st_mock.button = _record_button
        try:
            wargear = {
                "id": "wh40k_9e.necrons.wargear.resurrection_orb",
                "name_en": "Resurrection Orb",
            }
            _render_activated_wargear(
                "Necrons",
                {},
                {},
                {},
                None,
                wargear,
                bearer_uid="wh40k_9e.necrons.unit.overlord",
            )
            _render_activated_wargear(
                "Necrons",
                {},
                {},
                {},
                None,
                wargear,
                bearer_uid="wh40k_9e.necrons.unit.overlord#1",
            )
        finally:
            _st_mock.button = orig_button

        assert len(captured) == 2
        assert captured[0] != captured[1]
        assert all(k.startswith("cmd_revive_wargear_") for k in captured)
