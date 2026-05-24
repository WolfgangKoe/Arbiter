from dataclasses import dataclass, field

BATTLEFIELD_ROLE_DE: dict[str, str] = {
    "HQ": "HQ",
    "Troops": "Standard",
    "Elites": "Elite",
    "Fast Attack": "Sturm",
    "Heavy Support": "Unterstützung",
    "Flyer": "Flieger",
    "Dedicated Transport": "Transporter",
    "Lord of War": "Kriegskoloss",
}


@dataclass
class Unit:
    id: str
    name_en: str
    name_de: str
    roles: list[str] = field(default_factory=list)
    keywords: list[str] = field(default_factory=list)
