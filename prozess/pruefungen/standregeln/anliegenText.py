"""Formt, wer bei den Anliegen dran ist, als Text für den Stand."""

from pathlib import Path

from anliegenregeln.anliegenDran import dran, nachprüfungen, wartende


def nachprüfungenAlsText(wurzel: Path) -> str:
    fällig = nachprüfungen(wurzel)
    if not fällig:
        return ""
    teile = [
        f"{rolle} ({', '.join(f'{nummer:02d}' for nummer in nummern)})"
        for rolle, nummern in sorted(fällig.items())
    ]
    return "Nachprüfung fällig: " + ", ".join(teile)


def worauf(ziel: str) -> str:
    return f"{int(ziel):02d}" if ziel.isdigit() else f"die {ziel}"


def wartendeAnliegenAlsText(wurzel: Path) -> str:
    """Anliegen, die auf ein anderes oder die Prozessphase warten; für niemanden dran."""
    warten = wartende(wurzel)
    if not warten:
        return ""
    teile = [f"{nummer:02d} (auf {worauf(ziel)})" for nummer, ziel in sorted(warten.items())]
    return "Wartet: " + ", ".join(teile)


def dranAlsText(wurzel: Path) -> str:
    """Wer bei den Anliegen dran ist."""
    zuständig = dran(wurzel)
    if not zuständig:
        return ""
    teile = [
        f"{rolle} ({', '.join(f'{nummer:02d}' for nummer in nummern)})"
        for rolle, nummern in sorted(zuständig.items())
    ]
    return "Dran: " + ", ".join(teile)
