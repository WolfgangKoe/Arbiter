from __future__ import annotations

from collections.abc import Callable, Iterable, Mapping, MutableMapping
from typing import Any

import streamlit as st

from gameMechanic.combat import parse_dice
from gameMechanic.gameState import (
    faction_dir_for,
    round_choice_state_key,
    short_round_choice_label,
    subfaction_value_for,
    units_key_for,
)
from gameMechanic.unitMutations import heal_unit
from gameObjects.ability import Ability
from gameObjects.loader import (
    load_army,
    load_faction_abilities,
    load_round_choice_abilities,
    load_subfaction_abilities,
    load_unit_abilities,
)
from gameObjects.roundChoiceAbility import RoundChoiceAbility
from gameObjects.unit import Unit

# ---------------------------------------------------------------------------
# Timing constants — used by ability triggers and phaseRunner hooks
# ---------------------------------------------------------------------------

TIMING_PHASE_START = "phase_start"
TIMING_PHASE_END = "phase_end"
TIMING_BEFORE_UNIT_ACTS = "before_unit_acts"
TIMING_AFTER_UNIT_ATTACKED = "after_unit_attacked"


def check_trigger(ability: Ability, phase: str, timing: str, active_player: str) -> bool:
    t = ability.trigger
    if t.timing != timing:
        return False
    phase_list = t.phase if isinstance(t.phase, list) else [t.phase]
    if phase not in phase_list:
        return False
    if t.player not in ("either", active_player):
        return False
    return True


def check_conditions(ability: Ability, unit: Unit, unit_state: MutableMapping[str, Any]) -> bool:
    for cond in ability.conditions:
        if cond.unit_not_destroyed and unit_state.get("destroyed", False):
            return False
        if cond.has_rules and not any(r in unit.rules for r in cond.has_rules):
            return False
        if cond.has_keywords:
            unit_kw_upper = {kw.upper() for kw in unit.keywords}
            if not any(kw.upper() in unit_kw_upper for kw in cond.has_keywords):
                return False
        if cond.needs_healing:
            from gameMechanic.unitMutations import unit_max_hp  # noqa: PLC0415

            if unit_state.get("current_wounds", 0) >= unit_max_hp(unit, unit_state):
                return False
        # within_inches: spatial tracking not implemented — always passes
        # max_uses: handled by callers against session state
    return True


def _execute_heal(ability: Ability, uid: str, faction: str, unit: Unit) -> bool:
    hp = int(ability.effect.amount or 1)
    try:
        hp += get_active_heal_bonus(faction, unit)
    except KeyError:
        pass  # no faction-dir in session (e.g. minimal test state) -> no bonus
    return heal_unit(uid, faction, hp, unit, revive=ability.effect.revive)


# Single source of truth for "which effect.type does execute_effect actually apply".
# is_effect_executable() and execute_effect() both read this dict — a new dispatch
# branch here is automatically reflected in is_effect_executable(), no second set
# to keep in sync (armyCard.py must not maintain its own copy of this list).
_EFFECT_HANDLERS: dict[str, Callable[[Ability, str, str, Unit], bool]] = {
    "heal": _execute_heal,
}


def is_effect_executable(effect_type: str) -> bool:
    """True if ``execute_effect`` has a dispatch handler for this effect type."""
    return effect_type in _EFFECT_HANDLERS


def execute_effect(ability: Ability, uid: str, faction: str, unit: Unit) -> bool:
    """Apply ability effect to a unit. Returns True if state actually changed."""
    handler = _EFFECT_HANDLERS.get(ability.effect.type)
    if handler is None:
        return False
    return handler(ability, uid, faction, unit)


# Numeric directive effect types -> the key they contribute in the modifier dict.
# move_bonus: Sudden Storm P (+1" Move).
# Removed (Plan 025 Step 6): hit_modifier, wound_modifier, strength_modifier, ap_bonus
# (no active YAML consumers; migrated to specific effect types).
_MODIFIER_RESULT_KEY = {
    "move_bonus": "move",
}


def _tagged_effect(effect: dict[str, Any], source_id: str) -> dict[str, Any]:
    """Return a shallow copy of *effect* annotated with its source ability id.

    The loader caches effect dicts and shares them across callers, so we must
    copy before adding ``_source_id`` — never mutate the cached original.
    """
    return {**effect, "_source_id": source_id}


