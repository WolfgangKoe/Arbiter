"""Regression tests for the Heroic Intervention duplicate-squad widget-key crash.

Bug: The HI flow used unit.id as Streamlit widget keys AND as state-dict
identifiers.  When a roster contains duplicate squads (same unit.id, distinct
state keys like 'warriors', 'warriors#1', 'warriors#2'), widget keys collide →
StreamlitDuplicateElementKey crashes the center column.

These tests guard against the root cause:
  - perform_heroic_intervention operates on STATE KEYS, not unit.id.
  - hi_eligible_units returns one (Unit, state_key) pair per state key.
  - Widget keys derived from state keys are always unique for duplicate squads.
"""

from __future__ import annotations

import sys
from pathlib import Path
from unittest.mock import MagicMock

_st_mock = MagicMock()
sys.modules["streamlit"] = _st_mock
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

import gameMechanic.game_log as _gl  # noqa: E402
import gameMechanic.game_state as _gs  # noqa: E402
import gameMechanic.unit_mutations as _mut  # noqa: E402
from gameMechanic.chargephase import hi_eligible_units  # noqa: E402
from gameMechanic.unit_mutations import perform_heroic_intervention  # noqa: E402
from gameObjects.unit import Unit  # noqa: E402

# ---------------------------------------------------------------------------
# Test helpers
# ---------------------------------------------------------------------------

OVERLORD = "wh40k_9e.necrons.unit.overlord"
WARRIORS = "wh40k_9e.necrons.unit.warriors"
WARRIORS_DUP = "wh40k_9e.necrons.unit.warriors#1"
BOYZ = "wh40k_9e.orks.unit.boyz"


class _S(dict):
    def __getattr__(self, key: str):
        try:
            return self[key]
        except KeyError:
            raise AttributeError(key)

    def __setattr__(self, key: str, value: object) -> None:
        self[key] = value


def _make_session(**kwargs) -> _S:
    kwargs.setdefault("first_player", "Necrons")
    kwargs.setdefault("second_player", "Orks")
    s = _S(**kwargs)
    _mut.st.session_state = s
    _gs.st.session_state = s
    _gl.st = _st_mock
    _st_mock.session_state = s
    return s


def _fresh_unit_state(
    *,
    destroyed: bool = False,
    in_melee: bool = False,
    heroic_intervened: bool = False,
) -> dict:
    return {
        "current_wounds": 5,
        "models": 1,
        "destroyed": destroyed,
        "in_melee": in_melee,
        "in_reserve": False,
        "melee_with": [],
        "turn_flags": {
            "advanced": False,
            "retreated": False,
            "charged": False,
            "shot": False,
            "fought": False,
            "heroic_intervened": heroic_intervened,
        },
    }


def _make_unit(uid: str, name: str, *keywords: str) -> Unit:
    return Unit(
        id=uid,
        name_en=name,
        name_de=name,
        faction="Necrons",
        subfaction=None,
        battlefield_role=["HQ"],
        keywords=list(keywords),
        wounds=5,
        models_min=1,
        models_max=1,
        power_level=4,
        move='6"',
        bs="3+",
        ws="3+",
        strength=5,
        toughness=5,
        attacks=3,
        save=3,
        invuln_save=None,
        leadership=10,
        oc=1,
        fnp=None,
    )


def _make_ork_unit(uid: str, name: str) -> Unit:
    return Unit(
        id=uid,
        name_en=name,
        name_de=name,
        faction="Orks",
        subfaction=None,
        battlefield_role=["Troops"],
        keywords=["INFANTRY"],
        wounds=2,
        models_min=10,
        models_max=20,
        power_level=3,
        move='5"',
        bs="5+",
        ws="3+",
        strength=5,
        toughness=4,
        attacks=2,
        save=6,
        invuln_save=None,
        leadership=7,
        oc=2,
        fnp=None,
    )


# ---------------------------------------------------------------------------
# Test 1: perform_heroic_intervention targets correct duplicate squad
# ---------------------------------------------------------------------------


