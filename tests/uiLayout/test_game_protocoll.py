"""Tests for uiLayout/gameProtocoll.py — Battle Log deployment snapshot.

Regression target: the deployment snapshot iterated the bare-ID-keyed name
map instead of the (possibly '#N'-suffixed) state dict, so duplicate squads
never appeared. See Plan 034.
"""

import sys
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import MagicMock

sys.modules.setdefault("streamlit", MagicMock())
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

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
