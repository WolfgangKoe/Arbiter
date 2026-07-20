"""PsychicPhaseHandler — Psychic Phase for WH40k 9E.

Ziel 4f: Manifest (2D6 ≥ WC 5), Deny, Perils of the Warp, Smite.
Scope: Smite only. Blessing-flow (friendly target) follows in a later goal.
"""

from __future__ import annotations

from collections.abc import MutableMapping
from typing import Any, ClassVar

import streamlit as st

from constants.symbols import SYM_COLLAPSE, SYM_EXPAND
from gameMechanic.abilityEngine import find_unit_ability_by_effect
from gameMechanic.gameLog import log_action
from gameMechanic.gameState import unit_keys_for, units_key_for, units_list_for
from gameMechanic.unitMutations import apply_damage
from gameObjects.unit import Unit
from uiLayout._common import (
    lookup,
    render_explode_tiles_for_destroyed,
    render_mortal_wounds_cards_for_destroyed,
    render_reactive_ability_box,
    render_reactive_stratagem_box,
)


class PsychicPhaseHandler:
    """PhaseHandler for the Psychic Phase."""

    phase_name: ClassVar[str] = "psychic"

    def render_active(self, state: MutableMapping[str, Any]) -> None:
        first: str = state["first_player"]
        second: str = state["second_player"]

        # Track deny uses per faction within this phase (each faction can deny once).
        if "psychic_denies_used" not in st.session_state:
            st.session_state.psychic_denies_used = {}

        render_mortal_wounds_cards_for_destroyed(first, second)
        render_explode_tiles_for_destroyed(first, second)
        col1, col2 = st.columns(2)
        with col1:
            _render_psychic_column(first, state)
        with col2:
            _render_psychic_column(second, state)


# ---------------------------------------------------------------------------
# Pure helper functions (also exported for tests)
# ---------------------------------------------------------------------------


def has_psyker(units: list[Unit]) -> bool:
    return any(u.has_keyword("PSYKER") for u in units)


def can_deny(units: list[Unit]) -> bool:
    """R-PSYCHIC-16: a PSYKER or a unit-owned ``deny_psychic`` ability (e.g.
    Szarekh's Noctilith Beacons or the Canoptek Spyder's Gloom Prism) may
    attempt to deny a psychic power. Gloom Prism migrated off the old
    wargear-name gate onto this same ``find_unit_ability_by_effect`` ability
    path in S163 (B-028b-Rest) — both deny_psychic sources now render via
    ``_render_deny_ability_cards`` below instead of one being roll-UI-only."""

    def _unit_can_deny(u: Unit) -> bool:
        if u.has_keyword("PSYKER"):
            return True
        parts = u.id.split(".")
        if len(parts) < 2:
            return False
        return find_unit_ability_by_effect(parts[1], u.id, "deny_psychic") is not None

    return any(_unit_can_deny(u) for u in units)


def initial_deny_state(opponent_units: list[Unit]) -> bool | None:
    """R-PSYCHIC-16 / Deny the Witch (core_rules.txt:1274, 1302-1313): only a
    PSYKER unit (or deny wargear) may attempt to deny a psychic power. If the
    opponent has neither, no deny attempt is possible — the power resolves
    unopposed (``False``) instead of sitting in the ``None`` "awaiting a deny
    attempt" state forever."""
    return None if can_deny(opponent_units) else False


def smite_targets(
    selected_targets: list[tuple[str, str]], own_faction: str
) -> list[tuple[str, str]]:
    """Smite targets = every selected unit that is not the PSYKER's own faction.

    The damage button renders once this list is non-empty; the selection itself
    comes from the inactive player's unit cards (``_TARGET_PHASES`` in
    ``uiLayout/unitCard.py`` must include ``"psychic"`` — S129 fix)."""
    return [t for t in selected_targets if t[0] != own_faction]


def is_perils(roll: int) -> bool:
    return roll in (2, 12)


def smite_damage_die(roll: int) -> str:
    return "W6" if roll >= 11 else "W3"


def deny_succeeds(manifest_roll: int, deny_roll: int) -> bool:
    return deny_roll > manifest_roll


def cast_eligibility(unit_state: MutableMapping[str, Any]) -> tuple[bool, str | None]:
    """Return (eligible, reason) — None reason means eligible to manifest."""
    flags = unit_state.get("turn_flags", {})
    if flags.get("retreated"):
        return False, "Retreated this turn — cannot manifest psychic powers."
    if flags.get("cast"):
        return False, "Already manifested this phase — each PSYKER may only be chosen once."
    return True, None


