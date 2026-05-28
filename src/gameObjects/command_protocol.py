from __future__ import annotations

from dataclasses import dataclass


@dataclass
class CommandProtocol:
    id: str
    name_en: str
    name_de: str
    primary: str
    secondary: str
    auto_round_1: bool = False
