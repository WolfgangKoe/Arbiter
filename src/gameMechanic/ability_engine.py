from __future__ import annotations

import streamlit as st

from gameMechanic.game_state import (
    faction_dir_for,
    round_choice_state_key,
    short_round_choice_label,
    subfaction_value_for,
    units_key_for,
)
from gameMechanic.unit_mutations import heal_unit
from gameObjects.ability import Ability
from gameObjects.loader import (
    load_army,
    load_faction_abilities,
    load_round_choice_abilities,
    load_subfaction_abilities,
    load_unit_abilities,
)
from gameObjects.unit import Unit

# ---------------------------------------------------------------------------
# Timing constants — used by ability triggers and phase_runner hooks
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


def check_conditions(ability: Ability, unit: Unit, unit_state: dict) -> bool:  # type: ignore[type-arg]
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
            from gameMechanic.unit_mutations import unit_max_hp  # noqa: PLC0415

            if unit_state.get("current_wounds", 0) >= unit_max_hp(unit, unit_state):
                return False
        # within_inches: spatial tracking not implemented — always passes
        # max_uses: handled by callers against session state
    return True


def execute_effect(ability: Ability, uid: str, faction: str, unit: Unit) -> bool:
    """Apply ability effect to a unit. Returns True if state actually changed."""
    if ability.effect.type == "heal":
        hp = int(ability.effect.amount or 1)
        try:
            hp += get_active_heal_bonus(faction, unit)
        except KeyError:
            pass  # no faction-dir in session (e.g. minimal test state) -> no bonus
        return heal_unit(uid, faction, hp, unit, revive=ability.effect.revive)
    return False


# Numeric directive effect types -> the key they contribute in the modifier dict.
# move_bonus: Sudden Storm P (+1" Move).
# Removed (Plan 025 Step 6): hit_modifier, wound_modifier, strength_modifier, ap_bonus
# (no active YAML consumers; migrated to specific effect types).
_MODIFIER_RESULT_KEY = {
    "move_bonus": "move",
}


def _tagged_effect(effect: dict, source_id: str) -> dict:  # type: ignore[type-arg]
    """Return a shallow copy of *effect* annotated with its source ability id.

    The loader caches effect dicts and shares them across callers, so we must
    copy before adding ``_source_id`` — never mutate the cached original.
    """
    return {**effect, "_source_id": source_id}


def _extra_directive_effects(player: str, round_choices: list) -> list[dict]:  # type: ignore[type-arg]
    """Effect dict(s) of the player's always-active 6th round-choice ability.

    The 6th ability is the single one not assigned to any battle round. Its
    directive is stored under the ``extra_directive`` key. When the player's
    subfaction matches the ability's ``subfaction_affinity``, BOTH directives
    apply simultaneously (dynasty bonus) — mirrors the display logic in
    ``armyCard._render_extra_round_choice`` / ``game_state``.

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


def _active_directive_effects(player: str) -> list[dict]:  # type: ignore[type-arg]
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
    has_round = bool(active_id and directive)
    has_extra_setup = len({*assignments.values()}) >= 5
    if not has_round and not has_extra_setup:
        return []

    round_choices = load_round_choice_abilities(faction_dir_for(player))
    if not round_choices:
        return []

    effects: list[dict] = []  # type: ignore[type-arg]
    if has_round:
        active = next((p for p in round_choices if p.id == active_id), None)
        if active:
            raw = active.primary_effect if directive == "primary" else active.secondary_effect
            effects.append(_tagged_effect(raw, active.id))
    effects.extend(_extra_directive_effects(player, round_choices))
    return [e for e in effects if e]


def _directive_phase_excluded(effect: dict, use_melee: bool) -> bool:  # type: ignore[type-arg]
    """True if the directive's phase does not apply in the given melee/ranged context."""
    effect_phase = effect.get("phase", "any")
    if effect_phase == "shooting" and use_melee:
        return True
    if effect_phase == "melee" and not use_melee:
        return True
    return False


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


# Reroll-directive effect type -> the reroll flags it grants.
# reroll_save_1 removed: Eternal Guardian S is now hold_steady_or_set_to_defend (Plan 025 Step 4).
# reroll_hit_wound_1 removed: Conquering Tyrant S is now shoot_after_fall_back (Plan 025 Step 5).
_REROLL_DIRECTIVE_FLAGS: dict[str, set[str]] = {}


