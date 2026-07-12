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
from collections.abc import Callable
from itertools import groupby
from pathlib import Path

import streamlit as st

from constants.symbols import SYM_SWORDS
from gameMechanic.gameState import (
    PHASES,
    faction_dir_for,
    unit_id_from_state_key,
    units_key_for,
    units_list_for,
)
from gameMechanic.stratagemEngine import _effect_gate_met
from gameObjects.loader import load_stratagems
from gameObjects.stratagem import (
    Stratagem,
    is_core_stratagem,
    stratagem_conditions_met,
    stratagem_undo_visible,
    stratagem_usable_by_player,
    stratagem_visibility,
)
from uiLayout._common import (
    render_go_card,
    spend_stratagem,
    stratagem_used_elsewhere_unit_name,
    stratagem_used_here,
    undo_stratagem,
)
from uiLayout.goCard import GoCardState

_LOG_PATH = Path(__file__).parent.parent.parent / "data" / "log" / "game_log.json"

# This render spot's own stable anchor (S139 B12b, design_system.md §6.1) — the
# central Stratagems list is a single render location per (player, GO), unlike
# the reactive boxes/Advance-reroll card which render once per unit/occurrence,
# so one constant suffices (storage is already scoped per (faction, GO id) —
# see `spend_stratagem`'s `anchor_id` docstring).
_CENTRAL_LIST_ANCHOR_ID = "central_list"


