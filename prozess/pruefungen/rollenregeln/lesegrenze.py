"""Hook (PreToolUse): Der Koordinator liest nur kurze Dateien, auch per `git show`."""

from pathlib import Path

from gemeinsam.gitAufruf import blobGröße
from gemeinsam.hookProtokoll import HookEingabe, antwortAusgeben, eingabeLesen, verweigerung
from gemeinsam.pfade import projektordner

geprüfteRolle = "koordinator"
höchstlänge = 4000


def entscheide(daten: dict, wurzel: Path) -> dict | None:
    eingabe = HookEingabe.aus(daten)
    if eingabe.rolle != geprüfteRolle or eingabe.werkzeug != "Read":
        return None
    datei = Path(eingabe.angaben.get("file_path", ""))
    datei = datei if datei.is_absolute() else wurzel / datei
    if not datei.is_file():
        return None
    try:
        länge = len(datei.read_text(encoding="utf-8"))
    except UnicodeDecodeError:
        return None
    if länge <= höchstlänge:
        return None
    return verweigerung(
        f"{datei.name} hat {länge} Zeichen; du liest höchstens "
        f"{höchstlänge}. Nenne der zuständigen Rolle den Pfad, sie liest selbst."
    )


def gitShowZulässig(wörter: list[str], wurzel: Path) -> bool:
    """`git show` mit `--stat`, oder nur mit Dateiangaben `<rev>:<pfad>` bis zur Höchstlänge."""
    argumente = wörter[2:]
    if any(argument.startswith("--stat") for argument in argumente):
        return True
    angaben = [argument for argument in argumente if not argument.startswith("-")]
    if not angaben or any(argument.startswith("-") for argument in argumente):
        return False
    größen = [blobGröße(wurzel, angabe) if ":" in angabe else None for angabe in angaben]
    return all(größe is not None and größe <= höchstlänge for größe in größen)


if __name__ == "__main__":
    antwortAusgeben(entscheide(eingabeLesen(), projektordner()))
