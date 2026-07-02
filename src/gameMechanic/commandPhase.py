from __future__ import annotations

from typing import Any

import streamlit as st

from constants.symbols import SYM_COLLAPSE, SYM_EXPAND
from gameMechanic.ability_engine import get_activated_command_abilities, get_triggered_abilities
from gameMechanic.game_log import log_action
from gameMechanic.game_state import (
    TargetSelectionRequest,
    faction_dir_for,
    unit_id_from_state_key,
    units_key_for,
    units_list_for,
)
from gameMechanic.phase_handler import PhaseHandler  # noqa: F401 — used for type checking
from gameMechanic.unit_mutations import adjust_cp
from gameObjects.ability import Ability
from gameObjects.loader import activated_wargear_ids, load_unit_abilities, load_wargear_catalog
from gameObjects.unit import Unit
from uiLayout._common import (
    lookup,
    state_badges_html,
    wound_adjustment_buttons,
)


def resolve_command_start(state: dict) -> list[tuple[Ability, list[str]]]:  # type: ignore[type-arg]
    return get_triggered_abilities(state, "command", "phase_start")


# ---------------------------------------------------------------------------
# Pure helpers — army-wide command-phase ability checks (exported for tests)
# ---------------------------------------------------------------------------


def unit_has_command_ability(unit: Unit, faction_dir: str) -> bool:
    """Return True when *unit* has at least one command-phase ability.

    Checks three orthogonal sources (all data-driven, no faction strings):
    1. Activated unit abilities with trigger phase "command".
    2. Activated wargear (ability_type: activated in wargear.yaml).
    3. Triggered relics that fire at command phase_start (e.g. gain_cp_roll).
    """
    unit_abilities = load_unit_abilities(faction_dir)
    for a in unit_abilities:
        if a.ability_type != "activated":
            continue
        if a.unit_id != unit.id:
            continue
        phases = a.trigger.phase if isinstance(a.trigger.phase, list) else [a.trigger.phase]
        if "command" in phases:
            return True

    activated_ids = activated_wargear_ids(faction_dir)
    if any(wid in activated_ids for wid in unit.wargear_ids):
        return True

    if unit.get_triggered_effect("phase_start", "command", "gain_cp_roll") is not None:
        return True

    return False


def units_with_command_abilities(player: str) -> list[Unit]:
    """Return all units in *player*'s army that have at least one command-phase ability."""
    faction_dir = faction_dir_for(player)
    return [u for u in units_list_for(player) if unit_has_command_ability(u, faction_dir)]


# ---------------------------------------------------------------------------
# CP grant
# ---------------------------------------------------------------------------


def can_gain_command_point(game_mode: str) -> bool:
    """Return True when the army is Battle-forged and therefore eligible for the CP grant.

    In 9E the Command-Phase +1 CP is gated on the army being Battle-forged.
    Matched Play and Crusade armies are Battle-forged; Open Play armies are not.
    The app stores the chosen mode in session_state.game_mode ('matched' | 'open' | 'crusade').
    """
    return game_mode in ("matched", "crusade")


def _render_faction_actions(
    faction: str,
    state: dict,  # type: ignore[type-arg]
) -> None:
    st.divider()
    game_mode: str = st.session_state.get("game_mode", "matched")
    if not can_gain_command_point(game_mode):
        st.caption("Open Play — no Battle-forged CP grant.")
        return
    st.markdown(f"**+1 CP for {faction}**")
    already_granted = st.session_state.get("cp_granted_this_phase", False)
    if already_granted:
        st.caption("Already granted this phase.")
    else:
        if st.button("Grant +1 CP", key="cmd_cp", type="primary", use_container_width=True):
            adjust_cp(faction, 1)
            log_action(state["round"], "command", faction, "+1 CP received")
            st.session_state.cp_granted_this_phase = True
            st.rerun()


# ---------------------------------------------------------------------------
# Pure helpers — extracted so they are testable without Streamlit
# ---------------------------------------------------------------------------


