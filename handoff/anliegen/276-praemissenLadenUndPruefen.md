# Prämissen: laden, Höchstmaß, Verweise, CLAUDE.md ohne Mechanismus

276 · Kritik · von Organisationsentwickler (Prozess) → Regelumsetzer · Runde 1/3 · offen

## Runde 1
**Befund.** Der Stakeholder hat in Anliegen 255 (Runde 2) entschieden: Prämissen nach
Quadranten in `prozess/praemissen/` (`ich.md`, `es.md`, `wir.md`), F2 A, F3 A.
1. `es.md` soll nur laden, wo Code entsteht. Dafür steht `.claude/rules/es.md` mit `paths:`
   und Import. Ob Subagenten Regeln mit `paths:` und deren Import laden, sagt die
   Dokumentation nicht; das Bordmittel zum Messen ist der Hook `InstructionsLoaded`
   (`agent_type`, `file_path`, `load_reason`, `trigger_file_path`).
2. Eine CLAUDE.md enthält keine Regel mit Mechanismus; geprüft wird das nicht.
3. Prämissen haben höchstens 3.000 Zeichen ([Kennzahlen](../../prozess/kennzahlen.md)), nur Text.
4. Die Lesbarkeitsregeln stehen jetzt in `es.md`; auf `wir.md` verweisen noch
   `formregeln/benennung.py`, `kommentare.py`, `kommentareTest.py`, `sonarlint.py`,
   `sonarlintTest.py`, `frontendregeln/frontend.py`, `frontendTest.py`, `package.json`,
   `.stylelintrc.json`.

**Kosten.** Ohne Messung bleibt offen, ob `es.md` den Implementierer erreicht; die Verweise
in den Agentendefinitionen blieben doppelt. Ohne Prüfung wächst CLAUDE.md wieder.

**Gegenvorschlag.** Erledigt, wenn, je mit Scheiter-Test:
1. Ein Hook `InstructionsLoaded` schreibt je Ladevorgang Rolle, Datei, Grund und Auslöser
   in eine Datei unter `.git/arbiter/`; ein Befehl zeigt, welche Rolle `es.md` geladen hat.
2. `formregeln/hoechstmassTest.py`: Eine CLAUDE.md außerhalb der nur lesbaren Ordner mit
   `Mechanismus` ist rot; je Datei in `prozess/praemissen/` höchstens 3.000 Zeichen.
3. Die Verweise aus Befund 4 nennen `es.md` mit der Nummer der Regel.
Danach werte ich das Protokoll aus, nehme die Verweise auf `es.md` aus den
Agentendefinitionen, wenn sie laden, und ersetze „nur Text“.

**Stellungnahme.**
