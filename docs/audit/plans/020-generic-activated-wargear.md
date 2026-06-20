# Plan 020 — Generic Activated Wargear Flow (Resurrection Orb)

> **Executor instructions**: Follow this plan step by step. Run every
> verification command and confirm the expected result before moving to the
> next step. If anything in the "STOP conditions" section occurs, stop and
> report — do not improvise. When done, update the status row for this plan
> in `docs/audit/plans/README.md`.
>
> **Drift check (run first)**:
> `git diff --stat HEAD -- src/gameMechanic/commandPhase.py src/gameMechanic/ability_engine.py data/wh40k_9e/necrons/wargear.yaml`
> Wenn `_render_resurrection_orb` durch Plan 019 bereits teilweise umgebaut
> wurde: State-Keys prüfen — STOP wenn Naming-Convention abweicht.

## Status

- **Priority**: P2 (MITTEL)
- **Effort**: S–M
- **Risk**: MEDIUM
- **Depends on**: Plan 019 (empfohlen; State-Key-Naming muss konsistent sein)
- **Category**: refactor + feature (Generic src/ + Bug-Fix)
- **Planned at**: 2026-06-20

## Why this matters

`commandPhase.py` enthält `_render_resurrection_orb()` — eine
Necron-spezifische Renderer-Funktion mit mehreren Problemen:

1. **Hardcodierter UI-Text** `"Resurrection Orb"` (Zeile 232) — verletzt
   Generic-src/-Invariante (INV-4b).
2. **State-Key-Bug**: `revive_wargear_awaiting_target` ist nicht an die
   Orb-ID gebunden. Zwei Overlords mit Orb überschreiben gegenseitig ihren
   State — **Bug: nur einer kann pro Runde aktiviert werden**.
3. **Schema-Drift**: Necron-Wargear nutzt `max_uses: 1`, Orks nutzen
   `once_per_battle: true` — dasselbe Konzept, zwei Keys.

Ein generischer Flow, der aus `ability_type: activated` liest, löst alle
drei Probleme und macht die Infrastruktur für künftige Wargear-Abilities
(Orks, Custodes) wiederverwendbar.

## Current state

- `src/gameMechanic/commandPhase.py` — `_render_resurrection_orb()`:
  hardcodierter Name, State `revive_wargear_awaiting_target` (nicht ID-gebunden)
- `data/wh40k_9e/necrons/wargear.yaml` — `max_uses: 1` statt
  `once_per_battle: true`
- `src/gameMechanic/ability_engine.py` — kein `"heal_nearby_unit"`-Dispatcher

## Commands you will need

| Zweck | Befehl | Erwartet |
|-------|--------|----------|
| venv | `source .venv/bin/activate` | `(.venv)` |
| Orb-Tests | `python -m pytest tests/ -k "orb" -q` | grün |
| Vollsuite | `pytest --tb=short` | grün, ≥ 90 % |
| Architektur-Gate | `pytest tests/architecture/ --no-cov -q` | grün |
| INV-4b prüfen | `grep -rn "orb\|overlord\|phaeron" src/` | nur YAML-Refs, kein Literal |

## Scope

**In scope:**
- `commandPhase.py`: `_render_resurrection_orb()` →
  `_render_activated_wargear(wargear)` (liest `name_en`, `effect`,
  `once_per_battle` aus YAML)
- State-Keys: `wargear_{wargear_id}_awaiting_target`,
  `wargear_{wargear_id}_target_uid` (eindeutig je Orb-Instanz)
- `necrons/wargear.yaml`: `max_uses: 1` → `once_per_battle: true`
- `ability_engine.py`: neuer Eintrag `"heal_nearby_unit"` im
  Effect-Dispatcher
- Tests: Zwei-Overlord-Szenario, vorhandene Orb-Tests

**Out of scope:**
- Vollständige Ability-Engine-Überarbeitung
- Andere Effect-Types als `heal_nearby_unit`
- Custodes-Wargear (Daten-Nachpflege nur für Necrons hier)

## Ziel-YAML-Schema (generisch)

```yaml
ability_type: activated
conditions:
  - once_per_battle: true    # einheitlich (statt max_uses: 1)
effect:
  type: heal_nearby_unit     # generischer Effect-Type
  target: selected_unit
  within_inches: 6
```

## Git workflow

- Branch: `feature/020-generic-activated-wargear`.
- Commit z. B. `Make activated wargear flow generic, fix two-Orb state conflict`.
- Nicht pushen/PR ohne Anweisung.

## Steps

### Step 1: YAML-Migration

`data/wh40k_9e/necrons/wargear.yaml`: `max_uses: 1` → `once_per_battle: true`
für den Resurrection-Orb-Eintrag.

