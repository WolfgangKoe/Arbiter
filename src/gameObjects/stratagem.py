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


@dataclass(frozen=True)
class Stratagem:
    id: str
    name_en: str
    cp_cost: int  # 0 = free
    phase: str  # "command" | "movement" | "shooting" | ...
    stage: Literal["start", "active", "end"]  # when in the phase it may be used
    player: Literal["active", "inactive", "both"]  # who may use it
    conditions: list[str] = field(default_factory=list)  # keyword conditions
    rule_text: str = ""
    once_per_phase: bool = True


# ── GO visibility helper ──────────────────────────────────────────────────────


def stratagem_visibility(
    stratagem: Stratagem,
    cp_available: int,
    current_phase: str,
    current_stage: str,
    used_this_phase: set[str],
    conditions_met: bool,
) -> Literal["clickable", "greyed", "hidden"]:
    """Return the display state for a stratagem given the current game context.

    Parameters
    ----------
    stratagem:        The stratagem to evaluate.
    cp_available:     CP pool of the player who could use this stratagem.
    current_phase:    e.g. "shooting"
    current_stage:    "start" | "active" | "end"
    used_this_phase:  Set of stratagem IDs already used this phase.
    conditions_met:   Whether unit/keyword conditions for this GO are satisfied.
    """
    if not conditions_met:
        return "hidden"
    if stratagem.phase != current_phase:
        return "hidden"
    if stratagem.stage != current_stage:
        return "hidden"

    if stratagem.id in used_this_phase:
        return "greyed"
    if cp_available < stratagem.cp_cost:
        return "greyed"

    return "clickable"
