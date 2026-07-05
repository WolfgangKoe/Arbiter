# Plan 005: Loader-YAML pro Prozess cachen (Re-Parse bei jedem Rerun beenden)

> **Executor instructions**: Follow this plan step by step. Run every
> verification command and confirm the expected result before moving to the
> next step. If anything in the "STOP conditions" section occurs, stop and
> report — do not improvise. When done, update the status row for this plan
> in `docs/audit/plans/README.md`.
>
> **Drift check (run first)**:
> `git diff --stat c5bc891..HEAD -- src/gameObjects/loader.py`
> Wenn die unten zitierten Funktionen vom Live-Code abweichen: STOP.

## Status

- **Priority**: P3
- **Effort**: S
- **Risk**: LOW
- **Depends on**: 001 (empfohlen — Verifikations-Gates; technisch nicht zwingend)
- **Category**: perf
- **Planned at**: commit `c5bc891`, 2026-06-11

## Why this matters

Streamlit führt das gesamte Skript bei **jeder** Nutzer-Interaktion neu aus (Rerun).
`load_round_choice_abilities` öffnet und parst dabei jedes Mal `faction_abilities.yaml`
von der Platte — aufgerufen aus mehreren Render-Pfaden (`armyCard`, `gameActionsArea`,
`_common`, `ability_engine`). Dieselbe statische Datei wird so pro Interaktion mehrfach
neu geparst. Die Daten ändern sich nur bei Spielinitialisierung. Ein einfacher
Prozess-Cache (wie er im Repo bereits in `armyList._ABILITIES_CACHE` existiert) eliminiert
das wiederholte Disk-I/O.

## Current state

Datei `src/gameObjects/loader.py`:

- `load_round_choice_abilities(faction_dir)` (ab Zeile 426) liest bei jedem Aufruf:
  ```python
  def load_round_choice_abilities(faction_dir: str) -> list[CommandProtocol]:
      path = _DATA_ROOT / faction_dir / "faction_abilities.yaml"
      if not path.exists():
          return []
      with open(path) as f:
          data = yaml.safe_load(f)
      result = []
      for a in data.get("abilities", []):
          ...
      return result
  ```
- `load_round_choice_label(faction_dir)` (ab Zeile 457) liest dieselbe Datei erneut.

Bestehendes Cache-Vorbild im Repo — `src/uiLayout/armyList.py`, Zeilen 11–21:
```python
_ABILITIES_CACHE: dict[str, list] = {}

def _faction_abilities_for(faction: str) -> list:
    faction_dir = faction_dir_for(faction)
    if faction_dir not in _ABILITIES_CACHE:
        try:
            _ABILITIES_CACHE[faction_dir] = load_faction_abilities(faction_dir)
        except Exception:
            _ABILITIES_CACHE[faction_dir] = []
    return _ABILITIES_CACHE[faction_dir]
```

**Warum kein `@st.cache_data`:** `loader.py` wird in Tests **ohne** laufendes
Streamlit-Runtime importiert (`tests/gameObjects/test_loader.py` ruft die Loader direkt
auf). `@st.cache_data` setzt das Runtime voraus und würde dort warnen/scheitern. Der
Modul-Dict-Cache (wie oben) ist test-freundlich und im Repo etabliert — verwende ihn.

## Commands you will need

| Zweck   | Befehl | Erwartet |
|---------|--------|----------|
| venv    | `source .venv/bin/activate` | `(.venv)` |
| Lint    | `ruff check src/` | passt |
| Tests   | `python -m pytest tests/gameObjects/test_loader.py -q` | grün |
| Vollsuite | `python -m pytest tests/ -q` | grün |

## Scope

**In scope**:
- `src/gameObjects/loader.py` — Modul-Cache für `load_round_choice_abilities` und
  `load_round_choice_label`
- `tests/gameObjects/test_loader.py` — Cache-Test ergänzen

**Out of scope** (NICHT anfassen):
- Andere Loader-Funktionen (`load_unit_catalog`, `load_weapon_catalog`, …) — sie haben
  dasselbe Muster, aber dieser Plan begrenzt sich bewusst auf die zwei Funktionen mit den
  meisten Render-Pfad-Aufrufen. Ausweitung später separat.
- `src/uiLayout/armyList.py` — sein Cache bleibt wie er ist.

## Git workflow

- Branch: `advisor/005-cache-loader-yaml`.
- Commit-Stil imperativ Englisch, z. B. `Cache round-choice ability YAML per process`.
- Nicht pushen/PR ohne Anweisung.

## Steps

### Step 1: Modul-Cache-Dicts anlegen

Füge in `src/gameObjects/loader.py` nahe dem Modulkopf (nach den Imports / vorhandenen
Modulkonstanten) zwei Cache-Dicts hinzu:

```python
_ROUND_CHOICE_CACHE: dict[str, list] = {}
_ROUND_CHOICE_LABEL_CACHE: dict[str, str] = {}
```

**Verify**: `grep -n "_ROUND_CHOICE_CACHE" src/gameObjects/loader.py` → 1 Definitionszeile.

