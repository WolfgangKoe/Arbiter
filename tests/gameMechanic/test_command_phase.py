"""Tests for gameMechanic/commandPhase.py — pure logic only (no Streamlit UI)."""

import sys
from pathlib import Path
from unittest.mock import MagicMock, patch

# Stub streamlit before importing commandPhase
_st_mock = MagicMock()
sys.modules["streamlit"] = _st_mock
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

import gameMechanic.gameState as _gs  # noqa: E402
from gameMechanic.commandPhase import (  # noqa: E402
    _wargear_once_per_battle,
    _wargear_state_key,
    can_gain_command_point,
    resolve_command_start,
    resolve_gain_cp_roll,
    unit_has_command_ability,
    units_with_command_abilities,
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
# Plan 018 Task 18.1 — CP grant locked per (round, faction), not a global flag
# ---------------------------------------------------------------------------


class TestRenderFactionActionsCpGrant:
    """_render_faction_actions must not allow double-granting CP for the same round.

    Regression for the bug fixed in Task 18.1: the old cp_granted_this_phase flag was
    cleared by _reset_phase_state() on every phase change, so ←/→ navigation back into
    the Command phase let the same faction claim +1 CP again. cp_grants is a
    (round, faction) set that _reset_phase_state() does not touch.
    """

    def _session(self, **extra: object) -> _S:
        defaults: dict[str, object] = {
            "game_mode": "matched",
            "cp": {"Necrons": 4, "Orks": 4},
            "cp_grants": set(),
        }
        defaults.update(extra)
        session = _S(**defaults)
        _st_mock.session_state = session
        _gs.st.session_state = session
        return session

    def test_first_grant_awards_cp_and_locks_round_faction(self) -> None:
        session = self._session()
        with (
            patch.object(_st_mock, "button", return_value=True),
            patch("gameMechanic.commandPhase.log_action"),
        ):
            from gameMechanic.commandPhase import _render_faction_actions

            _render_faction_actions("Necrons", {"round": 1})

        assert session.cp["Necrons"] == 5
        assert (1, "Necrons") in session.cp_grants

    def test_second_render_same_round_does_not_reaward(self) -> None:
        """Already-granted (round, faction) must hide the button — no re-award possible."""
        session = self._session(cp_grants={(1, "Necrons")})
        with (
            patch.object(_st_mock, "button", return_value=True) as mock_button,
            patch("gameMechanic.commandPhase.log_action"),
        ):
            from gameMechanic.commandPhase import _render_faction_actions

            _render_faction_actions("Necrons", {"round": 1})
            assert not mock_button.called

        assert session.cp["Necrons"] == 4

    def test_back_and_forward_navigation_does_not_regrant(self) -> None:
        """Regression: _reset_phase_state() must not clear cp_grants (the Task 18.1 bug)."""
        session = self._session(cp_grants={(1, "Necrons")}, phase_idx=1, round=1)
        _gs._reset_phase_state()  # simulates the reset every ←/→ phase navigation triggers
        assert session.cp_grants == {(1, "Necrons")}

        with (
            patch.object(_st_mock, "button", return_value=True) as mock_button,
            patch("gameMechanic.commandPhase.log_action"),
        ):
            from gameMechanic.commandPhase import _render_faction_actions

            _render_faction_actions("Necrons", {"round": 1})
            assert not mock_button.called

        assert session.cp["Necrons"] == 4

    def test_new_round_allows_new_grant(self) -> None:
        session = self._session(cp_grants={(1, "Necrons")})
        with (
            patch.object(_st_mock, "button", return_value=True),
            patch("gameMechanic.commandPhase.log_action"),
        ):
            from gameMechanic.commandPhase import _render_faction_actions

            _render_faction_actions("Necrons", {"round": 2})

        assert session.cp["Necrons"] == 5
        assert session.cp_grants == {(1, "Necrons"), (2, "Necrons")}

    def test_second_player_has_independent_grant(self) -> None:
        session = self._session(cp_grants={(1, "Necrons")})
        with (
            patch.object(_st_mock, "button", return_value=True),
            patch("gameMechanic.commandPhase.log_action"),
        ):
            from gameMechanic.commandPhase import _render_faction_actions

            _render_faction_actions("Orks", {"round": 1})

        assert session.cp["Orks"] == 5
        assert (1, "Orks") in session.cp_grants
        assert (1, "Necrons") in session.cp_grants  # untouched


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

    def test_wargear_heal_ui_renders_for_duplicate_target(self) -> None:
        """revive_wargear_target_uid can hold a duplicate-squad state key
        ('...#1'); unit_by_id is bare-ID-keyed, so the object lookup must
        resolve the suffix before indexing — otherwise the heal UI
        (wound_adjustment_buttons) never renders for the second copy of a
        squad (regression). wound_adjustment_buttons itself must still be
        called with the FULL state key (it indexes session state, not the
        bare-ID map)."""
        from gameMechanic.commandPhase import _render_activated_wargear, _wargear_state_key

        target_unit = MagicMock()
        target_unit.name_en = "Necron Warriors"
        unit_by_id = {"wh40k_9e.necrons.unit.warriors": target_unit}

        wargear = {
            "id": "wh40k_9e.necrons.wargear.resurrection_orb",
            "name_en": "Resurrection Orb",
        }
        request_id = _wargear_state_key("wh40k_9e.necrons.unit.overlord", wargear["id"])

        session = _S(
            wargear_used={},
            revive_wargear_target_uid={request_id: "wh40k_9e.necrons.unit.warriors#1"},
            active="Necrons",
        )
        _st_mock.session_state = session
        orig_button = _st_mock.button
        _st_mock.button = MagicMock(return_value=False)
        try:
            with patch("gameMechanic.commandPhase.wound_adjustment_buttons") as mock_wound:
                _render_activated_wargear(
                    "Necrons",
                    {"round": 1},
                    {},
                    unit_by_id,
                    None,
                    wargear,
                    bearer_uid="wh40k_9e.necrons.unit.overlord",
                )
        finally:
            _st_mock.button = orig_button

        mock_wound.assert_called_once_with(
            "Necrons", "wh40k_9e.necrons.unit.warriors#1", target_unit
        )


# ---------------------------------------------------------------------------
# unit_has_command_ability — army-wide command-phase ability detection helper
# ---------------------------------------------------------------------------


class TestUnitHasCommandAbility:
    """unit_has_command_ability must be data-driven and render-free."""

    def test_overlord_has_command_ability_via_unit_ability(self) -> None:
        """Overlord has 'My Will Be Done' (unit_ability, phase: command) → True."""
        units, _ = load_army("necrons")
        overlord = next(u for u in units if u.id == "wh40k_9e.necrons.unit.overlord")
        assert unit_has_command_ability(overlord, "necrons") is True

    def test_necron_lord_has_command_ability_via_unit_ability(self) -> None:
        """Necron Lord has 'The Lord's Will' (unit_ability, phase: command) → True."""
        units, _ = load_army("necrons")
        lord = next(u for u in units if u.id == "wh40k_9e.necrons.unit.necron_lord")
        assert unit_has_command_ability(lord, "necrons") is True

    def test_warriors_have_no_command_ability(self) -> None:
        """Warriors only have a triggered RP ability — no command-phase ability → False."""
        units, _ = load_army("necrons")
        warriors = next(u for u in units if u.id == "wh40k_9e.necrons.unit.warriors")
        assert unit_has_command_ability(warriors, "necrons") is False

    def test_unit_with_activated_wargear_has_command_ability(self) -> None:
        """A unit whose wargear_ids include an activated wargear entry → True.

        This tests the wargear branch directly: create a minimal unit with the
        Resurrection Orb wargear id, which has ability_type: activated.
        """
        from gameObjects.unit import Unit

        orb_id = "wh40k_9e.necrons.wargear.resurrection_orb"
        dummy = Unit(
            id="wh40k_9e.necrons.unit.dummy_bearer",
            name_en="Dummy Bearer",
            name_de="Dummy Träger",
            faction="Necrons",
            subfaction=None,
            battlefield_role=["HQ"],
            keywords=["NECRONS"],
            wounds=4,
            models_min=1,
            models_max=1,
            power_level=4,
            move='5"',
            bs="3+",
            ws="3+",
            strength=4,
            toughness=4,
            attacks=3,
            save=3,
            invuln_save=None,
            leadership=10,
            oc=1,
            fnp=None,
            wargear_ids=[orb_id],
        )
        assert unit_has_command_ability(dummy, "necrons") is True

    def test_unit_without_activated_wargear_and_no_ability_returns_false(self) -> None:
        """Unit with no command-phase unit_ability, no activated wargear, no relic → False."""
        from gameObjects.unit import Unit

        bare = Unit(
            id="wh40k_9e.necrons.unit.bare_unit",
            name_en="Bare Unit",
            name_de="Bare Unit",
            faction="Necrons",
            subfaction=None,
            battlefield_role=["Troops"],
            keywords=["NECRONS"],
            wounds=1,
            models_min=10,
            models_max=10,
            power_level=3,
            move='5"',
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
            wargear_ids=[],
        )
        assert unit_has_command_ability(bare, "necrons") is False

    def test_unit_with_gain_cp_roll_relic_has_command_ability(self) -> None:
        """Unit with a gain_cp_roll triggered effect at phase_start/command → True.

        The TriggeredEffect is set directly (no YAML lookup needed) — tests the
        third source branch of unit_has_command_ability.
        """
        from gameObjects.unit import TriggeredEffect, Unit

        relic_te = TriggeredEffect(
            timing="phase_start",
            phase="command",
            effect="gain_cp_roll",
        )
        bearer = Unit(
            id="wh40k_9e.necrons.unit.relic_bearer",
            name_en="Relic Bearer",
            name_de="Relic Bearer",
            faction="Necrons",
            subfaction=None,
            battlefield_role=["HQ"],
            keywords=["NECRONS"],
            wounds=4,
            models_min=1,
            models_max=1,
            power_level=4,
            move='5"',
            bs="3+",
            ws="3+",
            strength=4,
            toughness=4,
            attacks=3,
            save=3,
            invuln_save=None,
            leadership=10,
            oc=1,
            fnp=None,
            wargear_ids=[],
            triggered_effects=[relic_te],
        )
        assert unit_has_command_ability(bearer, "necrons") is True


# ---------------------------------------------------------------------------
# units_with_command_abilities — army-wide aggregator (integration)
# ---------------------------------------------------------------------------


class TestUnitsWithCommandAbilities:
    """units_with_command_abilities must return only units with command-phase abilities."""

    def test_necrons_includes_overlord_and_necron_lord(self) -> None:
        """Necron army must list Overlord and Necron Lord among units with command abilities."""
        session = _S(
            first_player="Necrons",
            p1_faction_dir="necrons",
            p2_faction_dir="necrons",
        )
        _st_mock.session_state = session
        _gs.st.session_state = session

        units, _ = load_army("necrons")
        session["p1_units_list"] = units

        able = units_with_command_abilities("Necrons")
        able_ids = {u.id for u in able}
        assert "wh40k_9e.necrons.unit.overlord" in able_ids
        assert "wh40k_9e.necrons.unit.necron_lord" in able_ids

    def test_necrons_excludes_warriors(self) -> None:
        """Warriors have no command-phase ability → excluded from the army-wide list."""
        session = _S(
            first_player="Necrons",
            p1_faction_dir="necrons",
            p2_faction_dir="necrons",
        )
        _st_mock.session_state = session
        _gs.st.session_state = session

        units, _ = load_army("necrons")
        session["p1_units_list"] = units

        able = units_with_command_abilities("Necrons")
        able_ids = {u.id for u in able}
        assert "wh40k_9e.necrons.unit.warriors" not in able_ids

    def test_empty_army_returns_empty_list(self) -> None:
        """Army with no units → empty result, no crash."""
        session = _S(
            first_player="Necrons",
            p1_faction_dir="necrons",
            p2_faction_dir="necrons",
        )
        _st_mock.session_state = session
        _gs.st.session_state = session
        session["p1_units_list"] = []

        assert units_with_command_abilities("Necrons") == []