def _extra_directive_effects(
    player: str, round_choices: list[RoundChoiceAbility]
) -> list[dict[str, Any]]:
    """Effect dict(s) of the player's always-active 6th round-choice ability.

    The 6th ability is the single one not assigned to any battle round. Its
    directive is stored under the ``extra_directive`` key. When the player's
    subfaction matches the ability's ``subfaction_affinity``, BOTH directives
    apply simultaneously (dynasty bonus) — mirrors the display logic in
    ``armyCard._render_extra_round_choice`` / ``gameState``.

    Each returned dict carries ``_source_id`` so callers can identify which
    round-choice ability the effect originates from (used by badge label resolution).
    """
    assignments = st.session_state.get("round_choice_assignments", {}).get(player, {})
    assigned_ids = set(assignments.values())
    if len(assigned_ids) < 5:
        return []
    extras = [p for p in round_choices if p.id not in assigned_ids]
    if len(extras) != 1:
        return []
    extra = extras[0]
    subfaction = subfaction_value_for(player)
    if subfaction and subfaction == extra.subfaction_affinity:
        return [
            _tagged_effect(extra.primary_effect, extra.id),
            _tagged_effect(extra.secondary_effect, extra.id),
        ]
    extra_directive = st.session_state.get(round_choice_state_key(player, "extra_directive"))
    if extra_directive:
        raw = extra.primary_effect if extra_directive == "primary" else extra.secondary_effect
        return [_tagged_effect(raw, extra.id)]
    return []


def _active_directive_effects(player: str) -> list[dict[str, Any]]:
    """All effect dicts active for the player from round-choice directives.

    Aggregates the round-assigned protocol's chosen directive AND the always-active
    6th protocol's directive (incl. the dynasty bonus where both directives apply).
    State is keyed by the player slot (mirror-match safe); ability definitions load
    via the player's faction directory. Returns ``[]`` for factions without
    round-choice abilities or when nothing is selected (no faction-dir lookup needed).

    Each returned dict carries ``_source_id`` identifying the source round-choice
    ability, enabling callers to resolve the correct badge label (e.g. via
    ``get_short_label_for_effect_type``).
    """
    active_id: str | None = st.session_state.get(round_choice_state_key(player, "active"))
    directive: str | None = st.session_state.get(round_choice_state_key(player, "directive"))
    assignments = st.session_state.get("round_choice_assignments", {}).get(player, {})
    has_round = bool(active_id)
    has_extra_setup = len({*assignments.values()}) >= 5
    if not has_round and not has_extra_setup:
        return []

    round_choices = load_round_choice_abilities(faction_dir_for(player))
    if not round_choices:
        return []

    effects: list[dict[str, Any]] = []
    if has_round:
        active = next((p for p in round_choices if p.id == active_id), None)
        if active:
            subfaction = subfaction_value_for(player)
            if subfaction and subfaction == active.subfaction_affinity:
                effects.append(_tagged_effect(active.primary_effect, active.id))
                effects.append(_tagged_effect(active.secondary_effect, active.id))
            elif directive:
                raw = active.primary_effect if directive == "primary" else active.secondary_effect
                effects.append(_tagged_effect(raw, active.id))
    effects.extend(_extra_directive_effects(player, round_choices))
    return [e for e in effects if e]


def _directive_phase_excluded(effect: dict[str, Any], use_melee: bool) -> bool:
    """True if the directive's phase does not apply in the given melee/ranged context."""
    effect_phase = effect.get("phase", "any")
    if effect_phase == "shooting" and use_melee:
        return True
    if effect_phase == "melee" and not use_melee:
        return True
    return False


def _sum_effect_value(
    effects: Iterable[dict[str, Any]],
    effect_type: str,
    *,
    type_key: str = "type",
    value_key: str = "value",
    missing_value: int | None = 0,
    predicate: Callable[[dict[str, Any]], bool] | None = None,
    combine: Callable[[int, int], int] = lambda total, value: total + value,
) -> int | None:
    """Fold ``value_key`` across effect dicts whose ``type_key`` equals *effect_type*.

    Shared accumulate step behind the "filter effects by type [+ predicate],
    fold value_key via combine" pattern repeated across
    ``get_active_round_choice_strength_if_charged``,
    ``get_active_round_choice_ap_on_wound_6``, ``get_active_heal_bonus``,
    ``buff_stat_bonus``, ``ability_invuln_save`` (this module) and
    ``stratagemEngine.stratagem_strength_bonus``.

    *combine* seeds from the first match rather than a fixed 0 baseline, so
    ``combine=min`` (``ability_invuln_save``) isn't skewed low by a spurious
    zero. Returns ``None`` when nothing matched. *missing_value* is the
    fallback for effects missing (or holding an explicit ``None``) at
    ``value_key`` — pass ``None`` (as ``ability_invuln_save`` does) to skip
    such effects instead of counting them as 0.
    """
    total: int | None = None
    for effect in effects:
        if effect.get(type_key) != effect_type:
            continue
        if predicate is not None and not predicate(effect):
            continue
        raw = effect.get(value_key, missing_value)
        if raw is None:
            continue
        value = int(raw)
        total = value if total is None else combine(total, value)
    return total


