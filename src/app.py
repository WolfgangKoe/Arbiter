import streamlit as st

st.set_page_config(
    page_title="WH40k 9th Ed. – Battle Tracker",
    layout="wide",
    initial_sidebar_state="collapsed",
)

from gameMechanic.game_state import init_state  # noqa: E402
from uiLayout.armyList import render_army_list  # noqa: E402
from uiLayout.gameActionsArea import render_game_actions_area  # noqa: E402
from uiLayout.gameHeader import render_game_header  # noqa: E402
from uiLayout.gameProtocoll import render_game_protocoll  # noqa: E402

init_state()
render_game_header()
st.divider()

left, center, right = st.columns([1, 2, 1], gap="small")

with left:
    render_army_list(st.session_state.first_player)

with center:
    render_game_actions_area()
    phase_key = st.session_state.get("phase_idx", 0)
    if phase_key != 0:
        render_game_protocoll()

with right:
    render_army_list(st.session_state.second_player)
