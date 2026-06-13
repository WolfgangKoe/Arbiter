from dataclasses import dataclass, field

from gameObjects.weapon import Weapon


@dataclass
class WeaponSwapSpec:
    """One datasheet wargear option — replaces base weapons with picked options.

    scope "group":     the whole group swaps together (e.g. Boss Nob).
    scope "per_model": individual models swap; the loader splits them into
                       sub-groups with fixed weapons.
    limit caps how many models may take the swap: "any", "per_10", "per_5",
    "per_3" (per full 10/5/3 models the unit contains — core-rules wording).
    pick = number of weapons chosen per swap (Boss Nob: "two of the following").
    replaces = [] makes the swap a pure addition (e.g. Warbikers' extra slugga).
    """

    id: str
    scope: str  # "group" | "per_model"
    replaces: list[str]
    options: list[str]
    pick: int = 1
    limit: str = "any"  # "any" | "per_10" | "per_5" | "per_3"


@dataclass
class ModelGroupSpec:
    """Raw model group definition from YAML — count not yet resolved from roster.

    ``stats`` holds per-group stat overrides (e.g. a Boss Nob with WS 2+, S 5,
    A 3). Any of: attacks, strength, wounds (int) and ws, bs ("3+"). Missing keys
    fall back to the unit-level stat — homogeneous groups carry an empty dict.
    """

    id: str
    name_en: str
    count_raw: str | int  # "remainder" | "models_max" | int
    base_weapon_refs: list[str]
    weapon_swaps: list[WeaponSwapSpec]
    priority: int
    stats: dict[str, int | str] = field(default_factory=dict)


@dataclass
class ModelGroup:
    """Resolved model group — count and weapons finalized from roster entry."""

    id: str
    name_en: str
    count: int
    weapons: list[Weapon]
    priority: int
    stats: dict[str, int | str] = field(default_factory=dict)

    def stat(self, name: str, fallback: int | str | None) -> int | str | None:
        """Per-group stat override, falling back to the unit-level value."""
        return self.stats.get(name, fallback)


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
    model_group_specs: list[ModelGroupSpec] = field(default_factory=list)
    model_groups: list[ModelGroup] = field(default_factory=list)

    def has_keyword(self, keyword: str) -> bool:
        needle = keyword.upper()
        return any(kw.upper() == needle for kw in self.keywords)

    def group_wound_value(self, group: ModelGroup) -> int:
        """Per-model wounds for a group (e.g. Triarchal Menhirs 7), default unit.wounds."""
        return int(group.stat("wounds", self.wounds) or self.wounds)

    def has_per_group_wounds(self) -> bool:
        """True if any model group overrides wounds (e.g. Szarekh 16 + Menhirs 7)."""
        return any("wounds" in g.stats for g in self.model_groups)

    def get_triggered_effect(self, timing: str, phase: str, effect: str) -> TriggeredEffect | None:
        for te in self.triggered_effects:
            if te.timing == timing and te.phase == phase and te.effect == effect:
                return te
        return None
