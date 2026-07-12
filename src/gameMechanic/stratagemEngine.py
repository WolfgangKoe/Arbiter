"""Consolidated stratagem-effect dispatch (S142 Aufgabe 1, Option B).

Before S142 this logic was split across three call sites with no shared
module: ``uiLayout._common._apply_stratagem_effect`` (state mutation on
spend), ``uiLayout.gameProtocoll._effect_gate_met`` (pre-spend gate) and
``gameMechanic.abilityEngine.stratagem_strength_bonus`` (read-back helper).
All three dispatch on the same machine-readable ``Effect`` shape
(``gameObjects/stratagem.py``) — this module gives them one home so a new
effect shape is added in one place instead of three. Pure umzug: behaviour
unchanged, only the import path of each function moved.
"""

from __future__ import annotations

import streamlit as st

from gameMechanic.gameState import PHASES
from gameMechanic.unitMutations import activate_desperate_breakout, activate_morale_auto_pass
from gameObjects.stratagem import Stratagem


def _apply_stratagem_effect(strat: Stratagem, faction: str, unit_key: str) -> None:
    """Dispatch a stratagem's machine-readable ``effect`` to the unit it targets.

    Data-driven on ``effect.type`` (mirrors the Ability effect-dispatch pattern in
    gameMechanic/abilityEngine.py) — new effect types are added here as new
    branches, never via a stratagem-name check. Handles: ``auto_pass_morale``
    (Insane Bravery), ``move`` with ``handler: fall_back_through_models``
    (Desperate Breakout, Plan 016 S130), and ``invuln_save`` (Quantum
    Deflection, S135 Paket 4b) — the latter registers an ``active_modifiers``
    entry with ``roll_type: "invuln_save"`` so the Save block's invuln
    computation (``_stratagem_invuln_save``) picks it up the same way
    ``ability_invuln_save`` already reads faction-ability-granted invulns;
    ``undo_stratagem``'s generic ``source``-name cleanup removes it again
    unchanged. No-ops for any other effect type (e.g. attack-sequence
    stratagems, which use `.modifier` instead) — silently ignored here on
    purpose, same as an unmatched unit_key.
    """
    effect = strat.effect
    if effect is None:  # caller already checked; narrows the type for mypy
        return
    if effect.type == "auto_pass_morale":
        activate_morale_auto_pass(unit_key, faction)
    elif effect.type == "move" and effect.handler == "fall_back_through_models":
        activate_desperate_breakout(unit_key, faction)
    elif effect.type == "invuln_save" and effect.modifier is not None:
        current_phase = PHASES[st.session_state.get("phase_idx", 0)][1]
        active_mods = st.session_state.get("active_modifiers", [])
        active_mods.append(
            {
                "unit_key": unit_key,
                "source": strat.name_en,
                "effect": {
                    "roll_type": "invuln_save",
                    "value": effect.modifier,
                    "target": "defender",
                    "phase": current_phase,
                },
                "expires_at_phase": current_phase,
                "expires_at_round": None,
            }
        )
        st.session_state.active_modifiers = active_mods


# Effect shapes `_apply_stratagem_effect` (this module) dispatches on `unit_key`
# are unit-scoped by construction — that function has no effect at all without
# a selected unit. `("move", "fall_back_through_models")` (Desperate Breakout)
# carries its own additional per-unit-state conditions beyond "a unit is
# selected" and gets its own branch below; every other type in this set (S142
# Aufgabe 2, Befund 5: `auto_pass_morale`/Insane Bravery — rules_appendix.txt
# see docstring below; `invuln_save` mirrored here for the same reason, though
# it is currently `phase_reactive`-only and never reaches this gate) just
# needs "a unit is selected", nothing more. Add new unit-scoped effect types
# here (or as their own branch if they carry extra per-unit-state conditions)
# — never as a bare `elif` special case.
_UNIT_SCOPED_EFFECT_TYPES = frozenset({"auto_pass_morale", "invuln_save"})


def _effect_gate_met(
    strat: Stratagem, unit_state: dict | None  # type: ignore[type-arg]
) -> tuple[bool, str | None]:
    """Generic unit-state gate for GOs whose effect requires a selected unit.

    Dispatches on `effect.type`/`effect.handler` — the same shape-based dispatch
    `_apply_stratagem_effect` (this module) already uses — rather than a
    stratagem id/name check (INV-4b: no faction- or GO-name string literals in
    src/). `conditions` (keyword-based) is orthogonal and stays in
    `stratagem_conditions_met`; this covers a requirement keywords cannot
    express: the selected unit's own turn state.

    Two forms are checked, both against `_UNIT_SCOPED_EFFECT_TYPES`/the dispatch
    table above:

    - `type="move", handler="fall_back_through_models"` (Desperate Breakout,
      S133-D Befund 4): rules_appendix.txt 2618-2625 — "Select one unit from
      your army that has not been selected to move this phase and which is in
      Engagement Range with at least one enemy unit." `movement_chosen` is the
      same flag `set_movement_status()` sets for every movement declaration;
      `in_melee` is the same field every other "Engagement Range" check in
      this codebase reads (see e.g. movementPhase.py's Retreat-only-in-melee
      gating).
    - Any other type in `_UNIT_SCOPED_EFFECT_TYPES` (e.g. `auto_pass_morale` /
      Insane Bravery, core_rules.txt:3260-3267 — "Use this Stratagem before you
      take a Morale test for a unit in your army"; `conditions: []` in YAML,
      so nothing but this gate enforces "a unit" before the card is offered as
      ready): only requires `unit_state is not None` (S142 Befund 5 — without
      this, the card went "ready" as soon as CP sufficed, and clicking it spent
      CP + marked the GO used without ever calling `activate_morale_auto_pass`,
      because `spend_stratagem` only dispatches the effect when `unit_key is
      not None`).

    Any other effect shape (or no effect) is always gate-met — those GOs have
    no per-unit state requirement beyond `conditions`.
    """
    effect = strat.effect
    if effect is None:
        return True, None
    if effect.type == "move" and effect.handler == "fall_back_through_models":
        if unit_state is None:
            return False, "select an eligible unit"
        if unit_state.get("movement_chosen"):
            return False, "unit already moved this phase"
        if not unit_state.get("in_melee"):
            return False, "unit not in Engagement Range"
        return True, None
    if effect.type in _UNIT_SCOPED_EFFECT_TYPES:
        if unit_state is None:
            return False, "select an eligible unit"
        return True, None
    return True, None


def stratagem_strength_bonus(active_modifiers: list[dict], unit_key: str | None) -> int:
    """Total Strength-characteristic bonus from active stratagem modifiers (e.g. Disruption Fields).

    Mirrors abilityEngine.buff_stat_bonus's role but reads from the generic active_modifiers
    list (StratagemModifier entries via gameProtocoll.py) instead of faction ability effects.

    Scoped to `unit_key` (the attacker's state key): a modifier only counts if it was
    activated for this exact unit. Entries without a matching unit_key (including the
    legacy `unit_key: None`) are ignored — otherwise a stratagem activated for one unit
    (e.g. Disruption Fields on unit X) would buff every attacker's Strength.
    """
    total = 0
    for m in active_modifiers:
        if m.get("unit_key") != unit_key:
            continue
        eff = m.get("effect", {})
        if eff.get("roll_type") == "strength" and eff.get("target", "attacker") in (
            "attacker",
            "any",
        ):
            total += int(eff.get("value", 0))
    return total