SMITE_BASE_WARP_CHARGE = 5
PERILS_DAMAGE_DIE = "W3"


def smite_warp_charge(prior_attempts_this_phase: int) -> int:
    """R-PSYCHIC-17/18: Smite has Warp Charge 5, +1 per prior manifest attempt this phase."""
    return SMITE_BASE_WARP_CHARGE + prior_attempts_this_phase


def is_manifested(roll: int, warp_charge: int) -> bool:
    """R-PSYCHIC-11: a Psychic test passes when 2D6 is equal to or greater than the warp charge."""
    return roll >= warp_charge


def perils_pending(psi: dict) -> bool:  # type: ignore[type-arg]
    """R-PSYCHIC-22 gate: Perils was suffered but its mortal wounds are not yet applied."""
    return bool(psi.get("perils")) and not psi.get("perils_applied")


def faction_deny_used(denies_used: dict, faction: str) -> bool:  # type: ignore[type-arg]
    """R-PSYCHIC-16: a faction may attempt Deny the Witch at most once per Psychic Phase."""
    return bool(denies_used.get(faction))


def can_attempt_deny(
    psi: dict | None, faction: str, denies_used: dict  # type: ignore[type-arg]
) -> bool:
    """R-PSYCHIC-16: only one deny attempt per power — possible only while a manifested
    power is still unresolved (``denied is None``) and the faction has not denied this phase."""
    if faction_deny_used(denies_used, faction):
        return False
    if psi is None or not psi.get("manifested"):
        return False
    return psi.get("denied") is None


def refund_deny(denies_used: dict, faction: str | None) -> dict:  # type: ignore[type-arg]
    """Return a copy of the deny-budget map with ``faction``'s deny refunded.

    A power reset (or a deny undo) takes back the whole attempt, so the
    once-per-phase deny spent against it is returned. ``None`` means nothing was
    spent — the map is returned unchanged. Pure: the input map is not mutated.
    """
    refunded = dict(denies_used)
    if faction is not None:
        refunded.pop(faction, None)
    return refunded


def cleared_deny(psi: dict) -> dict:  # type: ignore[type-arg]
    """Return a copy of ``psi`` with the deny decision undone (back to unresolved).

    Symmetric counterpart to the active side's reset: ``denied``/``deny_roll``/
    ``deny_faction`` go back to ``None`` while the manifested power stands. Pure:
    the input dict is not mutated.
    """
    cleared = dict(psi)
    cleared["denied"] = None
    cleared["deny_roll"] = None
    cleared["deny_faction"] = None
    return cleared


# ---------------------------------------------------------------------------
# Column rendering
# ---------------------------------------------------------------------------


def _reset_active_power() -> None:
    """Clear the current power and refund any deny the inactive faction spent on it."""
    psi = st.session_state.get("psi_result")
    deny_faction = psi.get("deny_faction") if psi else None
    st.session_state.psi_result = None
    st.session_state.psychic_denies_used = refund_deny(
        st.session_state.get("psychic_denies_used", {}), deny_faction
    )


def _render_manifest_reroll(faction: str, uid: str) -> None:
    """Command Re-Roll anchor for the manifest roll (design_system.md
    §6.2/§6.3, S135 Paket 4b) — migrated from the Pull-not-Push inline offer
    to the canonical GO card. `_render_psi_result` opens this same window at
    three mutually exclusive branches (Perils pending / failed / manifested-
    not-denied), factored out here so the migration does not triple the call.
    """
    render_reactive_stratagem_box(
        faction,
        "psychic",
        "after_roll",
        decline_key=f"psi_manifest_{uid}",
        context_caption="A Psychic test manifest roll was just made.",
        effect_type="reroll",
        on_resolved=_reset_active_power,
    )


def _render_psychic_column(faction: str, state: MutableMapping[str, Any]) -> None:
    is_active = faction == state["active"]
    indicator = SYM_EXPAND if is_active else SYM_COLLAPSE
    st.markdown(f"**{indicator} {faction}**")

    if is_active:
        _render_active_psychic(faction, state)
    else:
        _render_deny_column(faction, state)


