"""Tests for game_state.py: next_phase, phase transitions, round increments."""

import sys
from pathlib import Path
from unittest.mock import MagicMock

_st_mock = MagicMock()
sys.modules["streamlit"] = _st_mock
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

import gameMechanic.game_state as _gs  # noqa: E402
import gameMechanic.unit_mutations as _mut  # noqa: E402
from gameMechanic.game_state import (  # noqa: E402
    _make_unit_state_dict,
    active_protocol_buff_labels,
    compute_roster_total_pts,
    dynasty_for,
    list_available_rosters,
    next_phase,
    short_protocol_label,
    swap_players,
    unit_id_from_state_key,
    unit_keys_for,
    units_key_for,
    units_list_for,
)


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
    return s


def _unit_state_dict() -> dict:
    return {
        "current_wounds": 5,
        "models": 1,
        "destroyed": False,
        "in_melee": False,
        "in_reserve": False,
        "deployment": "stationary",
        "lost_models_this_turn": 0,
        "movement_choice": None,
        "melee_with": [],
        "turn_flags": {
            "advanced": False,
            "retreated": False,
            "charged": False,
            "shot": False,
            "fought": False,
        },
    }


def _phase_session(phase_idx: int, active: str, round_num: int = 1, cp: dict | None = None) -> _S:
    return _make_session(
        phase_idx=phase_idx,
        active=active,
        round=round_num,
        cp=cp if cp is not None else {"Necrons": 4, "Orks": 4},
        selected_unit=None,
        selected_targets=[],
        p1_units={"u1": _unit_state_dict()},
        p2_units={"u2": _unit_state_dict()},
    )


# ---------------------------------------------------------------------------
# next_phase — state transitions
# ---------------------------------------------------------------------------


def test_next_phase_setup_goes_to_command() -> None:
    session = _phase_session(phase_idx=0, active="Necrons")
    next_phase()
    assert session["phase_idx"] == 1


def test_next_phase_advances_index_within_turn() -> None:
    session = _phase_session(phase_idx=1, active="Necrons")
    next_phase()
    assert session["phase_idx"] == 2


def test_next_phase_switches_active_player_after_necrons_morale() -> None:
    session = _phase_session(phase_idx=7, active="Necrons")
    next_phase()
    assert session["active"] == "Orks"
    assert session["phase_idx"] == 1


def test_next_phase_increments_round_after_orks_morale() -> None:
    session = _phase_session(phase_idx=7, active="Orks", round_num=1)
    next_phase()
    assert session["active"] == "Necrons"
    assert session["round"] == 2


def test_next_phase_does_not_award_cp_on_player_switch() -> None:
    """CP is granted manually via the Command Phase button — next_phase must not add CP."""
    session = _phase_session(phase_idx=7, active="Orks", cp={"Necrons": 4, "Orks": 4})
    next_phase()
    assert session["cp"]["Necrons"] == 4
    assert session["cp"]["Orks"] == 4


# ---------------------------------------------------------------------------
# active_buffs and command_ability_state
# ---------------------------------------------------------------------------


def test_reset_turn_state_clears_active_buffs() -> None:
    unit_with_buff = _unit_state_dict()
    unit_with_buff["active_buffs"] = [
        {"ability_id": "mwbd", "badge_label": "MWBD", "effect_type": "buff_roll"}
    ]
    session = _make_session(
        phase_idx=7,
        active="Orks",
        round=1,
        cp={"Necrons": 4, "Orks": 4},
        selected_unit=None,
        selected_targets=[],
        p1_units={"u1": unit_with_buff},
        p2_units={"u2": _unit_state_dict()},
    )
    next_phase()
    assert session["p1_units"]["u1"]["active_buffs"] == []
    assert session["p2_units"]["u2"]["active_buffs"] == []


