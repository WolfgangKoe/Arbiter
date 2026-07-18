"""Tests for fightPhase.py — Ziel 3c: can_fight() + integration smoke tests."""

from __future__ import annotations

import sys
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import MagicMock

sys.modules.setdefault("streamlit", MagicMock())
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

import gameMechanic.abilityEngine as _eng  # noqa: E402
import gameMechanic.fightPhase as fp  # noqa: E402
import gameMechanic.gameState as _gs  # noqa: E402
import uiLayout._common as common  # noqa: E402
from gameMechanic.combat import AttackParams, DefendParams, resolve_attack  # noqa: E402
from gameMechanic.fightPhase import _dice_max, _is_target_engaged, can_fight  # noqa: E402
from gameObjects.loader import load_roster, load_unit_catalog  # noqa: E402


class FakeSessionState(dict):
    """Dict with attribute access — mirrors streamlit's session_state API."""

    def __getattr__(self, name):  # type: ignore[no-untyped-def]
        try:
            return self[name]
        except KeyError as exc:
            raise AttributeError(name) from exc

    def __setattr__(self, name, value):  # type: ignore[no-untyped-def]
        self[name] = value


# ---------------------------------------------------------------------------
# can_fight — pure-function tests
# ---------------------------------------------------------------------------


class TestCanFight:
    def _state(self, in_melee: bool = False, **flags) -> dict:
        return {"turn_flags": flags, "in_melee": in_melee}

    def test_default_unit_cannot_fight(self):
        assert can_fight(self._state()) is False

    def test_in_melee_can_fight(self):
        assert can_fight(self._state(in_melee=True)) is True

    def test_charged_can_fight(self):
        assert can_fight(self._state(charged=True)) is True

    def test_in_melee_and_charged(self):
        assert can_fight(self._state(in_melee=True, charged=True)) is True

    def test_advanced_not_in_melee_cannot_fight(self):
        assert can_fight(self._state(advanced=True)) is False

    def test_retreated_not_in_melee_cannot_fight(self):
        assert can_fight(self._state(retreated=True)) is False

    def test_empty_state_cannot_fight(self):
        assert can_fight({"turn_flags": {}}) is False

    def test_in_reserve_cannot_fight(self):
        assert can_fight({"turn_flags": {}, "in_melee": False, "in_reserve": True}) is False

    def test_stationary_not_in_melee_cannot_fight(self):
        assert can_fight(self._state(advanced=False, retreated=False)) is False

    def test_charged_takes_priority_over_advanced(self):
        # Charged units are always eligible regardless of other flags.
        assert can_fight(self._state(charged=True, advanced=True)) is True


# ---------------------------------------------------------------------------
# _is_target_engaged — pure-function tests
# ---------------------------------------------------------------------------


class TestIsTargetEngaged:
    def _state(self, melee_with: list) -> dict:
        return {"melee_with": melee_with}

    def test_engaged_enemy_returns_true(self):
        state = self._state([["Orks", "wh40k_9e.orks.unit.boyz"]])
        assert _is_target_engaged(state, "Orks", "wh40k_9e.orks.unit.boyz") is True

    def test_non_engaged_enemy_returns_false(self):
        state = self._state([["Orks", "wh40k_9e.orks.unit.boyz"]])
        assert _is_target_engaged(state, "Orks", "wh40k_9e.orks.unit.gretchin") is False

    def test_wrong_faction_returns_false(self):
        state = self._state([["Orks", "wh40k_9e.orks.unit.boyz"]])
        assert _is_target_engaged(state, "Necrons", "wh40k_9e.orks.unit.boyz") is False

    def test_empty_melee_with_returns_false(self):
        assert _is_target_engaged({"melee_with": []}, "Orks", "wh40k_9e.orks.unit.boyz") is False

    def test_missing_melee_with_returns_false(self):
        assert _is_target_engaged({}, "Orks", "wh40k_9e.orks.unit.boyz") is False

    def test_multiple_engaged_enemies_correct_one_found(self):
        state = self._state(
            [
                ["Orks", "wh40k_9e.orks.unit.boyz"],
                ["Orks", "wh40k_9e.orks.unit.gretchin"],
            ]
        )
        assert _is_target_engaged(state, "Orks", "wh40k_9e.orks.unit.gretchin") is True

    def test_multiple_engaged_enemies_non_member_not_found(self):
        state = self._state(
            [
                ["Orks", "wh40k_9e.orks.unit.boyz"],
                ["Orks", "wh40k_9e.orks.unit.gretchin"],
            ]
        )
        assert _is_target_engaged(state, "Orks", "wh40k_9e.orks.unit.warboss") is False


