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

    # Convenience properties — delegate to profiles[0] for single-profile weapons.
    # Multi-profile weapons (dual-mode) should be handled by iterating .profiles.
    @property
    def is_melee(self) -> bool:
        return self.profiles[0].is_melee if self.profiles else False

    @property
    def range_inches(self) -> int:
        return self.profiles[0].range_inches if self.profiles else 0

    @property
    def attacks(self) -> str:
        return self.profiles[0].attacks if self.profiles else "0"

    @property
    def strength(self) -> str:
        return self.profiles[0].strength if self.profiles else "0"

    @property
    def ap(self) -> str:
        return self.profiles[0].ap if self.profiles else "0"

    @property
    def damage(self) -> str:
        return self.profiles[0].damage if self.profiles else "0"

    @property
    def abilities(self) -> str:
        return self.profiles[0].abilities if self.profiles else ""
