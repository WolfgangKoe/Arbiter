# Plan 001: CI führt Lint- und Coverage-Gates aus (nicht nur `pytest`)

> **Executor instructions**: Follow this plan step by step. Run every
> verification command and confirm the expected result before moving to the
> next step. If anything in the "STOP conditions" section occurs, stop and
> report — do not improvise. When done, update the status row for this plan
> in `docs/audit/plans/README.md`.
>
> **Drift check (run first)**:
> `git diff --stat c5bc891..HEAD -- .woodpecker.yml .github/workflows/deploy.yml pyproject.toml requirements-dev.txt CLAUDE.md`
> If any of these changed since this plan was written, compare the "Current state"
> excerpts against the live files before proceeding; on a mismatch, treat it as a
> STOP condition.

## Status

- **Priority**: P1
- **Effort**: M
- **Risk**: LOW
- **Depends on**: none
- **Category**: dx / tests
- **Planned at**: commit `c5bc891`, 2026-06-11

## Why this matters

Beide CI-Pipelines führen heute ausschließlich `pytest tests/` aus. `pyproject.toml`
konfiguriert `ruff`, `black`, `isort` und `mypy --strict`, doch keines davon läuft in
CI. `CLAUDE.md` behauptet eine erzwungene 80 %-Coverage-Schwelle, aber `pytest-cov`
ist nicht installiert und keine Pipeline misst Coverage. Folge: Lint-Verstöße,
Formatierungs-Drift und Coverage-Lücken landen unbemerkt auf `main`, und die
dokumentierte Schwelle ist eine Fiktion. Dieser Plan macht aus den vorhandenen,
aber ungenutzten Tools echte Gates — und korrigiert die Doku auf die Realität.

## Current state

Verifizierter Ausgangszustand (read-only zum Planungszeitpunkt gemessen):

- `ruff check src/` → **passt heute** (All checks passed).
- `black --check src/` → **passt heute** (38 files unchanged).
- `isort --check-only src/` → **passt heute** (keine Ausgabe, exit 0).
- `mypy src/` → **127 Fehler in 22 Dateien**. ⚠️ `mypy` darf deshalb **nicht**
  blockierend werden, sonst ist die Pipeline sofort rot. Dieser Plan baut `mypy`
  nur als **informativen, nicht-blockierenden** Schritt ein.
- `pytest-cov` ist in **keiner** requirements-Datei installiert; Coverage-Zahl unbekannt.

Relevante Dateien:

- `.woodpecker.yml` — Codeberg-CI. Aktueller Test-Schritt:
  ```yaml
  steps:
    - name: test
      image: python:3.12-slim
      commands:
        - pip install --quiet -r requirements.txt pytest
        - pytest tests/ -v --tb=short
  ```
- `.github/workflows/deploy.yml` — GitHub-Actions-CI. Aktueller Test-Job:
  ```yaml
  jobs:
    test:
      runs-on: ubuntu-latest
      steps:
        - name: Checkout repository
          uses: actions/checkout@v4
        - name: Set up Python
          uses: actions/setup-python@v5
          with:
            python-version: "3.12"
        - name: Install dependencies
          run: pip install -r requirements.txt pytest
        - name: Run tests
          run: pytest tests/ -v --tb=short
  ```
- `requirements-dev.txt` — Dev-Tools, derzeit:
  ```
  -r requirements.txt
  black
  isort
  ruff
  mypy
  pre-commit
  pytest
  ```
  Hinweis: CI installiert `requirements.txt` + `pytest` (NICHT `requirements-dev.txt`),
  installiert also weder ruff/black/isort/mypy noch pytest-cov. Du musst die für CI
  nötigen Tools im CI-Install-Schritt mit installieren.
