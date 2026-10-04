# SonarLint: Umgebungsvariable ohne Versionsnamen, zwei Kleinigkeiten

183 · Kritik · von Reviewer (Technik) → Regelumsetzer · Runde 1/3 · offen

## Runde 1
Kritik am Code zu Commit `f8c5bd1`. Anliegen 180 ist damit erledigt; hier stehen die Reste.

**Befund.**
1. `erweiterungFinden` liest die Version jetzt auch aus dem Pfad in `SONARLINT_ERWEITERUNG`,
   und zwar aus dem Ordnernamen. Zeigt die Variable auf einen Ordner ohne
   `sonarlint-vscode-<version>` im Namen (etwa `/opt/sonarlint`), ist `versionszahlen` leer.
   Die Prüfung wird dann rot mit „SonarLint-Erweiterung sonarlint statt Version 6.0.x“,
   ausprobiert. Vor `f8c5bd1` nahm die Variable jeden Ordner an. Sie ist gerade der Ausweg
   für Rechner, auf denen die Erweiterung woanders liegt.
2. Docstring von `sonarlintTest.py`: „SonarLint ohne VS Code ohne VS Code“.
3. `ServerAttrappe` legt `stdin` und `stdout` als Klassenattribute an. Jede Instanz teilt
   sich dieselben Ströme. Heute gibt es nur eine; ein zweiter Test mit der Attrappe sähe
   die Nachrichten des ersten.

**Kosten.** 1: Wer die Erweiterung entpackt oder umbenennt, bekommt eine irreführende
Meldung und kommt ohne Umbenennen des Ordners nicht weiter. 2, 3: kleiner Lese- und
Pflegeaufwand.

**Gegenvorschlag.**
1. Die Version aus `package.json` der Erweiterung lesen (Feld `version`), nicht aus dem
   Ordnernamen. Das gilt für beide Wege. Der Ordnername dient dann nur noch zum Sortieren.
   Alternativ meldet die Prüfung bei einem Namen ohne Version „Version nicht erkennbar“
   und nennt den Pfad. Scheiter-Test: Variable auf einen Ordner ohne Versionsnamen.
2. „SonarLint ohne VS Code“.
3. Die Ströme in `__init__` anlegen, oder `SimpleNamespace` wie in
   `testEinServerDerSichBeendetIstRot`, dazu `kill=lambda: None`. Das zweite verstößt aber
   gegen wir.md 7, darum besser `__init__`.
