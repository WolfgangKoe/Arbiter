# Plan 009: Modellgruppen-Auflösung härten — Duplikat-IDs mergen, unbekannte Weapon-Refs laut melden

> **Executor instructions**: Follow this plan step by step. Run every
> verification command and confirm the expected result before moving to the
> next step. If anything in the "STOP conditions" section occurs, stop and
> report — do not improvise. When done, update the status row for this plan
> in `docs/audit/plans/README.md`.
>
> **Drift check (run first)**:
> `git diff --stat 225d13b..HEAD -- src/gameObjects/loader.py`
> Wenn `_resolve_model_groups` vom unten zitierten Stand abweicht: STOP.

## Status

- **Priority**: P2
- **Effort**: S
- **Risk**: LOW
- **Depends on**: none (vor Plan 008 ausführen, der denselben Themenbereich
  in `_common.py` berührt; Konflikt gibt es aber nur in `loader.py` mit Plan 006/012 —
  diese nacheinander ausführen)
- **Category**: bug
- **Planned at**: commit `225d13b`, 2026-06-11

## Why this matters

Zwei stille Datenfehler in der Roster-Auflösung von Modellgruppen:

1. **Duplikat-Subgruppen-IDs kollidieren.** Schreibt ein Nutzer im Roster zwei
   `per_model`-Swap-Einträge mit derselben Waffenwahl (z. B. zweimal
   `{weapons: [big_shoota], count: 1}` statt einmal `count: 2`), erzeugt
   `_resolve_model_groups` zwei `ModelGroup`-Objekte mit **identischer ID**.
   Beim Initialisieren des Spielzustands kollabiert
   `{g.id: g.count for g in u.model_groups}` (`game_state.py:183`) beide zu einem
   Dict-Eintrag — eine Gruppe „verliert" ihre Modelle. Schaden- und
   Heilungs-Verrechnung (`_apply_group_losses`) iteriert anschließend über die
   Liste MIT Duplikat und zieht doppelt vom selben Key ab. Ergebnis: stille
   Divergenz der Modellzählung mitten im Spiel.

2. **Unbekannte Weapon-Refs werden still verworfen.** Ein Tippfehler in einem
   Roster-Swap (`shota` statt `shoota`) führt dazu, dass die Gruppe die Waffe
   kommentarlos nicht bekommt — `[weapon_catalog[r] for r in refs if r in weapon_catalog]`
   filtert stumm. Das widerspricht der Repo-Linie „laut scheitern"
   (vgl. Commit `7dd1f17`).

Fix: Duplikate beim Auflösen **mergen** (Nutzerintention: gleiche Waffenwahl =
gleiche Gruppe), unbekannte Refs mit klarem `ValueError` melden.

## Current state

`src/gameObjects/loader.py`, Funktion `_resolve_model_groups` (Zeilen 155–238).
Die drei relevanten Stellen:

```python
# Zeile 206-226 — per_model-Schleife: Sub-Gruppen mit IDs aus picks
            # per_model: each entry becomes a sub-group with fixed weapons
            for entry in chosen:
                picks = list(entry.get("weapons", []))[: swap.pick]
                sub_count = min(int(entry.get("count", 0)), remaining)
                if sub_count <= 0 or not picks:
                    continue
                sub_refs = _swap_weapons(spec.base_weapon_refs, swap.replaces, picks)
                pick_names = [
                    weapon_catalog[r].name_en if r in weapon_catalog else _short_ref(r)
                    for r in picks
                ]
                groups.append(
                    ModelGroup(
                        id=f"{spec.id}_{'_'.join(_short_ref(r) for r in picks)}",
                        name_en=f"{spec.name_en} ({' + '.join(pick_names)})",
                        count=sub_count,
                        weapons=[weapon_catalog[r] for r in sub_refs if r in weapon_catalog],
                        priority=spec.priority,
                    )
                )
                remaining -= sub_count
```

