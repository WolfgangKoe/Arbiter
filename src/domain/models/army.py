from dataclasses import dataclass, field

from src.domain.models.unit import BATTLEFIELD_ROLE_DE, Unit


@dataclass
class Army:
    name: str
    faction: str
    units: list[Unit] = field(default_factory=list)

    def units_by_role(self) -> dict[str, list[Unit]]:
        grouped: dict[str, list[Unit]] = {de: [] for de in BATTLEFIELD_ROLE_DE.values()}
        ungrouped: list[Unit] = []

        for unit in self.units:
            placed = False
            for en_role, de_role in BATTLEFIELD_ROLE_DE.items():
                if en_role in unit.roles:
                    grouped[de_role].append(unit)
                    placed = True
                    break
            if not placed:
                ungrouped.append(unit)

        result = {role: units for role, units in grouped.items() if units}
        if ungrouped:
            result["Sonstige"] = ungrouped
        return result
