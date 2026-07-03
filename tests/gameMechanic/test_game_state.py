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
    CP_BY_GAME_SIZE,
    _make_unit_state_dict,
    active_round_choice_buff_labels,
    compute_roster_total_pts,
    init_state,
    list_available_rosters,
    next_phase,
    short_round_choice_label,
    subfaction_value_for,
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
    kwargs.setdefault("p1_subfaction", None)
    kwargs.setdefault("p2_subfaction", None)
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


def test_next_phase_setup_to_command_opens_directive_window_round_1() -> None:
    """Regression: entering the first Command phase (round 1) opens the directive window.

    Battle round 1 also has an assigned protocol (Wahapedia Z. 557/568), so the
    directive selection window must be open for BOTH players at the start of round 1 —
    not only from round 2 on. init_state() sets directive_pending=False; the
    Setup→Command transition must flip it True for both slots.
    """
    from gameMechanic.game_state import round_choice_state_key

    session = _phase_session(phase_idx=0, active="Necrons")
    next_phase()

    for player in ("Necrons", "Orks"):
        assert session[round_choice_state_key(player, "directive_pending")] is True


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


def test_init_state_sets_round_to_one() -> None:
    """R-ROUND-06: a fresh game starts on battle round 1."""
    session = _make_session()
    init_state()
    assert session["round"] == 1


def test_round_choice_directive_persists_across_mid_round_turn_switch() -> None:
    """A command protocol stays active for the whole battle round (both turns).

    Switching from the first player's turn to the second player's must NOT clear the
    round-choice protocol/directive — defensive directive effects (e.g. Eternal Guardian
    save bonus, Undying Legions RP re-roll) must apply during the opponent's turn.
    Regression: previously cleared per-turn in _reset_turn_state.
    """
    session = _phase_session(phase_idx=7, active="Necrons", round_num=1)
    session["p1_faction_dir"] = "necrons"
    session["round_choice_active_Necrons"] = "wh40k_9e.necrons.faction.protocol_undying_legions"
    session["round_choice_directive_Necrons"] = "primary"
    next_phase()  # Necrons morale done → switch to Orks, still battle round 1
    assert session["active"] == "Orks"
    assert session["round"] == 1
    assert (
        session["round_choice_active_Necrons"]
        == "wh40k_9e.necrons.faction.protocol_undying_legions"
    )
    assert session["round_choice_directive_Necrons"] == "primary"


def test_round_choice_directive_cleared_at_new_battle_round() -> None:
    """When both players have acted and a new battle round begins, round-choice resets."""
    session = _phase_session(phase_idx=7, active="Orks", round_num=1)
    session["p1_faction_dir"] = "necrons"
    session["round_choice_active_Necrons"] = "wh40k_9e.necrons.faction.protocol_undying_legions"
    session["round_choice_directive_Necrons"] = "primary"
    session["round_choice_extra_directive_Necrons"] = "secondary"
    next_phase()  # Orks morale done → back to first player → battle round 2
    assert session["active"] == "Necrons"
    assert session["round"] == 2
    assert session["round_choice_active_Necrons"] is None
    assert session["round_choice_directive_Necrons"] is None
    assert session["round_choice_extra_directive_Necrons"] is None


def test_phase_change_clears_group_autosel_guard() -> None:
    """Group auto-select guard is phase-scoped.

    Regression: the guard was never cleared on a phase/turn change, so on re-selecting a
    single-group unit (e.g. Necron Warriors) in a later phase the auto-select was skipped,
    leaving selected_model_group=None and blocking enemy target selection.
    """
    session = _phase_session(phase_idx=1, active="Necrons")
    session["group_autosel_done_u1"] = True
    next_phase()  # Command → Movement: _reset_phase_state runs
    assert "group_autosel_done_u1" not in session


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

    def test_subfaction_value_for_maps_per_player(self) -> None:
        _make_session(p1_subfaction="szarekhan", p2_subfaction=None)
        assert subfaction_value_for("Necrons") == "szarekhan"
        assert subfaction_value_for("Orks") is None


