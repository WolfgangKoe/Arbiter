"""unitCard — New layout: name trigger, keywords, LP bars, state badges, collapsible phase area."""

import streamlit as st

from engine import PHASES, apply_damage, heal_unit, set_deployment
from gameObjects.unit import Unit

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


def _state_badges_html(state: dict) -> str:  # type: ignore[type-arg]
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


def _lookup_in_state(faction: str, uid: str) -> dict:  # type: ignore[type-arg]
    key = "necron_units" if faction == "Necrons" else "ork_units"
    return st.session_state[key][uid]


def _dynamic_setup(unit: Unit, state: dict, faction: str) -> None:  # type: ignore[type-arg]
    opts = ["Normal", "Stationary", "Reserve"]
    current = state.get("deployment", "normal").capitalize()
    idx = opts.index(current) if current in opts else 0
    chosen = st.selectbox(
        "Deployment",
        opts,
        index=idx,
        key=f"deploy_{faction}_{unit.id}",
    )
    mapping = {"Normal": "normal", "Stationary": "stationary", "Reserve": "reserve"}
    new_val = mapping[chosen]
    if new_val != state.get("deployment", "normal"):
        set_deployment(unit.id, faction, new_val)
        st.rerun()


def _dynamic_movement(unit: Unit, state: dict, faction: str) -> None:  # type: ignore[type-arg]
    if state.get("in_reserve"):
        if st.session_state.round == 1:
            st.caption("In Reserve — arrives from Round 2.")
        else:
            st.caption("In Reserve — can be deployed this turn.")
        return
    st.caption(f"**M** {unit.move}")
    badges_html = _state_badges_html(state)
    if badges_html:
        st.markdown(badges_html, unsafe_allow_html=True)
    else:
        st.caption("Status: Normal")


def _dynamic_shooting_attacker(unit: Unit, state: dict) -> None:  # type: ignore[type-arg]
    ms = state.get("movement_status", "normal")
    if ms == "advanced":
        st.caption("⚠ Advanced — cannot shoot.")
        return
    if ms == "retreated":
        st.caption("⚠ Retreated — cannot shoot.")
        return
    if state.get("in_melee"):
        st.caption("⚠ In melee — cannot shoot.")
        return
    ranged = [w for w in unit.weapons if not w.is_melee]
    if not ranged:
        st.caption("No ranged weapons.")
        return
    skill = int(unit.bs.rstrip("+"))
    for w in ranged:
        ap_int = int(w.ap)
        ap_str = f"AP{w.ap}" if ap_int != 0 else "AP0"
        st.caption(
            f"**{w.name_en}** · A{w.attacks} · BS{skill}+ · S{w.strength} · {ap_str} · D{w.damage}"
            + (f" · _{w.abilities}_" if w.abilities else "")
        )


def _dynamic_shooting_target(unit: Unit, state: dict) -> None:  # type: ignore[type-arg]
    inv_str = f"{unit.invuln_save}+" if unit.invuln_save else "—"
    fnp_str = f"{unit.fnp}+" if unit.fnp else "—"
    cols = st.columns(4)
    cols[0].metric("T", unit.toughness)
    cols[1].metric("Sv", f"{unit.save}+")
    cols[2].metric("++", inv_str)
    cols[3].metric("FNP", fnp_str)


def _dynamic_fight(unit: Unit, state: dict, is_active: bool) -> None:  # type: ignore[type-arg]
    in_melee = state.get("in_melee")
    if not in_melee and not is_active:
        st.caption("No action possible.")
        return
    if state.get("charged_this_turn"):
        st.caption("**Fights first** (charged this turn).")
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
            + (f" · _{w.abilities}_" if w.abilities else "")
        )


def _dynamic_morale(unit: Unit, state: dict) -> None:  # type: ignore[type-arg]
    lost = state.get("lost_models_this_turn", 0)
    if unit.models_max == 1:
        st.caption("Single model — auto-pass.")
        return
    if lost == 0:
        st.caption("No losses this turn — no test required.")
        return
    st.caption(f"**Ld** {unit.leadership} | Lost **{lost}** model(s) → morale test required.")


