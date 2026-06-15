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
from gameObjects.loader import load_round_choice_abilities, load_round_choice_label
from gameObjects.unit import Unit


def _faction_badge(text: str) -> str:
    return (
        f'<span style="background:#1a1a2e;border:1px solid #4a4a8a;border-radius:2px;'
        f"padding:2px 8px;font-size:10px;color:#9090d0;letter-spacing:0.07em;"
        f'font-weight:700;margin-right:4px;">{text}</span>'
    )


def _active_ability_badge(text: str) -> str:
    """HTML badge for an active army ability (faction once-per-battle, Command Protocol, …).

    Army abilities grant buffs → ONE generic buff-green badge for all factions
    (design_colors.md §0/§4a). No faction-specific colors in src/.
    """
    fg, bg = "#4a9a5a", "#0a1a0a"
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

        already_applied = st.session_state.get(f"applied_triggered_{ability.id}", False)
        n = len(eligible)
        st.caption(f"{ability.name_en} — {n} unit{'s' if n > 1 else ''} eligible")
        if already_applied:
            st.caption("Already applied this phase.")
        elif is_active and st.button(
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
            st.session_state[f"applied_triggered_{ability.id}"] = True
            st.rerun()


def _render_directive_buttons(protocol, faction: str, faction_dir: str, round_num: int) -> None:
    """Show Primary / Secondary directive selection buttons for the active protocol."""
    st.caption(f"↳ **Primary:** {protocol.primary}")
    st.caption(f"↳ **Secondary:** {protocol.secondary}")
    col_p, col_s = st.columns(2)
    if col_p.button(
        "Use Primary",
        key=f"cmd_directive_primary_{faction}_{round_num}",
        use_container_width=True,
    ):
        st.session_state[f"protocol_directive_{faction_dir}"] = "primary"
        st.rerun()
    if col_s.button(
        "Use Secondary",
        key=f"cmd_directive_secondary_{faction}_{round_num}",
        use_container_width=True,
    ):
        st.session_state[f"protocol_directive_{faction_dir}"] = "secondary"
        st.rerun()


def _get_extra_protocol_id(protocols: list, faction: str) -> str | None:
    """Return the ID of the 6th (always-active) protocol — the one not assigned to any round.

    Returns None when not all 5 round slots are filled (extra can't be determined yet).
    """
    assignments = st.session_state.get("protocol_assignments", {}).get(faction, {})
    assigned_ids = set(assignments.values())
    if len(assigned_ids) < 5:
        return None
    extras = [p.id for p in protocols if p.id not in assigned_ids]
    return extras[0] if len(extras) == 1 else None


def _render_extra_protocol(
    protocol, faction: str, faction_dir: str, is_active: bool, current_round: int
) -> None:
    """Render the always-active 6th protocol with its own directive selection.

    Dynasty bonus: if the faction's dynasty matches the protocol's subfaction_affinity,
    both directives are active simultaneously (no player choice required).
    """
    first = st.session_state.get("first_player")
    dynasty: str | None = st.session_state.get("p1_dynasty" if faction == first else "p2_dynasty")
    dynasty_bonus = bool(dynasty and dynasty == protocol.subfaction_affinity)

    extra_key = f"protocol_extra_directive_{faction_dir}"
    extra_directive: str | None = st.session_state.get(extra_key)
    st.caption("*Always active (extra protocol):*")

    if dynasty_bonus:
        badge_text = f"{protocol.name_en.upper()} — DYNASTY BONUS (BOTH)"
        st.markdown(_active_ability_badge(badge_text), unsafe_allow_html=True)
        st.caption(f"↳ Primary: {protocol.primary}")
        st.caption(f"↳ Secondary: {protocol.secondary}")
        return

    if extra_directive:
        badge_text = f"{protocol.name_en.upper()} — {extra_directive.upper()}"
        st.markdown(_active_ability_badge(badge_text), unsafe_allow_html=True)
        chosen_text = protocol.primary if extra_directive == "primary" else protocol.secondary
        st.caption(f"↳ {chosen_text}")
        if is_active and st.button(
            "Change extra directive",
            key=f"extra_dir_change_{faction}_{current_round}",
            use_container_width=True,
        ):
            st.session_state[extra_key] = None
            st.rerun()
    else:
        st.caption(f"**{protocol.name_en}**")
        st.caption(f"↳ Primary: {protocol.primary}")
        st.caption(f"↳ Secondary: {protocol.secondary}")
        if is_active:
            col_p, col_s = st.columns(2)
            if col_p.button(
                "Primary", key=f"extra_dir_p_{faction}_{current_round}", use_container_width=True
            ):
                st.session_state[extra_key] = "primary"
                log_action(
                    current_round, "command", faction, f"Extra: {protocol.name_en} — primary"
                )
                st.rerun()
            if col_s.button(
                "Secondary",
                key=f"extra_dir_s_{faction}_{current_round}",
                use_container_width=True,
            ):
                st.session_state[extra_key] = "secondary"
                log_action(
                    current_round, "command", faction, f"Extra: {protocol.name_en} — secondary"
                )
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

    protocols = load_round_choice_abilities(faction_dir)
    if not protocols:
        return

    phase_key = _current_phase_key()
    is_active = faction == st.session_state.get("active")
    active_key = f"protocol_active_{faction_dir}"
    directive_key = f"protocol_directive_{faction_dir}"
    used_key = f"protocol_used_ids_{faction_dir}"
    active_id = st.session_state.get(active_key)
    used_ids: list = st.session_state.get(used_key, [])
    current_round = st.session_state.get("round", 1)

    st.divider()
    label = load_round_choice_label(faction_dir)
    st.caption(f"**{label}**")

    active_directive: str | None = st.session_state.get(directive_key)

    # Auto-activate the assigned protocol for this round
    if not active_id:
        faction_assignments = st.session_state.get("protocol_assignments", {}).get(faction, {})
        assigned_id = faction_assignments.get(current_round)
        if assigned_id:
            active_id = assigned_id
            st.session_state[active_key] = assigned_id

    if active_id:
        p = next((p for p in protocols if p.id == active_id), None)
        if p:
            if not active_directive:
                st.caption(f"**{p.name_en}** — active this round")
                if is_active:
                    _render_directive_buttons(p, faction, faction_dir, current_round)
                else:
                    st.caption("↳ *Awaiting directive selection*")
            else:
                badge_text = f"{p.name_en.upper()} — {active_directive.upper()}"
                st.markdown(_active_ability_badge(badge_text), unsafe_allow_html=True)
                chosen_text = p.primary if active_directive == "primary" else p.secondary
                st.caption(f"↳ {chosen_text}")
    elif phase_key != "command" or not is_active:
        st.caption("— no protocol selected —")
    else:
        # Fallback free selection — active player, command phase, no assignment set
        available = [p for p in protocols if p.id not in used_ids]
        if not available:
            st.caption("All protocols have been used.")
        else:
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
                st.session_state[active_key] = chosen.id
                st.session_state[used_key] = used_ids + [chosen.id]
                st.session_state[directive_key] = None
                log_action(current_round, "command", faction, f"Protocol: {chosen.name_en}")
                st.rerun()

    # Render the 6th (always-active) protocol when all 5 rounds are assigned
    extra_id = _get_extra_protocol_id(protocols, faction)
    if extra_id:
        extra_p = next((p for p in protocols if p.id == extra_id), None)
        if extra_p:
            _render_extra_protocol(extra_p, faction, faction_dir, is_active, current_round)


def _render_once_per_battle_ability_ui(
    faction: str,
    faction_abilities: list[Ability],
    units: list[Unit],
) -> None:
    """Command-phase UI for factions with once-per-battle activated abilities.

    Generic: reads abilities from YAML, stores activation in activated_abilities session key.
    No-ops silently for factions without such abilities.
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

    # Factions with round-choice protocols are handled by _render_protocol_ui
    if load_round_choice_abilities(faction_dir):
        return

    once_ability = next(
        (a for a in command_activated if any(c.once_per_battle for c in a.conditions)),
        None,
    )
    if not once_ability:
        return

    phase_key = _current_phase_key()
    current_round = st.session_state.get("round", 1)
    is_active = faction == st.session_state.get("active")
    activated: dict = st.session_state.get("activated_abilities", {})
    entry = activated.get(faction)

    ability_name = once_ability.name_en.split("—")[0].strip()

    st.divider()

    if entry:
        # Show the currently active stage's badge_label and active_text from YAML
        current_id = entry.get("ability_id", once_ability.id)
        current_ability = next((a for a in faction_abilities if a.id == current_id), once_ability)
        badge_text = current_ability.badge_label or ability_name.upper()
        st.markdown(_active_ability_badge(badge_text), unsafe_allow_html=True)
        if current_ability.active_text:
            st.caption(f"↳ {current_ability.active_text}")
        return

    if not is_active or phase_key != "command":
        st.caption(f"— {ability_name} not called —")
        return

    has_activator = any(check_conditions(once_ability, u, {}) for u in units)
    required_kws = [kw for c in once_ability.conditions for kw in (c.has_keywords or [])]
    kw_str = " or ".join(required_kws) if required_kws else "activator"

    if has_activator:
        st.caption(f"**{ability_name}** — call once per battle (requires {kw_str})")
        if st.button(
            f"Call {ability_name}!",
            key=f"once_ability_call_{faction}",
            type="primary",
            use_container_width=True,
        ):
            activated[faction] = {
                "ability_id": once_ability.id,
                "round_activated": current_round,
            }
            st.session_state.activated_abilities = activated
            log_action(current_round, "command", faction, f"{ability_name} called")
            st.rerun()
    else:
        st.caption(f"— {ability_name} not available (no {kw_str}) —")


def render_army_card(
    faction: str,
    subfaction: str | None,
    faction_abilities: list[Ability],
    units: list[Unit],
    units_state: dict,  # type: ignore[type-arg]
    dynasty: str | None = None,
) -> None:
    phase_key = _current_phase_key()

    with st.container(border=True):
        army_name = f"{faction}" + (f" — {subfaction}" if subfaction else "")
        st.markdown(f"**{army_name}**")

        # Faction keyword badges
        badges_html = _faction_badge(faction)
        if subfaction:
            badges_html += _faction_badge(subfaction)
        if dynasty:
            badges_html += _faction_badge(dynasty.replace("_", " ").title())
        st.markdown(badges_html, unsafe_allow_html=True)

        # Command Protocol UI (Necrons — no-op for other factions)
        _render_protocol_ui(faction)

        # Once-per-battle command-phase faction abilities — no-op if faction has none
        _render_once_per_battle_ability_ui(faction, faction_abilities, units)

        # Triggered ability buttons (phase-dependent)
        _render_triggered_abilities(faction, faction_abilities, units, units_state, phase_key)
