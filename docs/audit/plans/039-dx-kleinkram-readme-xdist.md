# Plan 039: DX-Kleinkram — README-Setup vervollständigen, tote `DATA_DIR` entfernen, pytest-xdist einführen

> **Executor instructions**: Schritt für Schritt folgen, jede Verifikation
> ausführen. Bei STOP-Bedingung: stoppen und berichten. Am Ende Status-Zeile in
> `docs/audit/plans/README.md` aktualisieren.
>
> **Drift check (zuerst ausführen)**:
> `git diff --stat f6c464a..HEAD -- README.md .env.example requirements-dev.txt .github/workflows/deploy.yml`
> Bei Änderungen: Exzerpte gegen Live-Code prüfen; Abweichung → STOP.

## Status

- **Priority**: P3
- **Effort**: S
- **Risk**: LOW
- **Depends on**: none
- **Category**: dx
- **Planned at**: commit `f6c464a`, 2026-07-05

## Why this matters

Drei kleine, unabhängige Reibungspunkte: (1) Das README (14 Zeilen) reicht nicht,
um einen frischen Clone lauffähig zu machen (kein venv, kein Dependency-Install,
kein `pre-commit install`, kein Port, kein Testkommando) — die echten Schritte
stehen nur intern in `.claude/tasks/next_session.md`. (2) `.env.example` enthält
ausschließlich `DATA_DIR=data`, das nirgendwo in `src/` oder `tools/` gelesen
wird — tote Doku, die Suchende in die Irre führt. (3) Die 1445-Test-Suite läuft
~64 s single-threaded; das Repo-Workflow verlangt die Vollsuite vor jedem Commit,
also wird diese Minute viele Male pro Session bezahlt — `pytest-xdist` halbiert
das mindestens.

## Current state

`README.md` (vollständig, 14 Zeilen): HF-Spaces-Frontmatter + Titel + 2 Sätze +
`Start: streamlit run src/app.py`. Kein Setup.

`.env.example` (vollständig): `DATA_DIR=data`.
Beleg tot: `grep -rn "DATA_DIR" src/ tools/` → 0 Treffer.

`requirements-dev.txt`: `-r requirements.txt`, black, isort, ruff, mypy,
pre-commit, pytest, pytest-cov — kein pytest-xdist.

`pyproject.toml:23-25`: `addopts = "--cov=src --cov-report=term-missing"`
(bleibt unverändert — kein `-n auto` als Default, sonst zahlt jeder
Einzeltest-Aufruf den xdist-Startup).

Interner Setup-Stand (Quelle für README-Inhalte):
`.claude/tasks/next_session.md` nennt `source .venv/bin/activate`, Port 8501.
Messbefehl laut CLAUDE.md: `pytest --tb=short`. Pre-commit-Hooks existieren
(`.pre-commit-config.yaml`: black, isort, ruff).

## Commands you will need

| Purpose | Command | Expected on success |
|---|---|---|
| Vollsuite (Referenzzeit) | `time pytest --tb=short` | exit 0; Zeit notieren |
| Parallel | `time pytest -n auto --tb=short` | exit 0; deutlich schneller |
| Toter-Var-Check | `grep -rn "DATA_DIR" src/ tools/ docs/ README.md` | 0 Treffer nach Step 2 |
| Lint | `ruff check src/ && black --check src/ && isort --check-only src/` | exit 0 |

## Scope

**In scope:**
- `README.md` (Setup-Abschnitt)
- `.env.example` (löschen)
- `requirements-dev.txt` (+ pytest-xdist)
- `.github/workflows/deploy.yml` (Test-Step parallelisieren)

**Out of scope:**
- `pyproject.toml` `addopts` — Default bleibt seriell (Begründung oben).
- CLAUDE.md, LEITSTAND.md, next_session.md — interne Doku nicht anfassen.
- mypy/pip-audit-CI-Steps — Pläne 037/038.

## Git workflow

- Branch: `chore/039-dx-cleanup`
- Commits z. B. `Complete README setup instructions`, `Remove dead .env.example`,
  `Add pytest-xdist and parallelize CI test run`
- Nicht pushen ohne Anweisung.

