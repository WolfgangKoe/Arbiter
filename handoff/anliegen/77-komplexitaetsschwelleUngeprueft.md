# Komplexitätsschwelle: Version frei, Grenze ungeprüft

77 · Kritik · von Architekt (Technik) → Regelumsetzer · Runde 1/3 · offen

## Runde 1
Gegenstand: P7 in e15c5d2, `pyproject.toml` und `prozess/pruefungen/komplexitaetTest.py`.
Geprüft und in Ordnung: complexipy 8.0.1 liest `[tool.complexipy]` aus dem `pyproject.toml`
im Arbeitsordner; im Wegwerf-Versuch ist eine Funktion mit 15 grün und eine mit 16 rot;
ruff meldet `max_branches = 12`; der Code liegt bei höchstens 14 (`selbstDefinierteNamen`).

**Befund.**
1. `complexipy` steht ohne Version in `dependency-groups`, `ruff` daneben mit `==0.16.*` und
   der Begründung „damit ein Update nicht still neue Regeln bringt“. Für complexipy gilt das
   stärker: PyPI führt acht Hauptversionen (0.2 bis 8.0); eine neue kann anders zählen oder
   den Schlüssel `max-complexity-allowed` umbenennen. Ein unbekannter Schlüssel fiele nicht
   auf, denn der Standardwert ist ebenfalls 15.
2. Die Scheiter-Tests prüfen nicht die Schwellen, die `prozess/regeln.md` nennt. Die Probe für
   complexipy liegt bei 36, die für ruff bei 13 Fällen. Beispiel: Setzt jemand
   `max-complexity-allowed = 30`, bleibt `komplexitaetTest.py` grün, und
   `testDerCodeLiegtUnterDerKomplexitätsschwelle` prüft dann gegen 30. Der ruff-Test wählt
   `PLR0912` per `--select` selbst; fällt die Regel aus `select` im `pyproject.toml`, bleibt
   er grün. Der Eintrag „Schwelle 15 … | `komplexitaetTest.py`“ verspricht mehr, als der
   Test hält.

**Kosten.** Gering heute, steigend: Die Schwelle ist die einzige Sperre gegen verschachtelten
Code (Anliegen 31, Kritik des Entwicklers), und SonarLint, die Sicht des Stakeholders, misst
mit 15. Wandert die Agentensperre still nach oben, sieht der Stakeholder Meldungen, die die
Agenten nicht sehen (`prozess/ablauf.md`, Werkzeuge: „mindestens so streng wie SonarLint“).

**Gegenvorschlag.**
1. `"complexipy==8.0.*"` mit derselben Begründung wie bei ruff.
2. Grenzproben statt einer weit entfernten Probe, je ein Paar:
   - complexipy: eine Funktion mit Komplexität 15 grün, eine mit 16 rot. Zum Bauen: zwei
     verschachtelte `for`/`if`-Paare (1+2+3+4 = 10) plus `if c and d` (2) ergeben 12, jedes
     weitere `if` auf oberster Ebene +1.
   - ruff: 12 Fälle grün, 13 rot, mit der Auswahl aus `pyproject.toml` statt `--select`.

Erledigt, wenn: Ein Wert über 15 bzw. 12 im `pyproject.toml` oder ein Entfernen von
`PLR0912` aus `select` macht `komplexitaetTest.py` rot.

**Stellungnahme.**
