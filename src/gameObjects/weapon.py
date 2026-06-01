from dataclasses import dataclass, field


@dataclass
class WeaponProfile:
    weapon_type: str  # "Rapid Fire", "Heavy", "Assault", "Pistol", "Melee"
    range_inches: int
    attacks: str  # "1", "D6", "2D3", "*"
    strength: str  # "4", "User", "User+2", "User×2"
    ap: str  # "0", "-1", "-3"
    damage: str  # "1", "D3", "D3+3"
    is_melee: bool
    abilities: str = ""
    name_en: str = ""  # only set for dual-profile weapons (e.g. "Shooting", "Melee")


@dataclass
class WeaponGroup:
    """Links a group of models within a unit to the weapons they carry."""

    model_count: int
    weapons: list["Weapon"] = field(default_factory=list)


@dataclass
class Weapon:
    id: str
    name_en: str
    profiles: list[WeaponProfile] = field(default_factory=list)
    is_relic: bool = False
