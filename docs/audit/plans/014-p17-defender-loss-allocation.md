# Plan 014: P17 — Verteidiger-Korrektur bei Schadenszuweisung gegen Gruppen-Einheiten

> **Executor instructions**: Follow this plan step by step. Run every
> verification command and confirm the expected result before moving to the
> next step. If anything in the "STOP conditions" section occurs, stop and
> report — do not improvise. When done, update the status row for this plan
> in `docs/audit/plans/README.md`.
>
> **Drift check (run first)**:
> Plan 013 MUSS abgeschlossen sein (Status DONE in `docs/audit/plans/README.md`).
> `grep -n "render_attack_declaration" src/` → 0 Call-Sites (Beweis, dass 013 lief).
> Die Zeilennummern unten stammen von Commit `f0f4e17` (VOR 013) — nach 013
> verschoben, die Funktionsnamen gelten weiter. Bei strukturellen Abweichungen
> in `_render_damage_block`/`_apply_group_losses`: STOP.

## Status

- **Priority**: P1 (HOCH — ziel6.md §6n P17, nachgeschärft 2026-06-10)
- **Effort**: M
- **Risk**: MEDIUM (greift in den Schadenspfad ein; Gruppen-Buchhaltung muss konsistent bleiben)
- **Depends on**: 013 (zwingend — ein Code-Pfad; beide ändern `_common.py`)
- **Category**: feature (Regelkonformität Verlust-Zuweisung)
- **Planned at**: commit `f0f4e17`, 2026-06-12

## Why this matters

Regel (9E): Der **Verteidiger** entscheidet, welche Modelle als Verluste
entfernt werden. Die App verteilt Verluste heute automatisch nach
`priority` (`_apply_group_losses`, `unit_mutations.py:11-23`) — Standardmodelle
sterben zuerst. Kritischer Fall (Nutzer): Nobz mit gemischter Bewaffnung —
WELCHER Nob fällt, bestimmt die verfügbaren Waffen der Folgerunden. Ohne
Korrekturmöglichkeit „bricht die Logik". Nutzer-Entscheidung (2026-06-10):
Zielauswahl bleibt auf Einheiten-Ebene (Untergruppen des Verteidigers sind
für den Angreifer unsichtbar — regelkonform), aber NACH „Apply Damage"
bekommt der Verteidiger ±-Counter pro Gruppe (Summe = Verluste, Default =
priority-Verteilung). Danach muss klar erkennbar sein, welche Waffen
weggefallen sind.

## Current state

- `unit_mutations.py:40-72` — `apply_damage()`: reduziert `current_wounds` →
  `models`; `lost = old_models - models`; ruft `_apply_group_losses(state
  ["group_models"], lost, unit.model_groups)` (priority-aufsteigend).
- `_common.py:502-626` — `_render_damage_block()`: Apply-Button (Z. 586) ruft
  `apply_damage(..., resolved=True)`; schreibt `st.session_state[res_key] =
  {"applied": True, "models_lost": …, …}` (Z. 619-625). Applied-Branch
  (Z. 520-530): Success-Zeile + `_render_rp_block` + „↺ Reset"-Button.
- `_common.py:454-499` — `_render_rp_block()`: Reanimation nach Verlusten;
  `heal_unit` → `_restore_group_models` füllt nach priority zurück.
- Nach Plan 013 hat JEDE Einheit `model_groups`; die Korrektur-UI ist nur
  relevant, wenn die Einheit VOR dem Schaden mehr als eine Gruppe mit
  lebenden Modellen hatte (synthetische Einzelgruppen-Einheiten: nichts zu
  korrigieren).
- `render_group_cards` (`_common.py:971-977`) überspringt Gruppen mit
  `alive == 0` bereits — „Waffen weg" ist dort implizit sichtbar; es fehlt
  die EXPLIZITE Anzeige im Korrektur-Moment.

## Commands you will need

| Zweck | Befehl | Erwartet |
|-------|--------|----------|
| venv | `source .venv/bin/activate` | `(.venv)` |
| Mutations-Tests | `python -m pytest tests/gameMechanic/test_unit_mutations.py -q` | grün |
| Gruppen-Tests | `python -m pytest tests/uiLayout/test_group_flow.py -q` | grün |
| Vollsuite | `pytest --tb=short` | grün, ≥80 % |

## Scope

**In scope**:
- `src/gameMechanic/unit_mutations.py` — neue Funktion `reallocate_group_losses()`
- `src/uiLayout/_common.py` — Snapshot vor Schaden + Korrektur-UI im
  Applied-Branch von `_render_damage_block`; Waffen-Wegfall-Anzeige
