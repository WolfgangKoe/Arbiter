"""armyCard — Army header: faction badges + triggered army-wide ability buttons.

Design (see docs/spec/ui_layout.md §3):
- Thin border wrapping the whole card.
- Faction keyword badge + subfaction keyword badge.
- Triggered abilities: button shown only when current phase and conditions match.
  Clicking the button invokes the existing ability mechanism.
- Activated abilities (e.g. unit-specific commands) are NOT shown here;
  they appear in gameActionsArea when the relevant unit is selected.
"""

from __future__ import annotations

import streamlit as st

from gameMechanic.ability_engine import check_conditions, execute_effect
from gameMechanic.game_log import log_action
from gameMechanic.game_state import PHASES, faction_dir_for, unit_id_from_state_key
from gameObjects.ability import Ability
from gameObjects.loader import load_command_protocols
from gameObjects.unit import Unit

_ETERNAL_GUARDIAN_ID = "wh40k_9e.necrons.protocol.eternal_guardian"


def _faction_badge(text: str) -> str:
    return (
        f'<span style="background:#1a1a2e;border:1px solid #4a4a8a;border-radius:2px;'
        f"padding:2px 8px;font-size:10px;color:#9090d0;letter-spacing:0.07em;"
        f'font-weight:700;margin-right:4px;">{text}</span>'
    )


def _current_phase_key() -> str:
    return PHASES[st.session_state.phase_idx][1]


def _ability_matches_phase(ability: Ability, phase_key: str) -> bool:
    phases = ability.trigger.phase
    if isinstance(phases, list):
        return phase_key in phases
    return phases == phase_key


def _render_triggered_abilities(
    faction: str,
    faction_abilities: list[Ability],
    units: list[Unit],
    units_state: dict,  # type: ignore[type-arg]
    phase_key: str,
) -> None:
    is_active = faction == st.session_state.active
    triggered = [
        a
        for a in faction_abilities
        if a.ability_type == "triggered" and _ability_matches_phase(a, phase_key)
    ]
    if not triggered:
        return

    unit_by_id = {u.id: u for u in units}

    for ability in triggered:
        if ability.effect.type == "reanimate":
            st.caption(f"{ability.name_en} — triggers after enemy attacks")
            continue

        eligible = [
            state_key
            for state_key, ustate in units_state.items()
            if (unit := unit_by_id.get(unit_id_from_state_key(state_key))) is not None
            and check_conditions(ability, unit, ustate)
        ]
        if not eligible:
            st.caption(f"{ability.name_en} — no units eligible")
            continue

        n = len(eligible)
        st.caption(f"{ability.name_en} — {n} unit{'s' if n > 1 else ''} eligible")
        if is_active and st.button(
            f"Apply {ability.name_en}",
            key=f"army_triggered_{ability.id}",
            use_container_width=True,
        ):
            applied = sum(
                1
                for sk in eligible
                if execute_effect(ability, sk, faction, unit_by_id[unit_id_from_state_key(sk)])
            )
            log_action(
                st.session_state.round,
                phase_key,
                faction,
                f"{ability.name_en}: {applied} unit(s) healed",
            )
            st.rerun()


def _render_directive_buttons(protocol, faction: str, round_num: int) -> None:
    """Show Primary / Secondary directive selection buttons for the active protocol."""
    st.caption(f"↳ **Primary:** {protocol.primary}")
    st.caption(f"↳ **Secondary:** {protocol.secondary}")
    col_p, col_s = st.columns(2)
    if col_p.button(
        "Use Primary",
        key=f"cmd_directive_primary_{faction}_{round_num}",
        use_container_width=True,
    ):
        st.session_state.active_directive = "primary"
        st.rerun()
    if col_s.button(
        "Use Secondary",
        key=f"cmd_directive_secondary_{faction}_{round_num}",
        use_container_width=True,
    ):
        st.session_state.active_directive = "secondary"
        st.rerun()


def _render_protocol_ui(faction: str) -> None:
    """Command Protocol UI — only for factions with command_protocols.yaml (i.e. Necrons).

    During command phase: interactive selection. All other phases: read-only current protocol.
    """
    try:
        faction_dir = faction_dir_for(faction)
    except KeyError:
        return

    protocols = load_command_protocols(faction_dir)
    if not protocols:
        return

    phase_key = _current_phase_key()
    active_id = st.session_state.get("active_protocol_id")
    used_ids = st.session_state.get("used_protocol_ids", [])
    current_round = st.session_state.get("round", 1)

    st.divider()
    st.caption("**Command Protocols**")

    active_directive: str | None = st.session_state.get("active_directive")

    if current_round == 1:
        p = next((p for p in protocols if p.id == _ETERNAL_GUARDIAN_ID), None)
        if p:
            # Auto-activate Eternal Guardian for round 1
            if not active_id:
                st.session_state.active_protocol_id = _ETERNAL_GUARDIAN_ID
                active_id = _ETERNAL_GUARDIAN_ID
            st.caption(f"{p.name_en} — auto (Round 1)")
            if not active_directive:
                _render_directive_buttons(p, faction, current_round)
            else:
                chosen_text = p.primary if active_directive == "primary" else p.secondary
                st.caption(f"↳ **{active_directive.capitalize()}:** {chosen_text}")
        return

    if active_id:
        p = next((p for p in protocols if p.id == active_id), None)
        if p:
            st.caption(f"**{p.name_en}** — active this round")
            if not active_directive:
                _render_directive_buttons(p, faction, current_round)
            else:
                chosen_text = p.primary if active_directive == "primary" else p.secondary
                st.caption(f"↳ **{active_directive.capitalize()}:** {chosen_text}")
        return

    if phase_key != "command":
        st.caption("— no protocol selected —")
        return

    # Interactive selection — only available in command phase when no protocol is active yet
    available = [p for p in protocols if p.id not in used_ids]
    if not available:
        st.caption("All protocols have been used.")
        return

    choice = st.radio(
        "Choose protocol:",
        options=range(len(available)),
        format_func=lambda i: available[i].name_en,
        key=f"cmd_protocol_choice_{faction}",
    )
    if st.button(
        "Activate Protocol",
        key=f"cmd_protocol_activate_{faction}",
        type="primary",
        use_container_width=True,
    ):
        chosen = available[choice]
        st.session_state.active_protocol_id = chosen.id
        st.session_state.used_protocol_ids = used_ids + [chosen.id]
        st.session_state.active_directive = None
        log_action(current_round, "command", faction, f"Protocol: {chosen.name_en}")
        st.rerun()


def render_army_card(
    faction: str,
    subfaction: str | None,
    faction_abilities: list[Ability],
    units: list[Unit],
    units_state: dict,  # type: ignore[type-arg]
) -> None:
    phase_key = _current_phase_key()

    with st.container(border=True):
        army_name = f"{faction}" + (f" — {subfaction}" if subfaction else "")
        st.markdown(f"**{army_name}**")

        # Faction keyword badges
        badges_html = _faction_badge(faction)
        if subfaction:
            badges_html += _faction_badge(subfaction)
        st.markdown(badges_html, unsafe_allow_html=True)

        # Command Protocol UI (Necrons only — other factions: no-op)
        _render_protocol_ui(faction)

        # Triggered ability buttons (phase-dependent)
        _render_triggered_abilities(faction, faction_abilities, units, units_state, phase_key)
