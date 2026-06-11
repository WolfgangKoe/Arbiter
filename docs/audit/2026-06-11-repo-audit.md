# Arbiter — Repo-Audit

- **Datum:** 2026-06-11
- **Commit:** `c5bc891`
- **Effort:** standard (`/improve`, ganzes Repo)
- **Methode:** 4 parallele Read-only-Audit-Pässe (Korrektheit/Performance, Security/Input, Tech-Debt/DX, Tests/Docs/Direction), anschließend jede Stelle vom Auditor selbst im Code verifiziert.

## Baseline

594 Tests grün (33,8 s, `pytest`). Aber: CI führt **nur** `pytest tests/` aus — kein Lint, kein `mypy`, keine Coverage. `pytest-cov` ist nicht installiert; die in CLAUDE.md versprochene „80 %-Schwelle" existiert nicht. Dieser fehlende Verifikations-Unterbau rangiert deshalb als Finding #1 und sollte vor riskanteren Folge-Änderungen geschlossen werden.

## Findings (nach Leverage = Impact ÷ Aufwand, gewichtet mit Confidence)

| # | Finding | Kategorie | Impact | Aufwand | Risiko | Confidence |
|---|---------|-----------|--------|---------|--------|------------|
| 1 | CI ohne Lint/Type/Coverage-Gates; `pytest-cov` fehlt; „80 %"-Gate fiktiv | dx/tests | Fehler & Typbrüche landen ungehindert auf `main`; Doku lügt | S–M | LOW | HIGH |
| 2 | `.rosz`-Upload mit stdlib `ElementTree` → Billion-Laughs-DoS | security | Manipulierte Datei crasht den HF-Space-Prozess | S | LOW | HIGH |
| 3 | Fraktions-Logik fest in `src/` (verletzt Projekt-Regel #1) | tech-debt | 4. Fraktion zwingt zum Aufspüren versteckter Checks; DRY-Bruch | S (scoped) / L (voll) | MED | HIGH |
| 4 | `lookup()` ohne `next(...)`-Default → `StopIteration`-Crash | bug | Generischer Streamlit-Fehler statt Fallback | S | LOW | HIGH |
| 5 | Loader parst YAML bei jedem Streamlit-Rerun neu (ungecacht) | perf | Wiederholtes Disk-I/O + Parse pro Interaktion | S | LOW | HIGH |
| 6 | 18 ungeschützte `yaml.safe_load` → kaputte YAML crasht App | bug | Kein graceful degradation bei korrupter Daten-YAML | M | LOW | HIGH |
| 7 | Scenario-Query-Param ohne Validierung → Pfad-Traversal | security | Defense-in-Depth; cheap fix | S | LOW | HIGH |
| 8 | Zwei parallele CI/Deploy-Pipelines (Woodpecker + GH Actions) | dx | Doppel-Deploy / stille Divergenz | S | MED | HIGH |
| 9 | `Makefile` referenziert nicht-existentes `src/adapters/...` + `./tailwindcss` | dx | `make css` schlägt fehl; Onboarding-Verwirrung | S | LOW | HIGH |
| 10 | `.env.example` listet `FLASK_*` in reiner Streamlit-App | dx | Irreführende Setup-Doku | S | LOW | HIGH |
| 11 | `_common.py` ist 2077-LOC-Gott-Modul | tech-debt | Jede Attack-Änderung fasst die Datei an; schwer testbar | L | MED | HIGH |

---

## Detail je Finding

### #1 — CI hat keine Verifikations-Gates; Coverage-Gate ist fiktiv
- **Evidence:** [.woodpecker.yml:5](../../.woodpecker.yml) und [.github/workflows/deploy.yml:24](../../.github/workflows/deploy.yml) führen nur `pytest tests/ -v` aus. [pyproject.toml:1-21](../../pyproject.toml) konfiguriert `black`, `isort`, `ruff`, `mypy --strict` — keiner läuft in CI. [CLAUDE.md:94](../../CLAUDE.md) behauptet „Coverage-Schwelle: 80 % — darunter wird der Build rot". `pytest-cov` ist in keiner requirements-Datei.
- **Impact:** Typfehler, Lint-Verstöße und Coverage-Lücken landen still auf `main`. Die dokumentierte 80 %-Schwelle ist nicht gemessen und nicht erzwungen — falsche Sicherheit.
- **Fix-Skizze:** `pytest-cov` zu `requirements-dev.txt`; CI-Schritte für `ruff check`, `black --check`, `mypy`, `pytest --cov=src --cov-fail-under=<realistisch>`. Streamlit-UI (`src/uiLayout/`) von der Coverage-Schwelle ausnehmen (laut CLAUDE.md nicht automatisch testbar). Schwelle erst messen, dann setzen — ggf. CLAUDE.md auf den realen Wert korrigieren.

### #2 — `.rosz`-XML-Parsing anfällig für Billion-Laughs-DoS
- **Evidence:** [rosz_importer.py:10](../../src/gameObjects/rosz_importer.py) `import xml.etree.ElementTree as ET`; [rosz_importer.py:148](../../src/gameObjects/rosz_importer.py) `ET.fromstring(data)` auf hochgeladenem `.rosz`-Inhalt (via `st.file_uploader` in [setupScreen.py](../../src/uiLayout/setupScreen.py)). Stdlib-`ElementTree` ist laut Python-Doku gegen Entity-Expansion („billion laughs"/quadratic blowup) verwundbar; das 5-MB-Limit ([rosz_importer.py:19](../../src/gameObjects/rosz_importer.py)) verhindert das nicht.
- **Impact:** Eine präparierte Roster-Datei kann beim Parsen Speicher/CPU erschöpfen und den öffentlich deployten Space-Prozess crashen (DoS). Kein Code-Exec, keine Exfiltration.
- **Fix-Skizze:** `defusedxml` zu `requirements.txt`; `ET.fromstring` durch `defusedxml.ElementTree.fromstring` ersetzen (nur die Parse-Stelle, Element-API bleibt gleich).

### #3 — Fraktions-spezifische Logik in `src/` (verletzt „Generic src/"-Regel)
- **Evidence:**
  - WAAAGH-Ork-Keyword-Check, **wortgleich an 3 Stellen** dupliziert: [_common.py:1443](../../src/uiLayout/_common.py), [_common.py:1554](../../src/uiLayout/_common.py), [_common.py:1789](../../src/uiLayout/_common.py) — jeweils `waaagh_bonus = 1 if (waaagh and atk_unit.has_keyword("ORK")) else 0`.
  - Vierte Kopie der Keyword-Logik + hartcodierter Text: [chargephase.py:87](../../src/gameMechanic/chargephase.py), [chargephase.py:93](../../src/gameMechanic/chargephase.py).
  - Necron-Gate: [_common.py:935](../../src/uiLayout/_common.py) `if not fdir.startswith("necron"): return` im Reanimation-Protocols-Block.
  - Geringer: hartcodiertes `"Overlord"`-Log-Label [commandPhase.py:197](../../src/gameMechanic/commandPhase.py).
- **Impact:** CLAUDE.md-Kernprinzip („keine Fraktions-Logik in `src/`") verletzt. Eine 4. Fraktion erzwingt das Aufspüren und Duplizieren dieser versteckten Checks. Der 3× duplizierte WAAAGH-Bonus driftet, wenn nur eine Stelle geändert wird.
- **Fix-Skizze (scoped, S–M):** WAAAGH-Bonus in **einen** Helper extrahieren (z. B. `ability_engine.py`), der den Bonus aus den Fähigkeitsdaten ableitet statt aus `has_keyword("ORK")`; alle 4 Call-Sites darauf umstellen. RP-Gate von `fdir.startswith("necron")` auf eine Abfrage „hat diese Einheit gerade eine aktive Reanimate-Fähigkeit?" umstellen. Voller datengetriebener Umbau des Attack-Modifier-Pfads ist L/MED-Risiko und sollte separat geplant werden.
- **Hinweis:** Defaults wie `roster_p1="necrons_alpha.yaml"` ([game_state.py:216](../../src/gameMechanic/game_state.py)) oder `first_player`-Fallback `"Necrons"` ([gameHeader.py:249](../../src/uiLayout/gameHeader.py)) sind Default-Werte, keine Verzweigungslogik — niedrigere Priorität.

### #4 — `lookup()` ohne Default → `StopIteration`
- **Evidence:** [_common.py:169](../../src/uiLayout/_common.py) `unit = next(u for u in units if u.id == unit_id)` ohne Default. Aufgerufen aus vielen Render- und Phasen-Pfaden.
- **Impact:** Divergiert Session-State von geladenem Unit-Katalog (z. B. Roster mitten im Spiel neu geladen), crasht der Generator-`next` mit `StopIteration` als generischer Streamlit-Fehler.
- **Fix-Skizze:** `next((u for u in units if u.id == unit_id), None)` + sauberer Früh-Return/Fehlermeldung bei `None`. Regressionstest mit absichtlich divergentem State.

### #5 — Loader parst YAML bei jedem Rerun neu
- **Evidence:** [loader.py:432](../../src/gameObjects/loader.py) `load_round_choice_abilities` öffnet+parst `faction_abilities.yaml` bei jedem Aufruf; 6 Call-Sites, davon mehrere in Render-Pfaden: [_common.py:365](../../src/uiLayout/_common.py), [armyCard.py:221](../../src/uiLayout/armyCard.py), [gameActionsArea.py:94](../../src/uiLayout/gameActionsArea.py), [ability_engine.py:83](../../src/gameMechanic/ability_engine.py). Streamlit führt das Skript bei jeder Interaktion komplett neu aus → vielfaches Re-Parsing pro Rerun. Weitere Loader-Funktionen haben dasselbe Muster.
- **Impact:** Wiederholtes Disk-I/O und YAML-Parsing pro Interaktion. Dateien sind klein, daher moderat — aber durchgängig und gratis vermeidbar.
- **Fix-Skizze:** `@st.cache_data` auf die Loader-Funktionen (Key = `faction_dir`), oder modul-weiter Cache-Dict. Daten ändern sich nur bei Spielinitialisierung.

### #6 — Ungeschützte `yaml.safe_load`-Aufrufe
- **Evidence:** [loader.py](../../src/gameObjects/loader.py) — 18 `yaml.safe_load(f)`-Aufrufe ohne `try/except`. Eine syntaktisch kaputte/abgeschnittene YAML wirft `YAMLError` als roher Stacktrace in der Streamlit-UI.
- **Impact:** Kein graceful degradation; App unbrauchbar bis die Datei repariert ist. Betrifft v. a. importierte Roster-YAML.
- **Fix-Skizze:** Zentraler Helper `_safe_yaml_load(path, default)` mit `try/except YAMLError`, Logging und Default-Rückgabe; alle Loader darauf umstellen.

### #7 — Scenario-Query-Param ohne Validierung (Pfad-Traversal)
- **Evidence:** [app.py:24](../../src/app.py) `_scenario = st.query_params.get("scenario")` → `load_scenario(_scenario)`. [scenarios.py:16](../../src/gameMechanic/scenarios.py) `path = _SCENARIOS_DIR / f"{name}.json"` ohne Sanitisierung; auch `save_scenario` ([scenarios.py:105](../../src/gameMechanic/scenarios.py)) schreibt mit unvalidiertem Namen.
- **Impact:** Defense-in-Depth: Über `?scenario=../...` kann auf bestehende `.json`-Dateien außerhalb `data/scenarios/` gezeigt werden. Der Inhalt wird dem Angreifer **nicht** zurückgegeben und die Datei muss serverseitig existieren — daher begrenzt, aber unsauber für einen öffentlichen Space.
- **Fix-Skizze:** Name gegen Allowlist-Regex (`^[a-z0-9_-]+$`) prüfen, oder `path.resolve().relative_to(_SCENARIOS_DIR.resolve())` erzwingen.

### #8 — Zwei parallele CI/Deploy-Pipelines
- **Evidence:** [.woodpecker.yml](../../.woodpecker.yml) (Codeberg) und [.github/workflows/deploy.yml](../../.github/workflows/deploy.yml) deployen beide per `rsync` in den geklonten HF-Space, beide auf `dev`+`main`.
- **Impact:** Doppel-Deploy bzw. stille Divergenz, wenn nur eine Pipeline gepflegt wird.
- **Fix-Skizze:** Eine als Single Source of Truth festlegen, die andere deaktivieren/entfernen — oder, falls beide bewusst, den Grund dokumentieren und Trigger entkoppeln.

### #9 — `Makefile` referenziert nicht-existente Pfade
- **Evidence:** [Makefile:4-7](../../Makefile) verweist auf `./tailwindcss` und `src/adapters/web/static/input.css` — beides existiert nicht (App ist reines Streamlit, kein Flask+Tailwind).
- **Impact:** `make css`/`make css-watch` schlagen fehl; verwirrt Onboarding.
- **Fix-Skizze:** Tote Targets entfernen oder durch sinnvolle ersetzen (`run`, `test`, `lint`).

### #10 — `.env.example` mit Flask-Geistern
- **Evidence:** [.env.example](../../.env.example) listet `FLASK_ENV`, `FLASK_SECRET_KEY` — nie gelesen in der Streamlit-App.
- **Impact:** Irreführende Setup-Doku.
- **Fix-Skizze:** Auf real genutzte Variablen reduzieren (`DATA_DIR`, ggf. HF-Tokens) mit Kommentaren.

### #11 — `_common.py` ist ein Gott-Modul
- **Evidence:** [_common.py](../../src/uiLayout/_common.py) — 2077 LOC, mischt Dice-HTML-Generierung, Attack-Declaration-State-Machine, Damage-Resolution, fraktionsspezifische RP-/WAAAGH-UI und State-Lookup.
- **Impact:** Jede Attack-Flow-Änderung fasst die Datei an; UI und Logik verschränkt, schwer testbar; hohes Seiteneffekt-Risiko.
- **Fix-Skizze:** In fokussierte Module aufteilen (z. B. `dice_ui.py`, `attack_flow.py`, `faction_abilities_ui.py`); Circular-Import-Konvention (Handler importieren nur aus dem Common-Facade) erhalten. **Voraussetzung: Coverage aus #1**, sonst Refactor ohne Netz.

---

## Geprüft & verworfen (nicht erneut auditieren)

- **`weapon_max == 0`-„Crash"** ([_common.py:1836](../../src/uiLayout/_common.py)): `st.number_input(min_value=0, max_value=0)` crasht nicht — Streamlit sperrt auf 0. Eine `1_per_10`-Waffe in <10-Modell-Einheit zeigt Max 0, was regelkonform ist. Kein Bug.
- **Zip-Member-Pfad-Traversal** ([rosz_importer.py:163](../../src/gameObjects/rosz_importer.py)): nur In-Memory-`zf.read(...)`, kein `extractall`/Schreiben — kein realer Traversal-Pfad.
- **Scraper-`--out-dir`** (`tools/wahapedia_*`): reines lokales Dev-CLI, nicht web-exponiert.
- **`yaml.load`-Missbrauch:** überall korrekt `safe_load`; keine Maßnahme nötig.

## Direction (Optionen für den Maintainer, keine Bugs)

- **Fraktions-Bootstrap-Doku + 4. Fraktion.** Die Datenebene ist erwiesen data-driven (3 Fraktionen, `faction_abilities.yaml` mit generischen `effect_type`s). Neue Fraktion = reine YAML-Arbeit — **wenn** zuerst Finding #3 (die letzten Logik-Leaks) geschlossen ist. Confidence: HIGH.
- **Coverage-Messung als Fundament.** Ohne Messung sind die großen Tech-Debt-Posten (#11) nicht sicher angehbar. Hängt an #1. Confidence: HIGH.

## Abhängigkeits-Reihenfolge

1. **#1 (Verifikations-Gates) zuerst** — schützt jede riskantere Folge-Änderung (#3, #6, #11).
2. **#3 vor der 4. Fraktion** — sonst werden Leaks dupliziert statt entfernt.
3. **#11 (God-Modul-Split) erst nach Coverage aus #1** — sonst Refactor ohne Netz.
