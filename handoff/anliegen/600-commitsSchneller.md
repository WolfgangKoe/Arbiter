# Schneller committen, ohne eine Prüfung aufzugeben

600 · Fragen · von Organisationsentwickler → Stakeholder · Runde 1/3 · rückfrage

## Runde 1
**Befund.** Dein Befund: Das Committen dauert zu lange. Heute gemessen (603 Prüfungen):
- Ein Lauf aller Prüfungen dauert 3:45 Minuten. Davon braucht eine einzige 1:40: die
  Abdeckung, die alle Produkttests samt Bildschirmtests noch einmal ausführt. Drei Proben
  für SonarLint, die je einen Java-Server starten, brauchen 1:05. Die übrigen 599 Prüfungen
  brauchen zusammen 54 Sekunden.
- Je Commit läuft alles zweimal: Der [Koordinator](../../.claude/agents/koordinator.md)
  prüft vorher selbst, dann prüft der Commit-Hook „Prüfungen“. Bei Python-Dateien läuft
  dazu SonarLint über das ganze Repo, und der Hook „Benennung“ prüft ein zweites Mal, was in
  „Prüfungen“ schon steckt.
- Die meisten Commits ändern nur Anliegen, Plan oder Texte (Kritik, Moderation,
  Freigaben). Sie können weder die Abdeckung noch die Proben der Prüfskripte ändern, warten
  aber gleich lang.
- Deshalb committete der Koordinator im Hintergrund, während andere Rollen liefen. Dabei
  gingen nicht committete Dateien verloren (Anliegen 610, die Ursache ist dort benannt).

**Kosten.** Je Commit 7 bis 8 Minuten Warten, bei 20 und mehr Commits je Zyklus Stunden.
Der Druck, im Hintergrund zu committen, gefährdet die Arbeit der gleichzeitig laufenden
Rollen.

**Gegenvorschlag.** Bestehende Regeln (Ich 4): die Commit-Regel des Koordinators und die
Commit-Hooks ([Regeln](../../prozess/regeln.md#formregeln)). Jede Prüfung bleibt, sie
läuft nur nicht doppelt und nicht umsonst. Den Bau beschreibt Anliegen 601 an den
Regelumsetzer; es beginnt nach deiner Antwort.

**F1 · Prüft der Koordinator vor dem Commit nicht mehr selbst?**
A: Ja. Es prüft nur noch der Commit-Hook. Ist eine Prüfung rot, scheitert der Commit und
der Koordinator meldet es.
B: Nein, er prüft weiter doppelt.
Empfehlung: A. Halbiert die Wartezeit bei gleichem Ergebnis. Nach Anliegen 610 ändert der
Hook keine Dateien mehr, ein gescheiterter Commit lässt alles stehen.
Antwort: .

**F2 · Führt der Commit-Hook die langsamen Teile nur aus, wenn der Commit sie betrifft?**
A: Ja. Die Abdeckung läuft nur, wenn der Commit `technik/` oder `pyproject.toml` ändert.
Die Proben der Prüfskripte laufen nur, wenn er `prozess/pruefungen/` oder eine
Prüfkonfiguration ändert. Der doppelte Hook „Benennung“ entfällt.
B: Nein, immer alles.
Empfehlung: A. Was ein Commit nicht ändert, kann er nicht rot machen. Ein Commit nur mit
Texten braucht dann unter einer Minute, einer mit Produktcode etwa 3 Minuten. Vollständig
prüfen weiterhin der Regelumsetzer, bevor er fertig meldet, und der Reviewer bei der DoD.
Antwort: .

**F3 · Laufen die Prüfungen auf allen Kernen gleichzeitig (pytest-xdist)?**
A: Ja, zuerst als Wegwerf-Versuch nach F1 und F2. Es bleibt nur, wenn alle Prüfungen dabei
dreimal hintereinander grün sind.
B: Nein.
Empfehlung: A. Geschätzt sinkt ein Commit nur mit Texten auf 15 bis 20 Sekunden. Bei
Produktcode bestimmt die Abdeckung (1:40) die Dauer, bis auch ihre Produkttests parallel
laufen. Risiko: Prüfungen, die dieselben Dateien nutzen, stören sich; das zeigt der Versuch.
Antwort: .

Nicht empfohlen: mehrere fertige Rollen in einem Commit bündeln. Die Kritik am Code prüft
je Commit ([Ablauf](../../prozess/ablauf.md#kritik-am-code)), und ein gebündelter Commit
wartet nicht kürzer.

**Stellungnahme.**
Kommentar: Ich habe in die aktuelle Session einen Screenshot gelegt, der die Thematik ggf. nochmal erweitert und vielleicht auch tiefer legt. Bitte im Transskript nachsehen
