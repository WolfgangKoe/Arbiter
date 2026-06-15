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

import streamlit as st

from gameMechanic.game_log import log_action
from gameMechanic.game_state import PHASES, active_protocol_buff_labels, units_key_for
from gameMechanic.unit_mutations import set_deployment
from gameObjects.unit import Unit
from uiLayout._common import (
    front_group_hp,
    group_target_selectable,
    is_group_target,
    reset_group_declaration_state,
    toggle_group_target,
)

# design_colors.md §0: MOVED = blau (vormals Buff-Blau), Buff = grün (vormals
# MOVED-Grün), RESERVE = HEROIC-INT.-Farbe (temporäre Sonderzustände).
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
    "RESERVE": ("#ff9060", "#2a1208"),
    "DESTROYED": ("#c04040", "#1e1010"),
    "HEROIC INT.": ("#ff9060", "#2a1208"),
}

_BUFF_COLOR: tuple[str, str] = ("#4a9a5a", "#0a1a0a")
_DEBUFF_COLOR: tuple[str, str] = ("#ef4444", "#1e0808")

_TARGET_PHASES: frozenset[str] = frozenset({"shooting", "charge", "fight"})


def _badge(text: str, variant: str = "") -> str:
    if text in _BADGE_COLORS:
        fg, bg = _BADGE_COLORS[text]
    elif variant == "buff":
        fg, bg = _BUFF_COLOR
    elif variant == "debuff":
        fg, bg = _DEBUFF_COLOR
    else:
        fg, bg = ("#c9a84c", "#2e2618")
    return (
        f'<span style="background:{bg};border:1px solid {fg};border-radius:2px;'
        f"padding:1px 6px;font-size:10px;color:{fg};letter-spacing:0.06em;"
        f'font-weight:600;margin-right:3px;">{text}</span>'
    )


_MOVEMENT_BADGE: dict[str, str] = {
    "moved": "MOVED",
    "stationary": "STATIONARY",
    "advanced": "ADVANCED",
    "retreated": "RETREATED",
}


def _state_badges_html(state: dict) -> str:  # type: ignore[type-arg]
    parts: list[str] = []
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
        parts.append(_badge(movement_slot))

    if flags.get("shot"):
        parts.append(_badge("SHOT"))

    if state.get("in_melee") and movement_slot != "CHARGED":
        parts.append(_badge("IN MELEE"))

    if flags.get("heroic_intervened"):
        parts.append(_badge("HEROIC INT."))

    if state.get("in_reserve"):
        parts.append(_badge("RESERVE"))

    for buf in state.get("active_buffs", []):
        parts.append(_badge(buf.get("badge_label", "BUFF"), variant="buff"))

    return "".join(parts)


def _keyword_chip(kw: str, highlighted: bool) -> str:
    # Wargear-granted keywords look like any other keyword (design_colors.md §0):
    # wargear effects show up as buff/debuff badges, not as a colored chip class.
    if highlighted:
        fg, bg, border = "#f5d080", "#3a2e10", "#f5d080"
    else:
        fg, bg, border = "#6b5f44", "#1c1a14", "#2e2618"
    return (
        f'<span style="background:{bg};border:1px solid {border};border-radius:2px;'
        f"padding:1px 5px;font-size:9px;color:{fg};letter-spacing:0.05em;"
        f'margin-right:2px;">{kw}</span>'
    )


def _keywords_html(unit: Unit) -> str:
    """Render keyword chips, excluding the main faction keyword.

    Highlighting is all-or-nothing: if the unit has all highlight_keywords,
    each matching chip is highlighted; otherwise no chip is highlighted.
    """
    required: list[str] = st.session_state.get("highlight_keywords", [])
    visible_kws = [kw for kw in unit.keywords if kw != unit.faction]

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
            label = f"◀ {unit.name_en}" if is_sel else f"▶ {unit.name_en}"
            if st.button(
                label,
                key=f"sel_{faction}_{uid}",
                type="primary" if is_sel else "secondary",
                use_container_width=True,
            ):
                st.session_state.selected_unit = None if is_sel else (faction, uid)
                st.rerun()

        elif is_active:
            cmd_awaiting_id: str | None = (
                st.session_state.get("cmd_awaiting_ability_id") if phase_key == "command" else None
            )
            res_orb_awaiting = phase_key == "command" and st.session_state.get(
                "res_orb_awaiting_target", False
            )

            if cmd_awaiting_id:
                required_kws: list[str] = st.session_state.get("cmd_awaiting_required_kw", [])
                eligible = not required_kws or any(unit.has_keyword(kw) for kw in required_kws)
                if eligible:
                    if st.button(
                        f"▶ {unit.name_en}",
                        key=f"cmd_tgt_{cmd_awaiting_id}_{faction}_{uid}",
                        type="secondary",
                        use_container_width=True,
                    ):
                        badge = (
                            st.session_state.get("cmd_awaiting_badge_label")
                            or cmd_awaiting_id.split(".")[-1]
                        )
                        effect_type = st.session_state.get("cmd_awaiting_effect_type", "")
                        unit_state = st.session_state[units_key_for(faction)][uid]
                        unit_state.setdefault("active_buffs", [])
                        unit_state["active_buffs"].append(
                            {
                                "ability_id": cmd_awaiting_id,
                                "badge_label": badge,
                                "effect_type": effect_type,
                            }
                        )
                        cmd_state: dict = st.session_state.get("command_ability_state", {})
                        entry: dict = cmd_state.get(cmd_awaiting_id) or {}
                        targets: list[str] = list(
                            entry.get("targets")
                            or ([entry["target_uid"]] if entry.get("target_uid") else [])
                        )
                        if uid not in targets:
                            targets.append(uid)
                        cmd_state[cmd_awaiting_id] = {
                            "targets": targets,
                            "active_since_round": entry.get(
                                "active_since_round", st.session_state.round
                            ),
                        }
                        st.session_state.command_ability_state = cmd_state
                        st.session_state.cmd_awaiting_ability_id = None
                        log_action(
                            st.session_state.round,
                            "command",
                            faction,
                            f"{badge} → {unit.name_en}",
                        )
                        st.rerun()
                else:
                    st.markdown(f"**{unit.name_en}**")

            elif res_orb_awaiting:
                if uid == st.session_state.get("wargear_awaiting_bearer_uid"):
                    st.markdown(f"**{unit.name_en}**")
                else:
                    if st.button(
                        f"▷ {unit.name_en}",
                        key=f"res_orb_tgt_{faction}_{uid}",
                        type="secondary",
                        use_container_width=True,
                    ):
                        st.session_state.res_orb_target_uid = uid
                        st.session_state.res_orb_awaiting_target = False
                        st.session_state.wargear_awaiting_bearer_uid = None
                        st.rerun()

            else:
                sel = st.session_state.selected_unit
                is_sel = sel == (faction, uid)
                label = f"◀ {unit.name_en}" if is_sel else f"▶ {unit.name_en}"
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
                label = f"◀ {unit.name_en}" if is_tgt else f"▷ {unit.name_en}"
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
            badges = _state_badges_html(state)
            from gameMechanic.ability_engine import ability_badge_label  # noqa: PLC0415

            ability_lbl = ability_badge_label(faction, unit)
            if ability_lbl:
                badges += _badge(ability_lbl, variant="buff")
            for proto_lbl in active_protocol_buff_labels(faction):
                badges += _badge(proto_lbl, variant="buff")
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
