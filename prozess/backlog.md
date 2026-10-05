# Backlog · Prozess

Zurückgestellt, bis ein Befund es auslöst. Was ausgelöst ist, wird ein Prozess-Item der Retro.

Ausgelöst, ohne Wirkung auf Plan 3 (Anliegen 156); Auslöser: Prozessphase Zyklus 3.
- Höchstmaße in `formregeln/hoechstmassTest.py`: Code-Modul 12.000 (auch `conftest.py`,
  Anliegen 251), Einheitstest-Datei 8.000; vorher `kriterienregeln/rueckverfolgung.py` (114 B 7), `kriterienregeln/rueckverfolgungTest.py` und
  `standregeln/standTest.py` teilen (Retro 2, Befund 4).
- `standregeln/kennzahlen.py` rechnet die Prozesslast.
- Anliegen 114 (Prüfskripte ordnen) und 139 (Sandbox, nach der Entscheidung des Stakeholders).

- Auslösezähler für Regeln, Rollen und Skills (E26). Auslöser: Retro 3, oder eine Regel
  steht im Verdacht, nie zu greifen.
- Prüfungen zu DoR 1 bis 5 und kursiven Begriffen gegen das Glossar (E35). Auslöser: ein Item
  geht mit einem dieser Mängel in die Technikphase.
- Werkzeuge der DoD ([Ablauf](ablauf.md#dod-item-fertig)) außer complexipy, ruff,
  Code → Glossar, Abdeckung und vulture; import-linter ist ausgelöst (Anliegen 253). Auslöser:
  Review oder Kritik am Code findet, was das Werkzeug meldet.
- Frontend und Backend parallel (Anliegen 241): Der Stand nennt beide Implementierer
  zugleich (`standregeln/stand.py`); jedes JSON-Beispiel des Vertrags steht in einem Test
  beider Hälften. Auslöser: der des Frontend-Implementierers
  ([Ablauf](ablauf.md#rollen-mit-auslöser)).
- Skills `anforderung-schreiben`, `regel-nachschlagen`, `improve` (E19, E30). Auslöser: dieselbe
  Kritik an derselben Art Artefakt zweimal.
- Update der SonarLint-Erweiterung (heute 6.0.1): VS Code meldet wiederholt, JSON-Dateien
  analysiere SonarQube erst ab einer neueren Version (Befund des Stakeholders). Ein Update
  ändert `erwarteteVersion` in `formregeln/sonarlint.py` (6.0.), sonst ist die Sperre rot.
  Auslöser: ein Befund in JSON-Dateien, den die Prüfungen nicht finden, oder ein Grund
  für die neue Version jenseits von JSON.

Mechanismus: nur Text, Höchstmaß `prozess/kennzahlen.md` (Backlog je Perspektive).
