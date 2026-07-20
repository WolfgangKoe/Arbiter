"""gameMechanic test fixtures — cross-file mock isolation.

Root cause: _protocol_session() in test_ability_engine writes to
``_st_mock.session_state`` (the test file's own mock). src helpers like
faction_dir_for() read from ``_gs.st.session_state`` (the canonical mock
bound at import time). These are different objects when collection order
causes test_game_state to be imported first.

Each test_*.py in this package creates its own ``_st_mock = MagicMock()``
and assigns it to ``sys.modules["streamlit"]`` at module import time (i.e.
during pytest collection). That per-file assignment cannot be removed
without editing every test file (out of scope for this refactor: pure
test-infra cleanup, no test-behaviour change) — by the time collection
finishes, ``sys.modules["streamlit"]`` holds whichever file's mock was
imported last, and every other test file's own ``_st_mock`` still points
at ITS OWN (now-orphaned) mock.

Fix: bind everything to ONE canonical object ONCE, in a session-scoped
fixture that runs after collection (so it sees whichever mock "won") and
before the first test — not, as before, via an ad-hoc re-scan of
``sys.modules`` repeated on every single test. Nothing re-assigns
``sys.modules["streamlit"]`` once collection is over (verified: no test
function body does so — only module-level code, which only runs during
collection), so a one-shot bind is behaviourally equivalent to the old
per-test re-scan, just explicit and non-redundant instead of an implicit
side effect recomputed every test. The remaining per-test fixture only
resets the mutable state (session_state, loader caches) that genuinely
needs a fresh value per test.
"""

from __future__ import annotations

import sys
from unittest.mock import MagicMock

import pytest


@pytest.fixture(scope="session", autouse=True)
def _canonical_streamlit_mock():
    """Re-point every src/test module's ``st`` (or ``_st_mock``) reference
    at the single ``sys.modules["streamlit"]`` object left behind by
    collection, once for the whole session. See module docstring for why
    this must reference ``sys.modules`` at all (test files we may not
    touch) and why a one-shot session bind is safe (nothing rebinds
    ``sys.modules["streamlit"]`` after collection).
    """
    st_mod = sys.modules.get("streamlit")
    if st_mod is None:
        yield None
        return

    for mod_name, mod in list(sys.modules.items()):
        if mod_name.startswith(("gameMechanic.", "gameObjects.")) and hasattr(mod, "st"):
            mod.st = st_mod
    for mod in list(sys.modules.values()):
        if hasattr(mod, "_st_mock"):
            mod._st_mock = st_mod

    yield st_mod


@pytest.fixture(autouse=True)
def reset_streamlit_session_state(_canonical_streamlit_mock) -> None:
    _reset(_canonical_streamlit_mock)
    yield
    _reset(_canonical_streamlit_mock)


def _reset(st_mod: MagicMock | None) -> None:
    if st_mod is not None:
        # Fresh session_state per test — the actual per-test isolation need.
        st_mod.session_state = MagicMock()

    # Clear loader caches.
    try:
        from gameObjects.loader import (
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
    except ImportError:
        pass
