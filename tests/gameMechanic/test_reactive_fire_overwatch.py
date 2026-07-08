"""Plan 015 — Fire Overwatch reactive window wiring (chargephase.py).

`_inactive_charge` renders in the TARGET's own column for as long as it stays
in `selected_targets` — exactly the window core_rules.txt Z. 1907-1934/3240
describes: charge declared, roll not yet made. This is the natural trigger
site; no separate marker/session-state is needed (unlike Cut Them Down/
Emergency Disembarkation, whose trigger moments are not already represented
by an existing per-render callback).
"""

from __future__ import annotations

import sys
from pathlib import Path
from unittest.mock import MagicMock

_st_mock = MagicMock()
sys.modules["streamlit"] = _st_mock
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

import gameMechanic.chargephase as cp  # noqa: E402


class FakeSessionState(dict):
    def __getattr__(self, name):  # type: ignore[no-untyped-def]
        try:
            return self[name]
        except KeyError as exc:
            raise AttributeError(name) from exc

    def __setattr__(self, name, value):  # type: ignore[no-untyped-def]
        self[name] = value


def test_inactive_charge_opens_fire_overwatch_box_for_target_faction(monkeypatch) -> None:
    from types import SimpleNamespace

    target_unit = SimpleNamespace(name_en="Necron Warriors")
    charger_unit = SimpleNamespace(name_en="Boyz")
    session = FakeSessionState(selected_unit=("Orks", "boyz#1"))
    cp.st.session_state = session
    monkeypatch.setattr(cp, "lookup", lambda faction, uid: (charger_unit, {}))
    spy = MagicMock()
    monkeypatch.setattr(cp, "render_reactive_stratagem_box", spy)

    cp._inactive_charge("Necrons", "warriors#1", target_unit, {})

    spy.assert_called_once()
    call = spy.call_args
    assert call.args[0] == "Necrons"
    assert call.kwargs["phase"] == "charge"
    assert call.kwargs["event"] == "on_declaration"
    assert call.kwargs["decline_key"] == "warriors#1"
    assert "Necron Warriors" in call.kwargs["context_caption"]
    assert "Boyz" in call.kwargs["context_caption"]


def test_inactive_charge_caption_omits_charger_name_when_none_selected(monkeypatch) -> None:
    from types import SimpleNamespace

    target_unit = SimpleNamespace(name_en="Necron Warriors")
    session = FakeSessionState(selected_unit=None)
    cp.st.session_state = session
    spy = MagicMock()
    monkeypatch.setattr(cp, "render_reactive_stratagem_box", spy)

    cp._inactive_charge("Necrons", "warriors#1", target_unit, {})

    spy.assert_called_once()
    caption = spy.call_args.kwargs["context_caption"]
    assert caption == "Necron Warriors was declared a charge target."
