"""MovementPhaseHandler — Movement Phase for WH40k 9E.

Ziel 3a: Migrates existing movement UI from gameActionsArea.
Ziel 4:  Full turn_flags tracking, advance-roll, reserve deployment.
"""

from __future__ import annotations

from collections.abc import Callable
from typing import ClassVar

import streamlit as st

from constants.symbols import SYM_RESET
from gameMechanic.game_log import log_action
from gameMechanic.game_state import (
    faction_dir_for,
    unit_keys_for,
    units_key_for,
    units_list_for,
)
from gameMechanic.unit_mutations import (
    reset_movement_to_stationary,
    resolve_desperate_breakout,
    set_deployment,
    set_movement_status,
)
from gameObjects.loader import load_relic_catalog, load_stratagems
from gameObjects.stratagem import (
    Stratagem,
    reactive_stratagems_for,
    stratagem_undo_visible,
    stratagem_usable_by_player,
    stratagem_visibility,
)
from gameObjects.unit import TriggeredEffect, Unit
from uiLayout._common import (
    lookup,
    render_go_card,
    render_player_column,
    render_reactive_stratagem_box,
    render_unit_selectbox,
    spend_stratagem,
    undo_stratagem,
)
from uiLayout.go_card import GoCardState

# Fallbacks when a teleport relic's YAML entry carries no UI texts. Faction
# flavour (e.g. which keyword the second unit must carry) lives in the relic's
# prompt_text/selector_label fields in relics.yaml (INV-4b: data-driven).
_TELEPORT_PROMPT_FALLBACK = (
    "Once per battle: remove this unit (and optionally one eligible unit "
    'within 3") from the battlefield and set up both more than 9" from any '
    "enemy models. Both units count as having moved this turn."
)
_TELEPORT_SELECTOR_FALLBACK = 'Optional: select a CORE unit within 3"'


class MovementPhaseHandler:
    """PhaseHandler for the Movement Phase."""

    phase_name: ClassVar[str] = "movement"

    def render_active(self, state: dict) -> None:  # type: ignore[type-arg]
        first: str = state["first_player"]
        second: str = state["second_player"]

        col1, col2 = st.columns(2)
        with col1:
            render_player_column(first, state, active_content=_active_movement)
            if first == state["active"]:
                _render_reinforcements_step(first)
        with col2:
            render_player_column(second, state, active_content=_active_movement)
            if second == state["active"]:
                _render_reinforcements_step(second)

        _render_pending_cut_them_down(first, second)


# ---------------------------------------------------------------------------
# Phase-specific content helpers
# ---------------------------------------------------------------------------


def _active_movement(
    faction: str, uid: str, unit, unit_state: dict, state: dict  # type: ignore[type-arg]
) -> None:
    """Render movement type buttons for the active player's selected unit."""
    if unit_state.get("in_reserve"):
        st.caption("In reserve — manage deployment in 'Step 2: Reinforcements' below.")
        return

    in_melee = unit_state.get("in_melee", False)
    flags = unit_state.get("turn_flags", {})

    if flags.get("desperate_breakout_pending"):
        _render_desperate_breakout(uid, unit, faction, unit_state, state)
        return

    # Movement was locked by an ability (e.g. teleport) — block normal movement buttons
    if flags.get("movement_locked"):
        st.divider()
        te = unit.get_triggered_effect("phase_start", "movement", "teleport")
        if te:
            _render_teleport_effect(uid, unit, faction, state, unit_state, te)
        else:
            st.info("Movement locked by an ability — cannot change movement status this turn.")
        return

    _render_movement_buttons(faction, uid, unit, unit_state, in_melee)
    _render_advance_reroll_card(faction, uid, unit, unit_state, in_melee)

    te = unit.get_triggered_effect("phase_start", "movement", "teleport")
    if te:
        _render_teleport_effect(uid, unit, faction, state, unit_state, te)