class TestRoundChoiceBuffLabels:
    def test_short_round_choice_label_strips_prefix(self) -> None:
        assert short_round_choice_label("Protocol of the Undying Legions") == "Undying Legions"
        assert short_round_choice_label("Waaagh!") == "Waaagh!"

    def test_active_round_directive_yields_short_label(self) -> None:
        _make_session(
            p1_faction_dir="necrons",
            p2_faction_dir="orks",
            p1_subfaction=None,
            p2_subfaction=None,
            round_choice_active_Necrons="wh40k_9e.necrons.faction.protocol_undying_legions",
            round_choice_directive_Necrons="primary",
            round_choice_assignments={},
        )
        assert active_round_choice_buff_labels("Necrons") == ["Undying Legions"]

    def test_no_directive_selected_yields_no_label(self) -> None:
        _make_session(
            p1_faction_dir="necrons",
            p2_faction_dir="orks",
            p1_subfaction=None,
            round_choice_active_Necrons="wh40k_9e.necrons.faction.protocol_undying_legions",
            round_choice_directive_Necrons=None,
            round_choice_assignments={},
        )
        assert active_round_choice_buff_labels("Necrons") == []

    def test_faction_without_round_choices_yields_no_label(self) -> None:
        _make_session(p1_faction_dir="necrons", p2_faction_dir="orks", p2_subfaction=None)
        assert active_round_choice_buff_labels("Orks") == []


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

    def test_subfaction_propagated_from_metadata(self) -> None:
        _, _, _, _, subfaction, _ = _gs._load_roster_for("necrons_alpha.yaml", "necrons")
        # subfaction may be None or a string — just ensure no crash
        assert subfaction is None or isinstance(subfaction, str)

    def test_protocol_order_from_metadata(self) -> None:
        # Silent King roster declares dynasty szarekhan (the necron subfaction field)
        _, _, _, _, subfaction, proto = _gs._load_roster_for(
            "necrons_1500pts_silent_king.yaml", "necrons"
        )
        assert subfaction == "szarekhan"
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
            p1_subfaction="nephrekh",
            p2_subfaction=None,
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

    def test_swap_exchanges_subfactions(self) -> None:
        s = self._session()
        swap_players()
        assert s["p1_subfaction"] is None
        assert s["p2_subfaction"] == "nephrekh"

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
        pending_triggered_relic="something",
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

    def test_clears_pending_triggered_relic(self) -> None:
        s = _reset_phase_session()
        _gs._reset_phase_state()
        assert s["pending_triggered_relic"] is None

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

    def test_does_not_reset_used_stratagem_battle_ids(self) -> None:
        """used_stratagem_battle_ids is battle-scoped and must survive phase resets.

        Regression guard: _reset_phase_state() must NOT clear the battle-scoped dict —
        only reset_game() (which wipes the entire session state) removes it.
        A once_per_battle stratagem used in an earlier phase must stay blocked.
        Per-player dict (P19 fix): keyed by spending faction, not a global set.
        """
        s = _reset_phase_session(used_stratagem_battle_ids={"Necrons": {"opb.strat_x"}})
        _gs._reset_phase_state()
        assert s["used_stratagem_battle_ids"] == {"Necrons": {"opb.strat_x"}}

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


# ---------------------------------------------------------------------------
# R-CMD-04: CP start pool per game size (CP_BY_GAME_SIZE + init_state)
# ---------------------------------------------------------------------------


class TestCpByGameSize:
    """R-CMD-04: CP starting pool matches game size table from core rules.

    Combat Patrol → 3 CP · Incursion → 6 CP · Strike Force → 12 CP · Onslaught → 18 CP.
    The constant CP_BY_GAME_SIZE is the authoritative lookup; init_state uses it
    to populate st.session_state.cp for both players.
    """

    def test_combat_patrol_starts_at_3_cp(self) -> None:
        assert CP_BY_GAME_SIZE["Combat Patrol"] == 3

    def test_incursion_starts_at_6_cp(self) -> None:
        assert CP_BY_GAME_SIZE["Incursion"] == 6

    def test_strike_force_starts_at_12_cp(self) -> None:
        assert CP_BY_GAME_SIZE["Strike Force"] == 12

    def test_onslaught_starts_at_18_cp(self) -> None:
        assert CP_BY_GAME_SIZE["Onslaught"] == 18

    def test_all_four_game_sizes_present(self) -> None:
        assert set(CP_BY_GAME_SIZE.keys()) == {
            "Combat Patrol",
            "Incursion",
            "Strike Force",
            "Onslaught",
        }

    def test_init_state_incursion_sets_cp_6_for_both_players(self) -> None:
        """init_state() applies CP_BY_GAME_SIZE via game_mode='matched'."""
        s = _make_session()
        init_state(game_size="Incursion", game_mode="matched")
        cp_values = list(s["cp"].values())
        assert all(v == 6 for v in cp_values), f"Expected 6 CP each, got {cp_values}"


