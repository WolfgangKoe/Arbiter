# Zwei Prüfungen über die Prüfskripte sehen die Unterordner nicht

231 · Kritik · von Reviewer (Technik) → Regelumsetzer · Runde 1/3 · offen

## Runde 1
**Befund.** Kritik am Code von 4b492f5 (114 Teil A a). Mit dem Umzug decken zwei Prüfungen
nicht mehr alle Prüfskripte ab, sondern nur noch einen Teil:

1. `formregeln/konfigurationTest.py`, `testPytestFindetAlleTestdateienDerPrüfungen`. Der Test
   setzt `ordner = Path(__file__).resolve().parent`. Vor dem Umzug war das
   `prozess/pruefungen`, jetzt ist es `formregeln/`. `--collect-only` und `glob("*Test.py")`
   sehen nur noch die Tests in `formregeln/`. Eine Testdatei in `standregeln/`, die pytest
   nicht sammelt, bleibt unbemerkt, obwohl der Name „alle Testdateien“ verspricht.
2. `formregeln/abdeckung.py` misst mit `coverage --source=prozess/pruefungen`. Eine Datei,
   die kein Test importiert, nimmt coverage nur dann als 0 % in die Messung, wenn sie direkt
   im Quellordner liegt oder in einem Ordner mit `__init__.py`. Die Themenordner haben keine
   `__init__.py`. Wegwerf-Versuch unter `/tmp` (coverage 7.16.2): `q/oben.py` ohne Test
   steht mit 0 % im Bericht, `q/unter/nieImportiert.py` fehlt ganz. Mit
   `[tool.coverage.report] include_namespace_packages = true` steht sie wieder drin.

**Kosten.** Beide Prüfungen bleiben grün, prüfen aber weniger als vorher. Ein neues
Prüfskript ohne jeden Test drückt die Abdeckung nicht unter 95 %, es kommt in der Messung
gar nicht vor (DoD 1). Eine Testdatei, die pytest übersieht, fällt außerhalb von
`formregeln/` nicht mehr auf.

**Gegenvorschlag.**
1. `ordner` zeigt auf `prozess/pruefungen` (etwa `wurzel / "prozess" / "pruefungen"`),
   gesucht wird mit `rglob("*Test.py")`. Verglichen wird der Pfad relativ zu `ordner`, nicht
   nur der Dateiname: Zwei gleichnamige Tests in verschiedenen Ordnern sollen nicht
   zusammenfallen.
2. `include_namespace_packages = true` setzen, mit einer `# Warum:`-Zeile, etwa in
   `pyproject.toml` unter `[tool.coverage.report]`. Achtung: Die Probe in `abdeckungTest.py`
   schreibt ihr eigenes `pyproject.toml`. Der Scheiter-Test muss also dieselbe Einstellung
   treffen wie die echte Messung, sonst prüft er eine Kopie. Ort nach deiner Wahl. Der Fall
   für den Scheiter-Test: In der Probe liegt `quelle/unter/modul.py`, kein Test importiert es,
   und die Abdeckung liegt unter der Schwelle.

Erledigt, wenn beide Scheiter-Tests an ihrem Gegenbeispiel rot sind (Testdatei in einem
anderen Themenordner, die nicht gesammelt wird; Modul ohne Test im Unterordner) und
`python3 -m pytest prozess/pruefungen` grün ist.

**Stellungnahme.**

Stellungnahme: Entfällt mit dem Rückbau.
