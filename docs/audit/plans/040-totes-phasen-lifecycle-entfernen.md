# Plan 040: Totes Phasen-Lifecycle (`start`/`end`-Stages) entfernen

> **Executor instructions**: Schritt für Schritt folgen, jede Verifikation
> ausführen. Bei STOP-Bedingung: stoppen und berichten. Am Ende Status-Zeile in
> `docs/audit/plans/README.md` aktualisieren.
>
> **Drift check (zuerst ausführen)**:
> `git diff --stat f6c464a..HEAD -- src/gameMechanic/phase_runner.py src/gameMechanic/phase_handler.py src/gameMechanic/game_state.py src/gameMechanic/scenarios.py tests/gameMechanic/test_phase_runner.py`
> Bei Änderungen: Exzerpte gegen Live-Code prüfen; Abweichung → STOP.
> (Diffs aus Plan 033/035 in `game_state.py` sind erwartete Drift.)

## Status

- **Priority**: P2
- **Effort**: S–M
- **Risk**: LOW–MED (nur Löschung; Risiko = übersehener Nutzer des Mechanismus)
- **Depends on**: 033, 035 (gleiche Datei `game_state.py` — nacheinander)
- **Category**: tech-debt
- **Planned at**: commit `f6c464a`, 2026-07-05

## Why this matters

Das 3-Stufen-Phasen-Lifecycle (`start` → `active` → `end`) ist vollständig tot:
`advance_stage()` hat außerhalb seines eigenen Testfiles **null Aufrufer** — der
echte „Next Phase"-Button (`gameHeader.py:304-305`) ruft direkt
`game_state.next_phase()`. `phase_stage` wird einmal bei Spielstart auf
`"active"` gesetzt und nie wieder verändert; alle 14 `render_start`/`render_end`-
Methoden der 7 Handler sind unerreichbar, ebenso der „fire ability hooks"-Zweig.
Der Docstring von `advance_stage` behauptet sogar fälschlich „Called by the
phase-navigation button in gameProtocoll". Obendrein ist
`PsychicPhaseHandler.render_end` ein **inertes Duplikat** eines echten Resets
(`game_state.py:642-643` macht dasselbe live) — ein Drift-Kandidat. Die tote
Schicht führt jeden Leser (und jedes Modell) in die Irre, wie Phasenwechsel
funktionieren.

## Current state

`src/gameMechanic/phase_runner.py:30-62` — Dispatch + toter Hook + `advance_stage`:

```python
    stage: str = state.get("phase_stage", "active")

    # Fire ability hooks at phase transitions (start / end).
    if stage in ("start", "end"):
        get_triggered_abilities(state, phase_key, f"phase_{stage}")

    getattr(handler, f"render_{stage}")(state)


def advance_stage(state: dict) -> None:  # type: ignore[type-arg]
    """Advance the phase stage: start → active → end → next_phase.

    Called by the phase-navigation button in gameProtocoll.   # ← FALSCH (kein Aufrufer)
    ...
```

Belege für Totheit (beim Ausführen des Plans erneut prüfen, Step 1):
- `grep -rn "advance_stage" src/` → nur die Definition.
- `phase_stage`-Schreiber: nur `phase_runner.py:57-61` (toter Code selbst),
  `game_state.py:417` (Init auf `"active"`), `scenarios.py:28` (Reset-Tupel).
- `src/gameMechanic/phase_handler.py` (29 Zeilen): Protocol mit
  `render_start`/`render_active`/`render_end`; Docstring beschreibt den
  Stage-Dispatch als lebendig.
- 7 Handler-Dateien mit `render_start`/`render_end`-Stubs (meist `pass`);
  Ausnahme `psychicPhase.py:41-43` (`render_end` mit totem Duplikat-Reset).
- `src/gameObjects/ability.py:13`: `stage: str = "active"` mit Kommentar
  `# "start" | "active" | "end" — maps to phase_stage in session_state` —
  Feld bleibt (Out of scope), nur der Kommentar wird angepasst.

**Erwartete Test-Migrationen** (`tests/gameMechanic/test_phase_runner.py`, 290
Zeilen — Rote-Tests-Policy: NUR diese):
- `TestAdvanceStage` (Zeile ~262-290, 5 Tests) → komplett löschen.
- `test_all_handlers_have_render_start` (~105) und
  `test_all_handlers_have_render_end` (~117) → löschen.
- `TestRenderCurrentPhase`: `test_calls_render_start_for_start_stage` (~166),
  `test_calls_render_end_for_end_stage` (~185),
  `test_fires_triggered_abilities_on_start_stage` (~204),
  `test_fires_triggered_abilities_on_end_stage` (~223),
  `test_does_not_fire_triggered_abilities_on_active_stage` (~242) → löschen
  bzw. Letzteren zu „ruft keine Ability-Hooks auf" vereinfachen, falls der
  Hook-Import ganz verschwindet.
- Bleiben MÜSSEN: `test_all_seven_phase_keys_registered`,
  `test_each_handler_reports_correct_phase_name`,
  `test_all_handlers_have_render_active`,
  `test_warns_when_no_handler_registered`,
  `test_calls_render_active_for_active_stage` (anpassen: kein Stage-Getattr mehr).

## Commands you will need

| Purpose | Command | Expected on success |
|---|---|---|
| Totheits-Beweis | `grep -rn "advance_stage\|render_start\|render_end" src/` | nach Abschluss: 0 Treffer |
| Daten-Check | `grep -rn "phase_start\|phase_end" data/ \| grep -v "expires_at"` | 0 relevante Treffer (Step 1) |
| Vollsuite | `pytest --tb=short` | exit 0, Coverage ≥ 99 % |
| Lint | `ruff check src/ && black --check src/ && isort --check-only src/` | exit 0 |

