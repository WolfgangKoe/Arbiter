from dataclasses import dataclass


@dataclass
class Weapon:
    id: str
    name_en: str
    weapon_type: str  # "Rapid Fire", "Heavy", "Assault", "Pistol", "Melee"
    range_inches: str  # "12", "24", "Melee"
    attacks: str  # "1", "D6", "2D3"
    strength: str  # "4", "User", "×2"
    ap: str  # "0", "-1", "-3"
    damage: str  # "1", "D3"
    abilities: str = ""
    is_melee: bool = False
