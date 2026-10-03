"""Hook: Der Koordinator führt nur Befehle aus der Positivliste aus; Rollen nutzen git nur lesend.

Berechtigungsregeln reichen nicht: Ohne Write hat ein Agent in der Probe per
`echo > datei` geschrieben. Für den Koordinator sind Verkettung, Umleitung und
Befehlsersetzung gesperrt. Committen ist allein Sache des Koordinators; in Zyklus 1 hatten
Planer und Architekt selbst committet. `git show` darf der Koordinator nur mit `--stat` oder
für kurze Dateien (`lesegrenze.py`). Rollen ändern nichts, was `agenten.nurLesbar` nennt.
"""

import json
import re
import shlex
import sys
from pathlib import Path

from agenten import istNurLesbar, projektordner
from lesegrenze import gitShowZulässig

geprüfteRolle = "koordinator"

erlaubt = (
    "git status",
    "git diff",
    "git log",
    "git show",
    "git add",
    "git commit",
    "git push",
    "git rev-parse",
    "git ls-files",
    "ls",
    "python3 prozess/pruefungen/",
    "python3 -m pytest prozess/pruefungen",
)

operatorZeichen = set(";&|<>()")
trennOperatoren = {";", "&", "&&", "|", "||", "(", ")"}
umleitungen = {">", ">>", ">|", "&>"}

gitLesend = (
    "status", "log", "diff", "show", "grep", "ls-files", "ls-tree", "blame",
    "rev-parse", "shortlog", "cat-file", "describe",
)
gitOptionenMitWert = ("-C", "-c", "--git-dir", "--work-tree")

# Befehle, die jedes Pfadargument ändern; bei Kopierbefehlen zählt nur das Ziel.
ändernAlle = {"rm", "unlink", "shred", "truncate", "touch", "tee", "chmod", "chown", "mkdir",
              "rmdir", "patch", "dd", "mv"}
ändernZiel = {"cp", "ln", "rsync", "install"}


heredoc = re.compile(
    r"^(?P<kopf>[^\n]*?)<<-?\s*(?P<quote>['\"]?)(?P<ende>\w+)(?P=quote)[^\n]*\n"
    r".*?\n[ \t]*(?P=ende)[ \t]*$",
    re.DOTALL | re.MULTILINE,
)
shells = {"bash", "sh", "zsh", "dash", "eval", "source", "."}


def ohneHeredocText(befehl: str) -> str:
    """Entfernt Heredoc-Texte (etwa `cat > datei <<EOF`), außer sie füttern eine Shell."""

    def ersetzen(treffer: re.Match) -> str:
        kopf = treffer["kopf"]
        wörterImKopf = kopf.replace(";", " ").replace("&", " ").replace("|", " ").split()
        if wörterImKopf and Path(wörterImKopf[-1]).name in shells:
            return treffer.group(0)
        return kopf

    return heredoc.sub(ersetzen, befehl)


def zerlegen(befehl: str) -> list[str] | None:
    zerleger = shlex.shlex(befehl, posix=True, punctuation_chars=True)
    zerleger.whitespace_split = True
    try:
        return list(zerleger)
    except ValueError:
        return None


def wörter(befehl: str) -> list[str] | None:
    """Zerlegt wie die Shell; `None`, wenn der Befehl Verkettung oder Umleitung enthält."""
    if "$(" in befehl or "`" in befehl or "\n" in befehl:
        return None
    teile = zerlegen(befehl)
    if teile is None or any(teil and set(teil) <= operatorZeichen for teil in teile):
        return None
    return teile


def istErlaubt(befehl: str, wurzel: Path) -> bool:
    teile = wörter(befehl)
    if not teile:
        return False
    zeile = " ".join(teile)
    passt = any(
        zeile.startswith(eintrag)
        if eintrag.endswith("/")
        else zeile == eintrag or zeile.startswith(eintrag + " ")
        for eintrag in erlaubt
    )
    if passt and zeile.startswith("git show"):
        return gitShowZulässig(teile, wurzel)
    return passt


def beginntBefehl(teile: list[str], stelle: int) -> bool:
    """Ob das Wort an `stelle` ein Befehlsname ist: am Anfang oder nach einem Operator."""
    return stelle == 0 or set(teile[stelle - 1]) <= operatorZeichen


def unterbefehlNach(teile: list[str], stelle: int) -> str:
    """Das Wort nach `git` und seinen Optionen, `""` ohne Unterbefehl."""
    nächste = stelle + 1
    while nächste < len(teile) and teile[nächste].startswith("-"):
        nächste += 2 if teile[nächste] in gitOptionenMitWert else 1
    return teile[nächste] if nächste < len(teile) else ""