def resolve_gain_cp_roll(
    amount: int,
    roll_succeeded: bool,
    already_rolled: bool,
) -> tuple[int, bool]:
    """Resolve a once-per-phase gain_cp_roll: return (cp_delta, locked).

    Args:
        amount: number of CP to gain on a successful roll.
        roll_succeeded: True when the player reported a roll at or above the threshold.
        already_rolled: True when the lock flag is already set (once-per-phase).

    Returns:
        (cp_delta, locked): cp_delta is `amount` on success else 0; locked is always
        True after a resolution. Raises ValueError if already_rolled is True.
    """
    if already_rolled:
        raise ValueError("gain_cp_roll already resolved this Command Phase")
    return (amount if roll_succeeded else 0), True


# ---------------------------------------------------------------------------
# Generic buff_roll ability renderer
# ---------------------------------------------------------------------------


def _render_buff_roll_ability(
    ability: Ability,
    faction: str,
    state: dict,  # type: ignore[type-arg]
    units_state: dict,  # type: ignore[type-arg]
    unit_by_id: dict,  # type: ignore[type-arg]
) -> None:
    """Render activate / status UI for any buff_roll command-phase ability.

    Some abilities grant extra uses when the owning model has a given keyword
    (data-driven via the ability's ``extra_uses``). Uses are tracked as a list
    of target unit keys; max uses = 1 + the owner's data-driven keyword bonus.
    """
    ability_id = ability.id
    cmd_state: dict = st.session_state.get("command_ability_state", {})  # type: ignore[type-arg]
    this_state: dict = cmd_state.get(ability_id, {})  # type: ignore[type-arg]

    # Support both the multi-target list and the legacy single-target shape.
    targets: list[str] = list(
        this_state.get("targets")
        or ([this_state["target_uid"]] if this_state.get("target_uid") else [])
    )
    active_since_round: int | None = this_state.get("active_since_round")

    # Expire when a new command phase begins (round has advanced)
    if active_since_round is not None and state["round"] > active_since_round:
        for t in targets:
            if t in units_state:
                bufs: list[dict] = units_state[t].get("active_buffs", [])
                units_state[t]["active_buffs"] = [
                    b for b in bufs if b.get("ability_id") != ability_id
                ]
        cmd_state[ability_id] = {}
        st.session_state.command_ability_state = cmd_state
        targets = []

    owner = unit_by_id.get(ability.unit_id)
    max_uses = 1 + ability.bonus_uses_for(owner)
    effect_desc = "re-roll 1s to hit" if ability.effect.type == "reroll_hit_1" else "+1 to hit"

    st.divider()
    st.markdown(f"**{ability.name_en}**")

    _ptr = st.session_state.get("pending_target_request")
    awaiting = _ptr is not None and _ptr.ability_id == ability_id

    for t in targets:
        target_unit = unit_by_id.get(unit_id_from_state_key(t))
        name = target_unit.name_en if target_unit else t
        st.success(f"Active — **{name}** {effect_desc} until your next Command Phase.")

    uses = len(targets)
    if awaiting:
        st.info("Select an eligible unit from your army list.")
        if st.button("Cancel", key=f"cmd_cancel_{ability_id}", use_container_width=True):
            st.session_state.pending_target_request = None
            st.rerun()
    elif uses < max_uses:
        label = f"Activate {ability.name_en}"
        if max_uses > 1:
            label += f" ({uses + 1}/{max_uses})"
        if st.button(
            label,
            key=f"cmd_activate_{ability_id}",
            type="primary",
            use_container_width=True,
        ):
            required_kws = [kw for cond in ability.conditions for kw in (cond.has_keywords or [])]
            st.session_state.pending_target_request = TargetSelectionRequest(
                ability_id=ability_id,
                required_keywords=required_kws,
                exclude_uid=None,
                faction_filter="own",
                multi=False,
                badge_label=ability.badge_label or ability.name_en,
                effect_type=ability.effect.type,
            )
            st.rerun()


# ---------------------------------------------------------------------------
# gain_cp_roll — relic triggered effect: roll a die, gain CP on threshold+
# ---------------------------------------------------------------------------


