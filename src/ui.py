import streamlit as st

from engine import (
    adjust_cp,
    adjust_vp,
    apply_damage,
    heal_unit,
    init_state,
    log_action,
    next_phase,
    reset_game,
    set_charged,
    set_deployment,
    set_movement_status,
)
from models import NECRON_UNITS, ORK_UNITS, PHASES, Unit

CSS_THEME = """
<style>
/* ── Imperial Gothic Theme ──────────────────────────────────────────── */
:root {
    --arb-bg:        #0f0e0c;
    --arb-surface:   #1c1a14;
    --arb-border:    #2e2618;
    --arb-accent:    #c9a84c;
    --arb-accent-lt: #e8d5a3;
    --arb-muted:     #6b5f44;
    --arb-text:      #e0cca0;
    --arb-unit:      #b0a080;
    --arb-hover:     #2a2316;
    --arb-red:       #8b1a1a;
    --arb-btn:       #5a4820;
    --arb-green:     #4a7c3f;
    --arb-blue:      #2a4a6a;
}

/* Background */
.stApp, [data-testid="stApp"], [data-testid="stAppViewContainer"] {
    background-color: var(--arb-bg);
}
[data-testid="stHeader"] { background: var(--arb-surface); border-bottom: 1px solid var(--arb-border); }
section[data-testid="stMain"] > div { background-color: var(--arb-bg); }

/* Typography */
.stApp, .stMarkdown, .stMarkdown p,
h1, h2, h3, h4, h5, h6 { color: var(--arb-text) !important; }
h1, h2 { letter-spacing: 0.12em; text-transform: uppercase; }
h2 { color: var(--arb-accent) !important; font-size: 1rem; }
.stCaption, .stCaption p { color: var(--arb-muted) !important; }

/* Metrics */
[data-testid="metric-container"] {
    background: var(--arb-surface) !important;
    border: 1px solid var(--arb-border);
    border-left: 2px solid var(--arb-accent);
    border-radius: 2px;
    padding: 8px 12px;
}
[data-testid="stMetricValue"] { color: var(--arb-accent-lt) !important; }
[data-testid="stMetricLabel"] { color: var(--arb-muted) !important; font-size: 0.65rem; letter-spacing: 0.1em; text-transform: uppercase; }

/* Expanders (unit cards) */
[data-testid="stExpander"] {
    background: var(--arb-surface) !important;
    border: 1px solid var(--arb-border) !important;
    border-left: 2px solid var(--arb-accent) !important;
    border-radius: 2px !important;
}
[data-testid="stExpander"] summary {
    color: var(--arb-text) !important;
    background: var(--arb-hover) !important;
}
[data-testid="stExpander"] summary:hover { background: #332d1e !important; }
[data-testid="stExpanderDetails"] { background: var(--arb-surface) !important; }

/* Buttons */
.stButton > button {
    background: transparent !important;
    border: 1px solid var(--arb-btn) !important;
    color: var(--arb-accent-lt) !important;
    border-radius: 2px !important;
    letter-spacing: 0.05em;
    transition: background 0.15s, border-color 0.15s;
}
.stButton > button:hover {
    background: var(--arb-hover) !important;
    border-color: var(--arb-accent) !important;
}
.stButton > button[data-testid="baseButton-primary"],
.stButton > button[kind="primary"] {
    background: var(--arb-accent) !important;
    border-color: var(--arb-accent) !important;
    color: var(--arb-bg) !important;
    font-weight: 600;
}
.stButton > button[data-testid="baseButton-primary"]:hover {
    background: var(--arb-accent-lt) !important;
}

/* Dividers */
hr { border-color: var(--arb-border) !important; opacity: 1 !important; }

/* Inputs */
.stTextInput input, .stNumberInput input, .stTextArea textarea {
    background: var(--arb-surface) !important;
    border: 1px solid var(--arb-border) !important;
    color: var(--arb-text) !important;
    border-radius: 2px !important;
}
.stTextInput input:focus, .stNumberInput input:focus {
    border-color: var(--arb-accent) !important;
    box-shadow: none !important;
}
.stTextArea textarea {
    color: var(--arb-unit) !important;
    font-family: monospace;
    font-size: 11px !important;
}

/* Selectbox */
.stSelectbox [data-baseweb="select"] > div {
    background: var(--arb-surface) !important;
    border: 1px solid var(--arb-border) !important;
    color: var(--arb-text) !important;
    border-radius: 2px !important;
}
[data-baseweb="popover"] ul { background: var(--arb-surface) !important; }
[data-baseweb="popover"] li { color: var(--arb-text) !important; }
[data-baseweb="popover"] li:hover { background: var(--arb-hover) !important; }

/* Slider */
[data-testid="stSlider"] [data-baseweb="slider"] div[role="slider"] { background: var(--arb-accent) !important; }
[data-testid="stSlider"] [data-baseweb="slider"] div[data-testid="stSliderTrackFill"] { background: var(--arb-accent) !important; }

/* Progress bar */
[data-testid="stProgressBar"] > div { background: var(--arb-border) !important; border-radius: 0 !important; }
[data-testid="stProgressBar"] > div > div { background: var(--arb-accent) !important; border-radius: 0 !important; }

/* Info / success / error boxes */
[data-testid="stInfo"] {
    background: var(--arb-hover) !important;
    border-left: 2px solid var(--arb-accent) !important;
    color: var(--arb-text) !important;
    border-radius: 2px !important;
}
[data-testid="stSuccess"] {
    background: #141e10 !important;
    border-left: 2px solid #4a7c3f !important;
    color: #a0cc90 !important;
    border-radius: 2px !important;
}
[data-testid="stError"] {
    background: #1e1010 !important;
    border-left: 2px solid var(--arb-red) !important;
    color: #cc9090 !important;
    border-radius: 2px !important;
}
[data-testid="stWarning"] {
    background: #1e1a10 !important;
    border-left: 2px solid #8b6a1a !important;
    color: #ccb080 !important;
    border-radius: 2px !important;
}

/* Label text */
label, .stLabel { color: var(--arb-muted) !important; font-size: 0.7rem !important; letter-spacing: 0.08em; text-transform: uppercase; }

/* Title override */
[data-testid="stTitle"] { color: var(--arb-accent) !important; letter-spacing: 0.15em; text-transform: uppercase; }

/* Hide Streamlit default toolbar (deploy button, hamburger menu) */
header[data-testid="stHeader"] { display: none !important; }
[data-testid="stToolbar"] { display: none !important; }
[data-testid="stDecoration"] { display: none !important; }

</style>
"""


