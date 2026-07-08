"""Tests for uiLayout/gameProtocoll.py — Battle Log deployment snapshot.

Regression target: the deployment snapshot iterated the bare-ID-keyed name
map instead of the (possibly '#N'-suffixed) state dict, so duplicate squads
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