# Movement choices offered before any decision is made — contextual on melee
# (core_rules.txt Z. 709-724/739): a unit within Engagement Range may only
# Fall Back or Remain Stationary. "Remain Stationary" is never one of these
# initial buttons (S133 K2 decision item 3) — a unit simply left untouched
# already counts as Stationary (Z. 767-770), so an in-melee unit with no
# decision yet sees only Retreat, everyone else sees Move/Advance.
_FIELD_MOVE_OPTIONS: list[tuple[str, str, str]] = [
    ("Move", "moved", 'Move up to M"'),
    ("Advance", "advanced", 'M"+D6", no shoot/charge'),
]
_RETREAT_OPTION: tuple[str, str, str] = ("Retreat", "retreated", "Exit melee, no shoot/charge")

# Movement choices a Reset button ("Stay Stationary") can undo back to
# Stationary (S133 K2 decision item 3). "stationary" itself is excluded —
# reaching it (only ever via Reset) shows the same initial button set again,
# see _render_movement_buttons.
_COMMITTED_CHOICES: frozenset[str] = frozenset({"moved", "advanced", "retreated"})
_COMMITTED_LABEL: dict[str, str] = {
    "moved": "Moved",
    "advanced": "Advanced",
    "retreated": "Retreated",
}


def _render_movement_buttons(
    faction: str, uid: str, unit: Unit, unit_state: dict, in_melee: bool  # type: ignore[type-arg]
) -> None:
    """Render the Move/Advance/Retreat buttons, or the Reset button once one fired.

    "none" (never touched) and "stationary" (only reachable via Reset) render
    identically — the contextual initial button set — so a unit Reset back to
    Stationary shows exactly the options a freshly untouched unit would (S133
    K2 Entscheid: the pre-Retreat in-melee dependency reappears unchanged).
    """
    current = unit_state.get("movement_choice") or "none"

    if current in _COMMITTED_CHOICES:
        _render_reset_button(faction, uid, unit, current)
        return

    st.markdown("Set movement status:")
    options = [_RETREAT_OPTION] if in_melee else _FIELD_MOVE_OPTIONS
    for label, value, tip in options:
        if st.button(
            label,
            key=f"mv_{faction}_{uid}_{value}",
            type="secondary",
            use_container_width=True,
            help=tip,
        ):
            set_movement_status(uid, faction, value)
            if value == "retreated":
                # Opens the Cut Them Down reactive window (core_rules.txt Z. 773-778) —
                # "before any models in that unit are moved"; this app has no separate
                # movement-execution step, so the window opens immediately on
                # declaration and stays open until the enemy uses it (GO card Use →
                # on_resolved clears the marker, no Pass control per design_system.md
                # §6.1) or the phase ends (_reset_phase_state clears the marker too).
                st.session_state.pending_fall_back = {"faction": faction, "uid": uid}
            log_action(st.session_state.round, "movement", unit.name_en, f"movement: {value}")
            st.rerun()

    if in_melee:
        st.caption("Unit is in melee — only Retreat is available.")


def _render_reset_button(faction: str, uid: str, unit: Unit, current: str) -> None:
    """The one Reset button replacing whichever Move/Advance/Retreat button fired.

    Reuses ``unit_mutations.reset_movement_to_stationary`` — itself built on
    the existing ``set_movement_status`` mutation the pre-refactor "Stay
    Stationary" button already called (S133 K2 decision item 3: no new
    movement mutation, just a new entry point into the existing one). Always
    lands on "stationary" — never re-opens Move/Advance for a Retreated unit
    (core_rules.txt: Fall Back is final for the phase); a still-open Cut Them
    Down window for this exact Retreat is cleared too, since Reset undoes the
    Fall Back it was reacting to.
    """
    st.caption(f"{_COMMITTED_LABEL[current]} this turn.")
    if st.button(
        f"{SYM_RESET} Stay Stationary",
        key=f"mv_reset_{faction}_{uid}",
        type="secondary",
        use_container_width=True,
        help="Undo — unit remains Stationary",
    ):
        reset_movement_to_stationary(uid, faction)
        marker = st.session_state.get("pending_fall_back")
        if marker and marker.get("faction") == faction and marker.get("uid") == uid:
            st.session_state.pending_fall_back = None
        log_action(
            st.session_state.round, "movement", unit.name_en, "movement: reset to stationary"
        )
        st.rerun()


