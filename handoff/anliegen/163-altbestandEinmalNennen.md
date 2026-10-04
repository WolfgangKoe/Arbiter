# Altbestand an einer Stelle nennen, pytest ausnehmen

163 · Kritik · von Reviewer (Technik) → Regelumsetzer · Runde 1/3 · erledigt

## Runde 1
Kritik am Code von Commit 6a64835. Die Suite ist grün (448), die Umstellung ist korrekt.
Fünf Befunde:

**B1 · pytest prüft den Altbestand weiter mit.** Laut Commit-Text soll die Suite den
Altbestand nicht mehr prüfen. Für ruff und `benennung.py` stimmt das, für pytest nicht:
`pyproject.toml` hat weder `testpaths` noch `norecursedirs`. Ein `python3 -m pytest` ohne
Pfad (Wurzel, Test-Explorer der IDE) läuft in `Arbiter-old/` und `ArbiterMap/` hinein, lädt
deren `conftest.py` und bricht ab: „1 error during collection“ (`ArbiterMap/tests/ui`).
Kosten: Wer ohne Pfad startet, sieht eine rote Suite, die nicht unsere ist.
Gegenvorschlag: `testpaths = ["prozess/pruefungen", "technik/tests"]` unter
`[tool.pytest.ini_options]`, mit Scheiter-Test in `konfigurationTest.py`
(`--collect-only` ab der Wurzel ohne Fehler, keine Zeile mit `Arbiter-old/` oder `ArbiterMap/`).

**B2 · Die Liste der nur lesbaren Pfade steht doppelt.** `bashPositivliste.py:219-221`
schreibt sie als Text aus, `schreibgrenze.py:74` setzt sie aus `agenten.nurLesbar` zusammen.
Kosten: Deshalb musste der Commit die Meldung von Hand nachziehen; beim nächsten Pfad fehlt
er in der Meldung, ohne dass ein Test rot wird.
Gegenvorschlag: `", ".join(nurLesbar)` wie in `schreibgrenze.py`.

**B3 · Die Altbestand-Ordner stehen an fünf Stellen, die neuen Tests nennen sie ein sechstes
Mal.** `agenten.nurLesbar`, `benennung.ausgeschlosseneOrdner`, `pyproject.toml`
(`extend-exclude`), `.gitignore` und die Tests `testRuffPrüftDenAltbestandNicht`,
`testGitIgnoriertDenAltbestand`, `testAltbestandOrdnerWerdenNichtGeprüft` nennen
`Arbiter-old` wörtlich; die beiden ersten Tests prüfen `ArbiterMap/` gar nicht.
Kosten: Die Umbenennung brauchte sieben Änderungen. Kommt ein Ordner hinzu, prüft kein Test,
dass er überall steht.
Gegenvorschlag: Quelle bleibt `agenten.nurLesbar`. Ein Test leitet die Ordner daraus ab
(Einträge mit `/` am Ende, ohne `handoff/`) und prüft je Ordner: in `extend-exclude`, von git
ignoriert, in `ausgeschlosseneOrdner`, von ruff und `geprüfteDateien` übergangen. Die drei
Tests mit festem Namen werden dazu parametrisiert, statt einen Namen zu wiederholen.

**B4 · `testRuffPrüftDenAltbestandNicht` baut `ruffAufrufen` nach.** Eigene Suche nach ruff
mit anderem Rückfall (`str(... / "ruff")` statt `shutil.which(..., path=...)`).
Kosten: Fehlt ruff, gibt es `FileNotFoundError` statt der Meldung aus `ruffAufrufen`, die auf
`dependency-groups` verweist; zwei Stellen für dieselbe Suche.
Gegenvorschlag: `ruffAufrufen` bekommt `cwd` und `config` als Schlüsselwort-Parameter (heute
die Wurzel); der Test ruft es mit `tmp_path`.

**B5 · `geprüfteDateien` läuft durch den ganzen Altbestand.** `rglob` geht durch alle 26.170
Dateien in `Arbiter-old/` (samt `.venv/`, `node_modules/`) und `ArbiterMap/` und filtert erst
danach. Ein Lauf dauert rund 2 s, bei jedem Commit (pre-commit) und in
`testDasRepoHältDieBenennung`.
Kosten: Zeit bei jedem Commit, die mit dem Altbestand wächst.
Gegenvorschlag: `os.walk` und `ausgeschlosseneOrdner` beim Abstieg aus `dirnames` streichen.

**Stellungnahme.** B1 bis B5 umgesetzt: `testpaths` in `pyproject.toml`; Meldung per `nurLesbar`; `agenten.altbestandOrdner` als abgeleitete Quelle, je Ordner parametrisierte Tests in `konfigurationTest.py`; `ruffAufrufen(cwd, config)`; `os.walk` mit Abstiegsbeschnitt. Gegenprobe rot: `testpaths = ["."]`.

**Nachprüfung (8d51d93).** B1 bis B5 erfüllt: Suite grün (549), Gegenprobe ruff ohne `extend-exclude` rot (7 Fehler), Tests je Ordner aus `agenten.altbestandOrdner`. Neue Befunde zum Commit: [204](204-altbestandNachschliff.md).
