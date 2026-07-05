# Plan 003: WAAAGH-Angriffsbonus in einen Helper zentralisieren

> **Executor instructions**: Follow this plan step by step. Run every
> verification command and confirm the expected result before moving to the
> next step. If anything in the "STOP conditions" section occurs, stop and
> report — do not improvise. When done, update the status row for this plan
> in `docs/audit/plans/README.md`.
>
> **Drift check (run first)**:
> `git diff --stat c5bc891..HEAD -- src/uiLayout/_common.py src/gameMechanic/ability_engine.py`
> Bei Abweichung der unten zitierten Stellen vom Live-Code: STOP.

## Status

- **Priority**: P2
- **Effort**: S
- **Risk**: LOW
- **Depends on**: 001 (empfohlen — Verifikations-Gates; technisch nicht zwingend)
- **Category**: tech-debt
- **Planned at**: commit `c5bc891`, 2026-06-11

## Why this matters

Die WAAAGH!-Angriffsbonus-Berechnung steht **wortgleich an drei Stellen** in
`src/uiLayout/_common.py`. Jede prüft `atk_unit.has_keyword("ORK")` — eine
fraktionsspezifische Keyword-Abfrage, die laut `CLAUDE.md` (Prinzip „Generic src/")
nicht in der UI-Schicht verstreut sein soll. Ändert sich die WAAAGH-Regel, müssen
drei identische Zeilen synchron angefasst werden; vergisst man eine, driften sie.
Dieser Plan führt **eine** Helper-Funktion ein und ersetzt die drei Duplikate — die
Keyword-Regel lebt danach an genau einer Stelle. (Die vollständige Datengetriebenheit
— den String `"ORK"` ganz aus `src/` zu entfernen — ist ein größerer, riskanterer
Umbau und bewusst **nicht** Teil dieses Plans.)

## Current state

Datei `src/uiLayout/_common.py` — drei identische Vorkommen:

- Zeilen 1442–1443 (in `render_group_flow_attacker`-artiger Owner-Render-Funktion):
  ```python
      waaagh = st.session_state.get("waaagh_state", {}).get(atk_faction)
      waaagh_bonus = 1 if (waaagh and atk_unit.has_keyword("ORK")) else 0
  ```
- Zeilen 1553–1554 (Gruppen-Zusammenfassung):
  ```python
      waaagh = st.session_state.get("waaagh_state", {}).get(atk_faction)
      waaagh_bonus = 1 if (waaagh and atk_unit.has_keyword("ORK")) else 0
  ```
- Zeilen 1788–1789 (Attack-Resolution, eingerückt unter `if first_melee_profiles:`):
  ```python
              waaagh = st.session_state.get("waaagh_state", {}).get(atk_faction)
              waaagh_bonus = 1 if (waaagh and atk_unit.has_keyword("ORK")) else 0
  ```

In allen drei Funktionen heißen die Variablen `atk_faction` (str) und `atk_unit` (Unit).

Ziel-Heimat des Helpers: `src/gameMechanic/ability_engine.py`. Diese Datei importiert
bereits `streamlit as st` und `from gameObjects.unit import Unit` und ist die richtige
Schicht für Fähigkeits-Logik.

**Import-Konvention im Repo:** `src/uiLayout/_common.py` importiert aus `gameMechanic`
durchgängig **funktions-lokal** (innerhalb der Funktion, mit `# noqa: PLC0415`), um
zirkuläre Importe zu vermeiden — z. B. in `_render_rp_block`:
`from gameMechanic.game_state import faction_dir_for  # noqa: PLC0415`.
Folge dieser Konvention; importiere den Helper **nicht** auf Modulebene in `_common.py`.

## Commands you will need

| Zweck   | Befehl | Erwartet |
|---------|--------|----------|
| venv    | `source .venv/bin/activate` | `(.venv)` |
| Lint    | `ruff check src/` | passt |
| Format  | `black --check src/` | passt |
| Tests (Engine) | `python -m pytest tests/gameMechanic/test_ability_engine.py -q` | grün |
| Vollsuite | `python -m pytest tests/ -q` | grün |
| Grep    | `grep -rn 'has_keyword("ORK")' src/uiLayout/` | nach Fix: 0 Treffer |

## Scope

**In scope**:
- `src/gameMechanic/ability_engine.py` — Helper `waaagh_attack_bonus` hinzufügen
- `src/uiLayout/_common.py` — die drei `waaagh_bonus = …`-Zeilen ersetzen
- `tests/gameMechanic/test_ability_engine.py` — Tests für den Helper

**Out of scope** (NICHT anfassen):
- `src/gameMechanic/chargephase.py:87` — das `has_keyword("ORK")` dort ist Teil einer
  zusammengesetzten Bedingung (`waaagh_advance_charge`) mit anderer Form; separater Fall.
- `src/uiLayout/_common.py:935` — der Necron-RP-Gate `fdir.startswith("necron")`; anderes
  Finding, anderer Fix.
- Den String `"ORK"` ganz aus `src/` entfernen / Daten-Schema ändern — größerer Umbau.

## Git workflow

- Branch: `advisor/003-centralize-waaagh-bonus`.
- Commit-Stil imperativ Englisch, z. B. `Centralize WAAAGH attack bonus into one helper`.
- Nicht pushen/PR ohne Anweisung.

## Steps

### Step 1: Helper in `ability_engine.py` anlegen

Füge in `src/gameMechanic/ability_engine.py` eine neue Funktion hinzu (z. B. direkt
nach `get_active_protocol_modifier`, vor `get_activated_command_abilities`):

```python
def waaagh_attack_bonus(faction: str, unit: Unit) -> int:
    """+1 Attacks, solange für diese Fraktion ein WAAAGH! aktiv ist und die Einheit profitiert.

    Zentralisiert die zuvor an mehreren UI-Stellen duplizierte Berechnung.
    """
    waaagh = st.session_state.get("waaagh_state", {}).get(faction)
    return 1 if (waaagh and unit.has_keyword("ORK")) else 0
```

`st` und `Unit` sind in dieser Datei bereits importiert — keine neuen Modul-Importe nötig.

**Verify**: `python -c "import sys; sys.path.insert(0,'src'); from unittest.mock import MagicMock; sys.modules['streamlit']=MagicMock(); from gameMechanic.ability_engine import waaagh_attack_bonus; print('ok')"` → `ok`.

### Step 2: Die drei Duplikate in `_common.py` ersetzen

Ersetze an **jeder** der drei Stellen NUR die `waaagh_bonus = …`-Zeile durch einen
Aufruf des Helpers, mit funktions-lokalem Import unmittelbar davor. Die vorhandene
`waaagh = st.session_state.get(...)`-Zeile **bleibt unverändert stehen** (sie wird in
diesen Funktionen ggf. noch für Anzeigezwecke gebraucht — nicht entfernen).

Aus:
```python
    waaagh = st.session_state.get("waaagh_state", {}).get(atk_faction)
    waaagh_bonus = 1 if (waaagh and atk_unit.has_keyword("ORK")) else 0
```
wird:
```python
    waaagh = st.session_state.get("waaagh_state", {}).get(atk_faction)
    from gameMechanic.ability_engine import waaagh_attack_bonus  # noqa: PLC0415

    waaagh_bonus = waaagh_attack_bonus(atk_faction, atk_unit)
```

Achte bei der dritten Stelle (Zeilen 1788–1789) auf die tiefere Einrückung (sie steht
innerhalb `if first_melee_profiles:`); Import und Zuweisung entsprechend einrücken.

**Verify**:
- `grep -rn 'has_keyword("ORK")' src/uiLayout/` → **0 Treffer**
- `grep -rn "waaagh_attack_bonus" src/uiLayout/_common.py` → **3 Treffer** (je ein Aufruf)

### Step 3: Formatierung & Lint

`black src/uiLayout/_common.py src/gameMechanic/ability_engine.py` (formatiert ggf. die
neuen Import-/Leerzeilen). Dann:

**Verify**: `ruff check src/` → passt; `black --check src/` → passt.

### Step 4: Tests für den Helper

Ergänze in `tests/gameMechanic/test_ability_engine.py` Tests. Die Datei mockt Streamlit
bereits (`sys.modules["streamlit"] = MagicMock()`, als Modul-Alias `_eng.st`) und hat
einen `_make_unit(rules, keywords)`-Helper. Setze `st.session_state` als echtes Dict:

```python
from gameMechanic.ability_engine import waaagh_attack_bonus  # noqa: E402


def test_waaagh_bonus_one_for_ork_with_active_waaagh() -> None:
    _eng.st.session_state = {"waaagh_state": {"Orks": {"stage": 1}}}
    unit = _make_unit(rules=[], keywords=["ORK", "CORE"])
    assert waaagh_attack_bonus("Orks", unit) == 1


def test_waaagh_bonus_zero_without_active_waaagh() -> None:
    _eng.st.session_state = {"waaagh_state": {}}
    unit = _make_unit(rules=[], keywords=["ORK"])
    assert waaagh_attack_bonus("Orks", unit) == 0


def test_waaagh_bonus_zero_for_non_ork_unit() -> None:
    _eng.st.session_state = {"waaagh_state": {"Necrons": {"stage": 1}}}
    unit = _make_unit(rules=[], keywords=["NECRON"])
    assert waaagh_attack_bonus("Necrons", unit) == 0
```

**Verify**: `python -m pytest tests/gameMechanic/test_ability_engine.py -q` → grün
inkl. der drei neuen Tests.

### Step 5: Gesamte Suite

**Verify**: `python -m pytest tests/ -q` → alle grün.

## Test plan

- Drei neue Tests in `tests/gameMechanic/test_ability_engine.py`:
  ORK + aktives WAAAGH → 1; ORK ohne WAAAGH → 0; Nicht-ORK → 0.
- Strukturvorlage: bestehende Tests derselben Datei (`_make_unit`, `_eng.st.session_state`).
- Verifikation: `python -m pytest tests/gameMechanic/test_ability_engine.py -q` → grün.

## Done criteria

ALLE müssen gelten:

- [ ] `grep -n "def waaagh_attack_bonus" src/gameMechanic/ability_engine.py` → 1 Treffer
- [ ] `grep -rn 'has_keyword("ORK")' src/uiLayout/` → **0 Treffer**
- [ ] `grep -rn "waaagh_attack_bonus" src/uiLayout/_common.py` → 3 Treffer
- [ ] `ruff check src/` und `black --check src/` → beide passen
- [ ] 3 neue Tests vorhanden und grün
- [ ] `python -m pytest tests/ -q` → alle grün
- [ ] Keine Dateien außerhalb der In-scope-Liste geändert (`git status`)
- [ ] Status-Zeile in `docs/audit/plans/README.md` aktualisiert

## STOP conditions

Stoppen und zurückmelden, wenn:

- Eine der drei `_common.py`-Stellen **nicht** exakt dem zitierten Doppelzeilen-Muster
  entspricht (Codebase gedriftet).
- Das Entfernen/Ersetzen einer Zeile einen `NameError` für `atk_faction`/`atk_unit`
  auslöst — die Variablennamen weichen in einer Funktion ab; dann melde welche.
- Tests rot werden, weil `_eng.st.session_state` in der Testdatei anders gehandhabt wird
  als hier angenommen — melde das Setup, statt es umzubauen.

## Maintenance notes

- Dies ist die **scoped** Variante des Audit-Findings #3. Verbleibende Fraktions-Leaks
  (chargephase ORK-Bedingung, Necron-RP-Gate, der hartcodierte `"ORK"`-String im Helper)
  sind bewusst offen — ein späterer datengetriebener Umbau sollte `waaagh_attack_bonus`
  intern auf Fähigkeitsdaten umstellen, ohne die drei Call-Sites erneut anzufassen.
- Reviewer: prüfen, dass keine `waaagh`-Variable durch das Stehenlassen tatsächlich tote
  Logik erzeugt; falls eine Stelle `waaagh` nirgends sonst nutzt, kann die Zeile in einem
  Folge-Commit entfernt werden.