def get_active_round_choice_modifier(player: str, phase: str, use_melee: bool) -> dict[str, int]:
    """Return numeric modifiers from the active round-choice ability's chosen directive.

    Only numeric effect types in _MODIFIER_RESULT_KEY are returned (currently only move_bonus).
    Non-numeric effects (advance_and_charge, rp_reroll, etc.) are queried via dedicated
    functions and are silently skipped here.

    Returns a dict with any of: {"move"} mapped to int. Effects from multiple active
    directives (round-assigned plus the always-active 6th / dynasty protocol) accumulate per key.
    """
    result: dict[str, int] = {}
    for effect in _active_directive_effects(player):
        effect_type = effect.get("type", "")
        key = _MODIFIER_RESULT_KEY.get(effect_type)
        if not key:
            continue
        if _directive_phase_excluded(effect, use_melee):
            continue
        result[key] = result.get(key, 0) + effect.get("value", 0)
    return result


def get_active_round_choice_strength_if_charged(
    player: str, turn_flags: dict[str, bool], use_melee: bool
) -> int:
    """+N Strength from a ``strength_if_charged`` directive (Hungry Void D2, melee).

    Class A: the App computes it. Fires only when the attacking unit made a charge
    move, was charged, or performed a Heroic Intervention this turn (9E wording).
    The charge condition is read from the attacker's ``turn_flags`` so the rule
    lives in one tested place. Returns 0 in shooting or when no such directive is
    active. Sums across every active directive (round-assigned + 6th / dynasty).
    """
    if not use_melee:
        return 0
    charged = turn_flags.get("charged") or turn_flags.get("was_charged")
    if not (charged or turn_flags.get("heroic_intervened")):
        return 0
    return (
        _sum_effect_value(
            _active_directive_effects(player),
            "strength_if_charged",
            predicate=lambda effect: not _directive_phase_excluded(effect, use_melee),
        )
        or 0
    )


def get_active_round_choice_ap_on_wound_6(player: str, use_melee: bool) -> int:
    """AP improvement applied on an unmodified wound roll of 6 (Hungry Void D1, melee).

    Class B: combat is count-based (the App never sees individual dice faces), so
    the per-die effect is applied at the table — this drives the ``[AP-N]``-on-6
    display row only. Returns the AP magnitude (e.g. 1) or 0 when no such directive
    is active or the phase does not match. Sums across every active directive.
    """
    return (
        _sum_effect_value(
            _active_directive_effects(player),
            "ap_on_unmod_wound_6",
            predicate=lambda effect: not _directive_phase_excluded(effect, use_melee),
        )
        or 0
    )


def _active_directive_has_type(player: str, effect_type: str) -> bool:
    """True if any active round-choice directive has the given effect type."""
    return any(e.get("type") == effect_type for e in _active_directive_effects(player))


def get_active_round_choice_ignores_cover_half_range(player: str) -> bool:
    """True if an active directive negates the target's Light Cover within half range.

    Vengeful Stars D2, ranged (9E). Class B/hybrid: half-range is a table measurement,
    so the App only surfaces the hint inline — the player still toggles Light Cover
    manually. Returns False when no such directive is active (regardless of phase,
    because the firing model must confirm half-range at the table anyway).
    """
    return _active_directive_has_type(player, "ignore_cover_half_range")


def get_active_round_choice_light_cover_if_stationary(def_player: str, def_uid: str) -> bool:
    """True if the defending unit benefits from Light Cover (Eternal Guardian D1):
    directive active AND unit did not move this battle round (movement_choice == 'stationary').

    Class A — the App grants Light Cover automatically. Aggregates round-assigned AND
    always-active 6th/dynasty directive via _active_directive_effects (same pattern as
    get_active_round_choice_ignores_cover_half_range).
    """
    if not _active_directive_has_type(def_player, "light_cover_if_stationary"):
        return False
    state: dict[str, Any] = st.session_state.get(units_key_for(def_player), {}).get(def_uid, {})
    return state.get("movement_choice") == "stationary"


def get_active_round_choice_shoot_after_fall_back(atk_player: str, atk_uid: str) -> int:
    """Hit modifier from Conquering Tyrant D2 (shoot_after_fall_back) when active.

    Class A: returns −1 (as a negative int) when the directive is active AND the
    attacking unit's movement_choice == 'retreated'. Returns 0 otherwise.

    9E rule: "This unit is eligible to shoot in a turn in which it Fell Back, but if
    it does, then until the end of the turn, each time a model in this unit makes a
    ranged attack, subtract 1 from that attack's hit roll."
    """
    if not _active_directive_has_type(atk_player, "shoot_after_fall_back"):
        return 0
    state = st.session_state.get(units_key_for(atk_player), {}).get(atk_uid, {})
    if state.get("movement_choice") != "retreated":
        return 0
    effects = _active_directive_effects(atk_player)
    return sum(
        e.get("hit_modifier", 0) for e in effects if e.get("type") == "shoot_after_fall_back"
    )