def get_active_round_choice_rerolls(player: str, phase: str, use_melee: bool) -> set[str]:
    """Return reroll flags from the active round-choice directive (may be empty).

    Separate from get_active_round_choice_modifier because rerolls are flags, not
    numeric modifiers — keeping the dict[str, int] contract of that function clean.
    Flags: reroll_hit_1, reroll_wound_1. Unions the flags of every active directive
    (round-assigned plus the always-active 6th / dynasty protocol).
    """
    flags: set[str] = set()
    for effect in _active_directive_effects(player):
        granted = _REROLL_DIRECTIVE_FLAGS.get(effect.get("type", ""))
        if not granted:
            continue
        if _directive_phase_excluded(effect, use_melee):
            continue
        flags |= granted
    return flags


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
    return sum(
        effect.get("value", 0)
        for effect in _active_directive_effects(player)
        if effect.get("type") == "strength_if_charged"
        and not _directive_phase_excluded(effect, use_melee)
    )


def get_active_round_choice_ap_on_wound_6(player: str, use_melee: bool) -> int:
    """AP improvement applied on an unmodified wound roll of 6 (Hungry Void D1, melee).

    Class B: combat is count-based (the App never sees individual dice faces), so
    the per-die effect is applied at the table — this drives the ``[AP-N]``-on-6
    display row only. Returns the AP magnitude (e.g. 1) or 0 when no such directive
    is active or the phase does not match. Sums across every active directive.
    """
    return sum(
        effect.get("value", 0)
        for effect in _active_directive_effects(player)
        if effect.get("type") == "ap_on_unmod_wound_6"
        and not _directive_phase_excluded(effect, use_melee)
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
    state = st.session_state.get(units_key_for(def_player), {}).get(def_uid, {})
    return state.get("movement_choice") == "stationary"


def get_active_round_choice_shoot_after_fall_back(atk_player: str, atk_uid: str) -> int:
    """Hit modifier from Conquering Tyrant D2 (shoot_after_fall_back) when active.

    Class A: returns −1 (as a negative int) when the directive is active AND the
    attacking unit's movement_choice == 'fall_back'. Returns 0 otherwise.

    9E rule: "This unit is eligible to shoot in a turn in which it Fell Back, but if
    it does, then until the end of the turn, each time a model in this unit makes a
    ranged attack, subtract 1 from that attack's hit roll."
    """
    if not _active_directive_has_type(atk_player, "shoot_after_fall_back"):
        return 0
    state = st.session_state.get(units_key_for(atk_player), {}).get(atk_uid, {})
    if state.get("movement_choice") != "fall_back":
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


def get_active_rp_modifiers(player: str) -> dict[str, int | bool]:
    """Return Reanimation Protocol modifiers from the active round-choice directive.

    Undying Legions P (rp_reroll) -> {"rp_reroll": True}
    Any other / no directive      -> {}

    Considers every active directive, so the effect fires whether Undying Legions is
    the round-assigned protocol or the always-active 6th / dynasty protocol.
    """
    if any(e.get("type") == "rp_reroll" for e in _active_directive_effects(player)):
        return {"rp_reroll": True}
    return {}


def get_active_heal_bonus(player: str, unit: Unit) -> int:
    """Extra wounds healed from an active directive's ``heal_bonus`` effect.

    The directive names its target ability data-driven via ``target_rule``
    (e.g. Undying Legions S -> Living Metal). Generic: any faction/directive
    with a ``heal_bonus`` effect applies when the healed unit carries the
    matching rule. Returns 0 when no such directive is active or the rule
    does not match. Sums across every active directive (round-assigned plus the
    always-active 6th / dynasty protocol).
    """
    bonus = 0
    for effect in _active_directive_effects(player):
        if effect.get("type") != "heal_bonus":
            continue
        target_rule = effect.get("target_rule")
        if target_rule and target_rule not in unit.rules:
            continue
        bonus += int(effect.get("value", 0))
    return bonus


def _unit_matches_target(unit: Unit, effect: dict) -> bool:
    """True if unit satisfies the effect's target_keywords / target_keywords_any constraints."""
    required = effect.get("target_keywords", [])
    any_of = effect.get("target_keywords_any", [])
    if any(not unit.has_keyword(kw) for kw in required):
        return False
    if any_of and not any(unit.has_keyword(kw) for kw in any_of):
        return False
    return True


def _active_effects_for_faction(faction: str) -> list[dict]:
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
    total = 0
    for eff in _active_effects_for_faction(faction):
        if eff.get("type") == "buff_stat" and eff.get("stat") == stat:
            if _unit_matches_target(unit, eff):
                total += int(eff.get("modifier", 0))
    return total


def ability_invuln_save(faction: str, unit: Unit) -> int | None:
    """Best invuln save granted by active faction abilities for this unit, or None."""
    best: int | None = None
    for eff in _active_effects_for_faction(faction):
        if eff.get("type") == "invuln_save" and _unit_matches_target(unit, eff):
            val = eff.get("modifier")
            if val is not None:
                best = int(val) if best is None else min(best, int(val))
    return best


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
    state: dict,  # type: ignore[type-arg]
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
    units_state: dict = state.get(units_key, {})  # type: ignore[type-arg]

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
