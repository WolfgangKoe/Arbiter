"""armyCard — Army header: name, faction badges."""

import streamlit as st

_SUBFACTION: dict[str, str] = {
    "Necrons": "Nephrekh",
    "Orks": "Bad Moons",
}


def render_army_card(faction: str) -> None:
    subfaction = _SUBFACTION.get(faction, "")
    st.markdown(f"## {faction}")
    if subfaction:
        st.caption(subfaction)