def _render_active_psychic(faction: str, state: MutableMapping[str, Any]) -> None:
    units = units_list_for(faction)

    if not has_psyker(units):
        st.caption("No PSYKER units — skip this phase.")
        return

    sel = st.session_state.selected_unit
    if not sel or sel[0] != faction:
        st.caption("← Select a PSYKER from your army list.")
        return

    _, uid = sel
    unit, unit_state = lookup(faction, uid)
    st.markdown(f"*{unit.name_en}*")

    if not unit.has_keyword("PSYKER"):
        st.warning("Not a PSYKER — select a PSYKER unit.")
        return

    eligible, reason = cast_eligibility(unit_state)
    if not eligible:
        st.warning(reason)
        return

    _render_smite_flow(faction, uid, unit, state)


def _render_smite_flow(faction: str, uid: str, unit: Unit, state: MutableMapping[str, Any]) -> None:
    psi = st.session_state.get("psi_result")

    if psi is not None and psi.get("faction") == faction and psi.get("uid") == uid:
        _render_psi_result(faction, uid, unit, psi, state)
        return

    # No active result — show manifest input.
    wc = smite_warp_charge(st.session_state.get("psi_attempts_this_phase", 0))
    st.markdown(f"**Smite** — Warp Charge {wc}")
    roll = st.number_input(
        "2D6 roll",
        min_value=2,
        max_value=12,
        value=7,
        key=f"psi_roll_{faction}_{uid}",
    )
    if st.button(
        "Attempt Manifest",
        key=f"psi_manifest_{faction}_{uid}",
        type="primary",
        use_container_width=True,
    ):
        manifested = is_manifested(int(roll), wc)
        perils = is_perils(int(roll))
        st.session_state.psi_attempts_this_phase = (
            st.session_state.get("psi_attempts_this_phase", 0) + 1
        )
        opponent = (
            state["second_player"] if faction == state["first_player"] else state["first_player"]
        )
        denied = initial_deny_state(units_list_for(opponent))
        st.session_state.psi_result = {
            "faction": faction,
            "uid": uid,
            "roll": int(roll),
            "manifested": manifested,
            "perils": perils,
            "perils_applied": False,
            "denied": denied,
            "deny_roll": None,
            "deny_faction": None,
        }
        outcome = "manifested" if manifested else "failed"
        perils_note = " (Perils!)" if perils else ""
        log_action(
            state["round"],
            "psychic",
            unit.name_en,
            f"Smite manifest roll {int(roll)} — {outcome}{perils_note}",
        )
        st.rerun()


