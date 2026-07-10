"""Shared UI utilities for phase handlers.

Provides: lookup, state_badges_html, wound_adjustment_buttons,
          render_player_column, render_group_cards, render_group_assignment,
          render_attack_resolution, PHASE_RULES.

Handlers import from here — never from gameActionsArea — to avoid circular imports.
"""

from __future__ import annotations

from collections.abc import Callable
from typing import Any, cast

import streamlit as st

from constants.symbols import (
    SYM_ADD,
    SYM_CHECK,
    SYM_COLLAPSE,
    SYM_CROSS,
    SYM_EXPAND,
    SYM_EXPAND_ALT,
    SYM_RESET,
    SYM_SWORDS,
)
from gameMechanic.attack_math import (  # noqa: F401
    _compute_attacks,
    _detect_weapon_special,
    _group_melee_budget,
    _parse_strength,
    _rapid_fire_input_cap,
    _restriction_label,
    _total_attacks_int,
)
from gameMechanic.game_state import (
    PHASES,
    active_round_choice_buff_labels,
    faction_dir_for,
    units_key_for,
    units_list_for,
)
from gameMechanic.unit_mutations import (
    activate_desperate_breakout,
    activate_morale_auto_pass,
    adjust_cp,
    apply_damage,
    heal_unit,
)
from gameObjects.ability import Effect
from gameObjects.loader import load_stratagems
from gameObjects.stratagem import (
    Stratagem,
    reactive_stratagems_for,
    stratagem_conditions_met,
    stratagem_undo_visible,
    stratagem_usable_by_player,
    stratagem_visibility,
)
from gameObjects.unit import ModelGroup, Unit
from gameObjects.weapon import Weapon, WeaponProfile
from uiLayout.badges import badge
from uiLayout.dice_compose import (  # noqa: F401
    block_divider_html,
    dice_face_svg,
    dice_row_html,
    grid_row_html,
    modifier_die_pair_html,
    save_modifier_die_pair_html,
    special_die_html,
    threshold_header_html,
)
from uiLayout.dice_html import (  # noqa: F401
    _render_dice_roll_block,
    _render_dice_save_block,
    _render_dice_wound_block,
)
from uiLayout.go_card import (
    GoCardState,
    action_slot_text,
    go_card_container_style,
    go_card_html,
)

# ---------------------------------------------------------------------------
# Phase description texts
# ---------------------------------------------------------------------------

PHASE_RULES: dict[str, str] = {
    "command": (
        "**Command Phase**\n\n"
        "The active player receives **+1 CP** (Battle-forged armies). "
        "Activate abilities and stratagems that trigger in the Command Phase."
    ),
    "movement": (
        "**Movement Phase**\n\n"
        "Select a unit and choose its movement type:\n"
        '- **Normal** — move up to M"\n'
        '- **Advance** — move up to M"+D6", cannot shoot or charge afterwards\n'
        "- **Stationary** — do not move\n"
        '- **Retreat** — only if in melee; move up to M", cannot shoot or charge afterwards'
    ),
    "psychic": (
        "**Psychic Phase**\n\n"
        "PSYKER units attempt to manifest psychic powers. "
        "Roll **2D6** ≥ Warp Charge value to manifest. "
        "Opponent may attempt to deny with their own PSYKER (2D6 > manifesting roll)."
    ),
    "shooting": (
        "**Shooting Phase**\n\n"
        "Select a unit to shoot, then select a target. "
        "Units that Advanced or Retreated cannot shoot. "
        "Units in melee cannot shoot.\n\n"
        "Attack sequence: **Hit** (BS) → **Wound** (S vs T) → **Save** (Sv−AP) → **Damage**"
    ),
    "charge": (
        "**Charge Phase**\n\n"
        'Eligible units (≤ 12" from enemy, did not Advance or Retreat) may declare a charge. '
        "Roll **2D6** — result must be ≥ distance to closest target model. "
        "On success: move into melee range."
    ),
    "fight": (
        "**Fight Phase**\n\n"
        "Starting with the **non-active player**, both sides alternate selecting eligible units. "
        "Units that charged this turn fight **before** other units. "
        'Each unit: **Pile In** (up to 3") → **Melee attacks** → **Consolidate** (up to 3").'
    ),
    "morale": (
        "**Morale Phase**\n\n"
        "Units that suffered model losses this turn must take a morale test: "
        "Roll **D6** + models lost. If result > Leadership: additional models flee (result − Ld).\n\n"
        "Single-model units auto-pass."
    ),
}

# ---------------------------------------------------------------------------
# Badge rendering
# ---------------------------------------------------------------------------

# design_colors.md §0 (FESTGELEGT): MOVED = blue, Buff = green, RESERVE = HEROIC-INT.
# colour. Must match unitCard._BADGE_COLORS — the two tables had drifted apart
# (MOVED/Buff were swapped here), so badges looked different in the group-flow area.
_BADGE_COLORS: dict[str, tuple[str, str]] = {
    "MOVED": ("#60a5fa", "#0a1020"),
    "STATIONARY": ("#6b5f44", "#1c1a14"),
    "ADVANCED": ("#d4a017", "#2e2618"),
    "RETREATED": ("#c04040", "#1e1010"),
    "IN MELEE": ("#e07050", "#2a1810"),
    "CHARGED": ("#b070d8", "#1a0a2a"),
    "FOUGHT": ("#c080e8", "#200a30"),
    "SHOT": ("#40a0b8", "#081418"),
    "CAST": ("#9060d0", "#180a28"),
    "RESERVE": ("#ff9060", "#2a1208"),
    "DESTROYED": ("#c04040", "#1e1010"),
}

_BUFF_COLOR: tuple[str, str] = ("#4a9a5a", "#0a1a0a")
_DEBUFF_COLOR: tuple[str, str] = ("#ef4444", "#1e0808")

_MOVEMENT_BADGE: dict[str, str] = {
    "moved": "MOVED",
    "stationary": "STATIONARY",
    "advanced": "ADVANCED",
    "retreated": "RETREATED",
}


def _badge(text: str, variant: str = "") -> str:
    if text in _BADGE_COLORS:
        fg, bg = _BADGE_COLORS[text]
    elif variant == "buff":
        fg, bg = _BUFF_COLOR
    elif variant == "debuff":
        fg, bg = _DEBUFF_COLOR
    else:
        fg, bg = ("#c9a84c", "#2e2618")
    return badge(text, fg, bg)


def state_badges_html(unit_state: dict) -> str:  # type: ignore[type-arg]
    """Generate HTML state badges from movement_choice, turn_flags and active_buffs."""
    parts: list[str] = []
    flags = unit_state.get("turn_flags", {})
    mc = unit_state.get("movement_choice")

    # Movement slot: FOUGHT > CHARGED > movement_choice (suppressed when in_reserve)
    if flags.get("fought"):
        movement_slot = "FOUGHT"
    elif flags.get("charged"):
        movement_slot = "CHARGED"
    elif mc in _MOVEMENT_BADGE and not unit_state.get("in_reserve"):
        movement_slot = _MOVEMENT_BADGE[mc]
    else:
        movement_slot = None

    if movement_slot:
        parts.append(_badge(movement_slot))

    # SHOT and CAST are always additive alongside the movement slot
    if flags.get("shot"):
        parts.append(_badge("SHOT"))
    if flags.get("cast"):
        parts.append(_badge("CAST"))

    # IN MELEE: always visible except when CHARGED is the active movement slot
    if unit_state.get("in_melee") and movement_slot != "CHARGED":
        parts.append(_badge("IN MELEE"))

    if unit_state.get("in_reserve"):
        parts.append(_badge("RESERVE"))

    for buf in unit_state.get("active_buffs", []):
        parts.append(_badge(buf.get("badge_label", "BUFF"), variant="buff"))

    return "".join(parts)


# ---------------------------------------------------------------------------
# Unit lookup
# ---------------------------------------------------------------------------


def lookup(faction: str, uid: str) -> tuple[Unit, dict]:  # type: ignore[type-arg]
    """Return (Unit, unit_state_dict) for the given faction + state_key (uid).

    uid may be a bare unit ID or a deduplicated state key ('unit.id#N').
    """
    from gameMechanic.game_state import unit_id_from_state_key

    unit_id = unit_id_from_state_key(uid)
    units = units_list_for(faction)
    unit = next((u for u in units if u.id == unit_id), None)
    if unit is None:
        raise KeyError(
            f"No unit with id {unit_id!r} in catalog for faction {faction!r} "
            f"(state key {uid!r}). Session state and unit catalog are out of sync."
        )
    return unit, st.session_state[units_key_for(faction)][uid]


# ---------------------------------------------------------------------------
# Wound / heal buttons
# ---------------------------------------------------------------------------


def render_unit_selectbox(
    label: str,
    candidates: list[dict],  # type: ignore[type-arg]
    state_key: str,
    *,
    none_label: str | None = None,
) -> str | None:
    """Render a unit-selection selectbox and persist the chosen uid to session_state.

    Each candidate dict must have a ``uid`` key; ``custom_name`` or ``name`` are used
    for display. Returns the selected uid, or None when candidates is empty or the
    none-sentinel option is selected.

    ``none_label``: when set, prepends a ``None``-uid option with this label (e.g.
    "— Select target unit —"). The user choosing it sets session_state[state_key] to
    None and returns None.
    """
    options: list[str | None] = []
    labels: list[str] = []
    if none_label is not None:
        options.append(None)
        labels.append(none_label)
    for u in candidates:
        options.append(u["uid"])
        labels.append(u.get("custom_name") or u.get("name", u["uid"]))

    if not options:
        return None

    current = st.session_state.get(state_key)
    current_idx = options.index(current) if current in options else 0
    chosen_idx = st.selectbox(
        label,
        range(len(options)),
        format_func=lambda i: labels[i],
        index=current_idx,
        key=f"select_{state_key}",
    )
    selected = options[chosen_idx]
    st.session_state[state_key] = selected
    return selected


def wound_adjustment_buttons(faction: str, uid: str, unit: Unit) -> None:
    """Render ±1/2/3 wound-adjustment buttons for a unit."""
    bc = st.columns(6)
    for col, delta, label in zip(bc, [-3, -2, -1, 1, 2, 3], ["−3", "−2", "−1", "+1", "+2", "+3"]):
        with col:
            is_mortal = delta == -1
            if st.button(
                label,
                key=f"w{delta}_{faction}_{uid}",
                type="primary" if is_mortal else "secondary",
            ):
                if delta < 0:
                    _, unit_state = lookup(faction, uid)
                    was_destroyed = bool(unit_state.get("destroyed"))
                    apply_damage(uid, faction, -delta, unit, mortal=is_mortal)
                    _maybe_flag_transport_destroyed(faction, uid, unit, was_destroyed)
                else:
                    heal_unit(uid, faction, delta, unit)
                st.rerun()


# ---------------------------------------------------------------------------
# Melee engagement display
# ---------------------------------------------------------------------------


def render_melee_engagements(faction: str, uid: str, unit_state: dict) -> None:  # type: ignore[type-arg]
    """Show the list of enemy units this unit is engaged with, each with a Break button."""
    from gameMechanic.unit_mutations import leave_melee_pair

    melee_with: list[list[str]] = unit_state.get("melee_with", [])
    if not unit_state.get("in_melee") or not melee_with:
        return

    p1 = st.session_state.get("first_player", "")
    p2 = st.session_state.get("second_player", "")
    units_by_faction = {
        p1: {u.id: u for u in units_list_for(p1)},
        p2: {u.id: u for u in units_list_for(p2)},
    }

    st.markdown(f"**{SYM_SWORDS} Engaged with:**")
    for i, (enemy_fac, enemy_uid) in enumerate(list(melee_with)):
        enemy_unit = units_by_faction.get(enemy_fac, {}).get(enemy_uid)
        name = enemy_unit.name_en if enemy_unit else enemy_uid
        cols = st.columns([4, 1])
        cols[0].markdown(f"- {name}")
        if cols[1].button(
            f"Break {SYM_CROSS}", key=f"break_{faction}_{uid}_{enemy_fac}_{enemy_uid}_{i}"
        ):
            leave_melee_pair(uid, faction, enemy_uid, enemy_fac)
            st.rerun()


# ---------------------------------------------------------------------------
# Standard player-column renderer (shared by all handlers)
# ---------------------------------------------------------------------------


