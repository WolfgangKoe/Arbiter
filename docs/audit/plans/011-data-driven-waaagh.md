# Plan 011: WAAAGH-Effekte datengetrieben auswerten (letzte ORK-Hardcodes aus `src/` entfernen)

> **Executor instructions**: Follow this plan step by step. Run every
> verification command and confirm the expected result before moving to the
> next step. If anything in the "STOP conditions" section occurs, stop and
> report — do not improvise. When done, update the status row for this plan
> in `docs/audit/plans/README.md`.
>
> **Drift check (run first)**:
> `git diff --stat 225d13b..HEAD -- src/gameMechanic/ability_engine.py src/gameMechanic/chargephase.py data/wh40k_9e/orks/faction_abilities.yaml`
> Wenn die unten zitierten Auszüge vom Live-Code abweichen: STOP.

## Status

- **Priority**: P3 (aufschiebbar — wird P1, sobald eine 4. Fraktion mit
  WAAAGH-artiger Mechanik ansteht)
- **Effort**: M
- **Risk**: MED (Verhalten muss exakt gleich bleiben; YAML-Schema wird erweitert)
- **Depends on**: none (010 empfohlen vorher; NICHT parallel zu 008 ausführen —
  beide berühren `ability_engine`-Importe in `_common.py`)
- **Category**: tech-debt
- **Planned at**: commit `225d13b`, 2026-06-11

## Why this matters

Projekt-Kernregel (CLAUDE.md): **keine Fraktionslogik in `src/`** — alle
Entscheidungen über Necrons, Orks etc. kommen aus den YAML-Daten. Plan 003 hat
den WAAAGH-Attackenbonus auf EINE Stelle zentralisiert, aber diese Stelle prüft
weiterhin hartcodiert `unit.has_keyword("ORK")`; die Charge-Phase prüft zusätzlich
hartcodiert ORK+CORE/CHARACTER. Die YAML-Daten beschreiben dieselben Effekte
bereits strukturiert (`buff_stat`/`charge_after_advance`), aber der Code liest sie
nicht — er dupliziert ihr Wissen. Eine 4. Fraktion mit ähnlicher Mechanik müsste
wieder Code anfassen. Dieser Plan macht beide Stellen zu generischen
Effekt-Auswertungen: Der Code fragt „welche aktiven Effekte gelten für diese
Einheit?", die YAML sagt, wen sie betreffen.

## Current state

**Code-Stelle 1** — `src/gameMechanic/ability_engine.py:113-116`:

```python
def waaagh_attack_bonus(faction: str, unit: Unit) -> int:
    """+1 Attacks, solange für diese Fraktion ein WAAAGH! aktiv ist und die Einheit profitiert."""
    waaagh = st.session_state.get("waaagh_state", {}).get(faction)
    return 1 if (waaagh and unit.has_keyword("ORK")) else 0
```

Drei Call-Sites, alle in `src/uiLayout/_common.py` (Funktions-lokaler Import,
`waaagh_attack_bonus(atk_faction, atk_unit)`).

**Code-Stelle 2** — `src/gameMechanic/chargephase.py:83-93`:

```python
        waaagh = st.session_state.get("waaagh_state", {}).get(faction)
        waaagh_advance_charge = (
            waaagh
            and waaagh.get("stage") == 1
            and unit.has_keyword("ORK")
            and (unit.has_keyword("CORE") or unit.has_keyword("CHARACTER"))
        )
        if not waaagh_advance_charge:
            st.warning("Advanced this turn — cannot charge.")
            return
        st.caption("WAAAGH! Stage 1 — Advance & Charge (ORKS CORE/CHARACTER).")
```

**Session-State** — `waaagh_state[faction]` wird in
`src/uiLayout/armyCard.py:371-376` gesetzt und enthält bereits die Ability-ID:

```python
            waaagh_state[faction] = {
                "stage": 1,
                "round_activated": current_round,
                "ability_id": waaagh_ability.id,
            }
```

Stage-2-Ableitung (armyCard.py:347-349): `stage_id = ability_id.replace("stage1", "stage2")`.

**Daten** — `data/wh40k_9e/orks/faction_abilities.yaml:28-85` (gekürzt):

```yaml
  - id: wh40k_9e.orks.faction.waaagh_stage1
    ability_type: activated
    effect:
      type: multi
      effects:
        - type: charge_after_advance
          target: friendly_orks_core_or_character
        - type: buff_stat
          target: friendly_orks
          stat: strength
          modifier: 1
        - type: buff_stat
          target: friendly_orks
          stat: attacks
          modifier: 1
        - type: invuln_save
          target: friendly_orks
          modifier: 5
```

