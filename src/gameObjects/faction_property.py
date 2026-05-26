from dataclasses import dataclass


@dataclass
class FactionProperty:
    id: str
    name_en: str
    triggers_phase: str  # "command" | "shooting" | etc.
    affects_parameter: str  # "wounds" | "save" | etc.
    ability_keyword: str  # e.g. "livingMetal"
    rule_text: str
    applies_to_keyword: str | None
