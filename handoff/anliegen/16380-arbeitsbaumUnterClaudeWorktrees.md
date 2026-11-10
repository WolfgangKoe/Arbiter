# Lauf im Arbeitsbaum unter .claude/worktrees/ kann nichts schreiben

Form: Fragen
Von: Regelumsetzer
An: Stakeholder
Runde: 1/3
Status: erledigt

## Runde 1
**Befund.** Ein Lauf im Arbeitsbaum `.claude/worktrees/agent-…/` meldete: „regelumsetzer darf
`.claude/worktrees/agent-…/prozess/pruefungen/gemeinsam/gitAufruf.py` nicht schreiben“. Damit
geht Parallelarbeit in eigenen Arbeitsbäumen nicht (Anliegen 14360,
[Absicht 7](../../prozess/praemissen/absicht.md)).
Ursache (gelesen, nicht erprobt): Die Hooks laufen aus dem Projektordner. In
[schreibgrenze.py](../../prozess/pruefungen/rollenregeln/schreibgrenze.py) (`vorDemSchreiben`) wird
der Pfad relativ zu diesem Ordner gebildet; er lautet dann `.claude/worktrees/agent-…/prozess/…`
und liegt in keinem Schreibpfad der Rolle.
Bestehende Regel (Ich 4): [Commits](../../prozess/ablauf/commits.md) (P4) lässt den Commit in einem
Arbeitsbaum unter `/tmp` laufen; der Arbeitsbaum der Rolle selbst ist dort nicht geregelt, die
Schreibgrenze kennt ihn nicht.

**Kosten.** A: eine kleine Änderung in `schreibgrenze.py` samt Test, ein Lauf des Regelumsetzers.
Sie ändert Hook-Code und wartet darum auf den Lauf zu P4, der dieselbe Datei ändert
([Gleichzeitige Läufe](../../prozess/ablauf/gleichzeitigeLaeufe.md), Bedingung 3).

**Gegenvorschlag.** Siehe F1.

**Stellungnahme.**

**F1 · Wie dürfen Rollen im Arbeitsbaum unter `.claude/worktrees/` schreiben?**
A: `vorDemSchreiben` kürzt das Präfix `.claude/worktrees/<name>/` vom Pfad, bevor es gegen die
Schreibpfade prüft; der Arbeitsbaum zählt dann wie der Projektordner. Scheiter-Test:
Schreiben von `.claude/worktrees/agent-x/prozess/pruefungen/…` ist für den Regelumsetzer erlaubt,
`…/domaene/…` nicht. Danach nach P4 umsetzen. (Absicht 7, Anliegen 14360)
B: Läufe laufen weiter im gemeinsamen Arbeitsbaum, parallel nur bei getrennten Dateien
(Bedingung 1 bis 3 der Läufe). (Anliegen 279)
Empfehlung: A, denn B verzichtet auf die Parallelität, die Absicht 7 verlangt. Ohne Probe;
Rückweg: Commit zurücknehmen. Offen bleibt, wie die Änderungen des Arbeitsbaums nach `dev`
kommen: `zuegeUebernehmen.py` (P4) kennt nur `/tmp`.
Antwort: A, probieren wir es aus.
Stellungnahme: Umgesetzt. `ohneArbeitsbaum` in `gemeinsam/pfade.py` kürzt `.claude/worktrees/<name>/`; `vorDemSchreiben` (Write, Edit) prüft den gekürzten Pfad gegen Schreibpfade, Nur-lesbar und Regelsperre; Test `testImArbeitsbaumUnterClaudeWorktreesGeltenDieSchreibpfadeWieImProjektordner`. Nicht erfasst: Bash-Schreiben im Arbeitsbaum (`rm`, `mv`) und die Übernahme der Änderungen nach `dev` (offen, eigenes Anliegen nötig).

**Klärung.**
Worum es geht: Für gleichzeitige Arbeit (Absicht 7) kann jede Rolle eine eigene Kopie des Projekts
bekommen, einen „Arbeitsbaum“, und darin ändern, ohne andere zu stören. Die Sperre, die jede Rolle auf
ihre Ordner beschränkt, erkennt Dateien in dieser Kopie nicht als erlaubt und verweigert das Schreiben.

Was du heute merkst: Rollen laufen nur gleichzeitig, wenn sie verschiedene Dateien im gemeinsamen
Projekt ändern; wer dieselben braucht, wartet, und du wartest länger.

**A · Sperre kennt die Kopien.**
- Du: mehr gleichzeitige Läufe, kürzere Wartezeit; am Bildschirm ändert sich nichts.
- Rollen: gleiche Rechte, nur in ihrer Kopie.
- Token: etwas mehr, weil mehr Rollen zugleich ihren Kontext lesen.
- Schuld: eine kleine Änderung an der Sicherheitsdatei, die alle Rollen binden, mit Test. Ein Fehler
  dort ließe Rollen zu viel schreiben; darum erst nach P4, das dieselbe Datei ändert.

**B · Alles bleibt.** Du: keine Änderung, aber Parallelität nur bei getrennten Dateien. Rollen,
Token, Schuld: unverändert.

Offen bei A: Wie Änderungen aus der Kopie ins Projekt kommen; das Skript von P4 kennt nur
`/tmp`. Das wäre ein eigenes Anliegen.

Empfehlung: A, die kleinste Änderung für das, was Absicht 7 verlangt. Nicht erprobt; Rückweg:
Commit zurücknehmen.