def _advance_reroll_state(
    strat: Stratagem,
    in_melee: bool,
    movement_choice: str,
    cp: int,
    used_ids: set[str],
    used_battle_ids: set[str],
) -> tuple[GoCardState, str | None]:
    """Map the Advance re-roll's own preconditions to a GO-card state + reason.

    Mirrors gameProtocoll.py's ``_go_state_and_reason`` shape (clickable →
    ready, greyed+undo-window-open → used, else locked) but with the three
    movement-specific locked reasons the stakeholder named (S133 K2 item 1):
    in melee, no Advance roll open, CP short/already used — checked in that
    priority order.
    """
    if in_melee:
        return "locked", "unit is in melee"
    if movement_choice != "advanced":
        return "locked", "no Advance roll open"
    vis = stratagem_visibility(
        strat, cp, "movement", used_ids, True, used_battle_ids, reactive_trigger_active=True
    )
    if vis == "clickable":
        return "ready", None
    if stratagem_undo_visible(strat.id, used_ids, used_battle_ids):
        return "used", None
    return "locked", "CP insufficient"


def _render_advance_reroll_card(
    faction: str, uid: str, unit: Unit, unit_state: dict, in_melee: bool  # type: ignore[type-arg]
) -> None:
    """Always-visible GO card for the Advance-roll Command Re-Roll (S133 K2 item 1).

    Rendered before AND after a movement decision — unlike
    render_reactive_stratagem_box's GO card, there is no dice value
    to react to (the app never captures Advance-roll numbers): the card's job
    is CP bookkeeping plus a locked reason for the three inapplicable cases
    named above. Replaces the previous bare ``render_inline_command_reroll``
    button, which only ever appeared once "advanced" was already chosen.
    """
    try:
        stratagems = load_stratagems(faction_dir_for(faction))
    except Exception:
        return
    candidates = reactive_stratagems_for(stratagems, "movement", "after_roll")
    if not candidates:
        return

    is_active = faction == st.session_state.get("active")
    cp = st.session_state.get("cp", {}).get(faction, 0)
    used_ids = st.session_state.get("used_stratagem_ids", {}).get(faction, set())
    used_battle_ids = st.session_state.get("used_stratagem_battle_ids", {}).get(faction, set())
    current = unit_state.get("movement_choice") or "none"

    for strat in candidates:
        if not stratagem_usable_by_player(strat.player, is_active):
            continue
        card_state, reason = _advance_reroll_state(
            strat, in_melee, current, cp, used_ids, used_battle_ids
        )
        render_go_card(
            key=f"movement_reroll_{faction}_{uid}_{strat.id}",
            name=strat.name_en,
            cp_cost=strat.cp_cost,
            state=card_state,
            compact=True,
            rule_text=strat.rule_text,
            locked_reason=reason,
            target_name=unit.name_en,
            on_use=_spend_callback(strat, faction),
            on_undo=_undo_callback(strat, faction),
        )


def _spend_callback(strat: Stratagem, faction: str) -> Callable[[], None]:
    """Factory for the re-roll card's on_use callback.

    Same pattern (and reason) as gameProtocoll.py's `_use_callback`: a bare
    lambda in the loop body would capture the loop variable by reference, and
    the `lambda s=strat:` default-arg workaround defeats mypy's lambda type
    inference — the factory closure gets both right.
    """
    return lambda: spend_stratagem(strat, faction)


def _undo_callback(strat: Stratagem, faction: str) -> Callable[[], None]:
    """Factory for the re-roll card's on_undo callback (see `_spend_callback`)."""
    return lambda: undo_stratagem(strat, faction)


def _desperate_breakout_stratagem(faction: str) -> Stratagem | None:
    """Find the shared stratagem driving Desperate Breakout resolution.

    Matched by effect shape (`type="move"`, `handler="fall_back_through_models"`),
    not by id/name — mirrors `uiLayout._common._apply_stratagem_effect`'s
    dispatch (INV-4b: no faction- or GO-name string checks in src/).
    """
    stratagems = load_stratagems(faction_dir_for(faction))
    for s in stratagems:
        if (
            s.effect is not None
            and s.effect.type == "move"
            and s.effect.handler == "fall_back_through_models"
        ):
            return s
    return None


