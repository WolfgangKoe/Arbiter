"""Hooks `SessionStart` und `PostToolUse` (auf `Agent`): der Stand in einer Zeile."""

from pathlib import Path

from gemeinsam.gitAufruf import gitAusgabe
from gemeinsam.hookProtokoll import HookEingabe, antwortAusgeben, eingabeLesen, zusatzkontext
from gemeinsam.pfade import projektordner
from kriterienregeln.rueckverfolgung import wartendeAlsText
from lesen.anliegenKopf import anliegenDateien
from standregeln.anliegenText import dranAlsText, nachprüfungenAlsText
from standregeln.belegung import belegungAusTranskript, punkte, warnschwelle
from standregeln.codekritik import fälligeKritikAlsText
from standregeln.freigabeKommentare import autorenDran, freigabeZuCommitten
from standregeln.phasenfolge import aktuelleEtappe, lage


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
    committen = freigabeZuCommitten(wurzel)
    schritt = f"Koordinator: {committen} committen" if committen else aktuelle.schritt
    teile = [
        etappe.titel if etappe else "Keine Etappe",
        f"Zyklus {aktuelle.zyklus}, {aktuelle.phase}",
        f"Nächster Schritt: {schritt}",
        belegungsText(transkript),
        f"{len(anliegenDateien(wurzel))} offene Anliegen",
        dranAlsText(wurzel, autorenDran(wurzel)),
        nachprüfungenAlsText(wurzel),
        wartendeAlsText(wurzel),
        fälligeKritikAlsText(wurzel),
        f"{len(uncommittet)} uncommittete Dateien",
    ]
    return "Stand: " + " · ".join(teil for teil in teile if teil)


if __name__ == "__main__":
    eingabe = HookEingabe.aus(eingabeLesen())
    ereignis = eingabe.ereignis or "SessionStart"
    antwortAusgeben(zusatzkontext(ereignis, stand(projektordner(), eingabe.transkript)))
