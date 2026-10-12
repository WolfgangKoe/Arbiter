"""Hook (SubagentStart, PreToolUse): legt die vorgemerkten Züge des Stakeholders in die Anliegen."""

import re
from collections.abc import Callable
from pathlib import Path

from gemeinsam.hookProtokoll import HookEingabe, eingabeLesen
from gemeinsam.pfade import anliegenOrdner, projektordner
from lesen.anliegenKopf import Anliegen, Status, kopfAusText, stakeholder
from rollenregeln.eingang import (
    Verworfen,
    Zug,
    ersteVorgemerkteEntfernen,
    verworfenVermerken,
    vorgemerkte,
)

# Regel: Ablauf, Anliegen: Zug, setzt, Status; `seiten` nennt, auf welcher Seite er stehen darf
statusZüge = (
    (("empfänger",), {Status.offen}, {Status.angenommen, Status.rückfrage, Status.abgelehnt}),
    (
        ("absender",),
        {Status.angenommen, Status.abgelehnt, Status.rückfrage},
        {Status.erledigt, Status.offen},
    ),
    (("absender", "empfänger"), {Status.eskaliert}, {Status.offen, Status.erledigt}),
)
statusInKopf = re.compile(r"(Runde \d+/\d+ · )\w+")
rundeInKopf = re.compile(r"Runde (\d+)/")
commitBefehl = "git commit"
befehlsTrenner = re.compile(r"&&|\|\||[;|\n]")
keineFrage = "Die Frage steht nicht mehr im Anliegen."


def zulässigeStatus(anliegen: Anliegen) -> set[Status]:
    """Die Status, die der Stakeholder diesem Anliegen jetzt geben darf."""
    erlaubt: set[Status] = set()
    for seiten, von, nach in statusZüge:
        beteiligt = any(getattr(anliegen, seite) == stakeholder for seite in seiten)
        if beteiligt and anliegen.status in von:
            erlaubt |= nach
    return erlaubt


def einzeiler(text: str) -> str:
    return " ".join(text.split())


def zeileErsetzen(text: str, nummer: int, neu: str) -> str:
    zeilen = text.splitlines(keepends=True)
    zeilen[nummer] = neu + ("\n" if zeilen[nummer].endswith("\n") else "")
    return "".join(zeilen)


def statusSetzen(text: str, zug: Zug) -> str:
    kopf = text.splitlines()[2]
    return zeileErsetzen(text, 2, statusInKopf.sub(rf"\g<1>{zug.wert}", kopf, count=1))


def rundeSenken(text: str, zug: Zug) -> str:  # noqa: ARG001
    kopf = text.splitlines()[2]
    runde = int(rundeInKopf.search(kopf).group(1))
    return zeileErsetzen(text, 2, rundeInKopf.sub(f"Runde {runde - 1}/", kopf, count=1))


def antwortSetzen(text: str, zug: Zug) -> str | None:
    zeilen = text.splitlines(keepends=True)
    start = next(
        (stelle for stelle, zeile in enumerate(zeilen) if zeile.startswith(f"**{zug.frage} ·")),
        None,
    )
    if start is None:
        return None
    for stelle in range(start + 1, len(zeilen)):
        if zeilen[stelle].startswith("**F"):
            return None
        if zeilen[stelle].startswith("Antwort:"):
            return zeileErsetzen(text, stelle, f"Antwort: {einzeiler(zug.wert)}")
    return None


def kommentarAnhängen(text: str, zug: Zug) -> str:
    abschluss = "" if text.endswith("\n") else "\n"
    return f"{text}{abschluss}Kommentar: {einzeiler(zug.wert)}\n"


anwender: dict[str, Callable[[str, Zug], str | None]] = {
    "status": statusSetzen,
    "runde": rundeSenken,
    "antwort": antwortSetzen,
    "kommentar": kommentarAnhängen,
}


def grundDagegen(anliegen: Anliegen | None, zug: Zug) -> str | None:
    """Warum der Zug zum Anliegen nicht mehr passt; `None`, wenn er passt."""
    if anliegen is None:
        return "Das Anliegen gibt es nicht mehr."
    if zug.art not in anwender:
        return f"Unbekannte Art: {zug.art}."
    if zug.art == "kommentar":
        return None if einzeiler(zug.wert) else "Der Kommentar ist leer."
    if zug.art == "status" and zug.wert not in zulässigeStatus(anliegen):
        return f"Status {anliegen.status} erlaubt {zug.wert} nicht."
    if zug.art == "runde" and not (anliegen.status == Status.eskaliert and anliegen.runde > 1):
        return "Die Runde lässt sich nur bei `eskaliert` senken."
    if zug.art == "antwort" and not (
        anliegen.empfänger == stakeholder and anliegen.status == Status.offen
    ):
        return "Antworten gibt es nur auf offene Fragen an den Stakeholder."
    return None


def dateiZu(ordner: Path, nummer: int) -> Path | None:
    treffer = sorted((ordner / anliegenOrdner).glob(f"{nummer}-*.md"))
    return treffer[0] if treffer else None


def einzelnenÜbernehmen(ordner: Path, zug: Zug) -> Verworfen | None:
    datei = dateiZu(ordner, zug.nummer)
    text = datei.read_text(encoding="utf-8") if datei else ""
    anliegen = kopfAusText(text, datei) if datei else None
    grund = grundDagegen(anliegen, zug)
    if grund:
        return Verworfen(zug, grund)
    neu = anwender[zug.art](text, zug)
    if neu is None:
        return Verworfen(zug, keineFrage)
    datei.write_text(neu, encoding="utf-8")
    return None


def übernehmen(ordner: Path) -> tuple[int, int]:
    """Legt alle vorgemerkten Züge in die Dateien; gibt (übernommen, verworfen) zurück."""
    züge = vorgemerkte(ordner)
    verworfen = 0
    # Warum: das Formular merkt den Status vor die Antwort; nach dem Status gälte sie nicht mehr
    for zug in sorted(züge, key=lambda eintrag: eintrag.art != "antwort"):
        abgelehnt = einzelnenÜbernehmen(ordner, zug)
        if abgelehnt:
            verworfenVermerken(ordner, abgelehnt)
            verworfen += 1
    ersteVorgemerkteEntfernen(ordner, len(züge))
    return len(züge) - verworfen, verworfen


def löstAus(eingabe: HookEingabe) -> bool:
    """Vor jedem Rollenstart und vor dem Commit des Koordinators."""
    if eingabe.ereignis == "SubagentStart":
        return True
    befehl = str(eingabe.angaben.get("command") or "")
    return (
        eingabe.ereignis == "PreToolUse"
        and eingabe.werkzeug == "Bash"
        and not eingabe.rolle
        and any(teil.strip().startswith(commitBefehl) for teil in befehlsTrenner.split(befehl))
    )


if __name__ == "__main__":
    try:
        if löstAus(HookEingabe.aus(eingabeLesen())):
            übernehmen(projektordner())
    except Exception:  # Warum: ein Fehler hier darf weder Rollenstart noch Commit verhindern
        pass
