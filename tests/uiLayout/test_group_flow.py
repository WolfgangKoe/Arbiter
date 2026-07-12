"""Tests for the 6m group-by-group declaration flow state helpers."""

import sys
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import MagicMock

sys.modules.setdefault("streamlit", MagicMock())
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

import uiLayout._common as common  # noqa: E402
from uiLayout._common import (  # noqa: E402
    group_target_selectable,
    is_group_target,
    reset_group_declaration_state,
    toggle_group_target,
)

_FIGHT_IDX = next(i for i, (_, key) in enumerate(common.PHASES) if key == "fight")
_SHOOTING_IDX = next(i for i, (_, key) in enumerate(common.PHASES) if key == "shooting")
_MOVEMENT_IDX = next(i for i, (_, key) in enumerate(common.PHASES) if key == "movement")


class FakeSessionState(dict):
    """Dict with attribute access — mirrors streamlit's session_state API."""

    def __getattr__(self, name):  # type: ignore[no-untyped-def]
        try:
            return self[name]
        except KeyError as exc:
            raise AttributeError(name) from exc

    def __setattr__(self, name, value):  # type: ignore[no-untyped-def]
        self[name] = value


def _group(gid: str, count: int, weapons: list | None = None) -> SimpleNamespace:
    return SimpleNamespace(id=gid, count=count, weapons=weapons or [])


def _setup(  # type: ignore[no-untyped-def]
    monkeypatch,
    *,
    groups,
    group_models,
    selected_group,
    phase_idx=_SHOOTING_IDX,
    melee_with=None,
):
    unit = SimpleNamespace(model_groups=groups)
    unit_state = {"group_models": group_models, "melee_with": melee_with or []}
    common.st.session_state = FakeSessionState(
        selected_unit=("orks", "boyz"),
        selected_model_group=selected_group,
        group_targets={},
        group_decl={},
        phase_idx=phase_idx,
    )
    monkeypatch.setattr(common, "lookup", lambda f, u: (unit, unit_state))


# ---------------------------------------------------------------------------
# toggle_group_target
# ---------------------------------------------------------------------------


def test_toggle_returns_false_without_selected_group(monkeypatch) -> None:  # type: ignore[no-untyped-def]
    _setup(
        monkeypatch,
        groups=[_group("ork_boy", 9)],
        group_models={"ork_boy": 9},
        selected_group=None,
    )
    assert toggle_group_target("necrons", "warriors") is False


def test_toggle_returns_false_for_unit_without_groups(monkeypatch) -> None:  # type: ignore[no-untyped-def]
    _setup(monkeypatch, groups=[], group_models={}, selected_group="ork_boy")
    assert toggle_group_target("necrons", "warriors") is False


def test_toggle_returns_false_for_unknown_group_id(monkeypatch) -> None:  # type: ignore[no-untyped-def]
    _setup(
        monkeypatch,
        groups=[_group("ork_boy", 9)],
        group_models={"ork_boy": 9},
        selected_group="boss_nob",
    )
    assert toggle_group_target("necrons", "warriors") is False


def test_toggle_assigns_target_to_selected_group(monkeypatch) -> None:  # type: ignore[no-untyped-def]
    _setup(
        monkeypatch,
        groups=[_group("ork_boy", 9)],
        group_models={"ork_boy": 9},
        selected_group="ork_boy",
    )
    assert toggle_group_target("necrons", "warriors") is True
    assert common.st.session_state.group_targets["ork_boy"] == [("necrons", "warriors")]


def test_toggle_adds_second_target_for_multi_model_group(monkeypatch) -> None:  # type: ignore[no-untyped-def]
    _setup(
        monkeypatch,
        groups=[_group("ork_boy", 9)],
        group_models={"ork_boy": 9},
        selected_group="ork_boy",
    )
    toggle_group_target("necrons", "warriors")
    toggle_group_target("necrons", "immortals")
    assert common.st.session_state.group_targets["ork_boy"] == [
        ("necrons", "warriors"),
        ("necrons", "immortals"),
    ]


