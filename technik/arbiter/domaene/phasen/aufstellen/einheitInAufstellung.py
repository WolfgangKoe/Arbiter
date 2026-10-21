"""Wann ein Modell dran ist: nur die Einheit in Aufstellung des Spielers an der Reihe (AUF-7)."""

from collections.abc import Collection

from arbiter.domaene.sperre import Grund, Sperre
from arbiter.domaene.spielobjekte import Einheit, Spieler


def prüfenDassWählbar(
    einheit: Einheit,
    aufgestellt: Collection[Einheit],
    anDerReihe: Spieler | None,
    einheitInAufstellung: Einheit | None,
) -> None:
    """Wirft die Sperre ohne Stelle, wenn die Einheit jetzt nicht dran ist."""
    # Regel: AUF-7.2 und AUF-7.3 sperren vor jeder Prüfung der Stelle (AUF-3.8)
    if einheit in aufgestellt or anDerReihe is None or einheit not in anDerReihe.armee.einheiten:
        raise Sperre(Grund.nichtWählbar)
    if einheitInAufstellung not in (None, einheit):
        raise Sperre(Grund.einheitBegonnen)
