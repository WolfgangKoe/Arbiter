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


def _group(gid: str, count: int) -> SimpleNamespace:
    return SimpleNamespace(id=gid, count=count)


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
    """Group flow active but no group picked yet — ▷ stays disabled."""
    _setup(
        monkeypatch,
        groups=[_group("ork_boy", 9)],
        group_models={"ork_boy": 9},
        selected_group=None,
    )
    assert group_target_selectable("necrons", "warriors") is False


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
