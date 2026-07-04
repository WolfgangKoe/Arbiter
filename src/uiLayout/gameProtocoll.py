"""gameProtocoll — Battle Log + Stratagems tab.

Two tabs in the center column below the gameActionDisplayArea:
  - Battle Log:  round/phase log navigator (setup summary for now)
  - Stratagems:  GO list with visibility logic (data structure ready; Ziel 4)

GO visibility states (see docs/spec/processes.md P-06 and gameObjects/stratagem.py):
  clickable  — conditions met, CP available, not yet used this phase
  greyed     — conditions met, but CP insufficient OR already used this phase
  hidden     — conditions not met → not rendered at all
"""

import json
from itertools import groupby
from pathlib import Path

import streamlit as st

from constants.symbols import SYM_RESET, SYM_SWORDS
from gameMechanic.game_state import (
    PHASES,
    faction_dir_for,
    unit_id_from_state_key,
    units_key_for,
    units_list_for,
)
from gameMechanic.unit_mutations import adjust_cp
from gameObjects.loader import load_stratagems
from gameObjects.stratagem import (
    is_core_stratagem,
    stratagem_undo_visible,
    stratagem_usable_by_player,
    stratagem_visibility,
)

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


def _render_battle_log() -> None:
    first = st.session_state.get("first_player", "Player 1")
    second = st.session_state.get("second_player", "Player 2")

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


def _selected_unit_for(player: str):
    """Return the selected unit object if it belongs to `player`, else None."""
    sel = st.session_state.get("selected_unit")
    if sel is None:
        return None
    sel_faction, sel_state_key = sel
    if sel_faction != player:
        return None
    real_uid = unit_id_from_state_key(sel_state_key)
    for u in units_list_for(player):
        if u.id == real_uid:
            return u
    return None


def _render_stratagems() -> None:
    """Two fixed player columns: first_player left, second_player right.

    Layout is bound to first_player/second_player (domain constraint), never
    to `active` — only the usable-filter inside each column depends on whose
    turn it is.
    """
    active_faction = st.session_state.get("active", "—")
    first = st.session_state.get("first_player", "")
    second = st.session_state.get("second_player", "")

    left, right = st.columns(2)
    for player, col in ((first, left), (second, right)):
        with col:
            _render_stratagem_column(player, player == active_faction)


def _render_stratagem_column(player: str, is_active: bool) -> None:
    """Render one player's stratagem list; `player` IS the spending faction."""
    cp = st.session_state.get("cp", {})
    phase_idx = st.session_state.get("phase_idx", 0)
    current_phase = PHASES[phase_idx][1]
    current_stage = st.session_state.get("phase_stage", "active")
    used_ids_by_player: dict[str, set[str]] = st.session_state.get("used_stratagem_ids", {})
    used_ids = used_ids_by_player.get(player, set())
    used_battle_ids_by_faction: dict[str, set[str]] = st.session_state.get(
        "used_stratagem_battle_ids", {}
    )
    used_battle_ids = used_battle_ids_by_faction.get(player, set())

    role = "active" if is_active else "inactive"
    st.caption(f"**{player}** ({role}) · CP: **{cp.get(player, 0)}**")
    st.divider()

    try:
        stratagems = load_stratagems(faction_dir_for(player))
    except Exception:
        st.warning("Could not load stratagems.")
        return

    unit_for_check = _selected_unit_for(player)

    visible = []
    for s in stratagems:
        if not stratagem_usable_by_player(s.player, is_active):
            continue
        met = _conditions_met(s.conditions, unit_for_check)
        vis = stratagem_visibility(
            s, cp.get(player, 0), current_phase, current_stage, used_ids, met, used_battle_ids
        )
        if vis != "hidden":
            visible.append((s, vis))

    if not visible:
        st.caption(f"No stratagems available in the **{current_phase.capitalize()}** phase.")
        return

    # Section headers (design option 1): core/shared first, then faction-specific.
    visible.sort(key=lambda entry: not is_core_stratagem(entry[0].id))
    in_core_section: bool | None = None
    for i, (strat, vis) in enumerate(visible):
        is_core = is_core_stratagem(strat.id)
        if is_core != in_core_section:
            st.caption("**Core**" if is_core else f"**{player}**")
            in_core_section = is_core
        disabled = vis == "greyed"
        is_used = strat.id in used_ids or strat.id in used_battle_ids
        undo_visible = stratagem_undo_visible(strat.id, used_ids, used_battle_ids)
        label = f"**{strat.name_en}** · {strat.cp_cost} CP"
        if vis == "greyed":
            if is_used:
                label += " *(used)*"
            else:
                label += " *(CP insufficient)*"

        with st.expander(label, expanded=False):
            st.caption(strat.rule_text)
            if undo_visible:
                if st.button(
                    f"{SYM_RESET} Rückgängig (+{strat.cp_cost} CP)",
                    key=f"strat_undo_{player}_{strat.id}_{phase_idx}_{i}",
                ):
                    adjust_cp(player, strat.cp_cost)
                    used_ids.discard(strat.id)
                    used_ids_by_player[player] = used_ids
                    st.session_state.used_stratagem_ids = used_ids_by_player
                    if strat.once_per_battle:
                        used_battle_ids.discard(strat.id)
                        used_battle_ids_by_faction[player] = used_battle_ids
                        st.session_state.used_stratagem_battle_ids = used_battle_ids_by_faction
                    st.session_state.active_modifiers = [
                        m
                        for m in st.session_state.get("active_modifiers", [])
                        if m.get("source") != strat.name_en
                    ]
                    st.rerun()
            elif not disabled:
                if st.button(
                    f"Use — spend {strat.cp_cost} CP",
                    key=f"strat_{player}_{strat.id}_{phase_idx}_{i}",
                ):
                    adjust_cp(player, -strat.cp_cost)
                    used_ids.add(strat.id)
                    used_ids_by_player[player] = used_ids
                    st.session_state.used_stratagem_ids = used_ids_by_player
                    if strat.once_per_battle:
                        used_battle_ids.add(strat.id)
                        used_battle_ids_by_faction[player] = used_battle_ids
                        st.session_state.used_stratagem_battle_ids = used_battle_ids_by_faction
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
    tab_stratagems, tab_log = st.tabs([f"{SYM_SWORDS} Stratagems", "📋 Battle Log"])
    with tab_stratagems:
        _render_stratagems()
    with tab_log:
        _render_battle_log()