def test_reset_turn_state_does_not_clear_command_ability_state() -> None:
    existing = {"mwbd": {"target_uid": "u2", "active_since_round": 1}}
    session = _make_session(
        phase_idx=7,
        active="Orks",
        round=1,
        cp={"Necrons": 4, "Orks": 4},
        selected_unit=None,
        selected_targets=[],
        p1_units={"u1": _unit_state_dict()},
        p2_units={"u2": _unit_state_dict()},
        command_ability_state=existing,
    )
    next_phase()
    assert session["command_ability_state"] == existing


def test_unit_state_active_buffs_starts_empty() -> None:
    from gameObjects.unit import Unit  # noqa: PLC0415

    unit = Unit(
        id="test.u",
        name_en="T",
        name_de="T",
        faction="Necrons",
        subfaction=None,
        battlefield_role=[],
        keywords=[],
        wounds=3,
        models_min=1,
        models_max=1,
        power_level=4,
        move='6"',
        bs="3+",
        ws="3+",
        strength=4,
        toughness=4,
        attacks=3,
        save=3,
        invuln_save=None,
        leadership=10,
        oc=2,
        fnp=None,
        rules=[],
    )
    state = _gs._unit_state(unit)
    assert state["active_buffs"] == []


def test_next_phase_resets_selected_unit_and_targets() -> None:
    session = _make_session(
        phase_idx=1,
        active="Necrons",
        round=1,
        cp={"Necrons": 4, "Orks": 4},
        selected_unit=("Necrons", "wh40k_9e.necrons.unit.overlord"),
        selected_targets=[("Orks", "wh40k_9e.orks.unit.big_mek")],
        p1_units={"u1": _unit_state_dict()},
        p2_units={"u2": _unit_state_dict()},
    )
    next_phase()
    assert session["selected_unit"] is None
    assert session["selected_targets"] == []


# ---------------------------------------------------------------------------
# unit_id_from_state_key — pure function
# ---------------------------------------------------------------------------


class TestUnitIdFromStateKey:
    def test_plain_id_returned_unchanged(self) -> None:
        assert (
            unit_id_from_state_key("wh40k_9e.necrons.unit.overlord")
            == "wh40k_9e.necrons.unit.overlord"
        )

    def test_hash_suffix_stripped(self) -> None:
        assert (
            unit_id_from_state_key("wh40k_9e.necrons.unit.warriors#1")
            == "wh40k_9e.necrons.unit.warriors"
        )

    def test_higher_suffix_stripped(self) -> None:
        assert unit_id_from_state_key("wh40k_9e.orks.unit.boyz#3") == "wh40k_9e.orks.unit.boyz"

    def test_zero_suffix_stripped(self) -> None:
        assert unit_id_from_state_key("some.unit#0") == "some.unit"


# ---------------------------------------------------------------------------
# units_key_for / faction_dir_for / units_list_for / unit_keys_for
# ---------------------------------------------------------------------------


class TestPlayerKeyHelpers:
    def _session(self) -> _S:
        return _make_session(
            p1_faction_dir="necrons",
            p2_faction_dir="orks",
            p1_units_list=["unit_a"],
            p2_units_list=["unit_b"],
            p1_unit_keys=["key_a"],
            p2_unit_keys=["key_b"],
        )

    def test_units_key_for_first_player_returns_p1(self) -> None:
        self._session()
        assert units_key_for("Necrons") == "p1_units"

    def test_units_key_for_second_player_returns_p2(self) -> None:
        self._session()
        assert units_key_for("Orks") == "p2_units"

    def test_units_list_for_first_player(self) -> None:
        self._session()
        assert units_list_for("Necrons") == ["unit_a"]

    def test_units_list_for_second_player(self) -> None:
        self._session()
        assert units_list_for("Orks") == ["unit_b"]

    def test_unit_keys_for_first_player(self) -> None:
        self._session()
        assert unit_keys_for("Necrons") == ["key_a"]

    def test_unit_keys_for_second_player(self) -> None:
        self._session()
        assert unit_keys_for("Orks") == ["key_b"]

    def test_dynasty_for_maps_per_player(self) -> None:
        _make_session(p1_dynasty="szarekhan", p2_dynasty=None)
        assert dynasty_for("Necrons") == "szarekhan"
        assert dynasty_for("Orks") is None


