"""Hook SubagentStop: trägt Rolle und Belegung des Laufs ins Lauf-Log ein."""

import json
from datetime import datetime
from pathlib import Path

from agenten import projektordner
from belegung import belegungAusTranskript, eigenesTranskript
from hookProtokoll import eingabeLesen

logOrdner = "prozess/dashboard"
logDatei = "laeufe.jsonl"


def logPfad(wurzel: Path) -> Path:
    return wurzel / logOrdner / logDatei


def laufEintrag(eingabe: dict, zeit: datetime) -> dict | None:
    """Der Eintrag zu einem Rollenlauf; `None`, wenn Rolle oder Belegung fehlen."""
    rolle = eingabe.get("agent_type")
    transkript = eigenesTranskript(eingabe)
    belegung = belegungAusTranskript(transkript) if transkript else None
    if not rolle or belegung is None:
        return None
    return {
        "zeit": zeit.isoformat(timespec="seconds"),
        "rolle": rolle,
        "agent_id": eingabe.get("agent_id"),
        "sitzung": eingabe.get("session_id"),
        "belegung": belegung,
    }


def eintragAnhängen(wurzel: Path, eintrag: dict) -> None:
    datei = logPfad(wurzel)
    datei.parent.mkdir(parents=True, exist_ok=True)
    with datei.open("a", encoding="utf-8") as ziel:
        ziel.write(json.dumps(eintrag, ensure_ascii=False) + "\n")


def eintragAusZeile(zeile: str) -> dict | None:
    """Der Eintrag einer Zeile; `None` bei leerer oder unlesbarer Zeile."""
    try:
        eintrag = json.loads(zeile)
    except json.JSONDecodeError:
        return None
    return eintrag if isinstance(eintrag, dict) else None


def läufeLesen(wurzel: Path) -> list[dict]:
    datei = logPfad(wurzel)
    if not datei.is_file():
        return []
    gelesen = [
        eintrag
        for zeile in datei.read_text(encoding="utf-8").splitlines()
        if (eintrag := eintragAusZeile(zeile)) is not None
    ]
    letzte = {
        eintrag["agent_id"]: nummer
        for nummer, eintrag in enumerate(gelesen)
        if eintrag.get("agent_id")
    }
    return [
        eintrag
        for nummer, eintrag in enumerate(gelesen)
        if letzte.get(eintrag.get("agent_id"), nummer) == nummer
    ]


if __name__ == "__main__":
    try:
        from dashboard import dashboardSchreiben

        ordner = projektordner()
        gefunden = laufEintrag(eingabeLesen(), datetime.now().astimezone())
        if gefunden:
            eintragAnhängen(ordner, gefunden)
            dashboardSchreiben(ordner)
    except Exception:  # Warum: eine Messung, die scheitert, darf keinen Rollenlauf beenden
        pass