def render_player_column(
    faction: str,
    state: dict,  # type: ignore[type-arg]
    *,
    active_content: Callable[[str, str, Unit, dict, dict], None],  # type: ignore[type-arg]
    inactive_content: Callable[[str, str, Unit, dict], None] | None = None,  # type: ignore[type-arg]
    no_target_caption: str = "—",
    inactive_override: Callable[[], None] | None = None,
    show_wound_buttons: bool = True,
) -> None:
    """Render one player column (active or inactive).

    active_content(faction, uid, unit, unit_state, state) — called when a unit is
    selected for the active player; renders phase-specific actions.

    inactive_content(faction, uid, unit, unit_state) — called when the inactive
    player has a target selected from their army; renders target stats etc.
    If None, only wound adjustment buttons are shown for selected targets.

    no_target_caption — shown to the inactive player when the active player has a
    unit selected but no target from this faction is designated.

    inactive_override — replaces the whole inactive branch when set (used by the
    model-group flow to render the group attack assignment panel).

    show_wound_buttons — set False in phases where targets take no damage
    (e.g. charge declaration) to hide the manual wound adjustment buttons.
    """
    is_active = faction == state["active"]
    indicator = SYM_EXPAND if is_active else SYM_COLLAPSE
    st.markdown(f"**{indicator} {faction}**")
    _render_pending_emergency_disembarkation(faction)

    if is_active:
        sel = st.session_state.selected_unit
        if sel and sel[0] == faction:
            _, uid = sel
            unit, unit_state = lookup(faction, uid)
            badges = state_badges_html(unit_state)
            st.markdown(f"*{unit.name_en}*")
            if badges:
                st.markdown(badges, unsafe_allow_html=True)
            active_content(faction, uid, unit, unit_state, state)
        else:
            st.caption("← Select a unit from your army list.")

    elif inactive_override is not None:
        inactive_override()

    else:
        targets: list[tuple[str, str]] = st.session_state.selected_targets
        matching = [t for t in targets if t[0] == faction]
        if matching:
            for tgt in matching:
                _, uid = tgt
                unit, unit_state = lookup(faction, uid)
                badges = state_badges_html(unit_state)
                st.markdown(f"*{unit.name_en}* ← Target")
                if badges:
                    st.markdown(badges, unsafe_allow_html=True)
                if inactive_content is not None:
                    inactive_content(faction, uid, unit, unit_state)
                if show_wound_buttons:
                    st.divider()
                    wound_adjustment_buttons(faction, uid, unit)
        elif st.session_state.get("selected_unit"):
            st.caption(no_target_caption)
        else:
            st.caption("—")


# ---------------------------------------------------------------------------
# Reactive stratagems — contextual GO boxes (Plan 015)
# ---------------------------------------------------------------------------
#
# `stratagem_visibility()` hides every `timing: phase_reactive` stratagem in the
# central Stratagems tab (gameProtocoll.py) unconditionally — that pool is only
# ever surfaced here, at the exact moment a phase handler detects the rule
# trigger the stratagem's `event` field names (e.g. "an enemy charge was just
# declared"). `spend_stratagem` is the single CP/usage/modifier bookkeeping path
# for ANY stratagem use, central-list or contextual — gameProtocoll.py's list
# calls it too (Plan 015 Step 2).


def spend_stratagem(strat: Stratagem, faction: str, unit_key: str | None = None) -> None:
    """Deduct CP, mark the stratagem used (phase + battle-scoped), register its modifier.

    The one canonical spend path: CP accounting, once-per-battle/phase tracking,
    and `active_modifiers` registration must never drift apart between the central
    Stratagems-tab list and contextual reactive boxes.
    """
    adjust_cp(faction, -strat.cp_cost)

    used_ids_by_player: dict[str, set[str]] = st.session_state.get("used_stratagem_ids", {})
    used_ids = used_ids_by_player.get(faction, set())
    used_ids.add(strat.id)
    used_ids_by_player[faction] = used_ids
    st.session_state.used_stratagem_ids = used_ids_by_player

    if strat.once_per_battle:
        used_battle_ids_by_faction: dict[str, set[str]] = st.session_state.get(
            "used_stratagem_battle_ids", {}
        )
        used_battle_ids = used_battle_ids_by_faction.get(faction, set())
        used_battle_ids.add(strat.id)
        used_battle_ids_by_faction[faction] = used_battle_ids
        st.session_state.used_stratagem_battle_ids = used_battle_ids_by_faction

    if strat.modifier is not None:
        m = strat.modifier
        current_phase = PHASES[st.session_state.get("phase_idx", 0)][1]
        active_mods = st.session_state.get("active_modifiers", [])
        active_mods.append(
            {
                "unit_key": unit_key,
                "source": strat.name_en,
                "effect": {
                    "roll_type": m.roll_type,
                    "value": m.value,
                    "target": m.target,
                    "phase": m.phase or current_phase,
                },
                "expires_at_phase": (current_phase if m.expires_at == "phase_end" else None),
                "expires_at_round": (
                    None if m.expires_at != "turn_end" else st.session_state.get("round", 1)
                ),
            }
        )
        st.session_state.active_modifiers = active_mods

    if strat.effect is not None and unit_key is not None:
        _apply_stratagem_effect(strat.effect, faction, unit_key)


def undo_stratagem(strat: Stratagem, faction: str) -> None:
    """Full rollback of `spend_stratagem` while the activation window is still open.

    CP restored, both usage sets cleared, and any `active_modifiers` entry this
    stratagem registered removed — the exact counterpart `spend_stratagem`'s
    docstring names. Lives next to it so any future Undo affordance (today only
    the central Stratagems-list GO card, gameProtocoll.py, offers one) shares
    this bookkeeping instead of re-deriving it.
    """
    adjust_cp(faction, strat.cp_cost)

    used_ids_by_player: dict[str, set[str]] = st.session_state.get("used_stratagem_ids", {})
    used_ids = used_ids_by_player.get(faction, set())
    used_ids.discard(strat.id)
    used_ids_by_player[faction] = used_ids
    st.session_state.used_stratagem_ids = used_ids_by_player

    if strat.once_per_battle:
        used_battle_ids_by_faction: dict[str, set[str]] = st.session_state.get(
            "used_stratagem_battle_ids", {}
        )
        used_battle_ids = used_battle_ids_by_faction.get(faction, set())
        used_battle_ids.discard(strat.id)
        used_battle_ids_by_faction[faction] = used_battle_ids
        st.session_state.used_stratagem_battle_ids = used_battle_ids_by_faction

    st.session_state.active_modifiers = [
        m for m in st.session_state.get("active_modifiers", []) if m.get("source") != strat.name_en
    ]


def _apply_stratagem_effect(effect: Effect, faction: str, unit_key: str) -> None:
    """Dispatch a stratagem's machine-readable ``effect`` to the unit it targets.

    Data-driven on ``effect.type`` (mirrors the Ability effect-dispatch pattern in
    gameMechanic/ability_engine.py) — new effect types are added here as new
    branches, never via a stratagem-name check. Currently handles the two Core
    Stratagem effect types with an App-enforceable component (Plan 016 S130):
    ``auto_pass_morale`` (Insane Bravery) and ``move`` with
    ``handler: fall_back_through_models`` (Desperate Breakout). No-ops for any
    other effect type (e.g. attack-sequence stratagems, which use `.modifier`
    instead) — silently ignored here on purpose, same as an unmatched unit_key.
    """
    if effect.type == "auto_pass_morale":
        activate_morale_auto_pass(unit_key, faction)
    elif effect.type == "move" and effect.handler == "fall_back_through_models":
        activate_desperate_breakout(unit_key, faction)


def _reactive_go_state(
    strat: Stratagem, vis: str, used_ids: set[str], used_battle_ids: set[str]
) -> tuple[GoCardState, str | None]:
    """Map `stratagem_visibility()`'s clickable/greyed to a GO-card state, for
    reactive GO boxes only.

    Mirrors gameProtocoll.py's ``_go_state_and_reason()`` exactly (S134 task 2b
    closed the divergence): "greyed" with this phase's activation window still
    open (`stratagem_undo_visible`) maps to "used", so the card offers the
    full-rollback ``↺ Undo`` (§6.1) instead of dead-ending in "locked". This
    only ever displays for callers whose window marker survives the Use — e.g.
    Fire Overwatch, whose box is gated by `selected_targets`, not by an
    `on_resolved`-cleared marker. Callers that DO clear their own pending
    marker on Use (e.g. Cut Them Down via `pending_fall_back`) never re-render
    the box afterwards, so the "used" branch simply never shows there — the
    mapping is still correct, the caller's window just closed. With the
    undo window closed, "greyed" falls through to "locked", reason "used"
    for a once_per_battle stratagem spent earlier, else "CP insufficient".
    """
    if vis == "clickable":
        return "ready", None
    if stratagem_undo_visible(strat.id, used_ids, used_battle_ids):
        return "used", None
    reason = "used" if strat.id in used_battle_ids else "CP insufficient"
    return "locked", reason


def _context_caption_renderer(caption: str) -> Callable[[], None]:
    """Factory for a reactive GO card's `expanded_content` — shows the one-line
    "why this card appeared right now" text (e.g. "Warriors were declared a
    charge target") inside the card's own bordered container (S133-D Befund 2:
    never a free-floating caption outside the card). A bare
    ``lambda: st.caption(caption)`` fails mypy (``st.caption`` returns a
    ``DeltaGenerator``, not ``None``) — this wraps it in a real function with
    an explicit ``-> None`` body instead.
    """

    def _render() -> None:
        st.caption(caption)

    return _render


def _reactive_use_callback(
    strat: Stratagem,
    faction: str,
    unit_key_for_modifier: str | None,
    on_spent: Callable[[Stratagem], None] | None,
    on_resolved: Callable[[], None] | None,
) -> Callable[[], None]:
    """Factory for a reactive GO card's on_use callback (see gameProtocoll's
    `_use_callback` for why a factory, not an inline loop-body lambda, is
    required — closing over `strat`/`faction` by value, not the loop
    variable).

    Beyond the canonical `spend_stratagem` bookkeeping every GO card's Use
    button performs, a reactive box's Use also fires the two hooks the pre-
    migration Pass button used to share: `on_spent` (stratagem-specific side
    effect, e.g. Counter-Offensive reassigning `fight_current_player`) and
    `on_resolved` (clearing the caller's own pending-window marker) — now
    Use-only, since §6.1 leaves no Pass action to also trigger them.
    """

    def _use() -> None:
        spend_stratagem(strat, faction, unit_key_for_modifier)
        if on_spent is not None:
            on_spent(strat)
        if on_resolved is not None:
            on_resolved()

    return _use


def _reactive_undo_callback(strat: Stratagem, faction: str) -> Callable[[], None]:
    """Factory for a reactive GO card's on_undo callback (same closure-capture
    rationale as `_reactive_use_callback`). Routes through the canonical
    `undo_stratagem` full rollback — CP, both usage sets and any registered
    modifier revert — exactly like the central list's undo (gameProtocoll.py).
    Caller-side `on_spent`/`on_resolved` effects are NOT re-wound here: a card
    still rendering in the "used" state implies the caller's own window marker
    was never cleared by Use (see `_reactive_go_state`), so there is nothing
    of theirs to restore.
    """
    return lambda: undo_stratagem(strat, faction)


