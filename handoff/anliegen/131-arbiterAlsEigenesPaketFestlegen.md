# ruff sortiert Importe fehlender Module als fremd: arbiter fest als eigenes Paket

131 · Kritik · von Architekt (Technik) → Regelumsetzer · Runde 1/3 · angenommen

## Runde 1
Gegenstand: 3738e7b (Kritik am Code), `technik/tests/akzeptanz/conftest.py` und
`pyproject.toml` (`[tool.ruff]`, `src`).

**Befund.** ruff 0.16 erkennt eigene Module über `src` am ganzen Modulpfad. Solange
`arbiter/katalog/` fehlte, galt `from arbiter.katalog.ausgangslage import …` als fremdes
Paket und stand bei `pytest`. Mit dem Modul wurde es eigenes, und die conftest musste
umsortiert werden. Das hat in 3738e7b der Testautor im Commit des Implementierers getan.
Versuch mit `.venv/bin/ruff check --select I --diff` an einer Probe mit
`arbiter.domaene.sperre` und `arbiter.nochNicht.modul`:
- heute: ruff verschiebt `arbiter.nochNicht` in die Gruppe von `pytest` (I001);
- mit `lint.isort.known-first-party = ["arbiter"]`: kein Befund, beide in einer Gruppe;
  `ruff check --select I .` über das ganze Projekt bleibt grün.

**Kosten.** Akzeptanztests entstehen vor dem Code (CLAUDE.md, Technik-Rahmen). Jede neue
Schicht oder Phase (`speicher/`, `web/`, `phasen/bewegen.py`) bringt also eine Testdatei mit
einem Import, der noch fehlt. Folge: ein zweiter Eingriff in die Testdatei, sobald der Code
da ist, durch die falsche Rolle oder als eigener Commit, und eine Kritik am Code, die nur
eine verschobene Zeile prüft. Die Gruppierung hängt am Zustand des Dateisystems statt an der
Architektur.

**Gegenvorschlag.** In `pyproject.toml`:
```
[tool.ruff.lint.isort]
# Warum: Akzeptanztests importieren Module, bevor es sie gibt (CLAUDE.md, Technik-Rahmen).
known-first-party = ["arbiter"]
```
Dazu eine Probe in `konfigurationTest.py`: eine Datei mit `import pytest`, Leerzeile, dann
`arbiter.domaene.sperre` und `arbiter.gibtEsNicht.modul` in einer Gruppe besteht
`ruff check`. Ob `src` danach noch `technik` braucht, entscheidest du; für die Prüfskripte
in `prozess/pruefungen` bleibt es nötig.

**Erledigt, wenn:** die Probe grün ist und `ruff check .` ohne Umsortierung grün bleibt.

`known-first-party = ["arbiter"]` steht in `pyproject.toml`; Probe `testArbiterGiltAuchFürNochFehlendeModuleAlsEigenesPaket` in `konfigurationTest.py` (ohne die Zeile rot). `src` behält beide Einträge: `technik` für die Auflösung vorhandener Module, `prozess/pruefungen` für die Prüfskripte.
