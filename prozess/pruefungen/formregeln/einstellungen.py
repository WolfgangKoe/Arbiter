"""Prüft `.claude/settings.json`: Jeder Hook zeigt auf ein vorhandenes, lesbares Skript."""

import ast
import json
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


def verstöße(wurzel: Path) -> list[str]:
    datei = wurzel / ".claude" / "settings.json"
    einstellungen = json.loads(datei.read_text(encoding="utf-8"))
    meldungen = []
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