def render_reactive_stratagem_box(
    faction: str,
    phase: str,
    event: str,
    *,
    decline_key: str,
    context_caption: str,
    unit_key_for_modifier: str | None = None,
    unit_for_conditions: Unit | None = None,
    effect_type: str | None = None,
    effect_stat: str | None = None,
    on_spent: Callable[[Stratagem], None] | None = None,
    on_resolved: Callable[[], None] | None = None,
) -> None:
    """Render reactive GO card(s) for `faction` while a (phase, event) window is open.

    Call this from the phase handler at the exact moment a reactive window opens
    (e.g. right after an enemy charge target is declared, in the defender's
    column). Loads `faction`'s stratagem pool (shared + faction-specific),
    filters via `reactive_stratagems_for()`, and renders one compact GO card
    (`render_go_card`, design_system.md §6.1/§6.2 inline-anchor form) per
    stratagem still clickable or greyed for this player — the canonical card
    infrastructure Task 4/5 built for the central Stratagems list, not a
    parallel bespoke box (S130 finding this whole migration closes out).

    No Pass control (§6.1: "passen = [Use] nicht drücken") — a card the
    player does not click just keeps showing "ready" until CP/usage make it
    "locked" or the caller's own pending-window marker goes away (cleared by
    `on_resolved`, now wired to Use only — see `_reactive_use_callback`).
    `decline_key` therefore no longer feeds a suppression set; it only seeds
    a stable per-occurrence widget key (e.g. the charged target's uid) so two
    concurrent occurrences of the same stratagem never collide.

    unit_for_conditions — the unit `strat.conditions` (keyword gate) must be
    checked against, e.g. the targeted defender for an `on_target` anchor.
    Defaults to None, which only stays correct for callers whose reactive
    stratagems carry no keyword conditions (Fire Overwatch, Cut Them Down,
    Counter-Offensive — all `conditions: []` today); a future keyword-gated
    reactive GO with no `unit_for_conditions` passed is hidden rather than
    shown for every unit (fail-safe, mirrors gameProtocoll.py's central-list
    gate via the same `stratagem_conditions_met`).

    effect_type/effect_stat — narrow `candidates` beyond (phase, event) to
    stratagems whose machine-readable `effect` matches (e.g.
    effect_type="debuff_roll", effect_stat="hit" for the Hit-roll anchor vs.
    effect_stat="wound" for the Wound-roll anchor, S135 Paket 4a) — several
    `on_target` reactive GOs can share one (phase, event) window but belong at
    different anchors depending on which roll they modify. None (default)
    keeps every (phase, event) match, as before.

    on_spent(stratagem) — invoked after a successful spend, for stratagem-specific
    side effects beyond CP/usage bookkeeping (e.g. Counter-Offensive reassigning
    `fight_current_player`).

    on_resolved() — invoked after Use, for clearing the caller's own
    pending-window marker (e.g. `pending_fall_back`).
    """
    is_active = faction == st.session_state.get("active")

    try:
        stratagems = load_stratagems(faction_dir_for(faction))
    except Exception:
        return

    candidates = reactive_stratagems_for(stratagems, phase, event)
    if effect_type is not None:
        candidates = [
            c for c in candidates if c.effect is not None and c.effect.type == effect_type
        ]
    if effect_stat is not None:
        candidates = [
            c for c in candidates if c.effect is not None and c.effect.stat == effect_stat
        ]
    if not candidates:
        return

    cp = st.session_state.get("cp", {}).get(faction, 0)
    used_ids = st.session_state.get("used_stratagem_ids", {}).get(faction, set())
    used_battle_ids = st.session_state.get("used_stratagem_battle_ids", {}).get(faction, set())

    for strat in candidates:
        if not stratagem_usable_by_player(strat.player, is_active):
            continue
        met = stratagem_conditions_met(strat.conditions, unit_for_conditions)
        vis = stratagem_visibility(
            strat,
            cp,
            phase,
            used_ids,
            met,
            used_battle_ids,
            reactive_trigger_active=True,
        )
        if vis == "hidden":
            continue

        state, locked_reason = _reactive_go_state(strat, vis, used_ids, used_battle_ids)
        render_go_card(
            key=f"reactive_{faction}_{event}_{strat.id}_{decline_key}",
            name=strat.name_en,
            cp_cost=strat.cp_cost,
            state=state,
            rule_text=strat.rule_text,
            compact=True,
            locked_reason=locked_reason,
            expanded_content=_context_caption_renderer(context_caption),
            on_use=_reactive_use_callback(
                strat, faction, unit_key_for_modifier, on_spent, on_resolved
            ),
            on_undo=_reactive_undo_callback(strat, faction),
        )


# ---------------------------------------------------------------------------
# Command Re-Roll — non-blocking inline offer (S130 Plan 015 Option c)
# ---------------------------------------------------------------------------
#
# Unlike render_reactive_stratagem_box's GO card, Command Re-Roll is
# "Pull, not Push": a single small button next to an already-shown roll
# result, not a bordered card — Ignoring it costs nothing and the flow keeps
# moving. Data-driven via the stratagem's own (phase, event="after_roll")
# window — no stratagem-name string check.


def render_inline_command_reroll(
    faction: str,
    phase: str,
    *,
    reopen_key: str,
    on_reroll: Callable[[], None],
) -> None:
    """Render the inline ``↻ <name> (N CP)`` offer next to a just-made roll.

    Call this at the exact spot a phase handler shows a roll result that is
    still "the last roll" — i.e. before any later roll/step has superseded
    it. Unlike render_reactive_stratagem_box (a GO card that shows a "locked"
    state when CP is short), this Pull-not-Push offer is fully absent — not
    merely disabled — once CP is short or the stratagem was already spent
    this phase: a non-blocking hint has no reason to clutter the screen with
    something the player cannot act on.

    `on_reroll` owns the domain-specific reopening (e.g. popping an "applied"
    flag so the caller's own input widgets return to editable) — this
    function only owns the CP/usage bookkeeping, so callers with a locked
    value and callers with a still-editable value can share it.
    """
    try:
        stratagems = load_stratagems(faction_dir_for(faction))
    except Exception:
        return

    candidates = reactive_stratagems_for(stratagems, phase, "after_roll")
    if not candidates:
        return

    is_active = faction == st.session_state.get("active")
    cp = st.session_state.get("cp", {}).get(faction, 0)
    used_ids = st.session_state.get("used_stratagem_ids", {}).get(faction, set())

    for strat in candidates:
        if not stratagem_usable_by_player(strat.player, is_active):
            continue
        vis = stratagem_visibility(strat, cp, phase, used_ids, True, reactive_trigger_active=True)
        if vis != "clickable":
            continue
        if st.button(
            f"{SYM_RESET} {strat.name_en} ({strat.cp_cost} CP)",
            key=f"cmd_reroll_{faction}_{phase}_{strat.id}_{reopen_key}",
        ):
            spend_stratagem(strat, faction)
            on_reroll()
            st.rerun()


# ---------------------------------------------------------------------------
# GO card — canonical Use/Undo + accordion wrapper (design_system.md §6, Plan 016 S132 1a)
# ---------------------------------------------------------------------------
#
# Thin Streamlit shell around uiLayout.go_card.go_card_html(): renders the pure
# HTML card body, then the one real action widget (Use/Undo) and the optional
# rule-text accordion. Callers own the state (dormant/ready/used/locked) and
# the on_use/on_undo bookkeeping (typically spend_stratagem / its undo
# counterpart) — this function only owns rendering and the accordion's
# open/closed flag. Wired into the central Stratagems list
# (uiLayout.gameProtocoll._render_stratagem_column, Task 5) and the reactive
# GO box below (render_reactive_stratagem_box, Task 6/S133 Paket 3a) — the
# one card builder both surfaces share, per S130's no-parallel-structure
# finding.


def _resolve_go_card_action(
    accordion_key: str,
    has_rule_text: bool,
    state: GoCardState,
    on_use: Callable[[], None] | None,
    on_undo: Callable[[], None] | None,
) -> None:
    """`on_click` handler for the GO card's action button.

    Must run as an `on_click` callback, not inline after the button (see
    `render_go_card` docstring): it writes `st.session_state[accordion_key]`,
    and that key already belongs to the expander widget rendered earlier in
    the same script run — Streamlit forbids reassigning a keyed widget's
    session_state value later in the *same* run (`StreamlitAPIException`).
    A callback runs between the click and the next script run, before the
    expander is re-instantiated, so the reset is legal there.
    """
    if has_rule_text:
        st.session_state[accordion_key] = False
    if state == "used" and on_undo is not None:
        on_undo()
    elif state == "ready" and on_use is not None:
        on_use()


def render_go_card(
    key: str,
    name: str,
    cp_cost: int,
    state: GoCardState,
    *,
    keywords: list[str] | None = None,
    rule_text: str = "",
    compact: bool = False,
    locked_reason: str | None = None,
    target_name: str | None = None,
    expanded_content: Callable[[], None] | None = None,
    on_use: Callable[[], None] | None = None,
    on_undo: Callable[[], None] | None = None,
) -> None:
    """Render one GO card: one bordered container, header + button + accordion inside.

    `key` must be unique per card instance (e.g. ``f"{faction}_{strat.id}"``) —
    it seeds the container's widget key, the action button's widget key and
    the accordion's session_state flag.

    Single container (S133-D Befund 2, generalised beyond Desperate Breakout):
    the whole card — header line, action button, rule-text accordion, and any
    ``expanded_content`` — renders inside ONE ``st.container(border=True,
    key=...)``. The K1 version instead drew its border as an HTML ``<div>``
    around only the header text (in the left of two ``st.columns``), so the
    button (right column) and the rule-text accordion (a separate top-level
    element rendered after both columns closed) were never actually inside
    that border — nothing in the DOM grouped them, they only happened to sit
    below a bordered-looking box. `go_card_container_style()` recolours this
    one container's border per state (Gold-Primary ready/used, dimmed
    dormant/locked, §6.5) via a scoped ``st-key-<key>`` CSS override, since
    Streamlit's container border alone only offers one fixed theme colour.

    Accordion fix (S130 root cause, design_system.md §6.1): a bare
    ``st.expander(label, expanded=False)`` only sets the widget's *initial*
    value — once a user opens it, Streamlit keeps that open state across every
    later rerun on its own, regardless of what `expanded=` the code passes on
    the next run (there is no `key`, so nothing round-trips through
    `session_state` to let the code force it shut again). Giving the expander
    an explicit `key` makes `st.session_state[key]` the single source of
    truth: ordinary reruns leave the user's own toggle alone, but the action
    button's callback (`_resolve_go_card_action`) explicitly resets the flag
    to False on every Use/Undo — closing the accordion again unless the user
    re-opens it.

    on_use/on_undo — invoked when the button is pressed in the "ready"/"used"
    state respectively; not called for "dormant"/"locked" (button rendered
    disabled, so this never fires for them regardless).

    target_name — shown on the header line (S133-D Befund 3): which unit this
    GO is bound to, so using it never happens against an unnoticed selection.

    expanded_content — an optional callable rendering additional widgets (e.g.
    a table-roll input + confirm button for a GO whose resolution needs more
    than Use/Undo, such as Desperate Breakout) *inside* this same bordered
    container, directly under the header/button row — never a free-floating
    block elsewhere in the phase flow (S133-D Befund 2).
    """
    box_key = f"go_card_box_{key}"
    st.markdown(go_card_container_style(box_key, state), unsafe_allow_html=True)

    accordion_key = f"go_card_rule_open_{key}"

    with st.container(border=True, key=box_key):
        card_col, action_col = st.columns([5, 2])
        with card_col:
            st.markdown(
                go_card_html(
                    name,
                    cp_cost,
                    state,
                    keywords=keywords,
                    compact=compact,
                    locked_reason=locked_reason,
                    target_name=target_name,
                ),
                unsafe_allow_html=True,
            )

        with action_col:
            st.button(
                action_slot_text(state),
                key=f"go_card_action_{key}",
                disabled=state in ("dormant", "locked"),
                on_click=_resolve_go_card_action,
                args=(accordion_key, bool(rule_text), state, on_use, on_undo),
            )

        if rule_text:
            with st.expander("Rule text", key=accordion_key, expanded=False):
                st.caption(rule_text)

        if expanded_content is not None:
            expanded_content()


def _clear_pending_transport_destroyed() -> None:
    st.session_state.pending_transport_destroyed = None


def _maybe_flag_transport_destroyed(
    faction: str, uid: str, unit: Unit, was_destroyed_before: bool
) -> None:
    """Open the Emergency Disembarkation reactive window when a TRANSPORT is destroyed.

    Compares before/after `destroyed` state so a rerun that leaves an already-dead
    TRANSPORT alone does not keep re-opening the window. Coverage note: this is
    called from every damage-application choke point within this session's scope
    (`wound_adjustment_buttons`, `_render_damage_block`, and fightPhase.py's
    post-fight mortal-wound handler) — psychic-phase mortal wounds (Smite, Perils)
    are NOT covered (psychicPhase.py is outside Plan 015's file scope this
    session; documented as a known gap in the session report).
    """
    if was_destroyed_before or not unit.has_keyword("TRANSPORT"):
        return
    _, unit_state = lookup(faction, uid)
    if unit_state.get("destroyed"):
        st.session_state.pending_transport_destroyed = {"faction": faction, "uid": uid}


def _render_pending_emergency_disembarkation(faction: str) -> None:
    """Render the Emergency Disembarkation box in the TRANSPORT owner's own column.

    `player: both` in the YAML means either side's column filter would pass this
    stratagem — the real gate is ownership: only the player whose TRANSPORT was
    just destroyed may use it, so this checks `faction` against the marker
    directly rather than routing through the active/inactive split.
    """
    marker = st.session_state.get("pending_transport_destroyed")
    if not marker or marker.get("faction") != faction:
        return
    try:
        unit, _ = lookup(faction, marker["uid"])
    except KeyError:
        st.session_state.pending_transport_destroyed = None
        return
    render_reactive_stratagem_box(
        faction,
        phase=PHASES[st.session_state.get("phase_idx", 0)][1],
        event="on_destroy",
        decline_key=marker["uid"],
        context_caption=f"{unit.name_en} (TRANSPORT) was destroyed.",
        on_resolved=_clear_pending_transport_destroyed,
    )


