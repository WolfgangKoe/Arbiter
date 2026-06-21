from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class Trigger:
    timing: str
    phase: str | list[str]
    player: str = "active"  # "active" | "inactive" | "either"
    event: str | None = None
    stage: str = "active"  # "start" | "active" | "end" — maps to phase_stage in session_state


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
    handler: str | None = None
    revive: bool = True  # False = cap heal to current living models, no resurrection
    effects: list[dict] | None = None  # sub-effects for multi-type effects


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