def _render_gain_cp_roll(unit, faction: str, state: dict) -> None:  # type: ignore[type-arg]
    from gameObjects.unit import TriggeredEffect  # local import avoids circular dep

    te: TriggeredEffect | None = unit.get_triggered_effect("phase_start", "command", "gain_cp_roll")
    if not te:
        return

    display_name = unit.relic_name or unit.relic_id
    threshold = te.threshold or 4
    amount = te.amount or 1
    fail_label = f"1–{threshold - 1} (Failed)"
    success_label = f"{threshold}+ (Success)"

    st.divider()
    st.markdown(f"**{display_name}**")
    if st.session_state.get("morgog_cap_rolled_this_phase"):
        st.caption("Already rolled this Command Phase.")
        return
    st.caption(f"Roll {te.dice or 'D6'}: on a {threshold}+, gain {amount} CP.")
    col1, col2 = st.columns(2)
    with col1:
        if st.button(
            success_label,
            key=f"cp_roll_success_{unit.relic_id}",
            type="primary",
            use_container_width=True,
        ):
            cp_delta, locked = resolve_gain_cp_roll(amount, True, False)
            adjust_cp(faction, cp_delta)
            log_action(
                state["round"], "command", faction, f"{display_name}: {threshold}+ — +{cp_delta} CP"
            )
            st.session_state.morgog_cap_rolled_this_phase = locked
            st.rerun()
    with col2:
        if st.button(fail_label, key=f"cp_roll_fail_{unit.relic_id}", use_container_width=True):
            _, locked = resolve_gain_cp_roll(amount, False, False)
            log_action(state["round"], "command", faction, f"{display_name}: failed — no CP")
            st.session_state.morgog_cap_rolled_this_phase = locked
            st.rerun()


# ---------------------------------------------------------------------------
# Activated wargear — generic flow (target selection + manual adjustment),
# separate from the unit_abilities system. Data-driven from wargear.yaml.
# ---------------------------------------------------------------------------


def _wargear_once_per_battle(wargear: dict) -> bool:  # type: ignore[type-arg]
    """Read the once_per_battle flag from a wargear entry's conditions."""
    return any(c.get("once_per_battle") for c in wargear.get("conditions", []))


def _wargear_state_key(bearer_uid: str, wargear_id: str) -> str:
    """Per-bearer-instance state key for an activated wargear.

    Two units carrying the same wargear (same wargear_id — e.g. two Overlords each
    with a Resurrection Orb) must not share once-per-battle / target state. Including
    the bearer's per-instance uid keeps each bearer's activation independent.
    """
    return f"revive_wargear_{bearer_uid}_{wargear_id}"


def _render_activated_wargear(
    faction: str,
    state: dict,  # type: ignore[type-arg]
    units_state: dict,  # type: ignore[type-arg]
    unit_by_id: dict,  # type: ignore[type-arg]
    bearer: Any,
    wargear: dict,  # type: ignore[type-arg]
    bearer_uid: str = "",
) -> None:
    """Generic renderer for ``ability_type: activated`` wargear.

    Name and once_per_battle are read from the wargear entry; both session
    state AND Streamlit widget keys are namespaced by ``request_id`` (bearer +
    wargear id) so two bearers of the same wargear never collide.
    """
    wargear_id = wargear["id"]
    name = wargear.get("name_en", wargear_id)
    request_id = _wargear_state_key(bearer_uid, wargear_id)
    once_per_battle = _wargear_once_per_battle(wargear)

    st.divider()
    st.markdown(f"**{name}**")

    if once_per_battle and st.session_state.wargear_used.get(request_id, False):
        st.caption("Already used this battle.")
        return

    targets = st.session_state.get("revive_wargear_target_uid", {})
    target_uid = targets.get(request_id)
    if target_uid:
        target_unit = unit_by_id.get(target_uid)
        if target_unit:
            st.caption(f'Target: **{target_unit.name_en}** — verify within 6" on table')
            wound_adjustment_buttons(st.session_state.get("active", ""), target_uid, target_unit)
        if st.button(
            f"Confirm & Close {name}",
            key=f"cmd_revive_wargear_confirm_{request_id}",
            use_container_width=True,
        ):
            target_name = target_unit.name_en if target_unit else target_uid
            bearer_name = bearer.name_en if bearer else "Bearer"
            st.session_state.wargear_used[request_id] = True
            log_action(state["round"], "command", bearer_name, f"{name} → {target_name}")
            targets.pop(request_id, None)
            st.rerun()
    elif (
        st.session_state.get("pending_target_request") is not None
        and st.session_state.pending_target_request.ability_id == request_id
    ):
        st.info("Select a target unit from your army list.")
        if st.button("Cancel", key=f"revive_wargear_cancel_{request_id}", use_container_width=True):
            st.session_state.pending_target_request = None
            st.rerun()
    else:
        if st.button(
            f"Use {name}",
            key=f"cmd_revive_wargear_{request_id}",
            type="primary",
            use_container_width=True,
        ):
            st.session_state.pending_target_request = TargetSelectionRequest(
                ability_id=request_id,
                required_keywords=[],
                exclude_uid=bearer_uid,
                faction_filter="own",
                multi=False,
                badge_label="Revive",
                effect_type="",
            )
            st.rerun()


