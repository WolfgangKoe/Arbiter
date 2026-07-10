"""Tests for uiLayout/gameProtocoll.py — Battle Log deployment snapshot + the
central Stratagems-list GO-card migration (design_system.md §6, S132 1b).

Regression target (Battle Log): the deployment snapshot iterated the bare-ID-keyed
name map instead of the (possibly '#N'-suffixed) state dict, so duplicate squads
never appeared. See Plan 034.
"""

import json
import sys
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import MagicMock

sys.modules.setdefault("streamlit", MagicMock())
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

import gameMechanic.game_log as gl  # noqa: E402
import gameMechanic.game_state as gs  # noqa: E402
import uiLayout.gameProtocoll as gp  # noqa: E402
from gameObjects.ability import Effect  # noqa: E402
from gameObjects.stratagem import Stratagem  # noqa: E402


class FakeSessionState(dict):
    """Dict with attribute access — mirrors streamlit's session_state API."""

    def __getattr__(self, name):  # type: ignore[no-untyped-def]
        try:
            return self[name]
        except KeyError as exc:
            raise AttributeError(name) from exc

    def __setattr__(self, name, value):  # type: ignore[no-untyped-def]
        self[name] = value


def test_deployment_snapshot_lists_duplicate_squads(monkeypatch) -> None:
    """Two Necron Warriors squads (state keys 'u1' and 'u1#1') must BOTH
    appear in the Deployment Snapshot with their real name — not just the
    first, bare-ID copy (regression: the snapshot used to iterate the
    collapsed name map, so the second copy was silently dropped)."""
    warriors = SimpleNamespace(id="u1", name_en="Necron Warriors")
    session = FakeSessionState(
        first_player="Necrons",
        second_player="Orks",
        round=1,
        phase_idx=0,
        p1_units_list=[warriors],
        p1_units={
            "u1": {"deployment": "Deployed", "destroyed": False},
            "u1#1": {"deployment": "Reserve", "destroyed": False},
        },
        p2_units_list=[],
        p2_units={},
    )
    monkeypatch.setattr(gp, "st", MagicMock(session_state=session))
    monkeypatch.setattr(gs, "st", MagicMock(session_state=session))
    monkeypatch.setattr(gp, "_load_game_log", lambda: [])

    captured: list[str] = []
    gp.st.caption.side_effect = lambda msg: captured.append(msg)

    gp._render_battle_log()

    warrior_lines = [c for c in captured if "Necron Warriors" in c]
    assert len(warrior_lines) == 2
    assert any("Deployed" in line for line in warrior_lines)
    assert any("Reserve" in line for line in warrior_lines)


def test_reset_game_clears_battle_log_for_next_render(monkeypatch, tmp_path: Path) -> None:
    """Plan 018 Task 18.2 regression: after the Reset button (game_state.reset_game)
    the Battle Log tab must show no entries from the previous game.

    game_log.py defines its log path as a CWD-relative string (`_LOG_FILE`) while
    gameProtocoll.py defines it independently as a repo-root-anchored `Path`
    (`_LOG_PATH`) — two definitions of "the same" file. This test drives the real
    reset_game() -> archive_and_reset_log() call and reads the log back through
    gameProtocoll._load_game_log(), the function the Battle Log tab actually
    renders from, so a future drift between the two path definitions (or a
    reintroduced module-level buffer in game_log.py) would fail here even though
    each module's own unit tests stay green in isolation.
    """
    log_file = tmp_path / "game_log.json"
    archive_dir = tmp_path / "archive"
    monkeypatch.setattr(gl, "_LOG_FILE", str(log_file))
    monkeypatch.setattr(gl, "_ARCHIVE_DIR", str(archive_dir))
    monkeypatch.setattr(gp, "_LOG_PATH", log_file)

    gl.log_action(1, "shooting", "Overlord", "fired at Boyz")
    assert gp._load_game_log() == [
        {"round": 1, "phase": "shooting", "unit": "Overlord", "action": "fired at Boyz"}
    ]

    session = FakeSessionState(round=3, phase_idx=4, selected_unit="u1")
    monkeypatch.setattr(gs, "st", MagicMock(session_state=session))

    gs.reset_game()

    assert gp._load_game_log() == []
    archived = list(archive_dir.glob("*.json"))
    assert len(archived) == 1
    archived_data = json.loads(archived[0].read_text())
    assert archived_data["rounds"][0]["phases"][0]["events"][0]["action"] == "fired at Boyz"