def get_short_label_for_effect_type(player: str, effect_type: str) -> str | None:
    """Short protocol name for the first active directive effect matching *effect_type*.

    Resolves the label from the effect's ``_source_id`` (set by
    ``_active_directive_effects`` / ``_extra_directive_effects``) rather than
    always reading the round-assigned ``active`` slot.  This ensures the badge
    label reflects the *actual* source protocol — e.g. Vengeful Stars when it
    is the always-active 6th protocol rather than the round-assigned one.

    Returns ``None`` when no active directive has the requested effect type
    (callers should fall back to their previous behaviour in that case).
    """
    round_choices = load_round_choice_abilities(faction_dir_for(player))
    by_id = {p.id: p for p in round_choices}
    for effect in _active_directive_effects(player):
        if effect.get("type") != effect_type:
            continue
        source_id = effect.get("_source_id")
        ability = by_id.get(source_id) if source_id else None
        if ability:
            return short_round_choice_label(ability.name_en)
    return None


def get_active_protocol_effects(player: str, types: set[str]) -> list[dict[str, Any]]:
    """Raw effect dicts of the active directive(s) whose type is in *types*.

    Includes the dynasty protocol's BOTH directives when the subfaction affinity
    matches (6th-protocol rule, Bug-3 fix). Generic: works for any faction with
    round_choice abilities. Returns ``[]`` when nothing matches or no protocol
    is active.

    Each returned dict carries ``_source_id`` for label resolution via
    ``get_short_label_for_effect_type``.
    """
    return [e for e in _active_directive_effects(player) if e.get("type") in types]


def get_active_rp_modifiers(player: str) -> dict[str, int | bool]:
    """Return Reanimation Protocol modifiers from the active round-choice directive.

    Undying Legions P (rp_reroll) -> {"rp_reroll": True}
    Any other / no directive      -> {}

    Delegates to ``get_active_protocol_effects`` so dynasty/6th-protocol
    effects are included automatically.
    """
    if get_active_protocol_effects(player, {"rp_reroll"}):
        return {"rp_reroll": True}
    return {}


def get_unit_rp_reroll_ability(
    faction: str,
    unit: Unit,
    unit_state: MutableMapping[str, Any],
) -> Ability | None:
    """The unit's own Reanimation-Protocol reroll ability, or None (data-driven).

    Generic INV-4b seam: a unit carries a persistent ability declared in its
    faction's unit_abilities.yaml with ``effect.type: reroll_rp`` (e.g. Necron
    Their Number is Legion: re-roll unmodified Reanimation Protocol rolls of
    1). The gating rule key (e.g. ``theirNumberIsLegion``) is a YAML-declared
    ``has_rules`` condition, checked via ``check_conditions`` — src/ knows only
    this generic effect shape, never the faction-specific rule name.

    Distinct from ``get_active_rp_modifiers`` (round-choice directive path,
    e.g. Undying Legions P) — the two are independent sources and can both
    apply to the same unit at once.
    """
    try:
        faction_dir = faction_dir_for(faction)
    except KeyError:
        return None
    for ability in load_unit_abilities(faction_dir):
        if ability.effect.type != "reroll_rp":
            continue
        if check_conditions(ability, unit, unit_state):
            return ability
    return None


def _hit_reroll_ones_ability(
    faction: str,
    unit: Unit,
    unit_state: MutableMapping[str, Any],
) -> Ability | None:
    """The unit's own "re-roll a hit roll of 1" ability, or None (data-driven).

    Generic INV-4b seam (B-113 Teil A): a unit carries this via a persistent
    ``reroll_hit`` effect with ``modifier: 1`` and ``target: self`` — e.g.
    Necron Destroyer Cult "Hardwired for Destruction": "Each time a model in
    this unit makes an attack, re-roll a hit roll of 1"
    (data/wh40k_9e/necrons/subfaction_abilities.yaml). The gating rule key
    (e.g. ``hardwiredForDestruction``) is a YAML-declared ``has_rules``
    condition, checked via ``check_conditions`` — src/ knows only this
    generic effect shape, never the faction/unit-specific rule name.

    Checked against both ``load_unit_abilities`` and ``load_subfaction_abilities``
    since a ``reroll_hit`` ability may live in either file. ``modifier == 1``
    and ``target == "self"`` distinguish this narrow "re-roll unmodified 1s"
    reading from the differently-shaped full-reroll ``reroll_hit`` aura (e.g.
    Phaeron of the Stars: "you can re-roll the hit roll", no ``modifier``,
    ``target`` an aura label) — that full-reroll shape is not consumed here.
    """
    try:
        faction_dir = faction_dir_for(faction)
    except KeyError:
        return None
    candidates = load_unit_abilities(faction_dir) + load_subfaction_abilities(faction_dir)
    for ability in candidates:
        effect = ability.effect
        if effect.type != "reroll_hit" or effect.modifier != 1 or effect.target != "self":
            continue
        if check_conditions(ability, unit, unit_state):
            return ability
    return None


