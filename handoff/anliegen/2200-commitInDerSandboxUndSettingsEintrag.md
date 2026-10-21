# Der Koordinator kann in der Sandbox nicht committen: Eintrag in settings.json

Form: Fragen
Von: Regelumsetzer
An: Stakeholder
Runde: 2/3
Status: erledigt

## Runde 1
**Befund.** Zu P3 aus [Retro 6](../retro.md), Anliegen [1970](1970-sandboxFuerBashSchreibenNichtPruefbar.md),
[2050](2050-sonarlintBrauchtSchreibrechtInDerSandbox.md): Beim Commit legt pre-commit eine
Sicherungskopie unter `~/.cache/pre-commit` ab; der Käfig (die Sandbox) lässt das nicht zu, der
Commit bricht ab. SonarLint braucht `~/.sonarlint`.

**Gegenvorschlag.** Sicherungsort `/tmp/pre-commit` (dort darf der Käfig schreiben) und
`~/.sonarlint` freigeben. Verworfen: Commit ohne Käfig (Sperre hielte nicht), `~/.cache/pre-commit`
freigeben (ein Ort mehr).

**Stellungnahme.**

**F1 · Die beiden Änderungen eintragen?** Empfehlung: ja.
Antwort: Ja
Kommentar: HIer muss ich etwas machen. Du musst mir genau erklären, wie ich da vorgehen muss.
Kommentar: Was du hier schreibst, ist noch nicht genau genug

## Runde 2
**Befund.** Die Anleitung war zu ungenau. Hier die genaue.

**Stellungnahme.**

**Klärung.** Du änderst zwei Stellen in einer Datei. Die Datei darf nur du ändern, nicht die
Agenten. Zeilennummern gelten für den heutigen Stand.

*Schritt 0.* Sichere die Datei im Terminal im Projektordner:
`cp .claude/settings.json /tmp/settingsVorher.json`

*Schritt 1.* Öffne in VS Code die Datei
[.claude/settings.json](../../.claude/settings.json).

*Schritt 2.* Ersetze die Zeilen 7 bis 10, also von `"env": {` bis zur schließenden `},`, durch:
```
  "env": {
    "CLAUDE_CODE_DISABLE_GIT_INSTRUCTIONS": "1",
    "CLAUDE_CODE_DISABLE_CRON": "1",
    "PRE_COMMIT_HOME": "/tmp/pre-commit"
  },
```
Neu ist nur die dritte Zeile; in der Zeile davor kommt ein Komma hinzu.

*Schritt 3.* Ersetze die Zeile 17 (`"allowWrite": ["/tmp"],`) durch:
```
      "allowWrite": ["/tmp", "~/.sonarlint"],
```
Die Zeile `"network": {"allowAllUnixSockets": true},` (Zeile 15) lässt du stehen, bis du
[2160](2160-sitzungsbusAusDerSandboxSperren.md) beantwortet hast.

*Schritt 4.* Speichere (Strg+S). Prüfe im Terminal im Projektordner, dass die Datei gültig ist:
`python3 -m json.tool .claude/settings.json > /dev/null`
Keine Ausgabe heißt gültig; eine Fehlermeldung nennt die Zeile (meist ein vergessenes Komma).

*Schritt 5.* Beende Claude Code und starte es neu (die Einstellungen werden beim Start gelesen).

*Daran erkennst du den Erfolg.* Sage dem Koordinator nach dem Neustart „settings.json
eingetragen“. Er committet dann; geht der Commit durch, hat es geklappt. Danach ziehe ich die
Prüfung (`sandboxGrenzen.py`) nach, damit niemand die Einträge unbemerkt zurückdreht.
Geht etwas schief, ändert sich nichts an deinen Daten; mache die Änderung mit Strg+Z
rückgängig oder kopiere die Sicherung aus Schritt 0 zurück
(`cp /tmp/settingsVorher.json .claude/settings.json`) und sage mir Bescheid.

**F1 · Hast du `settings.json` so geändert und Claude Code neu gestartet?** Empfehlung: ja.
Annahme: Bis dahin bleibt alles wie heute.
Antwort: ja

**Abschluss.** Gegenstandslos: Der Stakeholder hat P3 gestrichen, die Sandbox entfällt
([1970](1970-sandboxFuerBashSchreibenNichtPruefbar.md)). Die Einträge `PRE_COMMIT_HOME` und
`~/.sonarlint` setzt er mit dem Sandbox-Block auf den Stand des letzten Commits zurück.
