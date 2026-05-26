"""gameProtocoll — Setup summary and future log navigator."""

import streamlit as st

from models import NECRON_UNITS, ORK_UNITS, Unit


def _units_for(faction: str) -> list[Unit]:
    return NECRON_UNITS if faction == "Necrons" else ORK_UNITS


def _states_for(faction: str) -> dict:  # type: ignore[type-arg]
    key = "necron_units" if faction == "Necrons" else "ork_units"
    return st.session_state[key]


def render_game_protocoll() -> None:
    with st.expander("Setup Summary", expanded=False):
        first = st.session_state.get("first_player", "Necrons")
        second = st.session_state.get("second_player", "Orks")
        st.caption(f"**First player:** {first}")
        st.divider()
        for faction in (first, second):
            st.caption(f"**{faction}**")
            for u in _units_for(faction):
                d = _states_for(faction)[u.uid].get("deployment", "stationary")
                st.caption(f"  {u.name}: {d}")
