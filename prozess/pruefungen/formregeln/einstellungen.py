"""Prüft `.claude/settings.json`: Jeder Hook zeigt auf ein Skript, das sein Ereignis nennt."""

import ast
import json
import re
import shlex
import sys
from pathlib import Path

from gemeinsam.pfade import projektordner


def hookBefehle(einstellungen: dict) -> list[str]:
    return [
        hook["command"]
        for gruppen in (einstellungen.get("hooks") or {}).values()
        for gruppe in gruppen
        for hook in gruppe.get("hooks", [])
        if hook.get("type") == "command"
    ]


def skripte(befehl: str, wurzel: Path) -> list[Path]:
    """Die Skripte eines Hook-Befehls; hinter `lauf.py` steht der Modulname des Prüfskripts."""
    ersetzt = befehl.replace("${CLAUDE_PROJECT_DIR}", str(wurzel)).replace(
        "$CLAUDE_PROJECT_DIR", str(wurzel)
    )
    wörter = shlex.split(ersetzt)
    gefunden = []
    for stelle, wort in enumerate(wörter):
        if wort.endswith(".py"):
            pfad = Path(wort)
            gefunden.append(pfad if pfad.is_absolute() else wurzel / pfad)
            if pfad.name == "lauf.py" and stelle + 1 < len(wörter):
                modul = wörter[stelle + 1].replace(".", "/") + ".py"
                gefunden.append(gefunden[-1].parents[1] / modul)
    return gefunden


def modulSkript(befehl: str, wurzel: Path) -> Path | None:
    """Das Prüfskript hinter `lauf.py`; `None`, wenn der Befehl nicht über den Starter läuft."""
    gefunden = skripte(befehl, wurzel)
    return gefunden[-1] if len(gefunden) > 1 and gefunden[-2].name == "lauf.py" else None


def eingetrageneEreignisse(einstellungen: dict, wurzel: Path) -> dict[Path, set[str]]:
    """Je Prüfskript die Ereignisse, unter denen `settings.json` es aufruft."""
    ereignisse: dict[Path, set[str]] = {}
    for ereignis, gruppen in (einstellungen.get("hooks") or {}).items():
        for gruppe in gruppen:
            for hook in gruppe.get("hooks", []):
                skript = modulSkript(hook.get("command", ""), wurzel)
                if skript is not None:
                    ereignisse.setdefault(skript, set()).add(ereignis)
    return ereignisse


def genannteEreignisse(skript: Path) -> set[str] | None:
    """Die Ereignisse aus der ersten Docstring-Zeile `Hook (A, B): …`; `None` ohne diese Form."""
    try:
        docstring = ast.get_docstring(ast.parse(skript.read_text(encoding="utf-8")))
    except (OSError, SyntaxError):
        return None
    treffer = re.match(r"Hook \(([^)]*)\)", docstring or "")
    return {name.strip() for name in treffer.group(1).split(",")} if treffer else None


def ereignisVerstöße(einstellungen: dict, wurzel: Path) -> list[str]:
    eingetragen = eingetrageneEreignisse(einstellungen, wurzel)
    meldungen = []
    for skript, ereignisse in eingetragen.items():
        genannt = genannteEreignisse(skript) if skript.is_file() else ereignisse
        if genannt != ereignisse:
            meldungen.append(
                f"Hook {skript.name}: eingetragen unter {sorted(ereignisse)}, "
                f"Docstring nennt {sorted(genannt) if genannt else 'kein Ereignis'}"
            )
    for skript in sorted((wurzel / "prozess" / "pruefungen").glob("*/*.py")):
        if skript not in eingetragen and genannteEreignisse(skript):
            meldungen.append(f"Hook {skript.name}: Docstring nennt Ereignisse, aber kein Eintrag")
    return meldungen


def verstöße(wurzel: Path) -> list[str]:
    datei = wurzel / ".claude" / "settings.json"
    einstellungen = json.loads(datei.read_text(encoding="utf-8"))
    meldungen = ereignisVerstöße(einstellungen, wurzel)
    for befehl in hookBefehle(einstellungen):
        for skript in skripte(befehl, wurzel):
            if not skript.is_file():
                meldungen.append(f"Hook `{befehl}`: {skript.name} fehlt")
                continue
            try:
                ast.parse(skript.read_text(encoding="utf-8"))
            except SyntaxError as fehler:
                meldungen.append(
                    f"Hook `{befehl}`: {skript.name} ist kein gültiges Python ({fehler})"
                )
    return meldungen


if __name__ == "__main__":
    gefunden = verstöße(projektordner())
    print("\n".join(gefunden))
    sys.exit(1 if gefunden else 0)