## Scope

**In scope:**
- `src/gameMechanic/phase_runner.py` (Dispatch vereinfachen, `advance_stage` löschen)
- `src/gameMechanic/phase_handler.py` (Protocol + Docstring)
- Die 7 Handler: `commandPhase.py`, `movementPhase.py`, `psychicPhase.py`,
  `shootingPhase.py`, `chargephase.py`, `fightPhase.py`, `moralePhase.py`
  (NUR die `render_start`/`render_end`-Stubs löschen)
- `src/gameMechanic/game_state.py:417` (`phase_stage`-Init entfernen)
- `src/gameMechanic/scenarios.py:28` (`"phase_stage"` aus dem Reset-Tupel)
- `src/gameObjects/ability.py:13` (nur den Kommentar hinter `stage` anpassen)
- `tests/gameMechanic/test_phase_runner.py` (Migrationen s. o.)

**Out of scope:**
- Das `stage`-**Feld** in `ability.py` und `get_triggered_abilities` selbst —
  wird evtl. künftig gebraucht; nur der tote **Aufruf-Zweig** im runner fällt.
- Alles andere in den 7 Handler-Dateien (dort arbeiten Pläne 015/034/041!).
- `next_phase()`-Logik in `game_state.py`.

## Git workflow

- Branch: `refactor/040-remove-dead-phase-lifecycle`
- Commit z. B. `Remove dead phase start/end lifecycle machinery`
- Nicht pushen ohne Anweisung.

## Steps

### Step 1: Totheit erneut beweisen (Gate für alles Weitere)

1. `grep -rn "advance_stage" src/` → nur Definition in `phase_runner.py`.
2. `grep -rn "phase_stage" src/ | grep -v "phase_runner\|game_state.py:417"` →
   nur `scenarios.py` (Reset) und Kommentare.
3. `grep -rn "stage:" data/wh40k_9e/ | grep -v "stage: active"` sowie
   `grep -rn '"phase_start"\|"phase_end"' src/ data/` → keine YAML-Daten und
   kein weiterer Code nutzen Start/End-Trigger.

Jeder unerwartete Treffer → **STOP** (der Mechanismus ist doch nicht tot).

### Step 2: Runner vereinfachen

`render_current_phase` reduzieren auf: Handler auflösen, warnen falls fehlt,
`handler.render_active(state)` aufrufen. Stage-Lesen, Hook-Zweig und den
dann ungenutzten `get_triggered_abilities`-Import entfernen. `advance_stage`
komplett löschen.

**Verify**: `pytest tests/gameMechanic/test_phase_runner.py --no-cov -q` →
genau die oben gelisteten Migrations-Tests schlagen fehl, keine anderen.

### Step 3: Protocol + Handler-Stubs + State-Reste

`phase_handler.py`: `render_start`/`render_end` aus dem Protocol, Docstring auf
den realen Ablauf umschreiben („render_active pro Phase; Übergänge macht
`game_state.next_phase()`"). In allen 7 Handlern die Stubs löschen
(inkl. des toten Duplikat-Resets in `psychicPhase.render_end`).
`game_state.py:417` und `scenarios.py:28` von `phase_stage` befreien.
`ability.py:13`-Kommentar kürzen (Feld dokumentieren, toten Mapping-Verweis raus).

**Verify**: `grep -rn "advance_stage\|render_start\|render_end\|phase_stage" src/` → 0 Treffer.

### Step 4: Test-Migrationen ausführen (Liste aus „Current state")

**Verify**: `pytest tests/gameMechanic/test_phase_runner.py --no-cov -q` → all pass.

### Step 5: Vollsuite + Lint

**Verify**: `pytest --tb=short` → exit 0, Coverage ≥ 99 % (Achtung: Löschungen
in gemessenen Dateien verändern den Nenner — das Gate muss trotzdem halten);
Lint-Dreier → exit 0.

## Test plan

Nur Migrationen (s. o.) — Löschpläne brauchen keine neuen Tests; das
Sicherheitsnetz ist die unveränderte restliche Suite plus der 0-Treffer-grep.

## Done criteria

- [ ] `grep -rn "advance_stage\|render_start\|render_end\|phase_stage" src/` → 0 Treffer
- [ ] `pytest --tb=short` exit 0, Coverage ≥ 99 %
- [ ] Nur die gelisteten Tests wurden entfernt/angepasst
- [ ] `phase_handler.py`-Docstring beschreibt den realen Dispatch
- [ ] `git status`: nur In-Scope-Dateien geändert
- [ ] Status-Zeile in `docs/audit/plans/README.md` aktualisiert

## STOP conditions

- Step 1 findet einen echten Nutzer von `advance_stage`/`phase_stage`/
  Start-End-Triggern (Code ODER YAML) → Plan-Prämisse fällt, berichten.
- Ein Test außerhalb der Migrations-Liste wird rot.
- Die Coverage fällt durch die Löschung unter 99 % (theoretisch möglich, wenn
  gelöschte Zeilen zu 100 % gedeckt waren und der Rest-Nenner ungünstiger wird)
  → berichten, NICHT das Gate absenken.

## Maintenance notes

- Braucht künftig ein Feature echte Phasen-Start/End-Hooks (z. B. neue
  Ability-Trigger), den Mechanismus **bewusst neu** einführen — zusammen mit
  YAML-Daten, die ihn nutzen, und Tests, die den Dispatch treiben. Nicht den
  alten Code aus der Git-History „reaktivieren", ohne die damalige
  Totheits-Ursache (kein Aufrufer am Button) zu beheben.
- Das `stage`-Feld in `ability.py` bleibt als Datenschema erhalten — wer es
  entfernt, muss die YAML-Kataloge mitprüfen.
