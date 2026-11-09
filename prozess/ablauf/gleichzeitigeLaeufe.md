# Gleichzeitige Läufe

Gleichzeitig laufen Rollen, die nur Anliegen schreiben, und Läufe zu verschiedenen Anliegen
oder Items, auch derselben Rolle, wenn (Anliegen 279):
1. ihre Dateien getrennt sind, nach Befund, Gegenvorschlag und `git status`; eine eigene
   Zeile in `prozess/regeln/` zählt als getrennt,
2. keiner auf den anderen wartet (`wartet auf`, Reihenfolge des Stakeholders),
3. höchstens einer Hook-Code ändert: Module, die `.claude/settings.json` startet, samt ihren
   Importen. Sie laufen aus demselben Arbeitsbaum als Hooks jedes Laufs.

Gleichzeitig ist die Regel ([Absicht 7](../praemissen/absicht.md)): Was danach darf, startet
der Koordinator gleichzeitig (Anliegen 730). Nach jedem Rollenlauf nennt ihm der Stand unter
„Frei“, was nicht wartet: die Anliegen, die dran sind, und die offenen Zeilen des
[Fortschritts](fortschritt.md), deren Vorgänger in dessen Tabelle abgehakt ist, je Item und
Prozess-Item für sich, ohne offenes `Hindernis:`. Was davon nicht schon läuft, startet er
oder nennt dem Stakeholder je den Grund: Bedingung 1 bis 3 oder die Reihenfolge des Plans
(Anliegen 14360). Mechanismus: nur Text, bis [P4](../../handoff/retro.md)
`standregeln/stand.py` (PostToolUse auf Agent) darum erweitert, samt dem Satz „Starte, was
frei ist, oder nenne je den Grund“. Der Auftrag des Koordinators nennt jeder Rolle, wer neben ihr läuft, und den Bereich, aus dem sie Nummern für neue
Anliegen vergibt; sie vergibt nur daraus. Mechanismus: nur Text; Nummern: `anliegenregeln/freieNummer.py` ([Anliegenregeln](../regeln/anliegenregeln.md)).
Ein Lauf, der Tests oder Prüfungen als Beleg meldet, liest alle Dateien, auch die der
Nachbarn: [DoD, Belege zu 1 und 2](dod.md); der Gesamtlauf darf neben Rollen laufen (allein
16, daneben 17 Minuten, Anliegen 14360).
Die Moderation nennt je Rolle die Stränge: was gleichzeitig läuft, was eine Kette bleibt.
Der Koordinator committet je Item nach dessen Pfaden ([Commits](commits.md)); die Zeile eines
Nachbarn in `prozess/regeln/` geht mit. Ist eine Prüfung nur in Dateien eines laufenden Nachbarn
rot, nennt der Lauf sie und meldet fertig; committet wird, wenn der Commit-Hook grün ist. Mechanismus: Ein Importfehler im Prüfmodul eines Nachbarn macht nur
dessen Tests rot, `pyproject.toml` ([Formregeln](../regeln/formregeln.md), Anliegen 304); sonst nur Text.
