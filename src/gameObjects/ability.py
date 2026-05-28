from __future__ import annotations

from dataclasses import dataclass


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


@dataclass
class Effect:
    type: str
    target: str
    amount: str | None = None
    stat: str | None = None
    modifier: int | None = None
    handler: str | None = None


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
    ability_type: str = "triggered"  # "triggered" | "activated"