# ---------------------------------------------------------------------------
# 6d-v2 Attack sequence — shared utilities
# ---------------------------------------------------------------------------


def _empty_attack_declaration() -> dict:  # type: ignore[type-arg]
    return {
        "active": False,
        "atk_faction": "",
        "atk_uid": "",
        "phase_key": "",
        "use_melee": False,
        "in_melee": False,
        "entries": [],
    }


def _next_declaration_seq() -> int:
    """Monotonic counter namespacing per-resolution widget keys.

    Without it, res_/rp_ keys from an earlier resolution of the same unit and
    target survive in session_state and the new tabs start as already applied.
    """
    seq = int(st.session_state.get("attack_decl_seq", 0)) + 1
    st.session_state.attack_decl_seq = seq
    return seq


def _round_choice_source_label(player: str) -> str:
    from gameMechanic.game_state import (  # noqa: PLC0415
        faction_dir_for,
        round_choice_state_key,
    )
    from gameObjects.loader import (  # noqa: PLC0415
        load_round_choice_abilities,
        load_round_choice_label,
    )

    faction_dir = faction_dir_for(player)
    active_id = st.session_state.get(round_choice_state_key(player, "active"))
    directive = st.session_state.get(round_choice_state_key(player, "directive"))
    if not active_id or not directive:
        return load_round_choice_label(faction_dir)
    round_choices = load_round_choice_abilities(faction_dir)
    p = next((rc for rc in round_choices if rc.id == active_id), None)
    return f"{p.name_en} ({directive.capitalize()})" if p else load_round_choice_label(faction_dir)


def _round_choice_short_label(player: str) -> str:
    """Short protocol name for compact dice badges — drops the 'Protocol of the '
    qualifier and the directive suffix, matching the unitCard directive badge."""
    from gameMechanic.game_state import (  # noqa: PLC0415
        faction_dir_for,
        round_choice_state_key,
        short_round_choice_label,
    )
    from gameObjects.loader import load_round_choice_abilities  # noqa: PLC0415

    active_id = st.session_state.get(round_choice_state_key(player, "active"))
    abilities = load_round_choice_abilities(faction_dir_for(player))
    p = next((rc for rc in abilities if rc.id == active_id), None)
    return short_round_choice_label(p.name_en) if p else ""


def _collect_atk_modifiers(
    atk_faction: str,
    atk_state: dict,  # type: ignore[type-arg]
    phase_key: str,
    use_melee: bool,
    def_uid: str = "",
) -> list[dict]:  # type: ignore[type-arg]
    """Collect hit/wound modifiers for this attack from round-choice abilities, buffs, and active_modifiers.

    `def_uid` scopes defender-registered modifiers (e.g. Shadows of Drazak, Whirling
    Onslaught — reactive GOs the DEFENDER activates on their own targeted unit,
    S135 Paket 4a) to attacks made against that exact unit: only a
    `target: "defender"` entry whose `unit_key` matches `def_uid` applies here,
    mirroring `stratagem_strength_bonus`'s attacker-side `unit_key` scoping so
    one unit's activated GO never silently debuffs attacks against a different
    unit. `target: "attacker"/"any"` entries stay unscoped (pre-existing
    behaviour, unchanged) — they are registered by the attacking unit's own
    stratagem use, and the caller only ever renders one attacker's tabs at a
    time.
    """
    from gameMechanic.ability_engine import get_active_round_choice_modifier  # noqa: PLC0415

    mods: list[dict] = []  # type: ignore[type-arg]
    try:
        proto = get_active_round_choice_modifier(atk_faction, phase_key, use_melee)
        label = _round_choice_source_label(atk_faction)
        if proto.get("hit"):
            mods.append(
                {
                    "label": label,
                    "value": proto["hit"],
                    "roll_type": "hit",
                    "source": "round_choice",
                }
            )
        if proto.get("wound"):
            mods.append(
                {
                    "label": label,
                    "value": proto["wound"],
                    "roll_type": "wound",
                    "source": "round_choice",
                }
            )
    except KeyError:
        pass
    for b in atk_state.get("active_buffs", []):
        if b.get("effect_type") == "buff_roll":
            mods.append(
                {
                    "label": b.get("badge_label", "Buff"),
                    "value": 1,
                    "roll_type": "hit",
                    "source": "buff",
                }
            )
    for m in st.session_state.get("active_modifiers", []):
        eff = m.get("effect", {})
        rt = eff.get("roll_type")
        if rt not in ("hit", "wound"):
            continue
        tgt = eff.get("target", "attacker")
        applies = tgt in ("attacker", "any") or (
            tgt == "defender" and def_uid and m.get("unit_key") == def_uid
        )
        if not applies:
            continue
        mods.append(
            {
                "label": m.get("source", "Modifier"),
                "value": eff.get("value", 0),
                "roll_type": rt,
                "source": "stratagem",
            }
        )
    return mods


def _collect_def_save_modifiers(
    def_faction: str,
    phase_key: str,
    use_melee: bool,
    def_uid: str = "",
) -> list[dict]:  # type: ignore[type-arg]
    """Collect save modifiers for the defender from round-choice abilities and active_modifiers.

    Note: light_cover_if_stationary (Eternal Guardian D1) is NOT collected here — it is
    injected via the Light Cover checkbox mechanic in the render path (Variante C), so
    the +1 from the checkbox is applied once automatically. Adding it here AND via the
    checkbox would cause a double-+1 modifier.
    """
    mods: list[dict] = []  # type: ignore[type-arg]
    for m in st.session_state.get("active_modifiers", []):
        eff = m.get("effect", {})
        if eff.get("roll_type") == "save" and eff.get("target") in ("defender", "any"):
            mods.append({"label": m.get("source", "Modifier"), "value": eff.get("value", 0)})
    return mods


# ---------------------------------------------------------------------------
# 6d-v2 Damage + RP blocks
# ---------------------------------------------------------------------------


def _rapid_fire_caption(weapon_type: str, range_inches: int) -> str | None:
    """Generate Rapid Fire caption text if applicable.

    Returns the caption string for Rapid Fire weapons showing half-range, or None
    if the weapon is not Rapid Fire or has no range.

    Implements R-COMBAT-17 (Klasse C): App displays Rapid Fire range hint.
    """
    if weapon_type.startswith("Rapid Fire") and range_inches > 0:
        half = range_inches // 2
        return f'[RAPID FIRE · {range_inches}" · ½ = {half}"]'
    return None


def _rp_directive_hints(def_faction: str) -> list[str]:
    """Caption strings for active round-choice directives that grant an RP re-roll.

    Pure: reads session state via the engine, returns display text. The label is
    data-driven from the directive's YAML name — no faction literals.
    """
    from gameMechanic.ability_engine import get_active_rp_modifiers  # noqa: PLC0415
    from gameMechanic.game_state import faction_dir_for  # noqa: PLC0415

    try:
        faction_dir_for(def_faction)  # validate player slot; raises if unknown
    except KeyError:
        return []
    if not get_active_rp_modifiers(def_faction).get("rp_reroll"):
        return []
    return [f"⟳ {_round_choice_source_label(def_faction)}: re-roll one RP die."]


def _render_rp_block(
    def_unit: Unit,
    def_faction: str,
    def_uid: str,
    models_lost: int,
    tab_key: str,
) -> None:
    """Render the revive block after damage if the unit has a matching ability.

    Data-driven (INV-4b): gate, label, dice formula and success threshold come
    from the faction's YAML-declared revive ability (effect type ``reanimate``,
    trigger event ``after_enemy_attack`` — e.g. Necron Reanimation Protocols);
    src/ knows only the generic effect shape.
    """
    from gameMechanic.ability_engine import (  # noqa: PLC0415
        get_after_attack_revive_ability,
        revive_dice_count,
    )
    from gameMechanic.unit_mutations import heal_unit  # noqa: PLC0415

    if models_lost <= 0:
        return
    unit_state = st.session_state.get(units_key_for(def_faction), {}).get(def_uid, {})
    ability = get_after_attack_revive_ability(def_faction, def_unit, unit_state)
    if ability is None:
        return

    rp_key = f"rp_{tab_key}"
    rp_state = st.session_state.get(rp_key, {})
    if rp_state.get("applied"):
        mb = rp_state.get("models_back", 0)
        if mb > 0:
            st.caption(f"RP: {mb} models returned {SYM_CHECK}")
        return

    rp_dice = revive_dice_count(ability.effect.amount, models_lost, def_unit.wounds)
    threshold = f" · Erfolg: {ability.effect.success_on}+" if ability.effect.success_on else ""
    st.markdown(
        f"**{ability.name_en.upper()}** &nbsp; "
        f"{models_lost} × {def_unit.name_en} gefallen → **{rp_dice} Würfel**{threshold}"
    )
    for hint in _rp_directive_hints(def_faction):
        st.caption(hint)
    # Half-width block — keep the RP entry compact
    rp_col, _ = st.columns(2)
    models_back = rp_col.number_input(
        "Modelle zurück",
        min_value=0,
        max_value=models_lost,
        step=1,
        key=f"rp_mb_{tab_key}",
    )
    c1, c2 = rp_col.columns(2)
    if c1.button("RP anwenden", key=f"rp_apply_{tab_key}", type="primary"):
        if int(models_back) > 0:
            heal_unit(def_uid, def_faction, int(models_back) * def_unit.wounds, def_unit)
        st.session_state[rp_key] = {"applied": True, "models_back": int(models_back)}
        st.rerun()
    if c2.button("Überspringen", key=f"rp_skip_{tab_key}"):
        st.session_state[rp_key] = {"applied": True, "models_back": 0}
        st.rerun()


def _render_subgroup_selector(
    def_unit: Unit,
    def_state: dict,  # type: ignore[type-arg]
    active_groups: list[ModelGroup],
    locked_gid: str | None,
    dmg_col: Any,
    tab_key: str,
) -> str:
    """Defender's per-group damage allocation (Zustand A/B). Returns the target gid.

    A — no wounded model: free radio choice (default: lowest priority).
    B — a model is wounded-but-alive: choice is forced onto that group and a
        warning explains the 9E lock. Zustand C (a group wiped out) is reported
        in the post-apply summary, not here.
    """
    gw: dict[str, int] = def_state["group_wounds"]

    def _label(group: ModelGroup) -> str:
        weapons = ", ".join(w.name_en for w in group.weapons) or group.name_en
        return f"{group.name_en} — {weapons} ({gw.get(group.id, 0)} HP)"

    if locked_gid is not None:
        locked = next((g for g in active_groups if g.id == locked_gid), None)
        if locked is not None:
            wval = def_unit.group_wound_value(locked)
            front = gw.get(locked_gid, 0) % wval or wval
            dmg_col.warning(
                f"► Angeschlagenes Modell in **{locked.name_en}** (noch {front} LP) "
                "muss zuerst abgehandelt werden."
            )
        return locked_gid

    ids = [g.id for g in active_groups]
    return cast(
        str,
        dmg_col.radio(
            "Schaden zuweisen an Subgruppe",
            options=ids,
            format_func=lambda gid: _label(next(g for g in active_groups if g.id == gid)),
            key=f"dmg_target_grp_{tab_key}",
        ),
    )