def unit_hit_reroll_ones(
    faction: str,
    unit: Unit,
    unit_state: MutableMapping[str, Any],
) -> bool:
    """True if *unit* re-rolls unmodified hit rolls of 1 (e.g. Hardwired for Destruction).

    → ``_hit_reroll_ones_ability`` for the matching-ability lookup. Consumed by
    ``combat.resolve_attack_modifiers`` (``hit_reroll_ones`` param) to mark the
    reroll-eligible slot in the HIT dice block (``reroll_marker_row_html``).
    """
    return _hit_reroll_ones_ability(faction, unit, unit_state) is not None


def _aura_source_alive(source_unit_id: str, units_state: Mapping[str, Any]) -> bool:
    """True if *source_unit_id* has a non-destroyed instance in *units_state*.

    Instance keys carry a ``#N`` duplicate suffix for a second+ copy of the same
    catalog unit in one roster (``gameState._make_unit_state_dict``), so an
    exact-key match alone would miss "Skorpekh Lord #2" — matched by prefix
    instead (rules_appendix.txt "Aura Abilities": "A model with an aura ability
    is always within range of its effect", B-113 Teil B).
    """
    for key, state in units_state.items():
        if (key == source_unit_id or key.startswith(f"{source_unit_id}#")) and not state.get(
            "destroyed", False
        ):
            return True
    return False


def _wound_reroll_ones_aura_ability(
    faction: str,
    unit: Unit,
    unit_state: MutableMapping[str, Any],
) -> Ability | None:
    """The wound-reroll-1 AURA ability affecting *unit* from an allied source, or None.

    Generic INV-4b seam (B-113 Teil B): unlike ``_hit_reroll_ones_ability``
    (a unit buffs itself, ``target: self``), this is an AURA — one unit (a
    Lord) carries the persistent ``reroll_wound_1`` effect
    (``target != "self"``, e.g. Necron Destroyer Cult "United in Destruction":
    "re-roll a wound roll of 1") and it applies to every OTHER eligible friendly
    unit in the same roster, gated by the ability's own YAML ``has_keywords``
    condition (e.g. DESTROYER CULT) checked against *unit* via
    ``check_conditions`` — src/ never names a keyword or unit id.

    Aura range ("within 6\"") has no spatial model in this app (no battlefield
    positions are tracked); consistent with ``check_conditions``'s existing
    no-op ``within_inches`` handling, the aura is treated as active whenever
    its source unit is alive (``_aura_source_alive``) — matching
    rules_appendix.txt "Aura Abilities": "A model with an aura ability is
    always within range of its effect" for the degenerate same-unit case, and
    left un-enforced for cross-unit range like every other aura target already
    declared in unit_abilities.yaml (e.g. ``friendly_core_aura_6``).
    """
    try:
        faction_dir = faction_dir_for(faction)
    except KeyError:
        return None
    candidates = [
        a
        for a in load_unit_abilities(faction_dir) + load_subfaction_abilities(faction_dir)
        if a.effect.type == "reroll_wound_1" and a.effect.target != "self"
    ]
    if not candidates:
        return None
    units_state: Mapping[str, Any] = st.session_state.get(units_key_for(faction), {})
    for ability in candidates:
        if ability.unit_id and not _aura_source_alive(ability.unit_id, units_state):
            continue
        if check_conditions(ability, unit, unit_state):
            return ability
    return None


def unit_wound_reroll_ones(
    faction: str,
    unit: Unit,
    unit_state: MutableMapping[str, Any],
) -> bool:
    """True if *unit* re-rolls unmodified wound rolls of 1 via an allied aura
    (e.g. Necron Destroyer Cult Lord "United in Destruction").

    → ``_wound_reroll_ones_aura_ability`` for the matching-ability lookup.
    Consumed by ``combat.resolve_attack_modifiers`` (``wound_reroll_ones``
    param) to mark the reroll-eligible slot in the WOUND dice block
    (``reroll_marker_row_html``).
    """
    return _wound_reroll_ones_aura_ability(faction, unit, unit_state) is not None


def get_after_attack_revive_ability(
    faction: str,
    unit: Unit,
    unit_state: MutableMapping[str, Any],
) -> Ability | None:
    """The unit's revive-after-enemy-attack ability, or None (data-driven).

    Generic INV-4b seam: a faction declares a triggered ability with
    ``effect.type: reanimate`` and ``trigger.event: after_enemy_attack`` in its
    faction_abilities.yaml (e.g. Necron Reanimation Protocols). Label
    (``name_en``), dice formula (``effect.amount``) and success threshold
    (``effect.success_on``) come from that YAML entry — src/ knows only this
    generic shape. Conditions (rule key, unit not destroyed) are checked
    against the YAML-declared conditions via ``check_conditions``.
    """
    try:
        faction_dir = faction_dir_for(faction)
    except KeyError:
        return None
    for ability in load_faction_abilities(faction_dir):
        if ability.effect.type != "reanimate":
            continue
        if ability.trigger.event != "after_enemy_attack":
            continue
        if check_conditions(ability, unit, unit_state):
            return ability
    return None


