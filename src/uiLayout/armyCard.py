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

from gameMechanic.game_log import log_action
from gameMechanic.game_state import PHASES
from gameMechanic.unit_mutations import apply_living_metal
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


def _living_metal_eligible(
    units: list[Unit], units_state: dict  # type: ignore[type-arg]
) -> list[str]:
    return [
        u.id
        for u in units
        if not units_state.get(u.id, {}).get("destroyed", False)
        and "livingMetal" in u.rules
        and units_state.get(u.id, {}).get("current_wounds", 0)
        < u.wounds * units_state.get(u.id, {}).get("models", 0)
    ]


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

    for ability in triggered:
        if ability.effect.type == "heal":
            eligible = _living_metal_eligible(units, units_state)
            if not eligible:
                continue
            n = len(eligible)
            st.caption(f"{ability.name_en} — {n} unit{'s' if n > 1 else ''} eligible")
            if is_active and st.button(
                f"Apply {ability.name_en}",
                key=f"army_triggered_{ability.id}",
                use_container_width=True,
            ):
                healed = 0
                for uid in eligible:
                    unit = next(u for u in units if u.id == uid)
                    if apply_living_metal(units_state[uid], unit):
                        healed += 1
                log_action(
                    st.session_state.round,
                    phase_key,
                    faction,
                    f"{ability.name_en}: {healed} unit(s) healed",
                )
                st.rerun()

        elif ability.effect.type == "reanimate":
            # RP button appears in gameActionsArea after attacks — not here.
            # armyCard only shows it as an info label so the player knows it's available.
            st.caption(f"{ability.name_en} — triggers after enemy attacks")


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
