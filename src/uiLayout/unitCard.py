"""unitCard — Passive display card with single selector button.

Design principles (see docs/spec/ui_layout.md §4):
- ONE button per card: the unit name. Clicking it toggles selection.
  - Own unit  → toggles selected_unit
  - Enemy unit → toggles selected_target (shooting / charge / fight phases only)
- No expander, no stats table, no wound buttons.
  Wound adjustments live in the PlayerArea of gameActionsArea.
- Layout (top to bottom, inside a border):
    LP/model bars → name button → state badges → keywords
- Main faction keyword (unit.faction) is omitted from keyword display;
  it is shown once in the armyCard.
- Keyword highlighting: when session_state.highlight_keywords is set,
  keywords are highlighted all-or-nothing: only if the unit has ALL required
  keywords do the matching chips light up.
- Setup phase exception: deployment selectbox shown inline below name.
- Model-group units: their subUnitCards live in the gameActionsArea player
  areas (render_group_cards in _common.py), not here. The target button (▷)
  assigns targets to the selected model group when the group flow is active.
"""

from collections.abc import Sequence

import streamlit as st

from constants.symbols import SYM_COLLAPSE, SYM_EXPAND, SYM_EXPAND_ALT
from gameMechanic.gameLog import log_action
from gameMechanic.gameState import (
    PHASES,
    TargetSelectionRequest,
    active_round_choice_buff_labels,
    units_key_for,
)
from gameMechanic.unitMutations import apply_buff_to_unit, set_deployment
from gameObjects.unit import Unit
from uiLayout._common import (
    front_group_hp,
    group_target_selectable,
    is_group_target,
    reset_group_declaration_state,
    toggle_group_target,
)
from uiLayout.badges import badge, chip

# design_colors.md §0: MOVED = blau (vormals Buff-Blau), Buff = grün (vormals
# MOVED-Grün), RESERVE = HEROIC-INT.-Farbe (temporäre Sonderzustände). CAST =
# --arb-blue-Familie analog SHOT (S137-Entscheid, design_colors.md §2).
# Keine Fraktions-Badges hier — Army-Abilities zeigt die armyCard (Buff-Grün).
_BADGE_COLORS: dict[str, tuple[str, str]] = {
    "MOVED": ("#60a5fa", "#0a1020"),
    "ADVANCED": ("#d4a017", "#2e2618"),
    "STATIONARY": ("#6b5f44", "#1c1a14"),
    "RETREATED": ("#c04040", "#1e1010"),
    "IN MELEE": ("#e07050", "#2a1810"),
    "CHARGED": ("#b070d8", "#1a0a2a"),
    "FOUGHT": ("#c080e8", "#200a30"),
    "SHOT": ("#40a0b8", "#081418"),
    "CAST": ("#93c5fd", "#1e3a8a"),
    "RESERVE": ("#ff9060", "#2a1208"),
    "DESTROYED": ("#c04040", "#1e1010"),
    "HEROIC INT.": ("#ff9060", "#2a1208"),
}

_BUFF_COLOR: tuple[str, str] = ("#4a9a5a", "#0a1a0a")
_DEBUFF_COLOR: tuple[str, str] = ("#ef4444", "#1e0808")

# Phases in which the inactive player's unit cards act as target selectors.
# "psychic" is required for Smite: without it no enemy card is clickable and
# selected_targets stays empty — the damage button can never appear (S129 fix).
_TARGET_PHASES: frozenset[str] = frozenset({"shooting", "charge", "fight", "psychic"})

# Phases that resolve for BOTH players regardless of whose turn it is — the
# Morale phase alternates between both players (data/wh40k_9e/_shared/
# stratagems.yaml insane_bravery comment; core_rules.txt:2094), so a player's
# own-unit self-select button (needed e.g. to pick the unit an
# `player: both` stratagem like Insane Bravery applies to) must not be gated
# on `is_active` there the way it correctly is in the turn-based phases.
_BOTH_PLAYERS_SELF_SELECT_PHASES: frozenset[str] = frozenset({"morale"})