def test_toggle_removes_assigned_target(monkeypatch) -> None:  # type: ignore[no-untyped-def]
    _setup(
        monkeypatch,
        groups=[_group("ork_boy", 9)],
        group_models={"ork_boy": 9},
        selected_group="ork_boy",
    )
    toggle_group_target("necrons", "warriors")
    toggle_group_target("necrons", "warriors")
    assert common.st.session_state.group_targets["ork_boy"] == []


def test_single_model_group_replaces_target(monkeypatch) -> None:  # type: ignore[no-untyped-def]
    """A group with one living model attacks a single target — new pick replaces old."""
    _setup(
        monkeypatch,
        groups=[_group("boss_nob", 1)],
        group_models={"boss_nob": 1},
        selected_group="boss_nob",
    )
    toggle_group_target("necrons", "warriors")
    toggle_group_target("necrons", "immortals")
    assert common.st.session_state.group_targets["boss_nob"] == [("necrons", "immortals")]


def test_single_living_model_in_larger_group_replaces_target(monkeypatch) -> None:  # type: ignore[no-untyped-def]
    """group_models (alive), not the initial count, decides the single-target rule."""
    _setup(
        monkeypatch,
        groups=[_group("ork_boy", 9)],
        group_models={"ork_boy": 1},
        selected_group="ork_boy",
    )
    toggle_group_target("necrons", "warriors")
    toggle_group_target("necrons", "immortals")
    assert common.st.session_state.group_targets["ork_boy"] == [("necrons", "immortals")]


def test_single_model_group_can_have_multiple_targets_in_fight_phase(monkeypatch) -> None:  # type: ignore[no-untyped-def]
    """In the fight phase a 1-model group may split attacks across targets (B1 regression)."""
    _setup(
        monkeypatch,
        groups=[_group("boss_nob", 1)],
        group_models={"boss_nob": 1},
        selected_group="boss_nob",
        phase_idx=_FIGHT_IDX,
        melee_with=[("necrons", "warriors"), ("necrons", "immortals")],
    )
    toggle_group_target("necrons", "warriors")
    toggle_group_target("necrons", "immortals")
    assert common.st.session_state.group_targets["boss_nob"] == [
        ("necrons", "warriors"),
        ("necrons", "immortals"),
    ]


def test_single_model_group_still_replaces_target_in_shooting_phase(monkeypatch) -> None:  # type: ignore[no-untyped-def]
    """In the shooting phase a 1-model group still replaces its single target (B1 regression)."""
    _setup(
        monkeypatch,
        groups=[_group("boss_nob", 1)],
        group_models={"boss_nob": 1},
        selected_group="boss_nob",
        phase_idx=_SHOOTING_IDX,
    )
    toggle_group_target("necrons", "warriors")
    toggle_group_target("necrons", "immortals")
    assert common.st.session_state.group_targets["boss_nob"] == [("necrons", "immortals")]


# ---------------------------------------------------------------------------
# is_group_target
# ---------------------------------------------------------------------------


def test_is_group_target_true_for_assigned_target(monkeypatch) -> None:  # type: ignore[no-untyped-def]
    _setup(
        monkeypatch,
        groups=[_group("ork_boy", 9)],
        group_models={"ork_boy": 9},
        selected_group="ork_boy",
    )
    toggle_group_target("necrons", "warriors")
    assert is_group_target("necrons", "warriors") is True
    assert is_group_target("necrons", "immortals") is False


def test_is_group_target_false_without_selected_group(monkeypatch) -> None:  # type: ignore[no-untyped-def]
    _setup(
        monkeypatch,
        groups=[_group("ork_boy", 9)],
        group_models={"ork_boy": 9},
        selected_group="ork_boy",
    )
    toggle_group_target("necrons", "warriors")
    common.st.session_state.selected_model_group = None
    assert is_group_target("necrons", "warriors") is False


# ---------------------------------------------------------------------------
# group_target_selectable + fight phase engagement (6n A1)
# ---------------------------------------------------------------------------