## Steps

### Step 1: README-Setup-Abschnitt

Nach dem bestehenden Intro (HF-Frontmatter unangetastet lassen — sie steuert
das Spaces-Deployment!) den Start-Abschnitt ersetzen durch:

```markdown
## Setup

​```bash
python3.12 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt -r requirements-dev.txt
pre-commit install
​```

## Start

​```bash
streamlit run src/app.py   # http://localhost:8501
​```

## Tests

​```bash
pytest --tb=short          # Vollsuite + Coverage-Gate (99 %)
pytest -n auto --tb=short  # dasselbe, parallel (schneller)
​```
```

(Die Zeichen `​` oben sind nur Template-Escaping dieses Plans — im README
normale Backtick-Fences schreiben.)

**Verify**: README rendert korrekt (`head -40 README.md`), Frontmatter-Block
(`---`-Zeilen 1–5) unverändert.

### Step 2: `.env.example` löschen

Vorher absichern: `grep -rn "env.example\|DATA_DIR" src/ tools/ docs/ .github/ README.md`
→ Treffer nur in Alt-Audit-Dokumenten (`docs/audit/2026-06-11-*`) sind ok
(historische Berichte, nicht anfassen). Andere Treffer → STOP.
Dann `git rm .env.example`.

**Verify**: `ls .env.example` → „No such file"; grep wie oben → keine
funktionalen Referenzen.

### Step 3: pytest-xdist

1. `pytest-xdist` in `requirements-dev.txt` ergänzen, installieren.
2. `time pytest -n auto --tb=short` ausführen.
   - Alle grün → weiter.
   - **Failures, die seriell nicht auftreten** → STOP: Das sind echte
     Test-Isolationsbugs (CLAUDE.md verspricht vollständige Isolation) —
     auflisten und berichten, NICHT als Flakiness abtun und nicht selbst fixen.
3. In `deploy.yml` den Test-Step auf `pytest -n auto --tb=short` umstellen.

**Verify**: `time pytest -n auto --tb=short` → exit 0, Coverage ≥ 99 %
(pytest-cov kombiniert xdist-Worker automatisch), Laufzeit im Bericht nennen
(vorher/nachher).

### Step 4: Vollsuite seriell als Gegenprobe + Lint

**Verify**: `pytest --tb=short` → exit 0 (seriell muss weiter funktionieren);
Lint-Dreier → exit 0.

## Test plan

Keine neuen Unit-Tests. Das Risiko dieses Plans sitzt in Step 3.2 — der
Parallel-Lauf selbst ist der Test (deckt Ordnungs-/Isolationsannahmen der
gesamten Suite auf).

## Done criteria

- [ ] README enthält Setup/Start/Tests-Abschnitte; HF-Frontmatter unverändert
- [ ] `.env.example` gelöscht, keine funktionalen Referenzen
- [ ] `pytest -n auto --tb=short` exit 0, Coverage ≥ 99 %; CI nutzt `-n auto`
- [ ] `pytest --tb=short` (seriell) weiterhin exit 0
- [ ] `git status`: nur In-Scope-Dateien geändert
- [ ] Status-Zeile in `docs/audit/plans/README.md` aktualisiert (inkl.
      Laufzeit vorher/nachher)

## STOP conditions

- Parallel-Lauf zeigt Failures, die seriell grün sind (Isolationsbugs — echte
  Befunde, Stakeholder-Entscheid über Fix-Reihenfolge).
- Coverage-Kombination unter xdist liefert eine abweichende Prozentzahl und
  reißt das 99-%-Gate → berichten (dann CI seriell lassen, xdist nur als
  lokale Option dokumentieren).
- `DATA_DIR`/`.env.example` hat doch einen funktionalen Verweis außerhalb der
  Alt-Audits.

## Maintenance notes

- Wächst die Suite weiter, bleibt `-n auto` der Hebel; erst bei >3–4 min über
  Test-Sharding im CI nachdenken.
- README bewusst minimal gehalten (Repo-Doku-Prinzip: eine Tür, LEITSTAND.md
  verlinkt den Rest) — kein Feature-Katalog ins README ziehen.