- `CLAUDE.md` — Zeile mit `Coverage-Schwelle: **80 %** — darunter wird der Build rot`
  (Abschnitt „## Testing").

Konventionen: YAML-Indentierung 2 Spaces. Befehle in CI als Liste unter `commands:`
(Woodpecker) bzw. einzelne `- name:`/`run:`-Steps (GitHub Actions).

## Commands you will need

| Zweck      | Befehl                                   | Erwartet bei Erfolg |
|------------|------------------------------------------|---------------------|
| venv       | `source .venv/bin/activate`              | Prompt zeigt `(.venv)` |
| Lint       | `ruff check src/`                        | `All checks passed!` |
| Format     | `black --check src/`                     | exit 0, „would be left unchanged" |
| Imports    | `isort --check-only src/`                | exit 0, keine Ausgabe |
| Typen      | `mypy src/`                              | (derzeit 127 Fehler — NUR informativ) |
| Coverage   | `pytest tests/ --cov=src --cov-report=term-missing` | Tests grün + Coverage-Tabelle |
| Tests      | `python -m pytest tests/ -q`             | alle grün (594 zum Planungszeitpunkt) |

## Scope

**In scope** (nur diese Dateien ändern):
- `requirements-dev.txt` — `pytest-cov` ergänzen
- `.woodpecker.yml` — Lint-/Coverage-/mypy-Schritte ergänzen
- `.github/workflows/deploy.yml` — dieselben Schritte ergänzen
- `pyproject.toml` — optionaler `[tool.coverage.run]`-Block (Streamlit-UI ausschließen)
- `CLAUDE.md` — Coverage-Zeile auf den real gemessenen Wert korrigieren

**Out of scope** (NICHT anfassen, auch wenn verwandt):
- Jeglicher `src/`-Code — dieser Plan ändert keine Anwendungslogik.
- Die `deploy`-Schritte/Logik beider Pipelines — nur die Test-Jobs ergänzen.
- Die 127 `mypy`-Fehler beheben — separater Aufwand; hier bleibt `mypy` nicht-blockierend.

## Git workflow

- Branch: `advisor/001-ci-verification-gates` (Repo arbeitet auf `dev`; `main` nur per PR).
- Commit-Stil: kurz, imperativ, Englisch — wie im Repo-Log (`Add shooting phase UI`).
  Beispiel hier: `Add lint and coverage gates to CI`.
- NICHT pushen oder PR öffnen, außer der Operator weist es an.

## Steps

### Step 1: `pytest-cov` zu Dev-Dependencies hinzufügen

Ergänze in `requirements-dev.txt` eine Zeile `pytest-cov` (nach `pytest`).

**Verify**: `grep -n pytest-cov requirements-dev.txt` → eine Trefferzeile.

### Step 2: Coverage lokal messen und realistische Schwelle bestimmen

Installiere im venv `pytest-cov` (nur lokal, nicht committen außer requirements):
`pip install pytest-cov` — dann messen:

`pytest tests/ --cov=src --cov-report=term-missing`

Lies den `TOTAL`-Prozentwert am Tabellenende ab. Setze die CI-Schwelle auf den
**abgerundeten gemessenen Wert minus 2 Punkte** als Sicherheitspuffer (z. B. gemessen
73 % → Schwelle `--cov-fail-under=70`). **Setze NICHT 80 %**, solange nicht gemessen
≥ 82 %. Notiere den gemessenen Wert; du brauchst ihn in Step 4 und 6.

**Verify**: Der Befehl endet mit einer `TOTAL`-Zeile und einem Prozentwert.

### Step 3: Optionalen Coverage-Konfig-Block in `pyproject.toml`

Füge ans Ende von `pyproject.toml` an (Streamlit-UI ist laut CLAUDE.md nicht
automatisch testbar und soll die Schwelle nicht verfälschen):

```toml
[tool.coverage.run]
omit = ["src/uiLayout/*", "src/app.py"]
```

Miss danach erneut `pytest tests/ --cov=src --cov-report=term-missing` — der TOTAL-Wert
steigt typischerweise. Verwende **diesen** Wert (mit der `omit`-Liste) für die Schwelle
in Step 4.

**Verify**: `pytest tests/ --cov=src` läuft ohne Fehler; TOTAL-Zeile erscheint.

### Step 4: Woodpecker-Pipeline erweitern

Ersetze in `.woodpecker.yml` den `test`-Schritt so, dass er Lint, Tests-mit-Coverage
und (informatives) mypy ausführt. `<N>` ist der in Step 3 bestimmte Schwellwert:

```yaml
  - name: test
    image: python:3.12-slim
    commands:
      - pip install --quiet -r requirements-dev.txt pytest-cov
      - ruff check src/
      - black --check src/
      - isort --check-only src/
      - mypy src/ || true   # informativ — 127 Bestandsfehler, noch nicht blockierend
      - pytest tests/ -v --tb=short --cov=src --cov-report=term-missing --cov-fail-under=<N>
```

**Verify**: `python -c "import yaml,sys; yaml.safe_load(open('.woodpecker.yml')); print('ok')"`
→ `ok` (gültiges YAML).

### Step 5: GitHub-Actions-Pipeline erweitern

Ersetze im `test`-Job von `.github/workflows/deploy.yml` den Install- und
Run-Tests-Schritt durch (gleicher `<N>` wie Step 4):

```yaml
      - name: Install dependencies
        run: pip install -r requirements-dev.txt pytest-cov
      - name: Lint
        run: |
          ruff check src/
          black --check src/
          isort --check-only src/
      - name: Type check (informational)
        run: mypy src/
        continue-on-error: true
      - name: Run tests with coverage
        run: pytest tests/ -v --tb=short --cov=src --cov-report=term-missing --cov-fail-under=<N>
```

**Verify**: `python -c "import yaml; yaml.safe_load(open('.github/workflows/deploy.yml')); print('ok')"`
→ `ok`.

### Step 6: CLAUDE.md auf die Realität korrigieren

Ändere in `CLAUDE.md` die Coverage-Zeile so, dass sie den real erzwungenen Wert
nennt (z. B. „Coverage-Schwelle: **<N> %** (in CI erzwungen via `--cov-fail-under`);
Streamlit-UI (`src/uiLayout/`) ist ausgenommen"). Keine Zahl behaupten, die nicht
in den CI-Befehlen aus Step 4/5 steht.

**Verify**: `grep -n "cov-fail-under" .woodpecker.yml .github/workflows/deploy.yml`
zeigt denselben `<N>`, der auch in `CLAUDE.md` steht.

## Test plan

- Keine neuen Python-Tests — dieser Plan ändert nur CI-Konfig und Doku.
- Lokale Gegenprobe, dass die neuen Gates grün sind, BEVOR du committest:
  - `ruff check src/` → passt
  - `black --check src/` → passt
  - `isort --check-only src/` → passt
  - `pytest tests/ --cov=src --cov-fail-under=<N>` → grün und über Schwelle
- `mypy src/` darf Fehler zeigen — das ist erwartet und absichtlich nicht-blockierend.

## Done criteria

Maschinell prüfbar. ALLE müssen gelten:

- [ ] `grep -n pytest-cov requirements-dev.txt` → Treffer
- [ ] `grep -n "cov-fail-under" .woodpecker.yml` → Treffer
- [ ] `grep -n "cov-fail-under" .github/workflows/deploy.yml` → Treffer
- [ ] `grep -n "ruff check" .woodpecker.yml .github/workflows/deploy.yml` → Treffer in beiden
- [ ] `python -c "import yaml; yaml.safe_load(open('.woodpecker.yml')); yaml.safe_load(open('.github/workflows/deploy.yml')); print('ok')"` → `ok`
- [ ] `pytest tests/ --cov=src --cov-fail-under=<N>` lokal grün
- [ ] `CLAUDE.md` nennt denselben `<N>` wie die CI-Befehle
- [ ] Keine Dateien außerhalb der In-scope-Liste geändert (`git status`)
- [ ] Status-Zeile in `docs/audit/plans/README.md` aktualisiert

## STOP conditions

Stoppen und zurückmelden (nicht improvisieren), wenn:

- `ruff check src/`, `black --check src/` oder `isort --check-only src/` lokal
  **fehlschlagen** (zum Planungszeitpunkt passten sie — die Codebase ist gedriftet).
  Diese Gates dürfen erst aktiviert werden, wenn sie grün sind.
- Die gemessene Coverage so niedrig ist, dass selbst `<gemessen>-2` unter 50 % liegt —
  dann melde den Wert, statt eine beschämend niedrige Schwelle zu hardcoden.
- Du versucht wärst, `mypy` blockierend zu machen oder mypy-Fehler im Code zu „fixen" —
  das ist explizit out of scope.

## Maintenance notes

- **Interagiert mit Audit-Finding #8** (zwei CI-Pipelines): Solange beide existieren,
  müssen Gate-Änderungen in **beiden** Dateien gespiegelt werden. Wird auf eine Pipeline
  konsolidiert, kann die Duplizierung entfallen.
- Wenn später die 127 `mypy`-Fehler abgearbeitet sind, kann `|| true` /
  `continue-on-error: true` entfernt werden, um `mypy` blockierend zu machen.
- Reviewer sollte prüfen, dass die `omit`-Liste in `pyproject.toml` und der `<N>`-Wert
  zusammenpassen und nicht versehentlich Logik-Module (`gameMechanic/`, `gameObjects/`)
  von der Coverage ausnehmen.
