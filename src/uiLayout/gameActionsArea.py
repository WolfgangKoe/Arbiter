"""gameActionsArea — Center canvas: dispatches to phase renderers."""

import streamlit as st

from engine import (
    _NECRON_UNITS,
    _ORK_UNITS,
    PHASES,
    log_action,
    set_charged,
    set_deployment,
    set_movement_status,
)
from gameObjects.unit import Unit

_PHASE_RULES: dict[str, str] = {
    "command": (
        "**Command Phase**\n\n"
        "The active player receives **+1 CP** (Battle-forged armies). "
        "Activate abilities and stratagems that trigger in the Command Phase."
    ),
    "movement": (
        "**Movement Phase**\n\n"
        "Select a unit and choose its movement type:\n"
        '- **Normal** — move up to M"\n'
        '- **Advance** — move up to M"+D6", cannot shoot or charge afterwards\n'
        "- **Stationary** — do not move\n"
        '- **Retreat** — only if in melee; move up to M", cannot shoot or charge afterwards'
    ),
    "psychic": (
        "**Psychic Phase**\n\n"
        "PSYKER units attempt to manifest psychic powers. "
        "Roll **2D6** ≥ Warp Charge value to manifest. "
        "Opponent may attempt to deny with their own PSYKER (2D6 > manifesting roll)."
    ),
    "shooting": (
        "**Shooting Phase**\n\n"
        "Select a unit to shoot, then select a target. "
        "Units that Advanced or Retreated cannot shoot. "
        "Units in melee cannot shoot.\n\n"
        "Attack sequence: **Hit** (BS) → **Wound** (S vs T) → **Save** (Sv−AP) → **Damage**"
    ),
    "charge": (
        "**Charge Phase**\n\n"
        'Eligible units (≤ 12" from enemy, did not Advance or Retreat) may declare a charge. '
        "Roll **2D6** — result must be ≥ distance to closest target model. "
        "On success: move into melee range."
    ),
    "fight": (
        "**Fight Phase**\n\n"
        "Starting with the **non-active player**, both sides alternate selecting eligible units. "
        "Units that charged this turn fight **before** other units. "
        'Each unit: **Pile In** (up to 3") → **Melee attacks** → **Consolidate** (up to 3").'
    ),
    "morale": (
        "**Morale Phase**\n\n"
        "Units that suffered model losses this turn must take a morale test: "
        "Roll **D6** + models lost. If result > Leadership: additional models flee (result − Ld).\n\n"
        "Single-model units auto-pass."
    ),
}


def _lookup(faction: str, uid: str) -> tuple[Unit, dict]:  # type: ignore[type-arg]
    units = _NECRON_UNITS if faction == "Necrons" else _ORK_UNITS
    unit = next(u for u in units if u.id == uid)
    key = "necron_units" if faction == "Necrons" else "ork_units"
    return unit, st.session_state[key][uid]


def _state_badges_html(state: dict) -> str:  # type: ignore[type-arg]
    _BADGE_COLORS: dict[str, tuple[str, str]] = {
        "ADVANCED": ("#c9a84c", "#2e2618"),
        "STATIONARY": ("#6b5f44", "#1c1a14"),
        "RETREATED": ("#8b1a1a", "#1e1010"),
        "IN MELEE": ("#cc6644", "#2a1810"),
        "CHARGED": ("#9b59b6", "#1a0a2a"),
        "RESERVE": ("#2a6a8b", "#101820"),
        "DESTROYED": ("#8b1a1a", "#1e1010"),
    }

    def _badge(text: str) -> str:
        fg, bg = _BADGE_COLORS.get(text, ("#c9a84c", "#2e2618"))
        return (
            f'<span style="background:{bg};border:1px solid {fg};border-radius:2px;'
            f"padding:1px 6px;font-size:10px;color:{fg};letter-spacing:0.06em;"
            f'font-weight:600;margin-right:3px;">{text}</span>'
        )

    parts = []
    ms = state.get("movement_status", "stationary")
    if ms == "advanced":
        parts.append(_badge("ADVANCED"))
    elif ms == "stationary":
        parts.append(_badge("STATIONARY"))
    elif ms == "retreated":
        parts.append(_badge("RETREATED"))
    if state.get("charged_this_turn"):
        parts.append(_badge("CHARGED"))
    elif state.get("in_melee"):
        parts.append(_badge("IN MELEE"))
    if state.get("in_reserve"):
        parts.append(_badge("RESERVE"))
    return "".join(parts)