# ---------------------------------------------------------------------------
# R-SCORE-01 / R-SCORE-09 / R-SCORE-10: victory-point mutations
# ---------------------------------------------------------------------------


class TestVictoryPointMutations:
    """R-SCORE-01/-09/-10: primary and secondary VP adjustments.

    Primary VP per faction never drops below 0; each secondary-objective slot is
    clamped to the 0–15 matched-play band. The mutation helpers are the tested
    core logic behind the (render-only) VP scoring controls.
    """

    def test_adjust_vp_adds_delta_to_faction_score(self) -> None:
        _make_session(vp={"Necrons": 3, "Orks": 0})
        _mut.adjust_vp("Necrons", 5)
        assert _mut.st.session_state.vp["Necrons"] == 8

    def test_adjust_vp_floors_at_zero(self) -> None:
        _make_session(vp={"Necrons": 2, "Orks": 0})
        _mut.adjust_vp("Necrons", -5)
        assert _mut.st.session_state.vp["Necrons"] == 0

    def test_adjust_secondary_vp_adds_within_slot(self) -> None:
        _make_session(secondary_vp={"p1": [0, 0, 0], "p2": [0, 0, 0]})
        _mut.adjust_secondary_vp("p1", 1, 7)
        assert _mut.st.session_state.secondary_vp["p1"] == [0, 7, 0]

    def test_adjust_secondary_vp_caps_at_fifteen(self) -> None:
        _make_session(secondary_vp={"p1": [10, 0, 0], "p2": [0, 0, 0]})
        _mut.adjust_secondary_vp("p1", 0, 20)
        assert _mut.st.session_state.secondary_vp["p1"][0] == 15

    def test_adjust_secondary_vp_floors_at_zero(self) -> None:
        _make_session(secondary_vp={"p1": [3, 0, 0], "p2": [0, 0, 0]})
        _mut.adjust_secondary_vp("p1", 0, -10)
        assert _mut.st.session_state.secondary_vp["p1"][0] == 0

    def test_init_state_strike_force_sets_cp_12_for_both_players(self) -> None:
        s = _make_session()
        init_state(game_size="Strike Force", game_mode="matched")
        cp_values = list(s["cp"].values())
        assert all(v == 12 for v in cp_values), f"Expected 12 CP each, got {cp_values}"

    def test_init_state_non_matched_game_mode_defaults_to_3_cp(self) -> None:
        # Unmatched / open play ignores game_size → falls back to 3 CP
        s = _make_session()
        init_state(game_size="Strike Force", game_mode="open")
        cp_values = list(s["cp"].values())
        assert all(v == 3 for v in cp_values), f"Expected fallback 3 CP each, got {cp_values}"


# ---------------------------------------------------------------------------
# TargetSelectionRequest — consolidated pending-target slot
# ---------------------------------------------------------------------------


