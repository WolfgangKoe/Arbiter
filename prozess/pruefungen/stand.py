"""Hooks `SessionStart` und `PostToolUse` (auf `Agent`): Stand in einer Zeile.

Er nennt den nächsten Schritt, kein Briefing. Nach jedem Rollenlauf meldet derselbe Stand,
wer dran ist und welche Kritik am Code fällig ist.

Jede Phase ist eine feste Folge von Artefakten; der Stand nennt das erste, das fehlt.
Übergänge: Domäne → Technik mit dem Commit `Freigabe Plan <n>`, Technik → Prozess mit
Review n, Prozess → Domäne mit `Freigabe Retro <n>`. Der Trigger für die Technik ist früh:
Ein Plan mit einem einzigen Item aus der ersten fertigen Anforderung genügt.
Die aktuelle Etappe ist die nach Namen erste Datei `domaene/etappen/*.md` (`# Etappe <n> · …`).
"""

import json
import re
import sys
from pathlib import Path

from agenten import projektordner
from anliegen import anliegenDateien, dranAlsText, nachprüfungenAlsText
from belegung import belegungAusTranskript, punkte, warnschwelle
from codekritik import fälligeKritikAlsText
from gitAufruf import gitAusgabe

rollenlaufKennzahl = {"Domänenphase": 8, "Technikphase": 10, "Prozessphase": 5}


def freigabeCommit(wurzel: Path, gegenstand: str, nummer: int) -> str | None:
    """Der Commit mit der Betreffzeile `Freigabe <gegenstand> <nummer>`, sonst `None`."""
    for zeile in gitAusgabe(wurzel, "log", "--format=%H %s").splitlines():
        kennung, _, betreff = zeile.partition(" ")
        if betreff == f"Freigabe {gegenstand} {nummer}":
            return kennung
    return None


def zyklus(datei: Path) -> int | None:
    if not datei.is_file():
        return None
    ersteZeile = datei.read_text(encoding="utf-8").partition("\n")[0]
    treffer = re.search(r"Zyklus\s+(\d+)", ersteZeile)
    return int(treffer.group(1)) if treffer else None


def aktuelleEtappe(wurzel: Path) -> tuple[int, str] | None:
    dateien = sorted((wurzel / "domaene" / "etappen").glob("*.md"))
    if not dateien:
        return None
    for zeile in dateien[0].read_text(encoding="utf-8").splitlines():
        treffer = re.match(r"# (Etappe\s+(\d+).*)", zeile)
        if treffer:
            return int(treffer.group(2)), treffer.group(1).strip()
    return None


def gibtAnforderungen(wurzel: Path) -> bool:
    return any(
        zeile.startswith("### ")
        for datei in (wurzel / "domaene" / "anforderungen").rglob("*.md")
        for zeile in datei.read_text(encoding="utf-8").splitlines()
    )


def akzeptanztestsSeit(wurzel: Path, kennung: str) -> bool:
    pfad = "technik/tests/akzeptanz"
    return bool(gitAusgabe(wurzel, "log", "--format=%H", f"{kennung}..HEAD", "--", pfad))


def offeneItems(wurzel: Path) -> list[str]:
    """Items des Plans: Links aus `handoff/plan.md` auf `domaene/items/<id>.md`.

    Offen ist ein Item, solange seine Datei existiert.
    """
    plan = wurzel / "handoff" / "plan.md"
    if not plan.is_file():
        return []
    links = re.findall(r"\]\(\.\./domaene/items/([^)#\s]+\.md)", plan.read_text(encoding="utf-8"))
    return [name for name in links if (wurzel / "domaene" / "items" / name).is_file()]


def domänenphase(wurzel: Path, zyklusNummer: int) -> str:
    etappe = aktuelleEtappe(wurzel)
    if etappe is None:
        return "Planer: Etappen aus dem Ziel ableiten"
    nummer, _ = etappe
    if freigabeCommit(wurzel, "Etappe", nummer) is None:
        return f"Etappe {nummer} wartet auf Kritik (Architekt) und Freigabe"
    if not gibtAnforderungen(wurzel):
        return f"Anforderungsautor: erste Anforderung zu Etappe {nummer}"
    return (
        f"Planer: Plan {zyklusNummer} mit den Items, die bereit sind (eins genügt, höchstens drei)"
    )


def lage(wurzel: Path) -> tuple[int, str, str]:
    """Zyklus, Phase und nächster Schritt aus den Artefakten in `handoff/` und git."""
    handoff = wurzel / "handoff"
    plan, review, retro = (zyklus(handoff / f"{name}.md") for name in ("plan", "review", "retro"))
    if plan is None:
        return 1, "Domänenphase", domänenphase(wurzel, 1)
    freigabePlan = freigabeCommit(wurzel, "Plan", plan)
    if freigabePlan is None:
        return plan, "Domänenphase", f"Plan {plan} wartet auf Kritik (Architekt) und Freigabe"
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


def protokoll(wurzel: Path) -> Path:
    return wurzel / ".git" / "arbiter" / "rollenlaeufe.jsonl"


def rollenläufe(wurzel: Path, schlüssel: str) -> int:
    datei = protokoll(wurzel)
    if not datei.is_file():
        return 0
    return sum(
        json.loads(zeile).get("phase") == schlüssel
        for zeile in datei.read_text(encoding="utf-8").splitlines()
        if zeile.strip()
    )


def kennzahlRollenläufe(wurzel: Path, zyklusNummer: int, phase: str) -> str:
    läufe = rollenläufe(wurzel, f"Zyklus {zyklusNummer} · {phase}")
    return f"Rollenläufe {läufe}/{rollenlaufKennzahl[phase]}"


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
        kennzahlRollenläufe(wurzel, zyklusNummer, phase),
        f"{len(anliegenDateien(wurzel))} offene Anliegen",
        dranAlsText(wurzel),
        nachprüfungenAlsText(wurzel),
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