# ---------------------------------------------------------------------------
# _go_state_and_reason() — pure vis -> GO-card-state mapping (no Streamlit)
# ---------------------------------------------------------------------------


def _make_stratagem(
    id_: str = "s1",
    name_en: str = "Test Strat",
    cp_cost: int = 1,
    once_per_battle: bool = False,
) -> Stratagem:
    return Stratagem(
        id=id_,
        name_en=name_en,
        cp_cost=cp_cost,
        phase="any",
        stage="active",
        player="both",
        once_per_battle=once_per_battle,
    )


def test_go_state_and_reason_clickable_maps_to_ready() -> None:
    strat = _make_stratagem()
    assert gp._go_state_and_reason(strat, "clickable", set(), set()) == ("ready", None)


def test_go_state_and_reason_greyed_with_open_undo_window_maps_to_used() -> None:
    """A stratagem used THIS phase (still discard-able) becomes "used", not
    "locked" — the Undo button must stay offered."""
    strat = _make_stratagem(id_="s1")
    assert gp._go_state_and_reason(strat, "greyed", {"s1"}, set()) == ("used", None)


def test_go_state_and_reason_once_per_battle_spent_earlier_maps_to_locked_used() -> None:
    """A once_per_battle stratagem spent in a previous phase: the phase-scoped
    undo window is closed (id not in used_ids), so it must render "locked"
    with reason "used" — not "used" (no Undo) and not the generic CP reason."""
    strat = _make_stratagem(id_="s1", once_per_battle=True)
    assert gp._go_state_and_reason(strat, "greyed", set(), {"s1"}) == ("locked", "used")


def test_go_state_and_reason_cp_insufficient_maps_to_locked_with_cp_reason() -> None:
    strat = _make_stratagem(id_="s1")
    assert gp._go_state_and_reason(strat, "greyed", set(), set()) == (
        "locked",
        "CP insufficient",
    )


# ---------------------------------------------------------------------------
# _effect_gate_met() — S133-D Befund 4: per-unit-state gate for GOs whose
# effect requires "not yet moved this phase" + "in Engagement Range"
# (rules_appendix.txt 2618-2625, Desperate Breakout). Pure, no Streamlit.
# ---------------------------------------------------------------------------


def _make_fall_back_stratagem() -> Stratagem:
    return _make_stratagem(id_="desperate_breakout", name_en="Desperate Breakout", cp_cost=2)


def _with_fall_back_effect(strat: Stratagem) -> Stratagem:
    from dataclasses import replace

    return replace(strat, effect=Effect(type="move", handler="fall_back_through_models"))


def test_effect_gate_met_true_when_stratagem_has_no_effect() -> None:
    strat = _make_stratagem()
    assert gp._effect_gate_met(strat, None) == (True, None)


def test_effect_gate_met_true_for_unrelated_effect_shape() -> None:
    from dataclasses import replace

    strat = replace(_make_stratagem(), effect=Effect(type="auto_pass_morale"))
    assert gp._effect_gate_met(strat, {"movement_chosen": True, "in_melee": False}) == (
        True,
        None,
    )


def test_effect_gate_met_false_when_no_unit_selected() -> None:
    strat = _with_fall_back_effect(_make_fall_back_stratagem())
    assert gp._effect_gate_met(strat, None) == (False, "select an eligible unit")


def test_effect_gate_met_false_when_unit_already_moved_this_phase() -> None:
    strat = _with_fall_back_effect(_make_fall_back_stratagem())
    unit_state = {"movement_chosen": True, "in_melee": True}
    assert gp._effect_gate_met(strat, unit_state) == (False, "unit already moved this phase")


