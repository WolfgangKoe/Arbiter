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
    unit_id_from_state_key,
    units_key_for,
    units_list_for,
)
from gameMechanic.unit_mutations import adjust_cp
from gameObjects.loader import load_stratagems
from gameObjects.stratagem import stratagem_visibility

_LOG_PATH = Path(__file__).parent.parent.parent / "data" / "log" / "game_log.json"


def _load_game_log() -> list[dict]:  # type: ignore[type-arg]
    """Load log entries as a flat list compatible with the battle-log renderer.

    Converts the nested {rounds → phases → events} format from game_log.py
    into flat dicts: {round, phase, unit, action}.
    """
    if not _LOG_PATH.exists():
        return []
    with _LOG_PATH.open() as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            return []
    if not isinstance(data, dict):
        return []
    entries = []
    for r in data.get("rounds", []):
        round_num = r.get("round", 0)
        for phase_entry in r.get("phases", []):
            phase = phase_entry.get("phase", "")
            for event in phase_entry.get("events", []):
                entries.append(
                    {
                        "round": round_num,
                        "phase": phase,
                        "unit": event.get("unit", ""),
                        "action": event.get("action", ""),
                    }
                )
    return entries


def _unit_name_map(faction: str) -> dict[str, str]:
    """Return uid → name_en mapping for a faction."""
    return {u.id: u.name_en for u in units_list_for(faction)}


def _state_for(faction: str) -> dict:  # type: ignore[type-arg]
    return st.session_state[units_key_for(faction)]


def _render_command_protocol() -> None:
    first = st.session_state.get("first_player", "Necrons")
    second = st.session_state.get("second_player", "Orks")

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


def _conditions_met(conditions: list[str], unit=None) -> bool:
    """Return True if conditions are satisfied.

    Requires an explicit unit — no army-wide fallback, as that would show
    unit-specific stratagems even when nothing relevant is selected.
    """
    if not conditions:
        return True
    if unit is None:
        return False
    return all(unit.has_keyword(kw) for kw in conditions)


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

    try:
        stratagems_active = load_stratagems(faction_dir_for(active_faction))
        stratagems_inactive = (
            load_stratagems(faction_dir_for(inactive_faction)) if inactive_faction else []
        )
    except Exception:
        st.warning("Could not load stratagems.")
        return
    stratagems = stratagems_active + stratagems_inactive

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
        met = _conditions_met(s.conditions, unit_for_check)

        vis = stratagem_visibility(s, cp_for_strat, current_phase, current_stage, used_ids, met)
        if vis != "hidden":
            visible.append((s, vis, spending_faction))

    if not visible:
        st.caption(f"No stratagems available in the **{current_phase.capitalize()}** phase.")
        return

    for i, (strat, vis, spending_faction) in enumerate(visible):
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
            if strat.id in used_ids:
                if st.button(
                    f"↺ Rückgängig (+{strat.cp_cost} CP)",
                    key=f"strat_undo_{strat.id}_{phase_idx}_{i}",
                ):
                    adjust_cp(spending_faction, strat.cp_cost)
                    used_ids.discard(strat.id)
                    st.session_state.used_stratagem_ids = used_ids
                    st.session_state.active_modifiers = [
                        m
                        for m in st.session_state.get("active_modifiers", [])
                        if m.get("source") != strat.name_en
                    ]
                    st.rerun()
            elif not disabled:
                if st.button(
                    f"Use — spend {strat.cp_cost} CP",
                    key=f"strat_{strat.id}_{phase_idx}_{i}",
                ):
                    adjust_cp(spending_faction, -strat.cp_cost)
                    used_ids.add(strat.id)
                    st.session_state.used_stratagem_ids = used_ids
                    if strat.modifier is not None:
                        m = strat.modifier
                        active_mods = st.session_state.get("active_modifiers", [])
                        active_mods.append(
                            {
                                "unit_key": None,
                                "source": strat.name_en,
                                "effect": {
                                    "roll_type": m.roll_type,
                                    "value": m.value,
                                    "target": m.target,
                                    "phase": m.phase or current_phase,
                                },
                                "expires_at_phase": (
                                    current_phase if m.expires_at == "phase_end" else None
                                ),
                                "expires_at_round": (
                                    None
                                    if m.expires_at != "turn_end"
                                    else st.session_state.get("round", 1)
                                ),
                            }
                        )
                        st.session_state.active_modifiers = active_mods
                    st.rerun()


def render_game_protocoll() -> None:
    tab_stratagems, tab_protocol = st.tabs(["⚔️ Stratagems", "📋 Command Protocol"])
    with tab_stratagems:
        _render_stratagems()
    with tab_protocol:
        _render_command_protocol()
