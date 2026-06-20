# Plan 014: P17 — Interaktive Schadenszuweisung auf Subgruppen (Defender Loss Allocation)

> **Executor instructions**: Follow this plan step by step. Run every
> verification command and confirm the expected result before moving to the
> next step. If anything in the "STOP conditions" section occurs, stop and
> report — do not improvise. When done, update the status row for this plan
> in `docs/audit/plans/README.md`.
>
> **Drift check (run first)**:
> Plan 013 MUSS abgeschlossen sein (Status DONE in `docs/audit/plans/README.md`).
> `grep -n "render_attack_declaration" src/` → 0 Call-Sites (Beweis, dass 013 lief).
> `grep -n "_render_damage_block\|apply_damage\|_apply_group_losses" src/uiLayout/_common.py src/gameMechanic/unit_mutations.py`
> → Funktionen existieren, Signaturen stimmen mit Step-Beschreibungen unten überein.
> Bei strukturellen Abweichungen: STOP.

## Status

- **Priority**: P1-HOCH (ziel6.md §6n P17, nachgeschärft Refinement 2026-06-20)
- **Effort**: M
- **Risk**: MEDIUM (greift in den Schadenspfad ein; Gruppen-Buchhaltung muss konsistent bleiben)
- **Depends on**: 013 (zwingend — ein Code-Pfad; beide ändern `_common.py`); 019 (empfohlen vorher)
- **Category**: feature (Regelkonformität Verlust-Zuweisung)
- **Planned at**: Refinement 2026-06-20
- **Branch**: `feature/014-defender-loss-allocation`

## Why this matters

Regel (9E, Verteidiger wählt Verluste): Der **Verteidiger** bestimmt, welche
Modelle Schaden erhalten. Kritisch: Nobz mit gemischter Bewaffnung — WELCHER Nob
fällt, bestimmt die verfügbaren Waffen der Folgerunden. Ohne interaktive Wahl
„bricht die Logik" (Nutzer-Originalformulierung).

**Lock-Regel (9E):** Ist ein Modell bereits angeschlagen (hat Wunden verloren,
aber lebt noch), MÜSSEN alle weiteren Wunden dieses Turns auf dieses Modell
gelenkt werden — andere Subgruppen sind gesperrt. Erst nach Zerstörung des
angeschlagenen Modells ist freie Wahl wieder möglich.

**Mortal Wounds (Overflow):** `mortal=True` ist bereits im Code implementiert
und erlaubt Overflow über Modell-Grenzen hinaus. Der neue interaktive Flow muss
diesen Parameter korrekt weiterreichen.

**Lethal Hits:** OUT OF SCOPE (eigener Plan nach 014).

## Current state

- `unit_mutations.py` — `apply_damage()`: reduziert `current_wounds` → `models`;
  `lost = old_models - models`; ruft `_apply_group_losses(state["group_models"],
  lost, unit.model_groups)` (priority-aufsteigend). Kein Lock-Check, keine
  Subgruppen-Auswahl.
- `_common.py` — `_render_damage_block()`: Apply-Button ruft `apply_damage(...,
  resolved=True)`; schreibt `st.session_state[res_key] = {"applied": True,
  "models_lost": …, …}`. Die Subgruppen-Auswahl fehlt komplett — sie muss VOR
  dem Apply-Button eingebaut werden.
- Nach Plan 013 hat JEDE Einheit `model_groups`; synthetische Einzelgruppen-
  Einheiten (homogen) haben genau eine Gruppe — dort kein interaktives UI nötig.

## 3 Zustände der Subgruppen-Auswahl

### Zustand A — Freie Wahl (kein angeschlagenes Modell)

```
SCHADENSZUWEISUNG — Nobz (5 Modelle · 3 LP je Modell)
 Subgruppe               Modelle   LP             Ausrüstung
 ──────────────────────────────────────────────────────────
 Nob – Power Klaw+BC       2       ●●● ●●●        Power Klaw, Big Choppa
 Nob – 2× Kill Saw         2       ●●● ●●●        Kill Saw ×2
 Nob – Slugga+Choppa       1       ●●●            Slugga, Choppa
 → Kein Modell angeschlagen. Welche Subgruppe erhält den nächsten Schaden?
   ○ Nob – Power Klaw+BC
   ○ Nob – 2× Kill Saw
   ○ Nob – Slugga+Choppa
```

### Zustand B — Gesperrt (angeschlagenes Modell vorhanden)

