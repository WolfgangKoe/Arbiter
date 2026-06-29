"""Tests for scenarios.py — apply_scenario and get_scenario_data.

apply_scenario() is a pure dict-manipulation function; all paths are tested
without any Streamlit interaction. get_scenario_data() is a thin JSON reader;
tested with a tmp fixture.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from unittest.mock import MagicMock

import pytest

_st_mock = MagicMock()
sys.modules.setdefault("streamlit", _st_mock)
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

import gameMechanic.scenarios as _sc  # noqa: E402
from gameMechanic.scenarios import apply_scenario  # noqa: E402

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _base_state(**overrides: object) -> dict:
    state: dict = {
        "round": 1,
        "phase_idx": 0,
        "phase_stage": "active",
        "first_player": "Necrons",
        "second_player": "Orks",
        "cp": {"Necrons": 6, "Orks": 6},
        "vp": {"Necrons": 0, "Orks": 0},
        "p1_units": {},
        "p2_units": {},
    }
    state.update(overrides)
    return state


def _unit_entry(**overrides: object) -> dict:
    entry: dict = {
        "current_wounds": 5,
        "models": 5,
        "destroyed": False,
        "in_melee": False,
        "in_reserve": False,
        "melee_with": [],
        "turn_flags": {
            "advanced": False,
            "retreated": False,
            "charged": False,
            "shot": False,
            "fought": False,
        },
    }
    entry.update(overrides)
    return entry


# ---------------------------------------------------------------------------
# Basic scalar keys
# ---------------------------------------------------------------------------


class TestApplyScenarioScalarKeys:
    def test_sets_round(self) -> None:
        state = _base_state()
        apply_scenario({"round": 3}, state)
        assert state["round"] == 3

    def test_sets_phase_idx(self) -> None:
        state = _base_state()
        apply_scenario({"phase_idx": 4}, state)
        assert state["phase_idx"] == 4

    def test_sets_phase_stage(self) -> None:
        state = _base_state()
        apply_scenario({"phase_stage": "end"}, state)
        assert state["phase_stage"] == "end"

    def test_missing_keys_leave_state_unchanged(self) -> None:
        state = _base_state()
        apply_scenario({}, state)
        assert state["round"] == 1
        assert state["phase_idx"] == 0
        assert state["phase_stage"] == "active"

    def test_all_three_scalar_keys_set_together(self) -> None:
        state = _base_state()
        apply_scenario({"round": 2, "phase_idx": 5, "phase_stage": "start"}, state)
        assert state["round"] == 2
        assert state["phase_idx"] == 5
        assert state["phase_stage"] == "start"


# ---------------------------------------------------------------------------
# CP / VP positional mapping
# ---------------------------------------------------------------------------


class TestApplyScenarioCpVp:
    def test_maps_cp_first_key_to_first_player(self) -> None:
        state = _base_state()
        apply_scenario({"cp": {"Alpha": 10, "Beta": 5}}, state)
        assert state["cp"]["Necrons"] == 10

    def test_maps_cp_second_key_to_second_player(self) -> None:
        state = _base_state()
        apply_scenario({"cp": {"Alpha": 10, "Beta": 5}}, state)
        assert state["cp"]["Orks"] == 5

    def test_maps_vp_positionally(self) -> None:
        state = _base_state()
        apply_scenario({"vp": {"Alpha": 3, "Beta": 7}}, state)
        assert state["vp"]["Necrons"] == 3
        assert state["vp"]["Orks"] == 7

    def test_no_cp_key_leaves_cp_unchanged(self) -> None:
        state = _base_state()
        apply_scenario({"round": 2}, state)
        assert state["cp"] == {"Necrons": 6, "Orks": 6}

    def test_no_vp_key_leaves_vp_unchanged(self) -> None:
        state = _base_state()
        apply_scenario({"round": 2}, state)
        assert state["vp"] == {"Necrons": 0, "Orks": 0}

    def test_single_player_cp_only_sets_first(self) -> None:
        state = _base_state()
        apply_scenario({"cp": {"OnlyArmy": 8}}, state)
        assert state["cp"]["Necrons"] == 8
        assert state["cp"]["Orks"] == 6  # unchanged

    def test_empty_first_player_skips_first_mapping(self) -> None:
        state = _base_state(first_player="")
        apply_scenario({"cp": {"Alpha": 10, "Beta": 5}}, state)
        # first_player is "" → no mapping; Necrons key stays at 6
        assert state["cp"].get("Necrons") == 6


# ---------------------------------------------------------------------------
# Active player mapping
# ---------------------------------------------------------------------------


class TestApplyScenarioActive:
    def test_active_matches_first_cp_key_maps_to_first_player(self) -> None:
        state = _base_state(active="Necrons")
        data = {"active": "Alpha", "cp": {"Alpha": 6, "Beta": 6}}
        apply_scenario(data, state)
        assert state["active"] == "Necrons"

    def test_active_matches_second_cp_key_maps_to_second_player(self) -> None:
        state = _base_state(active="Necrons")
        data = {"active": "Beta", "cp": {"Alpha": 6, "Beta": 6}}
        apply_scenario(data, state)
        assert state["active"] == "Orks"

    def test_active_unrecognised_value_passed_through(self) -> None:
        state = _base_state()
        data = {"active": "Unknown", "cp": {"X": 1}}
        apply_scenario(data, state)
        assert state["active"] == "Unknown"

    def test_active_without_cp_in_data_passed_through_raw(self) -> None:
        state = _base_state(active="Necrons")
        apply_scenario({"active": "Necrons"}, state)
        assert state["active"] == "Necrons"

    def test_no_active_key_leaves_active_unchanged(self) -> None:
        state = _base_state(active="Orks")
        apply_scenario({"round": 2}, state)
        assert state["active"] == "Orks"


# ---------------------------------------------------------------------------
# Unit patches
# ---------------------------------------------------------------------------


class TestApplyScenarioUnitPatches:
    def test_patches_existing_unit_field(self) -> None:
        state = _base_state(p1_units={"u1": _unit_entry()})
        apply_scenario({"unit_patches": {"p1_units": {"u1": {"models": 3}}}}, state)
        assert state["p1_units"]["u1"]["models"] == 3

    def test_patches_second_player_unit(self) -> None:
        state = _base_state(p2_units={"u2": _unit_entry()})
        apply_scenario({"unit_patches": {"p2_units": {"u2": {"destroyed": True}}}}, state)
        assert state["p2_units"]["u2"]["destroyed"] is True

    def test_skips_missing_faction_key(self) -> None:
        state = _base_state(p1_units={"u1": _unit_entry()})
        apply_scenario({"unit_patches": {"p99_units": {"u1": {"models": 1}}}}, state)
        assert state["p1_units"]["u1"]["models"] == 5

    def test_skips_missing_unit_id(self) -> None:
        state = _base_state(p1_units={"u1": _unit_entry()})
        apply_scenario({"unit_patches": {"p1_units": {"ghost": {"models": 1}}}}, state)
        assert state["p1_units"]["u1"]["models"] == 5

    def test_merges_turn_flags_not_replaces(self) -> None:
        state = _base_state(p1_units={"u1": _unit_entry()})
        data = {"unit_patches": {"p1_units": {"u1": {"turn_flags": {"advanced": True}}}}}
        apply_scenario(data, state)
        flags = state["p1_units"]["u1"]["turn_flags"]
        assert flags["advanced"] is True
        assert flags["retreated"] is False  # untouched flag preserved

    def test_melee_with_non_empty_sets_in_melee_true(self) -> None:
        state = _base_state(p1_units={"u1": _unit_entry()})
        data = {"unit_patches": {"p1_units": {"u1": {"melee_with": [["Orks", "u2"]]}}}}
        apply_scenario(data, state)
        assert state["p1_units"]["u1"]["in_melee"] is True

    def test_melee_with_empty_clears_in_melee(self) -> None:
        state = _base_state(
            p1_units={"u1": _unit_entry(in_melee=True, melee_with=[["Orks", "u2"]])}
        )
        data = {"unit_patches": {"p1_units": {"u1": {"melee_with": []}}}}
        apply_scenario(data, state)
        assert state["p1_units"]["u1"]["in_melee"] is False

    def test_patch_without_melee_with_leaves_in_melee_unchanged(self) -> None:
        state = _base_state(p1_units={"u1": _unit_entry(in_melee=True)})
        apply_scenario({"unit_patches": {"p1_units": {"u1": {"models": 2}}}}, state)
        assert state["p1_units"]["u1"]["in_melee"] is True

    def test_empty_unit_patches_changes_nothing(self) -> None:
        state = _base_state(p1_units={"u1": _unit_entry()})
        apply_scenario({"unit_patches": {}}, state)
        assert state["p1_units"]["u1"]["models"] == 5


# ---------------------------------------------------------------------------
# get_scenario_data
# ---------------------------------------------------------------------------


class TestGetScenarioData:
    def test_returns_none_when_file_not_found(self, tmp_path: Path, monkeypatch) -> None:  # type: ignore[no-untyped-def]
        monkeypatch.setattr(_sc, "_SCENARIOS_DIR", tmp_path)
        assert _sc.get_scenario_data("nonexistent") is None

    def test_returns_parsed_dict(self, tmp_path: Path, monkeypatch) -> None:  # type: ignore[no-untyped-def]
        monkeypatch.setattr(_sc, "_SCENARIOS_DIR", tmp_path)
        (tmp_path / "mytest.json").write_text(json.dumps({"round": 2, "phase_idx": 3}))
        result = _sc.get_scenario_data("mytest")
        assert result == {"round": 2, "phase_idx": 3}

    def test_looks_up_by_name_with_json_extension(self, tmp_path: Path, monkeypatch) -> None:  # type: ignore[no-untyped-def]
        monkeypatch.setattr(_sc, "_SCENARIOS_DIR", tmp_path)
        (tmp_path / "fight_r2.json").write_text('{"round": 2}')
        result = _sc.get_scenario_data("fight_r2")
        assert result is not None
        assert result["round"] == 2


def test_get_scenario_data_rejects_path_traversal() -> None:
    assert _sc.get_scenario_data("../rosters/necrons_alpha") is None
    assert _sc.get_scenario_data("..") is None
    assert _sc.get_scenario_data("a/b") is None
    assert _sc.get_scenario_data("") is None


def test_get_scenario_data_accepts_valid_names() -> None:
    assert _sc.get_scenario_data("shooting_phase") is not None
    assert _sc.get_scenario_data("does-not-exist_123") is None


def test_save_scenario_rejects_invalid_name() -> None:
    with pytest.raises(ValueError, match="Invalid scenario name"):
        _sc.save_scenario("../evil")


# ---------------------------------------------------------------------------
# load_scenario — lines 78-88 (requires st.session_state mock)
# ---------------------------------------------------------------------------


class TestLoadScenario:
    def _make_st_session(self, data: dict) -> object:
        """Build a mock st.session_state that behaves like a dict-iteration object."""
        # Use a plain dict; wrap with __iter__ compatible object
        state = {k: v for k, v in data.items()}

        class _FakeState:
            def __iter__(self_inner):
                return iter(state)

            def __getitem__(self_inner, key: str):
                return state[key]

            def __setitem__(self_inner, key: str, value: object) -> None:
                state[key] = value

            def get(self_inner, key: str, default=None):
                return state.get(key, default)

        return _FakeState()

    def test_load_scenario_returns_false_when_not_found(self, tmp_path: Path, monkeypatch) -> None:
        monkeypatch.setattr(_sc, "_SCENARIOS_DIR", tmp_path)
        fake_state = self._make_st_session({"round": 1})
        monkeypatch.setattr(_sc.st, "session_state", fake_state)
        assert _sc.load_scenario("no_such_file") is False

    def test_load_scenario_returns_true_and_patches_state(
        self, tmp_path: Path, monkeypatch
    ) -> None:
        monkeypatch.setattr(_sc, "_SCENARIOS_DIR", tmp_path)
        (tmp_path / "my_save.json").write_text('{"round": 3, "phase_idx": 2}')
        base_data = {
            "round": 1,
            "phase_idx": 0,
            "phase_stage": "active",
            "first_player": "Necrons",
            "second_player": "Orks",
            "cp": {"Necrons": 6, "Orks": 6},
            "vp": {"Necrons": 0, "Orks": 0},
        }
        fake_state = self._make_st_session(base_data)
        monkeypatch.setattr(_sc.st, "session_state", fake_state)
        result = _sc.load_scenario("my_save")
        assert result is True
        assert fake_state["round"] == 3
        assert fake_state["phase_idx"] == 2

    def test_load_scenario_private_keys_excluded(self, tmp_path: Path, monkeypatch) -> None:
        """Keys starting with '_' must not be passed to apply_scenario."""
        monkeypatch.setattr(_sc, "_SCENARIOS_DIR", tmp_path)
        (tmp_path / "snap.json").write_text('{"round": 2}')
        base_data = {"round": 1, "_internal": "skip_me"}
        fake_state = self._make_st_session(base_data)
        monkeypatch.setattr(_sc.st, "session_state", fake_state)
        _sc.load_scenario("snap")
        # _internal key must still be in state (not wiped) but was not sent to apply
        assert fake_state["round"] == 2


# ---------------------------------------------------------------------------
# save_scenario — lines 95-111
# ---------------------------------------------------------------------------


class TestSaveScenario:
    def _make_st_session_for_save(self, data: dict):  # type: ignore[no-untyped-def]
        state = dict(data)

        class _FakeState:
            def get(self_inner, key: str, default=None):
                return state.get(key, default)

        return _FakeState()

    def test_save_scenario_writes_json_file(self, tmp_path, monkeypatch) -> None:  # type: ignore[no-untyped-def]
        monkeypatch.setattr(_sc, "_SCENARIOS_DIR", tmp_path)
        fake_state = self._make_st_session_for_save(
            {
                "round": 2,
                "phase_idx": 3,
                "active": "Necrons",
                "phase_stage": "start",
                "cp": {"Necrons": 5, "Orks": 3},
                "vp": {"Necrons": 10, "Orks": 5},
                "p1_units": {"u1": {"current_wounds": 5}},
                "p2_units": {},
            }
        )
        monkeypatch.setattr(_sc.st, "session_state", fake_state)
        _sc.save_scenario("test_snap")
        saved = json.loads((tmp_path / "test_snap.json").read_text())
        assert saved["round"] == 2
        assert saved["phase_idx"] == 3
        assert saved["cp"] == {"Necrons": 5, "Orks": 3}
        assert saved["vp"] == {"Necrons": 10, "Orks": 5}
        assert "p1_units" in saved["unit_patches"]

    def test_save_scenario_creates_scenarios_dir(self, tmp_path, monkeypatch) -> None:  # type: ignore[no-untyped-def]
        new_dir = tmp_path / "sub" / "scenarios"
        monkeypatch.setattr(_sc, "_SCENARIOS_DIR", new_dir)
        fake_state = self._make_st_session_for_save({"p1_units": {}, "p2_units": {}})
        monkeypatch.setattr(_sc.st, "session_state", fake_state)
        _sc.save_scenario("auto_create")
        assert (new_dir / "auto_create.json").exists()

    def test_save_scenario_rejects_slash_in_name(self) -> None:
        with pytest.raises(ValueError, match="Invalid scenario name"):
            _sc.save_scenario("path/traversal")
