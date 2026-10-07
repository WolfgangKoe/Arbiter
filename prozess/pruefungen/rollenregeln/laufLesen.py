"""Liest das Lauf-Log (`prozess/dashboard/laeufe.jsonl`) und führt geteilte Läufe zusammen."""

import json
from pathlib import Path
from typing import NamedTuple

pflichtfelder = ("zeit", "rolle", "belegung")
logOrdner = "prozess/dashboard"
logDatei = "laeufe.jsonl"


class Lauf(NamedTuple):
    zeit: str
    rolle: str
    belegung: int
    agentId: str | None = None
    sitzung: str | None = None
    ziel: str | None = None
    modell: str | None = None
    koordinator: int | None = None
    dauer: int | None = None
    zyklus: int | None = None
    phase: str | None = None
    stoppWiederholt: bool = False

    @classmethod
    def ausEintrag(cls, eintrag: dict) -> "Lauf":
        felder = {name: eintrag.get(logFeld(name)) for name in cls._fields}
        felder["stoppWiederholt"] = bool(felder["stoppWiederholt"])
        return cls(**felder)

    def alsEintrag(self) -> dict:
        return {logFeld(name): wert for name, wert in self._asdict().items()}


logFelder = {"agentId": "agent_id", "stoppWiederholt": "stopp_wiederholt"}


def logFeld(name: str) -> str:
    return logFelder.get(name, name)


def logPfad(wurzel: Path) -> Path:
    return wurzel / logOrdner / logDatei


def eintragAusZeile(zeile: str, pflicht: tuple = pflichtfelder) -> dict | None:
    """Der Eintrag einer Zeile; `None` bei leerer, unlesbarer oder unvollständiger Zeile."""
    try:
        eintrag = json.loads(zeile)
    except json.JSONDecodeError:
        return None
    if not isinstance(eintrag, dict) or not all(feld in eintrag for feld in pflicht):
        return None
    return eintrag


def dauerSumme(spät: Lauf, früh: Lauf) -> int | None:
    """Beide Teile des Laufs zusammen; die Rückmeldung des Hooks zählt ab ihrem Beginn."""
    teile = (spät.dauer, früh.dauer)
    return sum(teile) if all(teil is not None for teil in teile) else spät.dauer


def läufeLesen(wurzel: Path) -> list[Lauf]:
    datei = logPfad(wurzel)
    if not datei.is_file():
        return []
    gelesen = [
        Lauf.ausEintrag(eintrag)
        for zeile in datei.read_text(encoding="utf-8").splitlines()
        if (eintrag := eintragAusZeile(zeile)) is not None
    ]
    späterer: dict[str, Lauf] = {}
    platzVon: dict[str, int] = {}
    ergebnis: list[Lauf] = []
    for lauf in reversed(gelesen):
        spät = späterer.get(lauf.agentId) if lauf.agentId else None
        if lauf.agentId:
            späterer[lauf.agentId] = lauf
        if spät and spät.stoppWiederholt:
            platz = platzVon[lauf.agentId]
            behalten = ergebnis[platz]
            # Warum: gilt dem Auftrag davor
            ergebnis[platz] = behalten._replace(ziel=lauf.ziel, dauer=dauerSumme(behalten, lauf))
            continue
        if lauf.agentId:
            platzVon[lauf.agentId] = len(ergebnis)
        ergebnis.append(lauf)
    return ergebnis[::-1]
