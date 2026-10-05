"""Prüft den Kopf einer Anliegen-Datei (Titel, Kopfzeile, Typ, Runde, Status, Rollen)."""

from pathlib import Path

from anliegenregeln.antworten import antwortVerstöße
from lesen.agenten import rollennamen
from lesen.anliegenKopf import Status, höchstRunde, kopfLesen, stakeholder, typWerte


def kopfVerstöße(datei: Path, wurzel: Path) -> list[str]:
    """Was am Kopf der Anliegen-Datei nicht stimmt; leer, wenn er in Ordnung ist."""
    zeilen = datei.read_text(encoding="utf-8").splitlines()
    if not zeilen or not zeilen[0].startswith("# "):
        return ["Zeile 1 ist kein Titel `# <Titel>`"]
    anliegen = kopfLesen(datei)
    if anliegen is None:
        return [
            "Zeile 3: Kopf `<nr> · <Typ> · von <Rolle> → <Rolle> · "
            f"Runde <n>/{höchstRunde} · <Status>` erwartet"
        ]
    verstöße = []
    if not datei.name.startswith(f"{anliegen.nummer:02d}-"):
        verstöße.append(f"Nummer {anliegen.nummer} passt nicht zum Dateinamen")
    if anliegen.typ not in typWerte:
        verstöße.append(f"Typ {anliegen.typ} ist keiner von {', '.join(typWerte)}")
    if not 1 <= anliegen.runde <= höchstRunde:
        verstöße.append(f"Runde {anliegen.runde} liegt außerhalb von 1 bis {höchstRunde}")
    if not isinstance(anliegen.status, Status):
        erlaubt = ", ".join(Status)
        verstöße.append(f"Status {anliegen.status} ist keiner von {erlaubt}")
    verstöße += antwortVerstöße(datei.read_text(encoding="utf-8"), anliegen)
    bekannt = {name.lower() for name in rollennamen(wurzel)} | {stakeholder.lower()}
    for rolle in (anliegen.absender, anliegen.empfänger):
        if rolle.lower() not in bekannt:
            verstöße.append(f"Rolle {rolle} gibt es nicht in .claude/agents/")
    return verstöße