```
 Nob – Power Klaw+BC       2       ●●● ●●●   [—]  Power Klaw, Big Choppa
 Nob – 2× Kill Saw     ►  2       ●●● ●○○   [▶]  Kill Saw ×2
                                    └─ 1 LP verbleibend
 Nob – Slugga+Choppa       1       ●●●       [—]  Slugga, Choppa
 ⚠ Angeschlagenes Modell muss zuerst abgehandelt werden.
   [ Schaden → Nob 2× Kill Saw ]
```

### Zustand C — Modell zerstört

```
 ✕ Nob – 2× Kill Saw: 1 Modell vernichtet.
   ⚠ [Wenn letztes Modell der Subgruppe: Fähigkeit verloren — Kill Saw ×2 nicht mehr verfügbar]
 → Nächster Schaden: freie Wahl (s. Zustand A)
```

## Commands you will need

| Zweck | Befehl | Erwartet |
|-------|--------|----------|
| venv | `source .venv/bin/activate` | `(.venv)` |
| Mutations-Tests | `python -m pytest tests/gameMechanic/test_unit_mutations.py -q` | grün |
| Gruppen-Tests | `python -m pytest tests/uiLayout/test_group_flow.py -q` | grün |
| Vollsuite | `pytest --tb=short` | grün, ≥ 90 % |
| Lint | `ruff check src/ && black --check src/ && isort --check-only src/` | passt |
| App | `streamlit run src/app.py` | Port 8501 |

## Scope

**In scope**:
- `src/gameMechanic/unit_mutations.py` — neue Funktionen `select_damage_target_group()`,
  `get_locked_group()`; Lock-Check in `apply_damage`
- `src/uiLayout/_common.py` — `_render_damage_block()`: neue Subgruppen-Auswahl
  VOR dem Apply-Button (Zustand A/B/C); Mortal-Wound-Overflow korrekt weiterreichen
- Tests: PFLICHT auf 4 Schichten (siehe Test plan)

**Out of scope** (NICHT anfassen):
- Frontmodell-Tracking (Mehrwunden-Einheit): `current_wounds` bleibt Unit-Level;
  im Abschlussbericht als bekannte Limitation dokumentieren
- Lethal Hits Overflow → eigener Plan nach 014
- Angreifer-seitige Sicht auf Verteidiger-Gruppen (bleibt verborgen)
- Morale-/Flee-Pfad (`flee_models` ohne Gruppen-Reduktion — falls auffällig: NUR melden)
- YAML-Daten — keine Änderungen

## Git workflow

- Branch: `feature/014-defender-loss-allocation`
- Commit-Stil imperativ Englisch, z. B. `Add select_damage_target_group and lock logic`
- Mehrere Commits erlaubt (sinnvolle Schnitte: Step 1 / Step 2 / Step 3+4)
- Nicht pushen/PR ohne Anweisung

## Steps

### Step 1: State-Erweiterung in `unit_mutations.py`

Zwei neue Funktionen ergänzen:

```python
def select_damage_target_group(uid: str, faction: str, group_id: str) -> None:
    """Defender's choice: set the active subgroup for the next damage application.

    Stores group_id as damage_active_group_id in the unit's session state.
    Raises ValueError if group_id is not a known group of this unit.
    """
```

```python
def get_locked_group(uid: str, faction: str) -> str | None:
    """Return the group_id that must receive the next wound, or None if free choice.

    A group is locked when any of its models has taken wounds but is not yet
    destroyed (i.e., group_wounds[gid] > 0 for that group).
    Returns the first such group_id found, or None if no group is wounded.
    """
```

**Lock-Check in `apply_damage`:**
- Vor Anwendung prüfen: wenn `get_locked_group()` einen `gid` zurückgibt UND
  `damage_active_group_id != gid` → ValueError (UI verhindert das, Defensiv-Check
  für Tests und direkte Aufrufe).
- Mortal-Wound-Overflow (`mortal=True`) bleibt als Parameter erhalten und wird
  korrekt durch den neuen Pfad weitergereicht.

**State-Felder** (in `group_models`-State der Einheit):
- `damage_active_group_id: str | None` — vom Verteidiger gewählte Gruppe
- `group_wounds: dict[str, int]` — aktuelle Wunden des Frontmodells je Gruppe
  (0 wenn kein angeschlagenes Modell in dieser Gruppe)

**Verify**:
```
python -m pytest tests/gameMechanic/test_unit_mutations.py -q
```
→ grün (neue Tests aus Test plan Step 1).

### Step 2: UI in `_common.py` — Subgruppen-Auswahl VOR Apply-Button

In `_render_damage_block()`, VOR dem Apply-Button, NUR wenn die Einheit mehr als
eine aktive Gruppe hat (`alive > 0` je Gruppe):