class TestProtocolBuffLabels:
    def test_short_protocol_label_strips_prefix(self) -> None:
        assert short_protocol_label("Protocol of the Undying Legions") == "Undying Legions"
        assert short_protocol_label("Waaagh!") == "Waaagh!"

    def test_active_round_protocol_directive_yields_short_label(self) -> None:
        _make_session(
            p1_faction_dir="necrons",
            p2_faction_dir="orks",
            p1_dynasty=None,
            p2_dynasty=None,
            protocol_active_necrons="wh40k_9e.necrons.faction.protocol_undying_legions",
            protocol_directive_necrons="primary",
            protocol_assignments={},
        )
        assert active_protocol_buff_labels("Necrons") == ["Undying Legions"]

    def test_no_directive_selected_yields_no_label(self) -> None:
        _make_session(
            p1_faction_dir="necrons",
            p2_faction_dir="orks",
            p1_dynasty=None,
            protocol_active_necrons="wh40k_9e.necrons.faction.protocol_undying_legions",
            protocol_directive_necrons=None,
            protocol_assignments={},
        )
        assert active_protocol_buff_labels("Necrons") == []

    def test_faction_without_protocols_yields_no_label(self) -> None:
        _make_session(p1_faction_dir="necrons", p2_faction_dir="orks", p2_dynasty=None)
        assert active_protocol_buff_labels("Orks") == []


# ---------------------------------------------------------------------------
# _make_unit_state_dict — duplicate-ID disambiguation
# ---------------------------------------------------------------------------


class TestMakeUnitStateDict:
    def _mock_unit(self, uid: str, wounds: int = 3, models_max: int = 1) -> MagicMock:
        u = MagicMock()
        u.id = uid
        u.wounds = wounds
        u.models_max = models_max
        u.model_groups = None
        return u

    def test_single_unit_no_suffix(self) -> None:
        u = self._mock_unit("unit.a")
        state_dict, keys = _make_unit_state_dict([(u, 1)])
        assert "unit.a" in state_dict
        assert keys == ["unit.a"]

    def test_duplicate_ids_get_hash_suffix(self) -> None:
        u = self._mock_unit("unit.warriors", models_max=10)
        state_dict, keys = _make_unit_state_dict([(u, 5), (u, 3)])
        assert "unit.warriors" in state_dict
        assert "unit.warriors#1" in state_dict
        assert len(keys) == 2

    def test_duplicate_states_are_independent(self) -> None:
        u = self._mock_unit("unit.warriors", models_max=10)
        state_dict, _ = _make_unit_state_dict([(u, 5), (u, 3)])
        assert state_dict["unit.warriors"]["models"] == 5
        assert state_dict["unit.warriors#1"]["models"] == 3

    def test_three_duplicates_all_suffixed(self) -> None:
        u = self._mock_unit("unit.warriors", models_max=10)
        state_dict, keys = _make_unit_state_dict([(u, 1), (u, 1), (u, 1)])
        assert "unit.warriors" in state_dict
        assert "unit.warriors#1" in state_dict
        assert "unit.warriors#2" in state_dict
        assert len(keys) == 3


# ---------------------------------------------------------------------------
# list_available_rosters — uses real data directory
# ---------------------------------------------------------------------------


class TestListAvailableRosters:
    def test_returns_list_of_yaml_filenames(self) -> None:
        rosters = list_available_rosters()
        assert isinstance(rosters, list)
        assert len(rosters) > 0
        assert all(r.endswith(".yaml") for r in rosters)

    def test_result_is_sorted(self) -> None:
        rosters = list_available_rosters()
        assert rosters == sorted(rosters)


# ---------------------------------------------------------------------------
# compute_roster_total_pts — uses real data files
# ---------------------------------------------------------------------------


class TestComputeRosterTotalPts:
    def test_necrons_alpha_returns_positive_int(self) -> None:
        pts = compute_roster_total_pts("necrons_alpha.yaml")
        assert isinstance(pts, int)
        assert pts > 0

    def test_nonexistent_roster_returns_zero(self) -> None:
        assert compute_roster_total_pts("does_not_exist.yaml") == 0

    def test_orks_roster_returns_positive_int(self) -> None:
        pts = compute_roster_total_pts("orks.yaml")
        assert isinstance(pts, int)
        assert pts > 0


