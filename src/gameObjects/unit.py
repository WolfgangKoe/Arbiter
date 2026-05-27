from dataclasses import dataclass, field

from gameObjects.weapon import Weapon


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
    move: str  # "6\"" (str because bikes etc. are more complex)
    bs: str  # "3+" (ballistic skill)
    ws: str  # "3+" (weapon skill)
    strength: int
    toughness: int
    save: int  # armour save target number (e.g. 3 = 3+)
    invuln_save: int | None  # invulnerable save or None
    leadership: int
    oc: int  # Objective Control
    fnp: int | None  # Feel No Pain or None
    weapons: list[Weapon] = field(default_factory=list)
    abilities: str = ""
    rules: list[str] = field(default_factory=list)