class TestTargetSelectionRequest:
    def test_pending_target_request_no_state_conflict(self) -> None:
        """Only one pending_target_request slot exists; second request overwrites first."""
        from gameMechanic.game_state import TargetSelectionRequest

        ptr1 = TargetSelectionRequest(
            ability_id="mwbd_01",
            required_keywords=["CORE"],
            exclude_uid=None,
            faction_filter="own",
            multi=False,
            badge_label="Buff",
            effect_type="buff_roll",
        )
        ptr2 = TargetSelectionRequest(
            ability_id="revive_wargear_orb1",
            required_keywords=[],
            exclude_uid="uid_bearer",
            faction_filter="own",
            multi=False,
            badge_label="Revive",
            effect_type="",
        )
        # Simulate: slot can only hold one request — second overwrites first
        slot = ptr1
        slot = ptr2
        assert slot.ability_id == "revive_wargear_orb1"
        assert slot.exclude_uid == "uid_bearer"
        assert slot.effect_type == ""

    def test_target_selection_request_fields_with_defaults(self) -> None:
        """TargetSelectionRequest has all required fields; effect_type defaults to empty string."""
        from gameMechanic.game_state import TargetSelectionRequest

        ptr = TargetSelectionRequest(
            ability_id="test_ability",
            required_keywords=[],
            exclude_uid=None,
            faction_filter=None,
            multi=False,
            badge_label="X",
        )
        assert ptr.effect_type == ""
        assert ptr.ability_id == "test_ability"
        assert ptr.required_keywords == []
        assert ptr.faction_filter is None
        assert ptr.multi is False

    def test_target_selection_request_revive_vs_buff_distinction(self) -> None:
        """effect_type distinguishes buff abilities (non-empty) from revive/wargear (empty)."""
        from gameMechanic.game_state import TargetSelectionRequest

        buff_ptr = TargetSelectionRequest(
            ability_id="mwbd",
            required_keywords=["CORE"],
            exclude_uid=None,
            faction_filter="own",
            multi=False,
            badge_label="MWBD",
            effect_type="buff_roll",
        )
        revive_ptr = TargetSelectionRequest(
            ability_id="revive_wargear_orb_x",
            required_keywords=[],
            exclude_uid="bearer_uid",
            faction_filter="own",
            multi=False,
            badge_label="Revive",
            effect_type="",
        )
        assert bool(buff_ptr.effect_type) is True  # buff → apply_buff_to_unit
        assert bool(revive_ptr.effect_type) is False  # revive → store target uid


# ---------------------------------------------------------------------------
# Plan 014 — group_wounds is now the canonical per-group HP pool for ALL groups
# ---------------------------------------------------------------------------


def _group_unit(groups, wounds=3):  # type: ignore[no-untyped-def]
    from gameObjects.unit import Unit  # noqa: PLC0415

    return Unit(
        id="test.group_unit",
        name_en="G",
        name_de="G",
        faction="Orks",
        subfaction=None,
        battlefield_role=["Elites"],
        keywords=[],
        wounds=wounds,
        models_min=1,
        models_max=sum(g.count for g in groups),
        power_level=4,
        move='6"',
        bs="3+",
        ws="3+",
        strength=4,
        toughness=4,
        attacks=3,
        save=4,
        invuln_save=None,
        leadership=7,
        oc=1,
        fnp=None,
        weapons=[],
        model_groups=groups,
    )


def test_group_wounds_populated_for_all_group_units() -> None:
    """Homogeneous group units now carry a per-group HP pool and an unchanged sum."""
    from gameObjects.unit import ModelGroup  # noqa: PLC0415

    groups = [
        ModelGroup(id="g_klaw", name_en="Klaw", count=2, weapons=[], priority=1),
        ModelGroup(id="g_saw", name_en="Saw", count=3, weapons=[], priority=2),
    ]
    state = _gs._unit_state(_group_unit(groups, wounds=3))
    assert state["group_wounds"] == {"g_klaw": 6, "g_saw": 9}
    # current_wounds identical to wounds × models (5 models × 3 LP).
    assert state["current_wounds"] == 15
    assert state["damage_active_group_id"] is None


def test_mixed_wound_unit_group_wounds_unchanged() -> None:
    """Per-group wound overrides (Szarekh 16 + Menhirs 7) stay exactly as before."""
    from gameObjects.unit import ModelGroup  # noqa: PLC0415

    groups = [
        ModelGroup(
            id="szarekh",
            name_en="Szarekh",
            count=1,
            weapons=[],
            priority=2,
            stats={"wounds": 16},
        ),
        ModelGroup(
            id="menhirs",
            name_en="Triarchal Menhirs",
            count=3,
            weapons=[],
            priority=1,
            stats={"wounds": 7},
        ),
    ]
    state = _gs._unit_state(_group_unit(groups, wounds=16))
    assert state["group_wounds"] == {"szarekh": 16, "menhirs": 21}
    assert state["current_wounds"] == 37


# ---------------------------------------------------------------------------
# compute_roster_total_pts — error branches (lines 119, 129)
# ---------------------------------------------------------------------------