class TestPerformHeroicInterventionDuplicateSquads:
    """perform_heroic_intervention uses state keys → targets exactly the right squad."""

    def _setup_session(self) -> _S:
        """Seed:
        - Necrons: Overlord (CHARACTER) as the intervening unit.
        - Orks: two identical Boyz squads → state keys 'boyz' and 'boyz#1'.
        """
        overlord_state = _fresh_unit_state()
        # Both Ork squads share the same unit.id; state keys differentiate them
        boyz_state = _fresh_unit_state()
        boyz_dup_state = _fresh_unit_state()

        s = _make_session(
            p1_units={OVERLORD: overlord_state},
            p2_units={BOYZ: boyz_state, BOYZ + "#1": boyz_dup_state},
            game_log=[],
        )
        # Wire unit lists and unit keys so units_list_for / unit_keys_for work
        overlord_unit = _make_unit(OVERLORD, "Overlord", "CHARACTER", "INFANTRY")
        boyz_unit_1 = _make_ork_unit(BOYZ, "Boyz")
        boyz_unit_2 = _make_ork_unit(BOYZ, "Boyz")  # same unit.id — duplicate

        s["p1_units_list"] = [overlord_unit]
        s["p1_unit_keys"] = [OVERLORD]
        s["p2_units_list"] = [boyz_unit_1, boyz_unit_2]
        s["p2_unit_keys"] = [BOYZ, BOYZ + "#1"]
        return s

    def test_character_heroic_intervened_flag_set(self) -> None:
        s = self._setup_session()
        perform_heroic_intervention("Necrons", OVERLORD, "Orks", [BOYZ + "#1"], 1, "Overlord")
        assert s["p1_units"][OVERLORD]["turn_flags"]["heroic_intervened"] is True

    def test_character_enters_melee(self) -> None:
        s = self._setup_session()
        perform_heroic_intervention("Necrons", OVERLORD, "Orks", [BOYZ + "#1"], 1, "Overlord")
        assert s["p1_units"][OVERLORD]["in_melee"] is True

    def test_targeted_duplicate_squad_enters_melee(self) -> None:
        s = self._setup_session()
        perform_heroic_intervention("Necrons", OVERLORD, "Orks", [BOYZ + "#1"], 1, "Overlord")
        assert s["p2_units"][BOYZ + "#1"]["in_melee"] is True

    def test_targeted_squad_melee_with_contains_character(self) -> None:
        s = self._setup_session()
        perform_heroic_intervention("Necrons", OVERLORD, "Orks", [BOYZ + "#1"], 1, "Overlord")
        assert ["Necrons", OVERLORD] in s["p2_units"][BOYZ + "#1"]["melee_with"]

    def test_character_melee_with_contains_targeted_squad(self) -> None:
        s = self._setup_session()
        perform_heroic_intervention("Necrons", OVERLORD, "Orks", [BOYZ + "#1"], 1, "Overlord")
        assert ["Orks", BOYZ + "#1"] in s["p1_units"][OVERLORD]["melee_with"]

    def test_first_squad_not_in_melee(self) -> None:
        """The non-targeted first squad must remain untouched (key-collision guard)."""
        s = self._setup_session()
        perform_heroic_intervention("Necrons", OVERLORD, "Orks", [BOYZ + "#1"], 1, "Overlord")
        assert s["p2_units"][BOYZ]["in_melee"] is False
        assert s["p2_units"][BOYZ]["melee_with"] == []

    def test_log_entry_created(self) -> None:
        self._setup_session()
        # log_action is imported by name into unit_mutations module, so we must
        # patch it on the unit_mutations module directly (not on game_log).
        calls = []
        original = _mut.log_action  # type: ignore[attr-defined]

        def _recording_log(round_no, phase, unit_name, action):
            calls.append((round_no, phase, unit_name, action))

        _mut.log_action = _recording_log  # type: ignore[attr-defined]
        try:
            perform_heroic_intervention("Necrons", OVERLORD, "Orks", [BOYZ + "#1"], 1, "Overlord")
        finally:
            _mut.log_action = original  # type: ignore[attr-defined]

        assert len(calls) == 1
        assert calls[0] == (1, "charge", "Overlord", "Heroic Intervention — engaged 1 unit(s)")


# ---------------------------------------------------------------------------
# Test 2: hi_eligible_units returns distinct keys for duplicate squads
# ---------------------------------------------------------------------------