# ---------------------------------------------------------------------------
# _load_roster_for — roster loading helper (lines 60-72)
# ---------------------------------------------------------------------------


class TestLoadRosterFor:
    def test_existing_file_returns_matched_units(self) -> None:
        matched, unmatched, display_name, faction_dir, dynasty, proto = _gs._load_roster_for(
            "necrons_alpha.yaml", "necrons"
        )
        assert len(matched) > 0
        assert faction_dir == "necrons"
        assert isinstance(display_name, str)

    def test_existing_file_display_name_from_metadata(self) -> None:
        _, _, display_name, _, _, _ = _gs._load_roster_for("necrons_alpha.yaml", "necrons")
        # display_name comes from YAML metadata or falls back to filename
        assert display_name != ""

    def test_missing_file_falls_back_to_full_catalog(self) -> None:
        matched, unmatched, display_name, faction_dir, dynasty, proto = _gs._load_roster_for(
            "does_not_exist_xyz.yaml", "necrons"
        )
        # Falls back: full catalog as matched, no unmatched
        assert len(matched) > 0
        assert unmatched == []
        assert faction_dir == "necrons"

    def test_missing_file_display_name_is_filename(self) -> None:
        _, _, display_name, _, _, _ = _gs._load_roster_for("missing.yaml", "necrons")
        assert display_name == "missing.yaml"

    def test_dynasty_propagated_from_metadata(self) -> None:
        _, _, _, _, dynasty, _ = _gs._load_roster_for("necrons_alpha.yaml", "necrons")
        # dynasty may be None or a string — just ensure no crash
        assert dynasty is None or isinstance(dynasty, str)

    def test_protocol_order_from_metadata(self) -> None:
        # Silent King roster declares dynasty szarekhan; protocol_order optional
        _, _, _, _, dynasty, proto = _gs._load_roster_for(
            "necrons_1500pts_silent_king.yaml", "necrons"
        )
        assert dynasty == "szarekhan"
        assert proto is None or isinstance(proto, list)


# ---------------------------------------------------------------------------
# swap_players — exchanges all p1/p2 session state (lines 332-338)
# ---------------------------------------------------------------------------


class TestSwapPlayers:
    def _session(self) -> _S:
        return _make_session(
            p1_units={"u_necron": {"models": 5}},
            p2_units={"u_ork": {"models": 10}},
            p1_units_list=["necron_unit"],
            p2_units_list=["ork_unit"],
            p1_unit_keys=["key_n"],
            p2_unit_keys=["key_o"],
            p1_faction_dir="necrons",
            p2_faction_dir="orks",
            p1_dynasty="nephrekh",
            p2_dynasty=None,
        )

    def test_swap_exchanges_player_names(self) -> None:
        s = self._session()
        swap_players()
        assert s["first_player"] == "Orks"
        assert s["second_player"] == "Necrons"

    def test_swap_exchanges_unit_dicts(self) -> None:
        s = self._session()
        swap_players()
        assert s["p1_units"] == {"u_ork": {"models": 10}}
        assert s["p2_units"] == {"u_necron": {"models": 5}}

    def test_swap_exchanges_unit_lists(self) -> None:
        s = self._session()
        swap_players()
        assert s["p1_units_list"] == ["ork_unit"]
        assert s["p2_units_list"] == ["necron_unit"]

    def test_swap_exchanges_faction_dirs(self) -> None:
        s = self._session()
        swap_players()
        assert s["p1_faction_dir"] == "orks"
        assert s["p2_faction_dir"] == "necrons"

    def test_swap_exchanges_dynasties(self) -> None:
        s = self._session()
        swap_players()
        assert s["p1_dynasty"] is None
        assert s["p2_dynasty"] == "nephrekh"

    def test_double_swap_restores_original(self) -> None:
        s = self._session()
        swap_players()
        swap_players()
        assert s["first_player"] == "Necrons"
        assert s["p1_faction_dir"] == "necrons"