def revive_dice_count(amount: str | None, models_lost: int, wounds_per_model: int) -> int:
    """Dice granted by a revive ability's ``amount`` formula.

    ``"D6_per_wound"`` → one die per wound of the destroyed models (e.g. 9E
    Reanimation Protocols: models_lost × wounds per model). Any other or
    missing formula → one die per destroyed model.
    """
    if amount == "D6_per_wound":
        return models_lost * wounds_per_model
    return models_lost


def get_active_heal_bonus(player: str, unit: Unit) -> int:
    """Extra wounds healed from an active directive's ``heal_bonus`` effect.

    The directive names its target ability data-driven via ``target_rule``
    (e.g. Undying Legions S -> Living Metal). Generic: any faction/directive
    with a ``heal_bonus`` effect applies when the healed unit carries the
    matching rule. Returns 0 when no such directive is active or the rule
    does not match. Sums across every active directive (round-assigned plus the
    always-active 6th / dynasty protocol).
    """
    return (
        _sum_effect_value(
            _active_directive_effects(player),
            "heal_bonus",
            predicate=lambda effect: not effect.get("target_rule")
            or effect.get("target_rule") in unit.rules,
        )
        or 0
    )


def _unit_matches_target(unit: Unit, effect: dict[str, Any]) -> bool:
    """True if unit satisfies the effect's target_keywords / target_keywords_any constraints."""
    required = effect.get("target_keywords", [])
    any_of = effect.get("target_keywords_any", [])
    if any(not unit.has_keyword(kw) for kw in required):
        return False
    if any_of and not any(unit.has_keyword(kw) for kw in any_of):
        return False
    return True


def _active_effects_for_faction(faction: str) -> list[dict[str, Any]]:
    """Raw sub-effect dicts from the faction's currently activated ability, if any."""
    entry = st.session_state.get("activated_abilities", {}).get(faction)
    if not entry:
        return []
    ability_id: str | None = entry.get("ability_id")
    if not ability_id:
        return []
    abilities = load_faction_abilities(faction_dir_for(faction))
    ability = next((a for a in abilities if a.id == ability_id), None)
    if not ability or ability.effect.type != "multi":
        return []
    return ability.effect.effects or []


def buff_stat_bonus(faction: str, unit: Unit, stat: str) -> int:
    """Total modifier for a stat from all active faction abilities matching this unit."""
    return (
        _sum_effect_value(
            _active_effects_for_faction(faction),
            "buff_stat",
            value_key="modifier",
            predicate=lambda eff: eff.get("stat") == stat and _unit_matches_target(unit, eff),
        )
        or 0
    )


# stratagem_strength_bonus moved to gameMechanic.stratagemEngine (S142 Aufgabe
# 1, Option B — consolidated stratagem-effect dispatch).


def ability_invuln_save(faction: str, unit: Unit) -> int | None:
    """Best invuln save granted by active faction abilities for this unit, or None."""
    return _sum_effect_value(
        _active_effects_for_faction(faction),
        "invuln_save",
        value_key="modifier",
        missing_value=None,
        predicate=lambda eff: _unit_matches_target(unit, eff),
        combine=min,
    )


def _wound_auto_fail_ability(faction: str, unit: Unit) -> Ability | None:
    """Ability granting the highest ``wound_auto_fail`` threshold for *unit*, or None.

    Reads persistent unit abilities (``unit_abilities.yaml``) whose effect type is
    ``wound_auto_fail`` and whose ``has_rules`` condition matches one of *unit*'s
    intrinsic rules — e.g. Necron Quantum Shielding: "an unmodified wound roll of
    1-3 always fails, irrespective of any abilities that the weapon or the
    attacker may have" (docs/work/wahapedia_necrons/units_all.txt:112). Generic
    dispatch on ``effect.type`` (INV-4b: no faction string here, the rule tag
    lives in YAML). Combined via max in the unlikely case more than one such
    ability applies to the same unit.
    """
    best: Ability | None = None
    best_value = -1
    for ability in load_unit_abilities(faction_dir_for(faction)):
        if ability.effect.type != "wound_auto_fail":
            continue
        if not check_conditions(ability, unit, {}):
            continue
        value = ability.effect.modifier
        if value is None:
            continue
        if value > best_value:
            best_value = value
            best = ability
    return best