- Tests: `tests/gameMechanic/test_unit_mutations.py` + UI-State-Tests

**Out of scope** (NICHT anfassen):
- Tracking, in welcher Gruppe das verwundete FRONTMODELL steht
  (Mehrwunden-Einheiten): bewusste Limitation — `current_wounds` bleibt
  Unit-Level. Im Abschlussbericht als bekannte Grenze dokumentieren;
  ziel6.md nennt es „Folgefrage bei Umsetzung".
- Angreifer-seitige Sicht auf Verteidiger-Gruppen (bleibt verborgen).
- Morale-/Flee-Pfad (`flee_models` hat keine Gruppen-Reduktion — falls das
  auffällt: NUR melden, separates Thema).

## Git workflow

- Branch: `feature/014-defender-loss-allocation`.
- Commit-Stil: z. B. `Add defender loss reallocation per model group`.
- Nicht pushen/PR ohne Anweisung.

## Steps

### Step 1: Mutation `reallocate_group_losses()`

In `unit_mutations.py`:

```python
def reallocate_group_losses(
    uid: str,
    faction: str,
    losses_by_group: dict[str, int],
    group_models_before: dict[str, int],
) -> None:
    """Defender's choice: redistribute this attack's model losses across groups.

    losses_by_group must sum to the models actually lost; each group's losses
    are capped by its pre-damage count. Overwrites group_models accordingly.
    """
```

- Validierung (bei Verstoß `ValueError`): jede Gruppe `0 <= losses <=
  group_models_before[gid]`; `sum(losses_by_group.values()) ==
  sum(before) - state["models"]`-Verluste dieses Angriffs (siehe Step 2 —
  die Zahl kommt als Snapshot mit).
- Anwendung: `state["group_models"][gid] = group_models_before[gid] - losses`.
- Konsistenz-Invariante danach: `sum(group_models.values()) == state["models"]`
  (assert/Exception, nicht stilles Weiterlaufen).

**Verify**: Neue Unit-Tests (s. Test plan) grün:
`python -m pytest tests/gameMechanic/test_unit_mutations.py -q`.

### Step 2: Snapshot vor dem Schaden

`_render_damage_block`, Apply-Zweig (vor dem `apply_damage`-Aufruf, Z. 588):
`group_models_before = dict(def_state["group_models"])` und
`models_before = def_state["models"]` erfassen; beide zusätzlich in den
`res_key`-State schreiben (`"group_models_before"`, `"models_before"`).
(`def_state` via `lookup(def_faction, def_uid)` — im Apply-Zweig verfügbar
machen, falls dort bisher nur `def_unit` herumgereicht wird.)

**Verify**: Bestehende Tests grün (reine State-Erweiterung).

### Step 3: Korrektur-UI im Applied-Branch

Im Applied-Branch von `_render_damage_block` (nach der Success-Zeile, VOR
`_render_rp_block`), NUR wenn alle drei gelten:
1. `models_lost > 0`,
2. die Einheit hatte vor dem Schaden ≥ 2 Gruppen mit Modellen
   (`group_models_before`),
3. RP wurde noch nicht angewendet (`rp_{tab_key}` nicht applied — sonst
   stimmt die priority-basierte Rückgabe nicht mehr; Korrektur dann gesperrt
   mit Hinweis „Korrektur vor RP durchführen").

UI (Verteidiger-Korrektur):

```
Verluste zuweisen (Verteidiger) — 3 Modelle:
  Nob (PK+BC)      [− 2 +]   power klaw, big choppa
  Nob (2 Killsaws) [− 1 +]   2× killsaw
  [✓ Zuweisung übernehmen]
```

- Ein `st.number_input` pro Gruppe (Key `lossfix_{tab_key}_{gid}`),
  `min_value=0`, `max_value=group_models_before[gid]`, Default = die
  automatische priority-Verteilung (rekonstruierbar: `before[gid] -
  state["group_models"][gid]`).
- Caption pro Gruppe: Waffennamen (`", ".join(w.name_en for w in group.weapons)`).
- Summen-Zeile live: `zugewiesen X / Verluste Y`; Übernehmen-Button
  disabled bei `X != Y`.
- Button ruft `reallocate_group_losses(...)`; danach `st.rerun()`.
- Nach Übernahme (und auch nach der automatischen Verteilung): Gruppen, die
  durch DIESEN Angriff auf 0 fielen (`before[gid] > 0 and group_models[gid]
  == 0`), explizit ausweisen:
  `st.warning("Weggefallen: Nob (2 Killsaws) — killsaw nicht mehr verfügbar")`.

Die Korrektur bleibt bis „↺ Reset" bzw. RP-Anwendung wiederholbar (Counter
behalten ihren State; erneutes Übernehmen überschreibt ausgehend vom
Snapshot — deshalb rechnet `reallocate_group_losses` immer von
`group_models_before` aus, nie inkrementell).