def _render_desperate_breakout(
    uid: str,
    unit: Unit,
    faction: str,
    unit_state: dict,  # type: ignore[type-arg]
    state: dict,  # type: ignore[type-arg]
) -> None:
    """Resolve a pending Desperate Breakout: casualty roll, then Fall Back.

    Rendered as the same GO card (design_system.md §6.1) the central Stratagems
    tab shows for this stratagem — not a free-floating block (S133-D Befund 2):
    the casualty-roll input and Confirm button are this card's
    ``expanded_content``, so they sit inside the card's own bordered container
    rather than lower down the phase flow, disconnected from any card. State is
    always "used" here — this block only renders once
    ``desperate_breakout_pending`` is set, i.e. after CP was already spent via
    the central list's Use button. ``on_undo`` fully reverses that spend (CP +
    usage bookkeeping via the canonical ``undo_stratagem``, plus clearing the
    pending flag) while the resolution window is still open — no roll has been
    applied yet at that point, so nothing else needs to unwind.

    Class C (Hybrid, R-MOVE-14): the App applies the destroyed-model count the
    player reports and the resulting Fall Back (leaves melee; locks
    shooting/charging/manifesting powers this turn — same as a normal Fall
    Back, R-MOVE-08). Whether the unit can actually find a valid Fall Back path
    and ending square outside every enemy's Engagement Range stays a table
    judgement (core_rules.txt: Fall Back "cannot end its move within Engagement
    Range of any enemy models — if it cannot do this then it cannot Fall
    Back"); rules_appendix.txt notes that if a rule prevents Falling Back, no
    further models are destroyed beyond the casualty roll already resolved here.
    """
    strat = _desperate_breakout_stratagem(faction)
    name = strat.name_en if strat is not None else "Desperate Breakout"
    cp_cost = strat.cp_cost if strat is not None else 0
    rule_text = strat.rule_text if strat is not None else ""

    def _expanded_content() -> None:
        st.caption(
            "Roll 1 D6 per model in this unit; for each result of 1, one model "
            "of your choice is destroyed. Then attempt to Fall Back."
        )
        casualties = st.number_input(
            "Models destroyed (rolled a 1)",
            min_value=0,
            max_value=unit_state["models"],
            step=1,
            key=f"desperate_breakout_casualties_{uid}",
        )
        if st.button(
            "Confirm Desperate Breakout",
            key=f"desperate_breakout_confirm_{uid}",
            type="primary",
            use_container_width=True,
        ):
            resolve_desperate_breakout(uid, faction, int(casualties), unit)
            log_action(
                state["round"],
                "movement",
                unit.name_en,
                f"Desperate Breakout — {int(casualties)} model(s) destroyed, Fall Back.",
            )
            if not unit_state.get("destroyed"):
                st.session_state.pending_fall_back = {"faction": faction, "uid": uid}
            st.rerun()

    def _on_undo() -> None:
        if strat is not None:
            undo_stratagem(strat, faction)
        unit_state["turn_flags"]["desperate_breakout_pending"] = False

    render_go_card(
        key=f"desperate_breakout_{faction}_{uid}",
        name=name,
        cp_cost=cp_cost,
        state="used",
        rule_text=rule_text,
        target_name=unit.name_en,
        expanded_content=_expanded_content,
        on_undo=_on_undo,
    )


