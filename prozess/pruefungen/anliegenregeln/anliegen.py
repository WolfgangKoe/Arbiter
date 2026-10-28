from pathlib import Path

from lesen.agenten import rollennamen
from lesen.anliegenKopf import Status, felderLesen, höchstRunde, kopfLesen, stakeholder, typWerte


def kopfVerstöße(datei: Path, wurzel: Path) -> list[str]:
    zeilen = datei.read_text(encoding="utf-8").splitlines()
    if not zeilen or not zeilen[0].startswith("# "):
        return ["Zeile 1 ist kein Titel `# <Titel>`"]
    if not felderLesen(zeilen):
        return [
            "Zeile 3: Kopf als Felder je Zeile erwartet: `Form:`, `Von:`, `An:`, "
            f"`Runde: <n>/{höchstRunde}`, `Status:`, dahinter höchstens `Wartet auf: <nr>` "
            "oder `Wartet auf: Prozessphase`"
        ]
    anliegen = kopfLesen(datei)
    if anliegen is None:
        return [
            "Kopf unvollständig oder ungültig: alle Felder bis `Status`, `Runde` als `<n>/3`, "
            "`Wartet auf` als Nummer oder Phase, Dateiname `<nr>-<kurz>.md`"
        ]
    verstöße = []
    if anliegen.typ not in typWerte:
        verstöße.append(f"Form {anliegen.typ} ist keine von {', '.join(typWerte)}")
    if not 1 <= anliegen.runde <= höchstRunde:
        verstöße.append(f"Runde {anliegen.runde} liegt außerhalb von 1 bis {höchstRunde}")
    if not isinstance(anliegen.status, Status):
        erlaubt = ", ".join(Status)
        verstöße.append(f"Status {anliegen.status} ist keiner von {erlaubt}")
    bekannt = {name.lower() for name in rollennamen(wurzel)} | {stakeholder.lower()}
    for rolle in (anliegen.absender, anliegen.empfänger):
        if rolle.lower() not in bekannt:
            verstöße.append(f"Rolle {rolle} gibt es nicht in .claude/agents/")
        elif rolle != rolle.capitalize():
            verstöße.append(f"Rolle {rolle} wird groß geschrieben: {rolle.capitalize()}")
    return verstöße
