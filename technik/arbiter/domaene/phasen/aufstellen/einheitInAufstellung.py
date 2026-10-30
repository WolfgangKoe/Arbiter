from collections.abc import Collection

from arbiter.domaene.sperre import Grund, Sperre
from arbiter.domaene.spielobjekte import Einheit, Spieler


def prüfenDassWählbar(
    einheit: Einheit,
    aufgestellt: Collection[Einheit],
    anDerReihe: Spieler | None,
    einheitInAufstellung: Einheit | None,
) -> None:
    if einheit in aufgestellt or anDerReihe is None or einheit not in anDerReihe.armee.einheiten:
        raise Sperre(Grund.nichtWählbar)
    if einheitInAufstellung not in (None, einheit):
        raise Sperre(Grund.einheitBegonnen)
