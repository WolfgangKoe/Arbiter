"""Hook SubagentStop: trägt Rolle, Auftrag, Modell, Belegung, Dauer und Zyklus ins Lauf-Log ein."""

import json
import re
from datetime import datetime
from pathlib import Path

from agenten import projektordner
from belegung import belegungAusTranskript, eigenesTranskript
from hookProtokoll import eingabeLesen

pflichtfelder = ("zeit", "rolle", "belegung")
zielLänge = 80
koordinatorVorspann = "The coordinator sent a message while you were working:"
hinweisBlock = re.compile(r"<system-reminder>.*?</system-reminder>", re.DOTALL)
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


def transkriptEinträge(transkript: Path) -> list[dict]:
    """Die Einträge mit Nachricht, ohne Meta-Einträge außer Nachrichten des Koordinators."""
    gefunden = []
    for zeile in transkript.read_text(encoding="utf-8").splitlines():
        eintrag = eintragAusZeile(zeile, ())
        nachricht = eintrag.get("message") if eintrag else None
        if isinstance(nachricht, dict) and (not eintrag.get("isMeta") or vonKoordinator(nachricht)):
            gefunden.append(eintrag)
    return gefunden


def nachrichten(transkript: Path) -> list[dict]:
    return [eintrag["message"] for eintrag in transkriptEinträge(transkript)]


def vonKoordinator(nachricht: dict) -> bool:
    return koordinatorVorspann in textDerNachricht(nachricht.get("content"))


def gekürzt(text: str) -> str:
    """Kürzt am letzten Leerzeichen vor `zielLänge` und hängt „…“ an."""
    if len(text) <= zielLänge:
        return text
    wortGrenze = text.rfind(" ", 0, zielLänge)
    return text[: wortGrenze if wortGrenze > 0 else zielLänge].rstrip() + "…"


def auftragsZeile(text: str) -> str:
    """Erste Zeile des Auftrags ohne Hinweise des Harness, Vorspann und „Ziel:“."""
    zeilen = hinweisBlock.sub("", text).replace(koordinatorVorspann, "").splitlines()
    erste = next((zeile.strip() for zeile in zeilen if zeile.strip()), "")
    return gekürzt(erste.removeprefix("Ziel:").strip())


def zielUndModell(transkript: Path) -> tuple[str, str]:
    """Erste Zeile des jüngsten Auftrags und Modell; leer, wenn das Transkript sie nicht hat."""
    alle = nachrichten(transkript)
    texte = [
        textDerNachricht(nachricht.get("content")).strip()
        for nachricht in alle
        if nachricht.get("role") == "user"
    ]
    jüngster = next((text for text in reversed(texte) if auftragsZeile(text)), "")
    ziel = auftragsZeile(jüngster)
    modelle = [
        nachricht.get("model")
        for nachricht in alle
        if nachricht.get("role") == "assistant" and nachricht.get("model")
    ]
    return ziel, next((modell for modell in reversed(modelle) if modell != "<synthetic>"), "")


def zeitstempel(eintrag: dict) -> datetime | None:
    try:
        return datetime.fromisoformat(eintrag["timestamp"])
    except (KeyError, TypeError, ValueError):
        return None


def dauerSekunden(transkript: Path) -> int | None:
    """Sekunden vom jüngsten Auftrag bis zur letzten Zeile; `None`, wenn Zeitstempel fehlen."""
    alle = transkriptEinträge(transkript)
    beginne = [
        zeitstempel(eintrag)
        for eintrag in alle
        if eintrag["message"].get("role") == "user"
        and auftragsZeile(textDerNachricht(eintrag["message"].get("content")))
    ]
    ende = [zeit for eintrag in alle if (zeit := zeitstempel(eintrag))]
    beginn = next((zeit for zeit in reversed(beginne) if zeit), None)
    return round((max(ende) - beginn).total_seconds()) if beginn and ende else None


def zyklusUndPhase(ordner: Path) -> tuple[int, str]:
    from phasenfolge import lage  # Warum: lädt git und die Plandateien nur beim Eintragen

    gefunden = lage(ordner)
    return gefunden.zyklus, str(gefunden.phase)


def koordinatorStand(eingabe: dict) -> int | None:
    haupt = eingabe.get("transcript_path")
    return belegungAusTranskript(Path(haupt)) if eingabe.get("agent_id") and haupt else None


def laufEintrag(eingabe: dict, zeit: datetime, ordner: Path | None = None) -> dict | None:
    """Der Eintrag zu einem Rollenlauf; `None`, wenn Rolle oder Belegung fehlen."""
    rolle = eingabe.get("agent_type")
    transkript = eigenesTranskript(eingabe)
    belegung = belegungAusTranskript(transkript) if transkript else None
    if not rolle or belegung is None:
        return None
    ziel, modell = zielUndModell(transkript)
    zyklus, phase = zyklusUndPhase(ordner) if ordner else (None, None)
    return {
        "zeit": zeit.isoformat(timespec="seconds"),
        "rolle": rolle,
        "agent_id": eingabe.get("agent_id"),
        "sitzung": eingabe.get("session_id"),
        "belegung": belegung,
        "ziel": ziel,
        "modell": modell,
        "koordinator": koordinatorStand(eingabe),
        "dauer": dauerSekunden(transkript),
        "zyklus": zyklus,
        "phase": phase,
        "stopp_wiederholt": bool(eingabe.get("stop_hook_active")),
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
            continue
        eintrag = dict(eintrag)
        ergebnis.append(eintrag)
        if laufId:
            behalten[laufId] = eintrag
    return ergebnis[::-1]


if __name__ == "__main__":
    try:
        from dashboard import dashboardSchreiben

        ordner = projektordner()
        gefunden = laufEintrag(eingabeLesen(), jetzt(), ordner)
        if gefunden:
            eintragAnhängen(ordner, gefunden)
            dashboardSchreiben(ordner)
    except Exception:  # Warum: eine Messung, die scheitert, darf keinen Rollenlauf beenden
        pass
