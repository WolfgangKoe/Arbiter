STATUS: ANSWERED (S147-Audit-Befundkatalog — behalten bis Fixing-Plan-Umsetzung S148)

# GO-Audit B2 — Ork-Abilities (S147)

## Grundannahmen
- Die App würfelt NICHT — alle Würfe passieren am Tisch; die App zeigt Werte/Modifikatoren/Hinweise.
- Klasse A = App rechnet/erzwingt, Klasse B = nur am Tisch prüfbar (App zeigt Hinweistext, kein Bug),
  Klasse C = Hybrid (App-Anteil + Tisch-Anteil) — analog `docs/spec/acceptance/rules.md`.
- `within_inches`/räumliche Nähe-Bedingungen sind laut `abilityEngine.check_conditions`
  bewusst **nicht** implementiert ("always passes") — das ist dokumentierte Klasse-B-Politik,
  kein Einzel-Bug je Fundstelle.
- `get_abilities_for_unit` (loader.py:889) liefert Fähigkeiten NUR zur Anzeige auf der UnitCard —
  Anzeige ohne Engine-Berechnung ist bei reinen Text-/Tisch-Regeln by design, keine Lücke per se.

## Stand `subfaction_abilities.yaml` (Parallel-Executor K1)
`git diff --stat -- data/wh40k_9e/orks/subfaction_abilities.yaml` war zu Beginn UND am Ende
meines Laufs leer (keine Änderung) — K1 hat die Datei während meiner Laufzeit nicht verändert.

## Bestandsaufnahme (S144-M1-Pflicht)
Alle 5 Scope-YAMLs vollständig gelesen: `faction_abilities.yaml` (126 Z., 4 Abilities),
`unit_abilities.yaml` (625 Z., 31 Abilities), `subfaction_abilities.yaml` (206 Z., 7 Klans/
Abilities), `wargear.yaml` (147 Z., 10 Items, 6 mit `effect`), `relics.yaml` (185 Z., 9 Relics).
Zusätzlich `docs/work/wahapedia_orks/{faction_overview,stratagems,units_all}.txt` und
`docs/work/wahapedia_core_rules/{core_rules,rules_appendix}.txt` (Advance/Assault-Weapon-Regel)
geprüft, keine Datei blind übersprungen.

## Lücken-Tabelle