def test_selectable_outside_group_phases(monkeypatch) -> None:  # type: ignore[no-untyped-def]
    """Movement/charge etc. never restrict ▷ — the group flow is not active there."""
    _setup(
        monkeypatch,
        groups=[_group("ork_boy", 9)],
        group_models={"ork_boy": 9},
        selected_group=None,
        phase_idx=_MOVEMENT_IDX,
    )
    assert group_target_selectable("necrons", "warriors") is True


def test_selectable_for_legacy_unit_without_groups(monkeypatch) -> None:  # type: ignore[no-untyped-def]
    _setup(monkeypatch, groups=[], group_models={}, selected_group=None)
    assert group_target_selectable("necrons", "warriors") is True


def test_not_selectable_without_selected_group(monkeypatch) -> None:  # type: ignore[no-untyped-def]
    """Group flow active, no group picked, no auto-select (no weapons) — ▷ stays disabled."""
    _setup(
        monkeypatch,
        groups=[_group("ork_boy", 9)],  # weapons=[] → not eligible → auto-select stays None
        group_models={"ork_boy": 9},
        selected_group=None,
    )
    assert group_target_selectable("necrons", "warriors") is False


def test_selectable_when_sole_eligible_group_would_auto_select(monkeypatch) -> None:  # type: ignore[no-untyped-def]
    """Bug 2 regression: second player as attacker — left column renders BEFORE center.

    selected_model_group is None when group_target_selectable is evaluated, but
    render_group_cards (center) would immediately auto-select the single eligible group.
    Without the fix: _single_eligible_group not consulted → returns False → target button
    disabled → player must deselect+reselect to unblock.
    With the fix: _single_eligible_group detects the sole eligible group → returns True.
    """
    ranged_profile = SimpleNamespace(is_melee=False, weapon_type="Rapid Fire")
    ranged_weapon = SimpleNamespace(profiles=[ranged_profile])
    _setup(
        monkeypatch,
        groups=[_group("warriors_models", 10, weapons=[ranged_weapon])],
        group_models={"warriors_models": 10},
        selected_group=None,  # centre column hasn't run yet — auto-select pending
        phase_idx=_SHOOTING_IDX,
    )
    assert group_target_selectable("necrons", "target_unit") is True


def test_not_selectable_when_multiple_eligible_groups_no_selection(monkeypatch) -> None:  # type: ignore[no-untyped-def]
    """Two eligible groups: auto-select does NOT fire → group must be chosen explicitly."""
    ranged_profile = SimpleNamespace(is_melee=False, weapon_type="Rapid Fire")
    ranged_weapon = SimpleNamespace(profiles=[ranged_profile])
    _setup(
        monkeypatch,
        groups=[
            _group("group_a", 5, weapons=[ranged_weapon]),
            _group("group_b", 5, weapons=[ranged_weapon]),
        ],
        group_models={"group_a": 5, "group_b": 5},
        selected_group=None,
        phase_idx=_SHOOTING_IDX,
    )
    assert group_target_selectable("necrons", "target_unit") is False


def test_shooting_allows_any_enemy(monkeypatch) -> None:  # type: ignore[no-untyped-def]
    _setup(
        monkeypatch,
        groups=[_group("ork_boy", 9)],
        group_models={"ork_boy": 9},
        selected_group="ork_boy",
        phase_idx=_SHOOTING_IDX,
    )
    assert group_target_selectable("necrons", "warriors") is True


def test_fight_phase_requires_engagement(monkeypatch) -> None:  # type: ignore[no-untyped-def]
    """In the fight phase only engaged enemies are legal group targets."""
    _setup(
        monkeypatch,
        groups=[_group("ork_boy", 9)],
        group_models={"ork_boy": 9},
        selected_group="ork_boy",
        phase_idx=_FIGHT_IDX,
        melee_with=[["necrons", "overlord"]],
    )
    assert group_target_selectable("necrons", "overlord") is True
    assert group_target_selectable("necrons", "warriors") is False


