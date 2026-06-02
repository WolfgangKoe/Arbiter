"""Setup screen — roster selection and game configuration before match start."""

from __future__ import annotations

import random

import streamlit as st

from gameMechanic.game_state import CP_BY_GAME_SIZE, PHASES, init_state, list_available_rosters
from gameObjects.rosz_importer import import_roster, parse_ros_bytes, parse_rosz_bytes

_GAME_SIZES = list(CP_BY_GAME_SIZE.keys())
_BATTLE_PHASE_NAMES = [name for name, _ in PHASES[1:]]

_GAME_MODES = ["Matched Play", "Open Play", "Crusade"]
_GAME_MODE_KEYS = {"Matched Play": "matched", "Open Play": "open", "Crusade": "crusade"}

# Missions per game size (Matched Play GT mission pack, 9th Edition)
_MISSIONS_BY_SIZE: dict[str, list[str]] = {
    "Combat Patrol": [
        "Incisive Attack",
        "Outriders",
        "Encircle",
    ],
    "Incursion": [
        "Divide and Conquer",
        "Tipping Point",
        "Scorched Earth",
        "Tear Down Their Icons",
        "Sweep and Clear",
        "Shifting Front",
    ],
    "Strike Force": [
        "Retrieval Mission",
        "Death and Glory",
        "Vital Ground",
        "No Mercy No Respite",
        "Only in Death Does Duty End",
        "Vital Intelligence",
    ],
    "Onslaught": [
        "Lines of Battle",
        "All-out War",
        "Pathway to Glory",
    ],
}

# Secondary objective categories and their objectives
_SECONDARY_CATEGORIES: list[str] = [
    "Purge the Enemy",
    "No Mercy, No Respite",
    "Battlefield Supremacy",
    "Shadow Operations",
    "Warpcraft",
]

_SECONDARY_OBJECTIVES: dict[str, list[str]] = {
    "Purge the Enemy": [
        "Assassination",
        "Bring It Down",
        "Titan Slayers",
        "Thin Their Ranks",
    ],
    "No Mercy, No Respite": [
        "Attrition",
        "Raise the Banners High",
        "The Long War",
        "To the Last",
    ],
    "Battlefield Supremacy": [
        "Domination",
        "Engage on All Fronts",
        "Linebreaker",
        "Outflank",
    ],
    "Shadow Operations": [
        "Behind Enemy Lines",
        "Deploy Scramblers",
        "Investigate Sites",
        "Repair Teleport Homer",
    ],
    "Warpcraft": [
        "Abhor the Witch",
        "Mental Interrogation",
        "Psychic Ritual",
        "Warp Ritual",
    ],
}


def _render_secondary_picker(player_label: str, key_prefix: str) -> tuple[list[str], list[str]]:
    """Render 3 category+objective selectors for one player. Returns (categories, objectives)."""
    selected_categories: list[str] = []
    selected_objectives: list[str] = []

    for slot in range(3):
        available_cats = [c for c in _SECONDARY_CATEGORIES if c not in selected_categories]
        cat_key = f"{key_prefix}_cat_{slot}"
        obj_key = f"{key_prefix}_obj_{slot}"

        col_cat, col_obj = st.columns([2, 3])
        with col_cat:
            category = st.selectbox(
                f"Category {slot + 1}",
                available_cats,
                key=cat_key,
                label_visibility="collapsed" if slot > 0 else "visible",
            )
        with col_obj:
            objectives_for_cat = _SECONDARY_OBJECTIVES.get(category, [])
            objective = st.selectbox(
                f"Objective {slot + 1}",
                objectives_for_cat,
                key=obj_key,
                label_visibility="collapsed" if slot > 0 else "visible",
            )

        selected_categories.append(category)
        selected_objectives.append(objective)

    return selected_categories, selected_objectives