Die `target`-Strings (`friendly_orks`, `friendly_orks_core_or_character`) sind
opake Marker — nichts im `src/`-Code interpretiert sie; das Wissen „ORK" bzw.
„ORK + CORE/CHARACTER" steckt stattdessen hartcodiert im Code.

**Keyword-Fakten:** `Unit.has_keyword` (unit.py:119-121) macht exakten,
case-insensitiven Vergleich. Die Ork-Einheiten tragen das Keyword `ORK`
(Singular) — der Code-Check `has_keyword("ORK")` funktioniert heute; übernimm
GENAU dieses Keyword in die YAML (Schritt 1), nicht das „ORKS" aus den Regeltexten.

## Target design

Erweiterung des Effekt-Schemas um maschinenlesbare Target-Bedingungen
(zusätzlich zum bestehenden `target`-String, der als Anzeige-/Doku-Marker bleibt):

```yaml
        - type: buff_stat
          target: friendly_orks
          target_keywords: [ORK]            # NEU: Einheit muss ALLE haben
          stat: attacks
          modifier: 1
        - type: charge_after_advance
          target: friendly_orks_core_or_character
          target_keywords: [ORK]            # NEU
          target_keywords_any: [CORE, CHARACTER]   # NEU: mindestens eines
```

Neue generische Helfer in `ability_engine.py`:

```python
def _unit_matches_target(unit: Unit, effect: dict) -> bool:
    """True if unit satisfies the effect's target_keywords / target_keywords_any."""
    required = effect.get("target_keywords", [])
    any_of = effect.get("target_keywords_any", [])
    if any(not unit.has_keyword(kw) for kw in required):
        return False
    if any_of and not any(unit.has_keyword(kw) for kw in any_of):
        return False
    return True


def active_waaagh_effects(faction: str) -> list[dict]:
    """Raw effect dicts of the faction's currently active waaagh-style ability (stage-aware)."""
```

`active_waaagh_effects` liest `st.session_state["waaagh_state"][faction]`, leitet
die Stage-ID ab (gleiches `replace("stage1", "stage2")`-Muster wie armyCard.py),
lädt die Ability über `load_faction_abilities(faction_dir)` — ABER: Abilities
sind dort bereits zu `Ability`-Objekten geparst, deren `Effect`-Dataclass die
neuen Felder nicht kennt. Siehe Step 2: Die `Effect`-Klasse braucht die
Rohdaten der Sub-Effekte. Danach:

```python
def waaagh_attack_bonus(faction: str, unit: Unit) -> int:
    total = 0
    for eff in active_waaagh_effects(faction):
        if eff.get("type") == "buff_stat" and eff.get("stat") == "attacks":
            if _unit_matches_target(unit, eff):
                total += int(eff.get("modifier", 0))
    return total


def charge_after_advance_allowed(faction: str, unit: Unit) -> bool:
    return any(
        eff.get("type") == "charge_after_advance" and _unit_matches_target(unit, eff)
        for eff in active_waaagh_effects(faction)
    )
```

`chargephase.py` ersetzt seinen Hardcode-Block durch
`charge_after_advance_allowed(faction, unit)`; der Caption-Text kommt aus den
Ability-Daten (`name_en`/`active_text`), nicht mehr als Literal.

## Commands you will need

| Zweck | Befehl | Erwartet |
|-------|--------|----------|
| venv | `source .venv/bin/activate` | `(.venv)` |
| Lint | `ruff check src/ && black --check src/ && isort --check-only src/` | passt |
| Engine-Tests | `python -m pytest tests/gameMechanic/test_ability_engine.py -q` | grün |
| WAAAGH-Tests | `python -m pytest tests/ -q -k "waaagh"` | grün |
| Vollsuite + Coverage | `pytest --tb=short` | grün, ≥80 % |

## Scope

**In scope**:
- `data/wh40k_9e/orks/faction_abilities.yaml` — `target_keywords`(`_any`) an den
  Sub-Effekten von `waaagh_stage1`, `waaagh_stage2` (und `speedwaaagh_*`, falls
  deren Effekte dieselben Marker tragen — prüfen!)
- `src/gameObjects/ability.py` + `src/gameObjects/loader.py` — NUR falls nötig,
  um die rohen Sub-Effekt-Dicts von `multi`-Effekten zugänglich zu machen (Step 2)
- `src/gameMechanic/ability_engine.py` — Helfer + Umbau `waaagh_attack_bonus`
- `src/gameMechanic/chargephase.py` — Hardcode-Block ersetzen
- `tests/gameMechanic/test_ability_engine.py` — neue Tests