def _self_select_eligible(phase_key: str, is_active: bool) -> bool:
    """Whether this faction's own-unit cards get the plain self-select button.

    Root cause (Bugfix A, S143): the inactive player's own units fell through
    to the `else` branch below, which only offers a button in `_TARGET_PHASES`
    — the Morale phase is not one of those, so the inactive player's units
    rendered as plain, unclickable text and `selected_unit` could never be set
    for them, permanently locking any unit-scoped effect gate (e.g. Insane
    Bravery's `_effect_gate_met`) at "select an eligible unit".
    """
    return is_active or phase_key in _BOTH_PLAYERS_SELF_SELECT_PHASES


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


_MOVEMENT_BADGE: dict[str, str] = {
    "moved": "MOVED",
    "stationary": "STATIONARY",
    "advanced": "ADVANCED",
    "retreated": "RETREATED",
}


def _state_badges_html(
    state: dict,  # type: ignore[type-arg]
    extra_buff_badges: Sequence[str] = (),
) -> str:
    """Combine the state group with the buff/debuff group.

    ``extra_buff_badges`` lets the caller add pre-rendered buff badges
    (army ability, protocol) to the buff group. The two groups are joined
    with a ``<br>`` only when both are non-empty (S137 decision).
    """
    state_parts: list[str] = []
    flags = state.get("turn_flags", {})
    mc = state.get("movement_choice")

    # Movement slot: FOUGHT > CHARGED > movement_choice (suppressed when in_reserve)
    if flags.get("fought"):
        movement_slot = "FOUGHT"
    elif flags.get("charged"):
        movement_slot = "CHARGED"
    elif mc in _MOVEMENT_BADGE and not state.get("in_reserve"):
        movement_slot = _MOVEMENT_BADGE[mc]
    else:
        movement_slot = None

    if movement_slot:
        state_parts.append(_badge(movement_slot))

    if flags.get("shot"):
        state_parts.append(_badge("SHOT"))

    if flags.get("cast"):
        state_parts.append(_badge("CAST"))

    if state.get("in_melee") and movement_slot != "CHARGED":
        state_parts.append(_badge("IN MELEE"))

    if flags.get("heroic_intervened"):
        state_parts.append(_badge("HEROIC INT."))

    if state.get("in_reserve"):
        state_parts.append(_badge("RESERVE"))

    buff_parts: list[str] = [
        _badge(buf.get("badge_label", "BUFF"), variant="buff")
        for buf in state.get("active_buffs", [])
    ]
    buff_parts.extend(extra_buff_badges)

    state_html = "".join(state_parts)
    buff_html = "".join(buff_parts)

    if state_html and buff_html:
        return state_html + "<br>" + buff_html
    return state_html + buff_html


def _keyword_chip(kw: str, highlighted: bool) -> str:
    # Wargear-granted keywords look like any other keyword (design_colors.md §0):
    # wargear effects show up as buff/debuff badges, not as a colored chip class.
    if highlighted:
        fg, bg, border = "#f5d080", "#3a2e10", "#f5d080"
    else:
        fg, bg, border = "#6b5f44", "#1c1a14", "#2e2618"
    return chip(kw, fg, bg, border)


def _fold_faction_keyword(text: str) -> str:
    """Case- and plural-fold a faction/keyword string for comparison.

    WH40k keyword grammar is not consistent across factions: Necron units
    carry the plural "NECRONS" (matching the faction name "Necrons"), but Ork
    units carry the singular "ORK" against the faction name "Orks" (Wahapedia
    data, verified S138). Stripping a single trailing "S" after upper-casing
    folds both onto the same key without hardcoding either faction's string.
    """
    folded = text.strip().upper()
    return folded[:-1] if folded.endswith("S") else folded


def _keywords_html(unit: Unit) -> str:
    """Render keyword chips, excluding the main faction keyword.

    Highlighting is all-or-nothing: if the unit has all highlight_keywords,
    each matching chip is highlighted; otherwise no chip is highlighted.
    """
    required: list[str] = st.session_state.get("highlight_keywords", [])
    faction_key = _fold_faction_keyword(unit.faction)
    visible_kws = [kw for kw in unit.keywords if _fold_faction_keyword(kw) != faction_key]

    if required:
        unit_kws = set(unit.keywords)
        qualifies = all(r in unit_kws for r in required)
        required_set = set(required) if qualifies else set()
    else:
        required_set = set()

    return "".join(_keyword_chip(kw, kw in required_set) for kw in visible_kws)