def render_setup_screen() -> None:
    """Render the pre-game setup UI. Calls init_state() on confirmation."""
    st.title("WH40k 9th Edition — Battle Tracker")
    st.markdown("### Setup")
    st.divider()

    # --- Game Mode ---
    col_mode, col_mode_spacer = st.columns([3, 7])
    with col_mode:
        game_mode_label = st.selectbox(
            "Game Mode",
            _GAME_MODES,
            index=0,
            key="setup_game_mode",
        )
    game_mode = _GAME_MODE_KEYS[game_mode_label]

    if game_mode == "crusade":
        st.info(
            "Crusade Mode — full Crusade mechanics are planned for Ziel 6. "
            "Select Matched or Open Play for now."
        )
        return

    # --- Game Size (Matched only) ---
    if game_mode == "matched":
        col_size, col_size_spacer = st.columns([3, 7])
        with col_size:
            game_size = st.selectbox("Game Size", _GAME_SIZES, index=1, key="setup_game_size")
        st.caption(f"Starting CP per player: **{CP_BY_GAME_SIZE[game_size]}**")
    else:
        game_size = "Incursion"
        st.caption("Open Play — Starting CP per player: **3** (fixed)")

    st.divider()

    # --- BattleScribe Import ---
    _render_rosz_import()

    # --- Rosters ---
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
        p2_roster = st.selectbox(
            "Roster",
            rosters,
            index=rosters.index(default_p2),
            key="setup_p2_roster",
            label_visibility="collapsed",
        )

    same_roster = p1_roster == p2_roster
    if same_roster:
        st.warning("Player 1 and Player 2 cannot use the same roster.")

    st.divider()

    # --- Mission (Matched only) ---
    if game_mode == "matched":
        missions = _MISSIONS_BY_SIZE.get(game_size, [])
        col_mission, col_mission_spacer = st.columns([4, 6])
        with col_mission:
            mission: str | None = st.selectbox(
                "Mission",
                missions,
                index=0,
                key="setup_mission",
            )
        st.divider()
    else:
        mission = None

    # --- VP Scoring ---
    st.markdown("**Victory Point Scoring**")
    col_vp_phase, col_vp_round, col_vp_spacer = st.columns([3, 2, 5])
    with col_vp_phase:
        vp_phase = st.selectbox(
            "Score VP at end of",
            _BATTLE_PHASE_NAMES,
            index=0,
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

    st.divider()

    # --- Attacker / Defender ---
    st.markdown("**Attacker / Defender**")

    attacker_key = "setup_attacker_result"
    if attacker_key not in st.session_state:
        st.session_state[attacker_key] = None

    current_attacker: str | None = st.session_state[attacker_key]

    col_roll, col_result = st.columns([2, 8])
    with col_roll:
        if st.button("Roll Off", key="setup_roll_attacker"):
            st.session_state[attacker_key] = random.choice(["p1", "p2"])
            st.rerun()

    with col_result:
        if current_attacker == "p1":
            st.success("Player 1 is Attacker — Player 2 is Defender")
        elif current_attacker == "p2":
            st.success("Player 2 is Attacker — Player 1 is Defender")
        else:
            st.caption("Roll off to determine Attacker and Defender.")

    st.divider()

    # --- Secondary Objectives (Matched only) ---
    secondaries: dict | None = None  # type: ignore[type-arg]
    secondary_vp: dict | None = None  # type: ignore[type-arg]

    if game_mode == "matched":
        st.markdown("**Secondary Objectives**")
        use_secondaries = st.toggle(
            "Use Secondary Objectives",
            value=False,
            key="setup_use_secondaries",
        )

        if use_secondaries:
            st.caption("Each player selects 3 Secondaries — one per category. Max 15 VP each.")
            col_sec_p1, col_sec_gap, col_sec_p2 = st.columns([5, 1, 5])

            with col_sec_p1:
                st.markdown("**Player 1 Secondaries**")
                st.caption("Category · Objective")
                p1_cats, p1_objs = _render_secondary_picker("P1", "sec_p1")

            with col_sec_gap:
                st.empty()

            with col_sec_p2:
                st.markdown("**Player 2 Secondaries**")
                st.caption("Category · Objective")
                p2_cats, p2_objs = _render_secondary_picker("P2", "sec_p2")

            secondaries = {"p1": p1_objs, "p2": p2_objs}
            secondary_vp = {"p1": [0, 0, 0], "p2": [0, 0, 0]}

        st.divider()
    else:
        use_secondaries = False

    # --- Start Game ---
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
            game_mode=game_mode,
            mission=mission,
            attacker=st.session_state.get(attacker_key),
            use_secondaries=use_secondaries,
            secondaries=secondaries,
            secondary_vp=secondary_vp,
        )
        st.rerun()


# ---------------------------------------------------------------------------
# BattleScribe import helper
# ---------------------------------------------------------------------------


def _render_rosz_import() -> None:
    """Render a collapsible section for importing BattleScribe .rosz rosters."""
    with st.expander("Import BattleScribe Roster (.rosz / .ros)", expanded=False):
        uploaded = st.file_uploader(
            "Upload roster file",
            type=["rosz", "ros"],
            key="setup_rosz_upload",
            label_visibility="collapsed",
        )
        if uploaded is None:
            st.caption("Supports BattleScribe .rosz exports for Necrons. Wargear is not imported.")
            return

        # Deduplicate: only process each unique file once per session
        file_key = (uploaded.name, uploaded.size)
        if st.session_state.get("_last_imported_rosz") == file_key:
            st.info(
                f"Already imported **{uploaded.name}**. Select it in the roster dropdowns below."
            )
            return

        data = uploaded.read()
        try:
            if uploaded.name.lower().endswith(".rosz"):
                roster_name, root = parse_rosz_bytes(data)
            else:
                roster_name, root = parse_ros_bytes(data)
            out_path, unmatched = import_roster(roster_name, root)
        except ValueError as exc:
            st.error(f"Import failed: {exc}")
            return

        st.session_state["_last_imported_rosz"] = file_key

        if unmatched:
            st.warning(
                f"Imported **{out_path.name}** with {len(unmatched)} unmatched unit(s): "
                + ", ".join(f"`{n}`" for n in unmatched)
            )
        else:
            st.success(f"Imported **{out_path.name}** — all units matched.")

        st.rerun()