# ---------------------------------------------------------------------------
# Badge helpers
# ---------------------------------------------------------------------------

_BADGE_COLORS = {
    "ADVANCED": ("#c9a84c", "#2e2618"),
    "STATIONARY": ("#6b5f44", "#1c1a14"),
    "RETREATED": ("#8b1a1a", "#1e1010"),
    "IN MELEE": ("#cc6644", "#2a1810"),
    "CHARGED": ("#9b59b6", "#1a0a2a"),
    "RESERVE": ("#2a6a8b", "#101820"),
    "DESTROYED": ("#8b1a1a", "#1e1010"),
}


def _badge(text: str) -> str:
    fg, bg = _BADGE_COLORS.get(text, ("#c9a84c", "#2e2618"))
    return (
        f'<span style="background:{bg};border:1px solid {fg};border-radius:2px;'
        f"padding:1px 6px;font-size:10px;color:{fg};letter-spacing:0.06em;"
        f'font-weight:600;margin-right:3px;">{text}</span>'
    )


def _state_badges_html(state: dict) -> str:  # type: ignore[type-arg]
    parts = []
    ms = state.get("movement_status", "stationary")
    if ms == "advanced":
        parts.append(_badge("ADVANCED"))
    elif ms == "stationary":
        parts.append(_badge("STATIONARY"))
    elif ms == "retreated":
        parts.append(_badge("RETREATED"))
    if state.get("charged_this_turn"):
        parts.append(_badge("CHARGED"))
    elif state.get("in_melee"):
        parts.append(_badge("IN MELEE"))
    if state.get("in_reserve"):
        parts.append(_badge("RESERVE"))
    return "".join(parts)


# ---------------------------------------------------------------------------
# Unit lookup helpers
# ---------------------------------------------------------------------------


def _lookup(faction: str, uid: str) -> tuple[Unit, dict]:  # type: ignore[type-arg]
    units = NECRON_UNITS if faction == "Necrons" else ORK_UNITS
    unit = next(u for u in units if u.uid == uid)
    key = "necron_units" if faction == "Necrons" else "ork_units"
    return unit, st.session_state[key][uid]


# ---------------------------------------------------------------------------
# Unit card — dynamic section per phase
# ---------------------------------------------------------------------------


def _dynamic_setup(unit: Unit, state: dict, faction: str) -> None:  # type: ignore[type-arg]
    opts = ["Normal", "Stationary", "Reserve"]
    current = state.get("deployment", "normal").capitalize()
    idx = opts.index(current) if current in opts else 0
    chosen = st.selectbox(
        "Deployment",
        opts,
        index=idx,
        key=f"deploy_{faction}_{unit.uid}",
    )
    mapping = {"Normal": "normal", "Stationary": "stationary", "Reserve": "reserve"}
    new_val = mapping[chosen]
    if new_val != state.get("deployment", "normal"):
        set_deployment(unit.uid, faction, new_val)
        st.rerun()


def _dynamic_movement(unit: Unit, state: dict, faction: str) -> None:  # type: ignore[type-arg]
    if state.get("in_reserve"):
        if st.session_state.round == 1:
            st.caption("In Reserve — arrives from Round 2.")
        else:
            st.caption("In Reserve — can be deployed this turn.")
        return
    st.caption(f"**M** {unit.move}")
    badges_html = _state_badges_html(state)
    if badges_html:
        st.markdown(badges_html, unsafe_allow_html=True)
    else:
        st.caption("Status: Normal")