def render_unit_card(
    unit: Unit,
    state: dict,  # type: ignore[type-arg]
    faction: str,
    state_key: str | None = None,
) -> None:
    phase_key = PHASES[st.session_state.phase_idx][1]
    active = st.session_state.active
    if phase_key == "fight":
        fight_player = st.session_state.get("fight_current_player", active)
        is_active = faction == fight_player
    else:
        is_active = faction == active
    uid = state_key if state_key is not None else unit.id
    in_reserve = state.get("in_reserve", False)

    with st.container(border=True):
        # ── Destroyed ─────────────────────────────────────────────
        if state["destroyed"]:
            st.markdown(f"~~{unit.name_en}~~  *DESTROYED*")
            return

        # ── LP bar (❤) and model bar (⬡) — top of card ───────────
        cur = state["current_wounds"]
        models_alive = state["models"]

        models_initial = state.get("models_initial", unit.models_max)
        if unit.models_max == 1:
            st.progress(min(1.0, cur / unit.wounds) if unit.wounds > 0 else 0)
            st.caption(f"❤ {cur}/{unit.wounds}")
        elif unit.wounds == 1:
            st.progress(min(1.0, models_alive / models_initial) if models_initial > 0 else 0)
            st.caption(f"⬡ {models_alive}/{models_initial}")
        else:
            # Mixed per-model wounds (e.g. Szarekh 16 + Menhirs 7): the front
            # model belongs to the lowest-priority surviving group, so derive its
            # HP and denominator from that group rather than unit.wounds.
            if state.get("group_wounds"):
                front_wounds, front_max = front_group_hp(unit, state)
            elif models_alive > 0:
                front_wounds, front_max = (
                    cur - (models_alive - 1) * unit.wounds,
                    unit.wounds,
                )
            else:
                front_wounds, front_max = 0, unit.wounds
            st.progress(min(1.0, models_alive / models_initial) if models_initial > 0 else 0)
            st.caption(f"⬡ {models_alive}/{models_initial}")
            st.progress(max(0.0, min(1.0, front_wounds / front_max)) if front_max > 0 else 0)
            st.caption(f"❤ {front_wounds}/{front_max}")

        # ── Name / Selector Button ─────────────────────────────────
        if phase_key == "setup":
            sel = st.session_state.selected_unit
            is_sel = sel == (faction, uid)
            label = f"{SYM_COLLAPSE} {unit.name_en}" if is_sel else f"{SYM_EXPAND} {unit.name_en}"
            if st.button(
                label,
                key=f"sel_{faction}_{uid}",
                type="primary" if is_sel else "secondary",
                use_container_width=True,
            ):
                st.session_state.selected_unit = None if is_sel else (faction, uid)
                st.rerun()

        elif _self_select_eligible(phase_key, is_active):
            _ptr: TargetSelectionRequest | None = (
                st.session_state.get("pending_target_request") if phase_key == "command" else None
            )

            if _ptr is not None:
                # Excluded unit (e.g. bearer) shows as plain text
                if uid == _ptr.exclude_uid:
                    st.markdown(f"**{unit.name_en}**")
                elif _ptr.required_keywords and not all(
                    unit.has_keyword(kw) for kw in _ptr.required_keywords
                ):
                    # Wrong keyword — show as ineligible plain text
                    st.markdown(f"**{unit.name_en}**")
                else:
                    symbol = SYM_EXPAND if _ptr.effect_type else SYM_EXPAND_ALT
                    if st.button(
                        f"{symbol} {unit.name_en}",
                        key=f"tgt_{uid}_{_ptr.ability_id}",
                        type="secondary",
                        use_container_width=True,
                    ):
                        if _ptr.effect_type:
                            # Buff ability → apply buff and update command_ability_state
                            unit_state = st.session_state[units_key_for(faction)][uid]
                            apply_buff_to_unit(
                                unit_state, _ptr.ability_id, _ptr.badge_label, _ptr.effect_type
                            )
                            cmd_state: dict = st.session_state.get("command_ability_state", {})
                            entry: dict = cmd_state.get(_ptr.ability_id) or {}
                            targets: list[str] = list(
                                entry.get("targets")
                                or ([entry["target_uid"]] if entry.get("target_uid") else [])
                            )
                            if uid not in targets:
                                targets.append(uid)
                            cmd_state[_ptr.ability_id] = {
                                "targets": targets,
                                "active_since_round": entry.get(
                                    "active_since_round", st.session_state.round
                                ),
                            }
                            st.session_state.command_ability_state = cmd_state
                            log_action(
                                st.session_state.round,
                                "command",
                                faction,
                                f"{_ptr.badge_label} → {unit.name_en}",
                            )
                        else:
                            # Wargear/revive ability → store target uid per wargear
                            # (keyed by request id so multiple bearers never collide)
                            targets = st.session_state.get("revive_wargear_target_uid") or {}
                            targets[_ptr.ability_id] = uid
                            st.session_state.revive_wargear_target_uid = targets
                        st.session_state.pending_target_request = None
                        st.rerun()

            else:
                sel = st.session_state.selected_unit
                is_sel = sel == (faction, uid)
                label = (
                    f"{SYM_COLLAPSE} {unit.name_en}" if is_sel else f"{SYM_EXPAND} {unit.name_en}"
                )
                if st.button(
                    label,
                    key=f"sel_{faction}_{uid}",
                    type="primary" if is_sel else "secondary",
                    use_container_width=True,
                    disabled=in_reserve,
                ):
                    st.session_state.selected_unit = None if is_sel else (faction, uid)
                    st.session_state.selected_targets = []
                    reset_group_declaration_state()
                    st.rerun()

        else:
            # Inactive player — target selector for relevant phases
            if phase_key in _TARGET_PHASES:
                tgts: list[tuple[str, str]] = st.session_state.selected_targets
                is_tgt = (faction, uid) in tgts or is_group_target(faction, uid)
                label = (
                    f"{SYM_COLLAPSE} {unit.name_en}"
                    if is_tgt
                    else f"{SYM_EXPAND_ALT} {unit.name_en}"
                )
                if st.button(
                    label,
                    key=f"tgt_{faction}_{uid}",
                    type="primary" if is_tgt else "secondary",
                    use_container_width=True,
                    disabled=in_reserve or not group_target_selectable(faction, uid),
                ):
                    # Group flow active → target belongs to the selected model group
                    if not toggle_group_target(faction, uid):
                        new_tgts = list(tgts)
                        if is_tgt:
                            new_tgts.remove((faction, uid))
                        else:
                            new_tgts.append((faction, uid))
                        st.session_state.selected_targets = new_tgts
                    st.rerun()
            else:
                st.markdown(f"**{unit.name_en}**")

        # ── State badges + Keywords ────────────────────────────────
        # Relics show no badge of their own — only their effects (buff/debuff).
        if phase_key != "setup":
            from gameMechanic.abilityEngine import ability_badge_label  # noqa: PLC0415

            extra_buffs: list[str] = []
            ability_lbl = ability_badge_label(faction, unit)
            if ability_lbl:
                extra_buffs.append(_badge(ability_lbl, variant="buff"))
            extra_buffs.extend(
                _badge(proto_lbl, variant="buff")
                for proto_lbl in active_round_choice_buff_labels(faction)
            )
            badges = _state_badges_html(state, extra_buffs)
            kws = _keywords_html(unit)
            if badges and kws:
                st.markdown(badges + "<br>" + kws, unsafe_allow_html=True)
            elif badges or kws:
                st.markdown(badges + kws, unsafe_allow_html=True)
        else:
            kws = _keywords_html(unit)
            if kws:
                st.markdown(kws, unsafe_allow_html=True)

        # ── Setup: deployment selector (inline, no expander) ──────
        if phase_key == "setup":
            opts = ["Normal", "Stationary", "Reserve"]
            current = state.get("deployment", "normal").capitalize()
            idx = opts.index(current) if current in opts else 0
            chosen = st.selectbox(
                "Deployment",
                opts,
                index=idx,
                key=f"deploy_{faction}_{uid}",
                label_visibility="collapsed",
            )
            mapping = {"Normal": "normal", "Stationary": "stationary", "Reserve": "reserve"}
            if mapping[chosen] != state.get("deployment", "normal"):
                set_deployment(uid, faction, mapping[chosen])
                st.rerun()
