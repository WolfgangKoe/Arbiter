from dataclasses import dataclass, field

from gameObjects.unit import Unit


@dataclass
class SlotConstraint:
    role: str
    min_units: int
    max_units: int  # -1 = unlimited


@dataclass
class DetachmentType:
    id: str
    name_en: str
    slot_constraints: list[SlotConstraint] = field(default_factory=list)


@dataclass
class Detachment:
    detachment_type: str  # "patrol" | "battalion" etc.
    name: str  # custom name or = type name
    units_by_role: dict[str, list[Unit]] = field(default_factory=dict)
