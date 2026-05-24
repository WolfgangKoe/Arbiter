import streamlit as st

st.set_page_config(
    page_title="WH40k 9th Ed. – Battle Tracker",
    layout="wide",
    initial_sidebar_state="collapsed",
)

from ui import main  # noqa: E402 – must come after set_page_config

main()