def _dynamic_shooting_attacker(unit: Unit, state: dict) -> None:  # type: ignore[type-arg]
    ms = state.get("movement_status", "normal")
    if ms == "advanced":
        st.caption("⚠ Advanced — cannot shoot.")
        return
    if ms == "retreated":
        st.caption("⚠ Retreated — cannot shoot.")
        return
    if state.get("in_melee"):
        st.caption("⚠ In melee — cannot shoot.")
        return
    ranged = [w for w in unit.weapons if not w.is_melee]
    if not ranged:
        st.caption("No ranged weapons.")
        return
    for w in ranged:
        ap_str = f"AP{w.ap}" if w.ap != 0 else "AP0"
        st.caption(
            f"**{w.name}** · A{w.attacks} · BS{w.skill}+ · S{w.strength} · {ap_str} · D{w.damage}"
            + (f" · _{w.abilities}_" if w.abilities else "")
        )


def _dynamic_shooting_target(unit: Unit, state: dict) -> None:  # type: ignore[type-arg]
    inv_str = f"{unit.invuln}+" if unit.invuln else "—"
    fnp_str = f"{unit.fnp}+" if unit.fnp else "—"
    cols = st.columns(4)
    cols[0].metric("T", unit.toughness)
    cols[1].metric("Sv", f"{unit.save}+")
    cols[2].metric("++", inv_str)
    cols[3].metric("FNP", fnp_str)


def _dynamic_fight(unit: Unit, state: dict, is_active: bool) -> None:  # type: ignore[type-arg]
    in_melee = state.get("in_melee")
    if not in_melee and not is_active:
        st.caption("No action possible.")
        return
    if state.get("charged_this_turn"):
        st.caption("**Fights first** (charged this turn).")
    melee = [w for w in unit.weapons if w.is_melee]
    if not melee:
        st.caption("No melee weapons.")
        return
    for w in melee:
        ap_str = f"AP{w.ap}" if w.ap != 0 else "AP0"
        st.caption(
            f"**{w.name}** · A{w.attacks} · WS{w.skill}+ · S{w.strength} · {ap_str} · D{w.damage}"
            + (f" · _{w.abilities}_" if w.abilities else "")
        )


def _dynamic_morale(unit: Unit, state: dict) -> None:  # type: ignore[type-arg]
    lost = state.get("lost_models_this_turn", 0)
    if unit.count == 1:
        st.caption("Single model — auto-pass.")
        return
    if lost == 0:
        st.caption("No losses this turn — no test required.")
        return
    st.caption(f"**Ld** {unit.leadership} | Lost **{lost}** model(s) → morale test required.")


def _unit_dynamic_section(
    unit: Unit, state: dict, faction: str, phase_key: str, is_active: bool  # type: ignore[type-arg]
) -> None:
    is_psyker = any(kw.upper() == "PSYKER" for kw in unit.other_keywords + unit.faction_keywords)

    if phase_key == "setup":
        _dynamic_setup(unit, state, faction)
        return

    if state.get("in_reserve") and phase_key != "movement":
        st.caption("In Reserve — not on battlefield.")
        return

    if phase_key == "command":
        st.caption("No phase-specific actions.")
    elif phase_key == "movement":
        if is_active:
            _dynamic_movement(unit, state, faction)
        else:
            st.caption("—")
    elif phase_key == "psychic":
        if is_psyker:
            st.caption("PSYKER — select to declare psychic powers.")
        else:
            st.caption("No action possible.")
    elif phase_key == "shooting":
        if is_active:
            _dynamic_shooting_attacker(unit, state)
        else:
            _dynamic_shooting_target(unit, state)
    elif phase_key == "charge":
        if is_active:
            ms = state.get("movement_status", "normal")
            if ms in ("advanced", "retreated"):
                st.caption(f"⚠ {ms.capitalize()} — cannot charge.")
            else:
                st.caption('Eligible to charge (≤ 12" from enemy).')
        else:
            st.caption("—")
    elif phase_key == "fight":
        _dynamic_fight(unit, state, is_active)
    elif phase_key == "morale":
        _dynamic_morale(unit, state)


# ---------------------------------------------------------------------------
# Unit card
# ---------------------------------------------------------------------------


