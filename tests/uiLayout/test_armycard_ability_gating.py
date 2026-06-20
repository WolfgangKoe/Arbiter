"""Regression tests for armyCard ability-section gating.

Ensures that round-choice and once-per-battle UI are suppressed during
the setup phase and visible in all subsequent phases.
"""

import sys
from pathlib import Path
from unittest.mock import MagicMock

_st_mock = MagicMock()
_st_mock.session_state = {}
sys.modules["streamlit"] = _st_mock
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

from uiLayout.armyCard import _ability_section_visible  # noqa: E402


def test_ability_sections_hidden_in_setup_only() -> None:
    """_ability_section_visible returns False only for 'setup'; True for all other phases."""
    assert _ability_section_visible("setup") is False
    assert _ability_section_visible("command") is True
    assert _ability_section_visible("movement") is True
    assert _ability_section_visible("shooting") is True
    assert _ability_section_visible("fight") is True