# ---------------------------------------------------------------------------
# Integration smoke tests — resolve_attack with typical melee profiles
# ---------------------------------------------------------------------------


class TestFightSmoke:
    def test_hyperphase_sword_1hit_1wound_1failed_save(self):
        """Overlord Hyperphase Sword: S6, AP-3, D2 vs T4 Sv4+."""
        params = AttackParams(attacks=4, skill=2, strength=6, ap=-3, damage=2)
        defender = DefendParams(toughness=4, save=4, wounds=2)
        damage, log = resolve_attack(
            params, defender, hits_rolled=2, wounds_rolled=1, saves_failed=1
        )
        assert damage == 2

    def test_mwbd_hit_modifier_applied(self):
        params = AttackParams(attacks=4, skill=2, strength=6, ap=-3, damage=2, mwbd_active=True)
        defender = DefendParams(toughness=4, save=4, wounds=2)
        damage, log = resolve_attack(
            params, defender, hits_rolled=3, wounds_rolled=2, saves_failed=2
        )
        assert damage == 4
        assert any("MWBD" in line for line in log)

    def test_invuln_better_than_armour(self):
        """AP-3 vs 5++ invuln: armour 3+3=6+ → invuln 5+ applies."""
        params = AttackParams(attacks=4, skill=2, strength=6, ap=-3, damage=2)
        defender = DefendParams(toughness=4, save=3, wounds=2, invul_save=5)
        damage, log = resolve_attack(
            params, defender, hits_rolled=2, wounds_rolled=2, saves_failed=1
        )
        assert any("Invuln" in line for line in log)

    def test_no_melee_wounds_no_damage(self):
        params = AttackParams(attacks=3, skill=3, strength=4, ap=-1, damage=1)
        defender = DefendParams(toughness=4, save=3, wounds=1)
        damage, log = resolve_attack(params, defender, hits_rolled=2, wounds_rolled=0)
        assert damage == 0

    def test_fnp_reduces_melee_damage(self):
        """3 failed saves, 2 FNP saved → 1 wound through."""
        params = AttackParams(attacks=5, skill=3, strength=5, ap=-1, damage=1)
        defender = DefendParams(toughness=4, save=4, wounds=1, fnp=5)
        damage, log = resolve_attack(
            params, defender, hits_rolled=4, wounds_rolled=3, saves_failed=3, fnp_saved=2
        )
        assert damage == 1


# ---------------------------------------------------------------------------
# _dice_max — pure parser
# ---------------------------------------------------------------------------


class TestDiceMax:
    def test_d3_returns_3(self) -> None:
        assert _dice_max("D3") == 3

    def test_d6_returns_6(self) -> None:
        assert _dice_max("D6") == 6

    def test_lowercase_d6(self) -> None:
        assert _dice_max("d6") == 6

    def test_plain_integer_string(self) -> None:
        assert _dice_max("6") == 6

    def test_invalid_string_returns_3(self) -> None:
        assert _dice_max("invalid") == 3

    def test_empty_string_returns_3(self) -> None:
        assert _dice_max("") == 3


# ---------------------------------------------------------------------------
# _render_melee_pairs — duplicate-squad state-key resolution (Plan 034)
# ---------------------------------------------------------------------------


class TestRenderMeleePairsDuplicateSquad:
    def test_melee_pairs_show_names_for_duplicate_squads(self, monkeypatch) -> None:
        """A melee_with entry keyed by a duplicate-squad state key ('u1#1')
        must resolve to the unit's real name, not fall back to showing the
        raw internal state key. name_map is bare-ID-keyed, so the lookup must
        strip the '#N' suffix before indexing (regression)."""
        warriors = SimpleNamespace(id="u1", name_en="Necron Warriors")
        boyz = SimpleNamespace(id="u2", name_en="Boyz")
        monkeypatch.setattr(
            fp,
            "units_list_for",
            lambda player: [warriors] if player == "Necrons" else [boyz],
        )
        monkeypatch.setattr(
            fp,
            "units_key_for",
            lambda player: "p1_units" if player == "Necrons" else "p2_units",
        )
        fp.st.session_state = FakeSessionState(
            first_player="Necrons",
            second_player="Orks",
            p1_units={"u1#1": {"melee_with": [["Orks", "u2"]]}},
        )
        markdown_calls: list[str] = []
        fp.st.markdown = lambda msg: markdown_calls.append(msg)

        fp._render_melee_pairs()

        assert any("Necron Warriors" in c and "Boyz" in c for c in markdown_calls)
        assert not any("#1" in c for c in markdown_calls)