def _render_damage_block(  # type: ignore[no-untyped-def]
    def_unit: Unit,
    def_faction: str,
    def_uid: str,
    profile,
    atk_faction: str,
    atk_unit_name: str,
    phase_key: str,
    tab_key: str,
) -> None:
    """Render damage input, apply button, post-apply summary, and RP block."""
    from gameMechanic.combat import apply_damage_attacks  # noqa: PLC0415
    from gameMechanic.game_log import log_action  # noqa: PLC0415
    from gameMechanic.game_state import units_key_for  # noqa: PLC0415
    from gameMechanic.unit_mutations import (  # noqa: PLC0415
        apply_damage,
        get_locked_group,
        select_damage_target_group,
    )

    res_key = f"res_{tab_key}"
    tab_state = st.session_state.get(res_key, {})

    if tab_state.get("applied"):
        m_lost = tab_state.get("models_lost", 0)
        mw = tab_state.get("mortal_wounds", 0)
        total = tab_state.get("total_damage", 0)
        st.success(f"{SYM_CHECK} {m_lost} models · {mw} MW · {total} damage applied")
        # Zustand C — a directed subgroup was wiped out by the last apply.
        for gname, weapons in tab_state.get("wiped_groups", []):
            st.warning(
                f"{SYM_CROSS} Subgruppe **{gname}** verloren — {weapons} nicht mehr verfügbar"
            )
        # Command Re-Roll (core_rules.txt Z. 3124-3130): a damage roll is the
        # attacker's dice, so `atk_faction` pays — reopens the same fields the
        # plain Reset below reopens, plus the CP/usage bookkeeping Reset alone
        # does not do.
        render_inline_command_reroll(
            atk_faction,
            phase_key,
            reopen_key=f"dmg_{tab_key}",
            on_reroll=lambda: st.session_state.pop(res_key, None),
        )
        # RP is rolled once per defender unit after the whole attacking unit has
        # resolved (render_attack_resolution), not per weapon tab.
        if st.button(f"{SYM_RESET} Reset", key=f"res_reset_{tab_key}"):
            st.session_state.pop(res_key, None)
            st.rerun()
        return

    st.markdown("**DAMAGE**")
    is_multi_lp = def_unit.wounds > 1
    is_single_model = def_unit.models_max <= 1
    dmg_str = str(profile.damage)
    dmg_label = f"D{dmg_str}" if not dmg_str.lstrip("+-").isdigit() else f"{dmg_str} fixed"
    st.markdown(
        f'<span style="font-size:1.05rem;font-weight:700;color:#fbbf24;">{dmg_label}</span> '
        f"per failed save · Target: "
        f'<span style="font-size:1.05rem;font-weight:700;color:#fbbf24;">'
        f"{def_unit.wounds} HP/model</span>",
        unsafe_allow_html=True,
    )

    # Half-width block — the damage entry does not need the whole displayArea
    dmg_col, _ = st.columns(2)

    _, def_state = lookup(def_faction, def_uid)
    is_group_wounds = bool(def_state.get("group_wounds"))
    weapon_special = _detect_weapon_special(profile)

    chosen_gid = None
    if is_group_wounds:
        # 9E loss allocation: when more than one subgroup is still alive, the
        # defender chooses which group takes the damage (Zustand A); a wounded-
        # but-alive model locks its group (Zustand B). Single active group → no
        # choice, fall back to the priority-spill default (damage_active_group_id
        # stays None).
        active_groups = sorted(
            (g for g in def_unit.model_groups if def_state["group_models"].get(g.id, 0) > 0),
            key=lambda g: g.priority,
        )
        if len(active_groups) > 1:
            locked_gid = get_locked_group(def_uid, def_faction, def_unit)
            chosen_gid = _render_subgroup_selector(
                def_unit, def_state, active_groups, locked_gid, dmg_col, tab_key
            )
        # Mixed per-model wounds in one unit (e.g. Szarekh 16 + Menhirs 7): the
        # losses are distributed by group/priority in apply_damage, so the user
        # enters total damage that got through rather than models/front wounds.
        gw_total = sum(def_state["group_wounds"].values())
        dmg_col.caption(
            "Per-group HP: "
            + " · ".join(
                f"{g.name_en} {def_state['group_wounds'].get(g.id, 0)}"
                for g in def_unit.model_groups
            )
        )
        damage_in = dmg_col.number_input(
            f"Total damage dealt (0–{gw_total})",
            min_value=0,
            max_value=gw_total,
            step=1,
            key=f"gwd_{tab_key}",
        )
        mortal_wounds = 0
        if weapon_special.get("has_mortal_wounds"):
            mortal_wounds = dmg_col.number_input(
                "Mortal Wounds", min_value=0, step=1, key=f"mw_{tab_key}"
            )
        total = int(damage_in) + int(mortal_wounds)
        models_lost = 0  # recomputed post-apply from group_models delta
    else:
        models_lost = 0
        if not is_single_model:
            models_lost = dmg_col.number_input(
                "Models lost",
                min_value=0,
                step=1,
                key=f"ml_{tab_key}",
            )

        wounds_on_front = 0
        if is_multi_lp:
            wf_label = (
                f"Wounds taken (0–{def_unit.wounds - 1})"
                if is_single_model
                else f"Wounds on front model (0–{def_unit.wounds - 1})"
            )
            wounds_on_front = dmg_col.number_input(
                wf_label,
                min_value=0,
                max_value=def_unit.wounds - 1,
                step=1,
                key=f"wf_{tab_key}",
            )

        mortal_wounds = 0
        if weapon_special.get("has_mortal_wounds"):
            mortal_wounds = dmg_col.number_input(
                "Mortal Wounds",
                min_value=0,
                step=1,
                key=f"mw_{tab_key}",
            )

        total = apply_damage_attacks(
            int(models_lost), int(wounds_on_front), int(mortal_wounds), def_unit.wounds
        )
    btn_label = (
        f"{SYM_SWORDS} Apply {total} Damage → {def_unit.name_en}" if total > 0 else "Apply Damage"
    )
    if dmg_col.button(btn_label, key=f"apply_{tab_key}", type="primary", use_container_width=True):
        models_before = def_state.get("models", 0) if is_group_wounds else 0
        groups_before = dict(def_state.get("group_models", {})) if is_group_wounds else {}
        if is_group_wounds:
            # Direct the next apply to the chosen group (Zustand A/B). Single
            # active group → clear the target so the priority-spill default runs.
            if chosen_gid is not None:
                select_damage_target_group(def_uid, def_faction, chosen_gid)
            else:
                def_state["damage_active_group_id"] = None
        was_destroyed_before = bool(def_state.get("destroyed"))
        if total > 0:
            apply_damage(def_uid, def_faction, total, def_unit, resolved=True)
            _maybe_flag_transport_destroyed(def_faction, def_uid, def_unit, was_destroyed_before)
        wiped_groups: list = []  # type: ignore[type-arg]
        if is_group_wounds:
            # Real loss only known after priority-based distribution
            _, def_state_after = lookup(def_faction, def_uid)
            models_lost = max(0, models_before - def_state_after.get("models", 0))
            gm_after = def_state_after.get("group_models", {})
            wiped_groups = [
                (g.name_en, ", ".join(w.name_en for w in g.weapons) or g.name_en)
                for g in def_unit.model_groups
                if groups_before.get(g.id, 0) > 0 and gm_after.get(g.id, 0) == 0
            ]
        wounds_on_front = 0
        decl = st.session_state.get("attack_declaration", {})
        atk_uid = decl.get("atk_uid", "")
        atk_f = decl.get("atk_faction", "")
        if atk_uid and atk_f:
            atk_flags = (
                st.session_state[units_key_for(atk_f)].get(atk_uid, {}).get("turn_flags", {})
            )
            if phase_key == "shooting":
                atk_flags["shot"] = True
            elif phase_key == "fight":
                atk_flags["fought"] = True
                try:
                    atk_unit, _ = lookup(atk_f, atk_uid)
                    if atk_unit.get_triggered_effect("after_fight", "fight", "mortal_after_melee"):
                        st.session_state.pending_triggered_relic = {
                            "uid": atk_uid,
                            "faction": atk_f,
                            "step": "initial",
                            "target_uid": None,
                            "target_faction": None,
                            "mortals": 0,
                        }
                except (StopIteration, KeyError):
                    pass
        log_action(
            st.session_state.round,
            phase_key,
            atk_unit_name,
            f"dealt {total} damage to {def_unit.name_en}",
        )
        st.session_state[res_key] = {
            "applied": True,
            "models_lost": int(models_lost),
            "wounds_on_front": int(wounds_on_front),
            "mortal_wounds": int(mortal_wounds),
            "total_damage": total,
            "wiped_groups": wiped_groups,
        }
        st.rerun()


# ---------------------------------------------------------------------------
# 6d-v2 Resolution tab
# ---------------------------------------------------------------------------


