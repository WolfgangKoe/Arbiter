"""FightPhaseHandler — Fight Phase for WH40k 9E.

9E rules (core_rules.txt Z. 1941-1973):
- Inactive player selects first; both players alternate.
- Charged units fight before non-charged units (Fights First rule).
- If one player has no eligible units, the other continues alone.
"""

from __future__ import annotations

import streamlit as st

from gameMechanic.game_log import log_action
from gameMechanic.game_state import unit_keys_for, units_key_for, units_list_for
from gameMechanic.unit_mutations import apply_mortal_wounds, heal_unit
from uiLayout._common import (
    group_flow_attacker,
    lookup,
    render_attack_resolution,
    render_group_assignment,
    render_group_cards,
    render_unit_selectbox,
    state_badges_html,
    wound_adjustment_buttons,
)


def _is_target_engaged(atk_state: dict, def_faction: str, def_uid: str) -> bool:  # type: ignore[type-arg]
    """Return True if def_faction/def_uid is in the attacker's melee_with list."""
    return [def_faction, def_uid] in atk_state.get("melee_with", [])


def can_fight(unit_state: dict) -> bool:  # type: ignore[type-arg]
    """Return True if the unit is generally eligible to fight this turn.

    9E: a unit is eligible if it is in melee or if it charged this turn.
    Units that have already fought may not fight again.
    """
    flags = unit_state.get("turn_flags", {})
    if flags.get("fought"):
        return False
    return bool(unit_state.get("in_melee") or flags.get("charged"))


def _any_charged_remain(first: str, second: str) -> bool:
    """Return True if any charged (but not yet fought) unit exists on either side."""
    for player in (first, second):
        for s in st.session_state[units_key_for(player)].values():
            flags = s.get("turn_flags", {})
            if flags.get("charged") and not flags.get("fought"):
                return True
    return False


def can_fight_now(unit_state: dict, first: str, second: str) -> bool:  # type: ignore[type-arg]
    """Return True if this unit may fight right now (considering CHARGED priority).

    Non-charged units must wait until all charged units from both sides have fought.
    """
    if not can_fight(unit_state):
        return False
    flags = unit_state.get("turn_flags", {})
    if _any_charged_remain(first, second) and not flags.get("charged"):
        return False
    return True


def _has_eligible_units(player: str, first: str, second: str) -> bool:
    """Return True if the player has at least one unit eligible to fight right now."""
    for s in st.session_state[units_key_for(player)].values():
        if can_fight_now(s, first, second):
            return True
    return False


def _advance_fight_turn_if_needed(first: str, second: str) -> None:
    """Switch fight_current_player after a unit fights or when a player has no eligible units.

    Reruns on change: the army columns render before this runs (app.py order),
    so a silent switch would leave them showing stale select/target buttons.

    Never advances while a resolution is in progress — the fought flag is set on
    the first Apply Damage, but the turn passes only after "All done — Continue"
    (rule: alternate AFTER a unit finished fighting; charged units fight first).
    """
    if st.session_state.get("attack_declaration", {}).get("active"):
        return
    current = st.session_state.get("fight_current_player")
    if current is None:
        return
    entered_with = current

    # Detect if the current player's selected unit just fought
    sel = st.session_state.get("selected_unit")
    if sel and sel[0] == current:
        _, unit_state = lookup(current, sel[1])
        if unit_state.get("turn_flags", {}).get("fought"):
            other = second if current == first else first
            st.session_state.fight_current_player = other
            st.session_state.selected_unit = None
            st.session_state.selected_targets = []
            current = other

    # Auto-skip if current player has no eligible units but the other does
    other = second if current == first else first
    if not _has_eligible_units(current, first, second) and _has_eligible_units(
        other, first, second
    ):
        st.session_state.fight_current_player = other

    if st.session_state.fight_current_player != entered_with:
        st.rerun()


def _dice_max(dice_str: str) -> int:
    """Parse 'D3' or 'D6' to its maximum value."""
    try:
        return int(str(dice_str).lstrip("Dd"))
    except (ValueError, AttributeError):
        return 3