def gitUnterbefehle(befehl: str) -> list[str]:
    """Die Unterbefehle aller git-Aufrufe, auch in verketteten Befehlen."""
    teile = zerlegen(befehl.replace("\n", " ; "))
    if teile is None:
        return ["(nicht lesbar)"] if "git" in befehl else []
    return [
        unterbefehlNach(teile, stelle)
        for stelle, teil in enumerate(teile)
        if Path(teil).name == "git" and beginntBefehl(teile, stelle)
    ]


def meintNurLesbares(wort: str, wurzel: Path) -> bool:
    """Ob ein Pfadwort auf einen nur lesbaren Pfad zeigt (relativ, absolut oder mit `..`)."""
    pfad = wort.split("=", 1)[-1] if wort.startswith(("of=", "--file=")) else wort
    if not pfad or pfad.startswith("-"):
        return False
    absolut = Path(pfad) if Path(pfad).is_absolute() else wurzel / pfad
    try:
        relativ = absolut.resolve().relative_to(wurzel.resolve()).as_posix()
    except ValueError:
        return False
    return istNurLesbar(relativ)


def ändertNurLesbares(befehl: str, wurzel: Path) -> bool:
    """Heuristik für Bash: Umleitung, rm, mv, cp (Ziel), sed -i auf einen nur lesbaren Pfad."""
    teile = zerlegen(befehl.replace("\n", " ; "))
    if teile is None:
        return False
    segment: list[str] = []
    segmente = [segment]
    for stelle, teil in enumerate(teile):
        if teil in trennOperatoren:
            segment = []
            segmente.append(segment)
        elif teil in umleitungen:
            ziel = teile[stelle + 1] if stelle + 1 < len(teile) else ""
            if meintNurLesbares(ziel, wurzel):
                return True
        else:
            segment.append(teil)
    return any(segmentÄndert(wörterDesSegments, wurzel) for wörterDesSegments in segmente)


def segmentÄndert(segment: list[str], wurzel: Path) -> bool:
    if not segment:
        return False
    befehl, *argumente = segment
    name = Path(befehl).name
    pfade = [argument for argument in argumente if not argument.startswith("-")]
    if name in ändernAlle:
        return any(meintNurLesbares(argument, wurzel) for argument in argumente)
    if name in ändernZiel:
        return bool(pfade) and meintNurLesbares(pfade[-1], wurzel)
    if name == "sed" and any(argument.startswith(("-i", "--in-place")) for argument in argumente):
        return any(meintNurLesbares(argument, wurzel) for argument in pfade)
    return False


def ablehnen(grund: str) -> dict:
    return {
        "hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "permissionDecision": "deny",
            "permissionDecisionReason": grund,
        }
    }


def entscheide(eingabe: dict, wurzel: Path) -> dict | None:
    rolle = eingabe.get("agent_type")
    if not rolle or eingabe.get("tool_name") != "Bash":
        return None
    befehl = (eingabe.get("tool_input") or {}).get("command", "")
    if rolle == geprüfteRolle:
        if istErlaubt(befehl, wurzel):
            return None
        return ablehnen(
            "Bash-Positivliste des Koordinators: nur "
            + ", ".join(erlaubt)
            + "; ohne Verkettung und Umleitung; git show nur mit --stat oder für Dateien unter "
            "4.000 Zeichen. Andere Arbeit beauftragst du bei einer Rolle."
        )
    befehl = ohneHeredocText(befehl)
    if ändertNurLesbares(befehl, wurzel):
        return ablehnen(
            "Dieser Pfad ist nur lesbar, für alle Rollen: VORGEHEN.md, "
            "handoff/kritik-entwickler.md, Arbiter/, ArbiterMap/. Löschen tut nur der Stakeholder."
        )
    schreibend = [name for name in gitUnterbefehle(befehl) if name not in gitLesend]
    if not schreibend:
        return None
    return ablehnen(
        f"git {schreibend[0]} ist dem Koordinator vorbehalten; Rollen nutzen git nur lesend "
        f"({', '.join(gitLesend)}). Lösche Dateien mit rm, committet wird vom Koordinator."
    )


if __name__ == "__main__":
    antwort = entscheide(json.load(sys.stdin), projektordner())
    if antwort:
        print(json.dumps(antwort, ensure_ascii=False))
