# Plan 019 — UI Target Consolidation: `pending_target_request`

> **Executor instructions**: Follow this plan step by step. Run every
> verification command and confirm the expected result before moving to the
> next step. If anything in the "STOP conditions" section occurs, stop and
> report — do not improvise. When done, update the status row for this plan
> in `docs/audit/plans/README.md`.
>
> **Drift check (run first)**:
> `git diff --stat HEAD -- src/uiLayout/unitCard.py src/gameMechanic/commandPhase.py src/uiLayout/_common.py`
> Drift durch Pläne 013/014 ist ERWARTET in `_common.py`. Wenn
> `cmd_awaiting_ability_id` oder `revive_wargear_awaiting_target` strukturell
> anders aussehen als unter Current state: STOP.

## Status

- **Priority**: P2 (MITTEL)
- **Effort**: S
- **Risk**: LOW
- **Depends on**: — (kein Vorgänger zwingend)
- **Empfohlen vor**: Plan 014
- **Category**: refactor (UI-Muster konsolidieren)
- **Planned at**: 2026-06-20

## Why this matters

In der App gibt es drei fast-identische „Awaiting-Target"-Muster, die alle
denselben Flow implementieren — Quelle auswählen, Kandidaten filtern,
Button rendern — aber eigene State-Keys und eigene Branches verwenden:

1. **MWBD / Buff-Roll** (`commandPhase.py`): `cmd_awaiting_ability_id`,
   Einheiten-Filter per Keyword, Button-Rendering in `unitCard.py:218–264`
2. **Resurrection Orb** (`commandPhase.py`): `revive_wargear_awaiting_target`,
   alle außer Träger, Button-Rendering in `unitCard.py:268–281`
3. **Subgruppen-Auswahl** (Plan 014): neue Auswahl-UI für Schadenszuweisung

Außerdem nutzen Veil of Darkness (Fall 3) und Mortal-Wound-Target (Fall 8)
beide `st.selectbox` mit ähnlicher Filterlogik.

Drei Branches für denselben Ablauf bedeuten drei Stellen, die bei jeder
Änderung synchron gehalten werden müssen — Fehlerquelle und DRY-Schuld.

## Current state

- `src/uiLayout/unitCard.py:218–264` — MWBD-awaiting-Branch
- `src/uiLayout/unitCard.py:268–281` — Orb-awaiting-Branch
- `src/gameMechanic/commandPhase.py` — setzt `cmd_awaiting_ability_id` und
  `revive_wargear_awaiting_target` getrennt
- `src/uiLayout/_common.py` — Veil / Mortal-Target: zwei separate
  `st.selectbox`-Blöcke ohne gemeinsamen Helper

## Commands you will need

| Zweck | Befehl | Erwartet |
|-------|--------|----------|
| venv | `source .venv/bin/activate` | `(.venv)` |
| Ability-Tests | `python -m pytest tests/gameMechanic/test_ability_engine.py -q` | grün |
| Vollsuite | `pytest --tb=short` | grün, ≥ 90 % |
| Architektur-Gate | `pytest tests/architecture/ --no-cov -q` | grün |

## Scope

**In scope:**
- `src/uiLayout/unitCard.py`: zwei getrennte awaiting-Branches zu einem
  einzigen konsolidieren
- `src/gameMechanic/commandPhase.py`: `cmd_awaiting_*`-Keys +
  `revive_wargear_awaiting_*`-Keys → `pending_target_request`
- `src/uiLayout/_common.py`: neue Hilfsfunktion
  `render_unit_selectbox(label, candidates, state_key)` für Veil + Mortal-Target
- Tests: alle bestehenden Ability-Tests müssen weiterhin grün bleiben

**Out of scope:**
- Globale Einheitenauswahl (`selected_unit`)
- Target-Designation (`selected_targets`)
- Group-Flow (Plan 014)
- Vollständige Ability-Engine-Überarbeitung

## Ziel-Datenstruktur

```python
@dataclass
class TargetSelectionRequest:
    ability_id: str              # eindeutiger Identifier (für State-Key)
    required_keywords: list[str]  # [] = alle eligible
    exclude_uid: str | None       # Träger ausschließen
    faction_filter: str | None    # "own" | "enemy" | None
    multi: bool                   # mehrere Ziele erlaubt?
    badge_label: str              # Button-Label in der UI
```

