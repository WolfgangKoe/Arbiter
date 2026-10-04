"""Hook SubagentStop: trägt Rolle, Auftrag, Modell und Belegung des Laufs ins Lauf-Log ein."""

import json
from datetime import datetime
from pathlib import Path

from agenten import projektordner
from belegung import belegungAusTranskript, eigenesTranskript
from hookProtokoll import eingabeLesen

pflichtfelder = ("zeit", "rolle", "belegung")
zielLänge = 80
logOrdner = "prozess/dashboard"
logDatei = "laeufe.jsonl"


def logPfad(wurzel: Path) -> Path:
    return wurzel / logOrdner / logDatei


def jetzt() -> datetime:
    return datetime.now().astimezone()


def textDerNachricht(inhalt) -> str:
    if isinstance(inhalt, str):
        return inhalt
    return " ".join(block.get("text", "") for block in inhalt or [] if isinstance(block, dict))


def nachrichten(transkript: Path) -> list[dict]:
    gefunden = []
    for zeile in transkript.read_text(encoding="utf-8").splitlines():
        eintrag = eintragAusZeile(zeile, ())
        nachricht = eintrag.get("message") if eintrag else None
        if isinstance(nachricht, dict):
            gefunden.append(nachricht)
    return gefunden


def zielUndModell(transkript: Path) -> tuple[str, str]:
    """Erste Zeile des Auftrags und Modell des Laufs; leer, wenn das Transkript sie nicht hat."""
    alle = nachrichten(transkript)
    texte = [
        textDerNachricht(nachricht.get("content")).strip()
        for nachricht in alle
        if nachricht.get("role") == "user"
    ]
    erste = next((text for text in texte if text), "")
    ziel = erste.splitlines()[0].removeprefix("Ziel:").strip()[:zielLänge] if erste else ""
    modelle = [
        nachricht.get("model")
        for nachricht in alle
        if nachricht.get("role") == "assistant" and nachricht.get("model")
    ]
    return ziel, next((modell for modell in reversed(modelle) if modell != "<synthetic>"), "")


def koordinatorStand(eingabe: dict) -> int | None:
    haupt = eingabe.get("transcript_path")
    return belegungAusTranskript(Path(haupt)) if eingabe.get("agent_id") and haupt else None


def laufEintrag(eingabe: dict, zeit: datetime) -> dict | None:
    """Der Eintrag zu einem Rollenlauf; `None`, wenn Rolle oder Belegung fehlen."""
    rolle = eingabe.get("agent_type")
    transkript = eigenesTranskript(eingabe)
    belegung = belegungAusTranskript(transkript) if transkript else None
    if not rolle or belegung is None:
        return None
    ziel, modell = zielUndModell(transkript)
    return {
        "zeit": zeit.isoformat(timespec="seconds"),
        "rolle": rolle,
        "agent_id": eingabe.get("agent_id"),
        "sitzung": eingabe.get("session_id"),
        "belegung": belegung,
        "ziel": ziel,
        "modell": modell,
        "koordinator": koordinatorStand(eingabe),
    }


def eintragAnhängen(wurzel: Path, eintrag: dict) -> None:
    datei = logPfad(wurzel)
    datei.parent.mkdir(parents=True, exist_ok=True)
    with datei.open("a", encoding="utf-8") as ziel:
        ziel.write(json.dumps(eintrag, ensure_ascii=False) + "\n")


def eintragAusZeile(zeile: str, pflicht: tuple = pflichtfelder) -> dict | None:
    """Der Eintrag einer Zeile; `None` bei leerer, unlesbarer oder unvollständiger Zeile."""
    try:
        eintrag = json.loads(zeile)
    except json.JSONDecodeError:
        return None
    if not isinstance(eintrag, dict) or not all(feld in eintrag for feld in pflicht):
        return None
    return eintrag


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
        gefunden = laufEintrag(eingabeLesen(), jetzt())
        if gefunden:
            eintragAnhängen(ordner, gefunden)
            dashboardSchreiben(ordner)
    except Exception:  # Warum: eine Messung, die scheitert, darf keinen Rollenlauf beenden
        pass
