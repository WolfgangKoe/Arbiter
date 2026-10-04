"""Die Lage des Zyklus: Phase und nächster Schritt aus den Artefakten in `handoff/` und git."""

import re
from enum import StrEnum
from pathlib import Path
from typing import NamedTuple

from gitAufruf import betreffeSeit, freigabeCommit, gitAusgabe
from pfade import akzeptanzOrdner, etappenOrdner, itemsOrdner
from plan import itemsOhneLink, offeneItems, offeneItemTexte, zyklus
from rueckverfolgung import fehlendeTests, nenntFehlendes


class Phase(StrEnum):
    domänenphase = "Domänenphase"
    technikphase = "Technikphase"
    prozessphase = "Prozessphase"


class Lage(NamedTuple):
    zyklus: int
    phase: Phase
    schritt: str


class Etappe(NamedTuple):
    nummer: int
    titel: str


def aktuelleEtappe(wurzel: Path) -> Etappe | None:
    dateien = sorted((wurzel / etappenOrdner).glob("*.md"))
    if not dateien:
        return None
    for zeile in dateien[0].read_text(encoding="utf-8").splitlines():
        treffer = re.match(r"# (Etappe\s+(\d+).*)", zeile)
        if treffer:
            return Etappe(int(treffer.group(2)), treffer.group(1).strip())
    return None


def akzeptanztestsSeit(wurzel: Path, kennung: str) -> bool:
    return bool(gitAusgabe(wurzel, "log", "--format=%H", f"{kennung}..HEAD", "--", akzeptanzOrdner))


def domänenphase(wurzel: Path, zyklusNummer: int) -> str:
    etappe = aktuelleEtappe(wurzel)
    if etappe is None:
        return "Planer: Etappen aus dem Ziel ableiten"
    nummer = etappe.nummer
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


def prozessItems(retro: Path) -> list[str]:
    """Die Kennungen `P<k>` der Zeilen `- P<k> ` im Abschnitt `## Prozess-Items` der Retro."""
    kennungen: list[str] = []
    imAbschnitt = False
    for zeile in retro.read_text(encoding="utf-8").splitlines():
        if zeile.startswith("## "):
            imAbschnitt = zeile.startswith("## Prozess-Items")
        treffer = re.match(r"- (P\d+) ", zeile)
        if imAbschnitt and treffer:
            kennungen.append(treffer.group(1))
    return kennungen


def offenesProzessItem(wurzel: Path, retro: int, freigabe: str) -> str | None:
    """Das erste Prozess-Item der Retro ohne Commit `P<k>: …` seit der Freigabe, sonst `None`."""
    # Warum: Der Betreff darf `Retro <n> ` voranstellen; so heißen die Commits von P4 und P5.
    betreffe = betreffeSeit(wurzel, freigabe)
    for kennung in prozessItems(wurzel / "handoff" / "retro.md"):
        muster = rf"(Retro {retro} )?{kennung}:"
        if not any(re.match(muster, betreff) for betreff in betreffe):
            return kennung
    return None


def prozessphase(wurzel: Path, plan: int, retro: int | None) -> Lage:
    """Retro, ihre Freigabe und die Prozess-Items; danach der nächste Zyklus."""
    if retro != plan and freigabeCommit(wurzel, "Review", plan) is None:
        return Lage(plan, Phase.technikphase, f"Review {plan} wartet auf Kritik und Freigabe")
    if retro != plan:
        return Lage(plan, Phase.prozessphase, f"Organisationsentwickler: Retro {plan}")
    freigabeRetro = freigabeCommit(wurzel, "Retro", plan)
    if freigabeRetro is None:
        return Lage(plan, Phase.prozessphase, f"Retro {plan} wartet auf Kritik und Freigabe")
    offen = offenesProzessItem(wurzel, plan, freigabeRetro)
    if offen is not None:
        return Lage(
            plan,
            Phase.prozessphase,
            f"Regelumsetzer: Prozess-Item {offen} aus Retro {plan} (Commit `{offen}: …`)",
        )
    return Lage(plan + 1, Phase.domänenphase, domänenphase(wurzel, plan + 1))


def lage(wurzel: Path) -> Lage:
    """Zyklus, Phase und nächster Schritt aus den Artefakten in `handoff/` und git."""
    handoff = wurzel / "handoff"
    plan, review, retro = (zyklus(handoff / f"{name}.md") for name in ("plan", "review", "retro"))
    if plan is None:
        return Lage(1, Phase.domänenphase, domänenphase(wurzel, 1))
    freigabePlan = freigabeCommit(wurzel, "Plan", plan)
    if freigabePlan is None and itemsOhneLink(wurzel):
        return Lage(
            plan, Phase.domänenphase, f"Planer: Items von Plan {plan} als Link auf {itemsOrdner}/"
        )
    if freigabePlan is None:
        return Lage(plan, Phase.domänenphase, planOhneFreigabe(wurzel, plan))
    items = offeneItems(wurzel)
    if (items or review != plan) and not akzeptanztestsSeit(wurzel, freigabePlan):
        return Lage(
            plan, Phase.technikphase, f"Testautor: Akzeptanztests zu den Items von Plan {plan}"
        )
    if items:
        return Lage(
            plan,
            Phase.technikphase,
            "Implementierer und Reviewer, dann Fachkritiker: Abnahme, "
            f"Planer löscht das Item (Items von Plan {plan})",
        )
    if review != plan:
        return Lage(plan, Phase.technikphase, f"Reviewer: Review {plan}")
    return prozessphase(wurzel, plan, retro)