def _render_teleport_effect(
    uid: str,
    unit,  # type: ignore[type-arg]
    faction: str,
    state: dict,  # type: ignore[type-arg]
    unit_state: dict,  # type: ignore[type-arg]
    te: TriggeredEffect,
) -> None:
    """Render a once-per-battle teleport relic UI.

    Step 1: "Prepare" button (disabled if already moved or already used).
    Step 2: Optional CORE unit selector + Confirm/Cancel.
    On confirm: mark bearer + optional CORE unit as moved; lock movement; mark relic used.
    """
    relic_id = unit.relic_id
    display_name = unit.relic_name or relic_id
    relic_entry = load_relic_catalog(faction_dir_for(faction)).get(relic_id) or {}

    st.divider()
    st.markdown(f"**{display_name}**")

    relic_used = st.session_state.get("relic_triggered_used", {})
    if relic_used.get(relic_id):
        if unit_state["turn_flags"].get("movement_locked"):
            st.info(
                f"{display_name} activated this turn — unit and selected CORE unit count as moved."
            )
            if st.button(
                f"Undo {display_name}", key=f"teleport_undo_{uid}", use_container_width=True
            ):
                _undo_teleport(relic_id, faction, state)
        else:
            st.caption("Already used this battle.")
        return

    # Teleport replaces normal move — block if already moved/advanced/retreated
    movement_choice = st.session_state[units_key_for(faction)].get(uid, {}).get("movement_choice")
    if movement_choice in ("moved", "advanced", "retreated"):
        st.caption(f"{display_name} not available — unit has already moved this turn.")
        return

    awaiting = st.session_state.get("veil_awaiting_confirm", False)

    if not awaiting:
        st.caption(relic_entry.get("prompt_text") or _TELEPORT_PROMPT_FALLBACK)
        if st.button(
            f"Prepare {display_name}",
            key=f"teleport_prepare_{uid}",
            type="primary",
            use_container_width=True,
        ):
            st.session_state.veil_awaiting_confirm = True
            st.session_state.veil_core_target_uid = None
            st.rerun()
        return

    # ---------------------------------------------------------------------------
    # Step 2 — CORE unit selector
    # ---------------------------------------------------------------------------
    st.info(
        'Verify bearer is within 3" of the target unit on the table. '
        'Both will be set up more than 9" from any enemy models.'
    )

    units_state = st.session_state[units_key_for(faction)]
    all_units = units_list_for(faction)
    all_keys = unit_keys_for(faction)

    # Build (state_key, unit) pairs for CORE candidates — exclude bearer, destroyed, reserve
    core_candidates: list[tuple[str, object]] = []  # type: ignore[type-arg]
    for state_key, cu in zip(all_keys, all_units):
        if cu.id == unit.id:
            continue
        if "CORE" not in cu.keywords:
            continue
        cu_state = units_state.get(state_key, {})
        if cu_state.get("destroyed") or cu_state.get("in_reserve"):
            continue
        core_candidates.append((state_key, cu))

    core_candidates_dicts = [{"uid": sk, "name": cu.name_en} for sk, cu in core_candidates]
    render_unit_selectbox(
        relic_entry.get("selector_label") or _TELEPORT_SELECTOR_FALLBACK,
        core_candidates_dicts,
        "veil_core_target_uid",
        none_label="— Bearer only (no second unit) —",
    )

    col1, col2 = st.columns(2)
    with col1:
        if st.button(
            "Confirm Teleport", key="veil_confirm", type="primary", use_container_width=True
        ):
            # Mark relic as used (once per battle)
            used = dict(st.session_state.get("relic_triggered_used", {}))
            used[relic_id] = True
            st.session_state.relic_triggered_used = used

            # Mark bearer as moved (locked by teleport ability)
            set_movement_status(uid, faction, "moved")
            _lock_teleport_movement(uid, faction)

            # Mark optional CORE unit as moved — core_uid IS already the state key
            core_uid = st.session_state.get("veil_core_target_uid")
            core_name = ""
            if core_uid:
                set_movement_status(core_uid, faction, "moved")
                _lock_teleport_movement(core_uid, faction)
                core_unit_pair = next(
                    ((sk, cu) for sk, cu in core_candidates if sk == core_uid), None
                )
                core_name = f" + {core_unit_pair[1].name_en}" if core_unit_pair else ""

            log_action(
                state["round"],
                "movement",
                unit.name_en,
                f"{display_name}: teleport{core_name}",
            )
            st.session_state.veil_awaiting_confirm = False
            st.session_state.veil_core_target_uid = None
            st.rerun()
    with col2:
        if st.button("Cancel", key="veil_cancel", use_container_width=True):
            st.session_state.veil_awaiting_confirm = False
            st.session_state.veil_core_target_uid = None
            st.rerun()


