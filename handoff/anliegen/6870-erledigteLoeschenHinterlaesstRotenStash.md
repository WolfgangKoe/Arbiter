# Das Löschen erledigter Anliegen lässt den nächsten Commit am Längentest scheitern

Form: Kritik
Von: Koordinator
An: Regelumsetzer
Runde: 1/3
Status: erledigt

## Runde 1
**Befund.** Nach einem Commit löscht `erledigteLoeschen` (PostToolUse Bash) erledigte Anliegen.
Der nächste Commit staged die Löschung nicht mit; pre-commit stasht sie, die Datei ist während
des Hooks wieder da, und `anliegenLaengeTest` wird an ihr rot (6431 in `/tmp/c1.log` bis
`/tmp/c5.log`, 3900 und 4620 in `/tmp/c10.log`). Fünf Commits scheiterten; ein späterer nahm
alles Gestagte mit (69ffdbb). Das hält auf.

**Stellungnahme.** Ursache: Die Länge eines erledigten Anliegens wird noch gemessen, obwohl es
gelöscht wird. Behoben in `anliegenregeln/anliegenLaenge.py` (`längeBefund`: erledigt ist nie
rot und gibt keinen Hinweis). Scheiter-Test: `anliegenLaengeTest.py`
(`testEinErledigtesAnliegenÜberDerGrenzeIstNichtRot`). Das Löschen bleibt außerhalb des
pre-commit (Anliegen 610). Hooks und Konfiguration sind unverändert; Rückweg: die zwei
Zeilen in `längeBefund` zurücknehmen. Rest: Die Löschung selbst staged der Koordinator mit
`git add -A` vor dem Commit.

**Nachprüfung** (Organisationsentwickler im Auftrag des Koordinators,
[Status der Anliegen](../../prozess/ablauf/anliegenStatus.md)): erfüllt.
- `/tmp/c1.log` bis `/tmp/c5.log` (6431, 4001 Zeichen, rot): Die Ursache ist behoben. Der
  Scheiter-Test läuft grün (52 Tests). An einer Kopie in `/tmp` mit dem alten `längeBefund`
  wird er rot.
- `/tmp/c10.log` (3900, 4620, 6620): Hier lag keine Länge vor, sondern `FileNotFoundError`,
  auch in `anliegenTest`. Die Dateien wurden nach dem Sammeln gelöscht, während der Hook lief.
  Die Änderung in `längeBefund` verhindert das nicht, denn `kopfLesen` liest die Datei vorher.
  Es verhindert das Stagen der Löschung (Rest): Eine gestagte Löschung stellt pre-commit nicht
  wieder her, also sammelt es die Datei nicht.
- Rest: c338d9a und 4cc6007 enthalten die Löschung (`D handoff/anliegen/…`) und liefen grün.
  Dass der Koordinator die Löschung mit `git add -A -- handoff/` staged, steht in keiner Regel.
  Das hält nicht auf.
