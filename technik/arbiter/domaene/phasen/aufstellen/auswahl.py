"""Die Auswahl: die eine ausgewählte Einheit der Ablagen (AUF-5)."""

from collections.abc import Collection

from arbiter.domaene.spielobjekte import Einheit, Spieler


class Auswahl:
    def __init__(self, spieler: tuple[Spieler, Spieler], aufgestellt: Collection[Einheit]) -> None:
        self._spieler = spieler
        self._aufgestellt = aufgestellt
        self._einheit: Einheit | None = None

    @property
    def einheit(self) -> Einheit | None:
        return self._einheit

    def auswählen(self, einheit: Einheit) -> None:
        self._prüfenDassZurAufstellung(einheit)
        if einheit in self._aufgestellt:
            raise ValueError("Eine aufgestellte Einheit ist nicht auswählbar")
        # Regel: AUF-5.11, die Einheit ist ausgewählt und keine andere
        self._einheit = einheit

    def abwählen(self, einheit: Einheit) -> None:
        self._prüfenDassZurAufstellung(einheit)
        if self._einheit is einheit:
            self._einheit = None

    def ausgewählt(self, einheit: Einheit) -> bool:
        return einheit is self._einheit

    def _prüfenDassZurAufstellung(self, einheit: Einheit) -> None:
        if not any(einheit in spieler.armee.einheiten for spieler in self._spieler):
            raise ValueError("Die Einheit gehört nicht zur Aufstellung")
