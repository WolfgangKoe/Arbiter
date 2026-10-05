"""Prüft, dass ein Commit `Freigabe <Plan|Review|Retro> <n>` die Freigabe des Stakeholders trägt."""

import re
from pathlib import Path

from gemeinsam.pfade import handoffOrdner
from lesen.artefakt import artefaktVon, freigabeJa
from rollenregeln.gitBefehle import unterbefehlNach
from rollenregeln.shellZerlegen import wörter
from standregeln.freigabeKommentare import freigegebenerZyklus

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