def test_effect_gate_met_false_when_unit_not_in_engagement_range() -> None:
    strat = _with_fall_back_effect(_make_fall_back_stratagem())
    unit_state = {"movement_chosen": False, "in_melee": False}
    assert gp._effect_gate_met(strat, unit_state) == (False, "unit not in Engagement Range")


def test_effect_gate_met_true_when_not_moved_and_in_engagement_range() -> None:
    strat = _with_fall_back_effect(_make_fall_back_stratagem())
    unit_state = {"movement_chosen": False, "in_melee": True}
    assert gp._effect_gate_met(strat, unit_state) == (True, None)


# ---------------------------------------------------------------------------
# _render_stratagem_column() — wiring: render_go_card gets the mapped state,
# Use/Undo route through the canonical spend_stratagem/undo_stratagem path
# ---------------------------------------------------------------------------


def test_render_stratagem_column_maps_visibility_to_go_card_state(monkeypatch) -> None:
    """Regression: the central list must hand render_go_card the MAPPED
    ready/used/locked GO state (via _go_state_and_reason), not the raw
    clickable/greyed string stratagem_visibility() returns."""
    ready_strat = _make_stratagem(id_="ready.strat", name_en="Ready GO", cp_cost=1)
    used_strat = _make_stratagem(id_="used.strat", name_en="Used GO", cp_cost=2)

    session = FakeSessionState(
        cp={"Necrons": 1},
        phase_idx=0,
        used_stratagem_ids={"Necrons": {"used.strat"}},
        used_stratagem_battle_ids={},
        selected_unit=None,
    )
    monkeypatch.setattr(gp, "st", MagicMock(session_state=session))
    monkeypatch.setattr(gp, "load_stratagems", lambda faction_dir: [ready_strat, used_strat])
    monkeypatch.setattr(gp, "faction_dir_for", lambda player: "necrons")

    captured: list[dict] = []
    monkeypatch.setattr(gp, "render_go_card", lambda **kwargs: captured.append(kwargs))

    gp._render_stratagem_column("Necrons", True)

    by_name = {c["name"]: c for c in captured}
    assert by_name["Ready GO"]["state"] == "ready"
    assert by_name["Ready GO"]["locked_reason"] is None
    assert by_name["Used GO"]["state"] == "used"
    assert by_name["Used GO"]["locked_reason"] is None


def test_render_stratagem_column_locks_gated_stratagem_for_ineligible_unit(monkeypatch) -> None:
    """S133-D Befund 4: a stratagem gated on unit state (not yet moved + in
    Engagement Range) must render "locked" with the gate reason when the
    selected unit fails the gate — even though CP/phase/conditions alone would
    otherwise make it "ready". Befund 3: the card must also show which unit
    it is bound to."""
    from dataclasses import replace

    strat = replace(
        _make_stratagem(id_="db", name_en="Desperate Breakout", cp_cost=2),
        effect=Effect(type="move", handler="fall_back_through_models"),
    )
    unit = SimpleNamespace(id="boyz", name_en="Boyz Mob")
    session = FakeSessionState(
        cp={"Orks": 2},
        phase_idx=0,
        used_stratagem_ids={},
        used_stratagem_battle_ids={},
        selected_unit=("Orks", "boyz"),
        p1_units={"boyz": {"movement_chosen": True, "in_melee": True}},
    )
    monkeypatch.setattr(gp, "st", MagicMock(session_state=session))
    monkeypatch.setattr(gp, "load_stratagems", lambda faction_dir: [strat])
    monkeypatch.setattr(gp, "faction_dir_for", lambda player: "orks")
    monkeypatch.setattr(gp, "units_list_for", lambda player: [unit])
    monkeypatch.setattr(gp, "units_key_for", lambda player: "p1_units")

    captured: list[dict] = []
    monkeypatch.setattr(gp, "render_go_card", lambda **kwargs: captured.append(kwargs))

    gp._render_stratagem_column("Orks", True)

    card = captured[0]
    assert card["state"] == "locked"
    assert card["locked_reason"] == "unit already moved this phase"
    assert card["target_name"] == "Boyz Mob"


