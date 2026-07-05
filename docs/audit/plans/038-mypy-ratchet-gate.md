# Plan 038: mypy vom Informational-Modus in ein Ratchet-Gate überführen

> **Executor instructions**: Schritt für Schritt folgen, jede Verifikation
> ausführen. Bei STOP-Bedingung: stoppen und berichten. Am Ende Status-Zeile in
> `docs/audit/plans/README.md` aktualisieren.
>
> **Drift check (zuerst ausführen)**:
> `git diff --stat f6c464a..HEAD -- .github/workflows/deploy.yml pyproject.toml tools/ docs/spec/architecture_invariants.md`
> Bei Änderungen: Exzerpte gegen Live-Code prüfen; Abweichung → STOP.

## Status

- **Priority**: P2
- **Effort**: M
- **Risk**: LOW
- **Depends on**: none
- **Category**: dx
- **Planned at**: commit `f6c464a`, 2026-07-05

## Why this matters

`pyproject.toml` konfiguriert `[tool.mypy] strict = true`, aber der CI-Step läuft
mit `continue-on-error: true` („informational"). Ergebnis: Der Fehlerbestand
wächst unbemerkt — beim Audit 2026-06-11 waren es 127 Fehler, jetzt ~136. In
einem Repo, das sonst überall Ratchets fährt (Coverage `fail_under`, INV-4b-
Ledger), ist Typsicherheit das einzige Gate ohne Zähne. Dieser Plan macht den
Bestand sichtbar und einfrierbar: **Der Zähler darf nur noch sinken.** Er baut
bewusst KEINE Fehler ab — das ist Folgearbeit in kleinen Schritten.

## Current state

`pyproject.toml:19-21`:

```toml
[tool.mypy]
python_version = "3.12"
strict = true
```

`.github/workflows/deploy.yml` (test-Job):

```yaml
      - name: Type check (informational)
        run: mypy src/
        continue-on-error: true
```

Referenz-Ist-Stand (verifizieren!): `mypy src/` endet mit
`Found ~136 errors in ~25 files` (Zahl schwankt je nach lokalem mypy-Stand —
der Plan friert die **gemessene** Zahl ein, nicht diese Schätzung).

**Repo-Muster für Ratchets** (als Vorbild lesen):
`tests/architecture/test_generic_src_vocab.py:10-18` — „DEBT LEDGER: … A new
faction token in a non-ledgered file fails the build. A ledger entry that no
longer leaks also fails — that is the ratchet: clean the code, shrink the
ledger." Dokumentiert in `docs/spec/architecture_invariants.md` (INV-4b).

**Design-Entscheidung dieses Plans**: Das Gate läuft als eigenständiges
CI-Skript (`tools/mypy_gate.py`), NICHT als pytest-Test — mypy braucht ~20–30 s,
und die lokale Vollsuite (`pytest --tb=short`) wird viele Male pro Session
ausgeführt; sie darf nicht langsamer werden. Bestehende tools/-Skripte
(`tools/token_report.py`, `tools/session_context.py`) zeigen die Konventionen
(Type Hints, argparse-frei wo unnötig, klare stdout-Meldungen).

## Commands you will need

| Purpose | Command | Expected on success |
|---|---|---|
| Ist-Stand messen | `mypy src/ 2>&1 \| tail -1` | `Found N errors in M files ...` |
| Gate lokal | `python tools/mypy_gate.py` | exit 0 + Zähler-Ausgabe |
| Vollsuite | `pytest --tb=short` | exit 0, Coverage ≥ 99 % (unverändert schnell) |
| Lint | `ruff check src/ tools/ && black --check src/ tools/ && isort --check-only src/ tools/` | exit 0 |

## Scope

**In scope:**
- `tools/mypy_gate.py` (neu)
- `.github/workflows/deploy.yml` (Step ersetzen)
- `docs/spec/architecture_invariants.md` (kurzer Abschnitt: neues Gate + Baseline
  — DoD-Regel „Gate + Doku gemeinsam, kein stilles Aufweichen")
- `tests/tools/` — falls dort Tests für tools/-Skripte existieren
  (`ls tests/tools/`), einen kleinen Test für die Parse-Funktion ergänzen

**Out of scope:**
- **Jegliches Fixen von mypy-Fehlern in `src/`** — der Plan friert nur ein.
  Kein einziger `src/`-Edit.
- `pyproject.toml` `[tool.mypy]` — strict bleibt strict; keine Ausnahmen/Overrides
  hinzufügen (das wäre stilles Aufweichen).
- Lokale pytest-Konfiguration (`addopts`) — Gate absichtlich nicht in pytest.

## Git workflow

- Branch: `chore/038-mypy-ratchet`
- Commit z. B. `Add mypy ratchet gate: error count may only shrink`
- Nicht pushen ohne Anweisung.

## Steps

### Step 1: Baseline messen

`mypy src/ 2>&1 | tail -1` ausführen; die exakte Fehlerzahl N notieren.
Erwartung: 120 ≤ N ≤ 150. Liegt N weit außerhalb → STOP (Umgebung weicht ab,
z. B. andere mypy-Version als im CI; dann zuerst mypy in `requirements-dev.txt`
pinnen — mit dem Stakeholder klären).

### Step 2: `tools/mypy_gate.py` schreiben

Verhalten (bewusst simpel, ~50 Zeilen):

1. Führt `mypy src/` als Subprozess aus (`sys.executable -m mypy src/`).
2. Parst die letzte Zeile `Found N errors in M files` (Regex; „Success: no
   issues" ⇒ N=0).
3. Vergleicht gegen `BASELINE = <N aus Step 1>` (Konstante im Skript, mit
   Kommentar „Ratchet: nur senken, nie erhöhen — bei Senkung Baseline im selben
   Commit nachziehen").
4. Exit-Codes: N > BASELINE → exit 1 („N neue mypy-Fehler über Baseline B —
   neue Fehler beheben, nicht die Baseline erhöhen"); N < BASELINE → exit 1
   („Fehlerbestand gesunken (N < B) — BASELINE in tools/mypy_gate.py auf N
   senken, im selben Commit"); N == BASELINE → exit 0 mit kurzer Statuszeile.
   (Beidseitige Strenge = INV-4b-Muster: Schrumpfen wird sofort eingelockt.)
5. mypy-Ausgabe bei Abweichung mit ausgeben (die letzten ~40 Zeilen reichen).

**Verify**: `python tools/mypy_gate.py` → exit 0, Ausgabe nennt N und BASELINE.
Gegenprobe: BASELINE testweise um 1 senken → exit 1 mit „Baseline senken"-
Meldung? Nein — umgekehrt: gemessen N wäre dann > BASELINE → exit 1 mit
„neue Fehler"-Meldung. Danach BASELINE zurücksetzen.

### Step 3: CI-Step ersetzen

In `deploy.yml`:

```yaml
      - name: Type check (ratchet gate)
        run: python tools/mypy_gate.py
```

(`continue-on-error` entfernen.)

**Verify**: `python -c "import yaml; yaml.safe_load(open('.github/workflows/deploy.yml'))"` → exit 0;
`grep -n "continue-on-error" .github/workflows/deploy.yml` → kein Treffer mehr.

### Step 4: Doku nachziehen

In `docs/spec/architecture_invariants.md` einen kurzen Abschnitt ergänzen
(Stil der bestehenden INV-Einträge übernehmen): Name (z. B. „Typ-Ratchet"),
Wächter (`tools/mypy_gate.py`, CI-Step), Baseline-Wert + Datum, Regel
(„shrink-only; Senkung = Baseline im selben Commit nachziehen; Erhöhung =
Build rot"), und der explizite Hinweis, dass der Abbau des Bestands
Folgearbeit ist (Backlog-Kandidat).

**Verify**: `grep -n "mypy" docs/spec/architecture_invariants.md` → Treffer im neuen Abschnitt.

### Step 5: Vollsuite + Lint

**Verify**: `pytest --tb=short` → exit 0 (Laufzeit unverändert — Gate hängt
NICHT in pytest); Lint (inkl. `tools/`) → exit 0.

## Test plan

- Falls `tests/tools/` existiert: ein Test für die Parse-Funktion
  (Regex gegen die drei Ausgabeformen: `Found N errors…`, `Success: no issues
  found`, leere/unerwartete Ausgabe → Fehler). Subprozess-Aufruf selbst wird
  nicht getestet (wäre 30-s-Test).
- Sonst: Verifikation über die Step-Kommandos; im Abschlussbericht vermerken,
  dass das Skript nur CI-verifiziert ist.

## Done criteria

- [ ] `python tools/mypy_gate.py` exit 0 lokal, Baseline == gemessener Ist-Stand
- [ ] `deploy.yml`: mypy-Step blocking, kein `continue-on-error` mehr
- [ ] Abschnitt in `architecture_invariants.md` vorhanden
- [ ] `pytest --tb=short` exit 0, Coverage ≥ 99 %, Laufzeit unverändert
- [ ] Kein Edit an `src/` (`git status`)
- [ ] Status-Zeile in `docs/audit/plans/README.md` aktualisiert

## STOP conditions

- Gemessene Fehlerzahl weit außerhalb 120–150 (mypy-Versionsdrift zwischen
  lokal und CI) → erst mypy-Version pinnen lassen (Stakeholder-Entscheid).
- mypy bricht mit Crash/Config-Fehler ab statt mit Fehlerliste → berichten.
- Es existiert bereits ein (übersehener) mypy-Gate-Mechanismus irgendwo
  (`grep -rn "mypy" tools/ tests/ .pre-commit-config.yaml`) → nicht doppeln,
  berichten.

## Maintenance notes

- Die Baseline ist eine **Schuld-Zahl**, kein Ziel: Backlog-Kandidat
  „mypy-Bestand modulweise abbauen" (beste Reihenfolge: zuerst `gameMechanic/`
  und `gameObjects/` — gemessene, gut getestete Module; `uiLayout/` zuletzt,
  da Render-Änderungen manuelle Verifikation kosten).
- mypy-Upgrades ändern die Fehlerzahl → Baseline im selben Commit wie das
  Upgrade anpassen (Richtung egal, aber im Commit begründen).
- Wer einen Fehler „wegfixt", indem er `# type: ignore` streut, erhöht die
  Zahl nicht — Reviewer sollten neue `type: ignore` trotzdem hinterfragen
  (strict zählt `ignore` ohne Code nicht als Fehler).