def unit_card(unit: Unit, state: dict, faction: str) -> None:  # type: ignore[type-arg]
    phase_key = PHASES[st.session_state.phase_idx][1]
    active = st.session_state.active
    is_active = faction == active

    destroyed = state["destroyed"]
    title = unit.name if not destroyed else f"~~{unit.name}~~"

    with st.expander(title, expanded=False):
        if destroyed:
            st.caption("Destroyed.")
            return

        # Keywords
        if unit.faction_keywords:
            st.caption(" · ".join(unit.faction_keywords))
        if unit.other_keywords:
            st.caption(
                '<span style="color:#4a3f2a;font-size:0.65rem;">'
                + " · ".join(unit.other_keywords)
                + "</span>",
                unsafe_allow_html=True,
            )

        # ── Permanent: stat profile ──────────────────────────────────────
        sc = st.columns(7)
        for col, lbl, val in zip(
            sc,
            ["M", "T", "Sv", "W", "++", "Ld", "OC"],
            [
                unit.move,
                unit.toughness,
                f"{unit.save}+",
                unit.wounds,
                f"{unit.invuln}+" if unit.invuln else "—",
                unit.leadership,
                unit.oc,
            ],
        ):
            col.metric(lbl, val)

        # HP display
        cur = state["current_wounds"]
        models_alive = state["models"]
        if unit.count == 1:
            st.caption(f"W: {cur}/{unit.wounds}")
            st.progress(cur / unit.wounds if unit.wounds > 0 else 0)
        elif unit.wounds == 1:
            st.caption(f"Models: {models_alive}/{unit.count}")
            st.progress(models_alive / unit.count if unit.count > 0 else 0)
        else:
            front_hp = (cur - (models_alive - 1) * unit.wounds) if cur > 0 else 0
            st.caption(f"Models: {models_alive}/{unit.count}")
            st.progress(models_alive / unit.count if unit.count > 0 else 0)
            st.caption(f"Current model: {front_hp}/{unit.wounds} W")
            st.progress(front_hp / unit.wounds if unit.wounds > 0 else 0)

        # Damage buttons
        uid = unit.uid
        bc = st.columns(6)
        for col, delta, label in zip(
            bc, [-3, -2, -1, 1, 2, 3], ["−3", "−2", "−1", "+1", "+2", "+3"]
        ):
            with col:
                is_mortal = delta == -1
                if st.button(
                    label,
                    key=f"w{delta}_{faction}_{uid}",
                    type="primary" if is_mortal else "secondary",
                ):
                    if delta < 0:
                        apply_damage(uid, faction, -delta, unit, mortal=is_mortal)
                    else:
                        heal_unit(uid, faction, delta, unit)
                    st.rerun()

        # State badges
        badges_html = _state_badges_html(state)
        if badges_html and phase_key != "setup":
            st.markdown(badges_html, unsafe_allow_html=True)

        # Select / Target button (not in setup)
        in_reserve = state.get("in_reserve", False)
        if phase_key != "setup":
            if is_active:
                sel = st.session_state.selected_unit
                is_sel = sel == (faction, uid)
                btn_lbl = "◀ Selected" if is_sel else "▶ Select"
                btn_type = "primary" if is_sel else "secondary"
                if st.button(
                    btn_lbl,
                    key=f"sel_{faction}_{uid}",
                    type=btn_type,
                    use_container_width=True,
                    disabled=in_reserve,
                ):
                    st.session_state.selected_unit = None if is_sel else (faction, uid)
                    st.session_state.selected_target = None
                    st.rerun()
            elif phase_key in ("shooting", "fight", "charge"):
                tgt = st.session_state.selected_target
                is_tgt = tgt == (faction, uid)
                btn_lbl = "◀ Targeted" if is_tgt else "▶ Target"
                btn_type = "primary" if is_tgt else "secondary"
                if st.button(
                    btn_lbl,
                    key=f"tgt_{faction}_{uid}",
                    type=btn_type,
                    use_container_width=True,
                    disabled=in_reserve,
                ):
                    st.session_state.selected_target = None if is_tgt else (faction, uid)
                    st.rerun()

        # ── Dynamic section ──────────────────────────────────────────────
        st.divider()
        _unit_dynamic_section(unit, state, faction, phase_key, is_active)

        # Abilities (always shown)
        if unit.abilities:
            st.caption(f"*{unit.abilities}*")


# ---------------------------------------------------------------------------
# Central area — phase renderers (3-level: overview / unit selected / both selected)
# ---------------------------------------------------------------------------

_PHASE_RULES = {
    "command": (
        "**Command Phase**\n\n"
        "The active player receives **+1 CP** (Battle-forged armies). "
        "Activate abilities and stratagems that trigger in the Command Phase."
    ),
    "movement": (
        "**Movement Phase**\n\n"
        "Select a unit and choose its movement type:\n"
        '- **Normal** — move up to M"\n'
        '- **Advance** — move up to M"+D6", cannot shoot or charge afterwards\n'
        "- **Stationary** — do not move\n"
        '- **Retreat** — only if in melee; move up to M", cannot shoot or charge afterwards'
    ),
    "psychic": (
        "**Psychic Phase**\n\n"
        "PSYKER units attempt to manifest psychic powers. "
        "Roll **2D6** ≥ Warp Charge value to manifest. "
        "Opponent may attempt to deny with their own PSYKER (2D6 > manifesting roll)."
    ),
    "shooting": (
        "**Shooting Phase**\n\n"
        "Select a unit to shoot, then select a target. "
        "Units that Advanced or Retreated cannot shoot. "
        "Units in melee cannot shoot.\n\n"
        "Attack sequence: **Hit** (BS) → **Wound** (S vs T) → **Save** (Sv−AP) → **Damage**"
    ),
    "charge": (
        "**Charge Phase**\n\n"
        'Eligible units (≤ 12" from enemy, did not Advance or Retreat) may declare a charge. '
        "Roll **2D6** — result must be ≥ distance to closest target model. "
        "On success: move into melee range."
    ),
    "fight": (
        "**Fight Phase**\n\n"
        "Starting with the **non-active player**, both sides alternate selecting eligible units. "
        "Units that charged this turn fight **before** other units. "
        'Each unit: **Pile In** (up to 3") → **Melee attacks** → **Consolidate** (up to 3").'
    ),
    "morale": (
        "**Morale Phase**\n\n"
        "Units that suffered model losses this turn must take a morale test: "
        "Roll **D6** + models lost. If result > Leadership: additional models flee (result − Ld).\n\n"
        "Single-model units auto-pass."
    ),
}