def _render_mortal_after_melee(state: dict) -> None:  # type: ignore[type-arg]
    """Render the post-fight mortal wound trigger UI (data-driven via triggered_effects).

    Step 'initial': target selection + Failed / Continue buttons.
    Step 'assign':  +/- wound counter + Back / Apply buttons.
    """
    pending = st.session_state.get("pending_triggered_relic") or {}
    uid = pending.get("uid", "")
    faction = pending.get("faction", "")
    step = pending.get("step", "initial")
    if not uid or not faction:
        return

    unit, _ = lookup(faction, uid)
    te = unit.get_triggered_effect("after_fight", "fight", "mortal_after_melee")
    if not te:
        st.session_state.pending_triggered_relic = None
        return

    display_name = unit.relic_name or unit.relic_id
    threshold = te.threshold or 2
    mortal_dice_str = te.mortal_dice or "D3"
    mortal_max = _dice_max(mortal_dice_str)
    fail_label = f"1–{threshold - 1} (Failed)" if threshold > 2 else "1 (Failed)"

    first = state["first_player"]
    enemy_faction = state["second_player"] if faction == first else first

    st.info(f"**{display_name}** — {unit.name_en} has finished attacking.")

    # ------------------------------------------------------------------
    # Step 1 — target selection + D6 result
    # ------------------------------------------------------------------
    if step == "initial":
        st.caption(
            f"Roll {te.dice or 'D6'}: on a {threshold}+, select one enemy unit within 1\" "
            f"and roll {mortal_dice_str} mortal wounds."
        )

        enemy_units_state = st.session_state[units_key_for(enemy_faction)]
        atk_state = st.session_state[units_key_for(faction)].get(uid, {})
        all_keys = unit_keys_for(enemy_faction)
        all_units = units_list_for(enemy_faction)
        candidates = [
            (sk, eu)
            for sk, eu in zip(all_keys, all_units)
            if not enemy_units_state.get(sk, {}).get("destroyed")
            and not enemy_units_state.get(sk, {}).get("in_reserve")
            and _is_target_engaged(atk_state, enemy_faction, sk)
        ]
        candidate_dicts = [{"uid": sk, "name": eu.name_en} for sk, eu in candidates]
        selected_target = render_unit_selectbox(
            'Target enemy unit (verify within 1" on table):',
            candidate_dicts,
            "mortal_target_uid",
            none_label="— Select target unit —",
        )

        col1, col2 = st.columns(2)
        with col1:
            if st.button(fail_label, key="mortal_fail", use_container_width=True):
                log_action(
                    state["round"], "fight", unit.name_en, f"{display_name}: failed — no effect"
                )
                st.session_state.pending_triggered_relic = None
                st.rerun()
        with col2:
            if st.button(
                f"2+ — Assign {mortal_dice_str} →",
                key="mortal_continue",
                type="primary",
                disabled=selected_target is None,
                use_container_width=True,
            ):
                updated = dict(pending)
                updated["step"] = "assign"
                updated["target_uid"] = selected_target
                updated["target_faction"] = enemy_faction
                st.session_state.pending_triggered_relic = updated
                st.rerun()

    # ------------------------------------------------------------------
    # Step 2 — +/- mortal wound counter
    # ------------------------------------------------------------------
    elif step == "assign":
        target_uid = pending.get("target_uid", "")
        target_faction = pending.get("target_faction", enemy_faction)
        target_unit, _ = lookup(target_faction, target_uid)
        mortals = pending.get("mortals", 0)

        st.caption(
            f"Roll {mortal_dice_str} on the table — assign mortal wounds to **{target_unit.name_en}**."
        )

        col_minus, col_count, col_plus = st.columns([1, 2, 1])
        with col_minus:
            if st.button("−", key="mortal_minus", disabled=mortals <= 0, use_container_width=True):
                updated = dict(pending)
                updated["mortals"] = mortals - 1
                st.session_state.pending_triggered_relic = updated
                st.rerun()
        with col_count:
            st.markdown(
                f"<div style='text-align:center;font-size:1.5rem;padding:0.3rem'><b>{mortals}</b></div>",
                unsafe_allow_html=True,
            )
        with col_plus:
            if st.button(
                "+", key="mortal_plus", disabled=mortals >= mortal_max, use_container_width=True
            ):
                updated = dict(pending)
                updated["mortals"] = mortals + 1
                st.session_state.pending_triggered_relic = updated
                st.rerun()

        col1, col2 = st.columns(2)
        with col1:
            if st.button("← Back", key="mortal_back", use_container_width=True):
                updated = dict(pending)
                updated["step"] = "initial"
                updated["mortals"] = 0
                st.session_state.pending_triggered_relic = updated
                st.rerun()
        with col2:
            plural = "s" if mortals != 1 else ""
            if st.button(
                f"Apply {mortals} mortal wound{plural}",
                key="mortal_apply",
                type="primary",
                disabled=mortals <= 0,
                use_container_width=True,
            ):
                apply_mortal_wounds(target_uid, target_faction, mortals, target_unit)
                st.session_state[units_key_for(faction)][uid]["turn_flags"][
                    "mortal_effect_applied"
                ] = True
                st.session_state.pending_mortal_undo = {
                    "attacker_uid": uid,
                    "attacker_faction": faction,
                    "target_uid": target_uid,
                    "target_faction": target_faction,
                    "count": mortals,
                    "display_name": display_name,
                }
                log_action(
                    state["round"],
                    "fight",
                    unit.name_en,
                    f"{display_name}: {mortals} mortal wound{plural} → {target_unit.name_en}",
                )
                st.session_state.pending_triggered_relic = None
                st.rerun()


