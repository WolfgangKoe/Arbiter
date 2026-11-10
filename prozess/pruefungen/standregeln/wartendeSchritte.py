import re
from pathlib import Path

from anliegenregeln.anliegenDran import wartetAuf
from gemeinsam.gitAufruf import dateiBeiCommit, gitAusgabe, letzteFreigabe
from gemeinsam.pfade import handoffOrdner
from lesen.anliegenKopf import Anliegen, Status, gelesene
from standregeln.phasenfolge import Lage, Phase, lage

mitSchritt = (Phase.domänenphase, Phase.technikphase)
dateiJePhase = {Phase.domänenphase: "review.md", Phase.technikphase: "plan.md"}
anliegenZeile = re.compile(r"^- \[([ x])\] ([^:]+): (Anliegen (\d+) .+)$", re.MULTILINE)
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


def standVersionen(wurzel: Path, datei: Path, freigabe: str | None) -> list[str]:
    texte = [datei.read_text(encoding="utf-8")] if datei.is_file() else []
    if freigabe is None:
        return texte
    commits = gitAusgabe(wurzel, "log", "--format=%H", f"{freigabe}..HEAD", "--", str(datei))
    kennungen = [freigabe, *commits.split()]
    return texte + [dateiBeiCommit(wurzel, kennung, datei) for kennung in kennungen]


def bleibendeSchritte(
    wurzel: Path, ziel: Lage, freigabe: str | None, schon: set[str]
) -> list[tuple[str, str, bool | None]]:
    datei = wurzel / handoffOrdner / dateiJePhase[ziel.phase]
    vorhanden = {anliegen.nummer: anliegen for anliegen in gelesene(wurzel)}
    schritte = []
    for text in standVersionen(wurzel, datei, freigabe):
        for haken, rolle, schritt, nummer in anliegenZeile.findall(text):
            anliegen = vorhanden.get(int(nummer))
            if nummer in schon or (anliegen is None and haken != "x"):
                continue
            schon.add(nummer)
            erledigt = anliegen is None or anliegen.status in (Status.angenommen, Status.erledigt)
            schritte.append((rolle, schritt, True if erledigt else None))
    return schritte


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
    schon = {schritt.split()[1] for _, schritt, _ in schritte}
    return schritte + bleibendeSchritte(wurzel, ziel, freigabe, schon)