def test_render_stratagem_column_ready_for_gated_stratagem_when_unit_eligible(
    monkeypatch,
) -> None:
    """Counterpart: the same gated stratagem is "ready" once the selected unit
    has not yet moved this phase and is in Engagement Range."""
    from dataclasses import replace

    strat = replace(
        _make_stratagem(id_="db", name_en="Desperate Breakout", cp_cost=2),
        effect=Effect(type="move", handler="fall_back_through_models"),
    )
    unit = SimpleNamespace(id="boyz", name_en="Boyz Mob")
    session = FakeSessionState(
        cp={"Orks": 2},
        phase_idx=0,
        used_stratagem_ids={},
        used_stratagem_battle_ids={},
        selected_unit=("Orks", "boyz"),
        p1_units={"boyz": {"movement_chosen": False, "in_melee": True}},
    )
    monkeypatch.setattr(gp, "st", MagicMock(session_state=session))
    monkeypatch.setattr(gp, "load_stratagems", lambda faction_dir: [strat])
    monkeypatch.setattr(gp, "faction_dir_for", lambda player: "orks")
    monkeypatch.setattr(gp, "units_list_for", lambda player: [unit])
    monkeypatch.setattr(gp, "units_key_for", lambda player: "p1_units")

    captured: list[dict] = []
    monkeypatch.setattr(gp, "render_go_card", lambda **kwargs: captured.append(kwargs))

    gp._render_stratagem_column("Orks", True)

    card = captured[0]
    assert card["state"] == "ready"
    assert card["locked_reason"] is None
    assert card["target_name"] == "Boyz Mob"


def test_render_stratagem_column_use_action_routes_through_spend_stratagem(
    monkeypatch,
) -> None:
    """The GO card's on_use callback must call the canonical spend_stratagem
    path with (stratagem, player, selected-unit state key) — the same
    bookkeeping the reactive box and inline offer use, so CP/usage tracking
    never drifts between the three GO surfaces."""
    strat = _make_stratagem(id_="ready.strat", name_en="Ready GO", cp_cost=1)
    session = FakeSessionState(
        cp={"Necrons": 1},
        phase_idx=0,
        used_stratagem_ids={},
        used_stratagem_battle_ids={},
        selected_unit=None,
    )
    monkeypatch.setattr(gp, "st", MagicMock(session_state=session))
    monkeypatch.setattr(gp, "load_stratagems", lambda faction_dir: [strat])
    monkeypatch.setattr(gp, "faction_dir_for", lambda player: "necrons")

    captured: list[dict] = []
    monkeypatch.setattr(gp, "render_go_card", lambda **kwargs: captured.append(kwargs))
    spend_calls: list[tuple] = []
    monkeypatch.setattr(gp, "spend_stratagem", lambda *args: spend_calls.append(args))

    gp._render_stratagem_column("Necrons", True)
    captured[0]["on_use"]()

    assert spend_calls == [(strat, "Necrons", None)]


def test_render_stratagem_column_undo_action_routes_through_undo_stratagem(
    monkeypatch,
) -> None:
    """The GO card's on_undo callback must call the canonical undo_stratagem
    counterpart with (stratagem, player) — full-rollback bookkeeping stays in
    one place instead of being re-inlined at the call site."""
    strat = _make_stratagem(id_="used.strat", name_en="Used GO", cp_cost=2)
    session = FakeSessionState(
        cp={"Necrons": 0},
        phase_idx=0,
        used_stratagem_ids={"Necrons": {"used.strat"}},
        used_stratagem_battle_ids={},
        selected_unit=None,
    )
    monkeypatch.setattr(gp, "st", MagicMock(session_state=session))
    monkeypatch.setattr(gp, "load_stratagems", lambda faction_dir: [strat])
    monkeypatch.setattr(gp, "faction_dir_for", lambda player: "necrons")

    captured: list[dict] = []
    monkeypatch.setattr(gp, "render_go_card", lambda **kwargs: captured.append(kwargs))
    undo_calls: list[tuple] = []
    monkeypatch.setattr(gp, "undo_stratagem", lambda *args: undo_calls.append(args))

    gp._render_stratagem_column("Necrons", True)
    captured[0]["on_undo"]()

    assert undo_calls == [(strat, "Necrons")]


