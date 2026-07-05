# Plan 021 — Arkana → `faction_abilities.yaml` + Loader generisch

> **Executor instructions**: Follow this plan step by step. Run every
> verification command and confirm the expected result before moving to the
> next step. If anything in the "STOP conditions" section occurs, stop and
> report — do not improvise. When done, update the status row for this plan
> in `docs/audit/plans/README.md`.
>
> **Drift check (run first)**:
> `git diff --stat HEAD -- src/gameObjects/loader.py data/wh40k_9e/necrons/`
> Drift in `loader.py` durch Pläne 006/012 ist ERWARTET. Wenn
> `load_faction_abilities` bereits existiert oder `data.get("arkana")`
> in `load_points()` nicht mehr vorhanden ist: STOP, Nutzer informieren.

## Status

- **Priority**: P3 (NIEDRIG)
- **Effort**: S
- **Risk**: LOW
- **Depends on**: —
- **Category**: refactor + data migration (Generic src/ / INV-4)
- **Planned at**: 2026-06-20

## Why this matters

`necrons/arkana.yaml` enthält 12 Arkana-Einträge (Cryptek-Fähigkeiten),
aber der zugehörige Loader ist nicht implementiert:

- `load_arkana()` im Loader enthält nur einen Platzhalter-Kommentar
- Punktekosten werden in `load_points()` über `data.get("arkana")` gelesen —
  ein hardcodierter Key (INV-4b Schuld)
- Kein `ability_type`, kein `trigger`, kein `effect` in den YAML-Einträgen
- `loader.py` hat `"arkana"` als Literal-Key in der Allowlist

Arkana sind konzeptionell ähnlich zu anderen Fraktionsfähigkeiten (RP,
Living Metal, WAAAGH!) und passen strukturell in eine generische
`faction_abilities.yaml`, die der Loader bereits für andere Daten kennt.
Die Migration schrumpft die INV-4-Allowlist und schließt eine offene
Schuld im Loader.

## Current state

- `data/wh40k_9e/necrons/arkana.yaml` — 12 Einträge, nur Punktekosten + Name
- `src/gameObjects/loader.py` — `load_arkana()` nicht implementiert (Kommentar);
  `load_points()` liest `data.get("arkana")` mit hardcodiertem Key
- INV-4 Allowlist in `tests/architecture/` — enthält `"arkana"` als erlaubten Token
- `data/wh40k_9e/necrons/faction_abilities.yaml` — existiert bereits (WAAAGH-
  analog, Protokolle, Living Metal); Arkana fehlen

## Commands you will need

| Zweck | Befehl | Erwartet |
|-------|--------|----------|
| venv | `source .venv/bin/activate` | `(.venv)` |
| Loader-Tests | `python -m pytest tests/gameObjects/test_loader.py -q` | grün |
| Vollsuite | `pytest --tb=short` | grün, ≥ 90 % |
| Architektur-Gate | `pytest tests/architecture/ --no-cov -q` | grün |
| INV-4 prüfen | `grep -rn "arkana" src/` | kein Treffer nach Migration |

## Scope

**In scope:**
- `necrons/faction_abilities.yaml`: Arkana-Einträge hinzufügen (initial als
  `ability_type: descriptive` — Regeltext, kein Effect-Dispatch)
- `loader.py`: neue Funktion `load_faction_abilities(faction_dir)`,
  ersetzt `data.get("arkana")` in `load_points()`
- `load_points()`: Punktekosten aus `faction_abilities` lesen statt aus
  `arkana`-Sektion
- INV-4 Allowlist: `arkana`-Eintrag entfernen

**Out of scope:**
- Vollständige Effect-Engine-Integration der Arkana (eigener Plan)
- `necrons/arkana.yaml` löschen (vorerst als Quelldatei behalten, bis alle
  Daten migriert und verifiziert sind)
- Ork-/Custodes-`faction_abilities.yaml` befüllen (eigener Schritt)

## Ziel-YAML-Schema (in `faction_abilities.yaml`)

```yaml
- id: arkana_veil_of_darkness
  name_en: Veil of Darkness
  ability_type: descriptive
  category: arkana
  cost_pts: 45
  description: "Once per battle, in your Movement phase ..."
```

## Git workflow

- Branch: `feature/021-faction-abilities-arkana`.
- Commit z. B. `Migrate Arkana to faction_abilities.yaml, make loader generic`.
- Nicht pushen/PR ohne Anweisung.

