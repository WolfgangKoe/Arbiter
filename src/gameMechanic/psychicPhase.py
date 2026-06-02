"""PsychicPhaseHandler — Psychic Phase for WH40k 9E.

Ziel 4f: Manifest (2D6 ≥ WC 5), Deny, Perils of the Warp, Smite.
Scope: Smite only. Blessing-flow (friendly target) follows in a later goal.
"""

from __future__ import annotations

import streamlit as st

from gameMechanic.game_log import log_action
from gameMechanic.game_state import units_key_for, units_list_for
from gameMechanic.unit_mutations import apply_damage
from gameObjects.unit import Unit
from uiLayout._common import PHASE_RULES, lookup


class PsychicPhaseHandler:
    """PhaseHandler for the Psychic Phase."""

    phase_name: str = "psychic"

    def render_start(self, state: dict) -> None:  # type: ignore[type-arg]
        pass

    def render_active(self, state: dict) -> None:  # type: ignore[type-arg]
        first: str = state["first_player"]
        second: str = state["second_player"]

        # Track deny uses per faction within this phase (each faction can deny once).
        if "psychic_denies_used" not in st.session_state:
            st.session_state.psychic_denies_used = {}

        col1, col2 = st.columns(2)
        with col1:
            _render_psychic_column(first, state)
        with col2:
            _render_psychic_column(second, state)

        st.divider()
        st.info(PHASE_RULES["psychic"])

    def render_end(self, state: dict) -> None:  # type: ignore[type-arg]
        st.session_state.psi_result = None
        st.session_state.psychic_denies_used = {}


# ---------------------------------------------------------------------------
# Pure helper functions (also exported for tests)
# ---------------------------------------------------------------------------


def has_psyker(units: list[Unit]) -> bool:
    return any("PSYKER" in {kw.upper() for kw in u.keywords} for u in units)


def can_deny(units: list[Unit]) -> bool:
    return any(
        "PSYKER" in {kw.upper() for kw in u.keywords} or "gloom_prism" in u.rules for u in units
    )


def is_perils(roll: int) -> bool:
    return roll in (2, 12)


def smite_damage_die(roll: int) -> str:
    return "W6" if roll >= 11 else "W3"


def deny_succeeds(manifest_roll: int, deny_roll: int) -> bool:
    return deny_roll > manifest_roll


def cast_eligibility(unit_state: dict) -> tuple[bool, str | None]:  # type: ignore[type-arg]
    """Return (eligible, reason) — None reason means eligible to manifest."""
    flags = unit_state.get("turn_flags", {})
    if flags.get("retreated"):
        return False, "Retreated this turn — cannot manifest psychic powers."
    if flags.get("cast"):
        return False, "Already manifested this phase — each PSYKER may only be chosen once."
    return True, None


# ---------------------------------------------------------------------------
# Column rendering
# ---------------------------------------------------------------------------


def _render_psychic_column(faction: str, state: dict) -> None:  # type: ignore[type-arg]
    is_active = faction == state["active"]
    indicator = "▶" if is_active else "◀"
    st.markdown(f"**{indicator} {faction}**")

    if is_active:
        _render_active_psychic(faction, state)
    else:
        _render_deny_column(faction, state)


def _render_active_psychic(faction: str, state: dict) -> None:  # type: ignore[type-arg]
    units = units_list_for(faction)

    if not has_psyker(units):
        st.caption("No PSYKER units — skip this phase.")
        return

    sel = st.session_state.selected_unit
    if not sel or sel[0] != faction:
        st.caption("← Select a PSYKER from your army list.")
        return

    _, uid = sel
    unit, unit_state = lookup(faction, uid)
    st.markdown(f"*{unit.name_en}*")

    if not any(kw.upper() == "PSYKER" for kw in unit.keywords):
        st.warning("Not a PSYKER — select a PSYKER unit.")
        return

    eligible, reason = cast_eligibility(unit_state)
    if not eligible:
        st.warning(reason)
        return

    _render_smite_flow(faction, uid, unit, state)