def _render_resolution_tab(
    entry: dict,  # type: ignore[type-arg]
    atk_faction: str,
    atk_unit: Unit,
    atk_state: dict,  # type: ignore[type-arg]
    use_melee: bool,
    phase_key: str,
    tab_key: str,
) -> None:
    """Render one resolution tab: Hit + Wound table + Save + Cover + Damage."""
    from gameMechanic.combat import (  # noqa: PLC0415
        resolve_attack_modifiers,
        resolve_fnp,
        resolve_save,
    )
    from gameObjects.loader import resolve_bracket_stats  # noqa: PLC0415

    def_faction = entry["def_faction"]
    def_uid = entry["def_uid"]
    atk_uid = entry.get("atk_uid", "")
    weapon_name = entry["weapon_name"]
    profile_idx = entry["profile_idx"]
    models_count = entry["models_count"]
    # Per-group stat overrides carried from the declaration (Boss Nob etc.);
    # fall back to the unit-level stats for homogeneous groups.
    grp_strength = entry.get("atk_strength", atk_unit.strength)
    grp_attacks = cast(int, entry.get("atk_attacks", atk_unit.attacks))
    grp_ws = entry.get("atk_ws")
    grp_bs = entry.get("atk_bs")

    def_unit, def_state = lookup(def_faction, def_uid)

    # Resolve weapon + profile
    in_melee_flag = st.session_state.get("attack_declaration", {}).get("in_melee", False)
    if use_melee:
        weapons = [w for w in atk_unit.weapons if any(p.is_melee for p in w.profiles)]
    elif in_melee_flag:
        weapons = [
            w
            for w in atk_unit.weapons
            if any(not p.is_melee and p.weapon_type.startswith("Pistol") for p in w.profiles)
        ]
    else:
        weapons = [w for w in atk_unit.weapons if any(not p.is_melee for p in w.profiles)]

    weapon = next((w for w in weapons if w.name_en == weapon_name), weapons[0] if weapons else None)
    if weapon is None:
        st.error("Weapon not found.")
        return
    profiles = [p for p in weapon.profiles if p.is_melee == use_melee]
    if not profiles:
        profiles = weapon.profiles
    profile = profiles[min(profile_idx, len(profiles) - 1)]

    from gameMechanic.ability_engine import (  # noqa: PLC0415
        ability_invuln_save,
        buff_stat_bonus,
        get_active_round_choice_ap_on_wound_6,
        get_active_round_choice_strength_if_charged,
        get_short_label_for_effect_type,
        stratagem_strength_bonus,
    )

    str_bonus = buff_stat_bonus(atk_faction, atk_unit, "strength")
    # Disruption Fields (and similar stratagems): +1 S from an active_modifiers
    # entry with roll_type=="strength", folded in the same way as the faction-
    # ability buff above so the WOUND block highlights the raised S in blue.
    str_bonus += stratagem_strength_bonus(st.session_state.get("active_modifiers", []), atk_uid)
    # Hungry Void D2: +1 S in melee if the attacker charged, was charged, or did a
    # Heroic Intervention. Folded into str_bonus so the WOUND block highlights the
    # raised S in blue exactly like a WAAAGH! strength buff.
    try:
        str_bonus += get_active_round_choice_strength_if_charged(
            atk_faction, atk_state.get("turn_flags", {}), use_melee
        )
        on_six_ap = get_active_round_choice_ap_on_wound_6(atk_faction, use_melee)
        on_six_label = (
            get_short_label_for_effect_type(atk_faction, "ap_on_unmod_wound_6")
            or _round_choice_short_label(atk_faction)
            if on_six_ap
            else ""
        )
    except KeyError:
        on_six_ap, on_six_label = 0, ""
    # str_bonus is added after weapon-strength calculation so that ×N weapons
    # give (User×N) + bonus rather than (User + bonus)×N. Base strength is the
    # group's value (e.g. Boss Nob S 5), not the unit-level S.
    strength = _parse_strength(profile.strength, grp_strength) + str_bonus
    ap = profile.ap
    skill_label = "WS" if use_melee else "BS"
    advanced = atk_state.get("turn_flags", {}).get("advanced", False)

    per_model_hp = atk_state.get("current_wounds", atk_unit.wounds) // max(
        1, atk_state.get("models", atk_unit.models_max)
    )
    live = resolve_bracket_stats(atk_unit, per_model_hp)
    # Per-group WS/BS override (e.g. Boss Nob WS 2+) wins over the bracket value.
    ws_str = grp_ws or live["ws"]
    bs_str = grp_bs or live["bs"]
    skill = int(str(ws_str).rstrip("+")) if use_melee else int(str(bs_str).rstrip("+"))

    is_shooting = phase_key == "shooting"
    is_fight = phase_key == "fight"

    # Cover checkboxes live inside their own resolution block (Dense → HIT,
    # Light/Heavy → SAVE), so each weapon×target tab carries its own cover state.
    cover_key = tab_key

    # Variante C: determine auto_light_cover BEFORE reading checkbox state so the
    # modifier reaches resolve_save on the same Streamlit run that the directive
    # first becomes active (not one run later via session_state write).
    # Also resolve shoot_after_fall_back (Conquering Tyrant D2) here so its −1 Hit
    # modifier is folded in before resolve_attack_modifiers runs.
    if is_shooting:
        from gameMechanic.ability_engine import (  # noqa: PLC0415
            get_active_round_choice_ignores_cover_half_range,
            get_active_round_choice_light_cover_if_stationary,
            get_active_round_choice_shoot_after_fall_back,
            get_short_label_for_effect_type,
        )
        from uiLayout.dice_compose import light_cover_label  # noqa: PLC0415

        auto_light_cover = get_active_round_choice_light_cover_if_stationary(def_faction, def_uid)
        fall_back_hit_mod = get_active_round_choice_shoot_after_fall_back(atk_faction, atk_uid)
    else:
        auto_light_cover = False
        fall_back_hit_mod = 0

    # Read cover checkbox states (checkboxes are rendered later, state read now)
    dense_cover = is_shooting and st.session_state.get(f"dense_cover_{cover_key}", False)
    # Fold auto_light_cover into light_cover so resolve_save sees the +1 on the
    # same run it is first computed (avoids one-rerun delay of the old
    # session_state-write approach).
    light_cover = is_shooting and (
        auto_light_cover or st.session_state.get(f"light_cover_{cover_key}", False)
    )
    heavy_cover = (
        is_fight
        and st.session_state.get(f"heavy_cover_{cover_key}", False)
        and not def_state.get("turn_flags", {}).get("charged")
    )

    # Build modifier lists including cover effects
    base_atk_mods = _collect_atk_modifiers(atk_faction, atk_state, phase_key, use_melee, def_uid)
    base_save_mods = _collect_def_save_modifiers(def_faction, phase_key, use_melee, def_uid)

    weapon_special = _detect_weapon_special(profile)

    final_atk_mods = list(base_atk_mods)
    final_save_mods = list(base_save_mods)
    if weapon_special["hit_roll_penalty"]:
        final_atk_mods.append(
            {"label": "−1 to Hit", "value": -1, "roll_type": "hit", "source": "weapon"}
        )
    if fall_back_hit_mod:
        # D2 (shoot_after_fall_back): −1 Hit when shooting after Fall Back (9E canonical).
        # Label is data-driven from YAML via get_short_label_for_effect_type — no hardcoded
        # faction string (Generic-src rule). Falls back to generic round-choice label.
        fall_back_label = get_short_label_for_effect_type(
            atk_faction, "shoot_after_fall_back"
        ) or _round_choice_short_label(atk_faction)
        final_atk_mods.append(
            {
                "label": f"{fall_back_label} (Fall Back)",
                "value": fall_back_hit_mod,
                "roll_type": "hit",
                "source": "round_choice",
            }
        )
    if dense_cover:
        final_atk_mods.append(
            {"label": "Dense Cover", "value": -1, "roll_type": "hit", "source": "terrain"}
        )
    if light_cover:
        final_save_mods.append({"label": "Light Cover", "value": 1})
    if heavy_cover:
        final_save_mods.append({"label": "Heavy Cover", "value": 1})

    atk_result = resolve_attack_modifiers(
        skill=skill,
        strength=strength,
        toughness=def_unit.toughness,
        weapon_type=profile.weapon_type,
        advanced=advanced,
        modifiers=final_atk_mods,
        use_melee=use_melee,
    )
    ability_inv = ability_invuln_save(def_faction, def_unit)
    native_inv = def_unit.invuln_save
    if ability_inv is not None and (native_inv is None or ability_inv < native_inv):
        effective_invuln: int | None = ability_inv
        invuln_from_ability = True
    else:
        effective_invuln = native_inv
        invuln_from_ability = False

    save_result = resolve_save(
        base_save=def_unit.save,
        invuln_save=effective_invuln,
        ap=ap,
        save_modifiers=final_save_mods,
    )
    fnp_value = resolve_fnp(def_unit.fnp, profile.ignores_fnp)

    # Header
    atk_override = entry.get("atk_override")
    atk_count = (
        str(atk_override)
        if atk_override is not None
        else _compute_attacks(
            profile.attacks, models_count, grp_attacks, profile.effect, profile.max_attacks
        )
    )
    # D5: no redundant weapon profile line — S/T, AP, Sv and damage all appear
    # in their blocks below. Only the attack count is needed up front.
    st.markdown(
        f"**{atk_unit.name_en}** → **{def_unit.name_en}**  \n"
        f"_{weapon.name_en}_ — "
        f'<span style="font-size:1.05rem;font-weight:700;color:#fbbf24;">{atk_count}</span>'
        " Attacks",
        unsafe_allow_html=True,
    )

    # HIT BLOCK
    if weapon_special["auto_hit"]:
        st.markdown("**HIT** &nbsp; AUTO-HIT", unsafe_allow_html=True)
    else:
        _render_dice_roll_block("HIT", skill_label, atk_result["hit"], weapon_special)

    # Hit-Anker (design_system.md §6.2/§6.3, S135 Paket 4a): the defender's own
    # reactive GOs that debuff THIS attack's hit roll (e.g. Shadows of Drazak)
    # — trigger is "unit selected as target of an attack" (event="on_target"),
    # scoped to effect_type/effect_stat so a wound-roll GO sharing the same
    # (phase, event) window does not also show up here.
    render_reactive_stratagem_box(
        def_faction,
        phase_key,
        "on_target",
        decline_key=tab_key,
        context_caption=f"{def_unit.name_en} was selected as the target of an attack.",
        unit_key_for_modifier=def_uid,
        unit_for_conditions=def_unit,
        effect_type="debuff_roll",
        effect_stat="hit",
    )

    # Dense Cover checkbox: Shooting phase only, affects hit roll → in the HIT block
    if is_shooting:
        st.checkbox("Dense Cover (−1 Hit)", key=f"dense_cover_{cover_key}")

    st.markdown("")

    # WOUND BLOCK
    _render_dice_wound_block(
        strength,
        def_unit.toughness,
        atk_result["wound"]["stack"],
        strength_buff=str_bonus,
        on_six_ap=on_six_ap,
        on_six_label=on_six_label,
    )

    # Wound-Anker (design_system.md §6.2/§6.3, S135 Paket 4a): same trigger as
    # above, filtered to the wound-roll debuff (e.g. Whirling Onslaught).
    render_reactive_stratagem_box(
        def_faction,
        phase_key,
        "on_target",
        decline_key=tab_key,
        context_caption=f"{def_unit.name_en} was selected as the target of an attack.",
        unit_key_for_modifier=def_uid,
        unit_for_conditions=def_unit,
        effect_type="debuff_roll",
        effect_stat="wound",
    )

    st.markdown("---")

    # SAVE BLOCK
    _render_dice_save_block(save_result, ap, ability_invuln=invuln_from_ability)

    # Cover checkboxes for save modifiers (phase-bound) → in the SAVE block
    # Imports were already resolved at the top of this block (above resolve_save).
    if is_shooting:
        short = (
            get_short_label_for_effect_type(atk_faction, "ignore_cover_half_range")
            or _round_choice_short_label(atk_faction)
            if get_active_round_choice_ignores_cover_half_range(atk_faction)
            else None
        )
        if auto_light_cover:
            # Badge label is data-driven from YAML (e.g. "Eternal Guardian"); always non-empty
            # for any correctly wired directive. Empty string silently omits the badge.
            # Buff-Badges are green per design_colors.md §3 — :green-badge not :blue-badge.
            # No session_state write here: light_cover was already folded in above; a
            # redundant write would trigger Streamlit's "widget value set via Session State"
            # warning alongside the disabled checkbox.
            d1_label = get_short_label_for_effect_type(def_faction, "light_cover_if_stationary")
            st.checkbox(
                light_cover_label(short) + (f"  :green-badge[{d1_label}]" if d1_label else ""),
                key=f"light_cover_{cover_key}",
                value=True,
                disabled=True,
            )
        else:
            st.checkbox(light_cover_label(short), key=f"light_cover_{cover_key}")
    if is_fight:
        def_charged = def_state.get("turn_flags", {}).get("charged", False)
        if not def_charged:
            st.checkbox("Heavy Cover (+1 Save vs Melee)", key=f"heavy_cover_{cover_key}")

    if def_unit.fnp is not None:
        st.markdown("")
        if fnp_value is None:
            st.markdown(f"~~**FNP**~~ ~~{def_unit.fnp}+~~ _(ignored)_")
        else:
            st.markdown(f"**FNP** &nbsp; [ {fnp_value}+ ]", unsafe_allow_html=True)

    st.markdown("---")

    # DAMAGE BLOCK
    _render_damage_block(
        def_unit,
        def_faction,
        def_uid,
        profile,
        atk_faction,
        atk_unit.name_en,
        phase_key,
        tab_key,
    )


# ---------------------------------------------------------------------------
# 6d-v2 Declaration phase
# ---------------------------------------------------------------------------


def reset_group_declaration_state() -> None:
    """Clear group-by-group declaration state (on unit switch, phase change, resolution).

    Also drops the per-target counter/profile widget keys (``decl_m_*``/``decl_a_*``/
    ``decl_p_*``); otherwise a stale count from a previous declaration reappears the
    next time the same group+target is selected, looking like a pre-made selection.
    """
    st.session_state.selected_model_group = None
    st.session_state.group_targets = {}
    st.session_state.group_decl = {}
    for k in list(st.session_state.keys()):
        if isinstance(k, str) and k.startswith(("decl_m_", "decl_a_", "decl_p_")):
            del st.session_state[k]
    for k in list(st.session_state.keys()):
        if isinstance(k, str) and k.startswith("group_autosel_done_"):
            del st.session_state[k]


def group_flow_attacker() -> tuple[str, str, Unit, dict] | None:  # type: ignore[type-arg]
    """Return (faction, uid, unit, state) when the selected unit declares via model groups."""
    sel = st.session_state.get("selected_unit")
    if not sel:
        return None
    faction, uid = sel
    unit, unit_state = lookup(faction, uid)
    if not unit.model_groups:
        return None
    return faction, uid, unit, unit_state


def is_group_target(def_faction: str, def_uid: str) -> bool:
    """True if the target is assigned to the currently selected model group."""
    gid = st.session_state.get("selected_model_group")
    if not gid:
        return False
    targets: dict = st.session_state.get("group_targets", {})  # type: ignore[type-arg]
    return (def_faction, def_uid) in targets.get(gid, [])


def _is_engaged_with(atk_state: dict, def_faction: str, def_uid: str) -> bool:  # type: ignore[type-arg]
    """True if the defender is in the attacker's melee_with list."""
    melee_with = atk_state.get("melee_with", [])
    return [def_faction, def_uid] in melee_with or (def_faction, def_uid) in melee_with


def _in_friendly_melee(atk_faction: str, def_faction: str, def_uid: str) -> bool:
    """True if the target is locked in melee with a unit friendly to the attacker.

    9E: a unit may not shoot into a combat involving friendly units.
    """
    def_state = st.session_state.get(units_key_for(def_faction), {}).get(def_uid, {})
    return any(fac == atk_faction for fac, _ in def_state.get("melee_with", []))


def _single_eligible_group(atk_unit: Unit, atk_state: dict, use_melee: bool, in_melee: bool):  # type: ignore[no-untyped-def, type-arg]
    """Return the sole undeclared, alive, weapon-capable group — or None.

    Mirrors the auto-select condition in render_group_cards so that
    group_target_selectable can anticipate the upcoming auto-select and keep
    target buttons enabled even before the center column has rendered.
    """
    group_models: dict[str, int] = atk_state.get("group_models", {})
    group_decl: dict = st.session_state.get("group_decl", {})  # type: ignore[type-arg]
    eligible = [
        g
        for g in atk_unit.model_groups
        if group_models.get(g.id, g.count) > 0
        and _group_phase_weapons(g, use_melee, in_melee)
        and group_decl.get(g.id) is None
    ]
    return eligible[0] if len(eligible) == 1 else None


