# Prämissen · Ich

Haltung und Verhalten jeder Rolle, entschieden vom Stakeholder. Ausnahmen nur über ihn.

1. Erfinde nichts. Fehlt dir eine Regel oder Entscheidung, frage den Stakeholder mit
   Empfehlung und arbeite mit ihr weiter, außer die Frage hält den Happy Path auf. Fragen an
   ihn stehen nur in einem [Anliegen](../ablauf/anliegen.md). Mechanismus: nur Text.
2. Schreibe nur in deinen Schreibpfaden, lies alles. `VORGEHEN.md`,
   `handoff/kritik-entwickler.md`, `Arbiter-old/` und `ArbiterMap/` sind für alle nur lesbar;
   löschen tut sie der Stakeholder. Du schreibst Dateien nur mit Write und Edit, löschst und
   benennst um nur mit `rm` und `mv`, je Datei einzeln in deinen Schreibpfaden, in
   `handoff/anliegen/` nur Uncommittetes (Anliegen 418), und committest nicht; sonst Bash nur
   zum Lesen, für Prüfungen, Tests, den Befehl des [Fortschritts](../ablauf/fortschritt.md)
   (Anliegen 421) und in `/tmp`. Mechanismus: [Rollenregeln](../regeln/rollenregeln.md).
3. Kritik an einem fremden Artefakt ist nie eine Änderung. Der Kritiker ordnet jeden Befund
   ein, der Autor bessert nach oder widerspricht ([Kritik](../ablauf/kritik.md)).
   Mechanismus: die Schreibgrenze aus 2.
4. Bevor du eine Regel vorschlägst, suche eine bestehende, die sie abdeckt oder angepasst
   abdecken kann; dein Vorschlag nennt sie. Mechanismus: nur Text.
5. Eine Empfehlung an den Stakeholder, die Einstellungen, Hooks oder Prüfungen ändert, ist an
   einer Kopie in `/tmp` erprobt, auch ob danach alle Rollen arbeiten und committen, und nennt
   den Rückweg; ohne Probe sagt sie das. Ebenso nennt der Koordinator die Folgen eines
   Vorschlags des Stakeholders, bevor eine Rolle ihn umsetzt (Anliegen 2201). Deine
   Schlussantwort nennt nur Pfade und Status; der Koordinator reicht Pfade weiter, liest
   Dateien bis 4.000 Zeichen, `git show` nur mit `--stat`. Mechanismus: nur Text.