def phase_setup() -> None:
    st.markdown("### Setup")
    st.info(
        "Configure your armies before the battle begins.\n\n"
        "1. **Select first player** — the active player takes their turn first each battle round.\n"
        "2. **Set deployment** for each unit using the dropdowns in the unit cards:\n"
        "   - **Normal** — deployed on the battlefield\n"
        "   - **Stationary** — deployed but will not move in turn 1\n"
        "   - **Reserve** — arrives from turn 2 onwards\n\n"
        "When ready, click **→** to begin Battle Round 1."
    )

    st.markdown("---")
    st.markdown("**First Player**")
    active = st.session_state.active
    c1, c2 = st.columns(2)
    with c1:
        nc_type = "primary" if active == "Necrons" else "secondary"
        if st.button(
            "Necrons go first", key="setup_first_necrons", type=nc_type, use_container_width=True
        ):
            st.session_state.active = "Necrons"
            st.session_state.first_player = "Necrons"
            st.session_state.second_player = "Orks"
            st.rerun()
    with c2:
        ok_type = "primary" if active == "Orks" else "secondary"
        if st.button(
            "Orks go first", key="setup_first_orks", type=ok_type, use_container_width=True
        ):
            st.session_state.active = "Orks"
            st.session_state.first_player = "Orks"
            st.session_state.second_player = "Necrons"
            st.rerun()
    st.caption(f"Currently selected: **{active}** go first.")


def _central_level1(phase_key: str) -> None:
    rules = _PHASE_RULES.get(phase_key, "")
    st.info(rules)


def _central_command_actions(faction: str, uid: str) -> None:
    unit, state = _lookup(faction, uid)
    st.markdown(f"**{unit.name}**")
    badges_html = _state_badges_html(state)
    if badges_html:
        st.markdown(badges_html, unsafe_allow_html=True)
    st.caption("No phase-specific unit actions in the Command Phase.")
    if unit.abilities:
        with st.expander("Abilities", expanded=False):
            st.caption(unit.abilities)


def _central_movement_actions(faction: str, uid: str) -> None:
    unit, state = _lookup(faction, uid)
    ms = state.get("movement_status", "normal")
    in_melee = state.get("in_melee", False)

    st.markdown(f"**{unit.name}** — M {unit.move}")
    badges_html = _state_badges_html(state)
    if badges_html:
        st.markdown(badges_html, unsafe_allow_html=True)

    if state.get("in_reserve"):
        if st.session_state.round == 1:
            st.warning("Unit is in Reserve — cannot deploy until Round 2.")
        else:
            st.info("Unit is in Reserve — deploy from the board edge.")
            if st.button(
                "Deploy from Reserve",
                key=f"deploy_reserve_{faction}_{uid}",
                type="primary",
                use_container_width=True,
            ):
                set_deployment(uid, faction, "normal")
                set_movement_status(uid, faction, "normal")
                log_action(st.session_state.round, "movement", unit.name, "deployed from reserve")
                st.rerun()
        return

    st.markdown("Set movement status:")
    cols = st.columns(4)
    options = [
        ("Normal", "normal", 'Move up to M"'),
        ("Advance", "advanced", 'M"+D6", no shoot/charge'),
        ("Stationary", "stationary", "Do not move"),
        ("Retreat", "retreated", "Exit melee, no shoot/charge"),
    ]
    for col, (label, value, tip) in zip(cols, options):
        with col:
            disabled = value == "retreated" and not in_melee
            btn_type = "primary" if ms == value else "secondary"
            if st.button(
                label,
                key=f"mv_{faction}_{uid}_{value}",
                type=btn_type,
                disabled=disabled,
                use_container_width=True,
                help=tip,
            ):
                set_movement_status(uid, faction, value)
                log_action(st.session_state.round, "movement", unit.name, f"movement: {value}")
                st.rerun()

    if in_melee and ms not in ("retreated", "stationary"):
        st.caption("Unit is in melee — only Stationary or Retreat allowed.")


