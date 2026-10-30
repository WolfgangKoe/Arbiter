"""Die Gründe gegen das Beenden der Bewegungsphase (BEW-4, V17)."""

from collections.abc import Iterable, Mapping

from arbiter.domaene.querschnitt.kohaerenz import einheitInKohärenz
from arbiter.domaene.sperre import Grund
from arbiter.domaene.spielobjekte import Einheit, Modell, Stelle


def gründeGegenDasBeenden(
    einheiten: Iterable[Einheit], stellen: Mapping[Modell, Stelle]
) -> set[Grund]:
    """Keine Kohärenz, sobald eine der Einheiten nicht in Kohärenz ist."""
    if all(einheitInKohärenz(einheit, stellen) for einheit in einheiten):
        return set()
    return {Grund.keineKohärenz}
