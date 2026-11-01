import re
from pathlib import Path

from lesen.agenten import rollennamen
from lesen.anliegenKopf import (
    Anliegen,
    Status,
    felderLesen,
    höchstRunde,
    kopfLesen,
    stakeholder,
    typWerte,
)

kürzelLänge = 2
frageZeile = re.compile(r"\*\*F\d+ · ")
offeneAntwort = {"", "."}
pflichtZeilen = ("A:", "Empfehlung:")


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
        elif rolle != schreibweise(rolle):
            verstöße.append(f"Rolle {rolle} wird so geschrieben: {schreibweise(rolle)}")
    return verstöße + antwortVerstöße(zeilen, anliegen)


def antwortVerstöße(zeilen: list[str], anliegen: Anliegen) -> list[str]:
    if anliegen.empfänger != stakeholder or anliegen.status == Status.erledigt:
        return []
    verstöße = []
    for beginn, zeile in enumerate(zeilen):
        if frageZeile.match(zeile):
            fehlend = fehlendeZeilen(zeilen[beginn + 1 :])
            verstöße += [f"Zeile {beginn + 1}: Frage ohne Zeile `{text}`" for text in fehlend]
    return verstöße


def fehlendeZeilen(frage: list[str]) -> list[str]:
    antworten = [stelle for stelle, text in enumerate(frage) if text.startswith("Antwort:")]
    if not antworten or frage[antworten[0]].removeprefix("Antwort:").strip() not in offeneAntwort:
        return []
    davor = frage[: antworten[0]]
    return [
        pflicht
        for pflicht in pflichtZeilen
        if not any(zeile.startswith(pflicht) for zeile in davor)
    ]


def schreibweise(rolle: str) -> str:
    return rolle.upper() if len(rolle) <= kürzelLänge else rolle.capitalize()