**Zustand A** (kein Lock: `get_locked_group() is None`):
- Radioauswahl aus aktiven Subgruppen (Gruppen mit `alive > 0`)
- Key: `dmg_target_grp_{tab_key}`; Default: erste Gruppe (nach priority)
- Caption je Option: Gruppenname + Waffennamen
- Auswahl ruft `select_damage_target_group()` beim nächsten Apply

**Zustand B** (Lock aktiv: `get_locked_group()` liefert `gid`):
- Tabelle zeigt alle Gruppen; gesperrte hervorgehoben (`►`), andere `[—]`
- LP-Anzeige für angeschlagenes Modell (`group_wounds[gid]` verbleibend)
- Direkter Schaden-Button nur auf die gesperrte Gruppe
- Warntext: „Angeschlagenes Modell muss zuerst abgehandelt werden."

**Zustand C** (nach Modell-Zerstörung, `models_lost > 0` im letzten Apply):
- Zerstörungs-Meldung: `✕ <Gruppenname>: 1 Modell vernichtet.`
- Wenn `group_models[gid] == 0` (letzte Modell der Subgruppe): Ausrüstungs-Warnung
  `st.warning(f"Fähigkeit verloren — <Waffenliste> nicht mehr verfügbar")`
- Danach: freie Wahl wieder möglich (zurück zu Zustand A)

Pattern orientiert sich an `pending_target_request` aus Plan 019 (wenn vorhanden),
sonst analog zu bestehenden `st.radio`-Patterns in `_common.py`.

**Verify**: Bestehende Tests grün (reine UI-Erweiterung vor dem Button).

### Step 3: Tests (PFLICHT — 4 Schichten)

**Schicht 1 — Unit-Tests `tests/gameMechanic/test_unit_mutations.py`:**

- `test_select_damage_target_group_sets_state`: Happy Path — `group_id` wird
  in State geschrieben.
- `test_select_damage_target_group_invalid_group_raises`: unbekannte `group_id`
  → ValueError.
- `test_get_locked_group_returns_none_when_no_wounded`: kein angeschlagenes
  Modell → `None`.
- `test_get_locked_group_returns_wounded_group`: Gruppe mit `group_wounds > 0`
  → liefert diese `gid`.
- `test_lock_invariante_apply_damage_wrong_group_raises`: Lock aktiv + falscher
  `group_id` in `apply_damage` → ValueError.
- `test_mortal_wound_overflow_through_new_flow`: `mortal=True` liefert Overflow
  korrekt (Regression).
- `test_single_group_unit_no_interactive_ui_needed`: Einzelgruppen-Einheit
  (nach Plan 013) → `get_locked_group` und `select_damage_target_group` funktionieren,
  aber UI-Bedingung `len(active_groups) > 1` ist False.

**Schicht 2 — Acceptance-Tests `tests/uiLayout/test_group_flow.py`:**

- `test_zustand_a_b_c_transition_nobz`: Nobz-Szenario (2 × PK+BC, 2 × Kill Saw,
  1 × Slugga+Choppa); Schaden auf Kill-Saw-Gruppe → Zustand B (Lock); weiterer
  Schaden zerstört Modell → Zustand C (Warnung); danach Zustand A (freie Wahl).
- `test_regressionstest_nobz_killsaw_group_destroyed`: Kill-Saw-Gruppe auf 0 →
  `group_models["kill_saw"] == 0`; Ausrüstungs-Warnung enthält „Kill Saw".

**Schicht 3 — Architektur-Test (bestehend):**

`pytest tests/architecture/ --no-cov -q` → grün.
Kein neuer Fraktions-String in `src/` eingeführt (prüfen mit
`grep -rn "necron\|ork\|custodes" src/gameMechanic/unit_mutations.py`
→ kein Treffer).

**Schicht 4 — Manuelle Verifikation (Nobz-Roster):**

Roster: Nobz-Einheit mit Subgruppen `2 × Nob (PK+BC)`, `2 × Nob (Kill Saw ×2)`,
`1 × Nob (Slugga+Choppa)`.

| Schritt | Erwartetes Verhalten |
|---|---|
| Schaden auf Kill-Saw-Gruppe wählen | Zustand A zeigt Radio; Auswahl möglich |
| Ersten Schaden anwenden (1 Wunde, Modell lebt) | Lock → Zustand B; andere Gruppen gesperrt |
| Weiteren Schaden anwenden (Modell stirbt) | Zustand C: Vernichtungs-Meldung |
| Kill Saw letztes Modell stirbt | Ausrüstungs-Warnung: „Kill Saw ×2 nicht mehr verfügbar" |
| Nächste Schadensrunde | Zustand A: freie Wahl wiederhergestellt |
| Einzelgruppen-Einheit (Warriors) | Keine Subgruppen-Auswahl angezeigt |

