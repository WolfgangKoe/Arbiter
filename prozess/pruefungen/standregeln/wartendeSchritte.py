from pathlib import Path

from anliegenregeln.anliegenDran import wartetAuf
from gemeinsam.gitAufruf import letzteFreigabe
from lesen.anliegenKopf import Anliegen, Status, gelesene
from standregeln.phasenfolge import Lage, Phase, lage

mitSchritt = (Phase.domänenphase, Phase.technikphase)
phasenreihe = list(Phase)


def nächsterZyklus(jetzt: Lage, phase: str) -> int:
    später = phasenreihe.index(Phase(phase)) < phasenreihe.index(jetzt.phase)
    return jetzt.zyklus + 1 if später else jetzt.zyklus


def betrifft(anliegen: Anliegen, jetzt: Lage, ziel: Lage) -> bool:
    wartet = anliegen.wartetAuf
    if wartet is None or wartet.phase != ziel.phase or anliegen.status == Status.erledigt:
        return False
    zyklus = wartet.zyklus if wartet.zyklus is not None else nächsterZyklus(jetzt, wartet.phase)
    return zyklus == ziel.zyklus


def titel(anliegen: Anliegen) -> str:
    erste = anliegen.datei.read_text(encoding="utf-8").splitlines()[0]
    return erste.removeprefix("# ")


def wartendeSchritte(wurzel: Path, ziel: Lage) -> list[tuple[str, str, bool | None]]:
    if ziel.phase not in mitSchritt:
        return []
    jetzt = lage(wurzel)
    freigabe = letzteFreigabe(wurzel)
    schritte = []
    for anliegen in gelesene(wurzel):
        rolle = wartetAuf(wurzel, anliegen, freigabe)
        if rolle and betrifft(anliegen, jetzt, ziel):
            angenommen = True if anliegen.status == Status.angenommen else None
            schritte.append((rolle, f"Anliegen {anliegen.nummer} {titel(anliegen)}", angenommen))
    return schritte