**Verify**: `grep "max_uses" data/wh40k_9e/necrons/wargear.yaml` → kein Treffer.

### Step 2: `_render_activated_wargear` implementieren

```python
def _render_activated_wargear(
    wargear: dict,
    unit: dict,
    faction_dir: str,
    player: str,
    state: dict,
) -> None:
    """Generic renderer for ability_type: activated wargear.

    Reads name_en, effect, once_per_battle from the wargear dict.
    State keys are namespaced by wargear id to avoid conflicts.
    """
```

- `name_en` aus `wargear` (kein Literal `"Resurrection Orb"`)
- State-Key: `wargear_{wargear["id"]}_awaiting_target`
- `once_per_battle` aus `wargear["conditions"]`

**Verify**: `grep -n "Resurrection Orb\|resurrection_orb" src/gameMechanic/commandPhase.py`
→ kein Treffer nach dem Refactoring.

### Step 3: Aufruf-Stelle umstellen

Alle Aufrufstellen von `_render_resurrection_orb()` in `commandPhase.py`
ersetzen durch `_render_activated_wargear(wargear, ...)`.

`_render_resurrection_orb` entfernen.

**Verify**: manuelle Prüfung — Orb erscheint in Command Phase, ist
deaktivierbar, bleibt nach Aktivierung verbraucht (once_per_battle).

### Step 4: Effect-Dispatcher `"heal_nearby_unit"`

`ability_engine.py`: neuer Dispatcher-Eintrag für `effect.type ==
"heal_nearby_unit"`:
- `target: selected_unit` → wirft auf die gewählte Einheit innerhalb
  `within_inches` die Heilungsmechanik
- Rückwärtskompatibel (bestehende Dispatcher-Einträge unberührt)

**Verify**: `pytest tests/gameMechanic/test_ability_engine.py -q` grün.

### Step 5: Tests + Coverage

- Bestehende Orb-Tests: weiterhin grün
- Neuer Test: Zwei Overlords mit Orb — `wargear_orb1_awaiting_target` und
  `wargear_orb2_awaiting_target` koexistieren konfliktfrei
- Neuer Test: `once_per_battle`-Flag verhindert Zweitaktivierung
- YAML-Schema-Test: `max_uses` existiert nicht mehr in `necrons/wargear.yaml`
- `pytest --tb=short` grün, Coverage ≥ 90 %

## Test plan

| Test | Kategorie |
|------|-----------|
| Bestehende Orb-Tests | Regression |
| `test_two_orb_bearers_no_state_conflict` | Bug-Fix |
| `test_once_per_battle_blocks_second_activation` | Invariante |
| `test_no_max_uses_key_in_necron_wargear` | YAML-Schema |
| `test_heal_nearby_unit_dispatcher` | Neuer Effect-Type |

## Done criteria

ALLE müssen gelten:

- [ ] `_render_resurrection_orb` entfernt, `_render_activated_wargear` an seiner Stelle
- [ ] State-Keys sind wargear-id-gebunden
- [ ] YAML: `once_per_battle: true` statt `max_uses: 1` in Necron-Wargear
- [ ] `pytest --tb=short` grün, Coverage ≥ 90 %
- [ ] Architektur-Gate grün (`pytest tests/architecture/ --no-cov -q`)
- [ ] INV-4b: `orb`/`overlord`/`phaeron` aus `commandPhase.py` entfernt
  (per `grep -n "orb\|overlord\|phaeron" src/gameMechanic/commandPhase.py`)
- [ ] Status-Zeile in `docs/audit/plans/README.md` aktualisiert

## STOP conditions

- Effect-Type `"heal_nearby_unit"` braucht umfangreichen neuen Dispatcher
  (z. B. komplexe Ziel-Validierung) → Scope abgrenzen, Nutzer informieren
- Andere Wargear-Typen in `necrons/wargear.yaml` haben inkompatibles Schema
  → melden, nicht improvisieren
- Zwei-Overlord-Szenario zeigt unerwartet weiteren State-Konflikt →
  STOP, State-Modell zeigen

## Maintenance notes

- `_render_activated_wargear` ist ab jetzt die generische Infrastruktur für
  alle `ability_type: activated`-Wargear aller Fraktionen. Neue Wargear-
  Abilities brauchen nur einen YAML-Eintrag mit `ability_type: activated`,
  `once_per_battle: true` und einem bekannten `effect.type`.
- Neue `effect.type`-Werte erfordern einen neuen Dispatcher-Eintrag in
  `ability_engine.py` — nicht in `commandPhase.py` verzweigen.
