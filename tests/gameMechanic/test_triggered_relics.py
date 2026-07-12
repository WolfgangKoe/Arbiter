"""Tests for 6l Phase 2 — triggered relic effects (data-driven via TriggeredEffect)."""

from __future__ import annotations

import sys
from pathlib import Path
from unittest.mock import MagicMock

_st_mock = MagicMock()
sys.modules["streamlit"] = _st_mock
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

import gameMechanic.gameState as _gs  # noqa: E402
from gameObjects.loader import load_unit_catalog  # noqa: E402
from gameObjects.unit import TriggeredEffect  # noqa: E402

# ---------------------------------------------------------------------------
# Load test units with relics applied
# ---------------------------------------------------------------------------

_MORGOG_ID = "wh40k_9e.orks.relic.morgogs_finkin_cap"
_IRONGOB_ID = "wh40k_9e.orks.relic.da_irongob"
_VEIL_ID = "wh40k_9e.necrons.relic.schleier_der_finsternis"


def _unit_with_relic(faction_dir: str, unit_id: str, relic_id: str):  # type: ignore[return]
    """Load a unit from the catalog and apply the given relic."""
    from gameObjects.loader import _apply_relic, load_relic_catalog

    catalog_units = load_unit_catalog(faction_dir)
    unit = catalog_units[unit_id]
    catalog = load_relic_catalog(faction_dir)
    return _apply_relic(unit, relic_id, catalog)


# ---------------------------------------------------------------------------
# TriggeredEffect dataclass — field access
# ---------------------------------------------------------------------------


class TestTriggeredEffectDataclass:
    def test_all_fields_accessible(self) -> None:
        te = TriggeredEffect(
            timing="phase_start",
            phase="command",
            effect="gain_cp_roll",
            once_per_battle=False,
            dice="D6",
            threshold=4,
            amount=1,
        )
        assert te.timing == "phase_start"
        assert te.phase == "command"
        assert te.effect == "gain_cp_roll"
        assert te.threshold == 4
        assert te.amount == 1
        assert te.mortal_dice is None

    def test_defaults(self) -> None:
        te = TriggeredEffect(timing="after_fight", phase="fight", effect="mortal_after_melee")
        assert te.once_per_battle is False
        assert te.dice is None
        assert te.threshold is None
        assert te.mortal_dice is None


# ---------------------------------------------------------------------------
# Unit.get_triggered_effect — correct dispatch
# ---------------------------------------------------------------------------


class TestUnitGetTriggeredEffect:
    def setup_method(self) -> None:
        self.warboss = _unit_with_relic("orks", "wh40k_9e.orks.unit.warboss", _MORGOG_ID)
        self.big_mek = _unit_with_relic("orks", "wh40k_9e.orks.unit.big_mek", _IRONGOB_ID)
        self.overlord = _unit_with_relic("necrons", "wh40k_9e.necrons.unit.overlord", _VEIL_ID)

    def test_morgog_cap_command_effect_found(self) -> None:
        te = self.warboss.get_triggered_effect("phase_start", "command", "gain_cp_roll")
        assert te is not None
        assert te.threshold == 4
        assert te.amount == 1

    def test_morgog_cap_wrong_phase_returns_none(self) -> None:
        assert self.warboss.get_triggered_effect("phase_start", "movement", "gain_cp_roll") is None

    def test_irongob_fight_effect_found(self) -> None:
        te = self.big_mek.get_triggered_effect("after_fight", "fight", "mortal_after_melee")
        assert te is not None
        assert te.threshold == 2
        assert te.mortal_dice == "D3"

    def test_irongob_wrong_timing_returns_none(self) -> None:
        assert (
            self.big_mek.get_triggered_effect("phase_start", "fight", "mortal_after_melee") is None
        )

    def test_veil_movement_effect_found(self) -> None:
        te = self.overlord.get_triggered_effect("phase_start", "movement", "teleport")
        assert te is not None
        assert te.once_per_battle is True

    def test_veil_relic_name_set(self) -> None:
        assert self.overlord.relic_name == "Veil of Darkness"

    def test_unit_without_relic_returns_none(self) -> None:
        catalog = load_unit_catalog("orks")
        plain = catalog["wh40k_9e.orks.unit.warboss"]
        assert plain.get_triggered_effect("phase_start", "command", "gain_cp_roll") is None


# ---------------------------------------------------------------------------
# gameState — phase reset clears relic state
# ---------------------------------------------------------------------------


class _S(dict):
    def __getattr__(self, key: str):  # type: ignore[override]
        try:
            return self[key]
        except KeyError:
            raise AttributeError(key)

    def __setattr__(self, key: str, value: object) -> None:
        self[key] = value


def _make_session(extra: dict | None = None) -> _S:
    s = _S(
        phase_idx=1,
        round=1,
        active_modifiers=[],
        morgog_cap_rolled_this_phase=True,
        pending_triggered_relic={"uid": "some.unit", "faction": "Orks"},
        used_stratagem_ids={},
        fight_current_player=None,
        attack_declaration={"active": False, "entries": []},
        charge_phase_step=1,
        pending_hi=None,
        hi_targets=[],
    )
    if extra:
        s.update(extra)
    return s


def test_reset_phase_clears_morgog_flag() -> None:
    session = _make_session()
    _st_mock.session_state = session
    _gs.st.session_state = session
    _gs._reset_phase_state()
    assert session.morgog_cap_rolled_this_phase is False


def test_reset_phase_clears_pending_triggered_relic() -> None:
    session = _make_session()
    _st_mock.session_state = session
    _gs.st.session_state = session
    _gs._reset_phase_state()
    assert session.pending_triggered_relic is None


def test_relic_triggered_used_persists_across_phase_reset() -> None:
    """relic_triggered_used (once-per-battle) must NOT be cleared by phase reset."""
    session = _make_session({"relic_triggered_used": {_VEIL_ID: True}})
    _st_mock.session_state = session
    _gs.st.session_state = session
    _gs._reset_phase_state()
    assert session.get("relic_triggered_used", {}).get(_VEIL_ID) is True
