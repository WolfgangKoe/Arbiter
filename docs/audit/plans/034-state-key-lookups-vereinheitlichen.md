# Plan 034: State-Key-Lookups vereinheitlichen — Duplikat-Einheiten in Morale, Battle-Log, Melee-Liste und Wargear-Heal korrekt auflösen

> **Executor instructions**: Diesem Plan Schritt für Schritt folgen. Jedes
> Verifikations-Kommando ausführen und das Ergebnis bestätigen. Bei einer
> STOP-Bedingung: stoppen und berichten. Am Ende die Status-Zeile in
> `docs/audit/plans/README.md` aktualisieren.
>
> **Drift check (zuerst ausführen)**:
> `git diff --stat f6c464a..HEAD -- src/gameMechanic/moralePhase.py src/uiLayout/gameProtocoll.py src/gameMechanic/fightPhase.py src/gameMechanic/commandPhase.py`
> Bei Änderungen: „Current state"-Exzerpte gegen Live-Code prüfen; Abweichung → STOP.

## Status

- **Priority**: P1
- **Effort**: S
- **Risk**: LOW
- **Depends on**: none (aber NICHT parallel zu Plan 015 ausführen — beide ändern `fightPhase.py`)
- **Category**: bug
- **Planned at**: commit `f6c464a`, 2026-07-05

## Why this matters

Stellt eine Armee zwei Trupps desselben Datasheets auf, bekommen die Kopien
State-Keys mit `#N`-Suffix (`wh40k_9e.necrons.unit.warriors#1`). Vier Code-Stellen
schlagen solche State-Keys in Maps nach, die mit **bloßen** Unit-IDs gekeyt sind —
der Lookup misst, und die Stelle fällt still aus. Folgen: Der zweite Trupp wird
**nie zum Moraltest aufgefordert** (Kernmechanik still ausgesetzt), fehlt im
Deployment-Snapshot des Battle-Logs, erscheint in der Melee-Liste als roher
interner Key, und die Heal-UI eines Revive-Wargears (z. B. Resurrection Orb)
rendert bei Duplikat-Ziel nicht. Das Roster
`data/rosters/necrons_1500pts_silent_king.yaml` enthält aktuell 4 duplizierte
Einheiten — der Bug ist live.

## Current state

Kanonischer Helper (`src/gameMechanic/game_state.py:289-294`):

```python
def unit_id_from_state_key(state_key: str) -> str:
    """'wh40k_9e.necrons.unit.warriors#1' → 'wh40k_9e.necrons.unit.warriors'"""
    return state_key.split("#")[0]
```

Key-Erzeugung (`game_state.py:314-316`): erste Kopie = bloße ID, weitere = `id#N`.

**Korrektes Vorbild** (`src/uiLayout/armyCard.py:110-116`): baut `unit_by_id`
mit bloßen IDs und löst State-Keys **vor** dem Lookup auf:

```python
            if (unit := unit_by_id.get(unit_id_from_state_key(state_key))) is not None
```

Die vier fehlerhaften Stellen:

**(a)** `src/gameMechanic/moralePhase.py:48-51` baut `unit_map` mit `{u.id: u ...}`;
`_render_faction_morale` (`moralePhase.py:80-83`) iteriert dann die State-Keys:

```python
    for uid, unit_state in unit_states.items():
        unit = units.get(uid)
        if unit is None:
            continue          # ← Duplikat-Kopien (#N) werden still übersprungen
```

**(b)** `src/uiLayout/gameProtocoll.py:71-73` (`_unit_name_map`) kollabiert
Duplikate (`{u.id: u.name_en ...}`); der Deployment-Snapshot
(`gameProtocoll.py:104-110`) iteriert `names.items()` — die zweite Kopie
erscheint nie:

```python
        names = _unit_name_map(faction)
        states = _state_for(faction)
        for uid, name in names.items():
            s = states.get(uid, {})
```

**(c)** `src/gameMechanic/fightPhase.py:473-487` (`_render_melee_pairs`):
`name_map` ist bare-ID-gekeyt, `uid`/`enemy_uid` sind State-Keys:

