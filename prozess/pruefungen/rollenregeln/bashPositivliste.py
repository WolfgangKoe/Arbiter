"""Hook (PreToolUse): Bash nur nach Positivliste; Rollen nutzen git nur lesend."""

from pathlib import Path

from gemeinsam.hookProtokoll import HookEingabe, antwortAusgeben, eingabeLesen, verweigerung
from gemeinsam.pfade import projektordner
from rollenregeln.freigabeCommit import freigabeCommitVerstoß
from rollenregeln.gitBefehle import gitLesend, gitUnterbefehle
from rollenregeln.lesegrenze import gitShowZulässig
from rollenregeln.pfadsperren import (
    anliegenMeldung,
    pfadsperren,
    skriptSchreibtAnliegen,
    ändertPfad,
)
from rollenregeln.shellZerlegen import ohneHeredocText, wörter

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


def entscheide(daten: dict, wurzel: Path) -> dict | None:
    eingabe = HookEingabe.aus(daten)
    rolle = eingabe.rolle
    if not rolle or eingabe.werkzeug != "Bash":
        return None
    befehl = eingabe.angaben.get("command", "")
    if rolle == geprüfteRolle:
        if istErlaubt(befehl, wurzel):
            grund = freigabeCommitVerstoß(befehl, wurzel)
            return verweigerung(f"Freigabe-Commit: {grund}") if grund else None
        return verweigerung(
            "Bash-Positivliste des Koordinators: nur "
            + ", ".join(erlaubt)
            + "; ohne Verkettung und Umleitung; git show nur mit --stat oder für Dateien unter "
            "4.000 Zeichen. Andere Arbeit beauftragst du bei einer Rolle."
        )
    if skriptSchreibtAnliegen(befehl):
        return verweigerung(anliegenMeldung)
    befehl = ohneHeredocText(befehl)
    for istGesperrt, meldung in pfadsperren:
        if ändertPfad(befehl, wurzel, istGesperrt):
            return verweigerung(meldung)
    schreibend = [name for name in gitUnterbefehle(befehl) if name not in gitLesend]
    if not schreibend:
        return None
    return verweigerung(
        f"git {schreibend[0]} ist dem Koordinator vorbehalten; Rollen nutzen git nur lesend "
        f"({', '.join(gitLesend)}). Lösche Dateien mit rm, committet wird vom Koordinator."
    )


if __name__ == "__main__":
    antwortAusgeben(entscheide(eingabeLesen(), projektordner()))