def _central_shooting_actions(faction: str, uid: str) -> None:
    unit, state = _lookup(faction, uid)
    ms = state.get("movement_status", "normal")

    st.markdown(f"**{unit.name}** — Shooting")
    badges_html = _state_badges_html(state)
    if badges_html:
        st.markdown(badges_html, unsafe_allow_html=True)

    if ms == "advanced":
        st.warning("Advanced this turn — cannot shoot.")
        return
    if ms == "retreated":
        st.warning("Retreated this turn — cannot shoot.")
        return
    if state.get("in_melee"):
        st.warning("Bound in melee — cannot shoot.")
        return

    ranged = [w for w in unit.weapons if not w.is_melee]
    if not ranged:
        st.warning("No ranged weapons — no action possible.")
        return

    tgt = st.session_state.selected_target
    if tgt is None:
        st.info("Select a **target** unit from the enemy sidebar (▶ Target).")
        return

    tgt_faction, tgt_uid = tgt
    tgt_unit, tgt_state = _lookup(tgt_faction, tgt_uid)

    st.markdown(f"**Target:** {tgt_unit.name}")
    inv_display = f"{tgt_unit.invuln}+" if tgt_unit.invuln else "—"
    st.markdown(f"T {tgt_unit.toughness} · Sv {tgt_unit.save}+ · ++ {inv_display}")
    st.divider()
    st.markdown("**Attack sequence** (for reference — roll dice on the table):")
    for w in ranged:
        thresh = _wound_thresh(w.strength, tgt_unit.toughness)
        eff_save = min(tgt_unit.save + abs(w.ap), tgt_unit.invuln or 99)
        save_str = f"{eff_save}+" if eff_save <= 6 else "none"
        st.caption(
            f"**{w.name}**: {w.attacks} att · hit on {w.skill}+ · "
            f"wound on {thresh}+ · save {save_str} · D{w.damage}"
        )
    if st.button("Log Shooting Action", key=f"log_shoot_{faction}_{uid}", use_container_width=True):
        log_action(st.session_state.round, "shooting", unit.name, f"shot at {tgt_unit.name}")
        st.success("Action logged.")


def _central_charge_actions(faction: str, uid: str) -> None:
    unit, state = _lookup(faction, uid)
    ms = state.get("movement_status", "normal")

    st.markdown(f"**{unit.name}** — Charge")
    badges_html = _state_badges_html(state)
    if badges_html:
        st.markdown(badges_html, unsafe_allow_html=True)

    if ms in ("advanced", "retreated"):
        st.warning(f"{ms.capitalize()} this turn — cannot charge.")
        return

    tgt = st.session_state.selected_target
    if tgt is None:
        st.info("Select a **target** to charge from the enemy sidebar (▶ Target).")
        return

    tgt_faction, tgt_uid = tgt
    tgt_unit, _ = _lookup(tgt_faction, tgt_uid)
    st.markdown(f"**Target:** {tgt_unit.name}")
    st.caption("Roll **2D6** — must equal or beat the distance to the target.")

    c1, c2 = st.columns(2)
    with c1:
        if st.button(
            "Charge Successful",
            key=f"charge_ok_{faction}_{uid}",
            type="primary",
            use_container_width=True,
        ):
            set_charged(uid, faction, tgt_uid, tgt_faction)
            log_action(
                st.session_state.round, "charge", unit.name, f"charged {tgt_unit.name} — success"
            )
            st.session_state.selected_target = None
            st.rerun()
    with c2:
        if st.button("Charge Failed", key=f"charge_fail_{faction}_{uid}", use_container_width=True):
            log_action(
                st.session_state.round, "charge", unit.name, f"charged {tgt_unit.name} — failed"
            )
            st.info("Charge failed — no movement.")


def _central_fight_actions(faction: str, uid: str) -> None:
    unit, state = _lookup(faction, uid)
    in_melee = state.get("in_melee", False)

    st.markdown(f"**{unit.name}** — Fight")
    if state.get("charged_this_turn"):
        st.markdown("**Fights first** (charged this turn).")
    badges_html = _state_badges_html(state)
    if badges_html:
        st.markdown(badges_html, unsafe_allow_html=True)

    if not in_melee:
        st.warning("Not in melee — no action possible.")
        return

    tgt = st.session_state.selected_target
    if tgt is None:
        st.info("Select a **target** in melee from the enemy sidebar (▶ Target).")
        return

    tgt_faction, tgt_uid = tgt
    tgt_unit, tgt_state = _lookup(tgt_faction, tgt_uid)
    st.markdown(f"**Target:** {tgt_unit.name}")
    inv_display = f"{tgt_unit.invuln}+" if tgt_unit.invuln else "—"
    st.markdown(f"T {tgt_unit.toughness} · Sv {tgt_unit.save}+ · ++ {inv_display}")
    st.divider()
    melee = [w for w in unit.weapons if w.is_melee]
    for w in melee:
        thresh = _wound_thresh(w.strength, tgt_unit.toughness)
        eff_save = min(tgt_unit.save + abs(w.ap), tgt_unit.invuln or 99)
        save_str = f"{eff_save}+" if eff_save <= 6 else "none"
        st.caption(
            f"**{w.name}**: {w.attacks} att · WS{w.skill}+ · "
            f"wound {thresh}+ · save {save_str} · D{w.damage}"
        )
    if st.button("Log Fight Action", key=f"log_fight_{faction}_{uid}", use_container_width=True):
        log_action(st.session_state.round, "fight", unit.name, f"fought {tgt_unit.name}")
        st.success("Action logged.")


