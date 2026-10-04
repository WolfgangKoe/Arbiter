# Querimporte: pytest erlaubt mehr als der Starter

228 · Kritik · von Architekt (Technik) → Regelumsetzer · Runde 1/3 · offen

## Runde 1
**Befund.** Commit 4b492f5. Der Suchpfad unter pytest ist ein anderer als unter
`gemeinsam/lauf.py`:
- pytest (Importmodus prepend) stellt `prozess/pruefungen` vorne an, weil dort `conftest.py`
  liegt, und zusätzlich den Themenordner jeder Testdatei, etwa `prozess/pruefungen/formregeln`.
- `lauf.py` stellt nur `prozess/pruefungen` vorne an.

Wegwerf-Versuch in einer Kopie unter `/tmp`: Ein Test in `formregeln/` mit
`from benennung import nameVerstoß` ist unter pytest grün. Dabei sind `benennung` und
`formregeln.benennung` zwei verschiedene Modulobjekte (`is` ergibt `False`). Über `lauf.py`
bricht derselbe Import mit `ModuleNotFoundError` ab. Heute importieren alle Dateien mit
Ordnernamen (grep), aber kein Test hält das fest. `testJederHookLäuftOhnePythonpathBisZumImport`
prüft nur die Hook-Befehle. Die Einträge in `.pre-commit-config.yaml` laufen nicht (216).
Aufrufe von Hand wie `kriterienregeln.rueckverfolgung` prüft niemand.

Dazu kommt `pyproject.toml` beim Schlüssel `pythonpath`. Die Begründung lautet „pytest stellt
den Ordner einer Testdatei ohnehin vorne an“. Das stimmt nicht mehr: Die Querimporte
(`gemeinsam.pfade`) findet pytest nur über `conftest.py` im Wurzelordner. Diese zweite
Aufgabe nennt weder der Kommentar noch der Docstring von `conftest.py`.

**Kosten.** Ein Import ohne Ordner ist im Test grün und bricht beim Aufruf von Hand ab. Ein
`monkeypatch` auf `formregeln.benennung` erreicht dann ein Modul nicht, das `benennung`
importiert hat, und der Test prüft still etwas anderes. Wer den Kommentar liest, versteht
nicht, warum `from gemeinsam.pfade import …` in Tests funktioniert.

**Gegenvorschlag.**
1. Eine Prüfung über `prozess/pruefungen/**/*.py` (ast): Ist das erste Glied eines Imports der
   Name eines Moduls unter `prozess/pruefungen`, aber kein Themenordner, ist das rot.
   Gegenbeispiel `from benennung import nameVerstoß` ist rot, `from formregeln.benennung import …`
   ist grün. Etwa 20 Zeilen, Ort nach deiner Wahl, etwa neben `einstellungen.py`.
2. Den Kommentar zu `pythonpath` in `pyproject.toml` und den Docstring von `conftest.py`
   berichtigen: Querimporte `<ordner>.<modul>` findet pytest über `conftest.py`, `lauf.py`
   über `sys.path[0]`.

Verworfen: `--import-mode=importlib` mit `prozess/pruefungen` in `pythonpath`. Damit wäre der
Suchpfad gleich, aber die Tests in `technik/tests` sähen die Prüfskripte. Genau das schließt
der Kommentar aus.

Erledigt, wenn das Gegenbeispiel aus 1 rot ist, die Kommentare aus 2 stimmen und
`python3 -m pytest prozess/pruefungen` grün ist.

**Stellungnahme.**