# ---------------------------------------------------------------------------
# _reset_phase_state — clears per-phase flags (line 357 + full coverage)
# ---------------------------------------------------------------------------


def _full_unit_state() -> dict:
    """Complete unit state matching _unit_state() output."""
    return {
        "current_wounds": 5,
        "models": 1,
        "models_initial": 1,
        "destroyed": False,
        "in_melee": False,
        "in_reserve": False,
        "deployment": "stationary",
        "lost_models_this_turn": 0,
        "fled_models_this_turn": 0,
        "movement_choice": "stationary",
        "movement_chosen": False,
        "melee_with": [],
        "active_buffs": [],
        "models_lost_since_last_rp": 0,
        "group_models": {},
        "turn_flags": {
            "advanced": False,
            "retreated": False,
            "charged": False,
            "shot": False,
            "fought": False,
            "cast": False,
            "heroic_intervened": False,
            "morale_tested": False,
            "movement_locked": False,
            "mortal_effect_applied": False,
        },
    }


def _reset_phase_session(**extra) -> _S:
    s = _make_session(
        phase_idx=1,
        round=1,
        cp_granted_this_phase=True,
        morgog_cap_rolled_this_phase=True,
        pending_irongob="something",
        veil_awaiting_confirm=True,
        veil_core_target_uid="some_uid",
        applied_triggered_veil="used",
        used_stratagem_ids={"strat_a"},
        fight_current_player="Necrons",
        attack_declaration={"active": True, "entries": ["e1"]},
        selected_model_group="grp1",
        group_targets={"g": ["t"]},
        group_decl={"g": "done"},
        charge_phase_step=2,
        pending_hi=("Necrons", "overlord"),
        hi_targets=["u1"],
        active_modifiers=[
            {"expires_at_phase": "command", "buff": "+1 hit"},
            {"expires_at_phase": "shooting", "buff": "+1 hit"},
        ],
        p1_units={"u1": _full_unit_state()},
        p2_units={"u2": _full_unit_state()},
        **extra,
    )
    return s


class TestResetPhaseState:
    def test_clears_cp_granted_flag(self) -> None:
        s = _reset_phase_session()
        _gs._reset_phase_state()
        assert s["cp_granted_this_phase"] is False

    def test_clears_morgog_cap_flag(self) -> None:
        s = _reset_phase_session()
        _gs._reset_phase_state()
        assert s["morgog_cap_rolled_this_phase"] is False

    def test_clears_pending_irongob(self) -> None:
        s = _reset_phase_session()
        _gs._reset_phase_state()
        assert s["pending_irongob"] is None

    def test_clears_veil_state(self) -> None:
        s = _reset_phase_session()
        _gs._reset_phase_state()
        assert s["veil_awaiting_confirm"] is False
        assert s["veil_core_target_uid"] is None

    def test_deletes_applied_triggered_keys(self) -> None:
        s = _reset_phase_session()
        # applied_triggered_veil was set in the session
        assert "applied_triggered_veil" in s
        _gs._reset_phase_state()
        assert "applied_triggered_veil" not in s

    def test_resets_used_stratagem_ids(self) -> None:
        s = _reset_phase_session()
        _gs._reset_phase_state()
        assert s["used_stratagem_ids"] == set()

    def test_resets_fight_current_player(self) -> None:
        s = _reset_phase_session()
        _gs._reset_phase_state()
        assert s["fight_current_player"] is None

    def test_resets_attack_declaration(self) -> None:
        s = _reset_phase_session()
        _gs._reset_phase_state()
        assert s["attack_declaration"] == {"active": False, "entries": []}

    def test_resets_group_state(self) -> None:
        s = _reset_phase_session()
        _gs._reset_phase_state()
        assert s["selected_model_group"] is None
        assert s["group_targets"] == {}
        assert s["group_decl"] == {}

    def test_resets_charge_phase_step(self) -> None:
        s = _reset_phase_session()
        _gs._reset_phase_state()
        assert s["charge_phase_step"] == 1

    def test_removes_expired_phase_modifiers(self) -> None:
        # phase_idx=1 → current_phase="command"; modifier for "command" should be removed
        s = _reset_phase_session()
        _gs._reset_phase_state()
        remaining = s["active_modifiers"]
        assert all(m["expires_at_phase"] != "command" for m in remaining)

    def test_keeps_non_expired_modifiers(self) -> None:
        s = _reset_phase_session()
        _gs._reset_phase_state()
        remaining = s["active_modifiers"]
        assert any(m["expires_at_phase"] == "shooting" for m in remaining)


