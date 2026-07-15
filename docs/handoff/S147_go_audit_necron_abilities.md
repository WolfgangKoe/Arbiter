STATUS: ANSWERED (S147-Audit-Befundkatalog — behalten bis Fixing-Plan-Umsetzung S148)

# GO-Audit B1 — Necron Abilities (S147)

Subagent: Audit B1. Rein lesend, kein Code/Daten geändert.
Scope: `data/wh40k_9e/necrons/{faction_abilities,unit_abilities,subfaction_abilities,wargear,relics,arkana}.yaml`
(+ `weapons.yaml`/`units.yaml` für GAUSS/TESLA) ↔ `src/gameMechanic/abilityEngine.py` + `src/gameObjects/loader.py`
↔ `docs/work/wahapedia_necrons/` (+ `core_rules.txt`/`rules_appendix.txt` für die Weapon-Definitions-Frage).

**Parallel-Hinweis:** `subfaction_abilities.yaml` wurde während der gesamten Laufzeit NICHT verändert —
`git diff --stat` und `git status --short` waren beide leer (keine Executor-Kollision, keine Neubewertung nötig).

---

## 1. Grundannahmen (Class A/B/C — analog `docs/spec/acceptance/rules.md`)

- Die App würfelt **nicht** — jede Wurf-Klassifizierung unten ist über die Frage
  "berechnet/erzwingt die App das Ergebnis" definiert, nicht über die physische Handlung des Würfelns.
- **Klasse A** = App berechnet/erzwingt (Zahlenwert, Automatik). **Klasse B** = nur am Tisch
  prüfbar, App zeigt höchstens einen Hinweis/Caption. **Klasse C** = Hybrid (Teil A, Teil B).
- `enforcement: table` (bei Directives) und eine reine `st.caption(...)`-Anzeige ohne Zustandsänderung
  sind **keine** automatischen Lücken — sie sind absichtlich als Tisch-Hinweis modelliert (Klasse B).
  Lücke ist erst, wenn eine Ability als "aktiv/anwendbar" suggeriert wird (Button "Apply"/"Activate"),
  aber der Klick **keine** Zustandsänderung bewirkt — das ist eine UI-Falle, keine bewusste B-Klasse.
- Bestandsaufnahme-Pflicht (S144-M1) erfüllt: alle 6 Necron-Ability-YAMLs vollständig gelesen (434 + 970 +
  157 + 189 + 97 + 141 Zeilen), `docs/work/wahapedia_necrons/{faction_overview,stratagems,units_all}.txt`
  und `docs/work/wahapedia_core_rules/rules_appendix.txt` gezielt durchsucht (keine Aussage aus dem Gedächtnis).

---

## 2. Lücken-Tabelle

