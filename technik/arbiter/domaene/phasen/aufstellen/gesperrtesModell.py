"""Das gesperrte Modell: seine Stelle, die Gründe und was „zurück“ wiederherstellt (AUF-9)."""

from collections.abc import Mapping
from dataclasses import dataclass

from arbiter.domaene.sperre import Grund
from arbiter.domaene.spielobjekte import Modell, Stelle


@dataclass(frozen=True)
class Gesperrtes:
    stelle: Stelle
    gründe: frozenset[Grund]
    vorige: Stelle | None
    loslassen: frozenset[Modell]


def zurücknehmen(gesperrte: Mapping[Modell, Gesperrtes], stellen: dict[Modell, Stelle]) -> None:
    """Jedes gesperrte Modell steht wieder, wo es war, oder die Gruppe seines Loslassens fehlt."""
    for modell, gesperrtes in gesperrte.items():
        if gesperrtes.vorige is not None:
            stellen[modell] = gesperrtes.vorige
            continue
        for aus in gesperrtes.loslassen:
            stellen.pop(aus, None)