# ---------------------------------------------------------------------------
# Generic unit command-phase ability renderer
# ---------------------------------------------------------------------------


def _render_unit_command_abilities(
    selected_state_key: str,
    faction: str,
    state: dict,  # type: ignore[type-arg]
    units_state: dict,  # type: ignore[type-arg]
    unit_by_id: dict,  # type: ignore[type-arg]
) -> None:
    """Render all activated command-phase abilities for the currently selected unit."""
    unit_id = unit_id_from_state_key(selected_state_key)
    faction_dir = faction_dir_for(faction)
    abilities = get_activated_command_abilities(unit_id, faction_dir)

    for ability in abilities:
        if ability.effect.type in ("buff_roll", "reroll_hit_1"):
            _render_buff_roll_ability(ability, faction, state, units_state, unit_by_id)

    unit = unit_by_id.get(unit_id)
    activated_ids = activated_wargear_ids(faction_dir)
    catalog = load_wargear_catalog(faction_dir)
    for wid in unit.wargear_ids if unit else []:
        if wid in activated_ids:
            _render_activated_wargear(
                faction,
                state,
                units_state,
                unit_by_id,
                unit,
                catalog[wid],
                bearer_uid=selected_state_key,
            )
    if unit and unit.get_triggered_effect("phase_start", "command", "gain_cp_roll"):
        _render_gain_cp_roll(unit, faction, state)


# ---------------------------------------------------------------------------
# Army-wide command-phase hint (render only)
# ---------------------------------------------------------------------------


def _render_command_ability_hint(faction: str) -> None:
    """Show which units in *faction*'s army have command-phase abilities.

    Analogous to the PSYKER hint in the psychic phase: always visible in the
    active column so the player knows which unit to select. Render-only — not
    covered by automated tests; must be verified manually.
    """
    able_units = units_with_command_abilities(faction)
    if not able_units:
        return
    names = ", ".join(u.name_en for u in able_units)
    st.caption(f"Units with command-phase abilities: {names}")


# ---------------------------------------------------------------------------
# PhaseHandler implementation
# ---------------------------------------------------------------------------


class CommandPhaseHandler:
    """PhaseHandler for the Command Phase."""

    phase_name: str = "command"

    def render_start(self, state: dict) -> None:  # type: ignore[type-arg]
        pass

    def render_active(self, state: dict) -> None:  # type: ignore[type-arg]
        first: str = state["first_player"]
        second: str = state["second_player"]

        col1, col2 = st.columns(2)
        with col1:
            _render_command_column(first, state)
        with col2:
            _render_command_column(second, state)

    def render_end(self, state: dict) -> None:  # type: ignore[type-arg]
        pass


def _render_command_column(faction: str, state: dict) -> None:  # type: ignore[type-arg]
    is_active = faction == state["active"]
    indicator = SYM_EXPAND if is_active else SYM_COLLAPSE
    st.markdown(f"**{indicator} {faction}**")

    if not is_active:
        st.caption("—")
        return

    sel = st.session_state.selected_unit

    if sel and sel[0] == faction:
        _, uid = sel
        unit, unit_state = lookup(faction, uid)
        badges = state_badges_html(unit_state)
        st.markdown(f"*{unit.name_en}*")
        if badges:
            st.markdown(badges, unsafe_allow_html=True)
        st.divider()

    unit_by_id = {u.id: u for u in units_list_for(faction)}
    units_key = units_key_for(faction)
    units_state: dict = state[units_key]  # type: ignore[type-arg]

    _render_faction_actions(faction, state)

    _render_command_ability_hint(faction)

    # Render activated command-phase abilities for the selected unit (any faction)
    if sel and sel[0] == faction:
        _, selected_uid = sel
        _render_unit_command_abilities(selected_uid, faction, state, units_state, unit_by_id)
