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
from gameObjects.loader import load_command_protocols, load_round_choice_label
from gameObjects.unit import Unit


def _faction_badge(text: str) -> str:
    return (
        f'<span style="background:#1a1a2e;border:1px solid #4a4a8a;border-radius:2px;'
        f"padding:2px 8px;font-size:10px;color:#9090d0;letter-spacing:0.07em;"
        f'font-weight:700;margin-right:4px;">{text}</span>'
    )


def _active_ability_badge(text: str, *, color: str = "protocol") -> str:
    """HTML badge for an active faction ability (protocol, waaagh, etc.)."""
    if color == "waaagh_1":
        fg, bg = "#4ade80", "#052e16"
    elif color == "waaagh_2":
        fg, bg = "#86efac", "#071a0e"
    else:  # protocol
        fg, bg = "#fbbf24", "#1c1007"
    return (
        f'<span style="background:{bg};border:1px solid {fg};border-radius:2px;'
        f"padding:2px 8px;font-size:10px;color:{fg};letter-spacing:0.07em;"
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
    """Command Protocol UI — only for factions with command_protocols.yaml.

    Only the active player may select/change protocols. The inactive player
    sees read-only status only.
    """
    try:
        faction_dir = faction_dir_for(faction)
    except KeyError:
        return

    protocols = load_command_protocols(faction_dir)
    if not protocols:
        return

    phase_key = _current_phase_key()
    is_active = faction == st.session_state.get("active")
    active_id = st.session_state.get("active_protocol_id")
    used_ids = st.session_state.get("used_protocol_ids", [])
    current_round = st.session_state.get("round", 1)

    st.divider()
    label = load_round_choice_label(faction_dir)
    st.caption(f"**{label}**")

    active_directive: str | None = st.session_state.get("active_directive")

    if current_round == 1:
        auto_protocol = next((p for p in protocols if p.auto_round_1), None)
        if auto_protocol:
            if not active_id:
                st.session_state.active_protocol_id = auto_protocol.id
                active_id = auto_protocol.id
            if not active_directive:
                st.caption(f"{auto_protocol.name_en} — auto (Round 1)")
                if is_active:
                    _render_directive_buttons(auto_protocol, faction, current_round)
                else:
                    st.caption("↳ *Awaiting directive selection*")
            else:
                badge_text = f"{auto_protocol.name_en.upper()} — {active_directive.upper()}"
                st.markdown(_active_ability_badge(badge_text), unsafe_allow_html=True)
                chosen_text = (
                    auto_protocol.primary
                    if active_directive == "primary"
                    else auto_protocol.secondary
                )
                st.caption(f"↳ {chosen_text}")
            return

    if active_id:
        p = next((p for p in protocols if p.id == active_id), None)
        if p:
            if not active_directive:
                st.caption(f"**{p.name_en}** — active this round")
                if is_active:
                    _render_directive_buttons(p, faction, current_round)
                else:
                    st.caption("↳ *Awaiting directive selection*")
            else:
                badge_text = f"{p.name_en.upper()} — {active_directive.upper()}"
                st.markdown(_active_ability_badge(badge_text), unsafe_allow_html=True)
                chosen_text = p.primary if active_directive == "primary" else p.secondary
                st.caption(f"↳ {chosen_text}")
        return

    if phase_key != "command" or not is_active:
        st.caption("— no protocol selected —")
        return

    # Interactive selection — active player, command phase, no protocol yet
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


def _render_waaagh_ui(
    faction: str,
    faction_abilities: list[Ability],
    units: list[Unit],
) -> None:
    """Command-phase faction ability UI for factions with once-per-battle activations (WAAAGH! etc.).

    Generic: reads command-phase activated abilities from the passed faction_abilities list.
    No-ops silently for factions without such abilities (Necrons, Space Marines, etc.).
    """
    command_activated = [
        a
        for a in faction_abilities
        if a.ability_type == "activated" and _ability_matches_phase(a, "command")
    ]
    if not command_activated:
        return

    try:
        faction_dir = faction_dir_for(faction)
    except KeyError:
        return

    # Necrons use command protocols instead — don't double-render
    if load_command_protocols(faction_dir):
        return

    phase_key = _current_phase_key()
    current_round = st.session_state.get("round", 1)
    is_active = faction == st.session_state.get("active")
    waaagh_state: dict = st.session_state.get("waaagh_state", {})
    player_ws = waaagh_state.get(faction)

    st.divider()

    if player_ws:
        stage = player_ws.get("stage", 1)
        color = "waaagh_1" if stage == 1 else "waaagh_2"
        badge_text = f"WAAAGH! — STAGE {stage}"
        st.markdown(_active_ability_badge(badge_text, color=color), unsafe_allow_html=True)
        if stage == 1:
            st.caption("↳ +1 Strength · +1 Attacks · 5+ invuln · Advance & Charge")
        else:
            st.caption("↳ +1 Strength · +1 Attacks · 6+ invuln")
        return

    # WAAAGH! not called yet
    if not is_active or phase_key != "command":
        st.caption("— WAAAGH! not called —")
        return

    # Require WARBOSS (or SPEEDBOSS / GHAZGHKULL THRAKA) on the battlefield
    waaagh_ability = next(
        (a for a in command_activated if "waaagh" in a.id.lower() and "speed" not in a.id.lower()),
        None,
    )
    has_warboss = any(u.has_keyword("WARBOSS") for u in units)

    if waaagh_ability and has_warboss:
        st.caption("**WAAAGH!** — call once per battle (requires WARBOSS)")
        if st.button(
            "Call Da WAAAGH!",
            key=f"waaagh_call_{faction}",
            type="primary",
            use_container_width=True,
        ):
            waaagh_state[faction] = {"stage": 1, "round_activated": current_round}
            st.session_state.waaagh_state = waaagh_state
            log_action(current_round, "command", faction, "WAAAGH! called — Stage 1 active")
            st.rerun()
    else:
        st.caption("— WAAAGH! not available (no WARBOSS) —")


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

        # Command Protocol UI (Necrons — no-op for other factions)
        _render_protocol_ui(faction)

        # Once-per-battle command-phase faction abilities (WAAAGH! etc. — no-op for Necrons)
        _render_waaagh_ui(faction, faction_abilities, units)

        # Triggered ability buttons (phase-dependent)
        _render_triggered_abilities(faction, faction_abilities, units, units_state, phase_key)