def _unit_dynamic_section(
    unit: Unit, state: dict, faction: str, phase_key: str, is_active: bool  # type: ignore[type-arg]
) -> None:
    is_psyker = any(kw.upper() == "PSYKER" for kw in unit.keywords)

    if phase_key == "setup":
        _dynamic_setup(unit, state, faction)
        return

    if state.get("in_reserve") and phase_key != "movement":
        st.caption("In Reserve — not on battlefield.")
        return

    if phase_key == "command":
        st.caption("No phase-specific actions.")
    elif phase_key == "movement":
        if is_active:
            _dynamic_movement(unit, state, faction)
        else:
            st.caption("—")
    elif phase_key == "psychic":
        if is_psyker:
            st.caption("PSYKER — select to declare psychic powers.")
        else:
            st.caption("No action possible.")
    elif phase_key == "shooting":
        if is_active:
            _dynamic_shooting_attacker(unit, state)
        else:
            _dynamic_shooting_target(unit, state)
    elif phase_key == "charge":
        if is_active:
            ms = state.get("movement_status", "normal")
            if ms in ("advanced", "retreated"):
                st.caption(f"⚠ {ms.capitalize()} — cannot charge.")
            else:
                st.caption('Eligible to charge (≤ 12" from enemy).')
        else:
            st.caption("—")
    elif phase_key == "fight":
        _dynamic_fight(unit, state, is_active)
    elif phase_key == "morale":
        _dynamic_morale(unit, state)


def render_unit_card(unit: Unit, state: dict, faction: str) -> None:  # type: ignore[type-arg]
    phase_key = PHASES[st.session_state.phase_idx][1]
    active = st.session_state.active
    is_active = faction == active

    destroyed = state["destroyed"]
    uid = unit.id

    if destroyed:
        st.markdown(f"~~{unit.name_en}~~  *(DESTROYED)*")
        return

    in_reserve = state.get("in_reserve", False)
    if phase_key != "setup" and is_active:
        sel = st.session_state.selected_unit
        is_sel = sel == (faction, uid)
        btn_label = f"◀ {unit.name_en}" if is_sel else f"▶ {unit.name_en}"
        btn_type: str = "primary" if is_sel else "secondary"
        if st.button(
            btn_label,
            key=f"name_{faction}_{uid}",
            type=btn_type,
            use_container_width=True,
            disabled=in_reserve,
        ):
            st.session_state.selected_unit = None if is_sel else (faction, uid)
            st.session_state.selected_target = None
            st.rerun()
    else:
        st.markdown(f"**{unit.name_en}**")

    # Keywords as HTML badge spans (all keywords in one style)
    kw_parts = [
        f'<span style="background:#1c1a14;border:1px solid #2e2618;border-radius:2px;'
        f'padding:1px 5px;font-size:9px;color:#6b5f44;letter-spacing:0.05em;margin-right:2px;">'
        f"{kw}</span>"
        for kw in unit.keywords
    ]
    if kw_parts:
        st.markdown("".join(kw_parts), unsafe_allow_html=True)

    cur = state["current_wounds"]
    models_alive = state["models"]

    if unit.models_max == 1:
        st.progress(cur / unit.wounds if unit.wounds > 0 else 0)
        st.caption(f"LP {cur}/{unit.wounds}")
    elif unit.wounds == 1:
        st.progress(models_alive / unit.models_max if unit.models_max > 0 else 0)
        st.caption(f"⬡ {models_alive}/{unit.models_max}")
    else:
        front_wounds = cur - (models_alive - 1) * unit.wounds if models_alive > 0 else 0
        st.progress(models_alive / unit.models_max)
        st.caption(f"⬡ {models_alive}/{unit.models_max}")
        st.progress(front_wounds / unit.wounds if unit.wounds > 0 else 0)
        st.caption(f"LP {front_wounds}/{unit.wounds}")

    badges_html = _state_badges_html(state)
    if badges_html and phase_key != "setup":
        st.markdown(badges_html, unsafe_allow_html=True)

    with st.expander(f"▾ {unit.name_en} — Info / Actions"):
        sc = st.columns(7)
        for col, lbl, val in zip(
            sc,
            ["M", "T", "Sv", "W", "++", "Ld", "OC"],
            [
                unit.move,
                unit.toughness,
                f"{unit.save}+",
                unit.wounds,
                f"{unit.invuln_save}+" if unit.invuln_save else "—",
                unit.leadership,
                unit.oc,
            ],
        ):
            col.metric(lbl, val)

        bc = st.columns(6)
        for col, delta, label in zip(
            bc, [-3, -2, -1, 1, 2, 3], ["−3", "−2", "−1", "+1", "+2", "+3"]
        ):
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

        if phase_key in ("shooting", "fight", "charge") and not is_active:
            tgt = st.session_state.selected_target
            is_tgt = tgt == (faction, uid)
            btn_lbl = "◀ Targeted" if is_tgt else "▶ Target"
            btn_type_tgt: str = "primary" if is_tgt else "secondary"
            if st.button(
                btn_lbl,
                key=f"tgt_{faction}_{uid}",
                type=btn_type_tgt,
                use_container_width=True,
                disabled=in_reserve,
            ):
                st.session_state.selected_target = None if is_tgt else (faction, uid)
                st.rerun()

        st.divider()
        _unit_dynamic_section(unit, state, faction, phase_key, is_active)

        if unit.abilities:
            st.caption(f"*{unit.abilities}*")