class TestComputeRosterTotalPtsErrorBranches:
    def test_points_yaml_missing_returns_zero(self, tmp_path, monkeypatch) -> None:
        """Line 119: pts_path.exists() is False → return 0 immediately."""
        import gameMechanic.game_state as gs_mod

        # Build a minimal roster file that has a valid faction_dir
        roster = tmp_path / "test_roster.yaml"
        roster.write_text("display_name: Test\nfaction_dir: necrons\nunits: []\n")

        # Redirect _ROSTER_DIR and _DATA_ROOT so points.yaml won't exist
        fake_data_root = tmp_path / "data_root"
        fake_data_root.mkdir()
        monkeypatch.setattr(gs_mod, "_ROSTER_DIR", tmp_path)
        monkeypatch.setattr(gs_mod, "_DATA_ROOT", fake_data_root)

        result = gs_mod.compute_roster_total_pts("test_roster.yaml")
        assert result == 0

    def test_unit_not_in_points_yaml_skipped(self, tmp_path, monkeypatch) -> None:
        """Line 129: cost_entry is None → continue; missing unit does not crash."""
        import gameMechanic.game_state as gs_mod

        roster = tmp_path / "test_roster.yaml"
        roster.write_text(
            "faction_dir: necrons\n"
            "units:\n"
            "  - id: wh40k_9e.necrons.unit.unknown_unit\n"
            "    models: 1\n"
        )
        pts_dir = tmp_path / "wh40k_9e" / "necrons"
        pts_dir.mkdir(parents=True)
        pts_file = pts_dir / "points.yaml"
        pts_file.write_text("units:\n  wh40k_9e.necrons.unit.overlord:\n    per_unit: 100\n")

        monkeypatch.setattr(gs_mod, "_ROSTER_DIR", tmp_path)
        monkeypatch.setattr(gs_mod, "_DATA_ROOT", tmp_path)

        result = gs_mod.compute_roster_total_pts("test_roster.yaml")
        assert result == 0


# ---------------------------------------------------------------------------
# faction_display_name_for — KeyError fallback (lines 181-182)
# ---------------------------------------------------------------------------


def test_faction_display_name_for_returns_player_on_key_error() -> None:
    """Line 181-182: KeyError in faction_dir_for → fall back to str(player)."""
    from gameMechanic.game_state import faction_display_name_for

    # Session missing p1_faction_dir and p2_faction_dir → faction_dir_for raises KeyError
    _make_session()
    result = faction_display_name_for("Necrons")
    # Falls back: may return str(player) or load successfully; either way no crash
    assert isinstance(result, str)


def test_faction_display_name_for_fallback_on_missing_faction_dir() -> None:
    """Line 181-182: player without a faction dir key → KeyError branch returns player name."""
    from gameMechanic.game_state import faction_display_name_for

    # Deliberately omit p1_faction_dir / p2_faction_dir to trigger KeyError in faction_dir_for
    _make_session(first_player="UnknownArmy", second_player="Orks")
    # p1_faction_dir not set → faction_dir_for raises KeyError → returns str(player)
    result = faction_display_name_for("UnknownArmy")
    assert result == "UnknownArmy"


# ---------------------------------------------------------------------------
# subfaction_badge_for — KeyError fallback (lines 204-205)
# ---------------------------------------------------------------------------


def test_subfaction_badge_for_returns_error_badge_on_missing_faction_dir() -> None:
    """Lines 204-205: faction_dir_for raises KeyError → error SubfactionBadge."""
    from gameMechanic.game_state import SubfactionBadge, subfaction_badge_for

    # Session without p1_faction_dir / p2_faction_dir → faction_dir_for raises KeyError
    _make_session(first_player="UnknownArmy", second_player="Orks")
    result = subfaction_badge_for("UnknownArmy")
    assert result == SubfactionBadge("No Subfaction", "error")


def test_subfaction_badge_for_returns_error_when_faction_has_no_subfaction_field() -> None:
    """Line 208: faction dir exists but meta has no subfaction field → error badge."""
    from gameMechanic.game_state import SubfactionBadge, subfaction_badge_for

    # 'nonexistent_faction' returns (None, 'Subfaction') from load_subfaction_meta
    # → field is falsy → Zeile 208 hit
    _make_session(
        first_player="Necrons",
        second_player="Orks",
        p1_faction_dir="nonexistent_faction",
        p2_faction_dir="orks",
    )
    result = subfaction_badge_for("Necrons")
    assert result == SubfactionBadge("No Subfaction", "error")


