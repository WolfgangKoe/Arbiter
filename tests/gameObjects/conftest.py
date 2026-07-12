"""gameObjects test fixtures — cache isolation.

The loader module keeps module-level caches that persist across test
functions. Without cleanup, tests that populate those caches (e.g. the
loader cache-hit tests) leak state into unrelated tests that assume a
clean loader — this causes ~50 abilityEngine failures when tests run
as a subset (cache-pollution). The autouse fixture below clears all 8
caches before every test in this package, keeping each test fully isolated.
"""

from __future__ import annotations

import pytest


@pytest.fixture(autouse=True)
def clear_loader_caches() -> None:
    """Clear all module-level loader caches before each test."""
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
