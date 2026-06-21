# Plan 024 — Directive Wiring + Arkana Effect Modelling

> **Executor instructions**: Follow this plan step by step. Run every
> verification command and confirm the expected result before moving to the
> next step. If anything in the "STOP conditions" section occurs, stop and
> report — do not improvise. When done, update the status row for this plan
> in `docs/audit/plans/README.md`.
>
> **Drift check (run first)**:
> `git diff --stat HEAD -- src/gameMechanic/ability_engine.py data/wh40k_9e/necrons/faction_abilities.yaml`
> If `_WIRED_EFFECT_TYPES` (ability_engine.py:67) already contains
> `"strength_modifier"`, or any arkana entry no longer has
> `ability_type: descriptive` — STOP and inform the user; unexpected drift may
> mean another plan already partially implemented this work.

## Status

- **Priority**: P2 (MITTEL-HOCH — schließt eine sichtbare Lücke im Protokoll-System)
- **Effort**: M
- **Risk**: MEDIUM
- **Depends on**: Plan 021 ✅ (Arkana nach `faction_abilities.yaml` migriert)
- **Category**: feature + data modelling (Directive-Wiring + Arkana-Schema, INV-4b)
- **Planned at**: 2026-06-21 (S85, research per Sonnet-Subagent, von Opus verifiziert)

## Reframe — was hier wirklich machbar ist (Research-Befund S85)

Plan 021 markierte 12 Arkana als `ability_type: descriptive` (Stopgap). Die
Annahme hinter Plan 024 war „descriptive → echte engine-dispatchbare Effekte".
Der Research-Befund (S85, gegen `wahapedia_necrons/faction_overview.txt` geprüft)
korrigiert diese Annahme **ehrlich**.

**Wichtig — woher die Einstufung kommt:** NICHT aus der YAML. Dort sind heute
**alle 12 Arkana identische `descriptive`-Stubs** (gleiche Felder, kein
`effect`-Block) — strukturell ununterscheidbar. „Dispatchbar" folgt allein aus
dem **Regeltext** je Arkanum (wahapedia) abgeglichen gegen die **vorhandenen
Engine-Handler**. Das Schema (`trigger`/`conditions`/`effect`) wird in diesem Plan
überhaupt erst angelegt.