```python
# Zeile 228-237 — Rest-Gruppe
        if remaining > 0:
            groups.append(
                ModelGroup(
                    id=spec.id,
                    name_en=spec.name_en,
                    count=remaining,
                    weapons=[weapon_catalog[r] for r in base_refs if r in weapon_catalog],
                    priority=spec.priority,
                )
            )
    return groups
```

Stilles Filtern: Zeile 222 und Zeile 234 (`if r in weapon_catalog`) sowie der
Fallback `else _short_ref(r)` in Zeile 214.

Konsumenten der IDs:
- `src/gameMechanic/game_state.py:183` —
  `group_models: dict[str, int] = {g.id: g.count for g in u.model_groups} if u.model_groups else {}`
- `src/gameMechanic/unit_mutations.py:11-23` — `_apply_group_losses` liest/schreibt
  `group_models[group.id]` in einer Schleife über die Liste.

Bestehende Tests für Modellgruppen: `tests/gameObjects/test_loader.py`
(z. B. `test_load_roster_unit_without_groups_has_empty_model_groups`, ~Zeile 1040,
und die Gruppen-Tests ~Zeile 700–790) — als Strukturvorlage verwenden.

## Commands you will need

| Zweck | Befehl | Erwartet |
|-------|--------|----------|
| venv | `source .venv/bin/activate` | `(.venv)` |
| Lint | `ruff check src/` | passt |
| Loader-Tests | `python -m pytest tests/gameObjects/test_loader.py -q` | grün |
| Daten-Smoke-Test | `python -m pytest tests/ -q -k "roster or loader"` | grün |
| Vollsuite + Coverage | `pytest --tb=short` | grün, ≥80 % |

## Scope

**In scope**:
- `src/gameObjects/loader.py` — nur `_resolve_model_groups`
- `tests/gameObjects/test_loader.py` — neue Tests

**Out of scope** (NICHT anfassen):
- `_unit_from_dict`/`_group_weapon_ref_union` — das tolerante `weapon_catalog.get`
  beim Laden von `units.yaml` (Katalogdaten, nicht Roster) bleibt; siehe
  Maintenance notes.
- `game_state.py`/`unit_mutations.py` — nach dem Merge gibt es keine Duplikate
  mehr, die Konsumenten brauchen keine Änderung.
- `_apply_wargear`/`_apply_relic` — eigene Toleranz-Semantik, nicht Teil dieses Plans.

## Git workflow

- Branch: `advisor/009-roster-group-validation`.
- Commit-Stil imperativ Englisch, z. B.
  `Merge duplicate sub-groups and reject unknown weapon refs in roster resolution`.
- Nicht pushen/PR ohne Anweisung.

## Steps

### Step 1: Unbekannte Refs laut melden

In `_resolve_model_groups`: Ersetze die zwei stillen Filter (Zeilen 222 und 234)
durch eine Validierung. Füge dafür am Funktionsanfang (nach `if not specs: return []`)
einen kleinen lokalen Helper ein:

```python
    def _resolve_refs(refs: list[str], group_id: str) -> list[Weapon]:
        missing = [r for r in refs if r not in weapon_catalog]
        if missing:
            raise ValueError(
                f"Model group {group_id!r}: unknown weapon ref(s) {missing} "
                f"— check the roster's group_loadouts/swaps against weapons.yaml."
            )
        return [weapon_catalog[r] for r in refs]
```

Verwende ihn an beiden Stellen:
- Zeile 222: `weapons=_resolve_refs(sub_refs, spec.id),`
- Zeile 234: `weapons=_resolve_refs(base_refs, spec.id),`

Den `pick_names`-Fallback in Zeile 214 (`else _short_ref(r)`) kannst du danach
vereinfachen zu `weapon_catalog[r].name_en` — durch die Validierung von
`sub_refs` (enthält alle `picks`) ist `r` garantiert im Katalog. Vorsicht:
`_resolve_refs(sub_refs, …)` muss dafür VOR der `pick_names`-Zeile aufgerufen
werden — ordne die Zeilen entsprechend (erst `sub_refs` bauen, dann
`weapons_resolved = _resolve_refs(...)`, dann `pick_names`, dann `ModelGroup(...)`
mit `weapons=weapons_resolved`).

