"""Gruppiert die Läufe des Logs nach Sitzung und Rolle und benennt die Sitzungen."""

from rollenregeln.laufLesen import Lauf

ohneSitzung = "ohne Sitzung"


def nachSitzung(läufe: list[Lauf]) -> dict[str, list[Lauf]]:
    gruppen: dict[str, list[Lauf]] = {}
    for lauf in läufe:
        gruppen.setdefault(lauf.sitzung[:8] if lauf.sitzung else ohneSitzung, []).append(lauf)
    return gruppen


def sitzungsTitel(sitzung: str, läufe: list[Lauf]) -> str:
    """„Zyklus 3 Prozessphase“; wechselt die Sitzung die Phase, „Zyklus 3 Domänenphase bis …“."""
    if sitzung == ohneSitzung:
        return f"Altbestand, {ohneSitzung}"
    benannt = [(lauf.zyklus, lauf.phase) for lauf in läufe if lauf.zyklus]
    if not benannt:
        return f"Sitzung {sitzung} (vor Zyklus und Phase im Log)"
    (zyklusVon, phaseVon), (zyklusBis, phaseBis) = benannt[0], benannt[-1]
    if (zyklusVon, phaseVon) == (zyklusBis, phaseBis):
        name = f"Zyklus {zyklusVon} {phaseVon}"
    elif zyklusVon == zyklusBis:
        name = f"Zyklus {zyklusVon} {phaseVon} bis {phaseBis}"
    else:
        name = f"Zyklus {zyklusVon} {phaseVon} bis Zyklus {zyklusBis} {phaseBis}"
    return name


def belegungNachRolle(läufe: list[Lauf]) -> dict[str, list[int]]:
    nachRolle: dict[str, list[int]] = {}
    for lauf in läufe:
        nachRolle.setdefault(lauf.rolle, []).append(lauf.belegung)
    return nachRolle