- **Nur 1 von 12 Arkana** (Failsafe Overcharger) ist mutmaßlich mit der heutigen
  Engine real dispatchbar — sein Regeleffekt („+1 Attacks auf eine CANOPTEK-
  Einheit") mappt auf das vorhandene `buff_stat`-Muster (`buff_stat_bonus`).
  **ANNAHME, in Step 5 zu verifizieren:** dass dieser Handler den Effekt wirklich
  trägt, ist NICHT gegen den Handler-Code geprüft (nur seine Existenz). Trägt er
  ihn nicht → STOP, Arkanum bleibt `descriptive`.
- **10 von 12 Arkana** brauchen Engine-Subsysteme, die es **nicht gibt**:
  Mortal-Wound-Handler (Atavindicator, Metalodermal Tesla Weave, Quantum Orb),
  räumliches Tracking (Hypermaterial Ablator, Prismatic Obfuscatron),
  Damage-Nullify-Hook im Save-Loop (Photonic Transubjector), Ability-Grant-Dispatch
  (Dimensional Sanctum), Meta-Ability-Targeting (Phylacterine Hive),
  Deferred-Trigger/Marker (Quantum Orb), Enemy-Direction-Modifier
  (Cryptogeometric Adjuster, Countertemporal Nanomines).
- **Cortical Subjugator Scarabs** ist *partiell* machbar (HI-Eligibility), aber
  braucht eine Unit-Auswahl — nicht in diesem Plan.

**Konsequenz für den Plan:** Der **eigentliche Gewinn ist Part B — die 9
unverdrahteten Protokoll-Direktiven** (`get_active_round_choice_modifier`
verwirft sie heute still). Das ist klar machbar, additiv und schließt die im
Backlog #2 dokumentierte Sichtbarkeitslücke. Part A (Arkana) liefert: (1) den
einen Failsafe-Overcharger-Dispatch-Pilot, (2) strukturiertes
`trigger`/`conditions`/`effect`-Schema für alle 12 (Doku/Display, keine
Dispatch-Pflicht), (3) 3 Punktkosten-Korrekturen vs. wahapedia. Die 10 nicht
dispatchbaren Arkana bleiben bewusst `descriptive` — jeweils mit Begründung.

## Why this matters

`get_active_round_choice_modifier` (ability_engine.py:70–113) gibt nur
`hit`/`wound`/`save` zurück; sein eigener Docstring sagt: „Effects for other
types … are registered in YAML but not yet wired into combat — they are silently
skipped here." Dadurch sind **9 von 12** Direktiv-Effekten unsichtbar: Hungry
Void S (Strength), Vengeful Stars S (AP), Sudden Storm P/S (Move / Advance+Charge),
Conquering Tyrant P/S (Leadership / Reroll), Eternal Guardian S (Reroll Save),
Undying Legions P/S (RP-Reroll / RP-Bonus). Die YAML-Daten existieren bereits —
nur die Engine-Brücke fehlt.

## Current state

- `src/gameMechanic/ability_engine.py:67` — `_WIRED_EFFECT_TYPES =
  {"hit_modifier", "wound_modifier", "save_modifier"}` (3 von 12 Direktiv-Typen)
- `get_active_round_choice_modifier` (70–113) → nur `{"hit","wound","save"}`;
  `strength_modifier`, `ap_bonus`, `move_bonus`, `leadership_bonus`, die beiden
  Reroll-Typen und die RP-Typen werden bei Zeile 96 still verworfen
- `charge_after_advance_allowed` (184) prüft nur `activated`-Effekte, nicht die
  aktive `round_choice`-Direktive (Sudden Storm S, `type: advance_and_charge`)
- `buff_stat_bonus` (142) existiert — Grundlage für den Failsafe-Pilot
- `faction_abilities.yaml` — 12 `category: arkana`, alle `ability_type:
  descriptive`, deutscher Freitext, kein strukturiertes `trigger/conditions/effect`
- 3 Punktkosten-Abweichungen vs. wahapedia (`faction_overview.txt`):
  `failsafe_overcharger` 30→25, `atavindicator` 25→20, `countertemporal_nanomines` 30→25

## Commands you will need

| Zweck | Befehl | Erwartet |
|-------|--------|----------|
| venv | `source .venv/bin/activate` | `(.venv)` |
| Engine-Tests | `python -m pytest tests/gameMechanic/test_ability_engine.py -q` | grün |
| Protocol-Tests | `python -m pytest tests/ -k "protocol or round_choice" -q` | grün |
| Vollsuite | `pytest --tb=short` | grün, ≥ 90 % |
| Architektur-Gate | `pytest tests/architecture/ --no-cov -q` | grün |
| INV-4b prüfen | `grep -rni "necron\|arkana\|canoptek\|dynasty\|mancer" src/gameMechanic/ability_engine.py` | nur LEGIT (Kommentar), kein Faction-Hardcoding |

## Scope

**In scope:**
- `ability_engine.py`: `_WIRED_EFFECT_TYPES` um `"strength_modifier"`,
  `"ap_bonus"`, `"move_bonus"`, `"leadership_bonus"` erweitern + Return-Zweige
  (neue Dict-Keys `strength`/`ap`/`move`/`leadership`)
- `ability_engine.py`: neue Funktion `get_active_round_choice_rerolls(faction_dir,
  phase, use_melee) -> set[str]` für die beiden Reroll-Direktiven
- `ability_engine.py`: `charge_after_advance_allowed` zusätzlich die aktive
  `round_choice`-Direktive (`advance_and_charge`) prüfen lassen
- `ability_engine.py`: neue Funktion `get_active_rp_modifiers(faction_dir) -> dict`
  (Undying Legions P/S)
- `ability_engine.py`: **Failsafe-Overcharger-Dispatch-Pilot** über das
  vorhandene `buff_stat`-Muster (`ability_type: activated`, CANOPTEK, Command-Phase)
- `faction_abilities.yaml`: strukturiertes `trigger`/`conditions`/`effect` +
  englisches `rule_text` für alle 12 Arkana; 3 Punktkosten-Korrekturen
- Tests: 4 Schichten pro Step
- `docs/spec/faction_abilities.md` + `docs/goals/backlog.md` #2 nachziehen

**Out of scope** (bleibt `descriptive`, nur Schema + `rule_text`):
- Mortal-Wound-Arkana (Atavindicator, Metalodermal Tesla Weave, Quantum Orb)
- Räumliche-/Target-Eligibility-Arkana (Hypermaterial Ablator, Prismatic Obfuscatron)
- Ability-Grant (Dimensional Sanctum), Meta-Ability (Phylacterine Hive),
  Damage-Nullify (Photonic Transubjector), Halve-Movement (Countertemporal Nanomines),
  Enemy-Direction-Hit-Debuff (Cryptogeometric Adjuster), HI-Grant (Cortical Subjugator)
- UI-Badges in den Phasen-Blöcken (Plan 016/017-Gebiet)
- Räumliches Proximity-Tracking (`within_inches` bleibt unimplementiert)
- Failsafe-Overcharger Unit-Target-Picker-UI (Pilot verdrahtet nur die Engine)
- D3-Variante (MONSTER/VEHICLE) von Failsafe Overcharger

**Generic-src (HART):** Keine Faction-Strings in `src/` — kein `"necrons"`,
`"arkana"`, `"canoptek"`, `"dynasty"`, `"…mancer"`. Alle Entscheidungen aus
YAML-Feldern (`effect.type`, `has_keywords`, `category`). INV-4b-Gate bleibt grün.

## Git workflow

- Branch: `feature/024-arkana-protocol-effect-modeling`
- Commit nach jedem Step (Step 1 ist eigenständig wertvoll)
- Kein Push/PR ohne Anweisung

## Steps

### Step 1 (PILOT): `strength_modifier`-Direktive verdrahten — end-to-end

Kleinster, sauberster Pilot: **eine** Direktive (Hungry Void S, `strength_modifier`),
additiv, gleiche Form wie das bestehende `hit_modifier`. Beweist das
Direktiv-Wiring-Muster, bevor die übrigen folgen.

**Engine** (`ability_engine.py`):
1. `"strength_modifier"` zu `_WIRED_EFFECT_TYPES` hinzufügen.
2. Return-Zweig in `get_active_round_choice_modifier`:
   ```python
   if effect_type == "strength_modifier":
       return {"strength": value}
   ```
3. Docstring aktualisieren (`strength` als möglicher Key).

**Caller:** prüfen, ob ein Konsument den `strength`-Key liest (Wound-Block in
`attack_math.py` / `_common.py`). Falls nicht: nur den Engine-Rückgabewert
verdrahten; die Anzeige-Verbindung ist Render-Code → manuelle Verifikation,
NICHT in diesem Step erzwingen (STOP-Bedingung beachten, wenn ein vorhandener
Konsument bricht).

**4-Schichten-Tests Step 1:**

| Schicht | Test | Prüft |
|---|---|---|
| Unit | `test_strength_modifier_wired_in_shooting` | Hungry Void S aktiv, phase=shooting → `{"strength": 1}` |
| Unit | `test_strength_modifier_skipped_in_melee` | `use_melee=True` → `{}` (Phasenfilter) |
| State | `test_strength_modifier_inactive_returns_empty` | keine Direktive aktiv → `{}` |
| Architektur | `tests/architecture/` (INV-4b) | kein neuer Faction-String |
| Manuell | Hungry Void S aktiv → `S+1` im Shooting-Wound-Block sichtbar |

**Verify:** `pytest tests/gameMechanic/test_ability_engine.py -q` grün;
`pytest --tb=short` grün; `pytest tests/architecture/ --no-cov -q` grün.
Commit: `Wire strength_modifier round-choice directive (Plan 024 pilot)`.

### Step 2: Restliche int-Direktiven — `ap_bonus`, `move_bonus`, `leadership_bonus`

**Engine** (`ability_engine.py`):
1. Die drei Typen zu `_WIRED_EFFECT_TYPES` hinzufügen.
2. Return-Zweige:
   ```python
   if effect_type == "ap_bonus":
       return {"ap": value}        # Vengeful Stars S: -1
   if effect_type == "move_bonus":
       return {"move": value}      # Sudden Storm P: +1
   if effect_type == "leadership_bonus":
       return {"leadership": value}
   ```
3. **`leadership_bonus`**: Morale-Phase ist nicht voll verdrahtet → rein
   informativ; `# TODO`-Kommentar setzen, NICHT an nicht-existierende UI hängen.

**4-Schichten-Tests Step 2:** `test_ap_bonus_wired_shooting`,
`test_move_bonus_wired_movement`, `test_leadership_bonus_wired`,
`test_ap_bonus_skipped_in_melee` (State), INV-4b (Architektur),
Manuell (AP-Verbesserung im SAVE-Block / Move-Badge — Render).
Commit: `Wire ap_bonus, move_bonus, leadership_bonus directives`.

### Step 3: Reroll-Direktiven + Advance+Charge

**3a. Neue Funktion** `get_active_round_choice_rerolls(faction_dir, phase,
use_melee) -> set[str]` (gleiches Session-State-Muster wie
`get_active_round_choice_modifier`; eigener Rückgabetyp `set[str]`, damit der
`dict[str,int]`-Vertrag der bestehenden Funktion sauber bleibt):
- Eternal Guardian S (`reroll_save_1`) → `{"reroll_save_1"}`
- Conquering Tyrant S (`reroll_hit_wound_1`, Melee) → `{"reroll_hit_1","reroll_wound_1"}`
- Phasenfilter wie bestehend; falscher Typ/keine Direktive → `set()`

**3b. `charge_after_advance_allowed` erweitern:** zusätzlich prüfen, ob die aktive
`round_choice`-Direktive `type: advance_and_charge` ist (Sudden Storm S). Helfer
`_active_directive_has_type(faction_dir, effect_type) -> bool` (liest Session-State,
lädt Direktive, prüft Typ — keine Faction-Strings).

**4-Schichten-Tests Step 3:** `test_reroll_save_1_eternal_guardian_s`,
`test_reroll_hit_wound_1_conquering_tyrant_s_melee`,
`test_reroll_hit_wound_skipped_in_shooting`, `test_reroll_empty_when_no_directive`,
`test_advance_and_charge_via_directive` / `…_inactive_returns_false`,
INV-4b, Manuell (Reroll-Hinweis im Save-Block; Advance+Charge in Charge-UI).
Commit: `Add get_active_round_choice_rerolls + advance_and_charge via directive`.

### Step 4: RP-Modifikatoren (Undying Legions P/S)

**Neue Funktion** `get_active_rp_modifiers(faction_dir) -> dict[str, int | bool]`:
- `rp_reroll` → `{"rp_reroll": True}`
- `rp_bonus` → `{"rp_bonus": int(value)}`
- sonst `{}`

Verdrahtung in der RP-Render (`commandPhase.py`) ist Render-Code → manuelle
Verifikation. Funktion selbst ist unit-getestet.

**4-Schichten-Tests Step 4:** `test_rp_reroll_undying_legions_p`,
`test_rp_bonus_undying_legions_s`, `test_rp_modifier_empty_when_other_directive`,
INV-4b, Manuell (RP-UI zeigt Reroll-Indikator / +1 Modell).
Commit: `Add get_active_rp_modifiers + wire Undying Legions directive`.

### Step 5: Failsafe-Overcharger-Dispatch-Pilot (einziges dispatchbares Arkanum)

**5a. Daten** — Failsafe-Overcharger-Eintrag in `faction_abilities.yaml` von
`descriptive` auf strukturiert + `activated` umstellen:
```yaml
- id: wh40k_9e.necrons.arkana.failsafe_overcharger
  name_en: Failsafe Overcharger
  ability_type: activated
  category: arkana
  source: arkana
  power_delta: 2
  cost_pts: 25          # korrigiert von 30 (wahapedia faction_overview.txt)
  rule_text: "TECHNOMANCER model only. In your Command phase, select one friendly
    CANOPTEK unit within 9\" of the bearer. Until the start of your next Command
    phase, add 1 to the Attacks characteristic of models in that unit (D3 instead
    if MONSTER or VEHICLE)."
  trigger:
    timing: phase_active
    phase: command
    player: active
  conditions:
  - has_keywords: [TECHNOMANCER]
  effect:
    type: buff_stat
    stat: attacks
    modifier: 1
    target_keywords: [CANOPTEK]
```
Die D3-Variante steht nur im `rule_text` (Doku); Dispatch-Basiswert ist `modifier: 1`.

**5b. Loader** (`loader.py`): prüfen, dass der jetzt `activated`-Eintrag von
`load_faction_abilities` NICHT herausgefiltert wird (Filter überspringt nur
`round_choice`/`descriptive`) und dass arkana-spezifische Felder (`category`,
`power_delta`, `cost_pts`) ohne Crash ignoriert werden.

**5c. Engine:** falls `buff_stat_bonus` das Muster nicht direkt abdeckt, additiven
Pfad ergänzen (kein neues Dataclass-Feld — STOP-Bedingung, falls doch nötig).

**4-Schichten-Tests Step 5:** `test_failsafe_overcharger_loaded_as_activated`
(Unit), `test_failsafe_overcharger_buff_stat_applied` (State/Acceptance —
`buff_stat_bonus("necrons", canoptek_unit, "attacks") == 1`), INV-4b,
Manuell (Failsafe Overcharger in Command-Phase aktivierbar via
`_render_activated_wargear`). **STOP**, falls Dispatch ein neues Ability/Effect-
Dataclass-Feld braucht.
Commit: `Add Failsafe Overcharger dispatch pilot (buff_stat)`.

### Step 6: Strukturiertes Schema + Punktkosten für die übrigen 11 Arkana

**6a. Punktkosten** (Daten, Null-Risiko): `atavindicator` 25→20;
`countertemporal_nanomines` 30→25 (Failsafe in Step 5 erledigt).

**6b. Strukturiertes Schema:** für jeden noch `descriptive`-Eintrag deutschen
`description`-Freitext durch englisches `rule_text:` ersetzen und
`trigger`/`conditions`/`effect` ergänzen (Schema je Arkanum aus dem Research-Digest
in der Session-Notiz / diesem Plan). **Dispatch ändert sich NICHT** — diese bleiben
`descriptive`; das Schema dient Doku + künftiger UI-Anzeige der Bedingungen.

**4-Schichten-Tests Step 6:** `test_all_arkana_have_rule_text`,
`test_all_arkana_have_trigger`, `test_arkana_point_costs_match_wahapedia`
(atavindicator=20, failsafe=25, nanomines=25),
`test_descriptive_arkana_not_dispatched` (State — `load_faction_abilities`
enthält keinen `descriptive`-Eintrag), INV-4b, Manuell (`rule_text` statt
deutschem Freitext im Display).
Commit: `Add structured schema + fix point costs for remaining arkana`.

### Step 7: Vollsuite + Lint + Doku

- `pytest --tb=short` grün, ≥ 90 %; `pytest tests/architecture/ --no-cov -q` grün
- `ruff check src/ && black --check src/ && isort --check-only src/` sauber
- `docs/spec/faction_abilities.md`: Direktiv-Wiring ✅; auflisten welche Arkana
  warum `descriptive` bleiben
- `docs/goals/backlog.md` #2 (Protokoll-Buff-Audit) Direktiven abhaken; INV-4b
  Cluster 6 Dispatch-Status notieren
- Status-Zeile in `docs/audit/plans/README.md` aktualisieren

## Test plan (Zusammenfassung)

| Test | Step | Schicht |
|---|---|---|
| `test_strength_modifier_wired_in_shooting` / `…_skipped_in_melee` / `…_inactive_returns_empty` | 1 | Unit/State |
| `test_ap_bonus_wired_shooting` / `test_move_bonus_wired_movement` / `test_leadership_bonus_wired` / `test_ap_bonus_skipped_in_melee` | 2 | Unit/State |
| `test_reroll_save_1_eternal_guardian_s` / `…_hit_wound_1_…_melee` / `…_skipped_in_shooting` / `…_empty_when_no_directive` | 3 | Unit |
| `test_advance_and_charge_via_directive` / `…_inactive_returns_false` | 3 | Unit |
| `test_rp_reroll_undying_legions_p` / `test_rp_bonus_undying_legions_s` / `…_empty_when_other_directive` | 4 | Unit/State |
| `test_failsafe_overcharger_loaded_as_activated` / `…_buff_stat_applied` | 5 | Unit/State |
| `test_all_arkana_have_rule_text` / `…_have_trigger` / `…_point_costs_match_wahapedia` / `test_descriptive_arkana_not_dispatched` | 6 | Unit/State |
| `test_generic_src_vocab` (bestehendes INV-4b-Gate) | alle | Architektur |
| Manuell: Strength/AP/Move/Reroll/RP-Anzeigen + Failsafe aktivierbar | 1–6 | Manuell |

## Done criteria

ALLE müssen gelten:

- [ ] `_WIRED_EFFECT_TYPES` enthält `strength_modifier`, `ap_bonus`, `move_bonus`, `leadership_bonus`
- [ ] `get_active_round_choice_modifier` liefert `strength`/`ap`/`move`/`leadership` für die jeweiligen Direktiven
- [ ] `get_active_round_choice_rerolls` existiert + korrekte Flags (Eternal Guardian S, Conquering Tyrant S)
- [ ] `charge_after_advance_allowed` True bei aktiver Sudden-Storm-S-Direktive
- [ ] `get_active_rp_modifiers` existiert + korrekte Dicts (Undying Legions P/S)
- [ ] Failsafe Overcharger `ability_type: activated`, lädt, `buff_stat` dispatcht
- [ ] 12 Arkana mit strukturiertem `trigger`/`conditions`/`effect` + englischem `rule_text`
- [ ] 3 Punktkosten korrigiert (atavindicator 20, failsafe 25, nanomines 25)
- [ ] 10 nicht dispatchbare Arkana bleiben `descriptive` (begründet)
- [ ] alle neuen Tests grün; `pytest --tb=short` grün, ≥ 90 %
- [ ] INV-4b-Gate grün; keine neuen Faction-Strings in `src/`
- [ ] `ruff`/`black`/`isort` sauber
- [ ] `faction_abilities.md` + `backlog.md` #2 + Plans-README aktualisiert

## STOP conditions

- **Ein vorher grüner Konsument bricht**, wenn ein neuer Modifier-Key
  (`strength`/`ap`/`move`/`leadership`) zurückkommt → STOP, failing Tests
  auflisten, fragen ob Verhaltensänderung beabsichtigt (CLAUDE.md-Sicherheitsnetz).
- **Failsafe-Dispatch braucht ein neues `Ability`/`Effect`-Dataclass-Feld** (nicht
  nur additive optionale YAML-Felder) → STOP, eigener Design-Entscheid.
- **Ein Arkanum-Effekt ist nicht mal als strukturiertes Schema abbildbar** → STOP,
  als reines `descriptive` + `rule_text` belassen.
- **Ein Arkanum bräuchte einen neuen `execute_effect`-Handler im Combat-Resolution**
  (z. B. Mortal-Wound/Damage-Nullify) → STOP, bleibt `descriptive` (out of scope).
- **INV-4b-Gate wird rot** (neuer Faction-String in `src/`) → STOP sofort, entfernen.
- **Coverage < 90 %** → STOP, Tests ergänzen vor Commit.

## Maintenance notes

- `_WIRED_EFFECT_TYPES` ist die autoritative Liste der numerischen
  Direktiv-Effekttypen. Ein neuer Eintrag hier wirkt automatisch für jede
  Fraktion mit `round_choice`-Direktiven — kein fraktionsspezifischer Code.
- `get_active_round_choice_rerolls` / `get_active_rp_modifiers` folgen demselben
  Session-State-Muster wie `get_active_round_choice_modifier`. Diese drei
  Funktionen sind die kanonische Abfrage-Oberfläche für Protokoll-Effekte —
  Konsumenten lesen NICHT direkt aus Session-State.
- Die 10 `descriptive`-Arkana warten auf Engine-Fähigkeiten (Mortal-Wound-Handler,
  Proximity-Tracking, Ability-Grant-Dispatch, Deferred-Trigger, Meta-Ability,
  Enemy-Direction-Modifier). Sobald eine davon (eigener Plan) existiert, kann der
  betreffende Arkana-Eintrag aufgewertet werden — ohne `src/` anzufassen.
- Failsafe-Overcharger-D3-Variante (MONSTER/VEHICLE) später: Feld
  `monster_vehicle_modifier: D3` in den YAML-`effect`-Block + `execute_effect`
  prüft `target_unit.has_keyword(...)` — alles aus YAML, keine Faction-Strings.
