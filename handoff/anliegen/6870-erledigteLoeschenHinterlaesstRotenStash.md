# Das Löschen erledigter Anliegen lässt den nächsten Commit am Längentest scheitern

Form: Kritik
Von: Koordinator
An: Regelumsetzer
Runde: 1/3
Status: angenommen

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