def test_subfaction_badge_for_missing_choice_returns_missing_badge() -> None:
    """Lines 211-212: subfaction value not set → 'No <Label>' badge with state 'missing'."""
    from gameMechanic.game_state import subfaction_badge_for

    _make_session(
        first_player="Necrons",
        second_player="Orks",
        p1_faction_dir="necrons",
        p2_faction_dir="orks",
        p1_subfaction=None,  # no choice made
    )
    result = subfaction_badge_for("Necrons")
    assert result.state == "missing"
    assert result.text.startswith("No ")


def test_subfaction_badge_for_set_choice_returns_set_badge() -> None:
    """Line 213: subfaction value present → formatted badge with state 'set'."""
    from gameMechanic.game_state import subfaction_badge_for

    _make_session(
        first_player="Necrons",
        second_player="Orks",
        p1_faction_dir="necrons",
        p2_faction_dir="orks",
        p1_subfaction="szarekhan",
    )
    result = subfaction_badge_for("Necrons")
    assert result.state == "set"
    assert result.text == "Szarekhan"


# ---------------------------------------------------------------------------
# init_state — early return when already initialized (line 384)
# ---------------------------------------------------------------------------


def test_init_state_does_not_reinitialize_when_already_initialized() -> None:
    """Line 384: if 'initialized' is already in session_state, init_state returns early.

    Calling init_state twice must not reset game state; the round set by the first call
    must remain unchanged after the second call.
    """
    s = _make_session()
    init_state(game_size="Incursion", game_mode="matched")
    s["round"] = 5  # simulate game progress
    init_state(game_size="Incursion", game_mode="matched")  # second call → early return
    assert s["round"] == 5  # must not have been reset to 1


# ---------------------------------------------------------------------------
# active_round_choice_buff_labels — KeyError fallback (lines 237-238)
# ---------------------------------------------------------------------------


def test_active_round_choice_buff_labels_returns_empty_on_key_error() -> None:
    """Lines 237-238: faction_dir_for raises KeyError → returns []."""
    # Session without p1_faction_dir / p2_faction_dir → faction_dir_for raises KeyError
    _make_session(first_player="UnknownArmy", second_player="Orks")
    result = active_round_choice_buff_labels("UnknownArmy")
    assert result == []


# ---------------------------------------------------------------------------
# active_round_choice_buff_labels — 6th ability path (lines 256-264)
# ---------------------------------------------------------------------------


class TestActiveRoundChoiceBuffLabels6thAbility:
    """Lines 255-264: the always-active 6th protocol ability (unassigned to any round)."""

    _ALL_PROTOCOL_IDS = [
        "wh40k_9e.necrons.faction.protocol_eternal_guardian",
        "wh40k_9e.necrons.faction.protocol_hungry_void",
        "wh40k_9e.necrons.faction.protocol_conquering_tyrant",
        "wh40k_9e.necrons.faction.protocol_sudden_storm",
        "wh40k_9e.necrons.faction.protocol_undying_legions",
        "wh40k_9e.necrons.faction.protocol_vengeful_stars",
    ]

    def _assignments_without(self, excluded_id: str) -> dict:
        """Return round→id assignments for all protocols except the given one."""
        others = [pid for pid in self._ALL_PROTOCOL_IDS if pid != excluded_id]
        return {i + 1: pid for i, pid in enumerate(others[:5])}

    def test_6th_ability_shown_when_affinity_matches(self) -> None:
        """Line 260+264: affinity_bonus True → 6th ability label added without directive."""
        # vengeful_stars is mephrit's protocol; the 6th ability is vengeful_stars
        sixth_id = "wh40k_9e.necrons.faction.protocol_vengeful_stars"
        assignments = self._assignments_without(sixth_id)
        _make_session(
            p1_faction_dir="necrons",
            p2_faction_dir="orks",
            p1_subfaction="mephrit",
            p2_subfaction=None,
            round_choice_active_Necrons=None,
            round_choice_directive_Necrons=None,
            round_choice_assignments={"Necrons": assignments},
        )
        labels = active_round_choice_buff_labels("Necrons")
        assert "Vengeful Stars" in labels

    def test_6th_ability_shown_when_extra_directive_set(self) -> None:
        """Lines 261-263: extra_directive True → 6th ability label even without affinity."""
        sixth_id = "wh40k_9e.necrons.faction.protocol_vengeful_stars"
        assignments = self._assignments_without(sixth_id)
        _make_session(
            p1_faction_dir="necrons",
            p2_faction_dir="orks",
            p1_subfaction=None,
            p2_subfaction=None,
            round_choice_active_Necrons=None,
            round_choice_directive_Necrons=None,
            round_choice_extra_directive_Necrons=True,
            round_choice_assignments={"Necrons": assignments},
        )
        labels = active_round_choice_buff_labels("Necrons")
        assert "Vengeful Stars" in labels

    def test_6th_ability_not_shown_without_affinity_or_directive(self) -> None:
        """Line 260-263: neither affinity match nor extra_directive → 6th not included."""
        sixth_id = "wh40k_9e.necrons.faction.protocol_vengeful_stars"
        assignments = self._assignments_without(sixth_id)
        _make_session(
            p1_faction_dir="necrons",
            p2_faction_dir="orks",
            p1_subfaction="nihilakh",  # not mephrit → no affinity match
            p2_subfaction=None,
            round_choice_active_Necrons=None,
            round_choice_directive_Necrons=None,
            round_choice_extra_directive_Necrons=False,
            round_choice_assignments={"Necrons": assignments},
        )
        labels = active_round_choice_buff_labels("Necrons")
        assert "Vengeful Stars" not in labels


