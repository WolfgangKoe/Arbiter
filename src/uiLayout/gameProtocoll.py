"""gameProtocoll — Command Protocol log + Stratagems tab.

Two tabs in the center column below the gameActionDisplayArea:
  - CommandProtocol: round/phase log navigator (setup summary for now)
  - Stratagems:      GO list with visibility logic (data structure ready; Ziel 4)

GO visibility states (see docs/spec/processes.md P-06 and gameObjects/stratagem.py):
  clickable  — conditions met, CP available, not yet used this phase
  greyed     — conditions met, but CP insufficient OR already used this phase
  hidden     — conditions not met → not rendered at all
"""

import json
from itertools import groupby
from pathlib import Path

import streamlit as st

from gameMechanic.game_state import _NECRON_UNITS, _ORK_UNITS, PHASES
from gameObjects.loader import load_command_protocols

_LOG_PATH = Path(__file__).parent.parent.parent / "data" / "log" / "game_log.json"


def _load_game_log() -> list[dict]:  # type: ignore[type-arg]
    if not _LOG_PATH.exists():
        return []
    with _LOG_PATH.open() as f:
        return json.load(f)


def _unit_name_map(faction: str) -> dict[str, str]:
    """Return uid → name_en mapping for a faction."""
    units = _NECRON_UNITS if faction == "Necrons" else _ORK_UNITS
    return {u.id: u.name_en for u in units}


def _state_for(faction: str) -> dict:  # type: ignore[type-arg]
    key = "necron_units" if faction == "Necrons" else "ork_units"
    return st.session_state[key]


def _render_necron_protocols() -> None:
    protocols = load_command_protocols("necrons")
    if not protocols:
        return

    active_id = st.session_state.get("active_protocol_id")
    used_ids = st.session_state.get("used_protocol_ids", [])

    st.caption("**Necron Command Protocols**")
    for p in protocols:
        if p.id == active_id:
            st.markdown(f"**{p.name_de}** — active")
            st.caption(f"  Directive 1: {p.primary}")
            st.caption(f"  Directive 2: {p.secondary}")
        elif p.id in used_ids:
            st.markdown(f"~~{p.name_de}~~ — used")
        else:
            st.caption(f"{p.name_de} — available")
    st.divider()


def _render_command_protocol() -> None:
    first = st.session_state.get("first_player", "Necrons")
    second = st.session_state.get("second_player", "Orks")

    if "Necrons" in (first, second):
        _render_necron_protocols()

    st.caption(
        f"**Round** {st.session_state.get('round', 1)}  ·  "
        f"**Phase** {PHASES[st.session_state.get('phase_idx', 0)][0]}"
    )
    st.caption(f"**Active player:** {st.session_state.get('active', first)}")
    st.divider()

    entries = _load_game_log()
    if entries:
        st.caption("**Battle Log**")
        key_fn = lambda e: (e["round"], e["phase"])  # noqa: E731
        for (round_num, phase), items in groupby(sorted(entries, key=key_fn), key=key_fn):
            with st.expander(f"R{round_num} · {phase.capitalize()}", expanded=False):
                for item in items:
                    st.caption(f"**{item['unit']}**: {item['action']}")
        st.divider()

    st.caption("**Deployment Snapshot**")
    for faction in (first, second):
        st.caption(f"**{faction}**")
        names = _unit_name_map(faction)
        states = _state_for(faction)
        for uid, name in names.items():
            s = states.get(uid, {})
            deployment = s.get("deployment", "—")
            status = "DESTROYED" if s.get("destroyed") else deployment
            st.caption(f"  {name}: {status}")


def _render_stratagems() -> None:
    """Stratagem (GO) panel — architecture ready, content loaded in Ziel 4."""
    active_faction = st.session_state.get("active", "—")
    cp = st.session_state.get("cp", {})
    cp_active = cp.get(active_faction, 0)

    st.caption(f"**{active_faction}** · CP available: **{cp_active}**")
    st.divider()

    # Placeholder: no stratagems loaded yet
    # In Ziel 4, this loop will iterate over loaded Stratagem objects and call
    # stratagem_visibility() from gameObjects/stratagem.py to determine display state.
    st.info(
        "No Stratagems loaded for this army.\n\n"
        "Stratagem data (YAML) and GO visibility logic will be added in Ziel 4.\n\n"
        "**Visibility rules:**\n"
        "- ✅ Conditions met + CP ≥ cost + not used this phase → shown, clickable\n"
        "- 🔘 Conditions met, but CP insufficient → shown, greyed out\n"
        "- 🔘 Conditions met, but already used this phase → shown, greyed out\n"
        "- *(not shown)* Conditions not met"
    )


def render_game_protocoll() -> None:
    tab_protocol, tab_stratagems = st.tabs(["📋 Command Protocol", "⚔️ Stratagems"])
    with tab_protocol:
        _render_command_protocol()
    with tab_stratagems:
        _render_stratagems()
