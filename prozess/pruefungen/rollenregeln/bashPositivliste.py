"""Hook: Der Koordinator führt nur Befehle der Positivliste aus; Rollen nutzen git nur lesend."""

import re
import shlex
from collections.abc import Callable
from pathlib import Path

from gemeinsam.hookProtokoll import HookEingabe, antwortAusgeben, eingabeLesen, verweigerung
from gemeinsam.pfade import anliegenOrdner, handoffOrdner, istNurLesbar, nurLesbar, projektordner
from rollenregeln.lesegrenze import gitShowZulässig
from standregeln.freigabeKommentare import artefakte, artefaktVon, freigabeJa, freigegebenerZyklus

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
    "status",
    "log",
    "diff",
    "show",
    "grep",
    "ls-files",
    "ls-tree",
    "blame",
    "rev-parse",
    "shortlog",
    "cat-file",
    "describe",
)
gitOptionenMitWert = ("-C", "-c", "--git-dir", "--work-tree")

# Warum: Befehle, die jedes Pfadargument ändern; bei Kopierbefehlen zählt nur das Ziel.
ändernAlle = {
    "rm",
    "unlink",
    "shred",
    "truncate",
    "touch",
    "tee",
    "chmod",
    "chown",
    "mkdir",
    "rmdir",
    "patch",
    "dd",
    "mv",
}
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


freigabeBetreff = re.compile(r"^Freigabe (Plan|Review|Retro) (\d+)\b")


def commitBetreff(teile: list[str]) -> str:
    """Erste Zeile der Nachricht nach `-m` oder `--message`, `""` ohne Nachricht."""
    for stelle, wort in enumerate(teile):
        nachricht = None
        kurz = re.fullmatch(r"-[a-zA-Z]*?m(.*)", wort, re.DOTALL)
        if wort.startswith("--message="):
            nachricht = wort.removeprefix("--message=")
        elif wort == "--message":
            nachricht = teile[stelle + 1] if stelle + 1 < len(teile) else ""
        elif kurz:
            nachricht = kurz[1] or (teile[stelle + 1] if stelle + 1 < len(teile) else "")
        if nachricht is not None:
            return nachricht.partition("\n")[0]
    return ""


def freigabeCommitVerstoß(befehl: str, wurzel: Path) -> str | None:
    """Der Betreff `Freigabe <Plan|Review|Retro> <n>` braucht `Freigabe: ja` und Zyklus n."""
    teile = wörter(befehl)
    if not teile or Path(teile[0]).name != "git" or unterbefehlNach(teile, 0) != "commit":
        return None
    treffer = freigabeBetreff.match(commitBetreff(teile))
    if treffer is None:
        return None
    gegenstand, nummer = treffer[1], int(treffer[2])
    artefakt = artefaktVon(gegenstand)
    if freigegebenerZyklus(wurzel, artefakt) == nummer:
        return None
    return (
        f"Freigabe {gegenstand} {nummer} nur, wenn {handoffOrdner}/{artefakt.datei} "
        f"`{freigabeJa}` trägt und in der ersten Zeile Zyklus {nummer} nennt; "
        "beides setzt der Stakeholder."
    )


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


def istAnliegen(relativerPfad: str) -> bool:
    return relativerPfad.startswith(f"{anliegenOrdner}/")


def istFreigabeArtefakt(relativerPfad: str) -> bool:
    return relativerPfad in {f"{handoffOrdner}/{artefakt.datei}" for artefakt in artefakte}


def meintPfad(wort: str, wurzel: Path, gesperrt: Callable[[str], bool]) -> bool:
    """Ob ein Pfadwort auf einen gesperrten Pfad zeigt (relativ, absolut oder mit `..`)."""
    pfad = wort.split("=", 1)[-1] if wort.startswith(("of=", "--file=")) else wort
    if not pfad or pfad.startswith("-"):
        return False
    absolut = Path(pfad) if Path(pfad).is_absolute() else wurzel / pfad
    try:
        relativ = absolut.resolve().relative_to(wurzel.resolve()).as_posix()
    except ValueError:
        return False
    return gesperrt(relativ)


def ändertPfad(befehl: str, wurzel: Path, gesperrt: Callable[[str], bool]) -> bool:
    """Heuristik für Bash: Umleitung, rm, mv, cp (Ziel), sed -i auf einen gesperrten Pfad."""
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
            if meintPfad(ziel, wurzel, gesperrt):
                return True
        else:
            segment.append(teil)
    return any(segmentÄndert(wörterDesSegments, wurzel, gesperrt) for wörterDesSegments in segmente)


def segmentÄndert(segment: list[str], wurzel: Path, gesperrt: Callable[[str], bool]) -> bool:
    if not segment:
        return False
    befehl, *argumente = segment
    name = Path(befehl).name
    pfade = [argument for argument in argumente if not argument.startswith("-")]
    if name in ändernAlle:
        return any(meintPfad(argument, wurzel, gesperrt) for argument in argumente)
    if name in ändernZiel:
        return bool(pfade) and meintPfad(pfade[-1], wurzel, gesperrt)
    if name == "sed" and any(argument.startswith(("-i", "--in-place")) for argument in argumente):
        return any(meintPfad(argument, wurzel, gesperrt) for argument in pfade)
    return False


pfadsperren = (
    (
        istNurLesbar,
        f"Dieser Pfad ist nur lesbar, für alle Rollen: {', '.join(nurLesbar)}. "
        "Löschen tut nur der Stakeholder.",
    ),
    (
        istAnliegen,
        "Anliegen ändern Rollen nur mit Write und Edit, nie per Bash: Daran vorbei "
        "greifen Statusrecht und Nummernprüfung nicht (prozess/ablauf.md, Anliegen).",
    ),
    (
        istFreigabeArtefakt,
        "Plan, Review und Retro ändern Rollen nur mit Write und Edit, nie per Bash: Daran "
        "vorbei greift die Freigabesperre nicht (prozess/ablauf.md, Freigabe und Kommentare).",
    ),
)


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