def _wound_thresh(strength: int, toughness: int) -> int:
    if strength >= toughness * 2:
        return 2
    if strength > toughness:
        return 3
    if strength == toughness:
        return 4
    if strength * 2 <= toughness:
        return 6
    return 5


def _central_level1(phase_key: str) -> None:
    rules = _PHASE_RULES.get(phase_key, "")
    st.info(rules)


def _central_command_actions(faction: str, uid: str) -> None:
    unit, state = _lookup(faction, uid)
    st.markdown(f"**{unit.name_en}**")
    badges_html = _state_badges_html(state)
    if badges_html:
        st.markdown(badges_html, unsafe_allow_html=True)
    st.caption("No phase-specific unit actions in the Command Phase.")
    if unit.abilities:
        with st.expander("Abilities", expanded=False):
            st.caption(unit.abilities)


def _central_movement_actions(faction: str, uid: str) -> None:
    unit, state = _lookup(faction, uid)
    ms = state.get("movement_status", "normal")
    in_melee = state.get("in_melee", False)

    st.markdown(f"**{unit.name_en}** — M {unit.move}")
    badges_html = _state_badges_html(state)
    if badges_html:
        st.markdown(badges_html, unsafe_allow_html=True)

    if state.get("in_reserve"):
        if st.session_state.round == 1:
            st.warning("Unit is in Reserve — cannot deploy until Round 2.")
        else:
            st.info("Unit is in Reserve — deploy from the board edge.")
            if st.button(
                "Deploy from Reserve",
                key=f"deploy_reserve_{faction}_{uid}",
                type="primary",
                use_container_width=True,
            ):
                set_deployment(uid, faction, "normal")
                set_movement_status(uid, faction, "normal")
                log_action(
                    st.session_state.round, "movement", unit.name_en, "deployed from reserve"
                )
                st.rerun()
        return

    st.markdown("Set movement status:")
    cols = st.columns(4)
    options = [
        ("Normal", "normal", 'Move up to M"'),
        ("Advance", "advanced", 'M"+D6", no shoot/charge'),
        ("Stationary", "stationary", "Do not move"),
        ("Retreat", "retreated", "Exit melee, no shoot/charge"),
    ]
    for col, (label, value, tip) in zip(cols, options):
        with col:
            disabled = value == "retreated" and not in_melee
            btn_type = "primary" if ms == value else "secondary"
            if st.button(
                label,
                key=f"mv_{faction}_{uid}_{value}",
                type=btn_type,
                disabled=disabled,
                use_container_width=True,
                help=tip,
            ):
                set_movement_status(uid, faction, value)
                log_action(st.session_state.round, "movement", unit.name_en, f"movement: {value}")
                st.rerun()

    if in_melee and ms not in ("retreated", "stationary"):
        st.caption("Unit is in melee — only Stationary or Retreat allowed.")


def _central_shooting_actions(faction: str, uid: str) -> None:
    unit, state = _lookup(faction, uid)
    ms = state.get("movement_status", "normal")

    st.markdown(f"**{unit.name_en}** — Shooting")
    badges_html = _state_badges_html(state)
    if badges_html:
        st.markdown(badges_html, unsafe_allow_html=True)

    if ms == "advanced":
        st.warning("Advanced this turn — cannot shoot.")
        return
    if ms == "retreated":
        st.warning("Retreated this turn — cannot shoot.")
        return
    if state.get("in_melee"):
        st.warning("Bound in melee — cannot shoot.")
        return

    ranged = [w for w in unit.weapons if not w.is_melee]
    if not ranged:
        st.warning("No ranged weapons — no action possible.")
        return

    tgt = st.session_state.selected_target
    if tgt is None:
        st.info("Select a **target** unit from the enemy sidebar (▶ Target).")
        return

    tgt_faction, tgt_uid = tgt
    tgt_unit, tgt_state = _lookup(tgt_faction, tgt_uid)

    st.markdown(f"**Target:** {tgt_unit.name_en}")
    inv_display = f"{tgt_unit.invuln_save}+" if tgt_unit.invuln_save else "—"
    st.markdown(f"T {tgt_unit.toughness} · Sv {tgt_unit.save}+ · ++ {inv_display}")
    st.divider()
    st.markdown("**Attack sequence** (for reference — roll dice on the table):")
    for w in ranged:
        skill = int(unit.bs.rstrip("+"))
        thresh = _wound_thresh(int(w.strength), tgt_unit.toughness)
        eff_save = min(tgt_unit.save + abs(int(w.ap)), tgt_unit.invuln_save or 99)
        save_str = f"{eff_save}+" if eff_save <= 6 else "none"
        st.caption(
            f"**{w.name_en}**: {w.attacks} att · hit on {skill}+ · "
            f"wound on {thresh}+ · save {save_str} · D{w.damage}"
        )
    if st.button("Log Shooting Action", key=f"log_shoot_{faction}_{uid}", use_container_width=True):
        log_action(st.session_state.round, "shooting", unit.name_en, f"shot at {tgt_unit.name_en}")
        st.success("Action logged.")