# ---------------------------------------------------------------------------
# B-028c1 S165 — mortal_wounds-on-destroy card reachability through the real
# phase entry point (FightPhaseHandler.render_active), not just the isolated
# card function. Diagnosed in S165 Task 1a: fightPhase.py's group-flow early
# return (the non-fighting column renders render_group_assignment(...) and
# returns) used to bypass the card's old per-column call site entirely before
# it was ever reached. The fix moves the card scan
# (render_mortal_wounds_cards_for_destroyed) to render_active, before any
# column/selection branching, so it fires regardless of what is selected.
# ---------------------------------------------------------------------------

SILENT_KING = "wh40k_9e.necrons.unit.the_silent_king"


def _silent_king_with_resolved_groups():  # type: ignore[no-untyped-def]
    """Load Silent King via load_roster() (not load_unit_catalog() alone) — only
    load_roster() resolves model_group_specs into the runtime model_groups field
    (loader.py:1232-1237). A catalog-only Unit has model_groups == [], which
    would make group_flow_attacker() always return None — a test artifact that
    would silently hide this regression rather than reproduce it (S165 Task 1a
    testing pitfall)."""
    repo_root = Path(__file__).parent.parent.parent
    catalog = load_unit_catalog("necrons")
    matched, unmatched = load_roster(
        repo_root / "data/rosters/necrons_1500pts_silent_king.yaml", catalog
    )
    assert not unmatched, unmatched
    return next(u for u, _n in matched if u.id == SILENT_KING)


class TestMortalWoundsCardReachableThroughGroupFlowEarlyReturn:
    def test_render_active_shows_card_despite_group_flow_early_return(self, monkeypatch) -> None:
        """Diagnosis Scenario B, reproduced end-to-end: the active fight side has
        a still fight-eligible model_groups attacker (Silent King) selected; the
        opposing side has its OWN destroyed Silent King (a mirror-match instance,
        the only unit in this data set with a `model_destroyed`-triggered
        mortal_wounds ability) sitting in selected_targets. Before the fix, the
        opposing column's group-flow branch returned before ever reaching the
        card check — the card never appeared. It must now appear regardless,
        because the scan runs once in render_active before either column."""
        silent_king = _silent_king_with_resolved_groups()
        assert silent_king.model_groups, "fixture must resolve model_groups via load_roster()"

        session = FakeSessionState(
            first_player="Necrons",
            second_player="NecronsMirror",
            active="Necrons",
            fight_current_player="Necrons",
            selected_unit=("Necrons", SILENT_KING),
            selected_targets=[("NecronsMirror", SILENT_KING)],
            selected_model_group=None,
            group_targets={},
            pending_transport_destroyed=None,
            pending_mortal_undo=None,
            pending_triggered_relic=None,
            attack_declaration={},
            phase_idx=6,  # fight
            round=3,
            used_ability_ids={},
            ability_use_anchors={},
            pending_mortal_wounds_ability=None,
            p1_faction_dir="necrons",
            p2_faction_dir="necrons",
            p1_units_list=[silent_king],
            p1_unit_keys=[SILENT_KING],
            p2_units_list=[silent_king],
            p2_unit_keys=[SILENT_KING],
            p1_units={
                SILENT_KING: {
                    "destroyed": False,
                    "in_reserve": False,
                    "in_melee": True,
                    "turn_flags": {"charged": True, "fought": False},
                }
            },
            p2_units={SILENT_KING: {"destroyed": True, "in_reserve": False, "turn_flags": {}}},
        )
        fp.st.session_state = session
        common.st.session_state = session
        _gs.st.session_state = session
        _eng.st.session_state = session

        captured: list[dict] = []  # type: ignore[type-arg]
        monkeypatch.setattr(common, "render_go_card", lambda **kwargs: captured.append(kwargs))
        # Short-circuit the heavyweight group-declaration UI on both sides — it
        # is not the subject under test (covered elsewhere) and would otherwise
        # require simulating full widget interaction with a mocked streamlit.
        monkeypatch.setattr(fp, "render_group_cards", lambda *a, **k: None)
        monkeypatch.setattr(fp, "render_group_assignment", lambda *a, **k: None)
        monkeypatch.setattr(fp.st, "columns", lambda n: tuple(MagicMock() for _ in range(n)))
        # A prior test in this module (TestRenderMeleePairsDuplicateSquad) leaves
        # a strict lambda on the shared fp.st mock's `markdown` attribute that
        # rejects kwargs — reset it here to a permissive no-op for this test.
        monkeypatch.setattr(fp.st, "markdown", lambda *a, **kw: None)

        fp.FightPhaseHandler().render_active(
            {"first_player": "Necrons", "second_player": "NecronsMirror", "round": 3}
        )

        assert any(k.get("name") == "Vengeance of the Enchained" for k in captured)
