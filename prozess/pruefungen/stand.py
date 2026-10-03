"""Hooks `SessionStart` und `PostToolUse` (auf `Agent`): der Stand in einer Zeile."""

from pathlib import Path

from agenten import projektordner
from anliegen import anliegenDateien, dranAlsText, nachprüfungenAlsText
from belegung import belegungAusTranskript, punkte, warnschwelle
from codekritik import fälligeKritikAlsText
from gitAufruf import gitAusgabe
from hookProtokoll import antwortAusgeben, eingabeLesen, zusatzkontext
from phasenfolge import aktuelleEtappe, lage
from rueckverfolgung import wartendeAlsText


def belegungsText(transkript: Path | None) -> str:
    belegung = belegungAusTranskript(transkript) if transkript else None
    if belegung is None:
        return ""
    hinweis = ", neuer Chat empfohlen" if belegung >= warnschwelle else ""
    return f"Belegung {punkte(belegung)}/{punkte(warnschwelle)} Token{hinweis}"


def stand(wurzel: Path, transkript: Path | None = None) -> str:
    aktuelle = lage(wurzel)
    etappe = aktuelleEtappe(wurzel)
    änderungen = gitAusgabe(wurzel, "status", "--porcelain").splitlines()
    uncommittet = [zeile for zeile in änderungen if zeile]
    teile = [
        etappe.titel if etappe else "Keine Etappe",
        f"Zyklus {aktuelle.zyklus}, {aktuelle.phase}",
        f"Nächster Schritt: {aktuelle.schritt}",
        belegungsText(transkript),
        f"{len(anliegenDateien(wurzel))} offene Anliegen",
        dranAlsText(wurzel),
        nachprüfungenAlsText(wurzel),
        wartendeAlsText(wurzel),
        fälligeKritikAlsText(wurzel),
        f"{len(uncommittet)} uncommittete Dateien",
    ]
    return "Stand: " + " · ".join(teil for teil in teile if teil)


if __name__ == "__main__":
    eingabe = eingabeLesen()
    transkript = eingabe.get("transcript_path")
    ereignis = eingabe.get("hook_event_name", "SessionStart")
    antwortAusgeben(
        zusatzkontext(ereignis, stand(projektordner(), Path(transkript) if transkript else None))
    )
