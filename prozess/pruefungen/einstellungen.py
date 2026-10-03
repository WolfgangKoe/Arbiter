"""Prüft `.claude/settings.json`: Jeder Hook zeigt auf ein vorhandenes, lesbares Skript.

Einstellungen wirken sofort in der laufenden Sitzung. Zeigt ein Hook auf eine fehlende Datei,
ist jeder Werkzeugaufruf aller Rollen blockiert. Darum gilt beim Umbenennen: neue Datei
anlegen, Einstellung umstellen, alte Datei löschen.
"""

import ast
import json
import shlex
import sys
from pathlib import Path

from agenten import projektordner


def hookBefehle(einstellungen: dict) -> list[str]:
    return [
        hook["command"]
        for gruppen in (einstellungen.get("hooks") or {}).values()
        for gruppe in gruppen
        for hook in gruppe.get("hooks", [])
        if hook.get("type") == "command"
    ]


def skripte(befehl: str, wurzel: Path) -> list[Path]:
    ersetzt = befehl.replace("${CLAUDE_PROJECT_DIR}", str(wurzel)).replace(
        "$CLAUDE_PROJECT_DIR", str(wurzel)
    )
    pfade = (Path(wort) for wort in shlex.split(ersetzt) if wort.endswith(".py"))
    return [pfad if pfad.is_absolute() else wurzel / pfad for pfad in pfade]


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
