"""Liest das Lauf-Log (`prozess/dashboard/laeufe.jsonl`) und führt geteilte Läufe zusammen."""

import json
from pathlib import Path

pflichtfelder = ("zeit", "rolle", "belegung")
logOrdner = "prozess/dashboard"
logDatei = "laeufe.jsonl"


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


def dauerSumme(spät: dict, früh: dict) -> int | None:
    """Beide Teile des Laufs zusammen; die Rückmeldung des Hooks zählt ab ihrem Beginn."""
    teile = (spät.get("dauer"), früh.get("dauer"))
    return sum(teile) if all(teil is not None for teil in teile) else spät.get("dauer")


def läufeLesen(wurzel: Path) -> list[dict]:
    datei = logPfad(wurzel)
    if not datei.is_file():
        return []
    gelesen = [
        eintrag
        for zeile in datei.read_text(encoding="utf-8").splitlines()
        if (eintrag := eintragAusZeile(zeile)) is not None
    ]
    späterer: dict = {}
    behalten: dict = {}
    ergebnis = []
    for eintrag in reversed(gelesen):
        laufId = eintrag.get("agent_id")
        spät = späterer.get(laufId) if laufId else None
        if laufId:
            späterer[laufId] = eintrag
        if spät and spät.get("stopp_wiederholt"):
            behalten[laufId]["ziel"] = eintrag.get("ziel")  # Warum: gilt dem Auftrag davor
            behalten[laufId]["dauer"] = dauerSumme(behalten[laufId], eintrag)
            continue
        eintrag = dict(eintrag)
        ergebnis.append(eintrag)
        if laufId:
            behalten[laufId] = eintrag
    return ergebnis[::-1]
