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

from gameMechanic.ability_engine import (
    build_aura_range_hint_text,
    check_conditions,
    execute_effect,
    get_active_heal_bonus,
)
from gameMechanic.game_log import log_action
from gameMechanic.game_state import (
    PHASES,
    faction_dir_for,
    faction_display_name_for,
    round_choice_state_key,
    short_round_choice_label,
    subfaction_badge_for,
    subfaction_value_for,
    unit_id_from_state_key,
)
from gameObjects.ability import Ability
from gameObjects.loader import (
    load_round_choice_abilities,
    load_round_choice_label,
    load_subfaction_meta,
)
from gameObjects.unit import Unit
from uiLayout.badges import badge

# Faction / subfaction keyword badges (design_colors.md §2a).
_BADGE_BLUE = "#a5b4fc"  # light blue — faction badge + a chosen subfaction
_BADGE_MUTED = "#9ca3af"  # subfaction placeholder: roster made no choice (no buffs)
_BADGE_ERROR = "#ef4444"  # subfaction data error: faction declares no subfaction field

_SUBFACTION_BADGE_COLOR: dict[str, str] = {
    "set": _BADGE_BLUE,
    "missing": _BADGE_MUTED,
    "error": _BADGE_ERROR,
}


_KEYWORD_BADGE_BG = "#1a1a2e"  # dark blue-grey behind faction/subfaction badges
_ACTIVE_ABILITY_FG = "#4a9a5a"  # buff-green (design_colors.md §0/§4a)
_ACTIVE_ABILITY_BG = "#0a1a0a"


def _keyword_badge(text: str, fg: str = _BADGE_BLUE) -> str:
    return badge(text, fg, _KEYWORD_BADGE_BG, margin_right="4px")


def _active_ability_badge(text: str) -> str:
    """HTML badge for an active army ability (faction once-per-battle, Command Protocol, …).

    Army abilities grant buffs → ONE generic buff-green badge for all factions
    (design_colors.md §0/§4a). No faction-specific colors in src/.
    """
    return badge(text, _ACTIVE_ABILITY_FG, _ACTIVE_ABILITY_BG, margin_right="4px")


def _current_phase_key() -> str:
    return PHASES[st.session_state.phase_idx][1]


def _ability_section_visible(phase_key: str) -> bool:
    """Round-choice and once-per-battle UI appear from the command phase on, never in setup."""
    return phase_key != "setup"


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

        if ability.effect.type == "heal":
            sample = unit_by_id[unit_id_from_state_key(eligible[0])]
            bonus = get_active_heal_bonus(faction, sample)
            if bonus:
                st.caption(f"↑ Directive active: +{bonus} wound per {ability.name_en} use")

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


def _directive_window_open(faction: str, kind: str) -> bool:
    """Whether the selection window for one directive choice is still open.

    A directive choice (``kind`` is "directive" or "extra_directive") may be made
    while the battle round's selection window is open (``directive_pending`` True)
    AND that specific directive has not yet been chosen. The two choices are
    independent: choosing the main directive must not close the extra directive's
    window, and vice versa (Wahapedia Z. 568/579 — both chosen at round start,
    independently). The window only re-opens on the next round-start reset.
    """
    pending = st.session_state.get(round_choice_state_key(faction, "directive_pending"), False)
    chosen = st.session_state.get(round_choice_state_key(faction, kind))
    return bool(pending) and chosen is None


def _render_directive_buttons(round_choice, faction: str, round_num: int) -> None:
    """Show Primary / Secondary directive selection buttons for the main directive.

    Sets only the main ``directive`` key. The selection window is gated by the caller
    on ``_directive_window_open(faction, "directive")``, so setting the directive
    closes this window independently of the extra directive's window.
    """
    directive_key = round_choice_state_key(faction, "directive")
    st.caption(f"↳ **Primary:** {round_choice.primary}")
    st.caption(f"↳ **Secondary:** {round_choice.secondary}")
    col_p, col_s = st.columns(2)
    if col_p.button(
        "Use Primary",
        key=f"cmd_directive_primary_{faction}_{round_num}",
        use_container_width=True,
    ):
        st.session_state[directive_key] = "primary"
        st.rerun()
    if col_s.button(
        "Use Secondary",
        key=f"cmd_directive_secondary_{faction}_{round_num}",
        use_container_width=True,
    ):
        st.session_state[directive_key] = "secondary"
        st.rerun()


