"""Regression: round-choice protocol state is keyed per player slot, not per faction.

Two armies of the same faction (a mirror match) share one ``faction_dir`` but must
keep fully independent command-protocol / directive state. Before the fix the runtime
state was keyed by ``faction_dir`` ("necrons"), so in a Necron-vs-Necron game one
player's protocol/directive choice silently overwrote the other's — and the combat
engine read the shared key. These tests pin the per-player keying.
"""

import sys
from pathlib import Path
from unittest.mock import MagicMock

_st_mock = MagicMock()
sys.modules["streamlit"] = _st_mock
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

import gameMechanic.ability_engine as _eng  # noqa: E402
import gameMechanic.game_state as _gs  # noqa: E402
from gameMechanic.ability_engine import (  # noqa: E402
    get_active_round_choice_ap_on_wound_6,
    get_active_round_choice_ignores_cover_half_range,
    get_active_round_choice_modifier,
)
from gameMechanic.game_state import (  # noqa: E402
    _reset_round_choice_state,
    round_choice_state_key,
)


def _install(session: "_S") -> None:
    """Bind the session onto the actual ``st`` the engine modules hold.

    The streamlit mock is a shared module object; assigning to a file-local mock
    would not reach engine/game_state (see backlog §4 mock fragility).
    """
    _eng.st.session_state = session
    _gs.st.session_state = session


# Vehicle protocols with numeric shooting/any-phase modifiers (Hungry Void's
# directives are now per-die/conditional, not numeric — see Plan 025 Step 2).
# primary: ap_on_unmod_wound_6 (shooting, class B) — no longer a generic wound modifier
# (Plan 025 Step 3). secondary: ignore_cover_half_range (shooting, class B).
_VENGEFUL_STARS = "wh40k_9e.necrons.faction.protocol_vengeful_stars"
_ETERNAL_GUARDIAN = "wh40k_9e.necrons.faction.protocol_eternal_guardian"  # primary: save +1


class _S(dict):
    def __getattr__(self, key: str):  # type: ignore[override]
        try:
            return self[key]
        except KeyError:
            raise AttributeError(key)

    def __setattr__(self, key: str, value: object) -> None:
        self[key] = value


def _mirror_session() -> _S:
    """Both players are Necrons (same faction_dir), but distinct player slots."""
    return _S(
        first_player="P1",
        second_player="P2",
        p1_faction_dir="necrons",
        p2_faction_dir="necrons",
    )


def test_mirror_match_protocol_modifiers_are_player_independent() -> None:
    session = _mirror_session()
    session[round_choice_state_key("P1", "active")] = _VENGEFUL_STARS
    session[round_choice_state_key("P1", "directive")] = "primary"
    session[round_choice_state_key("P2", "active")] = _ETERNAL_GUARDIAN
    session[round_choice_state_key("P2", "directive")] = "primary"
    _install(session)

    # Each army sees only its own directive's effect, despite the shared faction.
    # Vengeful Stars primary is class B (ap_on_unmod_wound_6), so it no longer shows
    # up in the generic numeric-modifier dict — it is read via the dedicated function,
    # which is itself player-keyed and so still proves the per-player isolation.
    assert get_active_round_choice_modifier("P1", "shooting", False) == {}
    assert get_active_round_choice_ap_on_wound_6("P1", use_melee=False) == 1
    assert get_active_round_choice_ap_on_wound_6("P2", use_melee=False) == 0
    assert get_active_round_choice_modifier("P2", "shooting", False) == {"save": 1}


def test_mirror_match_one_player_choice_does_not_leak_to_other() -> None:
    session = _mirror_session()
    session[round_choice_state_key("P1", "active")] = _VENGEFUL_STARS
    session[round_choice_state_key("P1", "directive")] = "primary"
    # P2 has made no choice at all.
    _install(session)

    # Vengeful Stars primary (class B) reads via the dedicated AP-on-6 function;
    # P2 made no choice, so neither the modifier dict nor the class-B effects leak.
    assert get_active_round_choice_modifier("P1", "shooting", False) == {}
    assert get_active_round_choice_ap_on_wound_6("P1", use_melee=False) == 1
    assert get_active_round_choice_modifier("P2", "shooting", False) == {}
    assert get_active_round_choice_ap_on_wound_6("P2", use_melee=False) == 0


def test_mirror_match_vengeful_stars_secondary_is_player_independent() -> None:
    """Vengeful Stars D2 (ignore_cover_half_range, class B) stays per-player keyed."""
    session = _mirror_session()
    session[round_choice_state_key("P1", "active")] = _VENGEFUL_STARS
    session[round_choice_state_key("P1", "directive")] = "secondary"
    # P2 has made no choice at all.
    _install(session)

    assert get_active_round_choice_ignores_cover_half_range("P1") is True
    assert get_active_round_choice_ignores_cover_half_range("P2") is False


def test_reset_clears_each_player_independently() -> None:
    session = _mirror_session()
    for player, protocol in (("P1", _VENGEFUL_STARS), ("P2", _ETERNAL_GUARDIAN)):
        session[round_choice_state_key(player, "active")] = protocol
        session[round_choice_state_key(player, "directive")] = "primary"
    _install(session)

    _reset_round_choice_state()

    for player in ("P1", "P2"):
        assert session[round_choice_state_key(player, "active")] is None
        assert session[round_choice_state_key(player, "directive")] is None
