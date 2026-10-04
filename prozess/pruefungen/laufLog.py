"""Hook SubagentStop: trägt Rolle und Belegung des Laufs ins Lauf-Log ein."""

import json
from datetime import UTC, datetime
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
    return {"zeit": zeit.isoformat(timespec="seconds"), "rolle": rolle, "belegung": belegung}


def eintragAnhängen(wurzel: Path, eintrag: dict) -> None:
    datei = logPfad(wurzel)
    datei.parent.mkdir(parents=True, exist_ok=True)
    with datei.open("a", encoding="utf-8") as ziel:
        ziel.write(json.dumps(eintrag, ensure_ascii=False) + "\n")


def läufeLesen(wurzel: Path) -> list[dict]:
    datei = logPfad(wurzel)
    if not datei.is_file():
        return []
    zeilen = datei.read_text(encoding="utf-8").splitlines()
    return [json.loads(zeile) for zeile in zeilen if zeile.strip()]


if __name__ == "__main__":
    try:
        from dashboard import dashboardSchreiben

        ordner = projektordner()
        gefunden = laufEintrag(eingabeLesen(), datetime.now(UTC))
        if gefunden:
            eintragAnhängen(ordner, gefunden)
            dashboardSchreiben(ordner)
    except Exception:  # Warum: eine Messung, die scheitert, darf keinen Rollenlauf beenden
        pass