### Step 2: `load_round_choice_abilities` cachen

Kapsle den bestehenden Funktionskörper so, dass beim ersten Aufruf gerechnet und das
Ergebnis im Cache abgelegt wird; danach wird der Cache zurückgegeben. Die einfachste
nicht-invasive Form: Cache-Check am Funktionsanfang, Speichern am Ende.

```python
def load_round_choice_abilities(faction_dir: str) -> list[CommandProtocol]:
    """..."""  # vorhandenen Docstring beibehalten
    if faction_dir in _ROUND_CHOICE_CACHE:
        return _ROUND_CHOICE_CACHE[faction_dir]
    path = _DATA_ROOT / faction_dir / "faction_abilities.yaml"
    if not path.exists():
        _ROUND_CHOICE_CACHE[faction_dir] = []
        return _ROUND_CHOICE_CACHE[faction_dir]
    with open(path) as f:
        data = yaml.safe_load(f)
    result = []
    for a in data.get("abilities", []):
        ...  # unveränderte Schleife beibehalten
    _ROUND_CHOICE_CACHE[faction_dir] = result
    return result
```

**Verify**: `python -m pytest tests/gameObjects/test_loader.py -q` → grün (bestehende
Tests, die diese Funktion nutzen, dürfen nicht brechen).

### Step 3: `load_round_choice_label` cachen

Analog: Cache-Check am Anfang, Speichern vor jedem `return`. Achte darauf, dass **jeder**
Rückgabepfad (inkl. dem Fallback `"Round Abilities"` bei fehlender Datei) den Cache füllt.

**Verify**: `grep -n "_ROUND_CHOICE_LABEL_CACHE" src/gameObjects/loader.py` → mindestens
Definition + Lese-/Schreibzugriff.

### Step 4: Cache-Test

Ergänze in `tests/gameObjects/test_loader.py` einen Test, der belegt, dass wiederholte
Aufrufe denselben (gecachten) Wert liefern — Identität beweist den Cache:

```python
def test_round_choice_abilities_are_cached() -> None:
    first = load_round_choice_abilities("necrons")
    second = load_round_choice_abilities("necrons")
    assert first is second  # identisches Objekt → aus dem Cache


def test_round_choice_label_is_cached() -> None:
    assert load_round_choice_label("necrons") == load_round_choice_label("necrons")
```

`load_round_choice_label` ist in der Datei bereits importiert (siehe Importblock oben);
`load_round_choice_abilities` ebenfalls. Falls nicht, ergänze den Import.

**Verify**: `python -m pytest tests/gameObjects/test_loader.py -q` → grün inkl. neuer Tests.

### Step 5: Lint & Gesamtsuite

**Verify**: `ruff check src/` → passt; `python -m pytest tests/ -q` → alle grün.

## Test plan

- Zwei neue Tests in `tests/gameObjects/test_loader.py`: Identität bei `…_abilities`
  (beweist Cache), Gleichheit bei `…_label`.
- Strukturvorlage: bestehende Loader-Tests derselben Datei.
- Verifikation: `python -m pytest tests/gameObjects/test_loader.py -q` → grün.

## Done criteria

ALLE müssen gelten:

- [ ] `grep -n "_ROUND_CHOICE_CACHE" src/gameObjects/loader.py` → Definition + Nutzung
- [ ] `grep -n "_ROUND_CHOICE_LABEL_CACHE" src/gameObjects/loader.py` → Definition + Nutzung
- [ ] Test `test_round_choice_abilities_are_cached` vorhanden und grün (Identitätscheck)
- [ ] `python -m pytest tests/ -q` → alle grün
- [ ] `ruff check src/` → passt
- [ ] Keine Dateien außerhalb der In-scope-Liste geändert (`git status`)
- [ ] Status-Zeile in `docs/audit/plans/README.md` aktualisiert

## STOP conditions

Stoppen und zurückmelden, wenn:

- Bestehende Loader-Tests durch das Caching rot werden (deutet auf einen Aufrufer hin, der
  die zurückgegebene Liste **mutiert** — dann ist ein Copy-on-return statt Identität nötig,
  und der Identitätstest aus Step 4 muss angepasst werden).
- Die zitierten Funktionskörper im Live-Code abweichen.

## Maintenance notes

- Der Cache lebt für die **Prozesslaufzeit**. Da die YAML-Daten sich nur bei
  Spielinitialisierung ändern, ist das korrekt. Würde künftig YAML zur Laufzeit editierbar
  (Hot-Reload), bräuchte es eine Invalidierung (z. B. Cache nach `mtime` schlüsseln).
- Reviewer: prüfen, dass **kein** Aufrufer die von `load_round_choice_abilities`
  zurückgegebene Liste in-place mutiert (sonst kontaminiert der geteilte Cache andere
  Aufrufer). Zum Planungszeitpunkt iterieren alle Aufrufer nur lesend.
- Dasselbe Muster lässt sich später auf die übrigen Loader-Funktionen ausweiten — separater
  Plan, falls Profiling weitere Hotspots zeigt.