```python
            a = name_map[p1].get(uid, uid)                      # Fallback zeigt rohen Key
            b = name_map.get(fac, {}).get(enemy_uid, enemy_uid)
```

**(d)** `src/gameMechanic/commandPhase.py:314-318` (`_render_activated_wargear`):
`target_uid` ist ein State-Key (geschrieben in `src/uiLayout/unitCard.py:269` als
`targets[_ptr.ability_id] = uid` mit `uid` = State-Key), `unit_by_id` ist
bare-ID-gekeyt:

```python
    target_uid = targets.get(request_id)
    if target_uid:
        target_unit = unit_by_id.get(target_uid)   # ← misst bei '#N'-Keys
        if target_unit:
            ... wound_adjustment_buttons(...)      # ← Heal-UI rendert nie
```

Hinweis: `commandPhase.py:186` löst an anderer Stelle bereits korrekt per
`unit_id_from_state_key(t)` auf — das Muster ist im Repo etabliert.

## Commands you will need

| Purpose | Command | Expected on success |
|---|---|---|
| Vollsuite + Coverage | `pytest --tb=short` | exit 0, Coverage ≥ 99 % |
| Lint | `ruff check src/ && black --check src/ && isort --check-only src/` | exit 0 |
| App für manuelle Prüfung | `streamlit run src/app.py` (Port 8501) | UI erreichbar |

## Scope

**In scope:**
- `src/gameMechanic/moralePhase.py` (nur Lookup in `_render_faction_morale`)
- `src/uiLayout/gameProtocoll.py` (nur Deployment-Snapshot-Schleife)
- `src/gameMechanic/fightPhase.py` (nur `_render_melee_pairs`-Lookups)
- `src/gameMechanic/commandPhase.py` (nur `target_unit`-Lookup in `_render_activated_wargear`)
- `tests/gameMechanic/test_morale_phase.py` bzw. passende bestehende Testdatei
  für Morale; `tests/uiLayout/`-Tests für die Render-Stellen (siehe Test plan)

**Out of scope:**
- Die Key-Erzeugung (`game_state.py:305-319`) — funktioniert korrekt, nicht ändern.
- `armyCard.py` — bereits korrekt.
- Alle anderen Funktionen der vier Dateien (insbesondere nichts an
  Stratagem-/HI-Logik in `fightPhase.py` — Plan 015 arbeitet dort).

## Git workflow

- Branch: `fix/034-state-key-lookups`
- Commit imperativ, Englisch, z. B. `Resolve state keys before unit map lookups for duplicate squads`
- Nicht pushen ohne Anweisung.

## Steps

### Step 1: Morale-Lookup fixen (kritischste Stelle)

In `moralePhase.py`, `_render_faction_morale`:

```python
        unit = units.get(unit_id_from_state_key(uid))
```

`unit_id_from_state_key` importieren (prüfen, was die Datei schon aus
`gameMechanic.game_state` importiert, und dort ergänzen).

**Verify**: `pytest tests/gameMechanic/ --no-cov -q` → all pass.

### Step 2: Deployment-Snapshot über States iterieren

In `gameProtocoll.py`, `_render_battle_log`, die Snapshot-Schleife umdrehen —
über `states.items()` iterieren (zeigt jede Instanz), Name per aufgelöster ID:

```python
        for uid, s in states.items():
            name = names.get(unit_id_from_state_key(uid), uid)
            deployment = s.get("deployment", "—")
            status = "DESTROYED" if s.get("destroyed") else deployment
            st.caption(f"  {name}: {status}")
```

**Verify**: `pytest --no-cov -q tests/uiLayout` → all pass.

### Step 3: Melee-Paar-Namen auflösen

In `fightPhase.py`, `_render_melee_pairs`:

```python
            a = name_map[p1].get(unit_id_from_state_key(uid), uid)
            b = name_map.get(fac, {}).get(unit_id_from_state_key(enemy_uid), enemy_uid)
```

**Verify**: `pytest --no-cov -q tests/gameMechanic` → all pass.

### Step 4: Wargear-Ziel-Lookup auflösen