# ---------------------------------------------------------------------------
# _reset_turn_state — resets turn flags + WAAAGH upgrade (lines 401-402)
# ---------------------------------------------------------------------------


def _turn_state_session(*, activated: dict | None = None, round_num: int = 1) -> _S:
    unit = _full_unit_state()
    unit["turn_flags"]["advanced"] = True
    unit["lost_models_this_turn"] = 3
    unit["active_buffs"] = [{"ability_id": "mwbd"}]
    s = _make_session(
        round=round_num,
        phase_idx=1,
        p1_units={"u1": unit},
        p2_units={"u2": _full_unit_state()},
        p1_faction_dir="necrons",
        p2_faction_dir="orks",
        activated_abilities=activated or {},
        pending_mortal_undo=None,
    )
    return s


class TestResetTurnState:
    def test_clears_turn_flags(self) -> None:
        s = _turn_state_session()
        _gs._reset_turn_state()
        flags = s["p1_units"]["u1"]["turn_flags"]
        assert all(v is False for v in flags.values())

    def test_resets_lost_models(self) -> None:
        s = _turn_state_session()
        _gs._reset_turn_state()
        assert s["p1_units"]["u1"]["lost_models_this_turn"] == 0

    def test_clears_active_buffs(self) -> None:
        s = _turn_state_session()
        _gs._reset_turn_state()
        assert s["p1_units"]["u1"]["active_buffs"] == []

    def test_stage1_upgrades_to_stage2_on_new_round(self) -> None:
        # Ability with next_stage_id activated in round 1; now round 2 → ability_id advances
        s = _turn_state_session(
            activated={
                "Orks": {"ability_id": "wh40k_9e.orks.faction.waaagh_stage1", "round_activated": 1}
            },
            round_num=2,
        )
        _gs._reset_turn_state()
        assert (
            s["activated_abilities"]["Orks"]["ability_id"] == "wh40k_9e.orks.faction.waaagh_stage2"
        )

    def test_stage1_stays_in_same_round(self) -> None:
        s = _turn_state_session(
            activated={
                "Orks": {"ability_id": "wh40k_9e.orks.faction.waaagh_stage1", "round_activated": 1}
            },
            round_num=1,
        )
        _gs._reset_turn_state()
        assert (
            s["activated_abilities"]["Orks"]["ability_id"] == "wh40k_9e.orks.faction.waaagh_stage1"
        )

    def test_stage2_unchanged_no_next_stage(self) -> None:
        # Stage 2 has no next_stage_id → ability_id must not change
        s = _turn_state_session(
            activated={
                "Orks": {"ability_id": "wh40k_9e.orks.faction.waaagh_stage2", "round_activated": 1}
            },
            round_num=3,
        )
        _gs._reset_turn_state()
        assert (
            s["activated_abilities"]["Orks"]["ability_id"] == "wh40k_9e.orks.faction.waaagh_stage2"
        )


# ---------------------------------------------------------------------------
# reset_game — clears all session state (lines 342-346)
# ---------------------------------------------------------------------------


class TestResetGame:
    def test_clears_all_session_state_keys(self) -> None:
        from unittest.mock import patch  # noqa: PLC0415

        s = _make_session(round=3, phase_idx=4)
        s["extra_key"] = "value"

        with patch("gameMechanic.game_log.archive_and_reset_log"):
            _gs.reset_game()

        assert len(s) == 0
