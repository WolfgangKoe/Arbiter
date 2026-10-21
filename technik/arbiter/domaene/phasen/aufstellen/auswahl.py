"""Die Auswahl: die eine ausgewählte Einheit der Ablagen mit ihrer Ebene (AUF-5, AUF-20, AUF-25)."""

from collections.abc import Collection

from arbiter.domaene.spielobjekte import Einheit, Modell, Spieler


class Auswahl:
    def __init__(self, spieler: tuple[Spieler, Spieler], aufgestellt: Collection[Einheit]) -> None:
        self._spieler = spieler
        self._aufgestellt = aufgestellt
        self._einheit: Einheit | None = None
        self._modellAlsEbene: Modell | None = None

    @property
    def einheit(self) -> Einheit | None:
        return self._einheit

    def auswählen(self, einheit: Einheit) -> None:
        self._prüfenDassZurAufstellung(einheit)
        if einheit in self._aufgestellt:
            raise ValueError("Eine aufgestellte Einheit ist nicht auswählbar")
        if einheit is self._einheit:
            return
        # Regel: AUF-5.11 (keine andere ausgewählt), AUF-20.2 (die Ebene ist die Einheit)
        self._einheit = einheit
        self._modellAlsEbene = None

    def abwählen(self, einheit: Einheit) -> None:
        self._prüfenDassZurAufstellung(einheit)
        if self._einheit is einheit:
            self._einheit = None
            self._modellAlsEbene = None

    def ausgewählt(self, einheit: Einheit) -> bool:
        return einheit is self._einheit

    def ebene(self, einheit: Einheit) -> Einheit | Modell | None:
        """Das Modell, sonst die Einheit, die Ziehen bewegt; None ohne Auswahl."""
        if not self.ausgewählt(einheit):
            return None
        return einheit if self._modellAlsEbene is None else self._modellAlsEbene

    def ebeneWählen(self, modell: Modell) -> None:
        self._prüfenDassZurAusgewähltenEinheit(modell)
        self._modellAlsEbene = modell

    def ebeneAbwählen(self, modell: Modell) -> None:
        self._prüfenDassZurAusgewähltenEinheit(modell)
        if self._modellAlsEbene is modell:
            self._modellAlsEbene = None

    def modellAusgewählt(self, modell: Modell) -> bool:
        """Regel: AUF-5.7 alle Modelle der ausgewählten Einheit, AUF-25.4 nur das der Ebene."""
        gehörtDazu = self._einheit is not None and modell in self._einheit.modelle
        return gehörtDazu and self._modellAlsEbene in (None, modell)

    def _prüfenDassZurAusgewähltenEinheit(self, modell: Modell) -> None:
        if self._einheit is None or modell not in self._einheit.modelle:
            raise ValueError("Das Modell gehört nicht zur ausgewählten Einheit")

    def _prüfenDassZurAufstellung(self, einheit: Einheit) -> None:
        if not any(einheit in spieler.armee.einheiten for spieler in self._spieler):
            raise ValueError("Die Einheit gehört nicht zur Aufstellung")