def test_fight_toggle_ignores_unengaged_target(monkeypatch) -> None:  # type: ignore[no-untyped-def]
    """The click is consumed (no legacy fallback) but nothing is assigned."""
    _setup(
        monkeypatch,
        groups=[_group("ork_boy", 9)],
        group_models={"ork_boy": 9},
        selected_group="ork_boy",
        phase_idx=_FIGHT_IDX,
        melee_with=[["necrons", "overlord"]],
    )
    assert toggle_group_target("necrons", "warriors") is True
    assert common.st.session_state.group_targets == {}


def test_fight_toggle_assigns_engaged_target(monkeypatch) -> None:  # type: ignore[no-untyped-def]
    _setup(
        monkeypatch,
        groups=[_group("ork_boy", 9)],
        group_models={"ork_boy": 9},
        selected_group="ork_boy",
        phase_idx=_FIGHT_IDX,
        melee_with=[["necrons", "overlord"]],
    )
    assert toggle_group_target("necrons", "overlord") is True
    assert common.st.session_state.group_targets["ork_boy"] == [("necrons", "overlord")]


def test_shooting_blocks_target_in_friendly_melee(monkeypatch) -> None:  # type: ignore[no-untyped-def]
    """P14: enemies locked in melee with the attacker's friends are not selectable."""
    _setup(monkeypatch, groups=[], group_models={}, selected_group=None)
    monkeypatch.setattr(common, "units_key_for", lambda p: f"{p}_units")
    common.st.session_state["necrons_units"] = {
        "warriors": {"melee_with": [["orks", "gretchin"]]},
        "immortals": {"melee_with": []},
    }
    assert group_target_selectable("necrons", "warriors") is False
    assert group_target_selectable("necrons", "immortals") is True


def test_fight_phase_does_not_apply_friendly_melee_block(monkeypatch) -> None:  # type: ignore[no-untyped-def]
    """The friendly-melee restriction is a shooting rule — fighting INTO melee is the point."""
    _setup(
        monkeypatch,
        groups=[_group("ork_boy", 9)],
        group_models={"ork_boy": 9},
        selected_group="ork_boy",
        phase_idx=_FIGHT_IDX,
        melee_with=[["necrons", "warriors"]],
    )
    monkeypatch.setattr(common, "units_key_for", lambda p: f"{p}_units")
    common.st.session_state["necrons_units"] = {
        "warriors": {"melee_with": [["orks", "boyz"]]},
    }
    assert group_target_selectable("necrons", "warriors") is True


# ---------------------------------------------------------------------------
# reset_group_declaration_state
# ---------------------------------------------------------------------------


def test_reset_clears_all_group_state() -> None:
    common.st.session_state = FakeSessionState(
        selected_model_group="ork_boy",
        group_targets={"ork_boy": [("necrons", "warriors")]},
        group_decl={"ork_boy": [{"weapon_name": "Choppa"}]},
    )
    reset_group_declaration_state()
    assert common.st.session_state.selected_model_group is None
    assert common.st.session_state.group_targets == {}
    assert common.st.session_state.group_decl == {}


# ---------------------------------------------------------------------------
# reset_group_declaration_state — clears stale counter widget keys (G4)
# ---------------------------------------------------------------------------


def test_reset_clears_stale_declaration_counter_keys() -> None:
    """G4: leftover decl_*/group_autosel_done_* keys must not survive a unit switch."""
    common.st.session_state = FakeSessionState(
        selected_unit=("orks", "warbikers"),
        selected_model_group="warbiker",
        group_targets={"warbiker": [("necrons", "warriors")]},
        group_decl={"warbiker": [{"weapon_name": "Dakkagun"}]},
    )
    # Stale widget state from a previous declaration
    common.st.session_state["decl_m_warbiker_warbikers_warriors_Dakkagun"] = 3
    common.st.session_state["decl_a_boss_nob_boyz_overlord_Power klaw"] = 4
    common.st.session_state["decl_p_warbiker_warbikers_warriors_Dakkagun"] = "Profile 1"
    common.st.session_state["group_autosel_done_warbikers"] = True
    common.st.session_state["unrelated_key"] = 99

    reset_group_declaration_state()

    s = common.st.session_state
    assert s.selected_model_group is None
    assert s.group_targets == {}
    assert s.group_decl == {}
    assert "decl_m_warbiker_warbikers_warriors_Dakkagun" not in s
    assert "decl_a_boss_nob_boyz_overlord_Power klaw" not in s
    assert "decl_p_warbiker_warbikers_warriors_Dakkagun" not in s
    assert "group_autosel_done_warbikers" not in s
    assert s["unrelated_key"] == 99