**Verify**: `python -m pytest tests/gameObjects/test_loader.py -q` → grün
(alle bestehenden Rosters unter `data/rosters/` haben gültige Refs — wenn hier
etwas rot wird: STOP, siehe unten).

### Step 2: Duplikat-IDs mergen

Am Ende von `_resolve_model_groups`, direkt vor `return groups`, füge die
Konsolidierung ein:

```python
    merged: dict[str, ModelGroup] = {}
    for g in groups:
        if g.id in merged:
            existing = merged[g.id]
            merged[g.id] = dataclasses.replace(existing, count=existing.count + g.count)
        else:
            merged[g.id] = g
    return list(merged.values())
```

(`dataclasses` ist in `loader.py` bereits importiert; `dict` erhält die
Einfüge-Reihenfolge, die Prioritäts-Sortierung der Konsumenten bleibt korrekt.
Bei gleicher ID sind Waffen und Name identisch — nur die Counts addieren.)

Passe die `return`-Zeile an: `return groups` → entfällt zugunsten des Blocks oben.

**Verify**: `python -m pytest tests/gameObjects/test_loader.py -q` → grün.

### Step 3: Tests ergänzen

In `tests/gameObjects/test_loader.py` (Strukturvorlage: die bestehenden
Modellgruppen-Tests derselben Datei, die `_resolve_model_groups` direkt oder via
`load_roster` aufrufen; `import pytest` ggf. ergänzen). Verwende die intern
getestete Funktion direkt — Beispielskelett:

```python
def test_duplicate_per_model_entries_merge_into_one_group() -> None:
    from gameObjects.loader import _resolve_model_groups, load_weapon_catalog
    from gameObjects.unit import ModelGroupSpec, WeaponSwapSpec

    catalog = load_weapon_catalog("orks")
    spec = ModelGroupSpec(
        id="boy",
        name_en="Boy",
        count_raw="models_max",
        base_weapon_refs=["wh40k_9e.orks.weapon.slugga", "wh40k_9e.orks.weapon.choppa"],
        weapon_swaps=[
            WeaponSwapSpec(
                id="special",
                scope="per_model",
                replaces=["wh40k_9e.orks.weapon.slugga"],
                options=["wh40k_9e.orks.weapon.big_shoota"],
                pick=1,
                limit="any",
            )
        ],
        priority=1,
    )
    loadouts = {
        "boy": {
            "swaps": {
                "special": [
                    {"weapons": ["wh40k_9e.orks.weapon.big_shoota"], "count": 1},
                    {"weapons": ["wh40k_9e.orks.weapon.big_shoota"], "count": 1},
                ]
            }
        }
    }
    groups = _resolve_model_groups([spec], 10, loadouts, catalog)
    ids = [g.id for g in groups]
    assert len(ids) == len(set(ids)), f"duplicate group ids: {ids}"
    merged = next(g for g in groups if "big_shoota" in g.id)
    assert merged.count == 2


def test_unknown_weapon_ref_in_swap_raises_clear_error() -> None:
    from gameObjects.loader import _resolve_model_groups, load_weapon_catalog
    from gameObjects.unit import ModelGroupSpec, WeaponSwapSpec

    catalog = load_weapon_catalog("orks")
    spec = ModelGroupSpec(
        id="boy",
        name_en="Boy",
        count_raw="models_max",
        base_weapon_refs=["wh40k_9e.orks.weapon.slugga"],
        weapon_swaps=[
            WeaponSwapSpec(
                id="special",
                scope="group",
                replaces=["wh40k_9e.orks.weapon.slugga"],
                options=["wh40k_9e.orks.weapon.shota_TYPO"],
                pick=1,
                limit="any",
            )
        ],
        priority=1,
    )
    loadouts = {"boy": {"swaps": {"special": {"weapons": ["wh40k_9e.orks.weapon.shota_TYPO"]}}}}
    with pytest.raises(ValueError, match="unknown weapon ref"):
        _resolve_model_groups([spec], 10, loadouts, catalog)
```

