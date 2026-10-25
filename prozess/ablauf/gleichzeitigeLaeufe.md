# Gleichzeitige Läufe

Gleichzeitig laufen Rollen, die nur Anliegen schreiben, und Läufe zu verschiedenen Anliegen
oder Items, auch derselben Rolle, wenn (Anliegen 279):
1. ihre Dateien getrennt sind, nach Befund, Gegenvorschlag und `git status`; eine eigene
   Zeile in `prozess/regeln/` zählt als getrennt,
2. keiner auf den anderen wartet (`wartet auf`, Reihenfolge des Stakeholders),
3. höchstens einer Hook-Code ändert: Module, die `.claude/settings.json` startet, samt ihren
   Importen. Sie laufen aus demselben Arbeitsbaum als Hooks jedes Laufs.

Was danach gleichzeitig laufen darf, startet der Koordinator gleichzeitig (Anliegen 730). Sein
Auftrag nennt jeder Rolle, wer neben ihr läuft, und den Bereich, aus dem sie Nummern für neue
Anliegen vergibt; sie vergibt nur daraus. Mechanismus: nur Text; Nummern: `anliegenregeln/freieNummer.py` ([Anliegenregeln](../regeln/anliegenregeln.md)).
Die Moderation nennt je Rolle die Stränge: was gleichzeitig läuft, was eine Kette bleibt.
Der Koordinator committet je Item nach dessen Pfaden ([Commits](commits.md)); die Zeile eines
Nachbarn in `prozess/regeln/` geht mit. Ist eine Prüfung nur in Dateien eines laufenden Nachbarn
rot, nennt der Lauf sie und meldet fertig; committet wird, wenn der Commit-Hook grün ist. Mechanismus: Ein Importfehler im Prüfmodul eines Nachbarn macht nur
dessen Tests rot, `pyproject.toml` ([Formregeln](../regeln/formregeln.md), Anliegen 304); sonst nur Text.
