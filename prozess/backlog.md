# Backlog · Prozess

Zurückgestellt, bis ein Befund es auslöst. Was ausgelöst ist, wird ein Prozess-Item der Retro.
Ein Mechanismus entsteht erst bei beobachtetem Bedarf (Retro 3).

- Höchstmaße der [Kennzahlen](kennzahlen.md) als Prüfung. Auslöser: Eine zu große Datei hält
  eine Rolle auf (Belegung über 120.000 beim Lesen) oder fällt im Review auf.
- Kopf der Anliegen nach Anliegen 254 in `anliegenregeln/anliegen.py` und `anliegenDran.py`:
  `Auftrag`, `· wartet auf`; `beantwortetDurchFreigabe` entfällt. Auslöser: Eine
  Rolle oder der Stakeholder braucht eins davon.
- Auslösezähler für Regeln, Rollen und Skills (E26). Auslöser: Eine Regel steht im Verdacht,
  nie zu greifen.
- Prüfungen zu DoR 1 bis 5 und kursiven Begriffen gegen das Glossar (E35). Auslöser: ein Item
  geht mit einem dieser Mängel in die Technikphase.
- Werkzeuge der DoD ([Ablauf](ablauf.md#dod-item-fertig)) außer complexipy, ruff,
  Code → Glossar, Abdeckung und vulture. Auslöser: Review oder Kritik am Code findet, was das
  Werkzeug meldet.
- Frontend und Backend parallel (Anliegen 241): jedes JSON-Beispiel des Vertrags steht in
  einem Test beider Hälften. Auslöser: der des Frontend-Implementierers
  ([Ablauf](ablauf.md#rollen-mit-auslöser)).
- Eigene Arbeitskopie je Lauf (Anliegen 279): `isolation: worktree` im Kopf der Rolle,
  Bedingung 3 der [gleichzeitigen Läufe](ablauf.md#gleichzeitige-läufe) fiele. Auslöser:
  Hook-Code oder rote Tests des Nachbarn halten zweimal eine Kette auf; zuerst ein
  Wegwerf-Versuch.
- Knöpfe im Dashboard für die Züge des Stakeholders (Anliegen 254). Auslöser: Die Sicht aus
  Anliegen 275 steht.
- Skills `anforderung-schreiben`, `regel-nachschlagen`, `improve` (E19, E30). Auslöser: dieselbe
  Kritik an derselben Art Artefakt zweimal.
- Update der SonarLint-Erweiterung (heute 6.0.1), ändert `erwarteteVersion` in
  `formregeln/sonarlint.py`. Auslöser: ein Befund in JSON-Dateien, den die Prüfungen nicht
  finden, oder ein anderer Grund für die neue Version.

Mechanismus: nur Text, Höchstmaß `prozess/kennzahlen.md` (Backlog je Perspektive).
