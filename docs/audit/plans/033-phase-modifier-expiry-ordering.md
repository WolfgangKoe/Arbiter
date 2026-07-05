# Plan 033: Phasen-Modifier laufen am Ende ihrer Phase ab (Expiry-Reihenfolge in `next_phase()` fixen)

> **Executor instructions**: Diesem Plan Schritt für Schritt folgen. Jedes
> Verifikations-Kommando ausführen und das erwartete Ergebnis bestätigen, bevor
> der nächste Schritt beginnt. Tritt eine STOP-Bedingung ein: stoppen und
> berichten — nicht improvisieren. Am Ende die Status-Zeile dieses Plans in
> `docs/audit/plans/README.md` aktualisieren.
>
> **Drift check (zuerst ausführen)**:
> `git diff --stat f6c464a..HEAD -- src/gameMechanic/game_state.py tests/gameMechanic/test_game_state.py`
> Hat sich eine In-Scope-Datei seit Planerstellung geändert: die
> „Current state"-Exzerpte gegen den Live-Code prüfen; bei Abweichung → STOP.

## Status

- **Priority**: P1
- **Effort**: S
- **Risk**: LOW
- **Depends on**: none
- **Category**: bug
- **Planned at**: commit `f6c464a`, 2026-07-05

## Why this matters

Stratagems mit `expires_at: phase_end` (6 Stück in `data/wh40k_9e/*/stratagems.yaml`,
z. B. Hit-/Wound-/Strength-Modifier) sollen genau bis zum Ende der Phase wirken, in
der sie aktiviert wurden. Wegen einer falschen Operations-Reihenfolge in
`next_phase()` überleben sie stattdessen, bis dieselbe Phase das nächste Mal
*beginnt* — also durch den Rest des eigenen Zugs und weite Teile des gegnerischen
Zugs. Ein „+1 Strength diese Phase" wirkt so z. B. noch in der gegnerischen
Shooting Phase und verfälscht die Kampfmathematik.

## Current state

- `src/gameMechanic/game_state.py` — enthält `next_phase()` und `_reset_phase_state()`.
- `src/uiLayout/gameProtocoll.py:280-282` — schreibt beim Aktivieren eines Stratagems
  `"expires_at_phase": current_phase if m.expires_at == "phase_end" else None` —
  der Eintrag trägt also den Namen der Aktivierungs-Phase und soll bei deren
  **Ende** entfernt werden.

`_reset_phase_state()` filtert abgelaufene Modifier über `phase_idx`
(`game_state.py:544-553`):

```python
    current_phase = PHASES[st.session_state.get("phase_idx", 0)][1]
    current_round = st.session_state.get("round", 1)
    st.session_state.active_modifiers = [
        m
        for m in st.session_state.get("active_modifiers", [])
        if not (
            m.get("expires_at_phase") == current_phase
            or (m.get("expires_at_round") is not None and m["expires_at_round"] <= current_round)
        )
    ]
```

`next_phase()` (`game_state.py:613-638`): Der Spielerwechsel-Zweig macht die
Reihenfolge **richtig** (Reset läuft, solange `phase_idx` noch auf die endende
Phase zeigt), der Intra-Turn-Zweig macht sie **falsch**:

```python
    elif idx >= num - 1:  # Morale done → switch player
        ...
        _reset_turn_state()
        _reset_phase_state()               # liest noch die endende Phase ("morale") — KORREKT
        st.session_state.phase_idx = 1
    else:
        st.session_state.phase_idx = idx + 1   # phase_idx zeigt schon auf die NEUE Phase
        _reset_phase_state()                   # Filter matcht die endende Phase nie — BUG
```

`PHASES` (`game_state.py:40-49`): setup, command, movement, psychic, shooting,
charge, fight, morale (Index 0–7).

Konkret: Modifier `expires_at_phase="shooting"`, aktiviert in der Shooting Phase
(idx 4). Übergang shooting→charge setzt `phase_idx` erst auf 5, der Filter liest
„charge" → kein Match. Entfernt wird der Modifier erst beim Übergang
psychic→shooting im **gegnerischen** Zug.

## Commands you will need

| Purpose | Command | Expected on success |
|---|---|---|
| Vollsuite + Coverage-Gate | `pytest --tb=short` | exit 0, Coverage ≥ 99 % |
| Nur betroffene Tests | `pytest tests/gameMechanic/test_game_state.py --no-cov -q` | all pass |
| Lint | `ruff check src/ && black --check src/ && isort --check-only src/` | exit 0 |

## Scope

**In scope** (nur diese Dateien ändern):
- `src/gameMechanic/game_state.py` (nur der `else`-Zweig von `next_phase()`)
- `tests/gameMechanic/test_game_state.py` (neue Regressionstests)