**Out of scope** (NICHT anfassen):
- Die drei Call-Sites in `_common.py` — Signatur von `waaagh_attack_bonus`
  bleibt `(faction, unit) -> int`, sie merken nichts.
- +1-Strength- und Invuln-Effekte des WAAAGH — werden heute auf anderem Weg
  (armyCard/Badges, `_parse_strength`-Pfad) behandelt; NICHT in diesem Plan
  zusätzlich verdrahten.
- `armyCard.py` — Aktivierungs-UI bleibt unverändert (`ability_id` liegt schon
  im State).
- Necron-/Custodes-YAML.

## Git workflow

- Branch: `advisor/011-data-driven-waaagh`.
- Commit-Stil imperativ Englisch, z. B. `Derive WAAAGH effects from ability data`.
- Nicht pushen/PR ohne Anweisung.

## Steps

### Step 1: Annahmen verifizieren (read-only)

1. `grep -n "ORK" data/wh40k_9e/orks/units.yaml | head` — bestätige, dass
   Einheiten das Keyword `ORK` tragen (exakte Schreibweise notieren).
2. `grep -rn "waaagh_attack_bonus\|charge_after_advance" src/ tests/` — bestätige:
   genau 1 Definition + 3 Call-Sites in `_common.py` + der chargephase-Block;
   notiere bestehende Tests, die das Verhalten pinnen.
3. Lies in `src/gameObjects/ability.py` die `Effect`-Dataclass und in
   `loader.py` `_ability_from_dict`: Wie werden `multi`-Effekte geparst — sind
   die Sub-Effekt-Dicts (`effects: [...]`) nach dem Parsen noch erreichbar?

**Verify**: Schreibe die drei Antworten in deine Arbeitsnotiz. Wenn (1) ein
anderes Keyword als `ORK` ergibt oder (2) mehr Call-Sites existieren als
beschrieben: STOP.

### Step 2: Sub-Effekte zugänglich machen (nur falls nötig)

Falls `Effect` die `multi`-Sub-Effekte heute verwirft: Ergänze in der
`Effect`-Dataclass ein Feld `effects: list[dict] | None = None` und parse es in
`_ability_from_dict` mit (`d["effect"].get("effects")`). Minimal-invasiv: rohe
Dicts durchreichen, KEINE rekursiven Effect-Objekte bauen.

**Verify**: `python -m pytest tests/gameObjects/ -q` → grün.

### Step 3: YAML erweitern

Ergänze in `data/wh40k_9e/orks/faction_abilities.yaml` an jedem Sub-Effekt von
`waaagh_stage1` und `waaagh_stage2`:
- `target: friendly_orks` → zusätzlich `target_keywords: [ORK]`
- `target: friendly_orks_core_or_character` → zusätzlich
  `target_keywords: [ORK]` und `target_keywords_any: [CORE, CHARACTER]`

Prüfe `speedwaaagh_stage1/2` (ab Zeile ~87): Tragen deren Effekte dieselben
`target`-Marker, gleich mitannotieren.

**Verify**: `python -c "import yaml; yaml.safe_load(open('data/wh40k_9e/orks/faction_abilities.yaml'))"` → kein Fehler.

### Step 4: Helfer implementieren und `waaagh_attack_bonus` umbauen

Implementiere `_unit_matches_target`, `active_waaagh_effects`,
`charge_after_advance_allowed` und den neuen `waaagh_attack_bonus` wie unter
„Target design" skizziert — in `src/gameMechanic/ability_engine.py`, direkt um
die bestehende Funktion herum. Wichtig:

- `active_waaagh_effects` braucht `faction_dir` für `load_faction_abilities`:
  nutze `faction_dir_for(faction)` aus `gameMechanic.game_state` (bestehende
  Importquelle im Modul prüfen).
- Kein WAAAGH aktiv (`waaagh_state` leer) → leere Liste → Bonus 0, Charge-Gate
  False: identisch zu heute.
- Fallback-Verhalten bei Ability-Daten OHNE `target_keywords` (z. B. alte
  Custom-YAML): `_unit_matches_target` gibt dann `True` zurück (leere
  required-Liste). Das ist akzeptabel, weil `active_waaagh_effects` nur Effekte
  der per `ability_id` aktivierten Ability liefert.

**Verify**: `python -m pytest tests/ -q -k "waaagh"` → grün (bestehende
WAAAGH-Tests pinnen das Verhalten; werden sie rot → STOP).

### Step 5: `chargephase.py` umstellen

Ersetze den Block Zeilen 83–93 durch:

```python
        from gameMechanic.ability_engine import charge_after_advance_allowed  # noqa: PLC0415

        if not charge_after_advance_allowed(faction, unit):
            st.warning("Advanced this turn — cannot charge.")
            return
        st.caption("Advance & Charge active (faction ability).")
```