def test_all_done_clears_group_autosel_guard() -> None:
    """Bug 2 regression: finishing an attack resolution ("All done — Continue" /
    "Reset Declaration") must clear ``group_autosel_done_<uid>`` so that re-selecting
    the SAME unit in the SAME phase re-triggers auto-select.

    Before the fix, only ``attack_declaration`` was reset while the guard flag stayed
    set → auto-select skipped → ``selected_model_group`` stayed None → the enemy-target
    button (``group_target_selectable``) remained disabled. Both completion buttons now
    also call ``reset_group_declaration_state()``.
    """
    common.st.session_state = FakeSessionState(
        selected_unit=("necrons", "warriors"),
        selected_model_group=None,
        group_targets={},
        group_decl={},
    )
    common.st.session_state["group_autosel_done_warriors"] = True

    # Both completion buttons run this after resetting attack_declaration.
    reset_group_declaration_state()

    # Guard cleared → next render's auto-select branch (sel_gid is None and not flag)
    # will fire again, so the unit becomes targetable once more.
    assert "group_autosel_done_warriors" not in common.st.session_state


# ---------------------------------------------------------------------------
# _group_effective_attacks — per-group attacks with damage bracket (G2 follow-up)
# ---------------------------------------------------------------------------


def _silent_king_groups():  # type: ignore[no-untyped-def]
    import dataclasses

    from gameObjects.loader import _resolve_model_groups, load_army, load_weapon_catalog

    units, _ = load_army("necrons")
    sk = next(u for u in units if u.id.endswith("the_silent_king"))
    groups = _resolve_model_groups(sk.model_group_specs, 3, {}, load_weapon_catalog("necrons"))
    return dataclasses.replace(sk, model_groups=groups), groups


def _gw_state(menhir_w: int, szarekh_w: int) -> dict:
    return {
        "group_wounds": {"triarchal_menhirs": menhir_w, "szarekh": szarekh_w},
        "group_models": {
            "triarchal_menhirs": 2 if menhir_w > 0 else 0,
            "szarekh": 1 if szarekh_w > 0 else 0,
        },
    }


def test_group_attacks_szarekh_follows_own_bracket() -> None:
    sk, groups = _silent_king_groups()
    szarekh = next(g for g in groups if g.id == "szarekh")
    assert common._group_effective_attacks(sk, szarekh, _gw_state(14, 16)) == 6
    assert common._group_effective_attacks(sk, szarekh, _gw_state(0, 6)) == 4
    assert common._group_effective_attacks(sk, szarekh, _gw_state(0, 3)) == 2


def test_group_attacks_menhirs_fixed_override() -> None:
    sk, groups = _silent_king_groups()
    menhirs = next(g for g in groups if g.id == "triarchal_menhirs")
    # Explicit A2 — never bracketed regardless of wounds
    assert common._group_effective_attacks(sk, menhirs, _gw_state(14, 16)) == 2
    assert common._group_effective_attacks(sk, menhirs, _gw_state(7, 16)) == 2


def test_group_attacks_homogeneous_unit_falls_back_to_unit_attacks() -> None:
    from gameObjects.loader import _resolve_model_groups, load_army, load_weapon_catalog

    units, _ = load_army("orks")
    boyz = next(u for u in units if u.id.endswith("unit.boyz"))
    groups = _resolve_model_groups(boyz.model_group_specs, 10, {}, load_weapon_catalog("orks"))
    ork_boy = next(g for g in groups if g.id == "ork_boy")
    assert common._group_effective_attacks(boyz, ork_boy, {"group_models": {}}) == boyz.attacks


