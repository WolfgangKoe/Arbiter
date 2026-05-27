"""gameActionsArea — Center column layout with three sections.

Internal layout (see docs/ui_layout.md §7):

  ┌────────────────────────────────────────────────────────┐
  │  firstPlayerArea (50%)  │  secondPlayerArea (50%)       │
  ├────────────────────────────────────────────────────────┤
  │              gameActionDisplayArea (full width)         │
  ├────────────────────────────────────────────────────────┤
  │   gameProtocoll tabs  [CommandProtocol | Stratagems]    │
  └────────────────────────────────────────────────────────┘

PlayerAreas:
  - Main interaction surface for each player.
  - Active player: action buttons for selected unit.
  - Inactive player: target info + reaction buttons.
  - Wound adjustment buttons appear here when an active_effect targets a unit.

gameActionDisplayArea:
  - Combined view: all effects (including passive auras) merged into one result.
  - Shows modifier chain and final outcome so the flow is always transparent.
"""

import streamlit as st

from engine import (
    _NECRON_UNITS,
    _ORK_UNITS,
    PHASES,
    apply_damage,
    heal_unit,
    log_action,
    set_charged,
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

    parts: list[str] = []
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


# ── Active player actions (per phase) ────────────────────────────────────────


def _active_movement(faction: str, uid: str, unit: Unit, state: dict) -> None:  # type: ignore[type-arg]
    ms = state.get("movement_status", "normal")
    in_melee = state.get("in_melee", False)

    if state.get("in_reserve"):
        if st.session_state.round == 1:
            st.warning("In Reserve — cannot deploy until Round 2.")
        else:
            st.info("In Reserve — deploy from the board edge.")
            if st.button(
                "Deploy from Reserve",
                key=f"deploy_reserve_{faction}_{uid}",
                type="primary",
                use_container_width=True,
            ):
                from engine import set_deployment

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


def _active_charge(faction: str, uid: str, unit: Unit, state: dict) -> None:  # type: ignore[type-arg]
    ms = state.get("movement_status", "normal")
    if ms in ("advanced", "retreated"):
        st.warning(f"{ms.capitalize()} this turn — cannot charge.")
        return

    tgt = st.session_state.selected_target
    if tgt is None:
        st.info("Select a **target** to charge from the enemy army list (▷).")
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


def _active_fight(faction: str, uid: str, unit: Unit, state: dict) -> None:  # type: ignore[type-arg]
    if state.get("charged_this_turn"):
        st.markdown("**Fights first** (charged this turn).")

    if not state.get("in_melee"):
        st.warning("Not in melee — no action possible.")
        return

    tgt = st.session_state.selected_target
    if tgt is None:
        st.info("Select a **target** in melee from the enemy army list (▷).")
        return

    tgt_faction, tgt_uid = tgt
    tgt_unit, _ = _lookup(tgt_faction, tgt_uid)
    melee = [w for w in unit.weapons if w.is_melee]
    if not melee:
        st.caption("No melee weapons.")
        return

    skill = int(unit.ws.rstrip("+"))
    for w in melee:
        ap_int = int(w.ap)
        ap_str = f"AP{w.ap}" if ap_int != 0 else "AP0"
        st.caption(
            f"**{w.name_en}** · A{w.attacks} · WS{skill}+ · S{w.strength} · {ap_str} · D{w.damage}"
        )
    if st.button("Log Fight Action", key=f"log_fight_{faction}_{uid}", use_container_width=True):
        log_action(st.session_state.round, "fight", unit.name_en, f"fought {tgt_unit.name_en}")
        st.success("Action logged.")


def _active_morale(unit: Unit, state: dict) -> None:  # type: ignore[type-arg]
    lost = state.get("lost_models_this_turn", 0)
    if unit.models_max == 1:
        st.success("Single model — auto-pass.")
        return
    if lost == 0:
        st.success("No losses this turn — no morale test.")
        return
    st.warning(
        f"**Ld {unit.leadership}** | Lost **{lost}** model(s) this turn.\n\n"
        f"Roll D6 + {lost}. If result > {unit.leadership}: "
        f"remove (result − {unit.leadership}) additional model(s)."
    )


# ── Wound adjustment (PlayerArea, triggered by active_effect) ─────────────────


def _wound_adjustment_buttons(faction: str, uid: str, unit: Unit) -> None:
    """Wound/heal buttons — shown in the PlayerArea of the affected player."""
    bc = st.columns(6)
    for col, delta, label in zip(bc, [-3, -2, -1, 1, 2, 3], ["−3", "−2", "−1", "+1", "+2", "+3"]):
        with col:
            is_mortal = delta == -1
            if st.button(
                label,
                key=f"w{delta}_{faction}_{uid}",
                type="primary" if is_mortal else "secondary",
            ):
                if delta < 0:
                    apply_damage(uid, faction, -delta, unit, mortal=is_mortal)
                else:
                    heal_unit(uid, faction, delta, unit)
                st.rerun()


# ── Player area renderers ─────────────────────────────────────────────────────


def _render_player_area(faction: str, phase_key: str) -> None:
    active_faction = st.session_state.active
    is_active = faction == active_faction

    indicator = "▶" if is_active else "◀"
    st.markdown(f"**{indicator} {faction}**")

    if phase_key == "setup":
        # First-player selection is shown in display area; nothing here
        return

    if is_active:
        sel = st.session_state.selected_unit
        if sel and sel[0] == faction:
            _, uid = sel
            unit, state = _lookup(faction, uid)
            badges = _state_badges_html(state)
            st.markdown(f"*{unit.name_en}*")
            if badges:
                st.markdown(badges, unsafe_allow_html=True)

            if phase_key == "command":
                from gameMechanic.commandPhase import render_actions_command  # noqa: PLC0415

                render_actions_command(st.session_state)

            elif phase_key == "movement":
                _active_movement(faction, uid, unit, state)

            elif phase_key == "psychic":
                is_psyker = any(kw.upper() == "PSYKER" for kw in unit.keywords)
                if is_psyker:
                    st.info("PSYKER — declare Smite or psychic powers manually.")
                else:
                    st.warning("Not a PSYKER — no action possible.")

            elif phase_key == "shooting":
                ms = state.get("movement_status", "normal")
                if ms == "advanced":
                    st.warning("Advanced this turn — cannot shoot.")
                elif ms == "retreated":
                    st.warning("Retreated this turn — cannot shoot.")
                elif state.get("in_melee"):
                    st.warning("Bound in melee — cannot shoot.")
                else:
                    ranged = [w for w in unit.weapons if not w.is_melee]
                    if ranged:
                        skill = int(unit.bs.rstrip("+"))
                        for w in ranged:
                            ap_int = int(w.ap)
                            ap_str = f"AP{w.ap}" if ap_int != 0 else "AP0"
                            st.caption(
                                f"**{w.name_en}** · A{w.attacks} · BS{skill}+ "
                                f"· S{w.strength} · {ap_str} · D{w.damage}"
                            )
                    else:
                        st.caption("No ranged weapons.")

            elif phase_key == "charge":
                _active_charge(faction, uid, unit, state)

            elif phase_key == "fight":
                _active_fight(faction, uid, unit, state)

            elif phase_key == "morale":
                _active_morale(unit, state)

            # Wound adjustment — always accessible for own selected unit
            st.divider()
            _wound_adjustment_buttons(faction, uid, unit)

        else:
            st.caption("← Select a unit from your army list.")

    else:
        # Inactive player — show target info or reaction options
        tgt = st.session_state.selected_target
        if tgt and tgt[0] == faction:
            _, uid = tgt
            unit, state = _lookup(faction, uid)
            badges = _state_badges_html(state)
            st.markdown(f"*{unit.name_en}* ← Target")
            if badges:
                st.markdown(badges, unsafe_allow_html=True)

            if phase_key in ("shooting", "fight"):
                inv_display = f"{unit.invuln_save}+" if unit.invuln_save else "—"
                cols = st.columns(3)
                cols[0].metric("T", unit.toughness)
                cols[1].metric("Sv", f"{unit.save}+")
                cols[2].metric("++", inv_display)
            elif phase_key == "charge":
                st.caption("Overwatch: only unmodified 6s hit.")

            # Wound adjustment — accessible for targeted unit too
            st.divider()
            _wound_adjustment_buttons(faction, uid, unit)

        elif st.session_state.selected_unit:
            if phase_key in ("shooting", "charge", "fight"):
                st.caption("← Designate a target (▷) from your army list.")
            else:
                st.caption("—")
        else:
            st.caption("—")


# ── Display area (combined effect view) ───────────────────────────────────────


def _render_display_area(phase_key: str) -> None:
    if phase_key == "setup":
        _display_setup()
        return

    # Phase context text
    rules = _PHASE_RULES.get(phase_key, "")
    if rules:
        st.info(rules)

    # Combined attack summary when both attacker and target are selected
    sel = st.session_state.selected_unit
    tgt = st.session_state.selected_target
    if sel and tgt and phase_key in ("shooting", "fight"):
        _display_attack_summary(sel, tgt, phase_key)


def _display_setup() -> None:
    st.markdown("### Setup")
    st.info(
        "Configure your armies before the battle begins.\n\n"
        "1. **Select first player** — the active player takes their turn first.\n"
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


def _display_attack_summary(
    sel: tuple[str, str],
    tgt: tuple[str, str],
    phase_key: str,
) -> None:
    atk_faction, atk_uid = sel
    def_faction, def_uid = tgt
    atk_unit, atk_state = _lookup(atk_faction, atk_uid)
    def_unit, _ = _lookup(def_faction, def_uid)

    use_melee = phase_key == "fight"
    weapons = [w for w in atk_unit.weapons if w.is_melee == use_melee]
    if not weapons:
        return

    st.markdown(f"**{atk_unit.name_en}** → **{def_unit.name_en}**")
    st.markdown("*Attack reference (roll dice on the table):*")

    skill = int(atk_unit.ws.rstrip("+")) if use_melee else int(atk_unit.bs.rstrip("+"))
    skill_label = "WS" if use_melee else "BS"
    inv_display = f"{def_unit.invuln_save}+" if def_unit.invuln_save else "none"

    for w in weapons:
        thresh = _wound_thresh(int(w.strength), def_unit.toughness)
        eff_save = def_unit.save + abs(int(w.ap))
        if def_unit.invuln_save and def_unit.invuln_save < eff_save:
            eff_save = def_unit.invuln_save
        save_str = f"{eff_save}+" if eff_save <= 6 else "none"
        st.caption(
            f"**{w.name_en}**: {w.attacks} att · {skill_label}{skill}+ · "
            f"wound {thresh}+ · save {save_str} (++ {inv_display}) · D{w.damage}"
        )

    if st.button(
        f"Log {'Shooting' if phase_key == 'shooting' else 'Fight'} Action",
        key=f"log_{phase_key}_{atk_faction}_{atk_uid}",
        use_container_width=True,
    ):
        log_action(
            st.session_state.round,
            phase_key,
            atk_unit.name_en,
            f"{'shot at' if phase_key == 'shooting' else 'fought'} {def_unit.name_en}",
        )
        st.success("Action logged.")


# ── Main entry point ──────────────────────────────────────────────────────────


def render_game_actions_area() -> None:
    phase_key = PHASES[st.session_state.phase_idx][1]
    first = st.session_state.first_player
    second = st.session_state.second_player

    # ── Section 1: Player Areas (50 / 50) ──────────────────────
    col_p1, col_p2 = st.columns(2)
    with col_p1:
        _render_player_area(first, phase_key)
    with col_p2:
        _render_player_area(second, phase_key)

    st.divider()

    # ── Section 2: Game Action Display (full width) ────────────
    _render_display_area(phase_key)