def _central_charge_actions(faction: str, uid: str) -> None:
    unit, state = _lookup(faction, uid)
    ms = state.get("movement_status", "normal")

    st.markdown(f"**{unit.name_en}** — Charge")
    badges_html = _state_badges_html(state)
    if badges_html:
        st.markdown(badges_html, unsafe_allow_html=True)

    if ms in ("advanced", "retreated"):
        st.warning(f"{ms.capitalize()} this turn — cannot charge.")
        return

    tgt = st.session_state.selected_target
    if tgt is None:
        st.info("Select a **target** to charge from the enemy sidebar (▶ Target).")
        return

    tgt_faction, tgt_uid = tgt
    tgt_unit, _ = _lookup(tgt_faction, tgt_uid)
    st.markdown(f"**Target:** {tgt_unit.name_en}")
    st.caption("Roll **2D6** — must equal or beat the distance to the target.")

    c1, c2 = st.columns(2)
    with c1:
        if st.button(
            "Charge Successful",
            key=f"charge_ok_{faction}_{uid}",
            type="primary",
            use_container_width=True,
        ):
            set_charged(uid, faction, tgt_uid, tgt_faction)
            log_action(
                st.session_state.round,
                "charge",
                unit.name_en,
                f"charged {tgt_unit.name_en} — success",
            )
            st.session_state.selected_target = None
            st.rerun()
    with c2:
        if st.button("Charge Failed", key=f"charge_fail_{faction}_{uid}", use_container_width=True):
            log_action(
                st.session_state.round,
                "charge",
                unit.name_en,
                f"charged {tgt_unit.name_en} — failed",
            )
            st.info("Charge failed — no movement.")


def _central_fight_actions(faction: str, uid: str) -> None:
    unit, state = _lookup(faction, uid)
    in_melee = state.get("in_melee", False)

    st.markdown(f"**{unit.name_en}** — Fight")
    if state.get("charged_this_turn"):
        st.markdown("**Fights first** (charged this turn).")
    badges_html = _state_badges_html(state)
    if badges_html:
        st.markdown(badges_html, unsafe_allow_html=True)

    if not in_melee:
        st.warning("Not in melee — no action possible.")
        return

    tgt = st.session_state.selected_target
    if tgt is None:
        st.info("Select a **target** in melee from the enemy sidebar (▶ Target).")
        return

    tgt_faction, tgt_uid = tgt
    tgt_unit, tgt_state = _lookup(tgt_faction, tgt_uid)
    st.markdown(f"**Target:** {tgt_unit.name_en}")
    inv_display = f"{tgt_unit.invuln_save}+" if tgt_unit.invuln_save else "—"
    st.markdown(f"T {tgt_unit.toughness} · Sv {tgt_unit.save}+ · ++ {inv_display}")
    st.divider()
    melee = [w for w in unit.weapons if w.is_melee]
    for w in melee:
        skill = int(unit.ws.rstrip("+"))
        thresh = _wound_thresh(int(w.strength), tgt_unit.toughness)
        eff_save = min(tgt_unit.save + abs(int(w.ap)), tgt_unit.invuln_save or 99)
        save_str = f"{eff_save}+" if eff_save <= 6 else "none"
        st.caption(
            f"**{w.name_en}**: {w.attacks} att · WS{skill}+ · "
            f"wound {thresh}+ · save {save_str} · D{w.damage}"
        )
    if st.button("Log Fight Action", key=f"log_fight_{faction}_{uid}", use_container_width=True):
        log_action(st.session_state.round, "fight", unit.name_en, f"fought {tgt_unit.name_en}")
        st.success("Action logged.")


