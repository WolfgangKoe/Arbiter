"""MoralePhaseHandler — Morale Phase for WH40k 9E."""

from __future__ import annotations

import streamlit as st

from gameMechanic.game_log import log_action
from gameMechanic.game_state import units_key_for, units_list_for
from gameMechanic.unit_mutations import flee_models
from gameObjects.unit import Unit


def morale_test_required(unit, unit_state: dict) -> bool:  # type: ignore[type-arg]
    """Return True when a unit must take a Morale test this phase (App-enforced filter).

    Implements the R-MORALE-02 filter:
    - Skips single-model units (models_max == 1) — they never test.
    - Skips destroyed units.
    - Requires at least one model lost this turn (lost_models_this_turn > 0).
    """
    if unit.models_max == 1:
        return False
    if unit_state.get("destroyed"):
        return False
    return unit_state.get("lost_models_this_turn", 0) > 0


def _fail_threshold(leadership: int, lost: int) -> int:
    """Minimum D6 result that causes the morale test to fail.

    Test fails when D6 + lost > leadership, i.e. D6 >= leadership - lost + 1.
    """
    return leadership - lost + 1


class MoralePhaseHandler:
    """PhaseHandler for the Morale Phase."""

    phase_name: str = "morale"

    def render_start(self, state: dict) -> None:  # type: ignore[type-arg]
        pass

    def render_active(self, state: dict) -> None:  # type: ignore[type-arg]
        first: str = state["first_player"]
        second: str = state["second_player"]
        unit_map = {
            first: {u.id: u for u in units_list_for(first)},
            second: {u.id: u for u in units_list_for(second)},
        }
        state_map = {
            first: st.session_state[units_key_for(first)],
            second: st.session_state[units_key_for(second)],
        }

        col1, col2 = st.columns(2)
        with col1:
            _render_faction_morale(first, unit_map[first], state_map[first], state)
        with col2:
            _render_faction_morale(second, unit_map[second], state_map[second], state)

    def render_end(self, state: dict) -> None:  # type: ignore[type-arg]
        pass


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _render_faction_morale(
    faction: str,
    units: dict[str, Unit],
    unit_states: dict,  # type: ignore[type-arg]
    state: dict,  # type: ignore[type-arg]
) -> None:
    st.markdown(f"**{faction}**")
    any_test = False
    for uid, unit_state in unit_states.items():
        unit = units.get(uid)
        if unit is None:
            continue
        if not morale_test_required(unit, unit_state):
            continue
        any_test = True
        st.divider()
        _render_unit_morale(faction, uid, unit, unit_state, state)
    if not any_test:
        st.success("Keine Einheit hat Verluste erlitten — keine Moraltests.")


def _render_unit_morale(
    faction: str,
    uid: str,
    unit: Unit,
    unit_state: dict,  # type: ignore[type-arg]
    state: dict,  # type: ignore[type-arg]
) -> None:
    st.markdown(f"**{unit.name_en}**")
    lost = unit_state["lost_models_this_turn"]
    flags = unit_state["turn_flags"]

    if flags.get("morale_tested"):
        fled = unit_state.get("fled_models_this_turn", 0)
        if fled > 0:
            st.warning(f"Fehlgeschlagen — {fled} Modelle geflohen.")
        else:
            st.success("Moraltest bestanden.")
        return

    ld = unit.leadership
    threshold = _fail_threshold(ld, lost)

    st.caption(f"Ld {ld} | Verluste diese Runde: {lost}")

    if threshold > 6:
        st.success(f"Kann nicht fehlschlagen — W6+{lost} ≤ {ld} bei jedem Ergebnis.")
        if st.button("Bestätigen (auto-bestanden)", key=f"morale_autopass_{uid}"):
            flags["morale_tested"] = True
            log_action(state["round"], "morale", unit.name_en, "Moraltest automatisch bestanden.")
            st.rerun()
        return

    if threshold <= 1:
        st.error(f"Schlägt immer fehl — W6+{lost} > {ld} bei jedem Ergebnis.")
    else:
        st.markdown(
            f"Schlägt fehl ab **W6-Ergebnis {threshold}** "
            f"({threshold}+{lost}={threshold + lost} > {ld})"
        )

    col_pass, col_fail = st.columns(2)
    with col_pass:
        if st.button("✓ Bestanden", key=f"morale_pass_{uid}"):
            flags["morale_tested"] = True
            log_action(state["round"], "morale", unit.name_en, "Moraltest bestanden.")
            st.rerun()
    with col_fail:
        if st.button("✗ Fehlgeschlagen", key=f"morale_fail_{uid}"):
            st.session_state[f"morale_failed_{uid}"] = True
            st.rerun()

    if st.session_state.get(f"morale_failed_{uid}"):
        fled_count = st.number_input(
            "Wie viele Modelle sind geflohen?",
            min_value=1,
            max_value=unit_state["models"],
            step=1,
            key=f"morale_fled_count_{uid}",
        )
        if st.button("Bestätigen", key=f"morale_confirm_{uid}"):
            flee_models(uid, faction, int(fled_count), unit)
            log_action(
                state["round"],
                "morale",
                unit.name_en,
                f"Moraltest fehlgeschlagen — {int(fled_count)} Modelle geflohen.",
            )
            st.session_state.pop(f"morale_failed_{uid}", None)
            st.rerun()
