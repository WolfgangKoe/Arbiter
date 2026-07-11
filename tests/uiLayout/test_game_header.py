"""Tests for gameHeader — end-of-battle result strip (battle_result_html).

The battle ends once the fifth battle round has ended; the player with the
most victory points wins, equal VP is a draw
(docs/work/wahapedia_core_rules/core_rules.txt:2337-2339).
"""

import sys
from pathlib import Path
from unittest.mock import MagicMock

_st_mock = MagicMock()
sys.modules["streamlit"] = _st_mock
sys.modules["streamlit.components"] = MagicMock()
sys.modules["streamlit.components.v1"] = MagicMock()
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

import uiLayout.gameHeader as _gh  # noqa: E402
from uiLayout.gameHeader import battle_result_html  # noqa: E402


class _S(dict):
    def __getattr__(self, key: str):
        try:
            return self[key]
        except KeyError:
            raise AttributeError(key)

    def __setattr__(self, key: str, value: object) -> None:
        self[key] = value


def _session_with_vp(vp_first: int, vp_second: int) -> None:
    _gh.st.session_state = _S(vp={"Necrons": vp_first, "Orks": vp_second})


def test_battle_result_html_first_player_wins_on_more_vp() -> None:
    _session_with_vp(45, 30)
    result = battle_result_html("Necrons", "Orks")
    assert "Winner: Necrons" in result
    assert "45 : 30 VP" in result


def test_battle_result_html_second_player_wins_on_more_vp() -> None:
    _session_with_vp(10, 25)
    result = battle_result_html("Necrons", "Orks")
    assert "Winner: Orks" in result
    assert "10 : 25 VP" in result


def test_battle_result_html_equal_vp_is_a_draw() -> None:
    _session_with_vp(30, 30)
    result = battle_result_html("Necrons", "Orks")
    assert "Draw" in result
    assert "Winner" not in result


def test_battle_result_html_escapes_player_names() -> None:
    _gh.st.session_state = _S(vp={"<b>Evil</b>": 9, "Orks": 1})
    result = battle_result_html("<b>Evil</b>", "Orks")
    assert "<b>Evil</b>" not in result  # raw tag never rendered
    assert "&lt;b&gt;Evil&lt;/b&gt;" in result