**Out of scope** (NICHT anfassen, auch wenn verwandt):
- `src/uiLayout/gameProtocoll.py` — der Schreibpfad des Modifiers ist korrekt.
- Der `idx == 0`-Zweig (Setup→Command): bei Spielstart existieren keine Modifier,
  die Reihenfolge ist dort folgenlos. Nicht „mitverschönern".
- `_reset_phase_state()` selbst — Filterlogik korrekt; nur die Aufruf-Reihenfolge
  im `else`-Zweig ist falsch.
- `_reset_turn_state()` — wird von Plan 035 geändert. Diesen Plan NICHT parallel
  zu Plan 035 ausführen (gleiche Datei, benachbarte Pfade).

## Git workflow

- Branch: `fix/033-phase-modifier-expiry` (Repo-Konvention: `fix/...` / `feature/NNN-...`)
- Commit kurz, imperativ, Englisch — z. B. `Fix phase modifier expiry to run before phase index advances`
- Nicht pushen, keinen PR öffnen, außer der Operator verlangt es.

## Steps

### Step 1: Reihenfolge im `else`-Zweig tauschen

In `next_phase()` den `else`-Zweig spiegelbildlich zum Spielerwechsel-Zweig ordnen:

```python
    else:
        _reset_phase_state()
        st.session_state.phase_idx = idx + 1
```

**Verify**: `pytest tests/gameMechanic/test_game_state.py --no-cov -q` → all pass
(die bestehenden Tests `test_removes_expired_phase_modifiers` /
`test_keeps_non_expired_modifiers`, Zeile ~715-726, rufen `_reset_phase_state()`
direkt auf; ihre Semantik ändert sich nicht — sie müssen grün bleiben).

### Step 2: Regressionstests auf `next_phase()`-Ebene

In `tests/gameMechanic/test_game_state.py` eine neue Testklasse (Streamlit-Mock
+ Session-Dict-Aufbau nach dem Muster von `test_next_phase_resets_selected_unit_and_targets`,
Zeile ~274):

1. `test_phase_end_modifier_removed_when_its_phase_ends` — `phase_idx=4`
   (shooting), Modifier `{"expires_at_phase": "shooting"}`, `next_phase()` →
   Modifier entfernt.
2. `test_phase_end_modifier_survives_other_phase_transitions` — `phase_idx=4`,
   Modifier `expires_at_phase="charge"` → nach `next_phase()` noch vorhanden
   (Charge hat erst begonnen).
3. `test_phase_end_modifier_removed_at_player_switch` — `phase_idx=7` (morale),
   Modifier `expires_at_phase="morale"` → nach `next_phase()` entfernt
   (sichert den bereits korrekten Zweig).

**Verify**: `pytest tests/gameMechanic/test_game_state.py --no-cov -q` → all pass, 3 neue Tests.

### Step 3: Vollsuite + Lint

**Verify**: `pytest --tb=short` → exit 0, Coverage ≥ 99 %.
**Verify**: `ruff check src/ && black --check src/ && isort --check-only src/` → exit 0.

## Test plan

Siehe Step 2 — drei neue Tests in `tests/gameMechanic/test_game_state.py`.

## Done criteria

- [ ] `pytest --tb=short` exit 0, Coverage ≥ 99 %
- [ ] 3 neue Tests aus Step 2 existieren und sind grün
- [ ] Im `else`-Zweig steht `_reset_phase_state()` vor der `phase_idx`-Zuweisung
- [ ] `git status`: keine Dateien außerhalb der In-Scope-Liste geändert
- [ ] Status-Zeile in `docs/audit/plans/README.md` aktualisiert

## STOP conditions

- Code an den zitierten Stellen weicht von den Exzerpten ab (Drift).
- Ein VORHER grüner Test wird rot, der oben nicht als erwartet genannt ist
  (CLAUDE.md-Sicherheitsnetz-Regel).
- Die Annahme „`_reset_phase_state()` hängt außer dem Modifier-Filter nicht von
  `phase_idx` ab" erweist sich als falsch (Zeilen 522–553 prüfen) — dann hätte
  das Vorziehen Nebenwirkungen.

## Maintenance notes

- Invariante für künftige `next_phase()`-Änderungen: `_reset_phase_state()` läuft
  immer, solange `phase_idx` noch auf die **endende** Phase zeigt. Reviewer
  sollten genau das im Diff prüfen.
- Der `idx == 0`-Zweig bleibt bewusst unverändert (keine Modifier bei Spielstart) —
  hier dokumentiert, damit es niemand als Inkonsistenz „mitfixt".