**Verify nach allen manuellen Schritten**: `pytest --tb=short` → grün.

### Step 4: Vollsuite + Lint + Doku

- `pytest --tb=short` grün, Coverage ≥ 90 %; kein neuer uncovered Pfad.
- `ruff check src/ && black --check src/ && isort --check-only src/` → passt.
- Abschlussbericht im `next_session.md`: manuelle Verifikationspunkte auflisten
  + bekannte Limitation Frontmodell-Tracking explizit dokumentieren.

## Test plan (Zusammenfassung)

| Test | Datei | Typ |
|---|---|---|
| `select_damage_target_group` Happy Path | `test_unit_mutations.py` | Unit |
| `select_damage_target_group` invalid group | `test_unit_mutations.py` | Unit |
| `get_locked_group` kein verwundetes Modell | `test_unit_mutations.py` | Unit |
| `get_locked_group` verwundete Gruppe | `test_unit_mutations.py` | Unit |
| Lock-Invariante: falscher group_id → ValueError | `test_unit_mutations.py` | Unit |
| Mortal-Wound-Overflow Regression | `test_unit_mutations.py` | Unit |
| Einzelgruppe: kein interaktives UI | `test_unit_mutations.py` | Unit |
| Zustand A→B→C Transition (Nobz) | `test_group_flow.py` | AC |
| Kill-Saw-Gruppe zerstört → Warnung | `test_group_flow.py` | AC |
| Kein Fraktions-String in src/ | `tests/architecture/` | Architektur |
| Nobz-Roster alle 3 Zustände | manuell | Manuell |
| Fähigkeits-Warnung bei Gruppen-Zerstörung | manuell | Manuell |
| Einzelgruppen-Einheit ohne UI | manuell | Manuell |

## Done criteria

ALLE müssen gelten:

- [ ] `select_damage_target_group()` und `get_locked_group()` implementiert, mit
      Validierung und Unit-Tests grün
- [ ] Lock-Check in `apply_damage`: falscher `group_id` bei Lock → ValueError (getestet)
- [ ] Mortal-Wound-Overflow (`mortal=True`) korrekt durch neuen Flow weitergereicht
      (Regressionstest grün)
- [ ] Zustand A/B/C korrekt gerendert; Locked-State persistiert zwischen Renders
- [ ] Einzelgruppen-Einheiten: kein interaktives Subgruppen-UI (Bedingung `len > 1`)
- [ ] `pytest --tb=short` grün, Coverage ≥ 90 %; Lint sauber
- [ ] Manuell verifiziert: Nobz-Roster alle 3 Zustände; Fähigkeits-Warnung erscheint;
      Warriors ohne Subgruppen-UI
- [ ] Status-Zeile in `docs/audit/plans/README.md` aktualisiert

## STOP conditions

- Plan 013 nicht DONE → STOP (falscher Ausgangszustand; `_render_damage_block`
  und `model_groups`-Invariante fehlen).
- `_render_damage_block` hat nach 013 eine strukturell andere Apply-Mechanik
  (z. B. kein `res_key`-State mehr) → STOP, Neuplanung nötig.
- Mehrwunden-Einheit ohne Subgruppen, bei der Frontmodell-Problem real auftritt
  (Schaden „hängt" zwischen Gruppen): dokumentieren, kein interaktives UI zeigen,
  NICHT improvisieren — melden.
- Lethal Hits Overflow wird für Korrektheit nötig → STOP, eigener Plan nach 014.
- Ein Test wird rot, der NICHT zu den neuen Features gehört → STOP, melden.

## Maintenance notes

- `select_damage_target_group` / `get_locked_group` sind UI-unabhängig — wenn
  Undo/Redo für ganze Angriffe gebaut wird, können dieselben State-Felder genutzt
  werden.
- Wenn Morale-Verluste (`flee_models`) später gruppenfähig werden, dieselbe
  Lock-Logik wiederverwenden.
- Frontmodell-Tracking (Mehrwunden-Einheit, Wunden zwischen Gruppen): bewusste
  bekannte Limitation; `current_wounds` bleibt Unit-Level. Ziel6.md nennt es
  „Folgefrage bei Umsetzung". Im Abschlussbericht explizit als Einschränkung
  benennen.