def _load_game_log() -> list[dict]:  # type: ignore[type-arg]
    """Load log entries as a flat list compatible with the battle-log renderer.

    Converts the nested {rounds → phases → events} format from gameLog.py
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
        for uid, s in states.items():
            name = names.get(unit_id_from_state_key(uid), uid)
            deployment = s.get("deployment", "—")
            status = "DESTROYED" if s.get("destroyed") else deployment
            st.caption(f"  {name}: {status}")


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


# _effect_gate_met moved to gameMechanic.stratagemEngine (S142 Aufgabe 1, Option
# B — consolidated stratagem-effect dispatch); imported below.


def _selected_state_key_for(player: str) -> str | None:
    """Return the raw state key (uid) of the unit selected by `player`, else None.

    Same (faction, state_key) tuple _selected_unit_for reads, but returns the state
    key itself instead of the resolved Unit object — this is the format attack-
    resolution entries use for atk_uid, so a stratagem modifier can be scoped to
    exactly the unit that was selected when the stratagem was activated.
    """
    sel = st.session_state.get("selected_unit")
    if sel is None:
        return None
    sel_faction, sel_state_key = sel
    if sel_faction != player:
        return None
    return sel_state_key


def _selected_unit_state_for(player: str) -> dict | None:  # type: ignore[type-arg]
    """Return the raw unit_state dict for the unit selected by `player`, else None.

    Companion to `_selected_state_key_for` — `_effect_gate_met` needs the state
    dict itself (movement_chosen/in_melee), not just the key.
    """
    state_key = _selected_state_key_for(player)
    if state_key is None:
        return None
    unit_state: dict | None = st.session_state.get(units_key_for(player), {}).get(  # type: ignore[type-arg]
        state_key
    )
    return unit_state


def _go_state_and_reason(
    strat: Stratagem,
    vis: str,
    used_ids: set[str],
    used_battle_ids: set[str],
    used_here: bool,
    used_elsewhere_unit: str | None = None,
) -> tuple[GoCardState, str | None]:
    """Map (`stratagem_visibility`, undo window) to a GO-card state + locked reason.

    Central-list-specific (design_system.md §6, S132 1b): `stratagem_visibility()`
    only ever returns "clickable"/"greyed" here — `conditions_met=False` already
    filtered the stratagem out as "hidden" before this runs, so "dormant" never
    appears in the central list (only 1a's isolated card demo shows that state).
    "greyed" splits into two GO states depending on whether THIS phase's
    activation window is still open (`stratagem_undo_visible`): open →
    "used" (Undo offered) if `used_here` — this render spot's own anchor
    (`_CENTRAL_LIST_ANCHOR_ID`) is the one recorded for this (player, GO) this
    phase — else "used_elsewhere" (disabled "Used", no Undo; S139 B12b,
    design_system.md §6.1 5th state); closed → "locked" (reason "used" for a
    once_per_battle stratagem spent in an earlier phase, else "CP
    insufficient"). `used_here` is computed by the caller via
    `stratagem_used_here` so this stays a pure, Streamlit-free decision
    function, mirroring `_reactive_go_state`/`_advance_reroll_state`.
    `used_elsewhere_unit` — the display name of the unit the GO was used on
    (caller resolves it via `stratagem_used_elsewhere_unit_name`, None when no
    unit is known); returned as the "used_elsewhere" reason so the card can
    show the §6.1 suffix "used on ⟨Einheit⟩" (S141 B12b).
    """
    if vis == "clickable":
        return "ready", None
    if stratagem_undo_visible(strat.id, used_ids, used_battle_ids):
        return ("used", None) if used_here else ("used_elsewhere", used_elsewhere_unit)
    reason = "used" if strat.id in used_battle_ids else "CP insufficient"
    return "locked", reason


def _use_callback(strat: Stratagem, player: str) -> Callable[[], None]:
    """Factory for the GO card's on_use callback.

    A dedicated factory function (rather than a lambda inline in the loop
    body) so each call gets its own closure over `strat`/`player` — a bare
    `lambda: spend_stratagem(strat, ...)` written directly in the loop would
    capture the loop variable *by reference*, so every card's callback would
    resolve to the LAST stratagem once actually invoked. A `lambda strat=strat:`
    default-arg workaround avoids that but defeats mypy's type inference for
    the lambda in strict mode — this factory gets both right.

    Guards against `unit_key is None` for a unit-scoped effect (S142 Aufgabe 2,
    Befund 5): `_effect_gate_met` should already keep such a card off "ready"
    until a unit is selected, but this is the last line of defence at the
    actual spend site — without it, a click here would still deduct CP and
    mark the GO used via `spend_stratagem` while `unit_key is None` silently
    skips `_apply_stratagem_effect`, spending the Stratagem for no game effect.
    """

    def _use() -> None:
        unit_key = _selected_state_key_for(player)
        if strat.effect is not None and unit_key is None:
            return
        spend_stratagem(strat, player, unit_key, anchor_id=_CENTRAL_LIST_ANCHOR_ID)

    return _use


def _undo_callback(strat: Stratagem, player: str) -> Callable[[], None]:
    """Factory for the GO card's on_undo callback (see `_use_callback`)."""
    return lambda: undo_stratagem(strat, player)


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
    unit_state_for_check = _selected_unit_state_for(player)

    visible = []
    for s in stratagems:
        if s.timing == "phase_reactive":
            # Static §6.2 model (S134 stakeholder decision): a reactive GO
            # renders ONLY at its inline trigger anchor, never in this central
            # list — even while its anchor is still missing (Paket-4 debt,
            # design_system.md §6.2). Generic YAML-field check, no id/name
            # strings (INV-4b). `stratagem_visibility()` would also hide these
            # (reactive_trigger_active defaults False); this explicit skip
            # makes the list's contract independent of that default.
            continue
        if not stratagem_usable_by_player(s.player, is_active):
            continue
        met = stratagem_conditions_met(s.conditions, unit_for_check)
        vis = stratagem_visibility(
            s, cp.get(player, 0), current_phase, used_ids, met, used_battle_ids
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
        used_here = stratagem_used_here(player, strat.id, _CENTRAL_LIST_ANCHOR_ID)
        state, locked_reason = _go_state_and_reason(
            strat,
            vis,
            used_ids,
            used_battle_ids,
            used_here,
            stratagem_used_elsewhere_unit_name(player, strat.id),
        )
        if state == "ready":
            # Keyword conditions (stratagem_conditions_met) already passed above — this
            # is the per-unit-state gate (S133-D Befund 4) keywords cannot
            # express: only overrides an otherwise-ready card, never a card
            # already "used"/"locked" for another reason.
            gate_met, gate_reason = _effect_gate_met(strat, unit_state_for_check)
            if not gate_met:
                state, locked_reason = "locked", gate_reason
        target_name = (
            unit_for_check.name_en if strat.effect is not None and unit_for_check else None
        )
        render_go_card(
            key=f"{player}_{strat.id}_{phase_idx}_{i}",
            name=strat.name_en,
            cp_cost=strat.cp_cost,
            state=state,
            keywords=strat.conditions,
            rule_text=strat.rule_text,
            locked_reason=locked_reason,
            target_name=target_name,
            on_use=_use_callback(strat, player),
            on_undo=_undo_callback(strat, player),
        )


def render_game_protocoll() -> None:
    tab_stratagems, tab_log = st.tabs([f"{SYM_SWORDS} Stratagems", "📋 Battle Log"])
    with tab_stratagems:
        _render_stratagems()
    with tab_log:
        _render_battle_log()