def _central_morale_info(faction: str, uid: str) -> None:
    unit, state = _lookup(faction, uid)
    lost = state.get("lost_models_this_turn", 0)

    st.markdown(f"**{unit.name_en}**")
    if unit.models_max == 1:
        st.success("Single model — auto-pass.")
        return
    if lost == 0:
        st.success("No losses this turn — no morale test.")
        return
    st.warning(
        f"**Ld {unit.leadership}** | Lost **{lost}** model(s) this turn.\n\n"
        f"Roll D6 + {lost}. If result > {unit.leadership}: remove (result − {unit.leadership}) additional model(s)."
    )


def phase_setup() -> None:
    st.markdown("### Setup")
    st.info(
        "Configure your armies before the battle begins.\n\n"
        "1. **Select first player** — the active player takes their turn first each battle round.\n"
        "2. **Set deployment** for each unit using the dropdowns in the unit cards:\n"
        "   - **Normal** — deployed on the battlefield\n"
        "   - **Stationary** — deployed but will not move in turn 1\n"
        "   - **Reserve** — arrives from turn 2 onwards\n\n"
        "When ready, click **→** to begin Battle Round 1."
    )

    st.markdown("---")
    st.markdown("**First Player**")
    active = st.session_state.active
    c1, c2 = st.columns(2)
    with c1:
        nc_type = "primary" if active == "Necrons" else "secondary"
        if st.button(
            "Necrons go first", key="setup_first_necrons", type=nc_type, use_container_width=True
        ):
            st.session_state.active = "Necrons"
            st.session_state.first_player = "Necrons"
            st.session_state.second_player = "Orks"
            st.rerun()
    with c2:
        ok_type = "primary" if active == "Orks" else "secondary"
        if st.button(
            "Orks go first", key="setup_first_orks", type=ok_type, use_container_width=True
        ):
            st.session_state.active = "Orks"
            st.session_state.first_player = "Orks"
            st.session_state.second_player = "Necrons"
            st.rerun()
    st.caption(f"Currently selected: **{active}** go first.")


def phase_command() -> None:
    from gameMechanic.commandPhase import render_actions_command  # noqa: PLC0415

    sel = st.session_state.selected_unit
    if sel is not None:
        _central_command_actions(*sel)
    else:
        _central_level1("command")
    render_actions_command(st.session_state)


def phase_movement() -> None:
    sel = st.session_state.selected_unit
    if sel is None:
        _central_level1("movement")
    else:
        _central_movement_actions(*sel)


def phase_psychic() -> None:
    sel = st.session_state.selected_unit
    if sel is None:
        _central_level1("psychic")
    else:
        faction, uid = sel
        unit, state = _lookup(faction, uid)
        is_psyker = any(kw.upper() == "PSYKER" for kw in unit.keywords)
        st.markdown(f"**{unit.name_en}**")
        if is_psyker:
            st.info(
                "PSYKER — declare Smite or psychic powers manually. Track results on the unit card."
            )
        else:
            st.warning("Not a PSYKER — no action possible.")


def phase_shooting() -> None:
    sel = st.session_state.selected_unit
    if sel is None:
        _central_level1("shooting")
    else:
        _central_shooting_actions(*sel)


def phase_charge() -> None:
    sel = st.session_state.selected_unit
    if sel is None:
        _central_level1("charge")
    else:
        _central_charge_actions(*sel)


def phase_fight() -> None:
    sel = st.session_state.selected_unit
    if sel is None:
        _central_level1("fight")
        active = st.session_state.active
        inactive = "Orks" if active == "Necrons" else "Necrons"
        st.caption(
            f"Fight order: **{inactive}** selects first (non-active player), "
            f"then **{active}**. Units that charged fight before others."
        )
    else:
        _central_fight_actions(*sel)


def phase_morale() -> None:
    sel = st.session_state.selected_unit
    if sel is None:
        _central_level1("morale")
    else:
        _central_morale_info(*sel)


PHASE_RENDERERS: dict[str, object] = {
    "setup": phase_setup,
    "command": phase_command,
    "movement": phase_movement,
    "psychic": phase_psychic,
    "shooting": phase_shooting,
    "charge": phase_charge,
    "fight": phase_fight,
    "morale": phase_morale,
}


def render_game_actions_area() -> None:
    phase_key = PHASES[st.session_state.phase_idx][1]
    PHASE_RENDERERS[phase_key]()  # type: ignore[operator]
