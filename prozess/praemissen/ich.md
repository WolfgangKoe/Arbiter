# Prämissen · Ich

Haltung und Verhalten jeder Rolle, entschieden vom Stakeholder. Ausnahmen nur über ihn.

1. Erfinde nichts. Fehlt eine Regel oder Entscheidung, wird daraus ein Anliegen.
2. Schreibe nur in deinen Schreibpfaden, lies alles. `VORGEHEN.md`,
   `handoff/kritik-entwickler.md`, `Arbiter-old/` und `ArbiterMap/` sind für alle nur lesbar;
   löschen tut sie der Stakeholder. Du schreibst Dateien nur mit Write und Edit, löschst und
   benennst um nur mit `rm` und `mv`, je Datei einzeln in deinen Schreibpfaden, in
   `handoff/anliegen/` nur Uncommittetes (Anliegen 418), und committest nicht; sonst Bash nur
   zum Lesen, für Prüfungen, Tests, den Befehl des [Fortschritts](../ablauf.md#fortschritt)
   (Anliegen 421) und in `/tmp`. Mechanismus: `rollenregeln/schreibgrenze.py`
   (Write, Edit und Bash; ein Skript, das selbst schreibt, nur Text, Anliegen 510),
   `rollenregeln/entfernen.py` (`rm`, `mv`); Lücken: [Regeln](../regeln.md#rollenregeln).
3. Kritik an einem fremden Artefakt ist nie eine Änderung. Ein Anliegen
   ([Ablauf](../ablauf.md#anliegen)) wird sie nur, wenn etwas aufhält: Das Item geht nicht
   weiter (Kriterium unklar, Test nicht schreibbar oder nicht grün zu machen), eine Prüfung
   oder die DoD ist rot, Code verstößt gegen [Es](es.md), oder der Stakeholder fragt. Die
   Befunde eines Kritiklaufs an einen Autor stehen in einem Anliegen. Übriger Feinschliff
   kommt in den Backlog der Perspektive und wird erledigt, wenn die Datei ohnehin geändert
   wird (Anliegen 630). Mechanismus: `rollenregeln/schreibgrenze.py` (keine Änderung);
   wann ein Anliegen: nur Text.
4. Bevor du eine Regel vorschlägst, suche eine bestehende, die sie abdeckt oder angepasst
   abdecken kann; dein Vorschlag nennt sie. Mechanismus: nur Text.
5. Fragen, Empfehlungen und Einschätzungen an den Stakeholder stehen als Datei in `handoff/`.
   Deine Schlussantwort nennt nur Pfade und Status; der Koordinator reicht Pfade weiter, liest
   Dateien bis 4.000 Zeichen, `git show` nur mit `--stat`. Mechanismus: nur Text.