def unit_wound_auto_fail_max(faction: str, unit: Unit) -> int | None:
    """Highest unmodified wound roll that always fails against *unit*, or None.

    ``effect.modifier`` carries the top of the auto-fail range (3 for Quantum
    Shielding). → ``_wound_auto_fail_ability`` for the matching-ability lookup.
    """
    ability = _wound_auto_fail_ability(faction, unit)
    return ability.effect.modifier if ability else None


def unit_wound_auto_fail_label(faction: str, unit: Unit) -> str | None:
    """Badge label for the active ``wound_auto_fail`` ability, or None.

    Read from ``badge_label`` (falling back to ``name_en``) — no hardcoded
    faction text here (B-103: the UI badge must show e.g. "Quantum Shielding",
    not a generic "Auto-fail" placeholder). ``loader.load_unit_abilities``
    rejects any ``wound_auto_fail`` ability with neither field set (B-109), so
    when an ability is found here the returned label is always non-empty.
    """
    ability = _wound_auto_fail_ability(faction, unit)
    if ability is None:
        return None
    return ability.badge_label or ability.name_en


def find_unit_ability_by_effect(faction_dir: str, unit_id: str, effect_type: str) -> Ability | None:
    """Return *unit_id*'s own unit_ability with ``effect.type == effect_type``, or None.

    Ownership match (``ability.unit_id == unit_id``), unlike
    ``_wound_auto_fail_ability``'s conditions/keyword match — reactive
    unit-owned abilities such as Noctilith Beacons (deny_psychic) carry no
    ``has_rules``/``has_keywords`` condition of their own (an empty
    ``conditions: []`` matches unconditionally), so ownership is the only
    thing that scopes the ability to the right unit. ``faction_dir`` is the
    raw data-directory name (e.g. "necrons"), matching ``load_unit_abilities``'s
    own parameter — callers that only have a unit id (not a player identity,
    e.g. ``psychicPhase.can_deny()``) derive it via ``unit_id.split(".")[1]``.
    """
    for ability in load_unit_abilities(faction_dir):
        if ability.unit_id == unit_id and ability.effect.type == effect_type:
            return ability
    return None


# Known ``target`` labels for a ``mortal_wounds`` unit_ability effect (B-028c1).
# Spatial resolution ("which units are within 2D6\"") is left to the caller/UI —
# this app has no positional battlefield model, so the target stays a data-driven
# label rather than a set of resolved unit ids. Kept as a single generic set here
# (not per-caller re-enumerated) so a YAML typo fails loudly via mortal_wounds_target().
_MORTAL_WOUNDS_TARGETS = frozenset(
    {
        "self",
        "attacker",
        "closest_enemy_within_6",
        "units_within_2d6",
        "enemy_units_within_1",
    }
)


def mortal_wounds_target(ability: Ability) -> str:
    """Validated ``target`` label of a ``mortal_wounds`` ability effect.

    Raises ``ValueError`` for a target outside ``_MORTAL_WOUNDS_TARGETS`` so an
    unrecognised/typo'd YAML value fails loudly instead of silently resolving
    to no targets. Callers (T2 call-sites) map the returned label to the actual
    unit(s) it applies to — that resolution is UI/game-state work, not this
    module's concern.
    """
    target = ability.effect.target
    if target not in _MORTAL_WOUNDS_TARGETS:
        raise ValueError(f"Unknown mortal_wounds target: {target!r}")
    return target


def resolve_mortal_wounds_effect(ability: Ability, *, trigger_met: bool | None = None) -> int:
    """Roll (or accept an externally-resolved) trigger and return mortal wounds inflicted.

    Generic dispatch for ``effect.type: mortal_wounds`` (B-028c1) — reads the
    YAML-declared ``roll_threshold``/``roll_type``/``amount`` fields, no
    faction-specific logic. Two trigger sources, selected by ``effect.roll_type``:

    - unset (e.g. Vengeance of the Enchained, Infused Madness, Wrath of the
      Seraptek): this function rolls one D6 itself via ``combat.parse_dice`` and
      compares it against ``effect.roll_threshold`` ("on a 4+").
    - ``"unmodified_hit_1"`` (e.g. Arc Fields): the trigger already happened at
      the table during an attack's hit roll — this app resolves combat by
      count, not individual dice faces (Class B, same reasoning as
      ``get_active_round_choice_ap_on_wound_6``), so the caller passes the
      already-known result via *trigger_met* instead of a fresh roll.

    Returns the number of mortal wounds inflicted (0 if untriggered).
    ``effect.amount`` ("1", "D3", "D6") is parsed via ``combat.parse_dice``.
    """
    effect = ability.effect
    if effect.roll_type:
        triggered = bool(trigger_met)
    else:
        threshold = effect.roll_threshold or 0
        triggered = parse_dice("D6") >= threshold
    if not triggered:
        return 0
    return parse_dice(effect.amount or "1")


