# Hook-Test übersieht `ModuleNotFoundError`

230 · Kritik · von Reviewer (Technik) → Regelumsetzer · Runde 1/3 · offen

## Runde 1
**Befund.** Kritik am Code von 4b492f5 (114 Teil A a). `pytest prozess/pruefungen` ist grün
(666 passed). Die Lücke steckt in `formregeln/einstellungenTest.py`,
`testJederHookLäuftOhnePythonpathBisZumImport`. Rot wird der Test nur, wenn
`"ImportError"` in stderr steht. Ein fehlender Querimport meldet aber
`ModuleNotFoundError: No module named …`, und darin kommt `ImportError` nicht vor.
`ImportError` meldet nur `runpy`, wenn das Modul hinter `lauf.py` fehlt. Das prüft
`einstellungen.verstöße` ohnehin.

Wegwerf-Versuch in einer Kopie unter `/tmp`: In `rollenregeln/lesegrenze.py` steht
`from agenten import projektordner` statt `from rollenregeln.agenten import …`. Dann gilt:
- `echo '{}' | python3 prozess/pruefungen/gemeinsam/lauf.py rollenregeln.lesegrenze` bricht ab
  mit `ModuleNotFoundError: No module named 'agenten'`;
- `pytest formregeln/einstellungenTest.py -k Pythonpath` ist grün (3 passed).

Nebenbei: Der Test ersetzt nur `$CLAUDE_PROJECT_DIR`, `skripte` auch `${CLAUDE_PROJECT_DIR}`.
Ein Hook in der zweiten Schreibweise liefe mit unaufgelöstem Pfad, und der Test merkte es nicht.

**Kosten.** Ein Hook, der beim Import abbricht, endet mit Code 1. Für Claude Code ist das
ein Fehler, der nicht sperrt. `schreibgrenze`, `lesegrenze`, `statusrecht` und
`bashPositivliste` fielen dann still aus, die Werkzeuge liefen ungeprüft weiter. Gerade
diesen Fall soll der Test nach dem Umzug abfangen (Anliegen 225).

**Gegenvorschlag.** In `testJederHookLäuftOhnePythonpathBisZumImport`:
1. Rot bei jedem Abbruch mit Traceback, nicht nur bei `ImportError`:
   `assert "Traceback" not in lauf.stderr`. Oder genauer: `"ModuleNotFoundError"` und
   `"ImportError"` prüfen.
2. Den Befehl über dieselbe Ersetzung laufen lassen wie `skripte`, also beide Schreibweisen.
   Am einfachsten zieht man die Ersetzung aus `skripte` in eine eigene Funktion und ruft sie
   an beiden Stellen auf.

Erledigt, wenn der Test am Gegenbeispiel oben (Import ohne Ordner in einem Hook-Skript) rot ist
und `python3 -m pytest prozess/pruefungen` grün ist.

**Stellungnahme.**
