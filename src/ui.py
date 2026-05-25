import streamlit as st

from engine import adjust_cp, adjust_vp, apply_damage, heal_unit, init_state, next_phase, reset_game
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
# Unit card
# ---------------------------------------------------------------------------


def unit_card(unit: Unit, state: dict, faction: str) -> None:  # type: ignore[type-arg]
    destroyed = state["destroyed"]
    cur = state["current_wounds"]
    total = unit.wounds * unit.count

    with st.expander(unit.name if not destroyed else f"~~{unit.name}~~", expanded=False):
        if destroyed:
            st.caption("Einheit vernichtet.")
            return

        # Keywords: Fraktion (oben) und Typ (darunter), getrennt
        if unit.faction_keywords:
            st.caption(" · ".join(unit.faction_keywords))
        if unit.other_keywords:
            st.caption(
                '<span style="color:#4a3f2a;font-size:0.65rem;">'
                + " · ".join(unit.other_keywords)
                + "</span>",
                unsafe_allow_html=True,
            )

        # Einheitenprofil – Standard-40k-Abkürzungen
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

        # Lebenspunkte-Balken
        if total > 0:
            st.progress(cur / total)

        # Schaden-Buttons: einfaches +1 / −1
        col_dmg, col_heal = st.columns(2)
        with col_dmg:
            if st.button("−1 W", key=f"dmg_{faction}_{unit.uid}"):
                apply_damage(unit.uid, faction, 1, unit)
                st.rerun()
        with col_heal:
            if st.button("+1 W", key=f"heal_{faction}_{unit.uid}"):
                heal_unit(unit.uid, faction, 1, unit)
                st.rerun()

        # Waffenprofil
        st.caption("**Waffen:**")
        for w in unit.weapons:
            kind = "NK" if w.is_melee else "FK"
            ap_str = f"AP{w.ap}" if w.ap != 0 else "AP0"
            st.caption(
                f"[{kind}] **{w.name}** · A{w.attacks} · "
                f"{'WS' if w.is_melee else 'BS'}{w.skill}+ · S{w.strength} · "
                f"{ap_str} · D{w.damage}" + (f" · _{w.abilities}_" if w.abilities else "")
            )

        # Sonderregeln
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


_SCORE_LABEL_STYLE = (
    "display:block;width:100%;text-align:center;font-size:1.6rem;font-weight:600;"
    "letter-spacing:0.15em;color:#c9a84c;text-transform:uppercase;"
)
_SCORE_VALUE_STYLE = (
    "display:block;width:100%;text-align:center;"
    "font-size:2rem;font-weight:600;color:#e8d5a3;padding:0.2rem 0;"
)


def _score_group(faction: str, prefix: str) -> None:
    """VP- und CP-Steuerung: Label oben, dann ▲ · Zahl · ▼ je Spalte."""
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


def main() -> None:
    st.markdown(CSS_THEME, unsafe_allow_html=True)
    init_state()

    # ── Header: [Score Necrons] [Mitte] [Score Orks] ─────────────────────────
    left_hdr, center_hdr, right_hdr = st.columns([2.5, 5, 2.5], gap="medium")

    with left_hdr:
        _score_group("Necrons", "nc")

    with center_hdr:
        # Reset oben mittig
        _, rst_c, _ = st.columns([2, 1, 2])
        with rst_c:
            if st.button("↺", key="reset_game", use_container_width=True):
                reset_game()
                st.rerun()

        # Runde
        st.markdown(
            f'<div style="text-align:center;font-size:1.6rem;font-weight:600;'
            f'letter-spacing:0.15em;color:#c9a84c;text-transform:uppercase;">'
            f"Runde {st.session_state.round}</div>",
            unsafe_allow_html=True,
        )

        # ← Phase · Fraktion →
        phase_name, _ = PHASES[st.session_state.phase_idx]
        prev_c, phase_c, next_c = st.columns([1, 5, 1])
        with prev_c:
            if st.button("←", key="prev_phase", type="primary", use_container_width=True):
                st.session_state.phase_idx = max(0, st.session_state.phase_idx - 1)
                st.rerun()
        with phase_c:
            st.markdown(
                f'<div style="text-align:center;font-size:1.0rem;font-weight:600;'
                f'letter-spacing:0.1em;color:#e8d5a3;text-transform:uppercase;padding:0.25rem 0;">'
                f"{phase_name} · {st.session_state.active}</div>",
                unsafe_allow_html=True,
            )
        with next_c:
            if st.button("→", key="next_phase", type="primary", use_container_width=True):
                next_phase()
                st.rerun()

    with right_hdr:
        _score_group("Orks", "ok")

    st.divider()

    # ── Drei-Spalten-Layout ──────────────────────────────────────────────────
    left, center, right = st.columns([1, 2, 1], gap="small")

    # ── LINKS: Necrons ───────────────────────────────────────────────────────
    with left:
        st.markdown("## Necrons")
        for unit in NECRON_UNITS:
            unit_card(unit, st.session_state.necron_units[unit.uid], "Necrons")

    # ── MITTE: Phasen ────────────────────────────────────────────────────────
    with center:
        _, phase_key = PHASES[st.session_state.phase_idx]

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

    # ── RECHTS: Orks ─────────────────────────────────────────────────────────
    with right:
        st.markdown("## Orks")
        for unit in ORK_UNITS:
            unit_card(unit, st.session_state.ork_units[unit.uid], "Orks")
