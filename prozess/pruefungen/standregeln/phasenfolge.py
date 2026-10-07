"""Etappe, Zyklus, Phase und nächster Schritt aus den Dateien in `handoff/` und den Freigaben."""

import re
from enum import StrEnum
from pathlib import Path
from typing import NamedTuple

from gemeinsam.gitAufruf import betreffeSeit, freigabeCommit
from gemeinsam.pfade import etappenOrdner, handoffOrdner
from lesen.plan import offeneItems, zyklus


class Phase(StrEnum):
    domänenphase = "Domänenphase"
    technikphase = "Technikphase"
    prozessphase = "Prozessphase"


class Lage(NamedTuple):
    etappe: str
    zyklus: int
    phase: Phase
    schritt: str

    def alsText(self) -> str:
        kopf = f"{self.etappe} · Zyklus {self.zyklus} · {self.phase}"
        return f"{kopf} · Nächster Schritt: {self.schritt}"


def aktuelleEtappe(wurzel: Path) -> str:
    """Die Überschrift der ersten Etappendatei, sonst „keine Etappe“."""
    for datei in sorted((wurzel / etappenOrdner).glob("*.md")):
        for zeile in datei.read_text(encoding="utf-8").splitlines():
            treffer = re.match(r"# (Etappe\s+\d+.*)", zeile)
            if treffer:
                return treffer.group(1).strip()
    return "keine Etappe"


def offenesProzessItem(wurzel: Path, retro: int, freigabe: str) -> str | None:
    """Das erste Item `- P<k> ` der Retro ohne Commit `P<k>: …` seit ihrer Freigabe."""
    # Warum: Der Ablauf erlaubt das Präfix `Retro <n> ` (Prozessphase, Schritt 5).
    text = (wurzel / handoffOrdner / "retro.md").read_text(encoding="utf-8")
    abschnitt = text.partition("## Prozess-Items")[2].partition("\n## ")[0]
    betreffe = betreffeSeit(wurzel, freigabe)
    for kennung in re.findall(r"^- (P\d+) ", abschnitt, re.MULTILINE):
        muster = rf"(Retro {retro} )?{kennung}:"
        if not any(re.match(muster, betreff) for betreff in betreffe):
            return kennung
    return None


def prozessschritt(wurzel: Path, plan: int, retro: int | None) -> tuple[int, Phase, str]:
    if retro != plan:
        return plan, Phase.prozessphase, f"Organisationsentwickler: Retro {plan}"
    freigabe = freigabeCommit(wurzel, "Retro", plan)
    if freigabe is None:
        return plan, Phase.prozessphase, f"Retro {plan} wartet auf Kritik und Freigabe"
    offen = offenesProzessItem(wurzel, plan, freigabe)
    if offen is not None:
        return plan, Phase.prozessphase, f"Regelumsetzer: Prozess-Item {offen} aus Retro {plan}"
    return plan + 1, Phase.domänenphase, f"Anforderungsautor, dann Planer: Plan {plan + 1}"


def technikschritt(wurzel: Path, plan: int, review: int | None) -> tuple[Phase, str]:
    if offeneItems(wurzel):
        return Phase.technikphase, f"Items von Plan {plan}: Tests, Umsetzung, Abnahme"
    if review != plan:
        return Phase.technikphase, f"Reviewer: Review {plan}"
    return Phase.technikphase, f"Review {plan} wartet auf Kritik und Freigabe"


def lage(wurzel: Path) -> Lage:
    """Wo der Zyklus steht, nach `prozess/ablauf.md`."""
    handoff = wurzel / handoffOrdner
    plan, review, retro = (zyklus(handoff / f"{name}.md") for name in ("plan", "review", "retro"))
    etappe = aktuelleEtappe(wurzel)
    if plan is None:
        return Lage(etappe, 1, Phase.domänenphase, "Planer: Plan 1")
    if freigabeCommit(wurzel, "Plan", plan) is None:
        schritt = f"Plan {plan} wartet auf Kritik und Freigabe"
        return Lage(etappe, plan, Phase.domänenphase, schritt)
    if freigabeCommit(wurzel, "Review", plan) is None:
        return Lage(etappe, plan, *technikschritt(wurzel, plan, review))
    return Lage(etappe, *prozessschritt(wurzel, plan, retro))
