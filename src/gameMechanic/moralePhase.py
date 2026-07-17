"""MoralePhaseHandler — Morale Phase for WH40k 9E."""

from __future__ import annotations

from collections.abc import MutableMapping
from typing import Any, ClassVar

import streamlit as st

from constants.symbols import SYM_CHECK
from gameMechanic.gameLog import log_action
from gameMechanic.gameState import (
    faction_dir_for,
    unit_id_from_state_key,
    units_key_for,
    units_list_for,
)
from gameMechanic.unitMutations import confirm_morale_auto_pass, flee_models
from gameObjects.ability import Ability
from gameObjects.loader import get_abilities_for_unit
from gameObjects.unit import Unit

# Combat Attrition (9E core rules): after a failed Morale test and the first
# fled model, roll one D6 per remaining model; each (modified) result of 1
# flees. Being below Half-strength subtracts 1 from each roll.
_ATTRITION_EFFECT_TYPE = "attrition_modifier"
_ATTRITION_BASE_THRESHOLD = 1


def morale_test_required(unit: Unit, unit_state: MutableMapping[str, Any]) -> bool:
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
    return bool(unit_state.get("lost_models_this_turn", 0) > 0)


def _fail_threshold(leadership: int, lost: int) -> int:
    """Minimum D6 result that causes the morale test to fail.

    Test fails when D6 + lost > leadership, i.e. D6 >= leadership - lost + 1.
    """
    return leadership - lost + 1


def attrition_modifier_abilities(abilities: list[Ability]) -> list[Ability]:
    """Abilities whose effect modifies Combat Attrition tests (data-driven filter)."""
    return [a for a in abilities if a.effect.type == _ATTRITION_EFFECT_TYPE]


def attrition_condition(ability: Ability) -> tuple[str | None, bool]:
    """Table-condition prompt and applies_when flag for an attrition modifier.

    The prompt text and flag ride in the effect's raw sub-effect list
    (``condition_prompt`` / ``applies_when``) because the Ability schema has no
    first-class fields for them yet. ``applies_when`` states for which checkbox
    state the modifier is active — ``False`` means the modifier applies while
    the prompted condition is NOT ticked (e.g. no herder model nearby).
    Distance checks stay table responsibility (same pattern as Cover).
    """
    for sub in ability.effect.effects or []:
        if "condition_prompt" in sub:
            return str(sub["condition_prompt"]), bool(sub.get("applies_when", True))
    return None, True


def _attrition_threshold(
    unit: Unit,
    unit_state: MutableMapping[str, Any],
    ability_mods: list[int],
) -> int:
    """Highest (unmodified) D6 result at which a model flees a Combat Attrition test.

    Base: a modified roll of 1 flees. Attrition tests are taken AFTER the first
    model has fled the failed Morale test, so Half-strength is checked against
    ``models - 1``. Each active ability modifier shifts the roll by its value —
    a -1 modifier therefore raises the flee threshold by 1. Clamped to 0..6
    (0 = no roll can flee, 6 = every roll flees).
    """
    initial = unit_state.get("models_initial") or unit.models_max
    remaining = unit_state["models"] - 1
    threshold = _ATTRITION_BASE_THRESHOLD - sum(ability_mods)
    if remaining * 2 < initial:
        threshold += 1
    return max(0, min(6, threshold))


class MoralePhaseHandler:
    """PhaseHandler for the Morale Phase."""

    phase_name: ClassVar[str] = "morale"

    def render_active(self, state: MutableMapping[str, Any]) -> None:
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


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _render_faction_morale(
    faction: str,
    units: dict[str, Unit],
    unit_states: MutableMapping[str, Any],
    state: MutableMapping[str, Any],
) -> None:
    st.markdown(f"**{faction}**")
    any_test = False
    for uid, unit_state in unit_states.items():
        unit = units.get(unit_id_from_state_key(uid))
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
    unit_state: MutableMapping[str, Any],
    state: MutableMapping[str, Any],
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

    if flags.get("morale_auto_pass"):
        st.success(f"{SYM_CHECK} Insane Bravery active — Morale test automatically passed.")
        if st.button("Confirm (Insane Bravery)", key=f"morale_insane_bravery_{uid}"):
            confirm_morale_auto_pass(uid, faction)
            log_action(
                state["round"],
                "morale",
                unit.name_en,
                "Insane Bravery — Moraltest automatisch bestanden.",
            )
            st.rerun()
        return

    ld = unit.leadership
    # unit.leadership is None only for buildings/fortifications (single-model
    # units) — morale_test_required's models_max == 1 filter keeps those from
    # ever reaching this render function, so ld is always a real Ld here.
    assert ld is not None
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
        if st.button(f"{SYM_CHECK} Bestanden", key=f"morale_pass_{uid}"):
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
        _render_attrition_hint(faction, uid, unit, unit_state)
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


def _render_attrition_hint(
    faction: str,
    uid: str,
    unit: Unit,
    unit_state: MutableMapping[str, Any],
) -> None:
    """Display-only Combat Attrition hint — the D6 rolls stay on the table.

    Renders one checkbox per conditional attrition modifier (prompt text comes
    from YAML) and shows the resulting flee threshold. The fled-count input
    above stays the single source of truth for the state mutation.
    """
    abilities = get_abilities_for_unit(unit, faction_dir_for(faction))
    active_mods: list[int] = []
    for ability in attrition_modifier_abilities(abilities):
        modifier = ability.effect.modifier or 0
        prompt, applies_when = attrition_condition(ability)
        if prompt is None:
            active_mods.append(modifier)
            continue
        checked = st.checkbox(prompt, key=f"attrition_cond_{uid}_{ability.id}")
        if checked == applies_when:
            active_mods.append(modifier)
    threshold = _attrition_threshold(unit, unit_state, active_mods)
    dice = max(unit_state["models"] - 1, 0)
    if threshold <= 0:
        st.caption(
            f"Combat Attrition: 1 W6 pro verbleibendem Modell ({dice}) — "
            "kein Modell flieht (Modifikatoren heben jedes Ergebnis über 1)."
        )
    else:
        st.caption(
            f"Combat Attrition: 1 W6 pro verbleibendem Modell ({dice}) — "
            f"flieht bei Ergebnis ≤ {threshold}."
        )
