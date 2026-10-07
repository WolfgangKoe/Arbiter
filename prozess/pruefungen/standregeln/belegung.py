"""Hook (PreToolUse, PostToolUse): Belegung des Kontextfensters je Lauf, für alle Agenten."""

import json
from pathlib import Path

from gemeinsam.hookProtokoll import (
    HookEingabe,
    antwortAusgeben,
    eingabeLesen,
    verweigerung,
    zusatzkontext,
)
from gemeinsam.pfade import projektordner

warnschwelle = 120_000
sperrschwelle = 150_000
belegungsfelder = ("input_tokens", "cache_creation_input_tokens", "cache_read_input_tokens")
erlaubteWerkzeuge = ("Write", "Edit", "NotebookEdit", "SubagentHandback")


def belegungAusZeile(zeile: str) -> int | None:
    if '"usage"' not in zeile:
        return None
    try:
        eintrag = json.loads(zeile)
    except json.JSONDecodeError:
        return None
    nutzung = (eintrag.get("message") or {}).get("usage")
    if eintrag.get("isApiErrorMessage") or not isinstance(nutzung, dict):
        return None
    belegung = sum(nutzung.get(feld) or 0 for feld in belegungsfelder)
    return belegung or None


def belegungAusTranskript(transkript: Path) -> int | None:
    """Belegung der jüngsten brauchbaren Anfrage; `None`, wenn das Transkript sie nicht hat."""
    if not transkript.is_file():
        return None
    for zeile in reversed(transkript.read_text(encoding="utf-8").splitlines()):
        belegung = belegungAusZeile(zeile)
        if belegung is not None:
            return belegung
    return None


def eigenesTranskript(eingabe: HookEingabe) -> Path | None:
    """Rollen haben ein eigenes Transkript; das der Eingabe ist dann das des Koordinators."""
    if not eingabe.agentId:
        return eingabe.transkript
    if eingabe.rollenTranskript:
        return eingabe.rollenTranskript
    if not (eingabe.transkript and eingabe.sitzung):
        return None
    treffer = sorted(
        (eingabe.transkript.parent / eingabe.sitzung).rglob(f"agent-{eingabe.agentId}.jsonl")
    )
    return treffer[0] if treffer else None


def freigabedatei(wurzel: Path) -> Path:
    return wurzel / ".git" / "arbiter" / "belegungsgrenze.txt"


def geltendeSperrschwelle(wurzel: Path) -> int:
    try:
        return max(sperrschwelle, int(freigabedatei(wurzel).read_text(encoding="utf-8").strip()))
    except (OSError, ValueError):
        return sperrschwelle


def meldungsdatei(wurzel: Path, schlüssel: str) -> Path:
    return wurzel / ".git" / "arbiter" / "belegung" / f"{schlüssel}.txt"


def punkte(zahl: int) -> str:
    return f"{zahl:,}".replace(",", ".")


def vorWerkzeug(eingabe: HookEingabe, wurzel: Path) -> dict | None:
    if not eingabe.rolle or eingabe.werkzeug in erlaubteWerkzeuge:
        return None
    transkript = eigenesTranskript(eingabe)
    belegung = belegungAusTranskript(transkript) if transkript else None
    grenze = geltendeSperrschwelle(wurzel)
    if belegung is None or belegung < grenze:
        return None
    if eingabe.agentId:
        weiter = "Schreibe nur noch in deinem Pfad und schließe mit der Schlussantwort ab."
    else:
        weiter = (
            "Der Stakeholder entscheidet: freigeben (höhere Grenze in "
            f"{freigabedatei(wurzel).relative_to(wurzel)}), kürzen oder neuer Chat."
        )
    return verweigerung(
        f"Belegung {punkte(belegung)} Token, Sperrschwelle {punkte(grenze)}. {weiter}"
    )


def nachWerkzeug(eingabe: HookEingabe, wurzel: Path) -> dict | None:
    rolle = eingabe.rolle
    transkript = eigenesTranskript(eingabe)
    belegung = belegungAusTranskript(transkript) if transkript else None
    if not rolle or belegung is None or belegung < warnschwelle:
        return None
    datei = meldungsdatei(wurzel, eingabe.agentId or eingabe.sitzung or "haupt")
    if datei.exists():
        return None
    datei.parent.mkdir(parents=True, exist_ok=True)
    datei.write_text(str(belegung), encoding="utf-8")
    if eingabe.agentId:
        folge = "Beginne nichts Neues, schließe ab und melde mit der Schlussantwort."
    else:
        folge = "Beginne nichts Neues und empfiehl dem Stakeholder einen neuen Chat."
    text = (
        f"Belegung {punkte(belegung)} Token, Warnschwelle {punkte(warnschwelle)}. {folge} "
        f"Ab {punkte(sperrschwelle)} sperrt ein Hook alles außer Schreiben im eigenen Pfad."
    )
    return zusatzkontext("PostToolUse", text)


def entscheide(daten: dict, wurzel: Path) -> dict | None:
    eingabe = HookEingabe.aus(daten)
    if eingabe.ereignis == "PreToolUse":
        return vorWerkzeug(eingabe, wurzel)
    if eingabe.ereignis == "PostToolUse":
        return nachWerkzeug(eingabe, wurzel)
    return None


if __name__ == "__main__":
    try:
        antwort = entscheide(eingabeLesen(), projektordner())
    except Exception:  # Warum: eine Messung, die scheitert, darf keinen Werkzeugaufruf sperren
        antwort = None
    antwortAusgeben(antwort)
