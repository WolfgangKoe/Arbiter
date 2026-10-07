# Backlog · Prozess

Zurückgestellt, bis ein Befund es auslöst. Was ausgelöst ist, wird ein Prozess-Item der Retro.

Neue Mechanismen, zurückgestellt wegen der Prozesslast (Retro 3); Auslöser: Retro 4 mit
Prozesslast unter der Schwelle.
- Höchstmaße in `formregeln/hoechstmassTest.py`: Code-Modul 12.000 (auch `conftest.py`,
  Anliegen 251), Einheitstest-Datei 8.000; vorher zu große Dateien teilen (Retro 2, Befund 4).
- Gesamtmaß für `prozess/pruefungen/`, damit Löschen wie Hinzufügen zählt (Anliegen 107).
- Auslösezähler für Regeln, Rollen und Skills (E26), oder eine Regel steht im Verdacht, nie
  zu greifen.

- Nachschliff an Prüfskripten (Anliegen 202 bis 206, 221; Anliegen 296). Auslöser: Der
  Regelumsetzer ändert die Datei ohnehin.
- Prüfungen zu DoR 1 bis 5 und kursiven Begriffen gegen das Glossar (E35). Auslöser: ein Item
  geht mit einem dieser Mängel in die Technikphase.
- Werkzeuge der DoD ([Ablauf](ablauf.md#dod-item-fertig)) außer complexipy, ruff,
  Code → Glossar, Abdeckung und vulture; import-linter ist ausgelöst (Anliegen 253). Auslöser:
  Review oder Kritik am Code findet, was das Werkzeug meldet.
- Frontend und Backend parallel (Anliegen 241): Der Stand nennt beide Implementierer
  zugleich (`standregeln/stand.py`); jedes JSON-Beispiel des Vertrags steht in einem Test
  beider Hälften. Auslöser: der des Frontend-Implementierers
  ([Ablauf](ablauf.md#rollen-mit-auslöser)).
- Eigene Arbeitskopie je Lauf (Anliegen 279, F1): `isolation: worktree` im Kopf der Rolle,
  Worktree unter `.claude/worktrees/`; Hooks laufen weiter aus dem Hauptbaum
  (`$CLAUDE_PROJECT_DIR`), Bedingung 3 der [gleichzeitigen Läufe](ablauf.md#gleichzeitige-läufe)
  fiele. Braucht `worktree.baseRef: "head"`, `.gitignore`, Worktree-Pfade in der Schreibgrenze,
  Merge durch den Koordinator; offen: `node_modules` und `pip install -e` zeigen auf den
  Hauptbaum. Auslöser: Hook-Code oder rote Tests des Nachbarn halten in zwei Moderationen eine
  Kette auf; dann zuerst ein Wegwerf-Versuch.
- Knöpfe im Dashboard für die Züge des Stakeholders (Anliegen 254, braucht einen lokalen
  Server). Auslöser: Die Sicht aus Anliegen 275 steht.
- Skills `anforderung-schreiben`, `regel-nachschlagen`, `improve` (E19, E30). Auslöser: dieselbe
  Kritik an derselben Art Artefakt zweimal.
- Update der SonarLint-Erweiterung (heute 6.0.1): VS Code meldet wiederholt, JSON-Dateien
  analysiere SonarQube erst ab einer neueren Version (Befund des Stakeholders). Ein Update
  ändert `erwarteteVersion` in `formregeln/sonarlint.py` (6.0.), sonst ist die Sperre rot.
  Auslöser: ein Befund in JSON-Dateien, den die Prüfungen nicht finden, oder ein Grund
  für die neue Version jenseits von JSON.

Mechanismus: nur Text, Höchstmaß `prozess/kennzahlen.md` (Backlog je Perspektive).