def _get_extra_round_choice_id(round_choices: list, faction: str) -> str | None:
    """Return the ID of the 6th (always-active) ability — the one not assigned to any round.

    Returns None when not all 5 round slots are filled (extra can't be determined yet).
    """
    assignments = st.session_state.get("round_choice_assignments", {}).get(faction, {})
    assigned_ids = set(assignments.values())
    if len(assigned_ids) < 5:
        return None
    extras = [p.id for p in round_choices if p.id not in assigned_ids]
    return extras[0] if len(extras) == 1 else None


def _render_aura_range_hint(faction: str) -> None:
    """Render the table-only aura-range hint when an ``aura_range_bonus`` directive is active.

    Data-driven via ``build_aura_range_hint_text`` (effect type + YAML ``affects`` list) —
    no faction/ability literals here. Silently renders nothing when no such directive is
    active. Hint type ``info`` per design_system.md §3 (neutral table reminder, Class B).
    """
    hint = build_aura_range_hint_text(faction)
    if hint:
        st.info(hint)


def _render_extra_round_choice(
    round_choice, faction: str, faction_dir: str, current_round: int
) -> None:
    """Render the always-active 6th ability with its own directive selection.

    Subfaction bonus: if the player's subfaction matches the ability's
    subfaction_affinity, both directives are active simultaneously (no choice).
    The selection window is controlled by ``directive_pending`` (same flag as the
    primary directive) — not ``is_active``.
    """
    subfaction = subfaction_value_for(faction)
    affinity_bonus = bool(subfaction and subfaction == round_choice.subfaction_affinity)
    _, subfaction_label = load_subfaction_meta(faction_dir)

    extra_key = round_choice_state_key(faction, "extra_directive")
    extra_directive: str | None = st.session_state.get(extra_key)
    st.caption("*Always active (extra):*")

    short_name = short_round_choice_label(round_choice.name_en)
    if affinity_bonus:
        badge_text = f"{short_name.upper()} — {subfaction_label.upper()} BONUS (BOTH)"
        st.markdown(_active_ability_badge(badge_text), unsafe_allow_html=True)
        st.caption(f"↳ Primary: {round_choice.primary}")
        st.caption(f"↳ Secondary: {round_choice.secondary}")
        _render_aura_range_hint(faction)
        return

    if extra_directive:
        badge_text = f"{short_name.upper()} — {extra_directive.upper()}"
        st.markdown(_active_ability_badge(badge_text), unsafe_allow_html=True)
        chosen_text = (
            round_choice.primary if extra_directive == "primary" else round_choice.secondary
        )
        st.caption(f"↳ {chosen_text}")
        _render_aura_range_hint(faction)
        # "Change extra directive" button intentionally removed: the extra directive is
        # chosen at the start of each battle round (Wahapedia Z. 579) and locked for
        # the whole round. The only valid reset path is _reset_round_choice_state().
    else:
        # Choosing the EXTRA directive sets only extra_key, closing this window
        # independently of the main directive's window (Wahapedia Z. 568/579).
        if _directive_window_open(faction, "extra_directive"):
            st.caption(f"**{round_choice.name_en}**")
            st.caption(f"↳ Primary: {round_choice.primary}")
            st.caption(f"↳ Secondary: {round_choice.secondary}")
            col_p, col_s = st.columns(2)
            if col_p.button(
                "Primary", key=f"extra_dir_p_{faction}_{current_round}", use_container_width=True
            ):
                st.session_state[extra_key] = "primary"
                log_action(
                    current_round, "command", faction, f"Extra: {round_choice.name_en} — primary"
                )
                st.rerun()
            if col_s.button(
                "Secondary",
                key=f"extra_dir_s_{faction}_{current_round}",
                use_container_width=True,
            ):
                st.session_state[extra_key] = "secondary"
                log_action(
                    current_round, "command", faction, f"Extra: {round_choice.name_en} — secondary"
                )
                st.rerun()
        else:
            st.caption("↳ *Awaiting directive selection (round start)*")


