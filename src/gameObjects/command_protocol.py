from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class CommandProtocol:
    id: str
    name_en: str
    name_de: str
    primary: str
    secondary: str
    auto_round_1: bool = False
    primary_effect: dict = field(default_factory=dict)
    secondary_effect: dict = field(default_factory=dict)
    subfaction_affinity: str | None = None
