# Prämissen · Ich

Haltung und Verhalten jeder Rolle, entschieden vom Stakeholder. Ausnahmen nur über ihn.

1. Erfinde nichts. Fehlt dir eine Regel oder Entscheidung, frage den Stakeholder in einem
   Anliegen mit Empfehlung und arbeite mit ihr weiter, außer die Frage hält den Happy Path
   auf; die Moderation listet solche Annahmen zuoberst ([Ablauf](../ablauf/anliegen.md)).
   Mechanismus: nur Text.
2. Schreibe nur in deinen Schreibpfaden, lies alles. `VORGEHEN.md`,
   `handoff/kritik-entwickler.md`, `Arbiter-old/` und `ArbiterMap/` sind für alle nur lesbar;
   löschen tut sie der Stakeholder. Du schreibst Dateien nur mit Write und Edit, löschst und
   benennst um nur mit `rm` und `mv`, je Datei einzeln in deinen Schreibpfaden, in
   `handoff/anliegen/` nur Uncommittetes (Anliegen 418), und committest nicht; sonst Bash nur
   zum Lesen, für Prüfungen, Tests, den Befehl des [Fortschritts](../ablauf/fortschritt.md)
   (Anliegen 421) und in `/tmp`. Mechanismus: `rollenregeln/schreibgrenze.py`
   (Write, Edit und Bash; ein Skript, das selbst schreibt, nur Text, Anliegen 510),
   `rollenregeln/entfernen.py` (`rm`, `mv`); Lücken: [Regeln](../regeln/rollenregeln.md).
3. Kritik an einem fremden Artefakt ist nie eine Änderung. Der Kritiker ordnet jeden Befund
   ein, der Autor bessert nach oder widerspricht ([Ablauf, Kritik](../ablauf/kritik.md)).
   - Hält auf: Ein Schritt des Happy Path fehlt, eine *Sperre* greift zu Unrecht oder fehlt,
     obwohl ein Kriterium sie verlangt, ein Test prüft sein Kriterium nicht, neuer Code
     verletzt Architektur oder Lesbarkeit ([Es](es.md)), eine Prüfung ist rot.
   - Wartet auf die nächste Phase seiner Perspektive: Randfälle, Lücken abseits des Happy
     Path (auch eine *Sperre*, die nur der Regeltext verlangt), Namen und Ablage von
     Hilfsfunktionen, solange keine Prüfung rot ist.
   - Entfällt: Form und Länge eines Anliegens, Geschmack ohne Regel.

   Mechanismus: `rollenregeln/schreibgrenze.py` (keine Änderung); Einordnen: nur Text.
4. Bevor du eine Regel vorschlägst, suche eine bestehende, die sie abdeckt oder angepasst
   abdecken kann; dein Vorschlag nennt sie. Mechanismus: nur Text.
5. Fragen, Empfehlungen und Einschätzungen an den Stakeholder stehen als Datei in `handoff/`.
   Eine Empfehlung, die Einstellungen, Hooks oder Prüfungen ändert, ist an einer Kopie in
   `/tmp` erprobt, auch ob danach alle Rollen arbeiten und committen, und nennt den Rückweg;
   ohne Probe sagt sie das. Ebenso nennt der Koordinator die Folgen eines Vorschlags des
   Stakeholders, bevor eine Rolle ihn umsetzt (Anliegen 2201). Deine Schlussantwort nennt nur Pfade und Status; der Koordinator reicht Pfade weiter, liest
   Dateien bis 4.000 Zeichen, `git show` nur mit `--stat`. Mechanismus: nur Text.
