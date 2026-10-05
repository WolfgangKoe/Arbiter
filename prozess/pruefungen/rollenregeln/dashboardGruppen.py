"""Gruppiert die Läufe des Logs nach Sitzung und Rolle und benennt die Sitzungen."""

ohneSitzung = "ohne Sitzung"


def nachSitzung(läufe: list[dict]) -> dict[str, list[dict]]:
    gruppen: dict[str, list[dict]] = {}
    for lauf in läufe:
        kennung = lauf.get("sitzung")
        gruppen.setdefault(kennung[:8] if kennung else ohneSitzung, []).append(lauf)
    return gruppen


def sitzungsTitel(sitzung: str, läufe: list[dict]) -> str:
    """„Zyklus 3 Prozessphase“; wechselt die Sitzung die Phase, „Zyklus 3 Domänenphase bis …“."""
    if sitzung == ohneSitzung:
        return f"Altbestand, {ohneSitzung}"
    benannt = [(lauf["zyklus"], lauf["phase"]) for lauf in läufe if lauf.get("zyklus")]
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


def belegungNachRolle(läufe: list[dict]) -> dict[str, list[int]]:
    nachRolle: dict[str, list[int]] = {}
    for lauf in läufe:
        nachRolle.setdefault(lauf["rolle"], []).append(lauf["belegung"])
    return nachRolle
