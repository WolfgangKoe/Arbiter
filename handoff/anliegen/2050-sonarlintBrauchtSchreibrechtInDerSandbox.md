# SonarLint kann in der Sandbox nicht schreiben, die Prüfung bleibt rot

Form: Fragen
Von: Regelumsetzer
An: Stakeholder
Runde: 1/3
Status: erledigt

## Runde 1
**Befund.** Zu P3 aus [Retro 6](../retro.md), Anliegen [1970](1970-sandboxFuerBashSchreibenNichtPruefbar.md):
SonarLint schreibt in `~/.sonarlint`; im Bash-Sandkasten ist das nur lesbar (belegt:
`open('/home/wolfgang/.sonarlint/x','w')` gibt „Das Dateisystem ist nur lesbar“). Der Lauf bricht
nach 120 Sekunden ab: `formregeln.sonarlint` und drei Tests in `formregeln/sonarlintTest.py`
sind rot. `lauf.py *` ist ausgenommen, `python3 -m pytest prozess/pruefungen` nicht; damit
wäre die Prüfung der DoD mit der Sandbox dauerhaft rot.

**Kosten.** Die Sandbox lässt sich nicht freigeben, ohne dass ein Teil der Prüfung ausfällt.

**Gegenvorschlag.** `allowWrite` um `~/.sonarlint` erweitern (außerhalb des Projekts, keine
Quelle); `sandboxGrenzen.py` lässt genau diesen Eintrag zu, der Scheiter-Test bleibt rot für
jeden weiteren. Verworfen: `pytest` als vierte Ausnahme (`excludedCommands`), denn dann liefe
jeder Test ohne Sandbox.

**Stellungnahme.**

**F1 · `~/.sonarlint` freigeben?** Empfehlung: ja. Ich ändere `settings.json` erst nach deiner
Antwort, denn die Sandbox ist deine Grenze (1970 F1).
Annahme: Bis dahin bleibt die Sandbox wie in 1970 und die SonarLint-Prüfung rot.
Antwort: ja

**Abschluss.** Gegenstandslos: Der Stakeholder hat P3 gestrichen, die Sandbox entfällt
([1970](1970-sandboxFuerBashSchreibenNichtPruefbar.md)). SonarLint schreibt wieder frei.