In `commandPhase.py`, `_render_activated_wargear`:

```python
        target_unit = unit_by_id.get(unit_id_from_state_key(target_uid))
```

Wichtig: `wound_adjustment_buttons(...)` weiterhin mit dem **vollen State-Key**
`target_uid` aufrufen (nur der Objekt-Lookup wird aufgelöst, nicht der State-Zugriff).

**Verify**: `pytest --tb=short` → exit 0, Coverage ≥ 99 %.

### Step 5: Regressionstests (siehe Test plan), dann Vollsuite + Lint

**Verify**: `pytest --tb=short` → exit 0. `ruff check src/ && black --check src/ && isort --check-only src/` → exit 0.

## Test plan

Alle vier Fixes liegen in Render-Funktionen (coverage-ausgenommen), sind aber mit
dem etablierten Streamlit-Mock testbar — strukturelles Vorbild:
`tests/uiLayout/test_group_flow.py` (mockt `st`, baut `session_state` als Dict).
Test-Mandat des Repos: Render-Verhalten über beobachtbare Mock-Aufrufe prüfen.

1. `test_duplicate_squad_gets_morale_test` — zwei Kopien derselben Unit
   (`u1`, `u1#1`), nur `u1#1` hat Verluste → `_render_faction_morale` rendert einen
   Moraltest (beobachtbar z. B. daran, dass der „keine Tests nötig"-Zweig NICHT
   läuft bzw. `morale_test_required` für die Kopie konsultiert wird).
2. `test_deployment_snapshot_lists_duplicate_squads` — States mit `u1` und `u1#1`
   → `st.caption` wird für beide Instanzen mit dem Klarnamen aufgerufen.
3. `test_melee_pairs_show_names_for_duplicate_squads` — `melee_with`-Eintrag mit
   `u1#1` → gerenderter String enthält `name_en`, nicht `#1`.
4. `test_wargear_heal_ui_renders_for_duplicate_target` — `revive_wargear_target_uid`
   auf `u1#1` → `wound_adjustment_buttons`-Pfad wird erreicht (Mock-Aufruf sichtbar).

Zusätzlich **manuelle UI-Verifikation** (Render-Code, im Abschlussbericht nennen):
Spiel mit `necrons_1500pts_silent_king.yaml` starten → Morale-Phase mit Verlusten
beim zweiten Warriors-Trupp zeigt Test an; Battle-Log-Snapshot listet alle
Duplikate; Melee-Liste zeigt Klarnamen.

## Done criteria

- [ ] `pytest --tb=short` exit 0, Coverage ≥ 99 %
- [ ] 4 neue Regressionstests existieren und sind grün
- [ ] `grep -n "units.get(uid)" src/gameMechanic/moralePhase.py` → kein Treffer
- [ ] `git status`: nur In-Scope-Dateien geändert
- [ ] Status-Zeile in `docs/audit/plans/README.md` aktualisiert; manuelle
      UI-Prüfpunkte im Abschlussbericht gelistet

## STOP conditions

- Exzerpte stimmen nicht mit dem Live-Code überein (Drift — insbesondere falls
  Plan 015 zwischenzeitlich `fightPhase.py` umgebaut hat).
- Ein vorher grüner Test wird rot (nicht erwartet — keine Testmigrationen geplant).
- Beim Umsetzen von Step 4 stellt sich heraus, dass `wound_adjustment_buttons`
  intern ebenfalls bare-ID-Lookups macht — dann nur berichten, nicht dort
  weiterfixen (Scope-Grenze).

## Maintenance notes

- Regel für Reviewer: Jede Map `{u.id: ...}` aus `units_list_for(...)` darf nur
  über `unit_id_from_state_key(key)` mit State-Keys angesprochen werden. Bei
  neuen Lookups im Review explizit prüfen.
- Follow-up (bewusst nicht hier): ein Lint-/Architekturwächter, der
  `\.get(uid)`-Muster auf solchen Maps findet, wäre denkbar, ist aber gegen
  False-Positives schwer abzugrenzen — erst erwägen, falls das Muster erneut
  auftritt.
