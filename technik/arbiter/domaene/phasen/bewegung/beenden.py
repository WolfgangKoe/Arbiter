from collections.abc import Iterable, Mapping

from arbiter.domaene.querschnitt.kohaerenz import einheitInKohärenz
from arbiter.domaene.sperre import Grund
from arbiter.domaene.spielobjekte import Einheit, Modell, Stelle


def gründeGegenDasBeenden(
    einheiten: Iterable[Einheit], stellen: Mapping[Modell, Stelle]
) -> set[Grund]:
    if all(einheitInKohärenz(einheit, stellen) for einheit in einheiten):
        return set()
    return {Grund.keineKohärenz}
