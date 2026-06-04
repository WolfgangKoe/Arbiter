# Necrons — Datendokumentation

> Stand: 2026-06-04 | Quelle: Wahapedia WH40k 9E

---

## Command Protocols (`round_choice`)

Geladen via `load_round_choice_abilities("necrons")`.  
`round_choice_label: "Command Protocols"`  
**Runde 1:** Eternal Guardian ist automatisch aktiv (`auto_round_1: true`).

| Protocol ID | Name | Subfaction Affinity | Primary | Secondary |
|-------------|------|---------------------|---------|-----------|
| `protocol_eternal_guardian` | Protocol of the Eternal Guardian | **nihilakh** | +1 Save | Re-roll Save 1 |
| `protocol_hungry_void` | Protocol of the Hungry Void | **novokh** | +1 Hit (Shooting) | +1 Strength (Shooting) |
| `protocol_conquering_tyrant` | Protocol of the Conquering Tyrant | sautekh | +1 Leadership | Re-roll Hit+Wound 1 (Melee) |
| `protocol_sudden_storm` | Protocol of the Sudden Storm | nephrekh | +1" Move | Advance+Charge |
| `protocol_undying_legions` | Protocol of the Undying Legions | **szarekhan** | Re-roll RP | +1 Model returned per RP |
| `protocol_vengeful_stars` | Protocol of the Vengeful Stars | **mephrit** | +1 Wound (Shooting) | -1 AP (Shooting) |

> **Hinweis:** Die 4 fett markierten Affinitäten wurden 2026-06-04 via Wahapedia korrigiert.  
> Vorher falsch: eternal_guardian=szarekhan, hungry_void=mephrit, undying_legions=novokh, vengeful_stars=nihilakh.

---

## Triggered Abilities

Alle in `faction_abilities.yaml` als `ability_type: triggered`:

| ID | Name | Timing | Condition |
|----|------|--------|-----------|
| `living_metal` | Living Metal | phase_start/command | `has_rules: [livingMetal]` |
| `reanimation_protocols` | Reanimation Protocols | phase_reactive | `has_rules: [reanimationProtocols]` |

---

## Unit Abilities (`unit_abilities.yaml`)

Keyword-basierte Spezialregeln:

| ID | Name | Condition |
|----|------|-----------|
| `quantum_shielding` | Quantum Shielding | `has_rules: [quantumShielding]` |
| `phase_shifter` | Phase Shifter | `has_rules: [phaseShifter]` |
| `wraith_form` | Wraith Form | `has_rules: [wraithForm]` |
| `dimensional_translocation` | Dimensional Translocation | `has_rules: [dimensionalTranslocation]` |
| `feel_no_pain.*` | Feel No Pain (verschiedene Schwellen) | je nach Einheit |
| `deep_strike.*` | Deep Strike | je nach Einheit |

---

## Subfaction Abilities (`subfaction_abilities.yaml`)

Dynastien-spezifische Regeln (Destroyer Cult, hardwired_for_destruction).

---

## Wargear Abilities (`wargear_abilities.yaml`)

13 Arkana-Einträge (migriert aus `arkana.yaml` in Ziel 6h).  
Arkana: failsafe_overcharger, countertemporal_nanomines, atavindicator, dimensional_sanctum, hypermaterial_ablator, cortical_subjugator_scarabs, cryptogeometric_adjuster, metalodermal_tesla_weave, photonic_transubjector, phylacterine_hive, prismatic_obfuscatron, quantum_orb, lethargic_veil.
