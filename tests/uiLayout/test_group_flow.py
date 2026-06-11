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