def group_target_selectable(def_faction: str, def_uid: str) -> bool:
    """Whether ▷ may select this enemy as a target right now.

    Shooting: targets in melee with the attacker's friends are blocked (9E).
    Group flow: a group must be selected first; in the fight phase only
    engaged enemies are legal targets (Engagement Range, core rules).

    When the left column (enemy targets) renders before the center column
    (auto-select), selected_model_group may still be None even though
    auto-select will immediately pick the only eligible group.  We treat
    that case as "effectively selected" so target buttons stay enabled.
    """
    phase_key = PHASES[st.session_state.phase_idx][1]
    if phase_key not in ("shooting", "fight"):
        return True
    sel = st.session_state.get("selected_unit")
    if phase_key == "shooting" and sel and _in_friendly_melee(sel[0], def_faction, def_uid):
        return False
    info = group_flow_attacker()
    if info is None:
        return True
    if not st.session_state.get("selected_model_group"):
        # A group is not yet selected, but auto-select may be about to pick the
        # sole eligible group (render_group_cards runs later in the same Rerun).
        _, _, atk_unit, atk_state = info
        use_melee = phase_key == "fight"
        in_melee = atk_state.get("in_melee", False)
        if _single_eligible_group(atk_unit, atk_state, use_melee, in_melee) is None:
            return False
    if phase_key != "fight":
        return True
    _, _, _, atk_state = info
    return _is_engaged_with(atk_state, def_faction, def_uid)


def toggle_group_target(def_faction: str, def_uid: str) -> bool:
    """Assign/unassign a target to the selected model group. Returns True if handled."""
    gid = st.session_state.get("selected_model_group")
    info = group_flow_attacker()
    if not gid or info is None:
        return False
    if not group_target_selectable(def_faction, def_uid):
        return True  # consume the click — never fall back to selected_targets
    _, _, unit, unit_state = info
    group = next((g for g in unit.model_groups if g.id == gid), None)
    if group is None:
        return False

    targets: dict = dict(st.session_state.get("group_targets", {}))  # type: ignore[type-arg]
    current: list = list(targets.get(gid, []))  # type: ignore[type-arg]
    key = (def_faction, def_uid)
    if key in current:
        current.remove(key)
    else:
        alive = unit_state.get("group_models", {}).get(gid, group.count)
        phase_key = PHASES[st.session_state.phase_idx][1]
        # In shooting phase a single-model group can only shoot one target;
        # in fight phase even a 1-model group may split attacks across targets.
        current = [key] if (alive == 1 and phase_key != "fight") else current + [key]
    targets[gid] = current
    st.session_state.group_targets = targets
    return True


def _group_effective_attacks(atk_unit: Unit, group, atk_state: dict) -> int:  # type: ignore[no-untyped-def, type-arg]
    """Attacks per model for a group (before WAAAGH bonus).

    A group with its own ``attacks`` stat is fixed (e.g. Triarchal Menhirs A2).
    A group that uses the unit-level Attacks (e.g. Szarekh) is reduced by the unit
    damage bracket, keyed to *that group's own* per-model wounds — so a wounded
    Szarekh drops to A4/A2 while the (separate) Menhirs are unaffected.
    """
    if "attacks" in group.stats:
        return int(group.stats["attacks"])
    base = atk_unit.attacks or 0
    group_wounds = atk_state.get("group_wounds") or {}
    if atk_unit.damage_bracket and group.id in group_wounds:
        from gameObjects.loader import resolve_bracket_stats  # noqa: PLC0415

        models = atk_state.get("group_models", {}).get(group.id, group.count) or 1
        per_model_hp = group_wounds[group.id] // max(1, models)
        live = resolve_bracket_stats(atk_unit, per_model_hp)
        if live.get("attacks") is not None:
            try:
                return int(str(live["attacks"]).rstrip("+"))
            except (TypeError, ValueError):
                pass
    return int(base)


def front_group_hp(unit: Unit, state: dict) -> tuple[int, int]:  # type: ignore[type-arg]
    """Front-model HP for a per-group-wounds unit: (front_wounds, per_model_wounds).

    Returns the partly-wounded front model of the lowest-priority surviving group
    (the group currently taking damage), so the health bar reflects mixed wounds
    (e.g. Triarchal Menhirs 7 first, then Szarekh 16). Falls back to (0, 1) if no
    group has wounds left.
    """
    group_wounds: dict[str, int] = state.get("group_wounds") or {}
    for group in sorted(unit.model_groups, key=lambda g: g.priority):
        remaining = group_wounds.get(group.id, 0)
        if remaining <= 0:
            continue
        wval = unit.group_wound_value(group)
        partial = remaining % wval
        return (partial if partial > 0 else wval, wval)
    return (0, 1)


def _group_phase_weapons(group, use_melee: bool, in_melee: bool) -> list:  # type: ignore[no-untyped-def, type-arg]
    """Weapons of a group usable in the current phase (Pistols only while engaged)."""
    if in_melee and not use_melee:
        return [
            w
            for w in group.weapons
            if any(not p.is_melee and p.weapon_type.startswith("Pistol") for p in w.profiles)
        ]
    return [w for w in group.weapons if any(p.is_melee == use_melee for p in w.profiles)]


def _target_display_name(def_faction: str, def_uid: str) -> str:
    tgt_unit, _ = lookup(def_faction, def_uid)
    return tgt_unit.name_en


def render_group_cards(
    atk_faction: str,
    atk_uid: str,
    atk_unit: Unit,
    atk_state: dict,  # type: ignore[type-arg]
    use_melee: bool,
    phase_key: str,
    in_melee: bool = False,
) -> None:
    """Owner-side subUnitCards: select a group, review declared groups, start resolution.

    Rendered in the player area of the unit's owner. Declared groups collapse to a
    summary with an Edit button; the resolution starts once at least one group has
    declared attacks.
    """
    from gameMechanic.ability_engine import buff_stat_bonus  # noqa: PLC0415

    atk_bonus = buff_stat_bonus(atk_faction, atk_unit, "attacks")
    group_models: dict[str, int] = atk_state.get("group_models", {})
    group_decl: dict = st.session_state.get("group_decl", {})  # type: ignore[type-arg]
    group_targets: dict = st.session_state.get("group_targets", {})  # type: ignore[type-arg]
    sel_gid = st.session_state.get("selected_model_group")

    autosel_flag = f"group_autosel_done_{atk_uid}"
    if sel_gid is None and not st.session_state.get(autosel_flag):
        solo = _single_eligible_group(atk_unit, atk_state, use_melee, in_melee)
        if solo is not None:
            st.session_state.selected_model_group = solo.id
            st.session_state[autosel_flag] = True
            sel_gid = solo.id

    for group in atk_unit.model_groups:
        alive = group_models.get(group.id, group.count)
        if alive == 0:
            continue
        grp_weapons = _group_phase_weapons(group, use_melee, in_melee)
        if not grp_weapons:
            continue

        with st.container(border=True):
            entries = group_decl.get(group.id)
            if entries is not None and sel_gid != group.id:
                st.markdown(f"**{SYM_CHECK} {group.name_en}** ({alive})")
                for e in entries:
                    count = e.get("atk_override", e["models_count"])
                    if count > 0:
                        st.caption(
                            f"{e['weapon_name']} → {count} @ "
                            f"{_target_display_name(e['def_faction'], e['def_uid'])}"
                        )
                if st.button(
                    "✎ Edit",
                    key=f"editgrp_{atk_uid}_{group.id}",
                    use_container_width=True,
                ):
                    st.session_state.selected_model_group = group.id
                    st.rerun()
                continue

            is_sel = sel_gid == group.id
            label = (
                f"{SYM_COLLAPSE} {group.name_en} ({alive})"
                if is_sel
                else f"{SYM_EXPAND} {group.name_en} ({alive})"
            )
            if st.button(
                label,
                key=f"selgrp_{atk_uid}_{group.id}",
                type="primary" if is_sel else "secondary",
                use_container_width=True,
            ):
                st.session_state.selected_model_group = None if is_sel else group.id
                st.rerun()
            if use_melee:
                grp_attacks = _group_effective_attacks(atk_unit, group, atk_state)
                budget = _group_melee_budget(grp_weapons, alive, grp_attacks + atk_bonus)
                st.caption(f"{budget} attacks")
            st.caption(", ".join(w.name_en for w in grp_weapons))
            if is_sel:
                assigned = group_targets.get(group.id, [])
                melee_with = atk_state.get("melee_with", [])
                if phase_key == "fight" and melee_with:
                    st.caption("Targets (engaged):")
                    for entry in melee_with:
                        def_faction, def_uid = entry[0], entry[1]
                        _, def_state = lookup(def_faction, def_uid)
                        if def_state.get("destroyed") or def_state.get("in_reserve"):
                            continue
                        is_assigned = (def_faction, def_uid) in [(f, u) for f, u in assigned]
                        tgt_name = _target_display_name(def_faction, def_uid)
                        btn_label = (
                            f"{SYM_CHECK} {tgt_name}" if is_assigned else f"{SYM_ADD} {tgt_name}"
                        )
                        if st.button(
                            btn_label,
                            key=f"engtgt_{atk_uid}_{group.id}_{def_uid}",
                            type="primary" if is_assigned else "secondary",
                            use_container_width=True,
                        ):
                            toggle_group_target(def_faction, def_uid)
                            st.rerun()
                else:
                    if assigned:
                        for tgt_faction, tgt_uid in assigned:
                            st.caption(f"→ {_target_display_name(tgt_faction, tgt_uid)}")
                    else:
                        st.caption(
                            f"Designate a target ({SYM_EXPAND_ALT}) from the enemy army list."
                        )

    all_entries = [
        e
        for grp_entries in group_decl.values()
        for e in grp_entries
        if e.get("atk_override", e["models_count"]) > 0
    ]
    if st.button(
        "Start Resolution →",
        type="primary",
        disabled=not all_entries,
        key=f"start_res_{atk_uid}",
    ):
        st.session_state.attack_declaration = {
            "active": True,
            "atk_faction": atk_faction,
            "atk_uid": atk_uid,
            "phase_key": phase_key,
            "use_melee": use_melee,
            "in_melee": in_melee,
            "entries": all_entries,
            "seq": _next_declaration_seq(),
        }
        reset_group_declaration_state()
        st.rerun()