def _render_smite_flow(
    faction: str, uid: str, unit: Unit, state: dict  # type: ignore[type-arg]
) -> None:
    psi = st.session_state.get("psi_result")

    if psi is not None and psi.get("faction") == faction and psi.get("uid") == uid:
        _render_psi_result(faction, uid, unit, psi, state)
        return

    # No active result — show manifest input.
    wc = 5 + st.session_state.get("psi_attempts_this_phase", 0)
    st.markdown(f"**Smite** — Warp Charge {wc}")
    roll = st.number_input(
        "2D6 roll",
        min_value=2,
        max_value=12,
        value=7,
        key=f"psi_roll_{faction}_{uid}",
    )
    if st.button(
        "Attempt Manifest",
        key=f"psi_manifest_{faction}_{uid}",
        type="primary",
        use_container_width=True,
    ):
        manifested = roll >= wc
        perils = is_perils(int(roll))
        st.session_state.psi_attempts_this_phase = (
            st.session_state.get("psi_attempts_this_phase", 0) + 1
        )
        st.session_state.psi_result = {
            "faction": faction,
            "uid": uid,
            "roll": int(roll),
            "manifested": manifested,
            "perils": perils,
            "perils_applied": False,
            "denied": None,
            "deny_roll": None,
        }
        outcome = "manifested" if manifested else "failed"
        perils_note = " (Perils!)" if perils else ""
        log_action(
            state["round"],
            "psychic",
            unit.name_en,
            f"Smite manifest roll {int(roll)} — {outcome}{perils_note}",
        )
        st.rerun()