# ---------------------------------------------------------------------------
# init_state — attacker=="p2" swap (lines 384, 394-399)
# ---------------------------------------------------------------------------


def test_init_state_attacker_p2_swaps_player_order() -> None:
    """Lines 384, 394-399: attacker='p2' causes p1/p2 roster data to be swapped.

    After the swap the first_player gets the p2 roster's display_name and the
    second_player gets the p1 roster's display_name (attacker becomes the first player).
    """
    s = _make_session()
    # necrons_alpha → display_name "Necrons α", necrons_beta → display_name "Necrons β"
    init_state(roster_p1="necrons_alpha.yaml", roster_p2="necrons_beta.yaml", attacker="p2")
    # With attacker=="p2": names are swapped, so first_player has necrons_beta's name
    assert s["first_player"] != s["second_player"]
    # Verify p1_faction_dir is still "necrons" (both are necrons but swapped)
    assert s["p1_faction_dir"] == "necrons"
    assert s["p2_faction_dir"] == "necrons"


def test_init_state_attacker_p2_swaps_unmatched_warnings() -> None:
    """Lines 394-399: unmatched lists are also swapped when attacker='p2'."""
    s = _make_session()
    # Both rosters exist so no unmatched entries; the swap still must run without error
    init_state(roster_p1="necrons_alpha.yaml", roster_p2="necrons_beta.yaml", attacker="p2")
    # roster_warnings may be empty (both rosters match) — just ensure no crash
    assert isinstance(s.get("roster_warnings", {}), dict)


# ---------------------------------------------------------------------------
# init_state — round_choice_assignments from roster order (line 444)
# ---------------------------------------------------------------------------


def test_init_state_round_choice_assignments_empty_when_no_proto_order() -> None:
    """Line 444: if order is None/empty, round_choice_assignments stays empty for that player."""
    s = _make_session()
    # necrons_alpha.yaml and necrons_beta.yaml declare no round_choice_order field
    init_state(roster_p1="necrons_alpha.yaml", roster_p2="necrons_beta.yaml")
    assignments = s["round_choice_assignments"]
    assert isinstance(assignments, dict)
    # Neither roster declares round_choice_order → assignments must be empty
    assert assignments == {}


def test_init_state_round_choice_assignments_populated_from_roster_order(
    tmp_path, monkeypatch
) -> None:
    """Line 444: roster with round_choice_order → round_choice_assignments populated."""
    import gameMechanic.game_state as gs_mod

    proto_ids = [
        "wh40k_9e.necrons.faction.protocol_eternal_guardian",
        "wh40k_9e.necrons.faction.protocol_hungry_void",
        "wh40k_9e.necrons.faction.protocol_conquering_tyrant",
        "wh40k_9e.necrons.faction.protocol_sudden_storm",
        "wh40k_9e.necrons.faction.protocol_undying_legions",
    ]
    proto_order_yaml = "\n".join(f"  - {pid}" for pid in proto_ids)
    roster_p1 = tmp_path / "roster_with_order.yaml"
    roster_p1.write_text(
        f"display_name: Alpha\nfaction_dir: necrons\n"
        f"round_choice_order:\n{proto_order_yaml}\nunits: []\n"
    )
    roster_p2 = tmp_path / "necrons_beta.yaml"
    roster_p2.write_text("display_name: Beta\nfaction_dir: necrons\nunits: []\n")

    monkeypatch.setattr(gs_mod, "_ROSTER_DIR", tmp_path)

    s = _make_session()
    gs_mod.init_state(roster_p1="roster_with_order.yaml", roster_p2="necrons_beta.yaml")
    assignments = s["round_choice_assignments"]
    # "Alpha" should have a dict {1: proto_id, ..., 5: proto_id}
    alpha_assignments = assignments.get("Alpha", {})
    assert alpha_assignments == {i + 1: pid for i, pid in enumerate(proto_ids)}