def render_group_assignment(
    atk_faction: str,
    atk_uid: str,
    atk_unit: Unit,
    atk_state: dict,  # type: ignore[type-arg]
    use_melee: bool,
    in_melee: bool = False,
) -> None:
    """Defender-side panel: assign attacks/models of the selected group to its targets.

    Rendered in the opposite player area. Writes the group's entries to
    st.session_state.group_decl when the player confirms the group.
    """
    gid = st.session_state.get("selected_model_group")
    if not gid:
        st.caption("Waiting — opponent selects a model group.")
        return
    group = next((g for g in atk_unit.model_groups if g.id == gid), None)
    if group is None:
        return
    alive = atk_state.get("group_models", {}).get(gid, group.count)
    tgts: list[tuple[str, str]] = st.session_state.get("group_targets", {}).get(gid, [])
    if not tgts:
        st.caption(f"← Designate a target ({SYM_EXPAND_ALT}) from your army list.")
        return

    from gameMechanic.ability_engine import buff_stat_bonus  # noqa: PLC0415

    atk_bonus = buff_stat_bonus(atk_faction, atk_unit, "attacks")
    grp_weapons = _group_phase_weapons(group, use_melee, in_melee)

    # Per-group stat overrides (e.g. Boss Nob A 3 / S 5 / WS 2+) fall back to the
    # unit-level value for homogeneous groups; bracketed units key off group wounds.
    grp_attacks = _group_effective_attacks(atk_unit, group, atk_state)
    grp_strength = int(cast(int, group.stat("strength", atk_unit.strength)))
    grp_ws = group.stat("ws", None)
    grp_bs = group.stat("bs", None)

    def _val(key: str) -> int:
        try:
            return int(st.session_state.get(key, 0) or 0)
        except (TypeError, ValueError):
            return 0

    def _ranged_profile(weapon: Weapon) -> WeaponProfile:
        return next((p for p in weapon.profiles if not p.is_melee), weapon.profiles[0])

    # Budget overview on top; counters below are capped so overbooking is impossible.
    group_budget = 0
    weapon_caps: dict[str, int] = {}
    if use_melee:
        group_budget = _group_melee_budget(grp_weapons, alive, grp_attacks + atk_bonus)
        total_assigned = sum(
            _val(f"decl_a_{gid}_{atk_uid}_{d_uid}_{w.name_en}")
            for _, d_uid in tgts
            for w in grp_weapons
        )
        # Filled after the counters render so it reflects the values the widgets
        # actually hold this run (defaults included). total_assigned above is a
        # pre-widget session_state read — correct for the overbooking cap, but
        # stale for display on the first render before defaults are written.
        header_ph = st.empty()
    else:
        # One model per UNIT may throw a grenade per phase (core rules: Grenade) —
        # the cap is shared across all model groups, so subtract grenades already
        # assigned in other groups' finished declarations.
        all_decl: dict = st.session_state.get("group_decl", {})  # type: ignore[type-arg]

        def _is_grenade(weapon_name: str) -> bool:
            wp = next((x for x in atk_unit.weapons if x.name_en == weapon_name), None)
            return wp is not None and _ranged_profile(wp).weapon_type.startswith("Grenade")

        grenade_used_other = sum(
            e.get("models_count", 0)
            for other_gid, other_entries in all_decl.items()
            if other_gid != gid
            for e in other_entries
            if _is_grenade(e["weapon_name"])
        )
        grenade_unit_cap = max(0, 1 - grenade_used_other)
        base_weapon_caps: dict[str, int] = {}
        for w in grp_weapons:
            ranged_profile = _ranged_profile(w)
            grenade = ranged_profile.weapon_type.startswith("Grenade")
            base_cap = grenade_unit_cap if grenade else alive
            base_weapon_caps[w.name_en] = base_cap
            # P20 (S119): Rapid Fire doubles attacks within half range. The app
            # has no range input, so the field's max is raised to let the player
            # represent the doubled total; the default (below) stays at base_cap.
            weapon_caps[w.name_en] = _rapid_fire_input_cap(ranged_profile.weapon_type, base_cap)
        weapon_assigned = {
            w.name_en: sum(_val(f"decl_m_{gid}_{atk_uid}_{d_uid}_{w.name_en}") for _, d_uid in tgts)
            for w in grp_weapons
        }
        summary = " · ".join(
            f"{name}: {weapon_assigned[name]}/{cap}" for name, cap in weapon_caps.items()
        )
        st.markdown(f"**{group.name_en}** — {alive} model(s)")
        st.caption(summary)

    entries: list[dict] = []  # type: ignore[type-arg]
    models_assigned = 0
    attacks_assigned = 0

    for i, (def_faction, def_uid) in enumerate(tgts):
        def_unit, _ = lookup(def_faction, def_uid)
        with st.container(border=True):
            st.markdown(f"**→ {def_unit.name_en}**")
            c_t, c_sv, c_inv = st.columns(3)
            c_t.metric("T", def_unit.toughness)
            c_sv.metric("Sv", f"{def_unit.save}+")
            c_inv.metric("++", f"{def_unit.invuln_save}+" if def_unit.invuln_save else "—")

            if use_melee:
                for weapon in grp_weapons:
                    profiles = [p for p in weapon.profiles if p.is_melee]
                    if not profiles:
                        profiles = weapon.profiles
                    if len(profiles) > 1:
                        p_names = [p.name or f"Profile {j + 1}" for j, p in enumerate(profiles)]
                        p_key = f"decl_p_{gid}_{atk_uid}_{def_uid}_{weapon.name_en}"
                        sel_p = st.radio(
                            f"Profile — {weapon.name_en}", p_names, key=p_key, horizontal=True
                        )
                        profile_idx = p_names.index(sel_p)
                    else:
                        profile_idx = 0
                    profile = profiles[profile_idx]
                    rule_max = (
                        _total_attacks_int(
                            profile.attacks,
                            alive,
                            grp_attacks + atk_bonus,
                            profile.effect,
                            profile.max_attacks,
                        )
                        or group_budget
                    )
                    atk_key = f"decl_a_{gid}_{atk_uid}_{def_uid}_{weapon.name_en}"
                    if atk_key not in st.session_state:
                        is_first = i == 0 and weapon is grp_weapons[0]
                        st.session_state[atk_key] = rule_max if is_first else 0
                    # Remaining budget caps this counter — overbooking impossible
                    budget_left = group_budget - (total_assigned - _val(atk_key))
                    weapon_max = max(0, min(rule_max, budget_left))
                    if _val(atk_key) > weapon_max:
                        st.session_state[atk_key] = weapon_max
                    atk_count = st.number_input(
                        f"{weapon.name_en} — Attacks",
                        min_value=0,
                        max_value=weapon_max,
                        step=1,
                        key=atk_key,
                    )
                    entries.append(
                        {
                            "def_faction": def_faction,
                            "def_uid": def_uid,
                            "weapon_name": weapon.name_en,
                            "profile_idx": profile_idx,
                            "models_count": alive,
                            "atk_override": int(atk_count),
                            "atk_attacks": grp_attacks,
                            "atk_strength": grp_strength,
                            "atk_ws": grp_ws,
                            "atk_bs": grp_bs,
                            "atk_uid": atk_uid,
                        }
                    )
                    attacks_assigned += int(atk_count)
            else:
                for weapon in grp_weapons:
                    profiles = [p for p in weapon.profiles if p.is_melee == use_melee]
                    if not profiles:
                        profiles = list(weapon.profiles)
                    if len(profiles) > 1:
                        p_names = [p.name or f"Profile {j + 1}" for j, p in enumerate(profiles)]
                        p_key = f"decl_p_{gid}_{atk_uid}_{def_uid}_{weapon.name_en}"
                        sel_p = st.radio(
                            f"Profile — {weapon.name_en}",
                            p_names,
                            key=p_key,
                            horizontal=True,
                        )
                        profile_idx = p_names.index(sel_p)
                    else:
                        profile_idx = 0
                    profile = profiles[profile_idx]
                    cap = weapon_caps.get(weapon.name_en, alive)
                    base_cap = base_weapon_caps.get(weapon.name_en, alive)
                    models_key = f"decl_m_{gid}_{atk_uid}_{def_uid}_{weapon.name_en}"
                    if models_key not in st.session_state:
                        # Grenades start at 0 (optional); everything else fires fully
                        # at the base (out-of-half-range) count — Rapid Fire's raised
                        # cap (above) widens the field's ceiling only, not the default.
                        st.session_state[models_key] = base_cap if (i == 0 and base_cap > 1) else 0
                    # Remaining models for this weapon cap the counter
                    others = weapon_assigned[weapon.name_en] - _val(models_key)
                    weapon_max = max(0, cap - others)
                    if _val(models_key) > weapon_max:
                        st.session_state[models_key] = weapon_max
                    models_val = st.number_input(
                        f"{weapon.name_en} — models",
                        min_value=0,
                        max_value=weapon_max,
                        step=1,
                        key=models_key,
                    )
                    eff_models = int(models_val)
                    displayed_count = _compute_attacks(
                        profile.attacks,
                        eff_models,
                        cast(int, atk_unit.attacks),
                        profile.effect,
                        profile.max_attacks,
                    )
                    rf_caption = _rapid_fire_caption(profile.weapon_type, profile.range_inches)
                    if rf_caption:
                        st.caption(rf_caption)
                    st.markdown(
                        f"**{weapon.name_en}** → "
                        f'<span style="font-size:1.1rem;font-weight:700;color:#fbbf24;">'
                        f"{displayed_count}</span> Attacks",
                        unsafe_allow_html=True,
                    )
                    entries.append(
                        {
                            "def_faction": def_faction,
                            "def_uid": def_uid,
                            "weapon_name": weapon.name_en,
                            "profile_idx": profile_idx,
                            "models_count": eff_models,
                            "atk_attacks": grp_attacks,
                            "atk_strength": grp_strength,
                            "atk_ws": grp_ws,
                            "atk_bs": grp_bs,
                            "atk_uid": atk_uid,
                        }
                    )
                    models_assigned += eff_models

    if use_melee:
        header_ph.markdown(
            f"**{group.name_en}** — {alive} model(s) · "
            f'<span style="font-size:1.1rem;font-weight:700;color:#fbbf24;">'
            f"{attacks_assigned} / {group_budget}</span> attacks assigned",
            unsafe_allow_html=True,
        )

    valid = attacks_assigned > 0 if use_melee else models_assigned > 0

    if st.button(
        f"{SYM_CHECK} Group done",
        type="primary",
        disabled=not valid,
        key=f"grp_done_{atk_uid}_{gid}",
    ):
        group_decl = dict(st.session_state.get("group_decl", {}))
        group_decl[gid] = entries
        st.session_state.group_decl = group_decl
        st.session_state.selected_model_group = None
        st.rerun()


# ---------------------------------------------------------------------------
# 6d-v2 Resolution phase
# ---------------------------------------------------------------------------


def render_attack_resolution(phase_key: str) -> None:
    """Phase 2 — One tab per (weapon × target). Reads state from attack_declaration."""
    decl = st.session_state.get("attack_declaration", {})
    if not decl.get("active"):
        return

    atk_faction = decl["atk_faction"]
    atk_uid = decl["atk_uid"]
    use_melee = decl["use_melee"]
    entries = decl.get("entries", [])

    atk_unit, atk_state = lookup(atk_faction, atk_uid)
    badges = state_badges_html(atk_state)
    for proto_lbl in active_round_choice_buff_labels(atk_faction):
        badges += _badge(proto_lbl, variant="buff")

    st.markdown(f"**{atk_unit.name_en}** — Resolution")
    if badges:
        st.markdown(badges, unsafe_allow_html=True)

    if st.button(f"{SYM_RESET} Reset Declaration", key="reset_decl"):
        st.session_state.attack_declaration = _empty_attack_declaration()
        reset_group_declaration_state()
        st.rerun()

    if not entries:
        return

    tab_labels = []
    for entry in entries:
        def_unit, _ = lookup(entry["def_faction"], entry["def_uid"])
        tab_labels.append(f"{entry['weapon_name']} → {def_unit.name_en}")

    seq = decl.get("seq", 0)

    # Cover checkboxes are rendered inside each tab's HIT/SAVE block (Option B),
    # so they appear in the block they actually modify.
    tabs = st.tabs(tab_labels)
    for i, (tab, entry) in enumerate(zip(tabs, entries)):
        with tab:
            tab_key = f"{seq}_{atk_uid}_{entry['def_uid']}_{i}"
            res_key = f"res_{tab_key}"
            tab_state = st.session_state.get(res_key, {})

            if tab_state.get("applied"):
                m_lost = tab_state.get("models_lost", 0)
                mw = tab_state.get("mortal_wounds", 0)
                total = tab_state.get("total_damage", 0)
                st.success(f"{SYM_CHECK} {m_lost} models · {mw} MW · {total} damage")
                if st.button(f"{SYM_RESET} Reset", key=f"res_reset_{tab_key}"):
                    st.session_state.pop(res_key, None)
                    st.rerun()
            else:
                _render_resolution_tab(
                    entry,
                    atk_faction,
                    atk_unit,
                    atk_state,
                    use_melee,
                    phase_key,
                    tab_key,
                )

    all_applied = all(
        st.session_state.get(f"res_{seq}_{atk_uid}_{e['def_uid']}_{j}", {}).get("applied", False)
        for j, e in enumerate(entries)
    )
    if all_applied and entries:
        st.markdown("---")
        _render_unit_rp(seq, atk_uid, entries)
        if st.button(f"{SYM_CHECK} All done — Continue", type="primary", key="all_done"):
            st.session_state.attack_declaration = _empty_attack_declaration()
            reset_group_declaration_state()
            st.rerun()


def _render_unit_rp(seq: int, atk_uid: str, entries: list[dict]) -> None:  # type: ignore[type-arg]
    """Reanimation Protocols once per defender unit, summing model losses across
    all weapon tabs of the attacking unit (the unit has now fully resolved).

    Generic: gated in _render_rp_block by the unit's YAML-declared revive
    ability (effect type ``reanimate``) — no faction-specific logic.
    """
    seen: list[tuple[str, str]] = []
    for entry in entries:
        key = (entry["def_faction"], entry["def_uid"])
        if key in seen:
            continue
        seen.append(key)
        def_unit, _ = lookup(*key)
        total_lost = sum(
            st.session_state.get(f"res_{seq}_{atk_uid}_{e['def_uid']}_{j}", {}).get(
                "models_lost", 0
            )
            for j, e in enumerate(entries)
            if (e["def_faction"], e["def_uid"]) == key
        )
        _render_rp_block(
            def_unit, key[0], key[1], total_lost, f"unit_{seq}_{atk_uid}_{entry['def_uid']}"
        )