| Ability/Bereich | Datei:Zeile | Befund-Typ | Status | Beleg |
|---|---|---|---|---|
| **Alle `unit_abilities.yaml`-Einträge mit `ability_type: activated`, `effect.type` ∉ {`buff_roll`,`reroll_hit_1`}** (Chronometron, Master Chronomancer, The Stars Are Right, Voice of the Triarch, Adaptive Strategy, Gravity Pulse, Nanoscarab Reanimation Beam) | `unit_abilities.yaml:152-206,68-85,290-307,804-821`; Renderer `src/gameMechanic/commandPhase.py:390-399` | **YAML→Engine: toter Pfad** | neu | `_render_unit_command_abilities` (commandPhase.py:390) rendert **nur** `effect.type in ("buff_roll","reroll_hit_1")`. Die o.g. 7 `activated`-Fähigkeiten haben **keinen** Renderer irgendwo im Repo — verifiziert per `grep -rn "buff_charge_and_invuln\|profile_switch\|alter_command_protocol\|allow_fell_back_shoot_charge\|buff_rp\b" src/` (0 Treffer außer der grep-Query selbst). Anders als bei Directives (`enforcement: table`) gibt es **nicht einmal** einen Hinweis-Caption — die Fähigkeit ist im Command-Phase-UI für die tragende Einheit schlicht unsichtbar. |
| **`_render_triggered_abilities` generischer Apply-Button für `ability_type: triggered` mit `effect.type` ∉ {`heal`,`reanimate`}** (u. a. Royal Warden/Silent King Relentless March = `buff_stat`, United in Destruction = `reroll_wound_1`, Phaeron of the Stars/Blades = `reroll_hit`/`reroll_wound`, Obeisance Generators = `fight_last`, Viral Construct = `buff_stat`, Hexmark Multi-threat Eliminator = `reroll_hits`, Hovering Sentinel = `toggle_keyword`, Dynastic Command Node = `allow_repeat_ability`, Translocation Protocols = `teleport`, Multi-limbed Combat = `bonus_attacks`, Enslaved Star God = `auto_pass_morale`) | `src/uiLayout/armyCard.py:90-151` (insb. 109 `if effect.type=="reanimate": continue`; 123 `if effect.type=="heal"`; generischer Button 134-151 ruft `execute_effect` für ALLE anderen Typen) | **Bug (schwerwiegender als reine Lücke)** | neu | `execute_effect()` (`abilityEngine.py:69-78`) behandelt **nur** `"heal"` — jeder andere `effect.type` fällt durch `return False`. Der generische "Apply {name}"-Button (armyCard.py:134) ist trotzdem für alle `triggered`-Abilities sichtbar, deren `trigger.phase` mit der aktuellen Phase übereinstimmt (siehe `_ability_matches_phase`, armyCard.py:83-87 — prüft **nur** `phase`, nicht `timing`). Klick: keine Zustandsänderung, aber `applied_triggered_{id}` wird **trotzdem** auf `True` gesetzt (armyCard.py:150) und der Log-Eintrag lautet hart-codiert `"{name}: {n} unit(s) healed"` (armyCard.py:148) — semantisch falsch für z. B. Quantum Shielding/United in Destruction. Nach einem Klick gilt die Fähigkeit fälschlich als "already applied" und ist für den Rest der Phase gesperrt (Zeile 132-133). |
| Persistente `invuln_save`/`fnp`/`restriction`/`deep_strike`/`move_through_terrain`/`profile_switch`/`double_use_power`-Trigger mit `trigger.phase: any` (Quantum Shielding, Phase Shifter, Wraith Form, Dynastic Advisors, Evasion Protocol, Infused Madness, Dominion Protocols, Out-of-Phase Existence, Fractured Personality, Vengeance of the Enchained, Reality Unravels — `timing: round_start`) | `unit_abilities.yaml` diverse | **kein Bug — nie sichtbar, weil `phase: any` nicht matcht** | bestätigt (unkritisch) | `_ability_matches_phase` (armyCard.py:83-87) vergleicht `phase_key` (nie `"any"`, siehe `PHASES`-Liste `gameState.py:40-49`: setup/command/movement/psychic/shooting/charge/fight/morale) gegen `ability.trigger.phase` — `"any" == phase_key` ist nie wahr. Diese Abilities rendern **nirgends** in `_render_triggered_abilities`. Für die reinen Passiv-Stat-Fälle (Quantum Shielding, Phase Shifter, Wraith Form, Evasion Protocol) ist das vermutlich unschädlich, **wenn** der Basiswert (`invuln_save`) bereits statisch in `units.yaml` steht — das war NICHT Teil des gelesenen Scopes (units.yaml nur für GAUSS/TESLA gegrept, nicht auf `invuln_save`-Felder geprüft) → **Anschlussfrage für S148**, nicht hier verifiziert. Für `reactive`-Events (`model_destroyed`, `pre_battle`, `round_start`) ist die fehlende Anzeige erwartbar, da diese über einen anderen Mechanismus (Reactive-Hooks) laufen müssten, die im gelesenen Scope (`abilityEngine.py`, `armyCard.py`) nicht existieren → vermutlich vollständig unimplementiert (Class-B-Kandidat: Sterbe-/Rundenstart-Effekte), aber nicht abschließend verifiziert (Kampf-/Rundenlogik liegt in `combat.py`/`phaseRunner.py`, außerhalb des Scopes). |
| Reaktive `mortal_wounds`/`free_attack`/`reroll_rp`-Trigger (Arc Fields, Wrath of the Seraptek, Inescapable Death, Their Number is Legion, Targeting Relay) | `unit_abilities.yaml` diverse (event: `after_enemy_attack`, `enemy_falls_back`, `reanimation_roll`, `after_unit_shoots`) | **außerhalb Scope, nicht abschließend geprüft** | offen (Weiterleitung) | Diese Events sind spezifischer als das generische `phase_reactive`/`event`-Paar, das `abilityEngine.py` nur für `after_enemy_attack` (Reanimation Protocols, Zeile 393-419) konkret verdrahtet. Ob `combat.py`/`shootingPhase.py`/`chargePhase.py` diese anderen Events konsumieren, ist außerhalb des Audit-Scopes (`abilityEngine.py`+`loader.py`) — Empfehlung: eigener Reaktiv-Ability-Audit-Auftrag S148. |
| `Disintegration Capacitors` (Gauss-Stratagem) und `Malevolent Arcing` (Tesla-Stratagem) | `stratagems.yaml:249-263` (Disintegration Capacitors, `conditions: []`), `:265-275` (Malevolent Arcing, `conditions: []`) | **Bedingungsvollständigkeit — bestätigte Lücke** | bestätigt (bekannt aus Plan 032, aber hier neu bewertet im GAUSS/TESLA-Kontext) | Beide Stratagems sind laut `rule_text` an "makes an attack with a gauss/tesla weapon" gebunden, haben aber `conditions: []` — die App zeigt sie für **jede** NECRONS-Einheit an, auch ohne Gauss-/Tesla-Bewaffnung. Das ist exakt die Lücke, die das unten skizzierte `grantsKeyword`-Konzept schließen soll (Abschnitt 4). Nicht Teil des heutigen Ability-YAML-Scopes (liegt in `stratagems.yaml`), aber hoch relevant als Consumer des neuen Keywords — daher hier dokumentiert statt übersehen. |
| Gauss-Grundwaffen ohne "AP+1 bei ungewürfeltem Wundwurf 6"-Text | `weapons.yaml:210-244` (gauss_flayer, gauss_reaper, gauss_blaster: `abilities: ""`) | **Regel-Textlücke, kein Engine-Bug** | neu, aber **nicht** Teil des Codex-Grundregeltextes — siehe unten | Wahapedia `faction_overview.txt:722-739` definiert GAUSS/TESLA **nur** als Namenskonvention ("a gauss weapon is any weapon whose profile includes the word 'gauss'") für den Gebrauch durch ANDERE Regeln (Stratagems, Weapon-Enhancement-Tabellen) — es gibt **keinen** eigenen "Gauss-Waffenfähigkeit"-Text im Codex, der pro Waffe stehen müsste (anders als Tesla: dort steht der Effekt explizit in der `abilities`-Spalte jeder Tesla-Waffe, z. B. `tesla_carbine` Zeile 253 "unmodified hit roll of 6 scores 2 additional hits"). Die leeren `abilities: ""` bei Gauss-Grundwaffen sind daher **korrekt** (Gauss hat keinen inhärenten Extra-Effekt pro Waffe) — die Lücke liegt einzig darin, dass **nichts** im Datenmodell markiert, welche Waffen "gauss"/"tesla" im Sinne der Namensdefinition sind, was die o.g. Stratagem-Bedingungen ungeprüft lässt. |
| Cryptek-Arkana `ability_type: descriptive` mit ausmodelliertem `effect`-Block (13 von 14 Arkana in `faction_abilities.yaml:184-434`) | `faction_abilities.yaml:203-434` | **YAML→Engine: komplett unverdrahtet** | bestätigt (bereits als "STOPGAP marker" im Kommentar Zeile 180-183 dokumentiert) | Kein einziger der Arkana-`effect.type`-Werte (`multi/buff_stat`, `halve_movement`, `mortal_wounds`, `ability_grant`, `cover_grant`, `hi_grant`, `hit_debuff`, `damage_nullify`, `meta_ability`, `untargetable`, `deferred_aoe_mortal_wounds`) taucht in der `effect.type ==`-Grep-Liste (Abschnitt „Engine→YAML" unten) auf. Bestätigt den bestehenden Kommentar — keine neue Information, aber verifiziert statt übernommen. |
| `wh40k_9e.necrons.arkana.dimensional_sanctum` → `grants_ability: wh40k_9e.necrons.unit.dimensional_translocation` | `faction_abilities.yaml:261-270` ↔ `unit_abilities.yaml:956-971` | **YAML→Engine: Ziel-Ability selbst tot** | bestätigt | Der Ziel-Ability `dimensional_translocation` ist `ability_type: triggered`, `trigger.phase: movement`, `stage: start` (kein `any`!) — würde also in `_render_triggered_abilities` theoretisch matchen (`phase_key == "movement"`), aber `effect.type == "deep_strike"` wird von `execute_effect` nicht konsumiert → fällt unter denselben "Apply-Button tut nichts"-Bug wie oben. Der `grants_ability`-Mechanismus selbst (Cryptek erhält fremde Ability) hat zusätzlich **keinen** Konsumenten (kein `grep`-Treffer für `grants_ability` in `src/`). |
| Wargear `effect.type` außerhalb `_apply_persistent_effect` (`complex` mit `handler:` z. B. `canoptekCloak`, `resurrectionOrb`) | `wargear.yaml:28-31,148-151` | **YAML→Engine: Handler nie registriert** | bestätigt | `grep -rn "canoptekCloak\|resurrectionOrb" src/` → 0 Treffer außerhalb der YAML selbst. `_apply_persistent_effect` (`loader.py:803-835`) kennt nur `set_stat/buff_stat/grant_keyword/set_invuln/buff_save/set_fnp` — der `effect:`-Block (nicht `persistent_effects:`) auf Wargear-Ebene wird von `load_wargear_abilities` (`loader.py:860ff`) zu `Ability`-Objekten verarbeitet, aber `effect.type in {"complex","invuln_save","deny_psychic","ignore_cover","heal"}` landet dann in genau demselben `execute_effect`-Nadelöhr, das nur `"heal"` kennt. `deny_psychic` hat einen eigenen Sonderpfad (`load_deny_wargear_names`, `loader.py:838-857`), `heal` funktioniert (Phylactery), aber `complex`/`invuln_save`(als Ability, nicht persistent_effect)/`ignore_cover` sind über den Ability-Pfad **nicht** konsumiert — zu prüfen, ob ein anderer Aufrufer (`combat.py`) sie direkt liest (außerhalb Scope, Anschlussfrage S148). |
| `grant_keyword` (`loader.py:823-826`) — 2 Verwendungen | `wargear.yaml:16-17` (Canoptek Cloak → FLY) | **kein Necron-spezifischer Befund** | bestätigt, **nicht doppelt behandelt** | Wie im Auftrag vorgegeben: Hand of the Phaeron läuft im Stratagem-Audit. Canoptek Cloak selbst ist korrekt verdrahtet (`_apply_persistent_effect` → `set_stat(move)` + `grant_keyword(FLY)`, beide Typen implementiert). |

### Engine→Effekttypen, die tatsächlich konsumiert werden (Gegenprobe „tote Engine-Typen")

Vollständige Grep-Liste aller `effect.type ==`/`ability.effect.type ==`-Vergleiche in `src/`:
`heal` (abilityEngine.py:71, armyCard.py:123), `reroll_hit_1` (commandPhase.py:191,391), `attrition_modifier`
(moralePhase.py:26,55), `reanimate` (armyCard.py:109), `move`+`handler=="fall_back_through_models"`
(movementPhase.py:366-367, stratagemEngine.py), `auto_pass_morale` (stratagemEngine.py:45 — **nur für
Stratagem-Effekte**, nicht für die gleichnamige Unit-Ability „Enslaved Star God"!), `invuln_save`
(stratagemEngine.py:49 — ebenfalls nur Stratagem-Kontext), `buff_roll` (commandPhase.py:391),
`extra_hits`/`alternating_fire`/`debuff_roll`(als Waffen-Effekt)/`extra_attacks` (attackMath.py — Waffenprofile,
anderer Namensraum als Unit-Abilities). **Kein** Necron-`unit_ability`/`faction_ability`-Effekttyp aus
Abschnitt 2 taucht hier auf außer `heal`/`reanimate`/`reroll_hit_1`/`buff_roll` — bestätigt die obige
Lücken-Tabelle als vollständig, keine übersehenen Konsumenten.

---

## 3. Bedingungsvollständigkeit gegen Wahapedia-Wortlaut (Stichproben)

Kein Wortlaut-Fehler in den Kernabilities gefunden, die eine engine-seitige Prüfung haben (Living Metal,
Reanimation Protocols, My Will Be Done, The Lord's Will) — `rule_text` deckt sich mit `docs/work/wahapedia_necrons/`.
Eine Abweichung bestätigt aus dem Code-Kommentar selbst: Szarekhan-Dynastiecode (`subfaction_abilities.yaml:99-104`)
trägt einen expliziten Korrektur-Kommentar zu einer früheren Fehlzuordnung ("Loyal to the Triarch" war falsch) —
bereits behoben, keine neue Aktion nötig.

---

## 4. GAUSS/TESLA-Konzept + Waffen-Inventar

### 4.1 Wahapedia-Befund (Regelbasis, nicht aus dem Gedächtnis)

`docs/work/wahapedia_necrons/faction_overview.txt:722-739` ("Weapon Definitions"):
- **Gauss weapon** = "any weapon whose profile includes the word 'gauss' ... and any Relic that replaces
  such a weapon" — reine **Namenskonvention**, kein eigener Fähigkeitstext pro Waffe nötig.
- **Tesla weapon** = "any weapon whose profile includes the word 'tesla' ... and any Relic that replaces
  such a weapon. **The Voltaic Staff is also a tesla weapon**" (explizite Ausnahme trotz fehlendem
  "tesla" im Namen!).
- `docs/work/wahapedia_core_rules/rules_appendix.txt` enthält **keinen** eigenen GAUSS/TESLA-Glossareintrag
  (0 Treffer) — die Definition lebt ausschließlich in der Necron-Fraktionsdatei.
- Verwendet von: 4 Stratagems (`stratagems.txt:91,157,193,214,271,295` — Disintegration Capacitors,
  Lokhust-spezifisches Damage+1, weitere Varianten), Weapon-Enhancement-Tabellen (`faction_overview.txt:3973-4034`).
- **Kein** GAUSS/TESLA-Unit-Keyword in Wahapedia — die Regeln sprechen immer von "unit ... makes an attack
  with a gauss/tesla weapon", nicht von einer GAUSS/TESLA-Einheit. Ein abgeleitetes Unit-Keyword ist daher
  eine **App-Annäherung** (pragmatisch für die Stratagem-Sichtbarkeitsprüfung), keine 1:1-Regelabbildung —
  sollte in der Spec so benannt werden (z. B. „hat mind. eine Gauss-/Tesla-Waffe im Loadout", nicht
  „ist eine Gauss-Einheit").

### 4.2 Waffen-Inventar (Datei:Zeile, `weapons.yaml` + `relics.yaml`)

**Gauss-Waffen (Name enthält „gauss"), 20 Fundstellen in `weapons.yaml`:**
`relic_gauss_blaster:131`, `gauss_flayer:210`, `gauss_reaper:222`, `gauss_blaster:234`,
`twin_heavy_gauss_cannon:421`, `gauss_cannon:457`, `gauss_destructor:515`, `twin_gauss_blaster:958`,
`twin_gauss_flayer:1032`, `gauss_flayer_array:1072`, `gauss_flux_arc:1260`, `gauss_annihilator:1456`,
`gauss_extrapolator:1468`, `sentry_gauss_cannon:1480`, `heavy_gauss_cannon_fw:1540`,
`twin_gauss_extrapolator:1552` (16 IDs — `grep -c` zählte 34 Textzeilen-Treffer wegen Mehrfachnennung
in Profilen/Kommentaren, tatsächliche IDs: 16). **Wahapedia nennt zusätzlich "Gauss slicers"**
(`units_all.txt:425`) — **keine passende Waffen-ID in `weapons.yaml` gefunden** (grep leer) →
mögliche Datenlücke, als Anschlussfrage an S148/Ziel 5c weiterzugeben, nicht Teil dieses Audits.

**Tesla-Waffen (Name enthält „tesla"), 6 IDs:** `tesla_carbine:246`, `tesla_cannon:469`,
`twin_tesla_destructor:486`, `twin_tesla_carbine:970`, `tesla_sphere:1229`.

**Tesla-Ausnahme ohne „tesla" im Namen:** `relics.yaml:31-54` `wh40k_9e.necrons.relic.voltaikstab`
("Voltaic Staff") — laut Wahapedia explizit Tesla-Waffe, ID/Name enthalten aber weder "tesla" noch
"voltaic" (Deutsch: "Voltaikstab") im Muster. **Belegt, warum eine reine Namens-Substring-Heuristik
in `src/` (INV-4b-widrig ohnehin, da faktisch eine Necron-Sonderregel) systematisch mindestens einen
Fall verfehlt** — das gestützt das `grantsKeyword`-Feld-Konzept gegenüber einer Text-Heuristik.

### 4.3 Konzept `grantsKeyword` (Stakeholder-Entscheid, hier nur Auditbefund + Einordnung)

1. **Datenebene:** `grantsKeyword: GAUSS` / `grantsKeyword: TESLA` als Feld auf Profil- oder Waffen-Ebene
   in `weapons.yaml`/`relics.yaml` (camelCase, wie vom Stakeholder entschieden — bewusster Bruch mit der
   sonst durchgängigen snake_case-Konvention dieser Scope-Dateien, siehe Abschnitt 5). Trägt **explizit**
   pro Waffe, nicht per Namens-Grep — deckt damit auch die Voltaic-Staff-Ausnahme korrekt ab.
2. **Ableitung Einheit ← Waffen (Loader):** generischer Mechanismus in `_apply_wargear`/`load_army`
   (`loader.py`) analog zum bestehenden `wargear_keywords`-Muster (`loader.py:1060-1073`, dort schon für
   `persistent_effects`-`grant_keyword` verdrahtet) — **keine Fraktions-Strings in `src/`**: die Ableitungsregel
   ist "trägt die Einheit eine Waffe mit `grantsKeyword: X` → Einheit erhält Keyword X", unabhängig ob X
   „GAUSS", „TESLA" oder ein zukünftiges Drittes ist. Das ist bereits INV-4b-konform, weil generisch.
3. **Anzeige unitCard:** analog der bestehenden Keyword-Zeile (`_keyword_badge`, `armyCard.py:61-62`) —
   abgeleitete Keywords müssten in die gleiche Badge-Reihe wie `unit.keywords` einfließen (heute nur
   YAML-`keywords:`-Feld + `wargear_keywords`, siehe `loader.py:1073`). Technischer Anschluss: ein zusätzliches
   `derived_keywords`-Set analog `wargear_keywords`, in der Anzeige zusammengeführt.
4. **Bedingungsprüfung:** `stratagem_conditions_met`/`check_conditions` (beide bereits generisch
   keyword-basiert, siehe `abilityEngine.py:55-58` `has_keywords`) müssten **ohne Änderung** funktionieren,
   sobald das abgeleitete Keyword im `unit.keywords`-Set (oder einem zusammengeführten Lookup) landet —
   das ist der entscheidende Vorteil ggü. der reinen `_detect_weapon_special`-Text-Erkennung: Stratagem-
   Sichtbarkeit ist heute (Abschnitt 2, Disintegration Capacitors/Malevolent Arcing) **nicht** gegated,
   weil `has_keywords: [GAUSS]` als `conditions`-Eintrag aktuell keine Entsprechung im Datenmodell hat.

### 4.4 Abgrenzung zu `_detect_weapon_special` (Empfehlung)

**Koexistent, nicht ablösen.** Begründung: `_detect_weapon_special` (`attackMath.py:141-163`) arbeitet
**pro abgefeuertem Waffenprofil** (z. B. Tesla-Extra-Hits beim konkreten Schuss dieser einen Waffe) —
das ist korrekt granular, weil eine Einheit gemischt bestückt sein kann (ein Modell Gauss Blaster,
ein anderes Tesla Carbine nach Wargear-Swap, siehe `units_all.txt:288`). Ein Unit-Keyword würde diese
Granularität verlieren, wenn es die Extra-Hits-Logik ersetzen sollte. `grantsKeyword` wird stattdessen
für die andere Fragestellung gebraucht: **"trägt diese Einheit überhaupt eine Gauss-/Tesla-Waffe"**
(Sichtbarkeits-Gate für Stratagems, die pauschal an "unit ... with a gauss weapon" anknüpfen, nicht an
das einzelne Profil). Beide Mechanismen bedienen unterschiedliche Fragen im selben Regelbereich —
keine Redundanz, kein Ablöse-Bedarf.

---

## 5. snake_case-Feld-Inventar (Necron-Ability-Scope, für camelCase-Migrationsplan)

Vollzähliges Vorkommen aller Top-Level-Feldnamen in den 6 Scope-Dateien (`grep -ohE '^\s*[a-z_]+:'`,
gezählt über `faction_abilities.yaml`, `unit_abilities.yaml`, `subfaction_abilities.yaml`, `wargear.yaml`,
`relics.yaml`, `arkana.yaml`):

| Feld | Fundstellen | Feld | Fundstellen | Feld | Fundstellen |
|---|---|---|---|---|---|
| name_en | 112 | phase | 93 | effect | 93 |
| type | 92 | ability_type | 86 | trigger | 80 |
| timing | 80 | rule_text | 80 | player | 80 |
| conditions | 80 | source | 77 | target | 69 |
| stage | 68 | unit_id | 45 | power_delta | 24 |
| modifier | 22 | within_inches | 20 | badge_label | 19 |
| handler | 15 | applies_to | 13 | amount | 13 |
| ability_en | 13 | value | 12 | text_de | 12 |
| stat | 12 | secondary | 12 | primary | 12 |
| keywords | 12 | cost_pts | 12 | category | 12 |
| event | 9 | abilities | 9 | target_keywords | 7 |
| subfaction_affinity | 6 | replaces | 6 | is_relic | 6 |
| directives | 6 | any_of | 6 | roll_threshold | 5 |
| once_per_battle | 5 | weapon_type | 4 | strength | 4 |
| range_inches | 4 | persistent_effects | 4 | damage | 4 |
| ap | 4 | abilities_en | 4 | revive | 3 |
| profiles | 3 | faction | 3 | extra_uses | 3 |
| bonus | 3 | wounds | 2 | unit_not_destroyed | 2 |
| threshold | 2 | roll | 2 | keyword | 2 |
| invuln_save | 2 | grants_ability | 2 | enforcement | 2 |
| did_not_move | 2 | affects | 2 | (37 weitere Felder mit je 1 Fundstelle, s. u.) | |

Felder mit genau 1 Fundstelle: `weapon, triggered_effects, target_rule, target_keywords_any, success_on,
subfactions, subfaction_label, subfaction_field, set_damage_to, selector_label, round_choice_label,
roll_type, restriction, reroll, remove, prompt_text, needs_healing, modifies_ability,
min_distance_from_enemy, max, hit_modifier, effects, cover_type, condition, bonus_vs_character, arkana,
aoe_radius_inches, active_text, ability_id`.

**Befund:** Der komplette Scope ist **durchgängig snake_case** — kein einziges camelCase-Feld existiert
heute in diesen 6 Dateien. Der stakeholder-entschiedene `grantsKeyword` wäre damit das **erste**
bewusst camelCase benannte Feld in diesem Bereich — Migrationsplan sollte diesen Bruch explizit
dokumentieren (z. B. in `docs/spec/loader_contract.md`), nicht stillschweigend mischen.

---

## 6. Fixing-Plan-Vorschlag für S148 (Häppchen ≤ Effort M)

| # | Aufgabe | Effort | Dateien | Abhängigkeit |
|---|---|---|---|---|
| 1 | **`grantsKeyword`-Feld einführen** (Gate/Konsens — Stakeholder-Entscheid liegt zwar vor, aber Feldname/Schema-Ort ist noch zu fixieren): Feld in `weapons.yaml`-Profilen der 16 Gauss- + 5 Tesla-Waffen + `relics.yaml` Voltaic Staff setzen; Loader-Ableitung Einheit←Waffe (neues `derived_keywords`-Set analog `wargear_keywords`) | M | `data/wh40k_9e/necrons/weapons.yaml`, `relics.yaml`, `src/gameObjects/loader.py`, `tests/gameObjects/test_loader.py` | keiner |
| 2 | **unitCard-Anzeige** der abgeleiteten Keywords (GAUSS/TESLA-Badges in der Keyword-Zeile) | S | `src/uiLayout/unitCard.py` bzw. `armyCard.py:61-62`, manuelle UI-Verifikation Pflicht (Render-Code) | Aufgabe 1 |
| 3 | **Stratagem-`conditions`-Lücke schließen**: `has_keywords: [GAUSS]` bei Disintegration Capacitors, `[TESLA]` bei Malevolent Arcing eintragen, gegen `stratagem_conditions_met` testen | S | `data/wh40k_9e/necrons/stratagems.yaml:249-263,265-275`, `tests/gameMechanic/test_ability_engine.py` oder passendes Stratagem-Test-File | Aufgabe 1 |
| 4 | **Apply-Button-Bug für tote `triggered`-Effekttypen fixen** (Abschnitt 2, Zeile 2 der Lücken-Tabelle): entweder (a) Button/Log ausblenden wenn `effect.type` nicht in einer bekannten "ausführbaren" Menge liegt (Minimal-Fix, kein neues Effektsystem), oder (b) je 1-2 Effekttypen (`buff_stat`, `reroll_wound_1`, `toggle_keyword`) real verdrahten. Empfehlung: (a) zuerst als Sofortfix (verhindert Falschbuchung "healed"/fälschliches Sperren), (b) als separate Pakete je Effekttyp | M (für a) / je S (für b, pro Typ) | `src/uiLayout/armyCard.py:90-151`, `src/gameMechanic/abilityEngine.py:69-78` | keiner — höchste Priorität, da aktiv irreführendes UI-Verhalten, nicht nur fehlende Funktion |
| 5 | **Activated-Ability-Renderer erweitern** um mind. 1 weiteren Effekttyp (Kandidat: `buff_charge_and_invuln` für Chronometron/Master Chronomancer — am häufigsten benutzte Fähigkeit dieser Gruppe) | M | `src/gameMechanic/commandPhase.py:378-410` | keiner |
| 6 | **`grants_ability`-Mechanismus (Dimensional Sanctum) verdrahten oder bewusst als Class-B markieren** — aktuell weder Konsument noch Hinweis | S | `data/wh40k_9e/necrons/faction_abilities.yaml:254-270`, `src/gameMechanic/abilityEngine.py` | Aufgabe 4/5 (gleicher Nadelöhr-Bereich) |

**Nicht in S148, sondern als offene Frage weitergeben:** Reaktive Events (`after_enemy_attack`-Familie
außerhalb Reanimation Protocols, `model_destroyed`, `round_start`, `pre_battle`) — Konsum-Prüfung liegt
in `combat.py`/`phaseRunner.py`, außerhalb dieses Scopes; eigener Audit-Auftrag empfohlen. Ebenso
"Gauss slicers" (Wahapedia-Waffe ohne `weapons.yaml`-Entsprechung) und ob `invuln_save`/`fnp` für
Quantum-Shielding-artige Einheiten bereits statisch in `units.yaml` steht.

---

## 7. Bestandsaufnahme-Nachweis (S144-M1)

Vollständig gelesen: `faction_abilities.yaml` (434 Z.), `unit_abilities.yaml` (970 Z.),
`subfaction_abilities.yaml` (157 Z.), `wargear.yaml` (189 Z.), `relics.yaml` (97 Z.), `arkana.yaml` (141 Z.),
`abilityEngine.py` (594 Z., komplett), `loader.py` (Ausschnitte 1-100, 750-880, 1000-1075 — gezielt um
`_apply_persistent_effect`/`grant_keyword`/`_apply_wargear` laut Auftrag), `commandPhase.py` (150-410),
`armyCard.py` (60-180), `attackMath.py` (120-180), `moralePhase.py` (Ausschnitt `_ATTRITION_EFFECT_TYPE`),
`gameState.py` (`PHASES`-Liste), `stratagems.yaml` (Gauss/Tesla-Treffer + Kontext), `weapons.yaml`
(vollständige ID-Liste Gauss/Tesla + Beispielprofile), `units.yaml` (grep auf GAUSS/TESLA-Keyword-Strings),
`docs/work/wahapedia_necrons/{faction_overview,stratagems,units_all}.txt` (gezielte Greps),
`docs/work/wahapedia_core_rules/rules_appendix.txt` (Gauss/Tesla-Grep, 0 Treffer — Negativbefund
dokumentiert statt übergangen). `git diff --stat`/`git status --short` auf `subfaction_abilities.yaml`
zu Beginn und am Ende der Recherche geprüft — unverändert.