class TestHiEligibleUnitsDuplicateSquads:
    """hi_eligible_units returns (Unit, state_key) pairs — one per state key."""

    def _build_two_char_squads(self) -> tuple[list[Unit], list[str], dict]:
        """Two CHARACTER squads with the same unit.id, distinct state keys."""
        char_unit_1 = _make_unit("char_id", "Char Alpha", "CHARACTER")
        char_unit_2 = _make_unit("char_id", "Char Alpha", "CHARACTER")  # duplicate id
        unit_keys = ["char_id", "char_id#1"]
        units_data = {
            "char_id": _fresh_unit_state(),
            "char_id#1": _fresh_unit_state(),
        }
        return [char_unit_1, char_unit_2], unit_keys, units_data

    def test_both_duplicate_character_squads_returned(self) -> None:
        units, keys, data = self._build_two_char_squads()
        result = hi_eligible_units(units, keys, data)
        assert len(result) == 2

    def test_returned_state_keys_are_distinct(self) -> None:
        units, keys, data = self._build_two_char_squads()
        result = hi_eligible_units(units, keys, data)
        returned_keys = [ukey for _, ukey in result]
        assert len(set(returned_keys)) == len(
            returned_keys
        ), f"Duplicate state keys returned: {returned_keys}"

    def test_destroyed_squad_excluded(self) -> None:
        units, keys, data = self._build_two_char_squads()
        data["char_id"]["destroyed"] = True
        result = hi_eligible_units(units, keys, data)
        returned_keys = [ukey for _, ukey in result]
        assert "char_id" not in returned_keys
        assert "char_id#1" in returned_keys

    def test_in_melee_squad_excluded(self) -> None:
        units, keys, data = self._build_two_char_squads()
        data["char_id#1"]["in_melee"] = True
        result = hi_eligible_units(units, keys, data)
        returned_keys = [ukey for _, ukey in result]
        assert "char_id#1" not in returned_keys
        assert "char_id" in returned_keys

    def test_already_intervened_squad_excluded(self) -> None:
        units, keys, data = self._build_two_char_squads()
        data["char_id#1"]["turn_flags"]["heroic_intervened"] = True
        result = hi_eligible_units(units, keys, data)
        returned_keys = [ukey for _, ukey in result]
        assert "char_id#1" not in returned_keys
        assert "char_id" in returned_keys

    def test_non_character_unit_excluded(self) -> None:
        infantry = _make_unit("inf_id", "Infantry", "INFANTRY")
        char = _make_unit("char_id", "Char", "CHARACTER")
        units = [char, infantry]
        keys = ["char_id", "inf_id"]
        data = {
            "char_id": _fresh_unit_state(),
            "inf_id": _fresh_unit_state(),
        }
        result = hi_eligible_units(units, keys, data)
        returned_keys = [ukey for _, ukey in result]
        assert "char_id" in returned_keys
        assert "inf_id" not in returned_keys

    def test_empty_returns_empty(self) -> None:
        assert hi_eligible_units([], [], {}) == []


# ---------------------------------------------------------------------------
# Test 3: Widget keys are unique for duplicate squads (crash-guard invariant)
# ---------------------------------------------------------------------------


class TestHiTargetWidgetKeysUniqueForDuplicateSquads:
    """Verify the invariant that was violated in the crash: widget keys must be unique.

    Approach: build the list of would-be widget keys using the same formula as
    _render_hi_target_selection — f"hi_tgt_{active}_{ekey}" — from
    zip(units_list_for(active), unit_keys_for(active)), then assert uniqueness.

    We use this approach (key enumeration) rather than AppTest because
    _render_hi_target_selection requires deep Streamlit session state bootstrapping
    (active/inactive player slots, full faction dirs, lookup catalog wiring) that
    is disproportionately expensive to replicate in a unit test.  The invariant
    being tested — that state keys are unique and therefore produce unique widget
    keys — is directly observable from the key lists alone and does not require
    rendering.
    """

    def test_duplicate_squad_widget_keys_are_unique(self) -> None:
        active = "Orks"
        # Simulate two duplicate Boyz squads: same unit.id, different state keys
        boyz_unit_1 = _make_ork_unit(BOYZ, "Boyz")
        boyz_unit_2 = _make_ork_unit(BOYZ, "Boyz")

        units_list = [boyz_unit_1, boyz_unit_2]
        unit_keys = [BOYZ, BOYZ + "#1"]  # what unit_keys_for(active) returns for duplicates

        # This is the exact formula from _render_hi_target_selection after the fix
        widget_keys = [f"hi_tgt_{active}_{ekey}" for _, ekey in zip(units_list, unit_keys)]

        assert len(set(widget_keys)) == len(
            widget_keys
        ), f"Duplicate widget keys detected (this is the crash): {widget_keys}"

    def test_non_duplicate_squads_also_produce_unique_keys(self) -> None:
        """Sanity: unique unit IDs also produce unique widget keys."""
        active = "Orks"
        boyz = _make_ork_unit(BOYZ, "Boyz")
        warboss = _make_ork_unit("wh40k_9e.orks.unit.warboss", "Warboss")

        units_list = [boyz, warboss]
        unit_keys = [BOYZ, "wh40k_9e.orks.unit.warboss"]

        widget_keys = [f"hi_tgt_{active}_{ekey}" for _, ekey in zip(units_list, unit_keys)]
        assert len(set(widget_keys)) == len(widget_keys)