def _render_psi_result(
    faction: str,
    uid: str,
    unit: Unit,
    psi: dict,  # type: ignore[type-arg]
    state: dict,  # type: ignore[type-arg]
) -> None:
    roll: int = psi["roll"]
    manifested: bool = psi["manifested"]
    perils: bool = psi["perils"]
    perils_applied: bool = psi["perils_applied"]
    denied = psi["denied"]  # None | True | False

    # Perils must be resolved before anything else.
    if perils and not perils_applied:
        if manifested:
            st.error(f"**Perils of the Warp!** Roll {roll} — power manifested.")
        else:
            st.error(f"**Perils of the Warp!** Roll {roll} — power failed.")
        st.markdown(f"Apply W3 mortal wounds to *{unit.name_en}*:")
        perils_dmg = st.number_input(
            "Perils damage (1–3)",
            min_value=1,
            max_value=3,
            value=2,
            key=f"psi_perils_dmg_{faction}_{uid}",
        )
        if st.button(
            f"Apply to {unit.name_en}",
            key=f"psi_perils_apply_{faction}_{uid}",
            type="primary",
            use_container_width=True,
        ):
            apply_damage(uid, faction, int(perils_dmg), unit, mortal=True)
            psi["perils_applied"] = True
            st.session_state.psi_result = psi
            log_action(
                state["round"],
                "psychic",
                unit.name_en,
                f"Perils of the Warp — {int(perils_dmg)} mortal wounds",
            )
            st.rerun()
        return

    # Power failed (and no perils, or perils already applied).
    if not manifested:
        st.warning(f"Roll {roll} — Power failed (< 5).")
        if st.button("Reset", key=f"psi_reset_{faction}_{uid}", use_container_width=True):
            st.session_state.psi_result = None
            st.rerun()
        return

    # Power denied.
    if denied is True:
        st.warning(f"Roll {roll} — Manifested, but Denied!")
        if st.button("Reset", key=f"psi_reset_denied_{faction}_{uid}", use_container_width=True):
            st.session_state.psi_result = None
            st.rerun()
        return

    # Manifested and not denied — show Smite application.
    die = smite_damage_die(roll)
    if denied is None:
        st.success(f"Roll {roll} — Manifested! Waiting for deny attempt… ({die} mortal wounds)")
    else:
        st.success(f"Roll {roll} — Manifested! Deny failed. ({die} mortal wounds)")

    targets = [t for t in st.session_state.selected_targets if t[0] != faction]
    if not targets:
        st.caption(
            "① Click an enemy unit in their army list to mark it as Smite target,"
            " then the damage button appears."
        )
    else:
        for tgt_faction, tgt_uid in targets:
            tgt_unit, _ = lookup(tgt_faction, tgt_uid)
            st.markdown(f"**Smite → {tgt_unit.name_en}** ({die})")
            max_val = 6 if die == "W6" else 3
            smite_dmg = st.number_input(
                f"Mortal wounds (1–{max_val})",
                min_value=1,
                max_value=max_val,
                value=max(1, max_val // 2),
                key=f"psi_smite_dmg_{faction}_{uid}_{tgt_uid}",
            )
            if st.button(
                f"Apply {int(smite_dmg)} mortal wounds to {tgt_unit.name_en}",
                key=f"psi_smite_apply_{faction}_{uid}_{tgt_uid}",
                type="primary",
                use_container_width=True,
            ):
                apply_damage(tgt_uid, tgt_faction, int(smite_dmg), tgt_unit, mortal=True)
                unit_key = units_key_for(faction)
                st.session_state[unit_key][uid]["turn_flags"]["cast"] = True
                log_action(
                    state["round"],
                    "psychic",
                    unit.name_en,
                    f"Smite → {tgt_unit.name_en}: {int(smite_dmg)} mortal wounds",
                )
                st.session_state.psi_result = None
                st.session_state.selected_targets = []
                st.rerun()

    if st.button("Reset (skip Smite)", key=f"psi_skip_{faction}_{uid}", use_container_width=True):
        st.session_state.psi_result = None
        st.rerun()


# ---------------------------------------------------------------------------
# Inactive player — deny column
# ---------------------------------------------------------------------------


def _render_deny_column(faction: str, state: dict) -> None:  # type: ignore[type-arg]
    units = units_list_for(faction)

    if not can_deny(units):
        st.caption("No PSYKER or Gloom Prism — cannot deny.")
        return

    # Each faction may deny at most once per Psychic Phase (Deny 1 / Gloom Prism).
    if st.session_state.get("psychic_denies_used", {}).get(faction):
        st.caption("Deny already used this phase (Deny 1 / Gloom Prism: once per phase).")
        return

    psi = st.session_state.get("psi_result")

    if psi is None:
        st.caption("Waiting for psychic manifest attempt.")
        return

    if not psi.get("manifested"):
        st.caption("Manifest failed — no deny needed.")
        return

    if psi.get("denied") is True:
        st.success("Denied!")
        return

    if psi.get("denied") is False:
        st.warning("Deny failed.")
        return

    # denied is None → deny attempt possible.
    manifest_roll: int = psi["roll"]
    st.markdown(f"**Deny the Witch: 2D6 > {manifest_roll}**")
    deny_roll = st.number_input(
        "Deny roll (2D6)",
        min_value=2,
        max_value=12,
        value=7,
        key=f"deny_roll_{faction}",
    )
    col_a, col_b = st.columns(2)
    with col_a:
        if st.button(
            "Attempt Deny",
            key=f"deny_btn_{faction}",
            type="primary",
            use_container_width=True,
        ):
            succeeded = deny_succeeds(manifest_roll, int(deny_roll))
            psi["denied"] = succeeded
            psi["deny_roll"] = int(deny_roll)
            st.session_state.psi_result = psi
            # Mark deny as used for this faction — only one deny per phase.
            used = st.session_state.get("psychic_denies_used", {})
            used[faction] = True
            st.session_state.psychic_denies_used = used
            outcome = "succeeded" if succeeded else "failed"
            log_action(
                state["round"],
                "psychic",
                faction,
                f"Deny {outcome} (roll {int(deny_roll)} vs {manifest_roll})",
            )
            st.rerun()
    with col_b:
        if st.button("Skip Deny", key=f"deny_skip_{faction}", use_container_width=True):
            # Explicitly mark as not denied so Smite proceeds.
            psi["denied"] = False
            st.session_state.psi_result = psi
            st.rerun()