def _lock_teleport_movement(state_key: str, faction: str) -> None:
    """Lock a teleported unit's movement and remove it from melee (F7).

    A teleport sets the unit up more than 9" from enemies, so it is no longer in
    Engagement Range. The prior in_melee value is stashed so _undo_teleport can
    restore it while the turn is still running.
    """
    u_state = st.session_state[units_key_for(faction)][state_key]
    u_state["turn_flags"]["movement_locked"] = True
    u_state["turn_flags"]["veil_prev_in_melee"] = u_state.get("in_melee", False)
    u_state["in_melee"] = False


def _undo_teleport(relic_id: str, faction: str, state: dict) -> None:  # type: ignore[type-arg]
    """Undo a confirmed teleport ability (only available within the same turn)."""
    used = dict(st.session_state.get("relic_triggered_used", {}))
    used.pop(relic_id, None)
    st.session_state.relic_triggered_used = used

    # Reset every unit in the faction whose movement was locked by the teleport
    for u_state in st.session_state[units_key_for(faction)].values():
        if u_state.get("turn_flags", {}).get("movement_locked"):
            u_state["turn_flags"]["movement_locked"] = False
            u_state["movement_choice"] = "stationary"
            u_state["movement_chosen"] = False
            # Restore pre-teleport melee state (F7)
            u_state["in_melee"] = u_state["turn_flags"].pop("veil_prev_in_melee", False)

    log_action(state["round"], "movement", "teleport", "undone")
    st.rerun()


def _clear_pending_fall_back() -> None:
    st.session_state.pending_fall_back = None


def _render_pending_cut_them_down(first: str, second: str) -> None:
    """Render the Cut Them Down box for the enemy of a unit that just Fell Back.

    `player: inactive` in the YAML means the box is for the OTHER faction —
    Cut Them Down punishes the enemy's Fall Back, not your own.
    """
    marker = st.session_state.get("pending_fall_back")
    if not marker:
        return
    retreat_faction = marker["faction"]
    enemy_faction = second if retreat_faction == first else first
    try:
        unit, _ = lookup(retreat_faction, marker["uid"])
    except KeyError:
        st.session_state.pending_fall_back = None
        return

    st.divider()
    render_reactive_stratagem_box(
        enemy_faction,
        phase="movement",
        event="on_declaration",
        decline_key=marker["uid"],
        context_caption=f"{unit.name_en} ({retreat_faction}) is Falling Back.",
        on_resolved=_clear_pending_fall_back,
    )


def _all_field_units_resolved(faction: str) -> bool:
    """True once every on-battlefield, non-destroyed unit has an explicit movement choice.

    Gates the Reinforcements step (S133 K2 item 2, core_rules.txt Z. 734-736/
    800-804): "Once you have moved all your units ... progress to the
    Reinforcements step" — Reinforcements is its own step AFTER the Move
    Units step, not something reachable in parallel with it.
    """
    units_state = st.session_state[units_key_for(faction)]
    return all(
        us.get("movement_chosen")
        for us in units_state.values()
        if not us.get("in_reserve") and not us.get("destroyed")
    )


def _render_reinforcements_step(faction: str) -> None:
    """Always-visible reinforcements section for the active player."""
    key = units_key_for(faction)
    units_state = st.session_state[key]
    reserve_units = [(uid, us) for uid, us in units_state.items() if us.get("in_reserve")]

    st.markdown("**Step 2: Reinforcements**")

    if not reserve_units:
        st.caption("No reinforcements this round.")
        return

    if st.session_state.round == 1:
        st.caption("Units in reserve — cannot deploy until Round 2.")
        return

    if not _all_field_units_resolved(faction):
        st.caption("Move all units on the battlefield before deploying reinforcements.")
        return

    for uid, _ in reserve_units:
        unit, _ = lookup(faction, uid)
        if st.button(
            f"Deploy {unit.name_en} from Reserve",
            key=f"deploy_reserve_{faction}_{uid}",
            type="primary",
            use_container_width=True,
        ):
            set_deployment(uid, faction, "normal")
            set_movement_status(uid, faction, "moved")
            log_action(st.session_state.round, "movement", unit.name_en, "deployed from reserve")
            st.rerun()