def resolve_explode_effect(ability: Ability, *, exploded: bool) -> bool:
    """Apply an already-resolved Explodes-family destruction trigger.

    Generic dispatch for ``effect.type: explode`` (Explodes-Familie /
    Pflicht-Trigger, B-028c1 b1) — deliberately contains **no** dice roll of
    any kind ("App würfelt nicht", §6.3/§7 ``design_system.md``): both the
    D6 gate roll ("on a 4+ it explodes") and the per-target mortal-wound
    amount happen physically at the table. ``exploded`` carries the gate
    outcome the player already rolled and entered (mockup V3 Auflage 4 —
    two buttons "Explodes!" / "Does not explode", per → `docs/spec/processes.md` §P-16,
    rather than the exact D6 face). The mortal-wound
    COUNT per affected unit is entered directly per target by the caller
    (``unitMutations.apply_mortal_wounds``) — this function never parses
    ``effect.damage`` via ``combat.parse_dice`` the way
    ``resolve_mortal_wounds_effect`` parses ``effect.amount``, because that
    would mean the app rolling the damage itself instead of the player.

    Raises ``ValueError`` if called on a non-``explode`` ability (wiring
    bug — fail loudly rather than silently no-op on the wrong ability).
    Returns ``exploded`` unchanged; kept as a named function (rather than
    inlining ``if exploded:`` at each call-site) so every b2 call-site shares
    one seam and the type-check guard, matching this module's existing thin
    dispatch style (e.g. ``mortal_wounds_target``).
    """
    if ability.effect.type != "explode":
        raise ValueError(
            f"resolve_explode_effect called on ability {ability.id!r} with "
            f"effect.type {ability.effect.type!r}, expected 'explode'."
        )
    return exploded


def ability_badge_label(faction: str, unit: Unit) -> str | None:
    """Badge label from the active faction ability if this unit benefits, else None.

    The label is read from the ability's badge_label field in YAML — no hardcoded strings.
    """
    entry = st.session_state.get("activated_abilities", {}).get(faction)
    if not entry:
        return None
    ability_id: str | None = entry.get("ability_id")
    if not ability_id:
        return None
    abilities = load_faction_abilities(faction_dir_for(faction))
    ability = next((a for a in abilities if a.id == ability_id), None)
    if not ability or not ability.badge_label:
        return None
    effects = ability.effect.effects or []
    if effects and not any(_unit_matches_target(unit, eff) for eff in effects):
        return None
    return ability.badge_label


def charge_after_advance_allowed(faction: str, unit: Unit) -> bool:
    """True if an active faction ability or round-choice directive permits charging
    after advancing for this unit.

    Two sources: a per-unit activated ability (charge_after_advance effect) or the
    army-wide active round-choice directive (advance_and_charge). The directive branch
    is generic; no shipped protocol currently grants it (Sudden Storm S was corrected
    to its canonical 9E directive in Plan 025).
    """
    if any(
        eff.get("type") == "charge_after_advance" and _unit_matches_target(unit, eff)
        for eff in _active_effects_for_faction(faction)
    ):
        return True
    return _active_directive_has_type(faction, "advance_and_charge")


def get_activated_command_abilities(unit_id: str, faction_dir: str) -> list[Ability]:
    """Return all activated command-phase abilities for a specific unit."""
    all_abilities = load_unit_abilities(faction_dir)
    result = []
    for a in all_abilities:
        if a.ability_type != "activated":
            continue
        if a.unit_id != unit_id:
            continue
        phases = a.trigger.phase if isinstance(a.trigger.phase, list) else [a.trigger.phase]
        if "command" in phases:
            result.append(a)
    return result


def get_triggered_abilities(
    state: MutableMapping[str, Any],
    phase: str,
    timing: str,
) -> list[tuple[Ability, list[str]]]:
    active: str = state.get("active", state.get("first_player", ""))
    faction_dir = faction_dir_for(active)

    all_abilities: list[Ability] = []
    all_abilities.extend(load_faction_abilities(faction_dir))
    all_abilities.extend(load_unit_abilities(faction_dir))
    all_abilities.extend(load_subfaction_abilities(faction_dir))

    units_key = units_key_for(active)
    units_state: MutableMapping[str, Any] = state.get(units_key, {})

    units, _ = load_army(faction_dir)
    unit_by_id = {u.id: u for u in units}

    result: list[tuple[Ability, list[str]]] = []
    for ability in all_abilities:
        if not check_trigger(ability, phase, timing, "active"):
            continue
        eligible: list[str] = [
            uid
            for uid, ustate in units_state.items()
            if (unit := unit_by_id.get(uid)) is not None and check_conditions(ability, unit, ustate)
        ]
        if eligible:
            result.append((ability, eligible))

    return result