| Ability | Datei:Zeile | Befund-Typ | Status | Beleg |
|---|---|---|---|---|
| Waaagh! Stage1/2 (`buff_stat`, `invuln_save`, `charge_after_advance`) | faction_abilities.yaml:47-99 | YAML→Engine OK | bestätigt | `abilityEngine.buff_stat_bonus`/`ability_invuln_save`/`charge_after_advance_allowed` lesen `_active_effects_for_faction`; Verdrahtung in `chargePhase.py:92-94`, `_common.py:1826,2352,2508`, `unitCard.py:389`. Stage-Übergang via `next_stage_id` in `gameState.py:629-660`. |
| Speedwaaagh! Stage1 — `assault_after_advance`, `dakka_hits`, `buff_ap` | faction_abilities.yaml:117-125 | YAML→Engine tot | **neu** | 0 Treffer für alle 3 Effect-Types in `src/`+`tests/`. Aktivierbar über den generischen Once-per-Battle-Button (`armyCard._render_once_per_battle_ability_ui`), aber KEINER der 3 Kampf-Effekte wird irgendwo konsumiert — reines Badge/Text, keine Wirkung auf Trefferwurf/AP/Advance-Feuerstrafe. |
| Grundmechanik „Assault-Waffe nach Advance" | `shootingPhase.py:44` | Root Cause für obigen Befund | **neu** | `can_shoot()` blockt Schießen nach Advance PAUSCHAL (`if flags.get("advanced"): return False`), ohne Ausnahme für Assault-Waffen. 9E-Regel (`rules_appendix.txt:2347-2354`): Assault-Waffen DÜRFEN nach Advance feuern (−1 Trefferwurf, sofern keine Ausnahme). Fehlt generisch — nicht Ork-spezifisch, aber Ursache dafür, dass `assault_after_advance` (Speedwaaagh, Evil Sunz Kultur) und die entsprechende Ork-SPEED-FREEKS-Ausnahme wirkungslos sind. |
| Evil Sunz Kultur — `assault_after_advance` | subfaction_abilities.yaml:124 | YAML→Engine tot | **neu** | Gleicher 0-Treffer-Befund; `buff_stat`(move) und `buff_roll`(advance_roll) sind ebenfalls 0 Treffer — nur `buff_roll`(21 Treffer) ist generisch belegt, aber Kontext zeigt: die 21 Treffer gehören zu `commandPhase._render_buff_roll_ability` (Command-Phase Aktivierung, nicht Movement-Buff) — Evil Sunz move/advance-Boni sind unverdrahtet. |
| Ghazghkull „The Great Waaagh!" (`activate_faction_ability`, `ability_ids` Plural) | unit_abilities.yaml:196-200 | YAML→Engine tot + Struktur-Bug | **neu, gravierend** | `activate_faction_ability` hat 0 Treffer irgendwo in `src/`. Der tatsächliche Aktivierungspfad läuft NICHT über unit_abilities, sondern direkt über `faction_abilities.yaml`-Einträge mit `ability_type: activated` (`armyCard._render_once_per_battle_ability_ui`, Zeile 401-405: nimmt IMMER nur die erste once-per-battle-Ability der Fraktion). Ghazghkull hat Keyword WARBOSS (units.yaml:385) → aktiviert nur `waaagh_stage1` wie jeder normale Warboss; die kombinierte Speedwaaagh-Wirkung (2. Ability-ID) wird nie ausgelöst — Ghazghkulls Alleinstellungsmerkmal ist unspielbar in der App. |
| Warboss/Warboss-Mega-Armour „Call Da Waaagh!" (`activate_faction_ability`) | unit_abilities.yaml:23-25, 536-538 | YAML→Engine tot, aber unschädlich | bestätigt | Gleicher 0-Treffer-Befund wie oben, ABER hier ist es redundant/harmlos: Aktivierung läuft real über `waaagh_stage1` direkt aus `faction_abilities.yaml` (eigene `has_keywords`/`once_per_battle`-Bedingung) — unit_abilities-Eintrag dient nur der Anzeige auf der UnitCard. |
| Mob Rule (`morale_immunity`) | unit_abilities.yaml:483-499 | YAML→Engine tot | bestätigt (Klasse B) | 0 Treffer für `morale_immunity`; `moralePhase._attrition_threshold` (Z.74-92) berechnet Half-Strength direkt/hardcoded, konsultiert keine Ork-Ability. Bedingung `nearby_friendly_above_half` ist eine räumliche Bedingung → Klasse B laut Grundannahme, kein Einzel-Bug, aber die App zeigt derzeit auch keinen Hinweistext im Morale-Screen dazu (nur auf der UnitCard). |
| Ramshackle (`damage_reduction`) | unit_abilities.yaml:501-518 | YAML→Engine tot | **neu** | 0 Treffer für `damage_reduction` — Vehicle-Schadensreduktion (S8+ Ausnahme) wird nirgends in `combat.py`/Schadensauswertung angewendet; reiner Anzeigetext auf der UnitCard. Betrifft mehrere Ork-Fahrzeuge (Trukk, Battlewagon, Gorkanaut/Morkanaut je nach units.yaml-Zuordnung). |
| Diverse Trigger-/Aura-Effekte (`invuln_save_aura`, `fnp_aura`, `buff_stat_aura`, `buff_hit`, `debuff_hit`, `reroll_charge`, `reroll_wound`, `extra_hit_on_6`, `deep_strike`, `scout_move`, `self_repair`, `psyker_powers`, `objective_control`) | unit_abilities.yaml (durchgängig, s. grep-Tabelle) | YAML→Engine tot | bestätigt (Klasse B/Anzeige) | Alle 0 Treffer in `src/`+`tests/`. Muster durchgängig: `unit_abilities.yaml` ist der Text-/Bedingungs-Layer für die UnitCard-Anzeige; die Kampfrechnung liest ausschließlich `_active_effects_for_faction` (aktivierte Fraktions-Fähigkeit) bzw. dedizierte Module (`moralePhase`, `chargePhase`, `commandPhase`). D.h. **Unit-Abilities ohne Verbindung zu einer aktivierbaren Fraktions-Ability werden nie berechnet** — nur angezeigt. Das ist ein strukturelles Muster (auch bei Necrons vermutlich gleich), keine Ork-spezifische Einzel-Lücke — aber die Menge (13 Effect-Types) zeigt: der Großteil der Ork-Unit-Abilities ist reine Dokumentation, keine Berechnung. |
| Klan-Kulturen (alle 7) | subfaction_abilities.yaml | YAML→Engine tot | bestätigt (Klasse B) | Keiner der Effect-Types (`cover_save`, `fallback_shoot_or_charge`, `reroll_one`, `mortal_wound_negate`, `objective_secured`, `wound_roll_fail_threshold`, `buff_roll`(wound_roll/advance_roll), `extra_hit_on_6`(fight)) hat einen Konsumenten. Klan-Auswahl wirkt aktuell NUR als reiner Info-Text im Roster (`subfaction_field: clan`), keine Kampfrechnung nutzt sie. Größere strukturelle Lücke, die über B2 hinausgeht (P2-Kandidat: „Klan-Kultur-Effekte verdrahten"). |
| `wh40k_9e.orks.unit.objective_secured` (`shared_ref`) | unit_abilities.yaml:463-479 | YAML→Engine tot | bestätigt (Klasse B/manuell) | `shared_ref` als Feld 0 Treffer in `src/`; App trackt keine Objective-Marker-Kontrolle — plausibel bewusst außerhalb des App-Scopes (VP/Missionsziele sind Tischsache). |
| Auto-Hit Waffen (Skorcha + 3 weitere + Da Gobshot Thunderbuss-Relic) | weapons.yaml:475,721,937-940,990; relics.yaml:19 | Daten-/Detektor-Bug | **neu, konkret** | `_detect_weapon_special` (attackMath.py:153) prüft `"Auto-hits" in abilities` (exakter Teilstring). Ork-Waffen tragen den vollen Wahapedia-Satz `"...that attack automatically hits the target."` — Substring passt NICHT → Badge/Flag bleibt False für alle 5 Fundstellen. Necron-Pendant nutzt den normalisierten String `"Auto-hits."` (necrons/weapons.yaml:391,715) — Beleg, dass die Ork-Daten nicht auf das erwartete Format normalisiert wurden. Zusätzlich: Skorcha (weapons.yaml:939) hat bereits ein strukturiertes `effect: {type: auto_hit}` — das der Detektor GAR NICHT liest (nur Text-Substring, kein `effect.type`-Check) → selbst die eine korrekt strukturierte Stelle ist tot. |

## Waffen-Keyword-Inventar Orks (Sondertypen-Bestandsaufnahme)

- `weapon_type: Dakka` — 11 Fundstellen in `weapons.yaml` (Z. 21,91,117,286,359,689,727,753,1028
  + 2 weitere). Wahapedia-Regel (`faction_overview.txt:625-626`): zwei Attacken-Werte, erster gilt
  innerhalb halber Reichweite. Bereits **strukturell modelliert** (nicht Text-Erkennung!): Profil
  trägt `effect: {type: alternating_fire}` (z. B. weapons.yaml:22-23) und `attacks: "N/M"`.
  `_detect_weapon_special` (attackMath.py:155) liest `effect_type == "alternating_fire"` generisch
  — KEIN String-Match auf "Dakka". Konsument: `diceHtml.py:70` rendert nur ein Info-Badge
  ("First attacks if within half range") — Attackenzahl selbst wird manuell vom Nutzer im
  Gruppen-Zuweisungsfeld eingetragen (`_total_attacks_int` nimmt `split("/")[0]` als Default-Cap,
  analog zum Rapid-Fire-Muster in `_rapid_fire_input_cap`, aber OHNE eigene Cap-Verdopplung für
  Dakka — Cap ist bereits der höhere Wert, daher unkritisch). **Fazit: Dakka braucht KEINE
  grantsKeyword-Migration** — ist bereits generisch effect-type-basiert, nur Anzeige (Klasse B/C
  korrekt gelöst).
- Echter Text-Erkennungs-Fall ist **nicht** Dakka, sondern **`auto_hit`** (s. Lücken-Tabelle oben)
  und `has_mortal_wounds` (`"mortal wound" in abilities.lower()`, attackMath.py:162) — beide sind
  echte String-Matches auf das freie `abilities`-Feld, kein Keyword. Für Orks: 5 Auto-Hit-Stellen
  betroffen (s.o.); `has_mortal_wounds` wurde nicht einzeln geprüft (Budget), aber gleiches Muster
  ist zu erwarten.
- Kein Necron-analoges GAUSS/TESLA-Muster (kein `grantsKeyword`-Feld existiert aktuell irgendwo
  im Repo — 0 Treffer für `grantsKeyword`/`grants_keyword` in `src/`). Die S147-Konvention ist also
  noch komplett neu einzuführen, nicht nur für Orks nachzuziehen.

## snake_case-Feld-Inventar (Migrationsplan-Basis)

Aggregiert über alle 5 Scope-Dateien (Feld → Gesamt-Fundstellen, grob):
`type`(≈76), `target`(≈56), `trigger`/`timing`/`stage`/`player`/`phase`/`conditions`/`effect`/
`ability_type`/`rule_text`/`name_en`(je ≈50-58), `modifier`(≈27), `stat`(≈20), `unit_id`(27),
`effects`(15), `once_per_battle`(9), `condition`(10), `target_keywords`(8), `persistent_effects`(9),
`badge_label`(6), `weapon_type`(3+11 in Profilen), `range_inches`/`ap`/`damage`/`profiles`(je 3),
`ability_id`(3), `within_inches`(2), `applies_to`/`replaces`/`any_of`(je 11-13, relics.yaml),
`triggered_effects`(2), `weapon_types`(1, Bad Moons — Plural-Variante von `weapon_type`!),
`min_range_from_enemy`, `roll_threshold`, `ranged_only`, `powers_per_turn`, `power_list`,
`waaagh_called_this_turn`, `nearby_friendly_above_half`, `except_strength_ge`, `condition_prompt`,
`applies_when`, `target_keyword`(Singular, 1x — Inkonsistenz zu `target_keywords`!), `shared_ref`,
`subfaction_field`, `subfaction_label`, `klan_keyword`, `mortal_dice`, `bonus_amount`.
Auffällig: `target_keyword` (Singular, unit_abilities.yaml „beast_snagga") vs. `target_keywords`
(Plural, sonst überall) — bereits jetzt ein Feld-Inkonsistenz-Fund, unabhängig von camelCase.

## Fixing-Plan-Vorschlag (je Häppchen ≤ Effort M, für S148)

1. **[S] Auto-Hit-Normalisierung**: `abilities`-Text in den 4 Ork-Waffen + 1 Relic auf
   `"Auto-hits."` vereinheitlichen (analog Necron) UND `_detect_weapon_special` um
   `effect_type == "auto_hit"` als zusätzliche/primäre Quelle erweitern (generisch, kein
   Fraktions-String). Regressionstest: `test_auto_hit_detected_from_effect_type`.
2. **[M] Assault-Waffen-nach-Advance-Grundmechanik**: `can_shoot()` in `shootingPhase.py` um
   die generische Ausnahme „Assault-Typ-Waffe im Gepäck → Schießen erlaubt, −1 Trefferwurf"
   erweitern (Kernregel `rules_appendix.txt:2347-2354`, nicht ork-spezifisch). Voraussetzung
   für Punkt 3 — sollte VOR den Ork-Kultur-Fixes laufen, da sonst kein Abnehmer existiert.
3. **[M] Speedwaaagh!/Evil-Sunz Kampf-Effekte verdrahten**: `assault_after_advance` (nutzt
   Punkt 2), `dakka_hits`/`buff_ap` (Speedwaaagh) und `move`/`advance_roll`-Boni (Evil Sunz)
   an `_active_effects_for_faction`/`_active_directive_effects`-Muster anschließen — analog
   `buff_stat_bonus`. Je Sub-Effekt eigener Regressionstest.
4. **[M] Ghazghkull „Great Waaagh!" strukturell reparieren**: entweder eigene
   `faction_abilities.yaml`-Ability mit `ability_type: activated`, kombiniertem Effect (multi
   aus beiden Waaagh-Effekt-Listen) UND Vorrang vor der generischen Warboss-Aktivierung, ODER
   `_render_once_per_battle_ability_ui` generisch auf „mehrere once-per-battle-Fähigkeiten,
   höchste zuerst/Unit-spezifisch" erweitern. Erfordert Stakeholder-Entscheidung zum
   UI-Vorgehen (NEEDS-DECISION) — Konsens-Modus.
5. **[S] Mob Rule / Ramshackle — Hinweistext statt Stille**: wo Engine-Berechnung laut
   Grundannahme bewusst Klasse B bleibt (räumliche Nähe), zumindest den Hinweistext auch im
   jeweiligen Phase-Screen (Morale/Damage) anzeigen, nicht nur auf der UnitCard — kleine
   UI-Ergänzung, kein Engine-Fix.
6. **[L, muss gesplittet werden] Klan-Kultur-Effekte verdrahten**: alle 7 Klans strukturell
   ohne Konsument — separates P2-Thema, nicht Teil von B2/S148, da Effort > M.
7. **grantsKeyword-Konvention**: da Dakka bereits sauber gelöst ist und kein GAUSS/TESLA-Analog
   im Repo existiert, ist der „Ork-Anteil" der grantsKeyword-Migration derzeit NUR Punkt 1
   (Auto-Hit) — kein größerer Migrationsaufwand nötig, sofern die Stakeholder-Entscheidung
   „grantsKeyword generisch für auto_hit/has_mortal_wounds" lautet statt eines dedizierten
   `effect.type`-Checks. Diese Wahl ist eine Konsens-Entscheidung für S148 (NEEDS-DECISION).

## Selbst-Stopp
Budget 30k (hart 45k) eingehalten — Recherche in einem Durchgang abgeschlossen, keine
Zwischenrückgabe nötig.