def _central_morale_info(faction: str, uid: str) -> None:
    unit, state = _lookup(faction, uid)
    lost = state.get("lost_models_this_turn", 0)

    st.markdown(f"**{unit.name}**")
    if unit.count == 1:
        st.success("Single model — auto-pass.")
        return
    if lost == 0:
        st.success("No losses this turn — no morale test.")
        return
    st.warning(
        f"**Ld {unit.leadership}** | Lost **{lost}** model(s) this turn.\n\n"
        f"Roll D6 + {lost}. If result > {unit.leadership}: remove (result − {unit.leadership}) additional model(s)."
    )


def _wound_thresh(strength: int, toughness: int) -> int:
    if strength >= toughness * 2:
        return 2
    if strength > toughness:
        return 3
    if strength == toughness:
        return 4
    if strength * 2 <= toughness:
        return 6
    return 5


def phase_command() -> None:
    sel = st.session_state.selected_unit
    if sel is None:
        _central_level1("command")
        active = st.session_state.active
        st.divider()
        st.markdown(f"**+1 CP for {active}**")
        if st.button("Grant +1 CP", key="cmd_cp", type="primary", use_container_width=True):
            adjust_cp(active, 1)
            log_action(st.session_state.round, "command", active, "+1 CP received")
            st.rerun()
    else:
        _central_command_actions(*sel)


def phase_movement() -> None:
    sel = st.session_state.selected_unit
    if sel is None:
        _central_level1("movement")
    else:
        _central_movement_actions(*sel)


def phase_psychic() -> None:
    sel = st.session_state.selected_unit
    if sel is None:
        _central_level1("psychic")
    else:
        faction, uid = sel
        unit, state = _lookup(faction, uid)
        is_psyker = any(
            kw.upper() == "PSYKER" for kw in unit.other_keywords + unit.faction_keywords
        )
        st.markdown(f"**{unit.name}**")
        if is_psyker:
            st.info(
                "PSYKER — declare Smite or psychic powers manually. Track results on the unit card."
            )
        else:
            st.warning("Not a PSYKER — no action possible.")


def phase_shooting() -> None:
    sel = st.session_state.selected_unit
    if sel is None:
        _central_level1("shooting")
    else:
        _central_shooting_actions(*sel)


def phase_charge() -> None:
    sel = st.session_state.selected_unit
    if sel is None:
        _central_level1("charge")
    else:
        _central_charge_actions(*sel)


def phase_fight() -> None:
    sel = st.session_state.selected_unit
    if sel is None:
        _central_level1("fight")
        active = st.session_state.active
        inactive = "Orks" if active == "Necrons" else "Necrons"
        st.caption(
            f"Fight order: **{inactive}** selects first (non-active player), "
            f"then **{active}**. Units that charged fight before others."
        )
    else:
        _central_fight_actions(*sel)


def phase_morale() -> None:
    sel = st.session_state.selected_unit
    if sel is None:
        _central_level1("morale")
    else:
        _central_morale_info(*sel)


def _setup_summary() -> None:
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


PHASE_RENDERERS = {
    "setup": phase_setup,
    "command": phase_command,
    "movement": phase_movement,
    "psychic": phase_psychic,
    "shooting": phase_shooting,
    "charge": phase_charge,
    "fight": phase_fight,
    "morale": phase_morale,
}


# ---------------------------------------------------------------------------
# Score group
# ---------------------------------------------------------------------------

_SCORE_LABEL_STYLE = (
    "display:block;width:100%;text-align:center;font-size:1.6rem;font-weight:600;"
    "letter-spacing:0.15em;color:#c9a84c;text-transform:uppercase;"
)
_SCORE_VALUE_STYLE = (
    "display:block;width:100%;text-align:center;"
    "font-size:2rem;font-weight:600;color:#e8d5a3;padding:0.2rem 0;"
)


