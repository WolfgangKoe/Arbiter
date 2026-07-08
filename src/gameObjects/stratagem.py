"""Stratagem (Gefechtsoption) data model.

A Stratagem is a one-time or once-per-phase ability that costs CP.
The GO visibility logic is implemented in gameMechanic/stratagems.py.

Visibility rules (see docs/spec/processes.md P-06):
  - conditions met + CP available + not yet used this phase  →  shown, clickable
  - conditions met + CP insufficient                         →  shown, greyed out
  - conditions met + already used this phase                 →  shown, greyed out
  - conditions not met                                       →  not shown
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Literal

from gameObjects.ability import Effect


@dataclass(frozen=True)
class StratagemModifier:
    """Describes how an active stratagem modifies attack rolls.

    Used by the attack sequence renderer (6d) to show transparent modifier stacks.
    """

    roll_type: str
    """hit | wound | save | fnp | charge | damage"""

    value: int
    """Positive = bonus, negative = penalty."""

    target: str
    """attacker | defender — which side of the combat this applies to."""

    expires_at: str
    """phase_end | turn_end"""

    source_label: str
    """Short display label shown in the modifier stack."""

    phase: str | None = None
    """Override for which phase the modifier applies in; None = same as stratagem phase."""


@dataclass(frozen=True)
class Stratagem:
    id: str
    name_en: str
    cp_cost: int  # 0 = free
    phase: str | list[str]  # "command" | "movement" | ... | "any" | ["shooting", "fight"]
    stage: Literal[
        "start", "active", "end"
    ]  # data schema only — no visibility filter; timing lives in rule_text
    player: Literal["active", "inactive", "both"]  # who may use it
    conditions: list[str] = field(default_factory=list)  # keyword conditions
    rule_text: str = ""
    once_per_phase: bool = True
    once_per_battle: bool = (
        False  # overrides once_per_phase; enforcement pending session-state tracking
    )
    timing: str | None = None  # None = proactive | "phase_reactive" | "phase_start" | "phase_end"
    event: str | None = None  # "after_roll" | "on_destroy" | "on_target" | "on_declaration"
    effect: Effect | None = None  # machine-readable effect (mirrors Ability.effect vocabulary)
    detachment: str | None = None  # detachment type required, e.g. "cult_of_the_cryptek"
    modifier: StratagemModifier | None = None  # attack-sequence modifier stack (6d)


# ── GO visibility helper ──────────────────────────────────────────────────────


_SHARED_ID_MARKER = ".shared."


def is_core_stratagem(stratagem_id: str) -> bool:
    """Whether the id belongs to the shared/core pool (game-wide, not faction-specific).

    Shared stratagem ids follow the ``<edition>.shared.stratagem.<name>`` namespace
    (see data/wh40k_9e/_shared/stratagems.yaml); faction ids carry the faction dir
    instead of ``shared``. Used by the player-split renderer for section headers.
    """
    return _SHARED_ID_MARKER in stratagem_id


def stratagem_usable_by_player(player_field: str, is_this_player_active: bool) -> bool:
    """Whether a stratagem's `player` field permits use by the given player.

    player_field: Stratagem.player ("active" | "inactive" | "both").
    is_this_player_active: True if the player in question currently holds the turn.
    """
    if player_field == "both":
        return True
    if player_field == "active":
        return is_this_player_active
    return not is_this_player_active


def stratagem_visibility(
    stratagem: Stratagem,
    cp_available: int,
    current_phase: str,
    used_this_phase: set[str],
    conditions_met: bool,
    used_in_battle: set[str] | None = None,
    reactive_trigger_active: bool = False,
) -> Literal["clickable", "greyed", "hidden"]:
    """Return the display state for a stratagem given the current game context.

    Visibility depends on phase, conditions, CP and usage — NOT on the
    ``stage`` field: 9E only codifies the phase binding; within-phase timing
    ("at the start of…", "at the end of…") lives in the rule text shown in
    the stratagem expander (see docs/spec/acceptance/rules.md, Stratagems).

    Parameters
    ----------
    stratagem:        The stratagem to evaluate.
    cp_available:     CP pool of the player who could use this stratagem.
    current_phase:    e.g. "shooting"
    used_this_phase:  Set of stratagem IDs already used this phase.
    conditions_met:   Whether unit/keyword conditions for this GO are satisfied.
    used_in_battle:   Battle-scoped set of once_per_battle stratagem IDs already used
                      by the spending player. When provided, a once_per_battle
                      stratagem in this set is greyed out regardless of phase, for
                      the remainder of this player's battle — not a global lock
                      shared across both players.
    reactive_trigger_active: For `timing == "phase_reactive"` stratagems only — True
                      when the caller has determined that this stratagem's specific
                      reactive moment (e.g. "an enemy charge was just declared") is
                      open right now. Defaults to False, which keeps every
                      phase_reactive stratagem hidden in proactive listings (the
                      central Stratagems tab never offers them — Plan 015). Contextual
                      reactive-GO boxes (gameProtocoll.py/_common.py) pass True only
                      for the one stratagem whose window they just opened; the normal
                      phase/CP/used checks below still apply on top of this gate.
    """
    if not conditions_met:
        return "hidden"
    if stratagem.timing == "phase_reactive" and not reactive_trigger_active:
        return "hidden"
    phase = stratagem.phase
    if phase != "any":
        phases = phase if isinstance(phase, list) else [phase]
        if current_phase not in phases:
            return "hidden"

    if stratagem.once_per_battle and used_in_battle is not None:
        if stratagem.id in used_in_battle:
            return "greyed"
    if stratagem.id in used_this_phase:
        return "greyed"
    if cp_available < stratagem.cp_cost:
        return "greyed"

    return "clickable"


def reactive_stratagems_for(stratagems: list[Stratagem], phase: str, event: str) -> list[Stratagem]:
    """Return the ``phase_reactive`` stratagems matching an open (phase, event) window.

    Pure data-shape filter — the single entry point phase handlers use to look up
    which reactive GOs could apply to a moment that just occurred (e.g. "an enemy
    charge was declared" → phase="charge", event="on_declaration"). Deliberately
    does NOT check the `player` field, CP, or usage: those depend on WHICH player
    is eligible to react, which varies per stratagem (e.g. Counter-Offensive keys
    off `fight_current_player`, not the generic active/inactive split) — callers
    resolve that via `stratagem_usable_by_player()` and `stratagem_visibility()`
    (passing `reactive_trigger_active=True`) themselves.
    """
    matched = []
    for s in stratagems:
        if s.timing != "phase_reactive" or s.event != event:
            continue
        phases = s.phase if isinstance(s.phase, list) else [s.phase]
        if "any" not in phases and phase not in phases:
            continue
        matched.append(s)
    return matched


def stratagem_undo_visible(
    stratagem_id: str,
    used_this_phase: set[str],
    used_in_battle: set[str],
) -> bool:
    """Return True only while the stratagem's own phase-window is still open.

    Undo must disappear once the phase changes, even if the stratagem stays
    battle-greyed afterwards (once_per_battle persists; the undo window does not).
    """
    return stratagem_id in used_this_phase