def _maybe_render_mortal_undo(state: dict) -> None:  # type: ignore[type-arg]
    """Show undo section after mortal wounds were applied (until turn end)."""
    undo = st.session_state.get("pending_mortal_undo")
    if not undo:
        return
    atk_uid = undo["attacker_uid"]
    atk_faction = undo["attacker_faction"]
    atk_flags = st.session_state[units_key_for(atk_faction)].get(atk_uid, {}).get("turn_flags", {})
    if not atk_flags.get("mortal_effect_applied"):
        return

    count = undo["count"]
    display_name = undo["display_name"]
    target_uid = undo["target_uid"]
    target_faction = undo["target_faction"]
    target_unit, _ = lookup(target_faction, target_uid)
    plural = "s" if count != 1 else ""

    st.warning(
        f"**{display_name}**: {count} mortal wound{plural} applied to **{target_unit.name_en}** this turn."
    )
    if st.button(
        f"Undo — restore {count} wound{plural} to {target_unit.name_en}",
        key="mortal_undo_btn",
        use_container_width=True,
    ):
        heal_unit(target_uid, target_faction, count, target_unit, revive=True)
        st.session_state[units_key_for(atk_faction)][atk_uid]["turn_flags"][
            "mortal_effect_applied"
        ] = False
        st.session_state.pending_mortal_undo = None
        log_action(
            state["round"],
            "fight",
            display_name,
            f"mortal wounds undone — {count} wound{plural} restored to {target_unit.name_en}",
        )
        st.rerun()
    st.divider()


class FightPhaseHandler:
    """PhaseHandler for the Fight Phase."""

    phase_name: str = "fight"

    def render_start(self, state: dict) -> None:  # type: ignore[type-arg]
        pass

    def render_active(self, state: dict) -> None:  # type: ignore[type-arg]
        first: str = state["first_player"]
        second: str = state["second_player"]
        active_player: str = st.session_state.active

        if st.session_state.get("pending_triggered_relic"):
            _render_mortal_after_melee(state)
            return

        _maybe_render_mortal_undo(state)

        # Priority goes to the inactive (non-active) player.
        # Rerun: the left army column already rendered without a fight player.
        if st.session_state.get("fight_current_player") is None:
            priority = second if active_player == first else first
            st.session_state.fight_current_player = priority
            st.rerun()

        _advance_fight_turn_if_needed(first, second)
        fight_player = st.session_state.fight_current_player

        attack_form_shown = _render_display(state, fight_player, first, second)
        if attack_form_shown:
            return

        st.divider()
        _render_melee_pairs()
        st.divider()

        col1, col2 = st.columns(2)
        with col1:
            _render_fight_column(first, state, fight_player, first, second)
        with col2:
            _render_fight_column(second, state, fight_player, first, second)

    def render_end(self, state: dict) -> None:  # type: ignore[type-arg]
        pass


# ---------------------------------------------------------------------------
# Phase-specific content helpers
# ---------------------------------------------------------------------------