def _score_group(faction: str, prefix: str) -> None:
    vp = st.session_state.vp[faction]
    cp = st.session_state.cp[faction]

    vp_col, cp_col = st.columns(2)

    with vp_col:
        st.markdown(f'<div style="{_SCORE_LABEL_STYLE}">VP</div>', unsafe_allow_html=True)
        if st.button("▲", key=f"{prefix}_vp_up", use_container_width=True):
            adjust_vp(faction, 1)
            st.rerun()
        st.markdown(f'<div style="{_SCORE_VALUE_STYLE}">{vp}</div>', unsafe_allow_html=True)
        if st.button("▼", key=f"{prefix}_vp_dn", use_container_width=True):
            adjust_vp(faction, -1)
            st.rerun()

    with cp_col:
        st.markdown(f'<div style="{_SCORE_LABEL_STYLE}">CP</div>', unsafe_allow_html=True)
        if st.button("▲", key=f"{prefix}_cp_up", use_container_width=True):
            adjust_cp(faction, 1)
            st.rerun()
        st.markdown(f'<div style="{_SCORE_VALUE_STYLE}">{cp}</div>', unsafe_allow_html=True)
        if st.button("▼", key=f"{prefix}_cp_dn", use_container_width=True):
            adjust_cp(faction, -1)
            st.rerun()


# ---------------------------------------------------------------------------
# Main layout
# ---------------------------------------------------------------------------


def _units_for(faction: str) -> list[Unit]:
    return NECRON_UNITS if faction == "Necrons" else ORK_UNITS


def _states_for(faction: str) -> dict:  # type: ignore[type-arg]
    key = "necron_units" if faction == "Necrons" else "ork_units"
    return st.session_state[key]


def main() -> None:
    st.markdown(CSS_THEME, unsafe_allow_html=True)
    init_state()

    active = st.session_state.active
    first = st.session_state.get("first_player", "Necrons")
    second = st.session_state.get("second_player", "Orks")
    phase_idx = st.session_state.phase_idx
    phase_name, phase_key = PHASES[phase_idx]

    # ── Header ───────────────────────────────────────────────────────────────
    left_hdr, center_hdr, right_hdr = st.columns([2.5, 5, 2.5], gap="medium")

    with left_hdr:
        _score_group(first, "left")

    with center_hdr:
        _, rst_c, _ = st.columns([2, 1, 2])
        with rst_c:
            if st.button("↺", key="reset_game", use_container_width=True):
                reset_game()
                st.rerun()

        round_label = "Setup" if phase_key == "setup" else f"Round {st.session_state.round}"
        st.markdown(
            f'<div style="text-align:center;font-size:1.6rem;font-weight:600;'
            f'letter-spacing:0.15em;color:#c9a84c;text-transform:uppercase;">'
            f"{round_label}</div>",
            unsafe_allow_html=True,
        )

        prev_c, phase_c, next_c = st.columns([1, 5, 1])
        with prev_c:
            prev_disabled = phase_idx == 0
            if st.button(
                "←",
                key="prev_phase",
                type="primary",
                use_container_width=True,
                disabled=prev_disabled,
            ):
                if phase_idx > 1:
                    st.session_state.phase_idx = phase_idx - 1
                else:
                    st.session_state.phase_idx = 0
                st.session_state.selected_unit = None
                st.session_state.selected_target = None
                st.rerun()
        with phase_c:
            active_label = "" if phase_key == "setup" else f" · {active} active"
            st.markdown(
                f'<div style="text-align:center;font-size:1.0rem;font-weight:600;'
                f'letter-spacing:0.1em;color:#e8d5a3;text-transform:uppercase;padding:0.25rem 0;">'
                f"{phase_name}{active_label}</div>",
                unsafe_allow_html=True,
            )
        with next_c:
            if st.button("→", key="next_phase", type="primary", use_container_width=True):
                next_phase()
                st.rerun()

    with right_hdr:
        _score_group(second, "right")

    st.divider()

    # ── Phase stepper (only during battle) ──────────────────────────────────
    if phase_key != "setup":
        battle_phases = PHASES[1:]  # skip setup
        steps_html = '<div style="display:flex;flex-wrap:wrap;gap:4px;margin-bottom:8px;">'
        for i, (pn, _) in enumerate(battle_phases):
            real_idx = i + 1
            if real_idx == phase_idx:
                steps_html += (
                    f'<span style="background:#2e2618;border:1px solid #c9a84c;border-radius:2px;'
                    f'padding:2px 8px;font-size:11px;color:#e8d5a3;letter-spacing:0.05em;">{pn}</span>'
                )
            else:
                steps_html += (
                    f'<span style="border:1px solid #2e2618;border-radius:2px;'
                    f'padding:2px 8px;font-size:11px;color:#4a3f2a;">{pn}</span>'
                )
        steps_html += "</div>"
        # render inside the center col — rebuild columns just for stepper
        _, ctr, _ = st.columns([1, 2, 1])
        with ctr:
            st.markdown(steps_html, unsafe_allow_html=True)

    # ── Three-column layout ──────────────────────────────────────────────────
    left, center, right = st.columns([1, 2, 1], gap="small")

    # First player always left, second always right
    with left:
        st.markdown(f"## {first}")
        for unit in _units_for(first):
            unit_card(unit, _states_for(first)[unit.uid], first)

    with center:
        PHASE_RENDERERS[phase_key]()
        if phase_key != "setup":
            _setup_summary()

    with right:
        st.markdown(f"## {second}")
        for unit in _units_for(second):
            unit_card(unit, _states_for(second)[unit.uid], second)
