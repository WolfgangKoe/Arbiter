"""gameHeader — CSS injection, VP/CP steppers, round/phase navigation."""

import streamlit as st

from gameMechanic.game_state import PHASES, next_phase, reset_game

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
.stButton > button[data-testid="baseButton-primary"],
.stButton > button[kind="primary"] {
    background: var(--arb-accent) !important;
    border-color: var(--arb-accent) !important;
    color: var(--arb-bg) !important;
    font-weight: 700;
}
.stButton > button[data-testid="baseButton-primary"]:hover,
.stButton > button[kind="primary"]:hover {
    background: var(--arb-accent-lt) !important;
    border-color: var(--arb-accent-lt) !important;
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

_LABEL_STYLE = (
    "display:block;width:100%;text-align:center;font-size:0.65rem;font-weight:600;"
    "letter-spacing:0.15em;color:#6b5f44;text-transform:uppercase;margin-bottom:2px;"
)
_VALUE_STYLE = (
    "display:block;width:100%;text-align:center;"
    "font-size:2rem;font-weight:600;color:#fbbf24;line-height:1.1;"
)


def _score_group(faction: str) -> None:
    vp = st.session_state.vp[faction]
    cp = st.session_state.cp[faction]

    vp_col, cp_col = st.columns(2)

    with vp_col:
        st.markdown(
            f'<div style="{_LABEL_STYLE}">VP</div>' f'<div style="{_VALUE_STYLE}">{vp}</div>',
            unsafe_allow_html=True,
        )

    with cp_col:
        st.markdown(
            f'<div style="{_LABEL_STYLE}">CP</div>' f'<div style="{_VALUE_STYLE}">{cp}</div>',
            unsafe_allow_html=True,
        )


def render_game_header() -> None:
    st.markdown(CSS_THEME, unsafe_allow_html=True)

    first = st.session_state.get("first_player", "Necrons")
    second = st.session_state.get("second_player", "Orks")
    phase_idx = st.session_state.phase_idx
    phase_name, phase_key = PHASES[phase_idx]
    active = st.session_state.active

    left_hdr, center_hdr, right_hdr = st.columns([2.5, 5, 2.5], gap="medium")

    with left_hdr:
        _score_group(first)

    with center_hdr:
        round_label = "Setup" if phase_key == "setup" else f"Round {st.session_state.round}"
        st.markdown(
            f'<div style="text-align:center;font-size:1.6rem;font-weight:600;'
            f'letter-spacing:0.15em;color:#d4a017;text-transform:uppercase;">'
            f"{round_label}</div>",
            unsafe_allow_html=True,
        )

        if phase_key == "setup":
            # During setup: only show phase label, no navigation or reset.
            st.markdown(
                f'<div style="text-align:center;font-size:1.0rem;font-weight:600;'
                f'letter-spacing:0.1em;color:#fbbf24;text-transform:uppercase;padding:0.25rem 0;">'
                f"{phase_name}</div>",
                unsafe_allow_html=True,
            )
        else:
            _, rst_c, _ = st.columns([2, 1, 2])
            with rst_c:
                if st.button("↺", key="reset_game", use_container_width=True):
                    reset_game()
                    st.rerun()

            prev_c, phase_c, next_c = st.columns([1, 5, 1])
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
                    st.rerun()
            with phase_c:
                st.markdown(
                    f'<div style="text-align:center;font-size:1.0rem;font-weight:600;'
                    f'letter-spacing:0.1em;color:#fbbf24;text-transform:uppercase;padding:0.25rem 0;">'
                    f"{phase_name} · {active} active</div>",
                    unsafe_allow_html=True,
                )
            with next_c:
                if st.button("→", key="next_phase", type="primary", use_container_width=True):
                    next_phase()
                    st.rerun()

    with right_hdr:
        _score_group(second)

    # Phase stepper chips (only during battle)
    if phase_key != "setup":
        battle_phases = PHASES[1:]  # skip setup
        steps_html = '<div style="display:flex;flex-wrap:wrap;gap:4px;margin-bottom:8px;">'
        for i, (pn, _) in enumerate(battle_phases):
            real_idx = i + 1
            if real_idx == phase_idx:
                steps_html += (
                    f'<span style="background:#2e2618;border:1px solid #d4a017;border-radius:2px;'
                    f'padding:2px 8px;font-size:11px;color:#fbbf24;letter-spacing:0.05em;">{pn}</span>'
                )
            else:
                steps_html += (
                    f'<span style="background:#1c1a14;border:1px solid #2e2618;border-radius:2px;'
                    f'padding:2px 8px;font-size:11px;color:#6b5f44;">{pn}</span>'
                )
        steps_html += "</div>"
        _, ctr, _ = st.columns([1, 2, 1])
        with ctr:
            st.markdown(steps_html, unsafe_allow_html=True)
