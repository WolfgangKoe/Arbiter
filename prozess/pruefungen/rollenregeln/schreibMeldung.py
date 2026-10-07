"""Hook (PostToolUse): Meldungen der Schreibbilanz erreichen den Koordinator."""

from pathlib import Path

from gemeinsam.hookProtokoll import HookEingabe, antwortAusgeben, eingabeLesen, zusatzkontext
from gemeinsam.pfade import projektordner
from rollenregeln.schreibBilanz import meldungsOrdner


def entscheide(daten: dict, wurzel: Path) -> dict | None:
    if HookEingabe.aus(daten).agentId:
        return None
    dateien = sorted(meldungsOrdner(wurzel).glob("*.txt"))
    if not dateien:
        return None
    texte = [datei.read_text(encoding="utf-8") for datei in dateien]
    for datei in dateien:
        datei.unlink()
    return zusatzkontext("PostToolUse", " ".join(texte))


if __name__ == "__main__":
    antwortAusgeben(entscheide(eingabeLesen(), projektordner()))
