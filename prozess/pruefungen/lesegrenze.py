"""Der Koordinator liest nur kurze Dateien: Hook `PreToolUse` auf `Read` und `git show`."""

import subprocess
from pathlib import Path

from agenten import projektordner
from hookProtokoll import antwortAusgeben, eingabeLesen, verweigerung, werkzeugAngaben

geprüfteRolle = "koordinator"
höchstlänge = 4000


def entscheide(eingabe: dict, wurzel: Path) -> dict | None:
    if eingabe.get("agent_type") != geprüfteRolle or eingabe.get("tool_name") != "Read":
        return None
    datei = Path(werkzeugAngaben(eingabe).get("file_path", ""))
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


def blobGröße(wurzel: Path, angabe: str) -> int | None:
    """Größe von `<rev>:<pfad>` in Byte (mindestens die Zeichenzahl); `None`, wenn unbekannt."""
    ergebnis = subprocess.run(
        ["git", "cat-file", "-s", angabe], cwd=wurzel, capture_output=True, text=True, check=False
    )
    return int(ergebnis.stdout) if ergebnis.returncode == 0 else None


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
