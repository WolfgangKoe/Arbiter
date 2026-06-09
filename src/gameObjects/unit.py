from dataclasses import dataclass, field

from gameObjects.weapon import Weapon


@dataclass
class TriggeredEffect:
    """A relic or ability effect that triggers at a specific game moment."""

    timing: str  # "phase_start" | "after_fight"
    phase: str  # "command" | "movement" | "fight"
    effect: str  # "gain_cp_roll" | "teleport" | "mortal_after_melee"
    once_per_battle: bool = False
    dice: str | None = None  # "D6" | "D3"
    threshold: int | None = None  # e.g. 4 → roll 4+
    amount: int | None = None  # e.g. +1 CP
    mortal_dice: str | None = None  # e.g. "D3" for mortal wound damage


@dataclass
class WargearOption:
    type: str  # "replace" | "replace_pair" | "add"
    with_refs: list[str] = field(default_factory=list)  # for replace / replace_pair
    replaces: str | None = None  # explicit slot for replace
    item: str | None = None  # ref for add


@dataclass
class DamageBracket:
    wounds_min: int
    wounds_max: int
    move: str | None = None
    ws: str | None = None
    bs: str | None = None
    attacks: str | None = None


@dataclass
class Unit:
    id: str  # e.g. "wh40k_9e.necrons.unit.warriors"
    name_en: str
    name_de: str
    faction: str  # "Necrons" | "Orks"
    subfaction: str | None  # "Nephrekh" | "Bad Moons" | None
    battlefield_role: list[str]  # ["Troops"] | ["HQ"] etc.
    keywords: list[str]  # all keywords flat: faction + other
    wounds: int  # wounds per model
    models_min: int
    models_max: int
    power_level: int
    move: str  # "6\"" (str because bikes etc. are more complex)
    bs: str  # "3+" (ballistic skill)
    ws: str  # "3+" (weapon skill)
    strength: int
    toughness: int
    attacks: int | None  # None for buildings/fortifications
    save: int  # armour save target number (e.g. 3 = 3+)
    invuln_save: int | None  # invulnerable save or None
    leadership: int | None  # None for buildings/fortifications
    oc: int  # Objective Control
    fnp: int | None  # Feel No Pain or None
    weapons: list[Weapon] = field(default_factory=list)
    wargear_options: list[WargearOption] = field(default_factory=list)
    damage_bracket: list[DamageBracket] | None = None
    rules: list[str] = field(default_factory=list)
    wargear_ids: list[str] = field(default_factory=list)
    wargear_keywords: list[str] = field(default_factory=list)
    weapon_restrictions: dict[str, str] = field(default_factory=dict)
    relic_id: str | None = None
    relic_name: str | None = None
    triggered_effects: list[TriggeredEffect] = field(default_factory=list)

    def has_keyword(self, keyword: str) -> bool:
        needle = keyword.upper()
        return any(kw.upper() == needle for kw in self.keywords)

    def get_triggered_effect(self, timing: str, phase: str, effect: str) -> TriggeredEffect | None:
        for te in self.triggered_effects:
            if te.timing == timing and te.phase == phase and te.effect == effect:
                return te
        return None