def _render_round_choice_ui(faction: str) -> None:
    """Round-choice ability UI — only for factions with round_choice entries in YAML.

    Both players may choose their directive simultaneously at the start of each battle
    round (Wahapedia Z. 568: "at the start of each battle round … select one of its
    directives"). The selection window is controlled by ``directive_pending``, not by
    ``is_active``, so the inactive player is not disadvantaged by a delayed choice.
    """
    try:
        faction_dir = faction_dir_for(faction)
    except KeyError:
        return

    round_choices = load_round_choice_abilities(faction_dir)
    if not round_choices:
        return

    phase_key = _current_phase_key()
    if not _ability_section_visible(phase_key):
        return
    is_active = faction == st.session_state.get("active")
    active_key = round_choice_state_key(faction, "active")
    directive_key = round_choice_state_key(faction, "directive")
    used_key = round_choice_state_key(faction, "used_ids")
    active_id = st.session_state.get(active_key)
    used_ids: list = st.session_state.get(used_key, [])
    current_round = st.session_state.get("round", 1)

    st.divider()
    label = load_round_choice_label(faction_dir)
    st.caption(f"**{label}**")

    active_directive: str | None = st.session_state.get(directive_key)

    # Auto-activate the assigned ability for this round
    if not active_id:
        faction_assignments = st.session_state.get("round_choice_assignments", {}).get(faction, {})
        assigned_id = faction_assignments.get(current_round)
        if assigned_id:
            active_id = assigned_id
            st.session_state[active_key] = assigned_id

    if active_id:
        p = next((p for p in round_choices if p.id == active_id), None)
        if p:
            if not active_directive:
                st.caption(f"**{p.name_en}** — active this round")
                if _directive_window_open(faction, "directive"):
                    # Choosing the MAIN directive closes only this window
                    # (its own `directive` key), independent of the extra directive.
                    _render_directive_buttons(p, faction, current_round)
                else:
                    st.caption("↳ *Awaiting directive selection (round start)*")
            else:
                badge_text = (
                    f"{short_round_choice_label(p.name_en).upper()} — {active_directive.upper()}"
                )
                st.markdown(_active_ability_badge(badge_text), unsafe_allow_html=True)
                chosen_text = p.primary if active_directive == "primary" else p.secondary
                st.caption(f"↳ {chosen_text}")
                _render_aura_range_hint(faction)
    elif not is_active or phase_key != "command":
        st.caption("— none selected —")
    else:
        # Fallback free selection — active player, command phase, no assignment set
        available = [p for p in round_choices if p.id not in used_ids]
        if not available:
            st.caption(f"All {label} have been used.")
        else:
            choice = st.radio(
                label,
                options=range(len(available)),
                format_func=lambda i: available[i].name_en,
                key=f"cmd_round_choice_choice_{faction}",
            )
            if st.button(
                "Activate",
                key=f"cmd_round_choice_activate_{faction}",
                type="primary",
                use_container_width=True,
            ):
                chosen = available[choice]
                st.session_state[active_key] = chosen.id
                st.session_state[used_key] = used_ids + [chosen.id]
                st.session_state[directive_key] = None
                log_action(current_round, "command", faction, f"{label}: {chosen.name_en}")
                st.rerun()

    # Render the 6th (always-active) ability when all 5 rounds are assigned
    extra_id = _get_extra_round_choice_id(round_choices, faction)
    if extra_id:
        extra_p = next((p for p in round_choices if p.id == extra_id), None)
        if extra_p:
            _render_extra_round_choice(extra_p, faction, faction_dir, current_round)


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

    # Factions with round-choice abilities are handled by _render_round_choice_ui
    if load_round_choice_abilities(faction_dir):
        return

    once_ability = next(
        (a for a in command_activated if any(c.once_per_battle for c in a.conditions)),
        None,
    )
    if not once_ability:
        return

    phase_key = _current_phase_key()
    if not _ability_section_visible(phase_key):
        return
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
    faction_abilities: list[Ability],
    units: list[Unit],
    units_state: dict,  # type: ignore[type-arg]
) -> None:
    phase_key = _current_phase_key()

    with st.container(border=True):
        # Roster title (top) — the player slot key is the roster's display name.
        st.markdown(f"**{faction}**")

        # Faction keyword badge (faction display name) + always-visible subfaction
        # badge: a chosen value, or a visible 'No <Label>' / 'No Subfaction' marker.
        subfaction = subfaction_badge_for(faction)
        badges_html = _keyword_badge(faction_display_name_for(faction))
        badges_html += _keyword_badge(
            subfaction.text, _SUBFACTION_BADGE_COLOR.get(subfaction.state, _BADGE_BLUE)
        )
        st.markdown(badges_html, unsafe_allow_html=True)

        # Round-choice ability UI (e.g. Necron Command Protocols — no-op otherwise)
        _render_round_choice_ui(faction)

        # Once-per-battle command-phase faction abilities — no-op if faction has none
        _render_once_per_battle_ability_ui(faction, faction_abilities, units)

        # Triggered ability buttons (phase-dependent)
        _render_triggered_abilities(faction, faction_abilities, units, units_state, phase_key)
