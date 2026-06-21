# Plan 024 — Arkana Research Digest (Step 6 Vorarbeit)

> **Lebensdauer (ADR-0006): DAUERHAFT.** Plan-Companion-Referenz unter `docs/`;
> bleibt erhalten, bis Plan 024 vollständig umgesetzt und abgeschlossen ist.

> Recherche per Sonnet-Subagent (S86, 2026-06-22), gegen
> `docs/work/wahapedia_necrons/faction_overview.txt` (Z. 2639–2844) geprüft, von
> Opus reviewt. Vorlage für die Step-6-YAML-Edits — **kein Dispatch**, nur
> strukturiertes `trigger`/`conditions`/`effect`-Schema + englisches `rule_text`
> für Doku/Display. Failsafe Overcharger ist separat in Step 5.

## ⚠️ Schlüssel-Befund: alle 12 Punktkosten +5 zu hoch

Plan 024 listete nur 3 Punktkosten-Korrekturen. Die Recherche zeigt: **alle 12
YAML-Einträge sind exakt 5 Punkte höher** als die Wahapedia-Tabelle
(`faction_overview.txt` Z. 2639–2677). Die Plan-021-Migration übernahm
systematisch +5 pro Arkanum.

**✅ ENTSCHEIDEN (Stakeholder, S86):** **Alle 12** Punktkosten in Step 6 auf die
Wahapedia-Werte (rechte Spalte unten) korrigieren — nicht nur die 3 im Plan.

| Arkanum | YAML | Wahapedia | im Plan? |
|---|---|---|---|
| failsafe_overcharger | 30 | 25 | ja (Step 5) |
| atavindicator | 25 | 20 | ja (Step 6a) |
| countertemporal_nanomines | 30 | 25 | ja (Step 6a) |
| dimensional_sanctum | 15 | 10 | neu |
| hypermaterial_ablator | 25 | 20 | neu |
| cortical_subjugator_scarabs | 15 | 10 | neu |
| cryptogeometric_adjuster | 15 | 10 | neu |
| metalodermal_tesla_weave | 20 | 15 | neu |
| photonic_transubjector | 20 | 15 | neu |
| phylacterine_hive | 20 | 15 | neu |
| prismatic_obfuscatron | 20 | 15 | neu |
| quantum_orb | 20 | 15 | neu |

## Fehlende Engine-Subsysteme → warum 10/12 `descriptive` bleiben

| Fehlendes Subsystem | Betroffene Arkana |
|---|---|
| Mortal-Wound-Handler | atavindicator, metalodermal_tesla_weave, quantum_orb |
| Deferred-Trigger / Marker | quantum_orb |
| Räumliches Proximity-Tracking | hypermaterial_ablator, prismatic_obfuscatron, metalodermal_tesla_weave, quantum_orb |
| Damage-Nullify-Hook (Save-Loop) | photonic_transubjector |
| Ability-Grant-Dispatch | dimensional_sanctum |
| Meta-Ability-Targeting | phylacterine_hive |
| Enemy-Direction-Hit-Debuff | cryptogeometric_adjuster |
| Halve-Movement-Debuff (feindlich) | countertemporal_nanomines |
| HI-Eligibility-Grant / Unit-Target-Picker | cortical_subjugator_scarabs |

## Schema-Vorschläge je Arkanum (Step 6b)

Jeweils `rule_text` (englisch, aus Wahapedia) + vorgeschlagenes
`trigger`/`conditions`/`effect`. Alle bleiben `ability_type: descriptive`.

- **atavindicator** (PSYCHOMANCER) — Ende Movement: ein Feind (ohne VEHICLE) in
  18", 3D6 ≥ Ld → D3 MW. `effect: {type: mortal_wounds, roll: 3d6,
  threshold: target_leadership, wounds: d3}`.
- **countertemporal_nanomines** (CHRONOMANCER) — Shooting: Feind in 18", bis
  Beginn nächster Runde Advance-/Charge-Würfe halbieren.
  `effect: {type: halve_movement, affects: [advance_roll, charge_roll]}`.
- **dimensional_sanctum** — passiv: Träger erhält Dimensional Translocation
  (YAML hat bereits `grants_ability`). `effect: {type: ability_grant}`.
- **hypermaterial_ablator** — Command: friendly CORE/CANOPTEK in 9", bis nächste
  Command-Phase Light Cover gegen Schützen >12".
  `effect: {type: cover_grant, cover_type: light_cover}`.
- **cortical_subjugator_scarabs** — once/battle, Start gegnerischer HI-Step:
  friendly DYNASTY in 6" darf HI wie CHARACTER (wenn nicht in Engagement Range).
  `effect: {type: hi_grant}`.
- **cryptogeometric_adjuster** — Start gegnerischer Shooting: Feind in 12" und
  sichtbar, −1 auf dessen Trefferwürfe bis Phasenende.
  `effect: {type: hit_debuff, modifier: -1, applies_to: attacks_made_by_target}`.
- **metalodermal_tesla_weave** — Ende gegnerischer Charges-Step: Feind, der
  Charge in 6" beendete, D6 2+ → D3 MW. `effect: {type: mortal_wounds,
  roll: 1d6, threshold: 2, wounds: d3}`.
- **photonic_transubjector** — once/turn, erster fehlgeschlagener Save des
  Trägers → Damage der Attacke auf 0. `effect: {type: damage_nullify,
  set_damage_to: 0}`.
- **phylacterine_hive** (TECHNOMANCER) — once/battle, wenn Träger Rites of
  Reanimation nutzt: CANOPTEK/DESTROYER CULT/TRIARCH PRAETORIAN statt CORE.
  `effect: {type: meta_ability, modifies_ability: rites_of_reanimation}`.
- **prismatic_obfuscatron** — passiv: solange Träger nicht nächstes Ziel ist,
  kann er nicht mit Fernkampf angegriffen werden.
  `effect: {type: untargetable, condition: not_closest_eligible_target}`.
- **quantum_orb** (PLASMANCER) — once/battle, Command: Marker in 24", nächste
  Command-Phase D6 je Einheit in 6" (−1 CHARACTER): 4–5 D3 MW, 6 = 3 MW.
  `effect: {type: deferred_aoe_mortal_wounds, aoe_radius_inches: 6}`.
