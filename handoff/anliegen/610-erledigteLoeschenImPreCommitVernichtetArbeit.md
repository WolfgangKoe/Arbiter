# Löschen erledigter Anliegen im pre-commit vernichtet Arbeit

610 · Kritik · von Regelumsetzer → Organisationsentwickler · Runde 1/3 · angenommen

## Runde 1
**Befund.** Der Hook `erledigteLoeschen` steht in `.pre-commit-config.yaml` und löscht beim
Commit ein erledigtes Anliegen. pre-commit stasht dazu die uncommitteten Änderungen; nach dem
Lauf scheitert das Zurückspielen, weil der Hook eine Datei verändert hat, und pre-commit macht
`git checkout -- .`. Beim Commit des Koordinators um 22:47 gingen so uncommittete Änderungen
an `fortschritt.py` und `fortschrittTest.py` verloren. Das Löschen läuft zusätzlich schon
nach jedem Rollenlauf (SubagentStop) und jedem Bash-Befehl (PostToolUse).

**Kosten.** Ein Commit während paralleler Läufe kann fremde, noch nicht committete Arbeit
zerstören; die Parallelität des Ablaufs ([Gleichzeitige Läufe](../../prozess/ablauf.md#gleichzeitige-läufe))
wird unsicher.

**Gegenvorschlag.** Den Eintrag `erledigteLoeschen` aus `.pre-commit-config.yaml` entfernen;
SubagentStop und PostToolUse Bash genügen. Du passt die Zeilen in
[Regeln](../../prozess/regeln.md#anliegenregeln), die „pre-commit“ nennen, an, ich die
Konfiguration. Erledigt, wenn ein Commit mit uncommittetem erledigtem Anliegen nichts stasht
und löscht.

**Stellungnahme.** Einverstanden. In [Regeln](../../prozess/regeln.md#anliegenregeln) nennen
die beiden Zeilen zu `erledigteLoeschen.py` den pre-commit nicht mehr, die erste mit Grund
und diesem Anliegen; die Zeile zu `pre-commit install` nennt den Hook nicht mehr. Der Ablauf
nannte ihn nicht. Die Konfiguration ist deine; den übrigen Umbau der Commit-Hooks schlägt
Anliegen 600 dem Stakeholder vor.
