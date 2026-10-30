from collections.abc import Mapping

from arbiter.domaene.querschnitt.setzen import gesetzteModelle
from arbiter.domaene.spielobjekte import Einheit, Modell, Stelle


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
            self.auswahlAufheben()

    def auswahlAufheben(self) -> None:
        self._einheit = None
        self._modellAlsEbene = None

    def ausgewählt(self, einheit: Einheit) -> bool:
        return einheit is self._einheit

    def ganzeEinheitIstEbene(self, einheit: Einheit) -> bool:
        return self.ausgewählt(einheit) and self._modellAlsEbene is None

    def ebene(
        self, einheit: Einheit, gezogenes: Modell, stellen: Mapping[Modell, Stelle]
    ) -> dict[Modell, Stelle]:
        if self.ganzeEinheitIstEbene(einheit):
            return gesetzteModelle(einheit, stellen)
        return {gezogenes: stellen[gezogenes]} if gezogenes in stellen else {}

    def ebeneDerAuswahl(self, stellen: Mapping[Modell, Stelle]) -> dict[Modell, Stelle]:
        if self._einheit is None:
            return {}
        if self._modellAlsEbene is None:
            return gesetzteModelle(self._einheit, stellen)
        return self.ebene(self._einheit, self._modellAlsEbene, stellen)

    def modellIstEbene(self, modell: Modell) -> bool:
        return self._modellAlsEbene is modell

    def modellAnklicken(self, einheit: Einheit, modell: Modell) -> None:
        if not self.ausgewählt(einheit):
            self.auswählen(einheit)
        elif self.modellIstEbene(modell):
            self.ebeneAbwählen(modell)
        else:
            self.ebeneWählen(modell)

    def ebeneWählen(self, modell: Modell) -> None:
        self._prüfenDassZurAusgewähltenEinheit(modell)
        self._modellAlsEbene = modell

    def ebeneAbwählen(self, modell: Modell) -> None:
        self._prüfenDassZurAusgewähltenEinheit(modell)
        if self.modellIstEbene(modell):
            self._modellAlsEbene = None

    def ganzeEinheitAlsEbene(self, einheit: Einheit) -> None:
        if self.ausgewählt(einheit):
            self._modellAlsEbene = None

    def modellAusgewählt(self, modell: Modell) -> bool:
        gehörtDazu = self._einheit is not None and modell in self._einheit.modelle
        return gehörtDazu and self._modellAlsEbene in (None, modell)

    def _prüfenDassZurAusgewähltenEinheit(self, modell: Modell) -> None:
        if self._einheit is None or modell not in self._einheit.modelle:
            raise ValueError("Das Modell gehört nicht zur ausgewählten Einheit")
