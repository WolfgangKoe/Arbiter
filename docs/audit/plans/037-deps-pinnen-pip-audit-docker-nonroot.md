# Plan 037: Dependencies pinnen, `pip-audit` im CI, Docker non-root

> **Executor instructions**: Schritt für Schritt folgen, jede Verifikation
> ausführen. Bei STOP-Bedingung: stoppen und berichten. Am Ende Status-Zeile in
> `docs/audit/plans/README.md` aktualisieren.
>
> **Drift check (zuerst ausführen)**:
> `git diff --stat f6c464a..HEAD -- requirements.txt requirements-dev.txt Dockerfile .github/workflows/deploy.yml`
> Bei Änderungen: Exzerpte gegen Live-Code prüfen; Abweichung → STOP.

## Status

- **Priority**: P2
- **Effort**: S
- **Risk**: LOW (Pinning/CI) / MED (Docker non-root — Schreibpfade prüfen)
- **Depends on**: none
- **Category**: security / deps
- **Planned at**: commit `f6c464a`, 2026-07-05

## Why this matters

`requirements.txt` nutzt Floating-Minimums (`>=`) ohne Lockfile — jeder
CI-/Deploy-Lauf kann still neue (ggf. brechende oder verwundbare) Versionen
ziehen; Builds sind nicht reproduzierbar. Es gibt keinen automatischen
Vulnerability-Scan. Zusätzlich läuft der Container als root (kein `USER` im
Dockerfile) — unnötig großer Blast-Radius, falls je eine Lücke (z. B. im
Upload-Pfad) ausgenutzt wird.

## Current state

`requirements.txt` (vollständig):

```
streamlit>=1.57
pyyaml>=6.0
defusedxml>=0.7
```

`requirements-dev.txt`: `-r requirements.txt`, black, isort, ruff, mypy,
pre-commit, pytest, pytest-cov (alle ungepinnt).

Lokal installierte (funktionierende) Versionen laut `.venv` (vor dem Pinnen per
`pip show streamlit pyyaml defusedxml` verifizieren!): `streamlit 1.57.0`,
`PyYAML 6.0.3`, `defusedxml 0.7.1`.

`.github/workflows/deploy.yml` (test-Job, Auszug):

```yaml
      - name: Install dependencies
        run: pip install -r requirements.txt -r requirements-dev.txt
      - name: Lint
        run: |
          ruff check src/
          ...
```

`Dockerfile` (vollständig relevant): `FROM python:3.12-slim`, `WORKDIR /app`,
pip install, `COPY . .`, `EXPOSE 7860`, Streamlit-ENVs, CMD streamlit run —
**kein `USER`**. Die App schreibt zur Laufzeit auf das Dateisystem:
Roster-Import nach `data/rosters/` (`rosz_importer.py`, `import_roster`) und
Spiel-Logs (Verzeichnis per `grep -rn "log" src/gameMechanic/game_log.py`
verifizieren — Stand Audit: fester Pfad unter dem Repo, aufgelistet via
`os.listdir`).

## Commands you will need

| Purpose | Command | Expected on success |
|---|---|---|
| Version verifizieren | `pip show streamlit pyyaml defusedxml \| grep -E "Name\|Version"` | 3 Versionen |
| Vollsuite | `pytest --tb=short` | exit 0, Coverage ≥ 99 % |
| Audit lokal | `pip install pip-audit && pip-audit -r requirements.txt` | exit 0, keine Findings |
| Docker (falls verfügbar) | `docker build -t arbiter-test . && docker run --rm arbiter-test id -u` | UID ≠ 0 |

## Scope

**In scope:**
- `requirements.txt` (exakte Pins)
- `requirements-dev.txt` (pip-audit ergänzen; Dev-Tools dürfen ungepinnt bleiben)
- `.github/workflows/deploy.yml` (pip-audit-Step im test-Job)
- `Dockerfile` (non-root User)

**Out of scope:**
- Versions-**Upgrades** — es wird der lokal verifizierte Ist-Stand gepinnt,
  nichts angehoben.
- `.pre-commit-config.yaml` — Hook-Versionen bleiben.
- README/Setup-Doku — macht Plan 039.

## Git workflow

- Branch: `chore/037-deps-pinning-docker-hardening`
- Commits z. B. `Pin runtime dependencies to verified versions`,
  `Add pip-audit step to CI`, `Run container as non-root user`
- Nicht pushen ohne Anweisung.

## Steps

### Step 1: Runtime-Pins setzen

Versionen aus dem lokalen venv per `pip show` ablesen und exakt pinnen:

