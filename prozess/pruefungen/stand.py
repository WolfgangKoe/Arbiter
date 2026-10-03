"""Hooks `SessionStart` und `PostToolUse` (auf `Agent`): der Stand in einer Zeile."""

import json
import re
import sys
from pathlib import Path

from agenten import projektordner
from anliegen import anliegenDateien, dranAlsText, nachprüfungenAlsText
from belegung import belegungAusTranskript, punkte, warnschwelle
from codekritik import fälligeKritikAlsText
from gitAufruf import freigabeCommit, gitAusgabe
from plan import itemsOhneLink, offeneItems, offeneItemTexte, zyklus
from rueckverfolgung import fehlendeTests, nenntFehlendes, wartendeAlsText


def aktuelleEtappe(wurzel: Path) -> tuple[int, str] | None:
    dateien = sorted((wurzel / "domaene" / "etappen").glob("*.md"))
    if not dateien:
        return None
    for zeile in dateien[0].read_text(encoding="utf-8").splitlines():
        treffer = re.match(r"# (Etappe\s+(\d+).*)", zeile)
        if treffer:
            return int(treffer.group(2)), treffer.group(1).strip()
    return None


def akzeptanztestsSeit(wurzel: Path, kennung: str) -> bool:
    pfad = "technik/tests/akzeptanz"
    return bool(gitAusgabe(wurzel, "log", "--format=%H", f"{kennung}..HEAD", "--", pfad))


def domänenphase(wurzel: Path, zyklusNummer: int) -> str:
    etappe = aktuelleEtappe(wurzel)
    if etappe is None:
        return "Planer: Etappen aus dem Ziel ableiten"
    nummer, _ = etappe
    if freigabeCommit(wurzel, "Etappe", nummer) is None:
        return f"Etappe {nummer} wartet auf Kritik (Architekt) und Freigabe"
    if not fehlendeTests(wurzel, []):
        return f"Anforderungsautor: Anforderungen zu Plan {zyklusNummer}"
    return (
        f"Planer: Plan {zyklusNummer} mit den Items, die bereit sind (eins genügt, höchstens drei)"
    )


def planOhneFreigabe(wurzel: Path, plan: int) -> str:
    """Nächster Schritt für einen Plan mit Links: Kriterien ohne Test müssen in den Items stehen."""
    fehlende = fehlendeTests(wurzel, [])
    texte = offeneItemTexte(wurzel)
    if texte and not fehlende:
        return f"Anforderungsautor: Kriterien zu den Items von Plan {plan}"
    if any(not any(nenntFehlendes([text], fehlend) for fehlend in fehlende) for text in texte):
        return f"Planer: Kriterien-IDs in die Items von Plan {plan}"
    return f"Plan {plan} wartet auf Kritik (Architekt) und Freigabe"


def lage(wurzel: Path) -> tuple[int, str, str]:
    """Zyklus, Phase und nächster Schritt aus den Artefakten in `handoff/` und git."""
    handoff = wurzel / "handoff"
    plan, review, retro = (zyklus(handoff / f"{name}.md") for name in ("plan", "review", "retro"))
    if plan is None:
        return 1, "Domänenphase", domänenphase(wurzel, 1)
    freigabePlan = freigabeCommit(wurzel, "Plan", plan)
    if freigabePlan is None and itemsOhneLink(wurzel):
        return plan, "Domänenphase", f"Planer: Items von Plan {plan} als Link auf domaene/items/"
    if freigabePlan is None:
        return plan, "Domänenphase", planOhneFreigabe(wurzel, plan)
    items = offeneItems(wurzel)
    if (items or review != plan) and not akzeptanztestsSeit(wurzel, freigabePlan):
        return plan, "Technikphase", f"Testautor: Akzeptanztests zu den Items von Plan {plan}"
    if items:
        return (
            plan,
            "Technikphase",
            "Implementierer und Reviewer, dann Fachkritiker: Abnahme, "
            f"Planer löscht das Item (Items von Plan {plan})",
        )
    if review != plan:
        return plan, "Technikphase", f"Reviewer: Review {plan}"
    if retro != plan:
        return plan, "Prozessphase", f"Organisationsentwickler: Retro {plan}"
    if freigabeCommit(wurzel, "Retro", plan) is None:
        return plan, "Prozessphase", f"Retro {plan} wartet auf Kritik und Freigabe"
    return plan + 1, "Domänenphase", domänenphase(wurzel, plan + 1)


def belegungsText(transkript: Path | None) -> str:
    belegung = belegungAusTranskript(transkript) if transkript else None
    if belegung is None:
        return ""
    hinweis = ", neuer Chat empfohlen" if belegung >= warnschwelle else ""
    return f"Belegung {punkte(belegung)}/{punkte(warnschwelle)} Token{hinweis}"


def stand(wurzel: Path, transkript: Path | None = None) -> str:
    zyklusNummer, phase, schritt = lage(wurzel)
    etappe = aktuelleEtappe(wurzel)
    änderungen = gitAusgabe(wurzel, "status", "--porcelain").splitlines()
    uncommittet = [zeile for zeile in änderungen if zeile]
    teile = [
        etappe[1] if etappe else "Keine Etappe",
        f"Zyklus {zyklusNummer}, {phase}",
        f"Nächster Schritt: {schritt}",
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
    eingabe = json.load(sys.stdin)
    transkript = eingabe.get("transcript_path")
    print(
        json.dumps(
            {
                "hookSpecificOutput": {
                    "hookEventName": eingabe.get("hook_event_name", "SessionStart"),
                    "additionalContext": stand(
                        projektordner(), Path(transkript) if transkript else None
                    ),
                }
            },
            ensure_ascii=False,
        )
    )
