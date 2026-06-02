import streamlit as st

st.set_page_config(
    page_title="Arbiter",
    layout="wide",
    initial_sidebar_state="collapsed",
)

from uiLayout.gameHeader import CSS_THEME  # noqa: E402

st.markdown(CSS_THEME, unsafe_allow_html=True)

from uiLayout.setupScreen import render_setup_screen  # noqa: E402

if "initialized" not in st.session_state:
    render_setup_screen()
    st.stop()

from uiLayout.armyList import render_army_list  # noqa: E402
from uiLayout.gameActionsArea import render_game_actions_area  # noqa: E402
from uiLayout.gameHeader import render_game_header  # noqa: E402
from uiLayout.gameProtocoll import render_game_protocoll  # noqa: E402

_scenario = st.query_params.get("scenario")
if _scenario and "scenario_loaded" not in st.session_state:
    from gameMechanic.scenarios import load_scenario  # noqa: PLC0415

    load_scenario(_scenario)
    st.session_state.scenario_loaded = True

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
