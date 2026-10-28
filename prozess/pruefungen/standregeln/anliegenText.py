from pathlib import Path

from anliegenregeln.anliegenDran import dran, nachprüfungen, wartende
from lesen.anliegenKopf import zielText


def nachprüfungenAlsText(wurzel: Path) -> str:
    fällig = nachprüfungen(wurzel)
    if not fällig:
        return ""
    teile = [
        f"{rolle} ({', '.join(f'{nummer:02d}' for nummer in nummern)})"
        for rolle, nummern in sorted(fällig.items())
    ]
    return "Nachprüfung fällig: " + ", ".join(teile)


def wartendeAnliegenAlsText(wurzel: Path) -> str:
    warten = wartende(wurzel)
    if not warten:
        return ""
    teile = [f"{nummer:02d} (auf {zielText(ziel)})" for nummer, ziel in sorted(warten.items())]
    return "Wartet: " + ", ".join(teile)


def dranAlsText(wurzel: Path) -> str:
    zuständig = dran(wurzel)
    if not zuständig:
        return ""
    teile = [
        f"{rolle} ({', '.join(f'{nummer:02d}' for nummer in nummern)})"
        for rolle, nummern in sorted(zuständig.items())
    ]
    return "Dran: " + ", ".join(teile)
