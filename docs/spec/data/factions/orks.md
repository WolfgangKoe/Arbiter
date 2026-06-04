# Orks — Datendokumentation

> Stand: 2026-06-04 | Quelle: Wahapedia WH40k 9E

---

## WAAAGH! (`activated`)

3 Varianten in `faction_abilities.yaml`, alle `ability_type: activated`, `phase: command`:

| ID | Name | Aktivator-Keyword | Effekt |
|----|------|-------------------|--------|
| `waaagh_stage1` | Waaagh! — Call Da Waaagh! | WARBOSS | +1 S+A, 5++ für ORKS; Angriff nach Vorrücken |
| `waaagh_stage2` | Waaagh! — Get Stuck In! | auto | +1 S+A, 6++ für ORKS (Folgerunde) |
| `speedwaaagh_stage1` | Speedwaaagh! — Da Big Race | SPEEDBOSS | Assault nach Advance, +Dakka-Treffer, +AP |

UI: `armyCard._render_waaagh_ui()` — generisch via `command_activated`-Filter.

---

## Triggered Abilities (`faction_abilities.yaml`)

| ID | Name | Condition |
|----|------|-----------|
| `ere_we_go` | 'Ere We Go | `has_rules: [ereWeGo]` |

---

## Objective Secured (Sonderfall)

> **Wichtig:** ObjSec ist bei Orks *nicht* in `faction_abilities.yaml`, sondern in `unit_abilities.yaml`.  
> Grund: GRETCHIN-Ausnahme — die Shared-Version kennt diese Einschränkung nicht.

In `unit_abilities.yaml`:
```yaml
- id: wh40k_9e.orks.unit.objective_secured
  shared_ref: wh40k_9e.shared.objective_secured
  conditions:
    - has_rules: [objectiveSecured]
    - not_has_keywords: [GRETCHIN]
```

---

## Psychic Powers (`powers.yaml`)

7 Kräfte der Waaagh!-Energy-Disziplin (Batch 3 Migration aus `faction_abilities.yaml`):

| ID | Name | Warp Charge | Bedingung |
|----|------|-------------|-----------|
| `smite` | Smite | 5 | `shared_ref: wh40k_9e.shared.power.smite` |
| `eadbanger` | 'Eadbanger | 5 | PSYKER + WEIRDBOY |
| `warpath` | Warpath | 6 | PSYKER + WEIRDBOY |
| `da_jump` | Da Jump | 7 | PSYKER + WEIRDBOY |
| `fists_of_gork` | Fists of Gork | 6 | PSYKER + WEIRDBOY |
| `da_krunch` | Da Krunch | 6 | PSYKER + WEIRDBOY |
| `jabbinfinger` | Jabbin' Fingerz | 6 | PSYKER + WEIRDBOY |

Loader: noch nicht verdrahtet — reine Datenmigration.

---

## Unit Abilities (`unit_abilities.yaml`)

Auswahl wichtiger Einträge:

| ID | Einheit | Fähigkeit |
|----|---------|-----------|
| `warboss.call_da_waaagh` | Warboss | Aktiviert waaagh_stage1 |
| `warboss_warbike.call_da_speedwaaagh` | Warboss on Warbike | Aktiviert speedwaaagh_stage1 |
| `ghazghkull.great_waaagh` | Ghazghkull | Kombiniert beide WAAGHs |
| `weirdboy.waaagh_energy` | Weirdboy | Kennt 2 Powers + Smite |
| `weirdboy.waaagh_juice` | Weirdboy | +2 Psychic Test wenn WAAAGH! ausgerufen |
| `mob_rule` | Keyword | Morale-Immunität bei nahen Mobs |
| `ramshackle` | Keyword | Damage -1 für S<8-Angriffe |
| `beast_snagga` | Keyword | +1 Hit vs VEHICLE/MONSTER, 6++ |