# ---------------------------------------------------------------------------
# §6.2 static model (S134 stakeholder decision): timing="phase_reactive" GOs
# render ONLY at their inline trigger anchor — never in the central list.
# ---------------------------------------------------------------------------


def test_render_stratagem_column_hides_phase_reactive_stratagems(monkeypatch) -> None:
    """A GO with timing="phase_reactive" never appears in the central
    Stratagems list, regardless of phase/CP/usage — generic YAML-field
    contract (no id/name check), the proactive sibling still renders."""
    from dataclasses import replace

    proactive = _make_stratagem(id_="pro.strat", name_en="Proactive GO")
    reactive = replace(
        _make_stratagem(id_="rea.strat", name_en="Reactive GO"), timing="phase_reactive"
    )
    session = FakeSessionState(
        cp={"Necrons": 5},
        phase_idx=0,
        used_stratagem_ids={},
        used_stratagem_battle_ids={},
        selected_unit=None,
    )
    monkeypatch.setattr(gp, "st", MagicMock(session_state=session))
    monkeypatch.setattr(gp, "load_stratagems", lambda faction_dir: [proactive, reactive])
    monkeypatch.setattr(gp, "faction_dir_for", lambda player: "necrons")

    captured: list[dict] = []
    monkeypatch.setattr(gp, "render_go_card", lambda **kwargs: captured.append(kwargs))

    gp._render_stratagem_column("Necrons", True)

    names = [c["name"] for c in captured]
    assert "Proactive GO" in names
    assert "Reactive GO" not in names


def test_desperate_breakout_appears_only_inline_not_in_central_list(monkeypatch) -> None:
    """S134 Doppler root fix: the real shared-data Desperate Breakout carries
    timing="phase_reactive" (data regression guard), so the central list never
    shows it — even for an eligible in-melee unit that pre-S134 rendered it
    "ready" — while movementPhase's inline resolution card still renders it.
    The stratagem is matched by effect shape, not by name (INV-4b pattern)."""
    from gameObjects.loader import load_stratagems as real_load

    stratagems = real_load("necrons")  # shared pool included
    db = [
        s
        for s in stratagems
        if s.effect is not None
        and s.effect.type == "move"
        and s.effect.handler == "fall_back_through_models"
    ]
    assert len(db) == 1
    assert db[0].timing == "phase_reactive"

    movement_idx = next(i for i, p in enumerate(gp.PHASES) if p[1] == "movement")
    unit = SimpleNamespace(id="boyz", name_en="Boyz Mob", has_keyword=lambda kw: True)
    session = FakeSessionState(
        cp={"Orks": 10},
        phase_idx=movement_idx,
        round=1,
        used_stratagem_ids={},
        used_stratagem_battle_ids={},
        selected_unit=("Orks", "boyz"),
        p1_units={"boyz": {"movement_chosen": False, "in_melee": True}},
    )
    monkeypatch.setattr(gp, "st", MagicMock(session_state=session))
    monkeypatch.setattr(gp, "load_stratagems", lambda faction_dir: stratagems)
    monkeypatch.setattr(gp, "faction_dir_for", lambda player: "necrons")
    monkeypatch.setattr(gp, "units_list_for", lambda player: [unit])
    monkeypatch.setattr(gp, "units_key_for", lambda player: "p1_units")

    central: list[dict] = []
    monkeypatch.setattr(gp, "render_go_card", lambda **kwargs: central.append(kwargs))
    gp._render_stratagem_column("Orks", True)
    assert all(c["name"] != db[0].name_en for c in central)

    import gameMechanic.movementPhase as mp

    inline: list[dict] = []
    monkeypatch.setattr(mp, "st", MagicMock(session_state=session))
    monkeypatch.setattr(mp, "load_stratagems", lambda faction_dir: stratagems)
    monkeypatch.setattr(mp, "faction_dir_for", lambda player: "necrons")
    monkeypatch.setattr(mp, "render_go_card", lambda **kwargs: inline.append(kwargs))
    mp._render_desperate_breakout("boyz", unit, "Orks", {"models": 10}, {"round": 1})
    assert [c["name"] for c in inline] == [db[0].name_en]