# ---------------------------------------------------------------------------
# front_group_hp — health bar for mixed per-group wounds (Silent King crash fix)
# ---------------------------------------------------------------------------


def test_front_group_hp_menhirs_then_szarekh() -> None:
    sk, _ = _silent_king_groups()
    # Full: front model is a Triarchal Menhir (priority 1)
    assert common.front_group_hp(
        sk, {"group_wounds": {"triarchal_menhirs": 14, "szarekh": 16}}
    ) == (
        7,
        7,
    )
    # Partly wounded menhir
    assert common.front_group_hp(sk, {"group_wounds": {"triarchal_menhirs": 9, "szarekh": 16}}) == (
        2,
        7,
    )
    # Menhirs dead → Szarekh becomes the front model
    assert common.front_group_hp(sk, {"group_wounds": {"triarchal_menhirs": 0, "szarekh": 10}}) == (
        10,
        16,
    )


def test_front_group_hp_progress_value_always_in_range() -> None:
    sk, _ = _silent_king_groups()
    for menhir_w in range(0, 15):
        for szarekh_w in range(0, 17):
            fw, fm = common.front_group_hp(
                sk, {"group_wounds": {"triarchal_menhirs": menhir_w, "szarekh": szarekh_w}}
            )
            bar = fw / fm if fm > 0 else 0
            assert 0.0 <= bar <= 1.0, (menhir_w, szarekh_w, fw, fm)


def test_front_group_hp_all_dead_returns_safe_default() -> None:
    sk, _ = _silent_king_groups()
    assert common.front_group_hp(sk, {"group_wounds": {"triarchal_menhirs": 0, "szarekh": 0}}) == (
        0,
        1,
    )


# ---------------------------------------------------------------------------
# Plan 014 Teil B — Defender loss allocation: A→B→C state transition
# These tests exercise apply_damage / select_damage_target_group / get_locked_group
# from gameMechanic.unitMutations using the same Nobz fixture pattern as
# tests/gameMechanic/test_unit_mutations.py (see _nobz_*  helpers there).
# ---------------------------------------------------------------------------

import gameMechanic.gameState as _gf_gs  # noqa: E402
import gameMechanic.unitMutations as _gf_mut  # noqa: E402
from gameMechanic.unitMutations import (  # noqa: E402
    apply_damage,
    get_locked_group,
    select_damage_target_group,
)
from gameObjects.unit import ModelGroup, Unit  # noqa: E402

_NOBZ_ID = "wh40k_9e.orks.unit.nobz"


def _gf_nobz_unit() -> Unit:
    """Nobz unit: 2 groups (Kill Saw + Slugga), 3 wounds per model, no stat overrides."""
    return Unit(
        id=_NOBZ_ID,
        name_en="Nobz",
        name_de="Nobz",
        faction="Orks",
        subfaction=None,
        battlefield_role=["Elites"],
        keywords=["ORK", "CORE"],
        wounds=3,
        models_min=4,
        models_max=4,
        power_level=6,
        move='5"',
        bs="5+",
        ws="3+",
        strength=5,
        toughness=4,
        attacks=3,
        save=4,
        invuln_save=None,
        leadership=7,
        oc=1,
        fnp=None,
        weapons=[],
        model_groups=[
            ModelGroup(id="nob_killsaw", name_en="Nob – Kill Saw", count=2, weapons=[], priority=1),
            ModelGroup(id="nob_slugga", name_en="Nob – Slugga", count=2, weapons=[], priority=2),
        ],
    )