def _render_fight_column(
    faction: str,
    state: dict,  # type: ignore[type-arg]
    fight_player: str,
    first: str,
    second: str,
) -> None:
    """Render one fight column — attacker side or target/waiting side."""
    is_my_turn = faction == fight_player
    indicator = "⚔" if is_my_turn else "◀"
    st.markdown(f"**{indicator} {faction}**")

    if is_my_turn:
        sel = st.session_state.selected_unit
        if sel and sel[0] == faction:
            _, uid = sel
            unit, unit_state = lookup(faction, uid)
            badges = state_badges_html(unit_state)
            st.markdown(f"*{unit.name_en}*")
            if badges:
                st.markdown(badges, unsafe_allow_html=True)
            _active_fight(faction, uid, unit, unit_state, state, first, second)
        else:
            st.caption("← Select a unit from your army list to fight.")
    else:
        # Model-group flow: this side shows the attack assignment for the
        # fighting player's selected group.
        info = group_flow_attacker()
        if info is not None and info[0] == fight_player:
            atk_faction, atk_uid, atk_unit, atk_state = info
            eligible = (
                can_fight(atk_state)
                and can_fight_now(atk_state, first, second)
                and not atk_state.get("turn_flags", {}).get("fought")
            )
            if eligible:
                render_group_assignment(atk_faction, atk_uid, atk_unit, atk_state, use_melee=True)
                return

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
                _inactive_target_stats(faction, uid, unit, unit_state)
                st.divider()
                wound_adjustment_buttons(faction, uid, unit)
        elif st.session_state.get("selected_unit"):
            st.caption("← Designate a target (▷) from your army list.")
        else:
            st.caption("Waiting — opponent selects a unit to fight.")


def _active_fight(
    faction: str,
    uid: str,
    unit,  # type: ignore[type-arg]
    unit_state: dict,  # type: ignore[type-arg]
    state: dict,  # type: ignore[type-arg]
    first: str,
    second: str,
) -> None:
    """Show fight eligibility, fights-first indicator, and melee weapons."""
    flags = unit_state.get("turn_flags", {})
    if flags.get("fought"):
        st.info("Already fought this phase.")
        return
    if not can_fight(unit_state):
        st.warning("Not eligible — not in melee and did not charge this turn.")
        return
    if not can_fight_now(unit_state, first, second):
        st.info("Charged units from both sides must fight first.")
        return

    if any(k.lower() == "fights_first" for k in unit.keywords):
        st.info("Fights First — this unit activates before others.")
    if flags.get("charged"):
        st.markdown("**Fights first** (charged this turn).")

    render_group_cards(faction, uid, unit, unit_state, use_melee=True, phase_key="fight")


def _inactive_target_stats(
    faction: str, uid: str, unit, unit_state: dict  # type: ignore[type-arg]
) -> None:
    """Show target defensive stats (T / Sv / ++) in the fight column."""
    inv_display = f"{unit.invuln_save}+" if unit.invuln_save else "—"
    cols = st.columns(3)
    cols[0].metric("T", unit.toughness)
    cols[1].metric("Sv", f"{unit.save}+")
    cols[2].metric("++", inv_display)


def _render_melee_pairs() -> None:
    """Show all active melee engagements, or the phase rule hint if none."""
    p1 = st.session_state.get("first_player", "")
    p2 = st.session_state.get("second_player", "")
    name_map = {
        p1: {u.id: u.name_en for u in units_list_for(p1)},
        p2: {u.id: u.name_en for u in units_list_for(p2)},
    }
    seen: set[frozenset[str]] = set()
    pairs: list[str] = []
    for uid, s in st.session_state[units_key_for(p1)].items():
        for fac, enemy_uid in s.get("melee_with", []):
            key = frozenset({f"{p1}:{uid}", f"{fac}:{enemy_uid}"})
            if key in seen:
                continue
            seen.add(key)
            a = name_map[p1].get(uid, uid)
            b = name_map.get(fac, {}).get(enemy_uid, enemy_uid)
            pairs.append(f"**{a}** ↔ **{b}**")
    if pairs:
        st.markdown("**Active Melee Engagements:**")
        for p in pairs:
            st.markdown(f"- {p}")
    else:
        st.caption("No active melee engagements.")


def _render_display(
    state: dict,  # type: ignore[type-arg]
    fight_player: str,
    first: str,
    second: str,
) -> bool:
    """Render attack form if applicable. Returns True when the form is shown."""
    decl = st.session_state.get("attack_declaration", {})
    if not decl.get("active") or decl.get("phase_key") != "fight":
        return False
    if decl.get("atk_faction") != fight_player:
        # Stale declaration from the previous player's fight turn — discard it.
        st.session_state.attack_declaration = {"active": False, "entries": []}
        return False
    render_attack_resolution("fight")
    return True
