from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class RoundChoiceAbility:
    id: str
    name_en: str
    name_de: str
    primary: str
    secondary: str
    primary_effect: dict[str, Any] = field(default_factory=dict)
    secondary_effect: dict[str, Any] = field(default_factory=dict)
    subfaction_affinity: str | None = None