def _render_psi_result(
    faction: str,
    uid: str,
    unit: Unit,
    psi: dict,  # type: ignore[type-arg]
    state: MutableMapping[str, Any],
) -> None:
    roll: int = psi["roll"]
    manifested: bool = psi["manifested"]
    denied = psi["denied"]  # None | True | False
    # Command Re-Roll (core_rules.txt Z. 3124-3130): the manifest roll is still
    # "the last roll" only while no later roll has superseded it (no deny
    # attempt has resolved yet) and, if Perils triggered, its mortal wounds
    # have not already been applied — that's a real consequence this app
    # cannot cleanly undo, so the offer stops appearing once it lands.
    manifest_rerollable = psi.get("deny_faction") is None and not psi.get("perils_applied")

    # Perils must be resolved before anything else.
    if perils_pending(psi):
        if manifested:
            st.error(f"**Perils of the Warp!** Roll {roll} — power manifested.")
        else:
            st.error(f"**Perils of the Warp!** Roll {roll} — power failed.")
        if manifest_rerollable:
            _render_manifest_reroll(faction, uid)
        st.markdown(f"Apply {PERILS_DAMAGE_DIE} mortal wounds to *{unit.name_en}*:")
        perils_dmg = st.number_input(
            "Perils damage (1–3)",
            min_value=1,
            max_value=3,
            value=2,
            key=f"psi_perils_dmg_{faction}_{uid}",
        )
        if st.button(
            f"Apply to {unit.name_en}",
            key=f"psi_perils_apply_{faction}_{uid}",
            type="primary",
            use_container_width=True,
        ):
            apply_damage(uid, faction, int(perils_dmg), unit, mortal=True)
            psi["perils_applied"] = True
            st.session_state.psi_result = psi
            log_action(
                state["round"],
                "psychic",
                unit.name_en,
                f"Perils of the Warp — {int(perils_dmg)} mortal wounds",
            )
            st.rerun()
        return

    # Power failed (and no perils, or perils already applied).
    if not manifested:
        st.warning(f"Roll {roll} — Power failed (< 5).")
        if manifest_rerollable:
            _render_manifest_reroll(faction, uid)
        if st.button("Reset", key=f"psi_reset_{faction}_{uid}", use_container_width=True):
            _reset_active_power()
            st.rerun()
        return

    # Power denied.
    if denied is True:
        st.warning(f"Roll {roll} — Manifested, but Denied!")
        if st.button("Reset", key=f"psi_reset_denied_{faction}_{uid}", use_container_width=True):
            _reset_active_power()
            st.rerun()
        return

    # Manifested and not denied — show Smite application.
    die = smite_damage_die(roll)
    if denied is None:
        st.success(f"Roll {roll} — Manifested! Waiting for deny attempt… ({die} mortal wounds)")
    elif psi.get("deny_faction") is None:
        st.success(f"Roll {roll} — Manifested! No deny possible. ({die} mortal wounds)")
    else:
        st.success(f"Roll {roll} — Manifested! Deny failed. ({die} mortal wounds)")

    if manifest_rerollable:
        _render_manifest_reroll(faction, uid)

    targets = smite_targets(st.session_state.selected_targets, faction)
    if not targets:
        st.caption(
            "① Click an enemy unit in their army list to mark it as Smite target,"
            " then the damage button appears."
        )
    else:
        for tgt_faction, tgt_uid in targets:
            tgt_unit, _ = lookup(tgt_faction, tgt_uid)
            st.markdown(f"**Smite → {tgt_unit.name_en}** ({die})")
            max_val = 6 if die == "W6" else 3
            smite_dmg = st.number_input(
                f"Mortal wounds (1–{max_val})",
                min_value=1,
                max_value=max_val,
                value=max(1, max_val // 2),
                key=f"psi_smite_dmg_{faction}_{uid}_{tgt_uid}",
            )
            if st.button(
                f"Apply {int(smite_dmg)} mortal wounds to {tgt_unit.name_en}",
                key=f"psi_smite_apply_{faction}_{uid}_{tgt_uid}",
                type="primary",
                use_container_width=True,
            ):
                apply_damage(tgt_uid, tgt_faction, int(smite_dmg), tgt_unit, mortal=True)
                unit_key = units_key_for(faction)
                st.session_state[unit_key][uid]["turn_flags"]["cast"] = True
                log_action(
                    state["round"],
                    "psychic",
                    unit.name_en,
                    f"Smite → {tgt_unit.name_en}: {int(smite_dmg)} mortal wounds",
                )
                st.session_state.psi_result = None
                st.session_state.selected_targets = []
                st.rerun()

    if st.button("Reset (skip Smite)", key=f"psi_skip_{faction}_{uid}", use_container_width=True):
        _reset_active_power()
        st.rerun()


# ---------------------------------------------------------------------------
# Inactive player — deny column
# ---------------------------------------------------------------------------


def _render_deny_ability_cards(faction: str) -> None:
    """Reactive GO card(s) for unit-owned Deny the Witch sources (B-028b).

    First productive callsite of the B-028a reactive-ability infrastructure
    (``render_reactive_ability_box``). PSYKER and deny-wargear sources keep
    the roll UI below unconditional, exactly as before — this only surfaces
    a card for ability-based sources (unit_ability with ``effect.type ==
    "deny_psychic"``, e.g. Szarekh's Noctilith Beacons), so they get the same
    Use/Undo bookkeeping as any other reactive GO. Additive: declining or
    ignoring the card does not block the roll UI, which stays gated solely by
    ``can_deny()`` as before — no existing deny path changes behaviour.
    """
    units = units_list_for(faction)
    uids = unit_keys_for(faction)
    for uid, unit in zip(uids, units):
        parts = unit.id.split(".")
        if len(parts) < 2:
            continue
        ability = find_unit_ability_by_effect(parts[1], unit.id, "deny_psychic")
        if ability is None:
            continue
        render_reactive_ability_box(
            faction,
            "psychic",
            "opponent_psychic_phase",
            [ability],
            decline_key=f"deny_ability_{uid}",
            context_caption=f"{unit.name_en} may attempt to deny as if it were a PSYKER.",
            unit_key=uid,
        )


def _render_deny_column(faction: str, state: MutableMapping[str, Any]) -> None:
    units = units_list_for(faction)

    if not can_deny(units):
        st.caption("No PSYKER or deny wargear — cannot deny.")
        return

    denies_used = st.session_state.get("psychic_denies_used", {})
    psi = st.session_state.get("psi_result")

    if psi is None or not psi.get("manifested"):
        st.caption(
            "Waiting for psychic manifest attempt."
            if psi is None
            else "Manifest failed — no deny needed."
        )
        return

    denied = psi.get("denied")

    # Already decided against *this* power — offer the symmetric undo.
    if denied is True:
        st.success("Denied!")
        _render_undo_deny_button(faction, psi, denies_used)
        return

    if denied is False:
        st.warning("Deny failed." if psi.get("deny_roll") is not None else "Deny skipped.")
        _render_undo_deny_button(faction, psi, denies_used)
        return

    # Undecided (denied is None): gate by the once-per-phase budget (R-PSYCHIC-16).
    if faction_deny_used(denies_used, faction):
        st.caption("Deny already used this phase (one deny attempt per phase per source).")
        return
    if not can_attempt_deny(psi, faction, denies_used):
        return
    _render_deny_ability_cards(faction)
    manifest_roll: int = psi["roll"]
    st.markdown(f"**Deny the Witch: 2D6 > {manifest_roll}**")
    deny_roll = st.number_input(
        "Deny roll (2D6)",
        min_value=2,
        max_value=12,
        value=7,
        key=f"deny_roll_{faction}",
    )
    col_a, col_b = st.columns(2)
    with col_a:
        if st.button(
            "Attempt Deny",
            key=f"deny_btn_{faction}",
            type="primary",
            use_container_width=True,
        ):
            succeeded = deny_succeeds(manifest_roll, int(deny_roll))
            psi["denied"] = succeeded
            psi["deny_roll"] = int(deny_roll)
            psi["deny_faction"] = faction
            st.session_state.psi_result = psi
            # Mark deny as used for this faction — only one deny per phase.
            used = st.session_state.get("psychic_denies_used", {})
            used[faction] = True
            st.session_state.psychic_denies_used = used
            outcome = "succeeded" if succeeded else "failed"
            log_action(
                state["round"],
                "psychic",
                faction,
                f"Deny {outcome} (roll {int(deny_roll)} vs {manifest_roll})",
            )
            st.rerun()
    with col_b:
        if st.button("Skip Deny", key=f"deny_skip_{faction}", use_container_width=True):
            # Explicitly mark as not denied so Smite proceeds (skip keeps the budget).
            psi["denied"] = False
            psi["deny_faction"] = faction
            st.session_state.psi_result = psi
            st.rerun()


def _undo_deny(faction: str, psi: dict, denies_used: dict) -> None:  # type: ignore[type-arg]
    """Return the deny decision to undecided and refund the once-per-phase budget.

    Shared by the plain "Undo deny" button and the Command Re-Roll GO card
    below — both reopen the exact same state, the CP/usage bookkeeping is
    what differs (spend_stratagem via render_reactive_stratagem_box's Use
    vs. free undo).
    """
    st.session_state.psi_result = cleared_deny(psi)
    st.session_state.psychic_denies_used = refund_deny(denies_used, psi.get("deny_faction"))


def _render_undo_deny_button(
    faction: str, psi: dict, denies_used: dict  # type: ignore[type-arg]
) -> None:
    """Symmetric reset for the inactive side: take the deny decision back and
    refund the once-per-phase budget so the power returns to undecided.

    Command Re-Roll (core_rules.txt Z. 3124-3130) applies only when an actual
    Deny the Witch test was rolled — "Skip Deny" declined the attempt, so
    there is no roll to re-roll (`deny_roll` stays None in that case).
    """
    if psi.get("deny_roll") is not None:
        render_reactive_stratagem_box(
            faction,
            "psychic",
            "after_roll",
            decline_key=f"deny_{faction}",
            context_caption=f"{faction} made a Deny the Witch test.",
            effect_type="reroll",
            on_resolved=lambda: _undo_deny(faction, psi, denies_used),
        )
    if st.button("Undo deny", key=f"deny_undo_{faction}", use_container_width=True):
        _undo_deny(faction, psi, denies_used)
        st.rerun()
