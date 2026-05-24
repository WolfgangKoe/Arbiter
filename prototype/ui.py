import random

import streamlit as st
from engine import add_log, apply_damage, heal_unit, init_state, next_phase, reset_game
from models import NECRON_UNITS, ORK_UNITS, PHASES, UnitData

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
</style>
"""


# ---------------------------------------------------------------------------
# Unit card
# ---------------------------------------------------------------------------


def unit_card(unit: UnitData, state: dict, faction: str) -> None:  # type: ignore[type-arg]
    destroyed = state["destroyed"]
    cur = state["current_wounds"]
    total = unit.wounds * unit.count
    models = state["models"]

    with st.expander(unit.name if not destroyed else f"~~{unit.name}~~", expanded=False):
        if destroyed:
            st.caption("Einheit vernichtet.")
            return

        st.caption(unit.keywords)

        sc = st.columns(7)
        for col, lbl, val in zip(
            sc,
            ["M", "T", "Ret", "W", "FU", "LD", "OC"],
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

        if total > 0:
            st.progress(cur / total)

        c1, c2, c3, c4 = st.columns(4)
        with c1:
            if st.button("−1W", key=f"w1_{faction}_{unit.uid}"):
                apply_damage(unit.uid, faction, 1, unit)
                add_log(f"{unit.name} −1 Wunde ({state['current_wounds']-1}/{total})")
                st.rerun()
        with c2:
            if st.button("−D3", key=f"wd3_{faction}_{unit.uid}"):
                d = random.randint(1, 3)
                apply_damage(unit.uid, faction, d, unit)
                add_log(f"{unit.name} −{d} Wunden")
                st.rerun()
        with c3:
            if st.button("−D6", key=f"wd6_{faction}_{unit.uid}"):
                d = random.randint(1, 6)
                apply_damage(unit.uid, faction, d, unit)
                add_log(f"{unit.name} −{d} Wunden")
                st.rerun()
        with c4:
            if st.button("+1W", key=f"h1_{faction}_{unit.uid}"):
                heal_unit(unit.uid, faction, 1, unit)
                add_log(f"{unit.name} +1 Wunde geheilt")
                st.rerun()

        st.caption("**Waffen:**")
        for w in unit.weapons:
            icon = "Nah" if w.is_melee else "Fern"
            ap_str = f"AP{w.ap}" if w.ap != 0 else "AP0"
            st.caption(
                f"[{icon}] **{w.name}** · A{w.attacks} · "
                f"{'WS' if w.is_melee else 'BS'}{w.skill}+ · S{w.strength} · "
                f"{ap_str} · D{w.damage}" + (f" · _{w.abilities}_" if w.abilities else "")
            )

        if unit.abilities:
            st.caption(f"*{unit.abilities}*")


# ---------------------------------------------------------------------------
# Phase renderers
# ---------------------------------------------------------------------------


_PHASE_INFO = {
    "command": "Erhalte 1 Befehlspunkt. Aktiviere Fähigkeiten. Nutze Strategeme.",
    "movement": 'Bewege Einheiten bis zu ihrem M-Wert. Vorstoßen: +D6", kein Schießen/Sturm danach.',
    "psychic": "Psyker wirken Kräfte: 2W6 ≥ Psi-Stärke. Gegner kann mit 2W6 abwehren.",
    "shooting": "Wähle Einheit → Waffe → Ziel. Treffer (BS) → Verwundung (S vs T) → Rettung (SV−AP) → Schaden.",
    "charge": 'Erkläre Sturm gegen Ziel ≤ 12". Würfle 2W6: Ergebnis ≥ Entfernung = Sturm erfolgreich.',
    "fight": "Gestürmte Einheiten kämpfen zuerst. Beide Seiten kämpfen. WS-Treffer → Verwundung → Rettung → Schaden.",
    "morale": "Einheiten mit Verlusten: W6 + verbleibende Modelle ≥ Führungswert, sonst Modelle entfernen.",
}


def _phase_placeholder(key: str) -> None:
    st.info(_PHASE_INFO[key])


def phase_command() -> None:
    _phase_placeholder("command")


def phase_movement() -> None:
    _phase_placeholder("movement")


def phase_psychic() -> None:
    _phase_placeholder("psychic")


def phase_shooting() -> None:
    _phase_placeholder("shooting")


def phase_charge() -> None:
    _phase_placeholder("charge")


def phase_fight() -> None:
    _phase_placeholder("fight")


def phase_morale() -> None:
    _phase_placeholder("morale")


PHASE_RENDERERS = {
    "command": phase_command,
    "movement": phase_movement,
    "psychic": phase_psychic,
    "shooting": phase_shooting,
    "charge": phase_charge,
    "fight": phase_fight,
    "morale": phase_morale,
}


# ---------------------------------------------------------------------------
# Main layout
# ---------------------------------------------------------------------------


def main() -> None:
    st.markdown(CSS_THEME, unsafe_allow_html=True)
    init_state()

    # ── Header ──────────────────────────────────────────────────────────────
    st.markdown(
        f"""
        <div style="
            display:grid;
            grid-template-columns:1fr auto 1fr;
            align-items:center;
            background:#1c1a14;
            border-bottom:1px solid #2e2618;
            padding:0.75rem 1.5rem;
            margin-bottom:1rem;
            gap:1rem;
        ">
            <div style="display:flex;align-items:center;gap:0.75rem;">
                <span style="font-size:0.65rem;letter-spacing:0.1em;color:#6b5f44;text-transform:uppercase;">VP</span>
                <span style="font-size:1.25rem;font-weight:600;color:#e8d5a3;">{st.session_state.vp["Necrons"]}</span>
                <span style="font-size:0.65rem;letter-spacing:0.1em;color:#6b5f44;text-transform:uppercase;">CP</span>
                <span style="font-size:1.25rem;font-weight:600;color:#e8d5a3;">{st.session_state.cp["Necrons"]}</span>
                <span style="font-size:0.8rem;color:#b0a080;margin-left:0.25rem;">Necrons</span>
            </div>
            <div style="text-align:center;">
                <div style="font-size:1.6rem;font-weight:600;letter-spacing:0.15em;color:#c9a84c;text-transform:uppercase;">
                    Runde {st.session_state.round}
                </div>
                <div style="font-size:1.1rem;font-weight:600;letter-spacing:0.1em;color:#e8d5a3;text-transform:uppercase;">
                    {PHASES[st.session_state.phase_idx][0]} · {st.session_state.active}
                </div>
            </div>
            <div style="display:flex;align-items:center;gap:0.75rem;justify-content:flex-end;">
                <span style="font-size:0.8rem;color:#b0a080;margin-right:0.25rem;">Orks</span>
                <span style="font-size:0.65rem;letter-spacing:0.1em;color:#6b5f44;text-transform:uppercase;">VP</span>
                <span style="font-size:1.25rem;font-weight:600;color:#e8d5a3;">{st.session_state.vp["Orks"]}</span>
                <span style="font-size:0.65rem;letter-spacing:0.1em;color:#6b5f44;text-transform:uppercase;">CP</span>
                <span style="font-size:1.25rem;font-weight:600;color:#e8d5a3;">{st.session_state.cp["Orks"]}</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # ── Three-column layout ──────────────────────────────────────────────────
    left, center, right = st.columns([1, 2, 1], gap="small")

    # ── LEFT: Necrons ────────────────────────────────────────────────────────
    with left:
        st.markdown("## Necrons")
        for unit in NECRON_UNITS:
            unit_card(unit, st.session_state.necron_units[unit.uid], "Necrons")

    # ── CENTER: Phases ───────────────────────────────────────────────────────
    with center:
        phase_name, phase_key = PHASES[st.session_state.phase_idx]

        steps_html = '<div style="display:flex;flex-wrap:wrap;gap:4px;margin-bottom:8px;">'
        for i, (pn, _) in enumerate(PHASES):
            if i == st.session_state.phase_idx:
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
        st.markdown(steps_html, unsafe_allow_html=True)

        PHASE_RENDERERS[phase_key]()

        st.divider()
        nav1, nav2, nav3 = st.columns(3)
        with nav1:
            if st.button("← Vorherige Phase", key="prev_phase"):
                st.session_state.phase_idx = max(0, st.session_state.phase_idx - 1)
                st.rerun()
        with nav2:
            if st.button("Spiel zurücksetzen", key="reset_game"):
                reset_game()
                st.rerun()
        with nav3:
            if st.button("Nächste Phase →", key="next_phase", type="primary"):
                next_phase()
                st.rerun()

        st.divider()
        st.markdown(
            '<span style="font-size:0.65rem;letter-spacing:0.1em;color:#6b5f44;text-transform:uppercase;">Kampfprotokoll</span>',
            unsafe_allow_html=True,
        )
        log_text = "\n".join(reversed(st.session_state.battle_log[-25:]))
        st.text_area(
            "",
            value=log_text,
            height=200,
            disabled=True,
            key="log_area",
            label_visibility="collapsed",
        )

    # ── RIGHT: Orks ──────────────────────────────────────────────────────────
    with right:
        st.markdown("## Orks")
        for unit in ORK_UNITS:
            unit_card(unit, st.session_state.ork_units[unit.uid], "Orks")