## Steps

### Step 1: Arkana in `faction_abilities.yaml` migrieren

Alle 12 Arkana-Einträge aus `necrons/arkana.yaml` in
`data/wh40k_9e/necrons/faction_abilities.yaml` übertragen:
- `ability_type: descriptive`
- `category: arkana`
- Punktekosten als `cost_pts`
- Regeltext als `description` (aus `arkana.yaml` übernehmen)

**Verify**: `python -c "import yaml; d=yaml.safe_load(open('data/wh40k_9e/necrons/faction_abilities.yaml')); print(len([x for x in d if x.get('category')=='arkana']))"` → 12.

### Step 2: `load_faction_abilities(faction_dir)` implementieren

`src/gameObjects/loader.py`:

```python
def load_faction_abilities(faction_dir: str) -> list[dict]:
    """Load faction_abilities.yaml for the given faction.

    Returns an empty list if the file does not exist (not all factions
    have faction_abilities.yaml yet).
    """
```

- Nutzt `load_yaml` (Plan-006-Helper, kein rohes `yaml.safe_load`)
- Caching analog zu bestehenden Cache-Dicts (Plan 012)
- Gibt `[]` zurück wenn Datei fehlt (nicht alle Fraktionen haben die Datei)

**Verify**: `pytest tests/gameObjects/test_loader.py -q` grün.

### Step 3: `load_points()` umstellen

`load_points()` in `loader.py`: `data.get("arkana")` →
über `load_faction_abilities()` filtern nach `category: arkana` und
`cost_pts` auslesen.

**Verify**: Punktekosten-Laden für Arkana weiterhin korrekt:
`python -c "from src.gameObjects.loader import load_points; p=load_points('necrons'); print([k for k in p if 'arkana' in k.lower() or 'veil' in k.lower()])"`

### Step 4: Architektur-Gate schrumpfen

`tests/architecture/` (INV-4 Allowlist): `arkana`-Eintrag entfernen.

**Verify**: `pytest tests/architecture/ --no-cov -q` grün;
`grep -rn "\"arkana\"" src/` → kein Treffer.

### Step 5: Tests + Coverage

- Neuer Test: `load_faction_abilities("necrons")` gibt 12 Arkana zurück
- Neuer Test: Fraktion ohne `faction_abilities.yaml` → `[]` (kein Crash)
- Bestehende Punktekosten-Tests: weiterhin grün
- `pytest --tb=short` grün, Coverage ≥ 90 %

## Test plan

| Test | Kategorie |
|------|-----------|
| `test_load_faction_abilities_returns_arkana` | neuer Helper |
| `test_load_faction_abilities_missing_file_returns_empty` | Robustheit |
| Bestehende Punktekosten-Tests | Regression |
| `test_no_arkana_literal_in_src` | Architektur (INV-4b) |

## Done criteria

ALLE müssen gelten:

- [ ] `faction_abilities.yaml` für Necrons enthält alle 12 Arkana
- [ ] `loader.py` liest generisch via `load_faction_abilities()`
- [ ] Punktekosten-Laden weiterhin korrekt
- [ ] INV-4 Allowlist: kein `arkana`-Eintrag mehr
- [ ] `grep -rn "\"arkana\"" src/` → kein Treffer
- [ ] `pytest --tb=short` grün, Coverage ≥ 90 %
- [ ] Architektur-Gate grün (`pytest tests/architecture/ --no-cov -q`)
- [ ] Status-Zeile in `docs/audit/plans/README.md` aktualisiert

## STOP conditions

- Arkana brauchen sofort Effect-Dispatch (nicht nur Punktekosten) →
  eigener Plan, hier nur Migration + descriptive
- `faction_abilities.yaml`-Format inkompatibel mit bestehenden Einträgen
  (Protokolle, Living Metal) → Format-Analyse, Nutzer informieren
- Bestehende Punktekosten-Tests werden rot → STOP, Nutzer auflisten welche

## Maintenance notes

- `load_faction_abilities` ist der einzige Loader-Eintrag für
  Fraktionsfähigkeiten. Neue Fähigkeiten aller Fraktionen gehen in
  `faction_abilities.yaml` — kein neuer dedizierter Key in `load_points()`.
- `arkana.yaml` bleibt vorerst als Quelldatei; nach vollständiger Verifikation
  und stabilem Effect-Dispatch kann sie in einem Folge-Schritt entfernt werden.
