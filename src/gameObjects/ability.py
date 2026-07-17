from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Literal


@dataclass
class Trigger:
    timing: str
    phase: str | list[str]
    player: str = "active"  # "active" | "inactive" | "either"
    event: str | None = None
    stage: str = (
        "active"  # "start" | "active" | "end" — data schema only; timing info lives in rule text
    )


@dataclass
class Condition:
    has_rules: list[str] | None = None
    has_keywords: list[str] | None = None
    within_inches: int | None = None
    max_uses: int | None = None
    min_round: int | None = None
    unit_not_destroyed: bool = False
    needs_healing: bool = False
    once_per_battle: bool = False


@dataclass
class Effect:
    type: str
    target: str | None = None
    amount: str | None = None
    stat: str | None = None
    modifier: int | None = None
    success_on: int | None = None  # alias for reanimate effects; modifier for other types
    handler: str | None = None
    revive: bool = True  # False = cap heal to current living models, no resurrection
    effects: list[dict[str, Any]] | None = None  # sub-effects for multi-type effects


@dataclass
class ExtraUses:
    """Extra activation uses an ability gains when its owner has a keyword.

    Data-driven (read from YAML) so no faction keyword is hardcoded in src/.
    """

    has_keyword: str
    bonus: int = 1


@dataclass
class Ability:
    id: str
    name_en: str
    source: str
    rule_text: str
    trigger: Trigger
    conditions: list[Condition]
    effect: Effect
    unit_id: str | None = None
    wargear_id: str | None = None
    ability_type: str = "triggered"  # "triggered" | "activated"
    badge_label: str | None = None
    active_text: str | None = None
    next_stage_id: str | None = None
    extra_uses: list[ExtraUses] = field(default_factory=list)

    def bonus_uses_for(self, unit: Any) -> int:
        """Extra activation uses granted by the owner's keywords (data-driven)."""
        if unit is None:
            return 0
        return sum(e.bonus for e in self.extra_uses if unit.has_keyword(e.has_keyword))


# ── Reactive-ability visibility helpers (B-028a) ──────────────────────────────
#
# Ability-side counterparts of gameObjects/stratagem.py's reactive_stratagems_for()
# / stratagem_visibility() / stratagem_undo_visible(). Kept as small, separate
# copies rather than a shared adapter: Stratagem carries timing/phase/event/player
# as flat fields, Ability nests the same information inside Trigger — a generic
# adapter over both shapes would cost more than this second small copy (2nd
# repetition, below the project's "3rd repetition" DRY threshold, CLAUDE.md
# "Clean Code"). See docs/handoff/S157_planning.md Grundannahme 1 for the full
# comparison.


def reactive_abilities_for(abilities: list[Ability], phase: str, event: str) -> list[Ability]:
    """Return the ``phase_reactive`` abilities matching an open (phase, event) window.

    Pure data-shape filter — mirrors ``gameObjects.stratagem.reactive_stratagems_for()``
    but reads ``ability.trigger.timing``/``.phase``/``.event`` instead of the flat
    Stratagem fields. Deliberately does NOT check ``trigger.player``, conditions or
    usage — callers resolve those via ``ability_usable_by_player()`` and
    ``ability_visibility()`` (passing ``reactive_trigger_active=True``) themselves,
    same division of labour as the Stratagem version.
    """
    matched = []
    for ability in abilities:
        trigger = ability.trigger
        if trigger.timing != "phase_reactive" or trigger.event != event:
            continue
        phases = trigger.phase if isinstance(trigger.phase, list) else [trigger.phase]
        if "any" not in phases and phase not in phases:
            continue
        matched.append(ability)
    return matched


def ability_usable_by_player(trigger_player: str, is_this_player_active: bool) -> bool:
    """Whether an ability's ``trigger.player`` field permits use by the given player.

    trigger_player: ``Trigger.player`` ("active" | "inactive" | "either") — Ability's
    own vocabulary differs from ``Stratagem.player`` ("active" | "inactive" | "both"),
    so this cannot just call ``stratagem_usable_by_player()`` with a translated
    string; a small second copy instead (2nd repetition, DRY threshold not crossed).
    """
    if trigger_player == "either":
        return True
    if trigger_player == "active":
        return is_this_player_active
    return not is_this_player_active


def ability_visibility(
    ability: Ability,
    current_phase: str,
    used_this_phase: set[str],
    conditions_met: bool,
    reactive_trigger_active: bool = False,
) -> Literal["clickable", "greyed", "hidden"]:
    """Return the display state for an Ability given the current game context.

    Ability-side counterpart of ``gameObjects.stratagem.stratagem_visibility()`` —
    deliberately WITHOUT a CP-gate: ``Ability`` has no ``cp_cost`` field (S157
    scope doc Grundannahme 2), so there is nothing to not-afford here. Also omits
    the once-per-battle gate ``stratagem_visibility`` has: none of today's
    ``phase_reactive`` Abilities declare a battle-scoped condition
    (``Condition.once_per_battle`` exists on the dataclass, but
    ``abilityEngine.check_conditions()`` does not read it — that flag is reserved
    for the separate once-per-battle *activated*-ability flow,
    ``armyCard._render_once_per_battle_ability_ui`` +
    ``gameState.is_once_per_battle_used``). Adding an unused parallel gate here
    would be dead plumbing (YAGNI) — extend this function if a future reactive
    Ability needs one, rather than bolting a `used_in_battle`-style parameter on
    ahead of need.

    Parameters mirror ``stratagem_visibility``'s minus ``cp_available``:
    ``current_phase`` (e.g. "shooting"), ``used_this_phase`` (ability IDs this
    player already used this phase), ``conditions_met`` (unit/keyword/rule gate,
    e.g. via ``abilityEngine.check_conditions``), ``reactive_trigger_active``
    (True only when the caller's specific (phase, event) window is open right
    now — see ``stratagem_visibility``'s docstring for the same contract).
    """
    if not conditions_met:
        return "hidden"
    if ability.trigger.timing == "phase_reactive" and not reactive_trigger_active:
        return "hidden"
    phase = ability.trigger.phase
    if phase != "any":
        phases = phase if isinstance(phase, list) else [phase]
        if current_phase not in phases:
            return "hidden"
    if ability.id in used_this_phase:
        return "greyed"
    return "clickable"


def ability_undo_visible(ability_id: str, used_this_phase: set[str]) -> bool:
    """Return True only while the ability's own phase-window is still open.

    Mirrors ``gameObjects.stratagem.stratagem_undo_visible()``. Today equivalent
    to plain set membership — ``ability_visibility()`` has no once-per-battle-style
    gate yet (see its docstring), so nothing yet persists "greyed" beyond the
    current phase the way a ``once_per_battle`` Stratagem does. Kept as its own
    named seam so a future battle-scoped Ability does not require every caller to
    change, same rationale as the Stratagem counterpart.
    """
    return ability_id in used_this_phase
