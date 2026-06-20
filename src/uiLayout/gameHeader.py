"""gameHeader — CSS injection, VP/CP steppers, round/phase navigation."""

import streamlit as st

from gameMechanic.game_state import PHASES, next_phase, reset_game
from uiLayout._common import reset_group_declaration_state

CSS_THEME = """
<style>
/* ── Imperial Gothic Theme ──────────────────────────────────────────── */
:root {
    --arb-bg:        #0f0e0c;
    --arb-surface:   #1c1a14;
    --arb-border:    #2e2618;
    --arb-accent:    #d4a017;
    --arb-accent-lt: #fbbf24;
    --arb-muted:     #6b5f44;
    --arb-text:      #e7e5e4;
    --arb-unit:      #a8a29e;
    --arb-hover:     #2a2316;
    --arb-red:       #991b1b;
    --arb-btn:       #7a5810;
    --arb-green:     #166534;
    --arb-blue:      #1e3a8a;
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

/* Resolution tabs — visible separation, slimmer chrome (6n D4) */
[data-testid="stTabs"] [data-testid="stTab"] {
    border-right: 1px solid var(--arb-border);
    padding: 2px 10px;
}
[data-testid="stTabs"] [data-testid="stTab"]:last-of-type {
    border-right: none;
}

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

/* Expanders */
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

/* Bordered containers (st.container(border=True)) — armyCard, unitCard
   Streamlit 1.57 uses Emotion class e1rw0b1u3 for all flex containers.
   border-color only affects elements that already have border-style:solid
   set by Emotion (border=True); non-bordered containers stay unaffected. */
.e1rw0b1u3 {
    border-color: var(--arb-border) !important;
    border-left-color: var(--arb-accent) !important;
}

/* Buttons — Streamlit 1.57 uses data-testid="stBaseButton-{kind}" */
.stButton > button {
    background: var(--arb-surface) !important;
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
button[data-testid="stBaseButton-primary"] {
    background: var(--arb-accent) !important;
    border-color: var(--arb-accent) !important;
    color: var(--arb-bg) !important;
    font-weight: 700;
}
button[data-testid="stBaseButton-primary"]:hover {
    background: var(--arb-accent-lt) !important;
    border-color: var(--arb-accent-lt) !important;
}
button[data-testid="stBaseButton-secondary"] {
    background: var(--arb-surface) !important;
    border-color: var(--arb-btn) !important;
    color: var(--arb-accent-lt) !important;
}
button[data-testid="stBaseButton-secondary"]:hover {
    background: var(--arb-hover) !important;
    border-color: var(--arb-accent) !important;
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
[data-testid="stNumberInputContainer"] {
    background: var(--arb-surface) !important;
    border: 1px solid var(--arb-border) !important;
    border-radius: 2px !important;
}
[data-testid="stNumberInputStepUp"],
[data-testid="stNumberInputStepDown"] {
    background: var(--arb-surface) !important;
    background-color: var(--arb-surface) !important;
    color: var(--arb-muted) !important;
}
[data-testid="stNumberInputStepUp"]:hover:enabled,
[data-testid="stNumberInputStepDown"]:hover:enabled {
    background: var(--arb-hover) !important;
    background-color: var(--arb-hover) !important;
    color: var(--arb-accent-lt) !important;
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

_SCORE_NUM = "font-size:4.5rem;font-weight:700;color:#fbbf24;line-height:1.0;"
_SCORE_LBL = "font-size:4.5rem;font-weight:700;color:#6b5f44;margin-left:6px;letter-spacing:0.1em;line-height:1.0;"


def _score_group(faction: str, justify: str = "center") -> None:
    vp = st.session_state.vp[faction]
    cp = st.session_state.cp[faction]
    st.markdown(
        f'<div style="display:flex;gap:40px;align-items:baseline;justify-content:{justify};">'
        f'<span><span style="{_SCORE_NUM}">{vp}</span><span style="{_SCORE_LBL}">VP</span></span>'
        f'<span><span style="{_SCORE_NUM}">{cp}</span><span style="{_SCORE_LBL}">CP</span></span>'
        f"</div>",
        unsafe_allow_html=True,
    )


def _phase_badges_html(phase_idx: int) -> str:
    battle_phases = PHASES[1:]  # skip setup
    html = '<div style="display:flex;flex-wrap:wrap;gap:4px;justify-content:center;">'
    for i, (pn, _) in enumerate(battle_phases):
        real_idx = i + 1
        if real_idx == phase_idx:
            html += (
                f'<span style="background:#2e2618;border:2px solid #d4a017;border-radius:2px;'
                f'padding:5px 16px;font-size:13px;color:#fbbf24;letter-spacing:0.07em;font-weight:700;">{pn}</span>'
            )
        else:
            html += (
                f'<span style="background:#1c1a14;border:1px solid #2e2618;border-radius:2px;'
                f'padding:5px 16px;font-size:13px;color:#6b5f44;">{pn}</span>'
            )
    html += "</div>"
    return html


def render_game_header() -> None:
    first = st.session_state.get("first_player", "Player 1")
    second = st.session_state.get("second_player", "Player 2")
    phase_idx = st.session_state.phase_idx
    phase_name, phase_key = PHASES[phase_idx]
    active = st.session_state.active

    # ── Zeile 1: Rundenanzeige ────────────────────────────────────────────────
    round_label = "Setup" if phase_key == "setup" else f"Round {st.session_state.round}"
    st.markdown(
        f'<div style="text-align:center;font-size:1.6rem;font-weight:600;'
        f'letter-spacing:0.15em;color:#d4a017;text-transform:uppercase;margin-bottom:2px;">'
        f"{round_label}</div>",
        unsafe_allow_html=True,
    )

    # ── Zeile 2: Phase · Armeename des aktiven Spielers ───────────────────────
    st.markdown(
        f'<div style="text-align:center;font-size:1.0rem;font-weight:600;'
        f'letter-spacing:0.1em;color:#fbbf24;text-transform:uppercase;margin-bottom:6px;">'
        f"{phase_name} · {active}</div>",
        unsafe_allow_html=True,
    )

    # ── Zeile 3: Scores | Phase-Badges | Scores ───────────────────────────────
    left_col, center_col, right_col = st.columns([2.5, 5, 2.5], gap="medium")
    with left_col:
        _score_group(first, justify="flex-start")
    with center_col:
        if phase_key != "setup":
            st.markdown(_phase_badges_html(phase_idx), unsafe_allow_html=True)
    with right_col:
        _score_group(second, justify="flex-end")

    # ── Zeile 4: Navigationsbuttons (nur im Kampf) ────────────────────────────
    if phase_key != "setup":
        _, prev_c, rst_c, next_c, _ = st.columns([2, 1, 1, 1, 2])
        with prev_c:
            if st.button(
                "←",
                key="prev_phase",
                type="primary",
                use_container_width=True,
                disabled=phase_idx <= 1,
            ):
                st.session_state.phase_idx = phase_idx - 1
                st.session_state.selected_unit = None
                st.session_state.selected_targets = []
                reset_group_declaration_state()
                st.rerun()
        with rst_c:
            if st.button("↺", key="reset_game", use_container_width=True):
                reset_game()
                st.rerun()
        with next_c:
            if st.button("→", key="next_phase", type="primary", use_container_width=True):
                next_phase()
                st.rerun()
