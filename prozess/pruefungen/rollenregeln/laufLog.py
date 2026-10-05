"""Hook SubagentStop: trägt Rolle, Auftrag, Modell, Belegung, Dauer und Zyklus ins Lauf-Log ein."""

import json
import re
from datetime import datetime
from pathlib import Path

from gemeinsam.hookProtokoll import HookEingabe, eingabeLesen
from gemeinsam.pfade import projektordner
from rollenregeln.dashboard import dashboardSchreiben
from rollenregeln.laufLesen import Lauf, eintragAusZeile, logPfad
from standregeln.belegung import belegungAusTranskript, eigenesTranskript

zielLänge = 80
koordinatorVorspann = "The coordinator sent a message while you were working:"
hinweisBlock = re.compile(r"<system-reminder>.*?</system-reminder>", re.DOTALL)


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


def zielUndModell(einträge: list[dict]) -> tuple[str, str]:
    """Erste Zeile des jüngsten Auftrags und Modell; leer, wenn das Transkript sie nicht hat."""
    alle = [eintrag["message"] for eintrag in einträge]
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


def dauerSekunden(alle: list[dict]) -> int | None:
    """Sekunden vom jüngsten Auftrag bis zur letzten Zeile; `None`, wenn Zeitstempel fehlen."""
    beginne = [
        zeitstempel(eintrag)
        for eintrag in alle
        if eintrag["message"].get("role") == "user"
        and auftragsZeile(textDerNachricht(eintrag["message"].get("content")))
    ]
    ende = [zeit for eintrag in alle if (zeit := zeitstempel(eintrag))]
    beginn = next((zeit for zeit in reversed(beginne) if zeit), None)
    return round((max(ende) - beginn).total_seconds()) if beginn and ende else None


def zyklusUndPhase(ordner: Path) -> tuple[int | None, str | None]:
    """Zyklus und Phase; leer, wenn die Lage nicht zu lesen ist (der Titel ist nur Zugabe)."""
    from standregeln.phasenfolge import (
        lage,  # Warum: lädt git und die Plandateien nur beim Eintragen
    )

    try:
        gefunden = lage(ordner)
    except Exception:  # Warum: halb geschriebene Dateien dürfen den Eintrag nicht kosten
        return None, None
    return gefunden.zyklus, str(gefunden.phase)


def koordinatorStand(eingabe: HookEingabe) -> int | None:
    haupt = eingabe.transkript
    return belegungAusTranskript(haupt) if eingabe.agentId and haupt else None


def laufEintrag(eingabe: HookEingabe, zeit: datetime, ordner: Path) -> Lauf | None:
    """Der Eintrag zu einem Rollenlauf; `None`, wenn Rolle oder Belegung fehlen."""
    rolle = eingabe.rolle
    transkript = eigenesTranskript(eingabe)
    belegung = belegungAusTranskript(transkript) if transkript else None
    if not rolle or belegung is None:
        return None
    einträge = transkriptEinträge(transkript)
    ziel, modell = zielUndModell(einträge)
    zyklus, phase = zyklusUndPhase(ordner)
    return Lauf(
        zeit=zeit.isoformat(timespec="seconds"),
        rolle=rolle,
        belegung=belegung,
        agentId=eingabe.agentId,
        sitzung=eingabe.sitzung,
        ziel=ziel,
        modell=modell,
        koordinator=koordinatorStand(eingabe),
        dauer=dauerSekunden(einträge),
        zyklus=zyklus,
        phase=phase,
        stoppWiederholt=eingabe.stoppWiederholt,
    )


def eintragAnhängen(wurzel: Path, lauf: Lauf) -> None:
    datei = logPfad(wurzel)
    datei.parent.mkdir(parents=True, exist_ok=True)
    with datei.open("a", encoding="utf-8") as ziel:
        ziel.write(json.dumps(lauf.alsEintrag(), ensure_ascii=False) + "\n")


def protokollieren(eingabe: HookEingabe, ordner: Path) -> None:
    """Trägt den Lauf ein und schreibt das Dashboard neu."""
    gefunden = laufEintrag(eingabe, jetzt(), ordner)
    if gefunden:
        eintragAnhängen(ordner, gefunden)
        dashboardSchreiben(ordner)


if __name__ == "__main__":
    try:
        protokollieren(HookEingabe.aus(eingabeLesen()), projektordner())
    except Exception:  # Warum: eine Messung, die scheitert, darf keinen Rollenlauf beenden
        pass