WICHTIG: Prüfe die tatsächlichen Konstruktor-Signaturen von `ModelGroupSpec` und
`WeaponSwapSpec` in `src/gameObjects/unit.py` und die echten Ork-Waffen-Ref-Strings
in `data/wh40k_9e/orks/units.yaml`, bevor du die Tests schreibst — die Skelette
oben zeigen die Struktur, nicht garantiert die exakten Feldnamen/Refs.

**Verify**: `python -m pytest tests/gameObjects/test_loader.py -q` → grün inkl.
2 neuer Tests.

### Step 4: Daten-Regression + Vollsuite

Sicherstellen, dass kein bestehendes Roster die neue Validierung auslöst:

**Verify**: `pytest --tb=short` → alle Tests grün (Baseline bei Plan-Erstellung 767,
+2 neue aus diesem Plan; durch andere abgeschlossene Pläne kann die Zahl höher liegen),
Coverage ≥ 80 %.

## Test plan

- `test_duplicate_per_model_entries_merge_into_one_group`: zwei gleiche
  per_model-Einträge → EINE Gruppe mit `count == 2`, keine Duplikat-IDs.
- `test_unknown_weapon_ref_in_swap_raises_clear_error`: Tippfehler-Ref →
  `ValueError`, Meldung nennt Gruppen-ID und fehlende Refs.
- Bestehende Gruppen-Tests (Boyz, Warbikers, Lychguard, …) bleiben grün —
  beweist, dass valide Rosters unverändert aufgelöst werden.

## Done criteria

ALLE müssen gelten:

- [ ] `grep -n "unknown weapon ref" src/gameObjects/loader.py` → 1 Treffer
- [ ] `grep -n "if r in weapon_catalog" src/gameObjects/loader.py` → 0 Treffer
  **innerhalb von `_resolve_model_groups`** (andere Funktionen unberührt)
- [ ] Merge-Block vor dem `return` vorhanden; keine zwei Gruppen mit gleicher ID
  möglich (Test beweist es)
- [ ] 2 neue Tests vorhanden und grün
- [ ] `pytest --tb=short` → alle grün, Coverage-Gate erfüllt
- [ ] `ruff check src/ && black --check src/ && isort --check-only src/` → passt
- [ ] Keine Dateien außerhalb der In-scope-Liste geändert (`git status`)
- [ ] Status-Zeile in `docs/audit/plans/README.md` aktualisiert

## STOP conditions

Stoppen und zurückmelden, wenn:

- Step 1/4 einen bestehenden Test oder ein bestehendes Roster unter
  `data/rosters/` rot macht — dann enthält ECHTE Spieldaten einen toten Ref;
  das ist ein Datenfund, den der Nutzer entscheiden muss (Daten fixen vs.
  Toleranz behalten). NICHT eigenmächtig die Daten ändern.
- `ModelGroupSpec`/`WeaponSwapSpec` andere Feldnamen haben als in den
  Test-Skeletten angenommen UND sich die Tests nicht trivial anpassen lassen.
- Der Merge die Einfüge-Reihenfolge oder `priority`-Semantik verändern würde
  (z. B. weil gleiche IDs mit UNTERSCHIEDLICHEN Waffenlisten auftauchen — das
  wäre ein tieferes Schema-Problem; melden).

## Maintenance notes

- Bewusst NICHT geändert: das tolerante `weapon_catalog.get` in
  `_unit_from_dict` (units.yaml-Pfad). Katalogdaten werden vom Maintainer
  gepflegt und vom Scraper erzeugt — dieselbe Laut-Validierung dort wäre ein
  sinnvoller Folgeschritt, hat aber größeren Blast-Radius (alle Fraktionen).
- Reviewer: prüfen, dass die Fehlermeldung Roster-Sprache spricht
  (group_loadouts/swaps), denn sie richtet sich an den YAML-Autor.
- Wenn künftig gleiche Sub-Gruppen-IDs mit unterschiedlichen Loadouts legal
  werden sollen, muss die ID-Erzeugung (Zeile 219) eindeutig gemacht werden
  (z. B. Laufindex) — dann den Merge-Block wieder entfernen.
