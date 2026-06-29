"""gameMechanic test fixtures — cross-file mock isolation.

Root cause: _protocol_session() in test_ability_engine writes to
``_st_mock.session_state`` (the test file's own mock). src helpers like
faction_dir_for() read from ``_gs.st.session_state`` (the canonical mock
bound at import time). These are different objects when collection order
causes test_game_state to be imported first.

Fix: patch all src-module ``st`` attributes to point to the test-file's
``_st_mock`` (not the other way around), so reads go to the same object
writes do. Clear loader caches between tests.
"""

from __future__ import annotations

import sys
from unittest.mock import MagicMock

import pytest


@pytest.fixture(autouse=True)
def reset_streamlit_session_state() -> None:
    _reset()
    yield
    _reset()


def _reset() -> None:
    # Find the test-file mock: the current sys.modules["streamlit"] which the
    # test files write to via ``_st_mock.session_state = session``.
    # After collection, sys.modules["streamlit"] IS the last test file's _st_mock.
    st_mod = sys.modules.get("streamlit")
    if st_mod is None:
        return

    # Reset its session_state to a blank MagicMock.
    st_mod.session_state = MagicMock()

    # Re-point ALL src-module ``st`` attributes to this same object, so reads
    # and writes both go through the same mock.
    for mod_name, mod in sys.modules.items():
        if mod_name.startswith(("gameMechanic.", "gameObjects.")) and hasattr(mod, "st"):
            mod.st = st_mod

    # Also sync _st_mock in both test modules so they all write to the same place.
    for mod in sys.modules.values():
        if hasattr(mod, "_st_mock"):
            mod._st_mock = st_mod

    # Clear loader caches.
    try:
        from gameObjects.loader import (
            _DENY_WARGEAR_CACHE,
            _FACTION_ABILITIES_CACHE,
            _FACTION_META_CACHE,
            _ROUND_CHOICE_CACHE,
            _ROUND_CHOICE_LABEL_CACHE,
            _STRATAGEM_CACHE,
            _SUBFACTION_ABILITIES_CACHE,
            _UNIT_ABILITIES_CACHE,
        )

        _ROUND_CHOICE_CACHE.clear()
        _ROUND_CHOICE_LABEL_CACHE.clear()
        _FACTION_ABILITIES_CACHE.clear()
        _FACTION_META_CACHE.clear()
        _UNIT_ABILITIES_CACHE.clear()
        _SUBFACTION_ABILITIES_CACHE.clear()
        _STRATAGEM_CACHE.clear()
        _DENY_WARGEAR_CACHE.clear()
    except ImportError:
        pass