def _gf_nobz_state(group_wounds: dict, active: str | None = None) -> dict:
    """Build a Nobz unit-state from per-group HP pools (3 LP per model, ceil division)."""
    group_models = {gid: -(-pool // 3) for gid, pool in group_wounds.items()}
    return {
        "current_wounds": sum(group_wounds.values()),
        "models": sum(group_models.values()),
        "destroyed": False,
        "in_melee": False,
        "lost_models_this_turn": 0,
        "melee_with": [],
        "group_models": group_models,
        "group_wounds": dict(group_wounds),
        "damage_active_group_id": active,
    }


class _GfSession(dict):
    def __getattr__(self, key: str):
        try:
            return self[key]
        except KeyError:
            raise AttributeError(key)

    def __setattr__(self, key: str, value: object) -> None:
        self[key] = value


def _gf_make_session(state: dict) -> _GfSession:
    """Wire session_state on both modules (mirrors _make_session in test_unit_mutations)."""
    s = _GfSession(first_player="Orks", second_player="Necrons", p1_units={_NOBZ_ID: state})
    _gf_mut.st.session_state = s
    _gf_gs.st.session_state = s
    return s


def test_zustand_a_b_c_transition_nobz() -> None:
    """A→B→C: free choice → wounded-model lock → lock released after model dies.

    Setup: 2 groups (Kill Saw × 2, Slugga × 2), 3 LP each model.
    Damage sequence chosen so pool % 3 != 0 after step 1 (→ Zustand B).
    """
    # Zustand A: all pools are integer multiples of 3 → no wounded model → no lock.
    # Kill Saw: 2 models × 3 LP = 6 HP. Slugga: 2 models × 3 LP = 6 HP.
    state = _gf_nobz_state({"nob_killsaw": 6, "nob_slugga": 6})
    _gf_make_session(state)
    unit = _gf_nobz_unit()

    assert get_locked_group(_NOBZ_ID, "Orks", unit) is None  # Zustand A

    # Defender picks Kill Saw group as target, then apply 1 damage (front model gets 1 wound).
    # After: pool = 5, 5 % 3 = 2 ≠ 0 → front Nob is wounded-but-alive → Zustand B.
    select_damage_target_group(_NOBZ_ID, "Orks", "nob_killsaw")
    apply_damage(_NOBZ_ID, "Orks", 1, unit, mortal=False)
    assert state["group_wounds"]["nob_killsaw"] == 5
    assert get_locked_group(_NOBZ_ID, "Orks", unit) == "nob_killsaw"  # Zustand B

    # In Zustand B: directing damage to the OTHER group must raise ValueError.
    state["damage_active_group_id"] = "nob_slugga"
    import pytest as _pytest

    with _pytest.raises(ValueError):
        apply_damage(_NOBZ_ID, "Orks", 1, unit, mortal=False)

    # Drain the remaining 2 HP from the wounded Kill Saw model → pool = 3, 3 % 3 = 0
    # → that model is dead, next model is intact → get_locked_group returns None (Zustand C / A).
    state["damage_active_group_id"] = "nob_killsaw"
    apply_damage(_NOBZ_ID, "Orks", 2, unit, mortal=False)
    assert state["group_wounds"]["nob_killsaw"] == 3
    assert get_locked_group(_NOBZ_ID, "Orks", unit) is None  # back to free choice


def test_regressionstest_nobz_killsaw_group_destroyed() -> None:
    """Kill Saw group (2 models × 3 LP = 6 HP) reduced to 0; Slugga group stays untouched.

    Verifies that group_models[nob_killsaw] reaches 0 and the sibling group is unaffected.
    """
    state = _gf_nobz_state({"nob_killsaw": 6, "nob_slugga": 6}, active="nob_killsaw")
    _gf_make_session(state)
    unit = _gf_nobz_unit()

    # Confirm the group name carries "Kill Saw" (spec check).
    ks_group = next(g for g in unit.model_groups if g.id == "nob_killsaw")
    assert "Kill Saw" in ks_group.name_en

    # Apply 6 damage (resolved=True bypasses per-model front cap) → entire Kill Saw pool gone.
    apply_damage(_NOBZ_ID, "Orks", 6, unit, mortal=False, resolved=True)

    assert state["group_wounds"]["nob_killsaw"] == 0
    assert state["group_models"]["nob_killsaw"] == 0  # all Kill Saw models destroyed
    assert state["group_wounds"]["nob_slugga"] == 6  # Slugga group untouched
    assert state["group_models"]["nob_slugga"] == 2  # both Sluggas alive