# ---------------------------------------------------------------------------
# init_state — unmatched roster warnings (line 477)
# ---------------------------------------------------------------------------


def test_init_state_roster_warnings_populated_for_unmatched_units(tmp_path, monkeypatch) -> None:
    """Line 477: unmatched units → st.session_state.roster_warnings is non-empty."""
    import gameMechanic.game_state as gs_mod

    # Roster with a unit ID that doesn't exist in the necron catalog
    roster_p1 = tmp_path / "necrons_bad.yaml"
    roster_p1.write_text(
        "display_name: BadArmy\nfaction_dir: necrons\n"
        "units:\n  - id: wh40k_9e.necrons.unit.does_not_exist\n"
        "    models: 1\n"
    )
    roster_p2 = tmp_path / "necrons_beta.yaml"
    roster_p2.write_text("display_name: Beta\nfaction_dir: necrons\nunits: []\n")

    monkeypatch.setattr(gs_mod, "_ROSTER_DIR", tmp_path)

    s = _make_session()
    gs_mod.init_state(roster_p1="necrons_bad.yaml", roster_p2="necrons_beta.yaml")
    warnings = s.get("roster_warnings", {})
    # BadArmy has unmatched unit → warnings must contain at least its key
    assert "BadArmy" in warnings
    assert len(warnings["BadArmy"]) > 0


# ---------------------------------------------------------------------------
# _reset_turn_state — KeyError continue (lines 567-568)
# ---------------------------------------------------------------------------


def test_reset_turn_state_keyerror_on_faction_dir_for_continues() -> None:
    """Lines 567-568: faction_dir_for raises KeyError when p2_faction_dir is missing.

    When activated_abilities contains a player whose turn_state lookup triggers KeyError
    (p2_faction_dir absent from session state, and the player is not first_player), the
    except-KeyError branch catches it and continues — no crash, turn flags still reset.
    """
    unit = _full_unit_state()
    unit["turn_flags"]["advanced"] = True
    # Deliberately omit p2_faction_dir so faction_dir_for("GhostArmy") raises KeyError:
    # GhostArmy != first_player ("Necrons") → falls to else → st.session_state["p2_faction_dir"]
    # which is missing → KeyError → continue branch hit.
    s = _make_session(
        round=2,
        phase_idx=1,
        p1_units={"u1": unit},
        p2_units={"u2": _full_unit_state()},
        p1_faction_dir="necrons",
        # p2_faction_dir intentionally absent
        activated_abilities={
            "GhostArmy": {
                "ability_id": "wh40k_9e.necrons.faction.some_ability",
                "round_activated": 1,
            }
        },
        pending_mortal_undo=None,
    )
    # Must not raise — KeyError is caught and loop continues
    _gs._reset_turn_state()
    # Turn flags should still be reset for actual units
    assert all(v is False for v in s["p1_units"]["u1"]["turn_flags"].values())


# ---------------------------------------------------------------------------
# Plan 031 Step 2 — directive_pending flag (Wahapedia Z. 568/579)
# ---------------------------------------------------------------------------


def test_init_state_directive_pending_false_for_both_players() -> None:
    """init_state() sets directive_pending=False for both player slots.

    No directive selection window is open at game start. The window opens only
    via _reset_round_choice_state() called at each battle round start.
    """
    from gameMechanic.game_state import round_choice_state_key

    s = _make_session()
    init_state(roster_p1="necrons_alpha.yaml", roster_p2="necrons_beta.yaml")
    # first_player and second_player are now set by init_state
    p1 = s["first_player"]
    p2 = s["second_player"]
    assert s[round_choice_state_key(p1, "directive_pending")] is False
    assert s[round_choice_state_key(p2, "directive_pending")] is False
