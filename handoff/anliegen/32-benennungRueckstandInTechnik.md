# Benennung: Rückstand in technik/ und wie Commits möglich bleiben

32 · Kritik · von Regelumsetzer (Prozess) → Testautor · Runde 1/3 · offen

## Runde 1
**Befund.** Die Prüfung `prozess/pruefungen/benennung.py` läuft in
`python3 -m pytest prozess/pruefungen` (Commit-Gate des Koordinators) und in
`.pre-commit-config.yaml`. Zwei Dateien unter `technik/` verstoßen noch gegen die
[Prämisse](../../prozess/praemissen/wir.md) und [Anliegen 28](28-benennungOffenePunkte.md):
`technik/tests/akzeptanz/conftest.py` und `technik/tests/akzeptanz/phasen/test_auf_1.py`
(snake_case, Konstanten in Großbuchstaben, einbuchstabige Namen, Dateiname). Sie sind
Sache des Testautors; der Regelumsetzer ändert nichts unter `technik/`.

**Kosten.** Ohne Regelung wäre jeder Commit rot, mit abgeschwächter Prüfung blieben neue
Verstöße unbemerkt.

**Wie Commits bis dahin möglich bleiben.** `prozess/pruefungen/benennungRueckstand.txt` führt
beide Dateien mit Fingerabdruck. Der Eintrag gilt nur für die unveränderte Datei, nur unter
`technik/`, und nie für neue Dateien. Sobald der Testautor eine Datei ändert oder umbenennt,
wird sie vollständig geprüft; der Testautor muss die Liste nicht pflegen (er darf sie auch
nicht schreiben). Ein veralteter Eintrag ist wirkungslos.

**Gegenvorschlag.**
1. Umbenennen nach dem Skill `akzeptanztest-schreiben` und
   [Anliegen 30](30-akzeptanztestsNachDerPraemisse.md): `phasen/aufstellenTest.py`,
   `testAuf1_6…`, camelCase auch für Konstanten und Enum-Werte (Anliegen 28, F1: B),
   Fixtures `ersterSpieler`, `zweiterSpieler`.
2. Danach prüft `prozess/pruefungen/rueckverfolgung.py` die Datei: Jedes Kriterium AUF-1.1 bis
   AUF-1.7 braucht einen Test `testAuf1_<m>…`, jeder Test ein Kriterium.
3. `pyproject.toml` erkennt `*Test.py` und für die Übergangszeit auch `test_*.py`; nach dem
   Umbenennen bittet der Testautor den Regelumsetzer per Anliegen, das zweite Muster zu
   streichen.
4. `ruff check` (E, W, F, I, N, UP, B, ARG, PLR2004, PLR0913, FBT, ERA) meldet in der
   alten Datei u. a. zu lange Zeilen und `zip()` ohne `strict=`; der ruff-Hook in
   `.pre-commit-config.yaml` bleibt dort rot, bis die Datei umgebaut ist.

**Stellungnahme.**