State-Key: `pending_target_request` (ein einziger Slot ersetzt
`cmd_awaiting_*` und `revive_wargear_awaiting_*`).

## Git workflow

- Branch: `feature/019-ui-target-consolidation`.
- Commit z. B. `Consolidate awaiting-target UI to single pending_target_request`.
- Nicht pushen/PR ohne Anweisung.

## Steps

### Step 1: `TargetSelectionRequest`-Dataclass anlegen

In `src/gameObjects/game_state.py` (oder eigenem Modul, wenn Importe sauberer):

```python
@dataclass
class TargetSelectionRequest:
    ability_id: str
    required_keywords: list[str]
    exclude_uid: str | None
    faction_filter: str | None
    multi: bool
    badge_label: str
```

**Verify**: `pytest --tb=short` grün (nur Import-Rauch-Test).

### Step 2: `commandPhase.py` refactoren

MWBD-Aufruf und Orb-Aufruf nutzen beide `pending_target_request`:

- Alle `cmd_awaiting_ability_id`-Schreibstellen → `pending_target_request`
  mit passendem `TargetSelectionRequest` befüllen
- Alle `revive_wargear_awaiting_target`-Schreibstellen analog
- Lese-Stellen in `commandPhase.py` entsprechend anpassen

**Verify**: `pytest tests/gameMechanic/ --tb=short -q` grün.

### Step 3: `unitCard.py` konsolidieren

Zwei awaiting-Branches → ein Branch, der `pending_target_request` ausliest
und via `TargetSelectionRequest`-Felder filtert und rendert.

**Verify**: manuell — MWBD-Trigger zeigt Ziel-Buttons; Orb-Trigger zeigt
Ziel-Buttons; kein Rendering wenn `pending_target_request` leer.

### Step 4: `render_unit_selectbox` in `_common.py` extrahieren

```python
def render_unit_selectbox(
    label: str,
    candidates: list[dict],
    state_key: str,
) -> str | None:
    ...
```

Veil of Darkness und Mortal-Wound-Target nutzen diese Funktion statt eigener
`st.selectbox`-Blöcke.

**Verify**: manuelle Prüfung Veil + Mortal-Target (Filterung korrekt).

### Step 5: Tests + Coverage

- Bestehende MWBD-Tests: weiterhin grün
- Bestehende Orb-Tests: weiterhin grün
- Neuer Test: zwei simultane Abilities (MWBD + Orb) — kein State-Konflikt
- Neuer Test: `render_unit_selectbox` filtert candidates korrekt
- `pytest --tb=short` grün, Coverage ≥ 90 %

## Test plan

| Test | Kategorie |
|------|-----------|
| Bestehende MWBD-Tests | Regression |
| Bestehende Orb-Tests | Regression |
| `test_pending_target_request_no_state_conflict` | zwei simultane Abilities |
| `test_render_unit_selectbox_filters_candidates` | Hilfsfunktion |

## Done criteria

ALLE müssen gelten:

- [ ] `unitCard.py` hat einen einzigen awaiting-Branch
- [ ] `pending_target_request` ersetzt `cmd_awaiting_*` und `revive_wargear_awaiting_*`
- [ ] `render_unit_selectbox` extrahiert und von Veil + Mortal-Target genutzt
- [ ] `pytest --tb=short` grün, Coverage ≥ 90 %
- [ ] Architektur-Gate grün (`pytest tests/architecture/ --no-cov -q`)
- [ ] Kein neuer Fraktions-String in `src/`
- [ ] Status-Zeile in `docs/audit/plans/README.md` aktualisiert

## STOP conditions

- Mehr als 3 Dateien müssen strukturell umgebaut werden → Scope-Überprüfung,
  Nutzer informieren
- Bestehende Ability-Tests werden rot → STOP, Nutzer auflisten welche

## Maintenance notes

- `pending_target_request` ist ab jetzt der einzige Slot für
  Zielauswahl-Anforderungen. Neue Abilities, die einen Zielauswahl-Flow
  brauchen, befüllen diesen Slot — keinen neuen Key anlegen.
- `TargetSelectionRequest.faction_filter` erlaubt künftig auch gegnerische
  Ziele (z. B. Debuff-Abilities) ohne weiteren Code-Branch.