**Verify**: Manuell (Streamlit): Nobz-Roster (2×PK+BC, 2×2-Killsaws) in der
Shooting Phase beschießen, 2 Modelle Verlust → Default nimmt priority-Gruppe;
Korrektur auf die Killsaw-Gruppe umverteilen → subUnitCards in der Fight
Phase zeigen die korrigierten Bestände; Warnung nennt die weggefallene Waffe.

### Step 4: RP-Wechselwirkung absichern

`_render_rp_block` wird im Applied-Branch NACH der Korrektur gerendert.
Sicherstellen (Test): Korrektur → DANN RP-Heal → `_restore_group_models`
füllt ab der neuen Verteilung nach priority auf; Invariante
`sum(group_models) == models` hält. Umgekehrt (RP zuerst) ist die Korrektur
gesperrt (Step 3, Bedingung 3).

**Verify**: Neuer Test (s. Test plan) + `pytest --tb=short` grün.

### Step 5: Vollsuite + Lint + Doku

- `pytest --tb=short` grün, ≥80 %; Lint passt.
- `docs/spec/unit_states.md`: Abschnitt „Verlust-Korrektur (P17)" mit
  Snapshot-Mechanik und RP-Sperr-Regel ergänzen.

## Test plan

- `reallocate_group_losses`: Happy Path; Summe ≠ Verluste → ValueError;
  Gruppe über `before`-Cap → ValueError; Invariante nach Anwendung.
- Default-Rekonstruktion: priority-Verteilung == `before - after`.
- Korrektur + anschließendes RP-Heal: Auffüllung konsistent.
- Synthetische Einzelgruppe (nach 013): Korrektur-UI erscheint NICHT
  (State-Test über die Render-Bedingung, Bedingung 2).
- Regressionstest Nobz-Fall: Killsaw-Gruppe auf 0 → `render_group_cards`
  bietet killsaw nicht mehr an (über `group_models`-State prüfbar).

## Done criteria

ALLE müssen gelten:

- [ ] `reallocate_group_losses` mit Validierung + Invariante; Tests grün
- [ ] Korrektur-UI: ±-Counter pro Gruppe, Default = priority, Summen-Gate,
      Waffen-Captions, Wegfall-Warnung
- [ ] Snapshot (`group_models_before`) im res-State; Korrektur wiederholbar
- [ ] RP-Sperre: nach RP keine Korrektur mehr (Hinweis statt Counter)
- [ ] `pytest --tb=short` grün, Coverage ≥ 80 %; Lint passt
- [ ] Abschlussbericht: manuelle Verifikationspunkte (Nobz-Fall Shooting +
      Fight, Einzelgruppen-Einheit ohne Korrektur-UI) + dokumentierte
      Limitation Frontmodell-Tracking
- [ ] Status-Zeile in `docs/audit/plans/README.md` aktualisiert

## STOP conditions

- Plan 013 ist nicht DONE → STOP (falscher Ausgangszustand).
- `_render_damage_block` hat nach 013 eine strukturell andere Apply-Mechanik
  (z. B. kein `res_key`-State mehr) → STOP, neu planen.
- Die UI bräuchte eine Korrektur über MEHRERE Resolution-Tabs hinweg
  (gleicher Verteidiger, mehrere Waffen): Snapshot-pro-Tab reicht dann nicht
  → melden, Designentscheidung des Nutzers.
- Mehrwunden-Einheit mit Gruppen, bei der das Frontmodell-Problem real
  auftritt (Schaden „hängt" zwischen Gruppen): dokumentieren + melden,
  NICHT improvisieren.

## Maintenance notes

- Die Korrektur arbeitet IMMER vom Snapshot aus (idempotent). Wer später
  Undo/Redo für ganze Angriffe baut, kann denselben Snapshot nutzen.
- Wenn Morale-Verluste (`flee_models`) später gruppenfähig werden, dieselbe
  Korrektur-UI wiederverwenden (Funktion ist UI-unabhängig).
