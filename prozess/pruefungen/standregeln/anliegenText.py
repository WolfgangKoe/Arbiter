"""Formt, wer bei den Anliegen dran ist, als Text für den Stand."""

from pathlib import Path

from anliegenregeln.anliegenDran import dran, nachprüfungen


def nachprüfungenAlsText(wurzel: Path) -> str:
    fällig = nachprüfungen(wurzel)
    if not fällig:
        return ""
    teile = [
        f"{rolle} ({', '.join(f'{nummer:02d}' for nummer in nummern)})"
        for rolle, nummern in sorted(fällig.items())
    ]
    return "Nachprüfung fällig: " + ", ".join(teile)


def dranAlsText(wurzel: Path, kommentare: dict[str, list[str]]) -> str:
    """Wer dran ist; `kommentare` nennt je Rolle Dateien mit offenem Kommentar des Stakeholders."""
    zuständig = {
        rolle: [f"{nummer:02d}" for nummer in nummern] for rolle, nummern in dran(wurzel).items()
    }
    for rolle, dateien in kommentare.items():
        zuständig.setdefault(rolle, []).extend(dateien)
    if not zuständig:
        return ""
    teile = [f"{rolle} ({', '.join(einträge)})" for rolle, einträge in sorted(zuständig.items())]
    return "Dran: " + ", ".join(teile)
