"""Setup screen — roster selection and game configuration before match start."""

from __future__ import annotations

import streamlit as st

from gameMechanic.game_state import CP_BY_GAME_SIZE, PHASES, init_state, list_available_rosters

_GAME_SIZES = list(CP_BY_GAME_SIZE.keys())
# Battle phases only (skip "Setup"), used for VP scoring config
_BATTLE_PHASE_NAMES = [name for name, _ in PHASES[1:]]


def render_setup_screen() -> None:
    """Render the pre-game setup UI. Calls init_state() on confirmation."""
    st.title("WH40k 9th Edition — Battle Tracker")
    st.markdown("### Setup")
    st.divider()

    rosters = list_available_rosters()
    if not rosters:
        st.error("No roster files found in `data/rosters/`. Add a `.yaml` roster to start.")
        return

    col_p1, col_gap, col_p2 = st.columns([5, 1, 5])

    with col_p1:
        st.markdown("**Player 1**")
        p1_roster = st.selectbox(
            "Roster",
            rosters,
            index=0,
            key="setup_p1_roster",
            label_visibility="collapsed",
        )

    with col_gap:
        st.markdown("<br><br>**vs**", unsafe_allow_html=True)

    with col_p2:
        st.markdown("**Player 2**")
        default_p2 = rosters[1] if len(rosters) > 1 else rosters[0]
        p2_index = rosters.index(default_p2)
        p2_roster = st.selectbox(
            "Roster",
            rosters,
            index=p2_index,
            key="setup_p2_roster",
            label_visibility="collapsed",
        )

    st.divider()

    col_size, col_spacer = st.columns([3, 7])
    with col_size:
        game_size = st.selectbox("Game size", _GAME_SIZES, index=1, key="setup_game_size")

    st.caption(f"Starting CP per player: **{CP_BY_GAME_SIZE.get(game_size, 3)}**")

    st.divider()
    st.markdown("**Victory Point Scoring**")

    col_vp_phase, col_vp_round, col_vp_spacer = st.columns([3, 2, 5])
    with col_vp_phase:
        # Default: Morale (last battle phase)
        default_phase_idx = len(_BATTLE_PHASE_NAMES) - 1
        vp_phase = st.selectbox(
            "Score VP at end of",
            _BATTLE_PHASE_NAMES,
            index=default_phase_idx,
            key="setup_vp_phase",
        )
    with col_vp_round:
        vp_from_round = st.number_input(
            "From round",
            min_value=1,
            max_value=5,
            value=1,
            step=1,
            key="setup_vp_from_round",
        )

    same_roster = p1_roster == p2_roster
    if same_roster:
        st.warning("Player 1 and Player 2 cannot use the same roster.")

    st.divider()
    if st.button(
        "Start Game",
        type="primary",
        disabled=same_roster,
        use_container_width=False,
    ):
        init_state(
            roster_p1=p1_roster,
            roster_p2=p2_roster,
            game_size=game_size,
            vp_phase=vp_phase,
            vp_from_round=int(vp_from_round),
        )
        st.rerun()
