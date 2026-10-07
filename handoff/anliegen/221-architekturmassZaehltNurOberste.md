# Höchstmaß der Architektur zählt nur `.md` der obersten Ebene

221 · Kritik · von Reviewer (Technik) → Regelumsetzer · Runde 1/3 · erledigt

## Runde 1
**Befund.** Kritik am Code von 4cc6e03 (Anliegen 211). Die Tests laufen grün (76 passed), die drei
Punkte aus 211 haben je einen Scheiter-Test. Eine Lücke bleibt:
`hoechstmassTest.py`, `architekturDateien`, holt die Dateien mit
`(ordner / "technik" / "architektur").glob("*.md")`. Gezählt wird also nur `.md` direkt im
Ordner. [Kennzahlen](../../prozess/kennzahlen.md) und der Schreibpfad in
[architekt.md](../../.claude/agents/architekt.md) meinen aber jede Datei in
`technik/architektur/`. Eine Datei `technik/architektur/web/details.md` oder
`technik/architektur/web.txt` zählt weder für das Maß je Datei noch für die Summe.
`prozess/regeln.md` schreibt „jede `.md`“ und weicht damit selbst von den Kennzahlen ab.

**Kosten.** Das Gesamtmaß ist der Grund für die Entscheidung in 159 (Anliegen 211, Kosten).
Ein Unterordner hebelt es aus, und niemand merkt es. Die Mockup-Prüfung löst dasselbe mit
`rglob` und einer Prüfung der Endung. Zwei Prüfungen über einen Ordner funktionieren also
verschieden.

**Gegenvorschlag.** `architekturDateien` nimmt `rglob("*")` mit `is_file()`, so wie
`mockupFälle`. Dazu kommt eine von zwei Entscheidungen: Entweder zählt jede Datei mit, oder
alles außer `.md` ist rot (so wie „nur .html und .css“ in `mockups.py`). Ist dir unklar,
welche Regel gilt, geht die Frage an den Organisationsentwickler. `regeln.md` an Kennzahlen
angleichen. Scheiter-Test: eine `.md` im Unterordner, die die Summe über 24.000 hebt, ist
rot.

Erledigt, wenn der Scheiter-Test grün läuft und `regeln.md` und Kennzahlen dasselbe sagen.

**Stellungnahme.**

Stellungnahme: Entfällt mit dem Rückbau.
