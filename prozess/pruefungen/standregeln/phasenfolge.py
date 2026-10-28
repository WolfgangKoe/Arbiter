import re
from enum import StrEnum
from pathlib import Path
from typing import NamedTuple

from gemeinsam.gitAufruf import betreffeSeit, freigabeCommit
from gemeinsam.pfade import etappenOrdner, handoffOrdner
from lesen.agenten import rollennamen
from lesen.plan import offeneItems, zyklus

itemzeile = re.compile(r"^- (P\d+) [^\n(]*\(([^),:]+)", re.MULTILINE)
umsetzer = "Regelumsetzer"


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
    for datei in sorted((wurzel / etappenOrdner).glob("*.md")):
        for zeile in datei.read_text(encoding="utf-8").splitlines():
            treffer = re.match(r"# (Etappe\s+\d+.*)", zeile)
            if treffer:
                return treffer.group(1).strip()
    return "keine Etappe"


def prozessItems(wurzel: Path) -> list[str]:
    text = (wurzel / handoffOrdner / "retro.md").read_text(encoding="utf-8")
    abschnitt = text.partition("## Prozess-Items")[2].partition("\n## ")[0]
    return re.findall(r"^- (P\d+) ", abschnitt, re.MULTILINE)


def itemRollen(wurzel: Path) -> dict[str, str]:
    text = (wurzel / handoffOrdner / "retro.md").read_text(encoding="utf-8")
    abschnitt = text.partition("## Prozess-Items")[2].partition("\n## ")[0]
    bekannt = {name.casefold(): name.capitalize() for name in rollennamen(wurzel)}
    genannt = {kennung: rolle.strip().casefold() for kennung, rolle in itemzeile.findall(abschnitt)}
    return {
        kennung: bekannt.get(genannt.get(kennung, ""), umsetzer) for kennung in prozessItems(wurzel)
    }


def hatItemCommit(betreffe: list[str], retro: int, kennung: str) -> bool:
    muster = rf"(Retro {retro} )?(P\d+(, | und ))*{kennung}((, | und )(P)?\d+)*:"
    return any(re.match(muster, betreff) for betreff in betreffe)


def offenesProzessItem(wurzel: Path, retro: int, freigabe: str) -> str | None:
    betreffe = betreffeSeit(wurzel, freigabe)
    for kennung in prozessItems(wurzel):
        if not hatItemCommit(betreffe, retro, kennung):
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
        rolle = itemRollen(wurzel)[offen]
        return plan, Phase.prozessphase, f"{rolle}: Prozess-Item {offen} aus Retro {plan}"
    return plan + 1, Phase.domänenphase, f"Anforderungsautor, dann Planer: Plan {plan + 1}"


def technikschritt(wurzel: Path, plan: int, review: int | None) -> tuple[Phase, str]:
    if offeneItems(wurzel):
        return Phase.technikphase, f"Items von Plan {plan}: Tests, Umsetzung, Abnahme"
    if review != plan:
        return Phase.technikphase, f"Reviewer: Review {plan}"
    return Phase.technikphase, f"Review {plan} wartet auf Kritik und Freigabe"


def lage(wurzel: Path) -> Lage:
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