```
streamlit==1.57.0
pyyaml==6.0.3
defusedxml==0.7.1
```

(Zahlen nur übernehmen, wenn `pip show` sie bestätigt — sonst die tatsächlich
installierten verwenden.)

**Verify**: `pytest --tb=short` → exit 0 (dieselben Versionen wie zuvor, es darf
sich nichts ändern).

### Step 2: pip-audit lokal laufen lassen und in CI verankern

1. `pip-audit` zu `requirements-dev.txt` hinzufügen.
2. Lokal ausführen: `pip install pip-audit && pip-audit -r requirements.txt`.
   Findings mit Fix-Version → **STOP und berichten** (Versionsentscheid ist
   Stakeholder-Sache, siehe Out of scope).
3. In `deploy.yml`, test-Job, nach dem Install-Step:

```yaml
      - name: Dependency vulnerability scan
        run: pip-audit -r requirements.txt
```

(Blocking — bewusst ohne `continue-on-error`.)

**Verify**: `pip-audit -r requirements.txt` → exit 0. YAML-Syntax:
`python -c "import yaml; yaml.safe_load(open('.github/workflows/deploy.yml'))"` → exit 0.

### Step 3: Dockerfile non-root

Vor dem `CMD` (HF Spaces empfiehlt UID 1000):

```dockerfile
RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app
USER appuser
ENV HOME=/home/appuser
```

Zu beachten: Die App schreibt nach `data/rosters/` und ins Log-Verzeichnis —
beides liegt unter `/app` und ist durch das `chown` abgedeckt. Prüfen, ob
Streamlit ein Config-/Cache-Verzeichnis unter `$HOME` anlegt (deshalb das
`ENV HOME`).

**Verify** (falls Docker verfügbar): `docker build -t arbiter-test .` → exit 0;
`docker run --rm arbiter-test id -u` → `1000`; Smoke:
`docker run --rm -p 7860:7860 -d arbiter-test` + `curl -s -o /dev/null -w "%{http_code}" http://localhost:7860` → `200`.
**Falls Docker lokal NICHT verfügbar**: Dockerfile-Änderung als „statisch
geprüft, Runtime-Verifikation auf HF Spaces beim nächsten Deploy nötig" im
Abschlussbericht ausweisen — nicht als verifiziert deklarieren.

### Step 4: Vollsuite + Lint

**Verify**: `pytest --tb=short` → exit 0; `ruff check src/ && black --check src/ && isort --check-only src/` → exit 0.

## Test plan

Keine neuen Unit-Tests (reine Infrastruktur). Verifikation über die
Step-Kommandos; der pip-audit-CI-Step ist selbst das dauerhafte Sicherheitsnetz.

## Done criteria

- [ ] `requirements.txt` enthält nur `==`-Pins, verifiziert gegen `pip show`
- [ ] `pip-audit -r requirements.txt` exit 0 lokal; Step in `deploy.yml` vorhanden (blocking)
- [ ] `Dockerfile` enthält `USER appuser` (UID 1000) nach `chown`
- [ ] `pytest --tb=short` exit 0, Coverage ≥ 99 %
- [ ] `git status`: nur In-Scope-Dateien geändert
- [ ] Status-Zeile in `docs/audit/plans/README.md` aktualisiert (inkl. Vermerk,
      ob Docker-Runtime-Verifikation erfolgte oder aussteht)

## STOP conditions

- `pip-audit` meldet eine Schwachstelle in einer gepinnten Version → berichten;
  das Upgrade entscheidet der Stakeholder (Out of scope hier).
- `pip show` zeigt andere Versionen als oben genannt und die Vollsuite ist mit
  ihnen NICHT grün → berichten statt raten.
- Der Docker-Smoke-Test schlägt mit Permission-Fehlern auf `data/` fehl →
  berichten (HF-Spaces-Mount-Ownership kann abweichen; nicht mit `chmod 777`
  „lösen").

## Maintenance notes

- Pins bewusst manuell (kein Lockfile-Tool) — bei 3 Runtime-Deps angemessen.
  Wächst die Dep-Liste, auf `pip-compile`/uv umstellen.
- Streamlit-Upgrades: CSS-Selektoren in CLAUDE.md („Bekannte Selektoren,
  Streamlit 1.57") sind versionsgebunden — beim Anheben des Pins die
  Emotion-Klassen prüfen (dokumentierter Repo-Gotcha).
- `pip-audit` im CI kann durch neu veröffentlichte Advisories „von allein" rot
  werden — das ist gewollt (Signal), nicht Flakiness.
