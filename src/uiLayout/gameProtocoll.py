"""gameProtocoll — Command Protocol log + Stratagems tab.

Two tabs in the center column below the gameActionDisplayArea:
  - CommandProtocol: round/phase log navigator (setup summary for now)
  - Stratagems:      GO list with visibility logic (data structure ready; Ziel 4)

GO visibility states (see docs/processes.md P-06 and gameObjects/stratagem.py):
  clickable  — conditions met, CP available, not yet used this phase
  greyed     — conditions met, but CP insufficient OR already used this phase
  hidden     — conditions not met → not rendered at all
"""

import streamlit as st

from engine import _NECRON_UNITS, _ORK_UNITS, PHASES


def _unit_name_map(faction: str) -> dict[str, str]:
    """Return uid → name_en mapping for a faction."""
    units = _NECRON_UNITS if faction == "Necrons" else _ORK_UNITS
    return {u.id: u.name_en for u in units}


def _state_for(faction: str) -> dict:  # type: ignore[type-arg]
    key = "necron_units" if faction == "Necrons" else "ork_units"
    return st.session_state[key]


def _render_command_protocol() -> None:
    first = st.session_state.get("first_player", "Necrons")
    second = st.session_state.get("second_player", "Orks")

    st.caption(
        f"**Round** {st.session_state.get('round', 1)}  ·  "
        f"**Phase** {PHASES[st.session_state.get('phase_idx', 0)][0]}"
    )
    st.caption(f"**Active player:** {st.session_state.get('active', first)}")
    st.divider()

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
