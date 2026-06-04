# _shared/ — Fraktionsübergreifende Daten

> Stand: 2026-06-04

Alle Dateien unter `data/wh40k_9e/_shared/` gelten für jede Fraktion ohne Einschränkung.

---

## stratagems.yaml — Core Stratagems (verdrahtet)

Geladen via `load_stratagems(faction_dir)` — immer zuerst, dann Fraktions-Stratagems.  
IDs: `wh40k_9e.shared.stratagem.*`

| ID | Name | CP | Phase |
|----|------|----|-------|
| `command_re_roll` | Command Re-Roll | 1 | any |
| `cut_them_down` | Cut Them Down | 1 | movement |
| `desperate_breakout` | Desperate Breakout | 2 | movement |
| `emergency_disembarkation` | Emergency Disembarkation | 1 | any |
| `fire_overwatch` | Fire Overwatch | 1 | charge |
| `counter_offensive` | Counter-Offensive | 2 | fight |
| `insane_bravery` | Insane Bravery | 2 | morale |

---

## shared_abilities.yaml — Universalregeln (Stub, nicht verdrahtet)

IDs: `wh40k_9e.shared.*`

| ID | Name | Keyword/Condition |
|----|------|------------------|
| `objective_secured` | Objective Secured | `has_rules: [objectiveSecured]` |
| `deep_strike` | Deep Strike | `has_rules: [deepStrike]` |
| `fly` | Fly | `has_keywords: [FLY]` |
| `feel_no_pain` | Feel No Pain | `has_rules: [feelNoPain]` |
| `big_guns_never_tire` | Big Guns Never Tire | `has_keywords: [VEHICLE, MONSTER]` |
| `look_out_sir` | Look Out, Sir | `has_keywords: [CHARACTER]`, `max_wounds: 9` |
| `heroic_intervention` | Heroic Intervention | `has_keywords: [CHARACTER]` |

**Hinweis ObjSec:** Orks haben eine eigene Variante in `unit_abilities.yaml` mit `not_has_keywords: [GRETCHIN]` und `shared_ref: wh40k_9e.shared.objective_secured`.

---

## shared_powers.yaml — Psionische Grundregeln (Stub, nicht verdrahtet)

IDs: `wh40k_9e.shared.power.*`

| ID | Name | Type | Warp Charge |
|----|------|------|-------------|
| `smite` | Smite | psychic | 5 (+1 pro weitere Smite der Armee) |
| `deny_the_witch` | Deny the Witch | deny | — |
| `perils_of_the_warp` | Perils of the Warp | psychic | auto (Doppel-1/6) |

---

## detachment_types.yaml — Detachment-Typen (verdrahtet)

Geladen via `load_detachment_types()`.

| ID | Name | command_cost | command_benefit |
|----|------|-------------|----------------|
| `patrol` | Patrol | 2 | 0 |
| `battalion` | Battalion | 0 | 3 |
| `brigade` | Brigade | 0 | 12 |
| `spearhead` | Spearhead | 1 | 0 |
| `outrider` | Outrider | 1 | 0 |
| `vanguard` | Vanguard | 1 | 0 |
| `air_wing` | Air Wing | 1 | 0 |