Für den Caption-Text: Wenn in Step 1 ein Test den exakten alten Text pinnt,
STOP und melden; andernfalls ist der generische Text gewollt (kein
Fraktions-Literal mehr in `src/`).

**Verify**: `grep -n 'has_keyword("ORK")' src/` → 0 Treffer;
`grep -rn '"WAAAGH' src/gameMechanic/chargephase.py` → 0 Treffer.

### Step 6: Tests ergänzen

In `tests/gameMechanic/test_ability_engine.py` (Strukturvorlage: die von Plan 003
ergänzten `waaagh_attack_bonus`-Tests in derselben Datei):

- `test_waaagh_bonus_zero_without_active_waaagh` (Regression)
- `test_waaagh_bonus_applies_to_ork_keyword_unit` (Stage 1 aktiv → +1)
- `test_waaagh_bonus_zero_for_non_ork_unit` (z. B. Necron-Unit → 0)
- `test_charge_after_advance_requires_core_or_character`
  (ORK ohne CORE/CHARACTER → False; ORK+CORE → True)
- `test_unit_matches_target_any_of_logic` (direkter Helfer-Test)

**Verify**: `python -m pytest tests/gameMechanic/test_ability_engine.py -q` →
grün inkl. neuer Tests.

### Step 7: Vollsuite + manuelle Prüfliste

**Verify**: `pytest --tb=short` → grün, Coverage ≥ 80 %.

Abschlussmeldung muss die manuelle UI-Prüfung nennen: **Orks-Roster laden,
WAAAGH! in der Command Phase rufen, dann: (a) Nahkampf-Deklaration zeigt +1
Attacke pro Modell, (b) advancte ORK-CORE-Einheit darf chargen, advancte
Nicht-CORE/CHARACTER-Einheit nicht, (c) nach Zugwechsel Stage 2: Bonus bleibt,
Advance&Charge nicht mehr.**

## Test plan

Siehe Step 6 — fünf neue Tests; bestehende WAAAGH-Tests (Plan 003 + Session 28)
fungieren als Verhaltens-Pins und MÜSSEN unverändert grün bleiben.

## Done criteria

ALLE müssen gelten:

- [ ] `grep -rn 'has_keyword("ORK")' src/` → 0 Treffer
- [ ] `grep -rn 'has_keyword("CORE")\|has_keyword("CHARACTER")' src/gameMechanic/chargephase.py` → 0 Treffer
- [ ] `grep -n "target_keywords" data/wh40k_9e/orks/faction_abilities.yaml` → ≥ 4 Treffer
- [ ] Neue Tests aus Step 6 vorhanden und grün; bestehende WAAAGH-Tests unverändert grün
- [ ] `pytest --tb=short` → alle grün, Coverage-Gate erfüllt
- [ ] `ruff check src/ && black --check src/ && isort --check-only src/` → passt
- [ ] Keine Dateien außerhalb der In-scope-Liste geändert (`git status`)
- [ ] Status-Zeile in `docs/audit/plans/README.md` aktualisiert
- [ ] Abschlussmeldung enthält die manuelle UI-Prüfliste aus Step 7

## STOP conditions

Stoppen und zurückmelden, wenn:

- Step 1 andere Keywords, mehr Call-Sites oder Text-pinnende Tests findet als
  beschrieben.
- Die `Effect`-Dataclass sich nicht minimal-invasiv erweitern lässt (z. B. weil
  `multi`-Effekte an anderen Stellen bereits anders entpackt werden).
- Ein bestehender WAAAGH-Test rot wird — das Verhalten ist gepinnt
  (next_session.md: „P20 Logik gepinnt"); Repo-Regel: STOP, Nutzer fragen.
- Sich herausstellt, dass auch Stage-2-/Speedwaaagh-Zustände im
  `waaagh_state` anders kodiert sind als `{"stage": 1|2, "ability_id": ...}`.

## Maintenance notes

- Damit ist das Effekt-Schema um `target_keywords`/`target_keywords_any`
  erweitert — in `docs/spec/faction_abilities.md` bzw. `loader_contract.md`
  dokumentieren (eine Zeile genügt; gehört zur Abnahme dieses Plans, wenn der
  Nutzer es wünscht).
- Die +1-Strength- und Invuln-Pfade des WAAAGH laufen weiterhin über ihre alten
  Mechanismen — ein Folge-Plan kann sie auf `active_waaagh_effects` umziehen.
- Die 4. Fraktion mit „Buff-bei-Aktivierung"-Mechanik braucht jetzt NUR noch
  YAML: `ability_type: activated` + Sub-Effekte mit `target_keywords`.
