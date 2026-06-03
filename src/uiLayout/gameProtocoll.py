"""gameProtocoll — Command Protocol log + Stratagems tab.

Two tabs in the center column below the gameActionDisplayArea:
  - CommandProtocol: round/phase log navigator (setup summary for now)
  - Stratagems:      GO list with visibility logic (data structure ready; Ziel 4)

GO visibility states (see docs/spec/processes.md P-06 and gameObjects/stratagem.py):
  clickable  — conditions met, CP available, not yet used this phase
  greyed     — conditions met, but CP insufficient OR already used this phase
  hidden     — conditions not met → not rendered at all
"""

import json
from itertools import groupby
from pathlib import Path

import streamlit as st

from gameMechanic.game_state import (
    PHASES,
    faction_dir_for,
    is_necron_faction,
    unit_id_from_state_key,
    units_key_for,
    units_list_for,
)
from gameMechanic.unit_mutations import adjust_cp
from gameObjects.loader import load_command_protocols, load_stratagems
from gameObjects.stratagem import stratagem_visibility

_LOG_PATH = Path(__file__).parent.parent.parent / "data" / "log" / "game_log.json"


def _load_game_log() -> list[dict]:  # type: ignore[type-arg]
    if not _LOG_PATH.exists():
        return []
    with _LOG_PATH.open() as f:
        return json.load(f)


def _unit_name_map(faction: str) -> dict[str, str]:
    """Return uid → name_en mapping for a faction."""
    return {u.id: u.name_en for u in units_list_for(faction)}


def _state_for(faction: str) -> dict:  # type: ignore[type-arg]
    return st.session_state[units_key_for(faction)]


def _render_necron_protocols() -> None:
    protocols = load_command_protocols("necrons")
    if not protocols:
        return

    active_id = st.session_state.get("active_protocol_id")
    used_ids = st.session_state.get("used_protocol_ids", [])

    st.caption("**Necron Command Protocols**")
    for p in protocols:
        if p.id == active_id:
            st.markdown(f"**{p.name_en}** — active")
            st.caption(f"  Directive 1: {p.primary}")
            st.caption(f"  Directive 2: {p.secondary}")
        elif p.id in used_ids:
            st.markdown(f"~~{p.name_en}~~ — used")
        else:
            st.caption(f"{p.name_en} — available")
    st.divider()


def _render_command_protocol() -> None:
    first = st.session_state.get("first_player", "Necrons")
    second = st.session_state.get("second_player", "Orks")

    if is_necron_faction(first) or is_necron_faction(second):
        _render_necron_protocols()

    st.caption(
        f"**Round** {st.session_state.get('round', 1)}  ·  "
        f"**Phase** {PHASES[st.session_state.get('phase_idx', 0)][0]}"
    )
    st.caption(f"**Active player:** {st.session_state.get('active', first)}")
    st.divider()

    entries = _load_game_log()
    if entries:
        st.caption("**Battle Log**")
        key_fn = lambda e: (e["round"], e["phase"])  # noqa: E731
        for (round_num, phase), items in groupby(sorted(entries, key=key_fn), key=key_fn):
            with st.expander(f"R{round_num} · {phase.capitalize()}", expanded=False):
                for item in items:
                    st.caption(f"**{item['unit']}**: {item['action']}")
        st.divider()

    st.caption("**Deployment Snapshot**")
    for faction in (first, second):
        st.caption(f"**{faction}**")
        names = _unit_name_map(faction)
        states = _state_for(faction)
        for uid, name in names.items():
            s = states.get(uid, {})
            deployment = s.get("deployment", "—")
            status = "DESTROYED" if s.get("destroyed") else deployment
            st.caption(f"  {name}: {status}")


def _conditions_met(conditions: list[str], faction: str, unit=None) -> bool:
    """Return True if conditions are satisfied.

    If unit is provided (selected unit), check only that unit.
    Otherwise check all units in the faction (army-wide fallback).
    """
    if not conditions:
        return True
    if unit is not None:
        return all(unit.has_keyword(kw) for kw in conditions)
    for u in units_list_for(faction):
        if all(u.has_keyword(kw) for kw in conditions):
            return True
    return False


def _render_stratagems() -> None:
    active_faction = st.session_state.get("active", "—")
    first = st.session_state.get("first_player", "")
    second = st.session_state.get("second_player", "")
    inactive_faction = second if active_faction == first else first

    cp = st.session_state.get("cp", {})
    cp_active = cp.get(active_faction, 0)
    cp_inactive = cp.get(inactive_faction, 0)
    phase_idx = st.session_state.get("phase_idx", 0)
    current_phase = PHASES[phase_idx][1]
    current_stage = st.session_state.get("phase_stage", "active")
    used_ids: set[str] = st.session_state.get("used_stratagem_ids", set())

    st.caption(f"**{active_faction}** (active) · CP: **{cp_active}**")
    st.caption(f"**{inactive_faction}** (inactive) · CP: **{cp_inactive}**")
    st.divider()

    faction_dir = faction_dir_for(active_faction)
    try:
        stratagems = load_stratagems(faction_dir)
    except Exception:
        st.warning("Could not load stratagems.")
        return

    # Resolve selected unit for unit-level condition check
    sel = st.session_state.get("selected_unit")
    sel_faction_unit: tuple[str, object] | None = None
    if sel is not None:
        sel_faction, sel_state_key = sel
        real_uid = unit_id_from_state_key(sel_state_key)
        for u in units_list_for(sel_faction):
            if u.id == real_uid:
                sel_faction_unit = (sel_faction, u)
                break

    visible = []
    for s in stratagems:
        spending_faction = inactive_faction if s.player == "inactive" else active_faction
        cp_for_strat = cp_inactive if s.player == "inactive" else cp_active

        unit_for_check = None
        if sel_faction_unit is not None and sel_faction_unit[0] == spending_faction:
            unit_for_check = sel_faction_unit[1]
        met = _conditions_met(s.conditions, spending_faction, unit_for_check)

        vis = stratagem_visibility(s, cp_for_strat, current_phase, current_stage, used_ids, met)
        if vis != "hidden":
            visible.append((s, vis, spending_faction))

    if not visible:
        st.caption(f"No stratagems available in the **{current_phase.capitalize()}** phase.")
        return

    for strat, vis, spending_faction in visible:
        disabled = vis == "greyed"
        label = f"**{strat.name_en}** · {strat.cp_cost} CP"
        if strat.player == "inactive":
            label += f" *({inactive_faction})*"
        if vis == "greyed":
            if strat.id in used_ids:
                label += " *(used)*"
            else:
                label += " *(CP insufficient)*"

        with st.expander(label, expanded=False):
            st.caption(strat.rule_text)
            if not disabled:
                if st.button(
                    f"Use — spend {strat.cp_cost} CP",
                    key=f"strat_{strat.id}_{phase_idx}",
                ):
                    adjust_cp(spending_faction, -strat.cp_cost)
                    used_ids.add(strat.id)
                    st.session_state.used_stratagem_ids = used_ids
                    st.rerun()


def render_game_protocoll() -> None:
    tab_protocol, tab_stratagems = st.tabs(["📋 Command Protocol", "⚔️ Stratagems"])
    with tab_protocol:
        _render_command_protocol()
    with tab_stratagems:
        _render_stratagems()
