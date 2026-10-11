"""Die Auswahl: die ausgewählten Einheiten der Ablage (AUF-5)."""

from collections.abc import Collection

from arbiter.domaene.spielobjekte import Einheit, Spieler


class Auswahl:
    def __init__(self, spieler: tuple[Spieler, Spieler], aufgestellt: Collection[Einheit]) -> None:
        self._spieler = spieler
        self._aufgestellt = aufgestellt
        self._einheiten: set[Einheit] = set()

    def auswählen(self, einheit: Einheit) -> None:
        self._prüfenDassZurAufstellung(einheit)
        if einheit in self._aufgestellt:
            raise ValueError("Eine aufgestellte Einheit ist nicht auswählbar")
        self._einheiten.add(einheit)

    def abwählen(self, einheit: Einheit) -> None:
        self._prüfenDassZurAufstellung(einheit)
        self._einheiten.discard(einheit)

    def ausgewählt(self, einheit: Einheit) -> bool:
        return einheit in self._einheiten

    def _prüfenDassZurAufstellung(self, einheit: Einheit) -> None:
        if not any(einheit in spieler.armee.einheiten for spieler in self._spieler):
            raise ValueError("Die Einheit gehört nicht zur Aufstellung")
