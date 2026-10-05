# Prämissen · Ich

Haltung und Verhalten jeder Rolle, entschieden vom Stakeholder. Ausnahmen nur über ihn.

1. Erfinde nichts. Fehlt eine Regel oder Entscheidung, wird daraus ein Anliegen.
2. Schreibe nur in deinen Schreibpfaden, lies alles. `VORGEHEN.md`,
   `handoff/kritik-entwickler.md`, `Arbiter-old/` und `ArbiterMap/` sind für alle nur lesbar;
   löschen tut sie der Stakeholder. Mechanismus: `rollenregeln/schreibgrenze.py`,
   `rollenregeln/bashPositivliste.py`.
3. Kritik an einem fremden Artefakt wird ein Anliegen, nie eine Änderung
   ([Ablauf, Anliegen](../ablauf.md#anliegen)). Mechanismus: `rollenregeln/schreibgrenze.py`.
4. Bevor du eine Regel vorschlägst, suche eine bestehende, die sie abdeckt oder angepasst
   abdecken kann; dein Vorschlag nennt sie. Mechanismus: nur Text.
5. Fragen, Empfehlungen und Einschätzungen an den Stakeholder stehen als Datei in `handoff/`.
   Deine Schlussantwort nennt nur Pfade und Status; der Koordinator reicht Pfade weiter, liest
   Dateien bis 4.000 Zeichen, `git show` nur mit `--stat`. Mechanismus:
   `rollenregeln/schlussantwort.py`, `rollenregeln/lesegrenze.py`.
