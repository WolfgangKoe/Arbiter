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
from gameMechanic.game_state import PHASES
from gameObjects.ability import Ability
from gameObjects.unit import Unit


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
            uid
            for uid, ustate in units_state.items()
            if (unit := unit_by_id.get(uid)) is not None and check_conditions(ability, unit, ustate)
        ]
        if not eligible:
            continue

        n = len(eligible)
        st.caption(f"{ability.name_en} — {n} unit{'s' if n > 1 else ''} eligible")
        if is_active and st.button(
            f"Apply {ability.name_en}",
            key=f"army_triggered_{ability.id}",
            use_container_width=True,
        ):
            applied = sum(
                1 for uid in eligible if execute_effect(ability, uid, faction, unit_by_id[uid])
            )
            log_action(
                st.session_state.round,
                phase_key,
                faction,
                f"{ability.name_en}: {applied} unit(s) healed",
            )
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

        # Triggered ability buttons (phase-dependent)
        _render_triggered_abilities(faction, faction_abilities, units, units_state, phase_key)
