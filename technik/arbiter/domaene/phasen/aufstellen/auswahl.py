"""Die Auswahl: die eine ausgewählte Einheit mit ihrer Ebene (AUF-5, AUF-20, AUF-25)."""

from arbiter.domaene.spielobjekte import Einheit, Modell


class Auswahl:
    def __init__(self) -> None:
        self._einheit: Einheit | None = None
        self._modellAlsEbene: Modell | None = None

    @property
    def einheit(self) -> Einheit | None:
        return self._einheit

    def auswählen(self, einheit: Einheit) -> None:
        if einheit is self._einheit:
            return
        self._einheit = einheit
        self._modellAlsEbene = None

    def abwählen(self, einheit: Einheit) -> None:
        if self._einheit is einheit:
            self._einheit = None
            self._modellAlsEbene = None

    def ausgewählt(self, einheit: Einheit) -> bool:
        return einheit is self._einheit

    def ganzeEinheitIstEbene(self, einheit: Einheit) -> bool:
        """Ob Ziehen die ganze ausgewählte Einheit bewegt (AUF-21.1)."""
        return self.ausgewählt(einheit) and self._modellAlsEbene is None

    def modellIstEbene(self, modell: Modell) -> bool:
        """Ob das Modell die Ebene seiner ausgewählten Einheit ist (AUF-25.1)."""
        return self._modellAlsEbene is modell

    def ebeneWählen(self, modell: Modell) -> None:
        self._prüfenDassZurAusgewähltenEinheit(modell)
        self._modellAlsEbene = modell

    def ebeneAbwählen(self, modell: Modell) -> None:
        self._prüfenDassZurAusgewähltenEinheit(modell)
        if self.modellIstEbene(modell):
            self._modellAlsEbene = None

    def modellAusgewählt(self, modell: Modell) -> bool:
        """Alle Modelle der ausgewählten Einheit; ist ein Modell die Ebene, nur dieses."""
        gehörtDazu = self._einheit is not None and modell in self._einheit.modelle
        return gehörtDazu and self._modellAlsEbene in (None, modell)

    def _prüfenDassZurAusgewähltenEinheit(self, modell: Modell) -> None:
        if self._einheit is None or modell not in self._einheit.modelle:
            raise ValueError("Das Modell gehört nicht zur ausgewählten Einheit")
