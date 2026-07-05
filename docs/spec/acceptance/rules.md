# Regel-Katalog: Akzeptanzkriterien

Zweck: Dieser Katalog ist der **Nenner** für die Abdeckungsmessung — die Gesamtheit der
9E-Spielregeln, gegen die wir Implementierungs- und Test-Coverage als Prozentsatz messen.

## Regelklassen

- **Klasse A** — die App rechnet/erzwingt die Regel (Würfelschwellen, Tabellen, Modifikatoren).
  Akzeptanzkriterium: Code bildet die Regel ab **und** ein Test prüft das Verhalten.
- **Klasse B** — nur am physischen Tisch prüfbar (Abstände, Sichtlinien, Kohärenz).
  Akzeptanzkriterium: App zeigt einen **Hinweis**; ein Test prüft, dass der Hinweis erscheint.
- **Klasse C** — **Hybrid**: Ein App-erzwingbarer Anteil **plus** ein reiner Tisch-Anteil
  (z. B. Locked in Combat: das `in_melee`-Flag erzwingt die App, die Distanzmessung nicht).
  Akzeptanzkriterium: App erzwingt/zeigt ihren Anteil + Test darauf. Zählt als eigene Spalte.

## Format

Jede Regel ist ein `### R-<BEREICH>-<NN>`-Eintrag. Feldkonventionen:

- **status**: `implementiert` | `offen` (`offen` = Regel existiert im 9E-Regelwerk, App bildet sie
  noch nicht ab — trotzdem aufnehmen, damit der Nenner echt ist).
- **getestet**: `ja — <testname>` | `nein`. Bei `ja` **immer** den Testnamen nennen, damit das
  Gate die Regel↔Test-Verknüpfung maschinell prüfen kann. `getestet: nein` bei
  `status: implementiert` ist eine **Schuld** (Ratchet → darf nur schrumpfen).
- **code**: `datei:funktion` — **keine Zeilennummern** (driften). `—` wenn `status: offen`.

IDs sind stabil und werden nie wiederverwendet. Der Katalog wächst pro Bereich
(diese Datei: Attackenabfolge/Combat (Schießen + Nahkampf), Command Phase, Movement Phase,
Charge Phase, Morale Phase, Psychic Phase, Battle-Round-Struktur).

---

## Bereich: Attackenabfolge / Combat

### R-COMBAT-01
- **klasse**: A
- **status**: implementiert
- **getestet**: ja — test_hit_no_mods_returns_base
- **quelle**: core_rules.txt — "1. Hit Roll" (Making Attacks)
- **code**: combat.py:resolve_attack
- **regel**: Trefferwurf (Schießen): D6 ≥ BS des Schützen = Treffer; unmodifizierte 1 verfehlt immer, unmodifizierte 6 trifft immer.

### R-COMBAT-02
- **klasse**: A
- **status**: implementiert
- **getestet**: ja — test_hit_no_mods_returns_base
- **quelle**: core_rules.txt — "1. Hit Roll" (Making Attacks)
- **code**: combat.py:resolve_attack
- **regel**: Trefferwurf (Nahkampf): D6 ≥ WS des Angreifers = Treffer; gleiche 1/6-Sonderregeln wie beim Schießen.

### R-COMBAT-03
- **klasse**: A
- **status**: implementiert
- **getestet**: ja — test_hit_capped_at_plus1 / test_hit_capped_at_minus1
- **quelle**: core_rules.txt — "Hit and wound rolls cannot be modified by more than -1 or +1"
- **code**: combat.py:resolve_attack_modifiers
- **regel**: Trefferwurf-Modifikatoren werden auf ±1 gekappt (kumuliert, dann gecappt).

### R-COMBAT-04
- **klasse**: A
- **status**: implementiert
- **getestet**: ja — test_double_strength_wounds_on_2 / test_strength_greater_wounds_on_3 / test_half_strength_wounds_on_6
- **quelle**: core_rules.txt — "2. Wound Roll" (Wound Roll Tabelle)
- **code**: combat.py:wound_threshold
- **regel**: Verwundungstabelle: S≥2×T→2+, S>T→3+, S=T→4+, S<T→5+, S≤T/2→6+.

### R-COMBAT-05
- **klasse**: A
- **status**: implementiert
- **getestet**: ja — test_wound_modifier_applies / test_hit_and_wound_mods_independent
- **quelle**: core_rules.txt — "Hit and wound rolls cannot be modified by more than -1 or +1"
- **code**: combat.py:resolve_attack_modifiers
- **regel**: Verwundungswurf-Modifikatoren werden auf ±1 gekappt (kumuliert, dann gecappt).

### R-COMBAT-06
- **klasse**: A
- **status**: implementiert
- **getestet**: ja — test_hit_minimum_2
- **quelle**: core_rules.txt — "Hit roll … minimum 2+" / "Wound roll … minimum 2+"
- **code**: combat.py:resolve_attack_modifiers
- **regel**: Modifizierte Treff- und Verwundungsschwellen können nie unter 2+ fallen (Minimum 2).

### R-COMBAT-07
- **klasse**: A
- **status**: implementiert
- **getestet**: ja — test_save_with_ap / test_ap_minus2_worsens_save
- **quelle**: core_rules.txt — "4. Saving Throw" (Making Attacks)
- **code**: combat.py:resolve_save
- **regel**: Rettungswurf: AP verschlechtert den Rüstungswurf (armour_eff = save + |AP|); schlägt fehl wenn Ergebnis < modifizierter Sv. Unmodifizierte 1 schlägt immer fehl.

### R-COMBAT-08
- **klasse**: A
- **status**: implementiert
- **getestet**: ja — test_save_invuln_better_than_armour / test_invul_save_used_when_better
- **quelle**: core_rules.txt — "Invulnerable Saves" (Advanced Rules)
- **code**: combat.py:resolve_save
- **regel**: Invulnerable Save ist niemals durch AP modifiziert; der Spieler wählt den besseren der beiden Saves (armour vs invuln).

### R-COMBAT-09
- **klasse**: A
- **status**: implementiert
- **getestet**: ja — test_ability_invuln_save_picks_best_of_multiple
- **quelle**: core_rules.txt — "Invulnerable Saves" — "If a model has more than one invulnerable save, it can only use one of them"
- **code**: ability_engine.py:ability_invuln_save
- **regel**: Hat ein Modell mehrere Invulnerable Saves, wird nur der beste verwendet (kleinster Zahlenwert). Die „bester von mehreren"-Auswahl liegt in `ability_invuln_save` (`min(...)` über alle aktiven Invuln-Effekte), NICHT in `resolve_save` (nimmt einen Einzelwert).

### R-COMBAT-10
- **klasse**: A
- **status**: implementiert
- **getestet**: ja — test_damage_1_per_failed_save / test_damage_2_per_failed_save
- **quelle**: core_rules.txt — "5. Inflict Damage"
- **code**: combat.py:resolve_attack
- **regel**: Schaden pro fehlgeschlagenem Rettungswurf = D-Charakteristik der Waffe; Modell verliert entsprechend viele Wunden.

### R-COMBAT-11
- **klasse**: A
- **status**: implementiert
- **getestet**: ja — test_apply_damage_multiwound_caps_damage_to_front_model
- **quelle**: core_rules.txt — "5. Inflict Damage — excess damage inflicted by that attack is lost"
- **code**: unit_mutations.py:apply_damage
- **regel**: Überzähliger Schaden, der ein Einzelmodell überschreitet (non-mortal), verfällt und hat keinen Effekt auf andere Modelle.

### R-COMBAT-12
- **klasse**: A
- **status**: implementiert
- **getestet**: ja — test_fnp_normal / test_fnp_reduces_damage
- **quelle**: core_rules.txt — "Ignoring Wounds" (Advanced Rules)
- **code**: combat.py:resolve_fnp
- **regel**: Feel No Pain (FNP): Für jeden Schadenspunkt darf das Modell versuchen, diesen zu ignorieren (Wurf ≥ FNP-Schwelle); jede Wunde nur durch eine einzige Ignorieren-Regel geschützt.

### R-COMBAT-13
- **klasse**: A
- **status**: implementiert
- **getestet**: ja — test_user_keyword / test_plus_one / test_times_two
- **quelle**: core_rules.txt — "Weapon Strength … 'User' … modifier '+1' … 'x2'"
- **code**: attack_math.py:_parse_strength / combat.py:resolve_weapon_strength
- **regel**: Waffenstärke wird aus der Notation aufgelöst: fester Wert, "User" (= Trägerstärke), "+N", "×N", "-N".

### R-COMBAT-14
- **klasse**: A
- **status**: implementiert
- **getestet**: ja — test_apply_damage_attacks_wounds_on_front
- **quelle**: core_rules.txt — "3. Allocate Attack — if a model … has already lost any wounds … must be allocated to that model"
- **code**: unit_mutations.py:apply_damage
- **regel**: Angegriffene Modelle mit bereits verlorenen Wunden müssen zuerst weitere Angriffe zugeteilt bekommen (Front-Modell-Prinzip).

### R-COMBAT-15
- **klasse**: A
- **status**: implementiert
- **getestet**: ja — test_apply_damage_mortal_wounds_kill_multiple_1wound_models / test_apply_damage_mortal_wound_bypasses_spillover_cap
- **quelle**: core_rules.txt — "Mortal Wounds" (Advanced Rules)
- **code**: unit_mutations.py:apply_damage
- **regel**: Mortal Wounds: kein Verwundungs- oder Rettungswurf; jede Mortal Wound = 1 Schadenspunkt. Überzähliger Schaden durch Mortal Wounds verfällt NICHT, sondern geht auf das nächste Modell über.

### R-COMBAT-16
- **klasse**: A
- **status**: implementiert
- **getestet**: ja — test_heavy_penalty_when_advanced / test_heavy_no_penalty_when_not_advanced
- **quelle**: core_rules.txt — "HEAVY … subtract 1 from the hit rolls … if the firing model's unit has moved"
- **code**: combat.py:resolve_attack_modifiers
- **regel**: Heavy-Waffe (INFANTRY): -1 auf Trefferwürfe, wenn die Einheit sich in dieser Runde bewegt hat (Advance gilt ebenfalls als Bewegung).

### R-COMBAT-17
- **klasse**: C
- **status**: implementiert
- **getestet**: ja — test_rapid_fire_caption_shown_for_rapid_fire_weapon
- **quelle**: core_rules.txt — "RAPID FIRE … double the number of attacks … if its target is within half the weapon's range"
- **code**: _common.py:_rapid_fire_caption
- **regel**: Rapid-Fire-Waffe: Angriffszahl wird verdoppelt, wenn das Ziel innerhalb der halben Reichweite ist. App-Anteil: zeigt nur einen Hinweis-Caption (`[RAPID FIRE · ½ = …"]`); die Verdopplung selbst rechnet die App NICHT — das ist Tisch-Anteil. (S69-Befund: war fälschlich Klasse A „App rechnet" mit `code: attack_math` — `_compute_attacks` ist range-agnostisch und verdoppelt nicht. Auf Klasse C korrigiert.)

### R-COMBAT-18
- **klasse**: A
- **status**: offen
- **getestet**: nein
- **quelle**: core_rules.txt — "ASSAULT … subtract 1 from hit rolls if the firing model's unit has Advanced"
- **code**: —
- **regel**: Assault-Waffe: -1 auf Trefferwürfe, wenn die eigene Einheit in dieser Runde Advanced hat (Schießen bleibt erlaubt).

### R-COMBAT-19
- **klasse**: A
- **status**: offen
- **getestet**: nein
- **quelle**: core_rules.txt — "PISTOL … can be shot even if … within Engagement Range … must target … within Engagement Range"
- **code**: —
- **regel**: Pistol-Waffe: Darf auch aus dem Nahkampf heraus geschossen werden; muss eine Einheit in Engagement Range anvisieren; nicht mit anderen Waffentypen kombinierbar.

### R-COMBAT-20
- **klasse**: A
- **status**: offen
- **getestet**: nein
- **quelle**: core_rules.txt — "Blast Weapons" (Advanced Rules)
- **code**: —
- **regel**: Blast-Waffe: Mindestens 3 Angriffe gegen Einheiten mit 6–10 Modellen; maximal mögliche Angriffe gegen 11+ Modelle; nie gegen Einheiten in Engagement Range der eigenen Einheit.

### R-COMBAT-21
- **klasse**: A
- **status**: offen
- **getestet**: nein
- **quelle**: core_rules.txt — "GRENADE … only one model … can resolve attacks with it"
- **code**: —
- **regel**: Grenade-Waffe: Nur ein Modell pro Einheit pro Schießphase darf eine Granate werfen, unabhängig von der Einheitengröße.

### R-COMBAT-22
- **klasse**: A
- **status**: offen
- **getestet**: nein
- **quelle**: core_rules.txt — "Big Guns Never Tire" (Advanced Rules)
- **code**: —
- **regel**: VEHICLE/MONSTER: Dürfen aus dem Nahkampf schießen, aber nur Ziele in Engagement Range. Heavy-Waffe im Nahkampf: zusätzlich -1 auf Trefferwürfe, falls noch Feinde in Engagement Range.

### R-COMBAT-23
- **klasse**: A
- **status**: offen
- **getestet**: nein
- **quelle**: core_rules.txt — "Overwatch" (Charge Phase)
- **code**: —
- **regel**: Overwatch: Schießangriff vor dem Charge-Würfelwurf; trifft nur auf unmodifizierter 6, unabhängig von BS und Modifikatoren.

### R-COMBAT-24
- **klasse**: A
- **status**: offen
- **getestet**: nein
- **quelle**: core_rules.txt — "Re-rolls … happen before modifiers … A dice can never be re-rolled more than once"
- **code**: —
- **regel**: Würfelwiederholen (Re-rolls): Vor Modifikatoren angewendet; ein Würfel höchstens einmal neu gewürfelt. "Unmodified" bezieht sich auf das Ergebnis nach Re-roll, vor Modifikatoren.

### R-COMBAT-25
- **klasse**: A
- **status**: offen
- **getestet**: nein
- **quelle**: core_rules.txt — "Automatically hit … no hit roll is made"
- **code**: — (erkannt in attack_math.py:_detect_weapon_special "auto_hit", aber in der Berechnungslogik **nicht erzwungen** → Teil-Implementierung)
- **regel**: Automatischer Treffer (z. B. Tesla, Auto-hit-Fähigkeiten): Kein Trefferwurf; jeder Angriff gilt als Treffer.

### R-COMBAT-26
- **klasse**: A
- **status**: implementiert
- **getestet**: ja — test_save_bonus_does_not_improve_invuln
- **quelle**: core_rules.txt — "Invulnerable Saves — never modified by a weapon's Armour Penetration"
- **code**: combat.py:resolve_save
- **regel**: Rüstungs-Bonus-Modifikatoren (z. B. Cover, Stratagems) verbessern den Rüstungswurf, aber nicht den Invulnerable Save.

### R-COMBAT-27
- **klasse**: B
- **status**: offen
- **getestet**: nein
- **quelle**: core_rules.txt — "Select Targets … at least one model … must be within range … and be visible to the shooting model"
- **code**: —
- **regel**: Schuss-/Sichtlinie: Mindestens ein Modell der Zieleinheit muss sichtbar und in Reichweite sein. Nur am Tisch prüfbar; App kann höchstens einen Hinweis anzeigen.

### R-COMBAT-28
- **klasse**: B
- **status**: offen
- **getestet**: nein
- **quelle**: core_rules.txt — "Select Targets … within range (i.e. within the distance of the Range characteristic)"
- **code**: —
- **regel**: Reichweitenmessung: Entfernung zwischen den nächsten Punkten der Bases (oder Hulls). Nur am Tisch prüfbar; App kann höchstens einen Hinweis anzeigen.

### R-COMBAT-29
- **klasse**: B
- **status**: offen
- **getestet**: nein
- **quelle**: core_rules.txt — "Terrain and Cover" (Shooting Phase / Making Attacks)
- **code**: —
- **regel**: Cover: Bestimmte Geländemerkmale gewähren +1 auf den Rettungswurf (Armour, nicht Invuln). Ob eine Einheit im Cover steht, ist nur am Tisch prüfbar; App kann höchstens einen Hinweis anzeigen.

### R-COMBAT-30
- **klasse**: C
- **status**: implementiert
- **getestet**: ja — test_in_melee_cannot_shoot / test_pistol_in_melee_can_shoot
- **quelle**: core_rules.txt — "Locked in Combat … cannot make attacks with ranged weapons while … within Engagement Range"
- **code**: shootingPhase.py:can_shoot
- **regel**: Locked in Combat: Hybrid — die App **erzwingt** die Sperre über das `in_melee`-Flag (App-Anteil); ob eine Einheit tatsächlich in Engagement Range (1" horizontal, 5" vertikal) steht, ist Tisch-Anteil.

### R-COMBAT-31
- **klasse**: B
- **status**: offen
- **getestet**: nein
- **quelle**: core_rules.txt — "Look Out, Sir" (Advanced Rules)
- **code**: —
- **regel**: Look Out, Sir: CHARACTER mit ≤9 Wunden kann nicht beschossen werden, wenn eine befreundete Einheit mit 1+ VEHICLE/MONSTER oder 3+ non-CHARACTER-Modellen in 3" Nähe ist (außer es ist das nächste Ziel). Nur am Tisch prüfbar; App kann einen Hinweis anzeigen.

### R-COMBAT-32
- **klasse**: A
- **status**: implementiert
- **getestet**: ja — test_non_charged_waits_while_charged_pending
- **quelle**: core_rules.txt — "Charging Units Fight First" (Fight Phase)
- **code**: fightPhase.py:can_fight_now
- **regel**: In der Kampfphase kämpfen Einheiten, die in dieser Runde gechargt haben, zuerst — vor allen anderen Einheiten.

### R-COMBAT-33
- **klasse**: A
- **status**: offen
- **getestet**: nein
- **quelle**: core_rules.txt — "Which Models Fight … within Engagement Range … or within ½\" of another model … within ½\" of an enemy unit"
- **code**: —
- **regel**: Im Nahkampf dürfen nur Modelle angreifen, die in Engagement Range eines Feindes stehen oder innerhalb ½" eines eigenen Modells, das selbst innerhalb ½" eines Feindes steht.

### R-COMBAT-34
- **klasse**: A
- **status**: offen
- **getestet**: nein
- **quelle**: core_rules.txt — "Mortal Wounds … in addition to the normal damage … the target unit still suffers the mortal wounds, even if the normal damage is … saved"
- **code**: —
- **regel**: Mortal Wounds als Zusatzschaden: Werden immer angewandt, auch wenn der normale Waffenschaden durch den Rettungswurf geblockt wurde.

---

## Bereich: Command Phase

### R-CMD-01
- **klasse**: A
- **status**: implementiert
- **getestet**: ja — test_next_phase_setup_goes_to_command
- **quelle**: core_rules.txt — "COMMAND PHASE … Both players muster strategic resources"
- **code**: game_state.py:next_phase
- **regel**: Die Command Phase ist die erste Phase jedes Spielerzugs; sie folgt unmittelbar auf das Setup und wird bei jedem Phasenwechsel über `next_phase` korrekt eingeleitet.

### R-CMD-02
- **klasse**: A
- **status**: implementiert
- **getestet**: ja — test_next_phase_does_not_award_cp_on_player_switch
- **quelle**: core_rules.txt — "at the start of your Command phase, before doing anything else, you gain 1 Command point"
- **code**: commandPhase.py:_render_faction_actions
- **regel**: Zu Beginn der Command Phase erhält die aktive Spielerseite 1 CP — manuell per Button bestätigt und über das Flag `cp_granted_this_phase` auf einmal pro Phase gesperrt; `next_phase` selbst vergibt kein CP.

### R-CMD-03
- **klasse**: A
- **status**: implementiert
- **getestet**: ja — test_matched_play_is_battle_forged / test_open_play_is_not_battle_forged
- **quelle**: core_rules.txt — "If your army is Battle-forged, then at the start of your Command phase … you gain 1 Command point"
- **code**: commandPhase.py:can_gain_command_point
- **regel**: Der CP-Gewinn pro Command Phase ist regelseitig an den Battle-forged-Status gebunden. `can_gain_command_point(game_mode)` gibt True für `matched`/`crusade`, False für `open`. Der Grant-Button ist für Open-Play-Armeen ausgeblendet.

### R-CMD-04
- **klasse**: A
- **status**: implementiert
- **getestet**: ja — test_combat_patrol_starts_at_3_cp
- **quelle**: core_rules.txt — Battle-forged CP-Bonus / Spielgröße: Combat Patrol 3 · Incursion 6 · Strike Force 12 · Onslaught 18
- **code**: game_state.py:init_state
- **regel**: Der CP-Startvorrat richtet sich nach der Spielgröße (`CP_BY_GAME_SIZE`: 3/6/12/18). (Schuld: kein Test prüft die vier Stufen.)

### R-CMD-05
- **klasse**: A
- **status**: implementiert
- **getestet**: ja — test_clickable_when_all_conditions_met / test_greyed_when_insufficient_cp / test_greyed_when_already_used_this_phase
- **quelle**: core_rules.txt — "CPs … can be spent to utilise Stratagems"
- **code**: stratagem.py:stratagem_visibility
- **regel**: Stratagems kosten CP; `stratagem_visibility()` schaltet einen Button auf `clickable` (CP ausreichend, nicht verwendet), `greyed` (CP fehlen oder bereits genutzt) oder `hidden` (Bedingungen/Phase nicht erfüllt). Das YAML-Feld `stage` ist bewusst KEIN Sichtbarkeits-Kriterium: 9E kodifiziert nur die Phasen-Bindung; das Timing innerhalb der Phase („at the start of…"/„at the end of…") steht im `rule_text` des Expanders (Plan 040, Test: test_start_and_end_stage_stratagems_visible_in_matching_phase).

### R-CMD-06
- **klasse**: A
- **status**: implementiert
- **getestet**: ja — test_resets_used_stratagem_ids
- **quelle**: core_rules.txt — "once per phase" / "once per battle" Stratagem-Restriktionen
- **code**: game_state.py:_reset_phase_state
- **regel**: Die Menge der in dieser Phase genutzten Stratagems (`used_stratagem_ids`) wird bei jedem Phasenwechsel geleert, sodass Einmal-pro-Phase-Stratagems regelkonform zurückgesetzt werden.

### R-CMD-07
- **klasse**: A
- **status**: offen
- **getestet**: nein
- **quelle**: core_rules.txt — "Each player can only gain or have refunded a total of 1 CP per battle round as the result of such rules"
- **code**: —
- **regel**: CP-Rückerstattungen/-Gewinne aus Abilities oder Stratagems dürfen insgesamt höchstens 1 CP pro Spielrunde ergeben. Die App erzwingt dieses Limit nicht.

### R-CMD-08
- **klasse**: B
- **status**: offen
- **getestet**: nein
- **quelle**: core_rules.txt — "Battle-forged CP bonus and CPs gained at start of Command phase via mission special rules are exempt from this limit"
- **code**: —
- **regel**: Der Battle-forged-CP-Bonus und mission-bedingte CP-Gewinne in der Command Phase sind vom 1-CP-pro-Runde-Limit ausgenommen. Nur am Tisch buchführbar; App kann höchstens einen Hinweis zeigen.

### R-CMD-09
- **klasse**: A
- **status**: implementiert
- **getestet**: ja — test_resolve_command_start_returns_living_metal / test_resolve_command_start_ork_returns_empty
- **quelle**: core_rules.txt — "Some abilities found on datasheets … are used in your Command phase"
- **code**: commandPhase.py:resolve_command_start
- **regel**: Datasheet-Fähigkeiten, die in der Command Phase auslösen (`trigger.phase = "command"`, `timing = "phase_start"`), werden generisch für alle berechtigten Einheiten der aktiven Seite ermittelt.

### R-CMD-10
- **klasse**: A
- **status**: implementiert
- **getestet**: ja — test_adds_buff_to_empty_active_buffs / test_buff_records_correct_effect_type
- **quelle**: core_rules.txt — "Some abilities found on datasheets … are used in your Command phase"
- **code**: unit_mutations.py:apply_buff_to_unit (Schreibstelle: uiLayout/unitCard.py)
- **regel**: Aktivierte Command-Phase-Fähigkeiten vom Typ `buff_roll`/`reroll_hit_1` werden pro ausgewählter Einheit gerendert und ihr Effekt als `active_buffs` im Einheitenzustand eingetragen. `apply_buff_to_unit` ist idempotent für dieselbe ability_id.

### R-CMD-11
- **klasse**: A
- **status**: implementiert
- **getestet**: ja — test_success_returns_cp_delta / test_lock_prevents_second_resolution
- **quelle**: core_rules.txt — "Some abilities found on datasheets … are used in your Command phase"
- **code**: commandPhase.py:resolve_gain_cp_roll
- **regel**: Fähigkeiten mit `gain_cp_roll`-Effekt (Würfelwurf am Phase-Start; bei Schwellenwert+ erhält die aktive Seite CP) sind einmal pro Command Phase auflösbar und danach gesperrt. `resolve_gain_cp_roll` wirft ValueError bei Doppelaufruf.

### R-CMD-12
- **klasse**: A
- **status**: implementiert
- **getestet**: ja — test_command_re_roll_has_phase_reactive_timing
- **quelle**: core_rules.txt — "COMMAND RE-ROLL … Use this Stratagem after you have made a hit roll, a wound roll, a damage roll, a saving throw, an Advance roll, a charge roll, a Psychic test … 1 CP"
- **code**: stratagem.py:stratagem_visibility
- **regel**: Command Re-Roll (1 CP, Core-Stratagem) erlaubt das Wiederholen eines einzelnen Würfels; als `phase_reactive` klassifiziert wird es in der UI nicht proaktiv angeboten (reaktiver Einsatz nach einem Würfelwurf am Tisch). (Schuld: kein Test prüft die reaktive Klassifizierung von `command_re_roll`.)

### R-CMD-13
- **klasse**: B
- **status**: offen
- **getestet**: nein
- **quelle**: core_rules.txt — "some missions have rules that take place in the Command phase"
- **code**: —
- **regel**: Missionsspezifische Regeln, die in/zum Ende der Command Phase wirken (z. B. VP-Vergabe bei progressiven Missionen), sind nur am Tisch auswertbar; die App bietet dafür keinen automatischen Mechanismus.

### R-CMD-14
- **klasse**: A
- **status**: implementiert
- **getestet**: ja — test_next_phase_advances_index_within_turn
- **quelle**: core_rules.txt — "Once you and your opponent have resolved all of these rules … progress to your Movement phase"
- **code**: game_state.py:next_phase
- **regel**: Nach Abschluss der Command Phase (Phasenwechsel-Bestätigung) wechselt der Zustand in die Movement Phase; der Phasenindex wird innerhalb des Zugs korrekt fortgeschrieben.

---

## Bereich: Movement Phase

### R-MOVE-01
- **klasse**: A
- **status**: offen
- **getestet**: nein
- **quelle**: core_rules.txt — "No unit can be selected to move more than once in each Movement phase"
- **code**: —
- **regel**: Jede Einheit darf pro Bewegungsphase höchstens einmal zum Bewegen ausgewählt werden; eine zweite Bewegungsauswahl ist unzulässig. (App erzwingt keine harte Sperre — die Bewegungs-Buttons bleiben nach Auswahl klickbar.)

### R-MOVE-02
- **klasse**: C
- **status**: implementiert
- **getestet**: ja — test_scenario_3_normal_move / test_scenario_8_advanced_sets_flag
- **quelle**: core_rules.txt — "it can either make a Normal Move, it can Advance, or it can Remain Stationary"
- **code**: movementPhase.py:_active_movement
- **regel**: Eine Einheit außerhalb der Engagement Range wählt genau eine von drei Bewegungsoptionen: Normal Move, Advance oder Remain Stationary; die App erzwingt die Auswahl per Button (App-Anteil), die zurückgelegte Distanz wird am Tisch gemessen (Tisch-Anteil).

### R-MOVE-03
- **klasse**: C
- **status**: implementiert
- **getestet**: ja — test_scenario_9_in_melee_stationary_stationary_allowed
- **quelle**: core_rules.txt — "within Engagement Range of any enemy models … it can either Remain Stationary or it can Fall Back"
- **code**: movementPhase.py:_active_movement
- **regel**: Eine Einheit in Engagement Range eines Feindes darf ausschließlich Remain Stationary oder Fall Back wählen; Normal Move und Advance sind gesperrt. Die App erzwingt die Sperre über das `in_melee`-Flag; ob die Einheit tatsächlich in Engagement Range (1" horizontal, 5" vertikal) steht, ist Tisch-Anteil.

### R-MOVE-04
- **klasse**: B
- **status**: offen
- **getestet**: nein
- **quelle**: core_rules.txt — "Normal Move: Models move up to M\". Cannot move within Engagement Range of any enemy models."
- **code**: —
- **regel**: Bei einer normalen Bewegung darf jedes Modell bis zu M Zoll zurücklegen und darf nicht innerhalb der Engagement Range eines feindlichen Modells enden. Distanz und Endposition sind nur am Tisch prüfbar.

### R-MOVE-05
- **klasse**: C
- **status**: implementiert
- **getestet**: ja — test_set_movement_status_advanced_sets_turn_flag / test_advanced_cannot_shoot
- **quelle**: core_rules.txt — "Advance: Models move up to M\"+D6\". … Units that Advance cannot shoot or charge this turn."
- **code**: unit_mutations.py:set_movement_status
- **regel**: Bei einem Advance wird ein D6 zum M-Wert addiert (Maximaldistanz M+D6 Zoll, am Tisch gemessen); die App setzt das `advanced`-Flag, das Schießen und Laden in dieser Runde erzwingt-sperrt (App-Anteil).

### R-MOVE-06
- **klasse**: A
- **status**: implementiert
- **getestet**: ja — test_scenario_1_stationary_no_action
- **quelle**: core_rules.txt — "Remain Stationary: Models cannot move this phase. Any units … not selected to move … are assumed to have Remained Stationary"
- **code**: unit_mutations.py:set_movement_status
- **regel**: Eine Einheit, die Remain Stationary wählt, setzt keine Bewegungs-Flags (`advanced`/`retreated` bleiben false) und gilt als unbewegte Einheit dieser Phase; nicht ausgewählte Einheiten gelten ebenfalls als unbewegt.

### R-MOVE-07
- **klasse**: B
- **status**: offen
- **getestet**: nein
- **quelle**: core_rules.txt — "Fall Back: Models move up to M\". … it cannot end its move within Engagement Range of any enemy models – if it cannot do this then it cannot Fall Back."
- **code**: —
- **regel**: Eine zurückweichende Einheit bewegt jedes Modell bis zu M Zoll, darf durch Engagement Ranges hindurchbewegen, muss aber außerhalb aller feindlichen Engagement Ranges enden; ist das unmöglich, kann sie nicht zurückweichen. Distanz und Endposition sind nur am Tisch prüfbar.

### R-MOVE-08
- **klasse**: C
- **status**: implementiert
- **getestet**: ja — test_retreated_cannot_shoot / test_retreated_blocks_cast
- **quelle**: core_rules.txt — "A unit cannot declare a charge in the same turn that it Fell Back. … cannot shoot or attempt to manifest a psychic power … unless it is TITANIC."
- **code**: unit_mutations.py:set_movement_status
- **regel**: Fall Back setzt das `retreated`-Flag, das Schießen, Psykraft-Wirken und Laden in dieser Runde erzwingt-sperrt (App-Anteil). Die TITANIC-Ausnahme (darf trotz Fall Back schießen/Psykräfte wirken) ist noch nicht abgebildet.

### R-MOVE-09
- **klasse**: B
- **status**: offen
- **getestet**: nein
- **quelle**: core_rules.txt — "a unit must finish any type of move in unit coherency"
- **code**: —
- **regel**: Jede Einheit muss nach jeder Bewegung Einheitenkohärenz wahren: alle Modelle innerhalb 2" horizontal und 5" vertikal von mindestens einem anderen Modell; ab 6 Modellen zu mindestens zwei anderen. Ist Kohärenz unmöglich, darf die Bewegung nicht ausgeführt werden. Nur am Tisch prüfbar.

### R-MOVE-10
- **klasse**: C
- **status**: implementiert
- **getestet**: ja — test_scenario_13_deploy_from_reserve_sets_moved
- **quelle**: core_rules.txt — "Reinforcement units cannot make a Normal Move, an Advance, Fall Back or Remain Stationary this turn. Reinforcement units always count as having moved this turn."
- **code**: movementPhase.py:_render_reinforcements_step
- **regel**: Verstärkungseinheiten werden im Reinforcements-Schritt aufgestellt und gelten dabei automatisch als bewegt (`movement_choice = "moved"`, kein Advance-Flag); App-Anteil. Der Mindestabstand ≥9" von Feinden und die Vernichtung nicht eingesetzter Reserven am Spielende sind Tisch-Anteil.

### R-MOVE-11
- **klasse**: B
- **status**: offen
- **getestet**: nein
- **quelle**: core_rules.txt — "A model can be moved over terrain features that are 1\" or less in height as if they were not there … Models cannot finish any kind of move mid-climb"
- **code**: —
- **regel**: Geländemerkmale bis 1" Höhe werden ignoriert; höhere Merkmale werden erklommen (vertikale Distanz zählt zur Bewegung); kein Modell darf eine Bewegung halbfertig auf einem Merkmal beenden. Nur am Tisch prüfbar.

### R-MOVE-12
- **klasse**: B
- **status**: offen
- **getestet**: nein
- **quelle**: core_rules.txt — "FLY … models can be moved across other models … and they can be moved within Engagement Range of enemy models … cannot finish their move … on top of another model … or within Engagement Range"
- **code**: —
- **regel**: Einheiten mit dem FLY-Schlüsselwort dürfen bei Normal Move, Advance und Fall Back über andere Modelle hinweg und durch Engagement Ranges fliegen sowie vertikale Distanzen ignorieren, dürfen aber nicht auf einem Modell oder innerhalb einer Engagement Range enden. Bewegungspfad und Endposition sind nur am Tisch prüfbar.

### R-MOVE-13
- **klasse**: B
- **status**: offen
- **getestet**: nein
- **quelle**: core_rules.txt — "Units can embark in a friendly TRANSPORT if every model ends a Normal Move, an Advance or a Fall Back within 3\" of it. A unit cannot embark within a TRANSPORT that is within Engagement Range of any enemy models."
- **code**: —
- **regel**: Eine Einheit kann nach Normal Move, Advance oder Fall Back in ein befreundetes TRANSPORT-Modell einsteigen, sofern alle Modelle innerhalb 3" davon enden, das Transportmodell nicht in Engagement Range eines Feindes steht und die Einheit nicht in derselben Phase ausgestiegen ist. Abstände sind nur am Tisch prüfbar.

---

## Bereich: Charge Phase

### R-CHARGE-01
- **klasse**: A
- **status**: implementiert
- **getestet**: ja — test_resets_charge_phase_step
- **quelle**: core_rules.txt — "The Charge phase is split into two steps. First you charge with your units. Then your opponent performs Heroic Interventions."
- **code**: chargephase.py:ChargePhaseHandler.render_active
- **regel**: Die Charge Phase besteht aus genau zwei Schritten: (1) Charges der aktiven Seite, (2) Heroic Interventions der inaktiven Seite. Die App führt die Schritte über den Zustand `charge_phase_step` (1→2); beim Phasenwechsel wird er auf 1 zurückgesetzt.

### R-CHARGE-02
- **klasse**: C
- **status**: implementiert
- **getestet**: ja — test_charge_after_advance_requires_core_or_character
- **quelle**: core_rules.txt — "An eligible unit is one that is within 12\" of any enemy units at the start of the Charge phase. Units that have Advanced … Fell Back … or … within Engagement Range … are not eligible units."
- **code**: chargephase.py:_active_charge / ability_engine.py:charge_after_advance_allowed
- **regel**: Charge-Berechtigung: Hybrid — die App erzwingt die Sperren für Advanced (außer faktionsseitige Advance-&-Charge-Ausnahme), Fall Back und bereits in Engagement Range stehende Einheiten (App-Anteil); ob eine Einheit innerhalb 12" eines Feindes steht, ist Tisch-Anteil.

### R-CHARGE-03
- **klasse**: A
- **status**: offen
- **getestet**: nein
- **quelle**: core_rules.txt — "No unit can be selected to charge more than once in each Charge phase."
- **code**: —
- **regel**: Jede Einheit darf pro Charge Phase höchstens einmal zum Laden ausgewählt werden. (App erzwingt keine harte Sperre — die Charge-Buttons bleiben nach erfolgtem Charge klickbar; analog R-MOVE-01.)

### R-CHARGE-04
- **klasse**: B
- **status**: offen
- **getestet**: nein
- **quelle**: core_rules.txt — "you must select one or more enemy units within 12\" of it as the targets of its charge. The target(s) of this charge do not need to be visible to the charging unit."
- **code**: —
- **regel**: Beim Charge-Deklarieren wird mindestens ein feindliches Ziel innerhalb 12" gewählt (mehrere erlaubt); die Ziele müssen nicht sichtbar sein. Die App lässt zwar Ziele auswählen, prüft aber weder die 12"-Reichweite noch die Sichtbarkeitsfreiheit — beides ist nur am Tisch prüfbar.

### R-CHARGE-05
- **klasse**: B
- **status**: offen
- **getestet**: nein
- **quelle**: core_rules.txt — "you then make a charge roll for your unit by rolling 2D6. This is the maximum number of inches each model in the charging unit can now be moved"
- **code**: —
- **regel**: Der Charge Roll besteht aus 2D6; das Ergebnis ist die maximale Bewegungsdistanz jedes Modells. Der Wurf und die Distanzmessung erfolgen am Tisch; die App zeigt nur einen Hinweis und bietet Erfolg/Fehlschlag-Buttons.

### R-CHARGE-06
- **klasse**: C
- **status**: implementiert
- **getestet**: ja — test_set_charged_sets_charged_flag / test_set_charged_enters_melee_for_both_units / test_set_charged_multiple_targets
- **quelle**: core_rules.txt — "the unit's charge roll must be sufficient that it is able to end that move in unit coherency and within Engagement Range of every unit that was a target of its charge … If this is impossible, the charge fails and no models … move this phase."
- **code**: chargephase.py:_active_charge / unit_mutations.py:set_charged
- **regel**: Gültiger Charge: Hybrid — ob der 2D6-Wurf reicht, um in Kohärenz und in Engagement Range jedes Ziels zu enden, ohne nicht-gewählte Feinde zu berühren, ist Tisch-Anteil. Bei bestätigtem Erfolg setzt die App `charged` und registriert die Einheit für alle Ziele im Nahkampf (`set_charged`); bei Fehlschlag bewegt sich nichts (App-Anteil).

### R-CHARGE-07
- **klasse**: A
- **status**: offen
- **getestet**: nein
- **quelle**: core_rules.txt — "each of those units can fire Overwatch before the charge roll is made … an unmodified hit roll of 6 is always required for a successful hit roll, irrespective of … Ballistic Skill or any hit roll modifiers"
- **code**: —
- **regel**: Overwatch wird nach Charge-Deklaration, aber vor dem Charge Roll ausgelöst; Treffer nur auf unmodifizierter 6, unabhängig von BS und Modifikatoren. Die App zeigt bisher nur einen Hinweis, erzwingt nichts. (Siehe auch R-COMBAT-23.)

### R-CHARGE-08
- **klasse**: A
- **status**: offen
- **getestet**: nein
- **quelle**: core_rules.txt — "A unit cannot fire Overwatch if there are any enemy units within Engagement Range of it."
- **code**: —
- **regel**: Eine Einheit in Engagement Range eines Feindes darf keinen Overwatch feuern, auch wenn sie Ziel eines Charges ist. (Bedingung von R-CHARGE-07; Overwatch insgesamt noch nicht implementiert.)

### R-CHARGE-09
- **klasse**: C
- **status**: implementiert
- **getestet**: ja — test_character_not_in_melee_is_eligible / test_non_character_is_ineligible / test_character_in_melee_is_ineligible
- **quelle**: core_rules.txt — "An eligible CHARACTER unit is one that is not within Engagement Range of any enemy units, but is within 3\" horizontally and 5\" vertically of an enemy unit."
- **code**: chargephase.py:hi_eligible_units
- **regel**: Heroic Intervention nur für CHARACTER-Einheiten, die nicht im Nahkampf stehen und in 3" horizontal / 5" vertikal eines Feindes sind. Die App erzwingt die CHARACTER- und Nicht-im-Nahkampf-Bedingung (App-Anteil); die 3"/5"-Distanz ist Tisch-Anteil.

### R-CHARGE-10
- **klasse**: A
- **status**: implementiert
- **getestet**: ja — test_character_already_intervened_is_ineligible / test_returns_true_when_flag_set
- **quelle**: core_rules.txt — "No unit can perform more than one Heroic Intervention in each enemy Charge phase. A unit can never perform a Heroic Intervention in their own Charge phase."
- **code**: chargephase.py:hi_already_performed / hi_eligible_units
- **regel**: Jede CHARACTER-Einheit darf pro gegnerischer Charge Phase höchstens eine Heroic Intervention durchführen; das Flag `heroic_intervened` sperrt eine zweite. Der Heroic-Intervention-Schritt läuft ausschließlich für die inaktive Seite, nie in der eigenen Charge Phase.

### R-CHARGE-11
- **klasse**: B
- **status**: offen
- **getestet**: nein
- **quelle**: core_rules.txt — "you can move each model in that unit up to 3\" … Each model in the unit must finish its Heroic Intervention move closer to the closest enemy model."
- **code**: —
- **regel**: Bei einer Heroic Intervention bewegt sich jedes Modell bis zu 3" und muss näher am nächstgelegenen Feind enden als zuvor. Bewegungsdistanz, Endposition und Kohärenz sind nur am Tisch prüfbar.

### R-CHARGE-12
- **klasse**: B
- **status**: offen
- **getestet**: nein
- **quelle**: core_rules.txt — "Charging Over Terrain … A model can be moved over terrain features that are 1\" or less in height as if they were not there … Models cannot finish a charge move mid-climb"
- **code**: —
- **regel**: Beim Charge Move gelten dieselben Geländeregeln wie bei jeder Bewegung: Merkmale bis 1" Höhe werden ignoriert, höhere erklommen (vertikale Distanz zählt), kein Modell darf mitten auf einem Merkmal enden. Nur am Tisch prüfbar. (Analog R-MOVE-11, auf den Charge Move angewandt.)

### R-CHARGE-13
- **klasse**: B
- **status**: offen
- **getestet**: nein
- **quelle**: core_rules.txt — "Flying When Charging … its models can be moved across other models (and their bases) as if they were not there"
- **code**: —
- **regel**: FLY-Einheiten dürfen beim Charge Move über andere Modelle und Bases hinwegfliegen, müssen aber wie normale Modelle auf freier Fläche und in Kohärenz enden. Bewegungspfad und Endposition sind nur am Tisch prüfbar. (Analog R-MOVE-12, auf den Charge Move angewandt.)

---

## Bereich: Morale Phase

### R-MORALE-01
- **klasse**: A
- **status**: offen
- **getestet**: nein
- **quelle**: core_rules.txt — "The Morale phase is split into two steps. First you take Morale tests for your units. Then you remove any out-of-coherency models."
- **code**: —
- **regel**: Die Morale Phase besteht aus zwei Schritten: (1) Morale Tests, (2) Unit Coherency Checks. Nur Schritt 1 ist in `moralePhase.py` umgesetzt; der Unit-Coherency-Check-Schritt (R-MORALE-12/13) fehlt noch, daher gilt die vollständige Zwei-Schritt-Struktur als offen.

### R-MORALE-02
- **klasse**: C
- **status**: implementiert
- **getestet**: ja — test_unit_with_losses_requires_test / test_single_model_unit_always_skipped / test_destroyed_unit_skipped
- **quelle**: core_rules.txt — "Starting with the player whose turn is taking place, the players must alternate selecting a unit … that has had models destroyed this turn and taking a Morale test for it."
- **code**: moralePhase.py:morale_test_required
- **regel**: Morale-Test-Pflicht: Die App zeigt Tests nur für Einheiten mit Verlusten dieser Runde (`lost_models_this_turn > 0`), überspringt Einzelmodell- und zerstörte Einheiten (App-Anteil). Die abwechselnde Auswahlreihenfolge beider Spieler (beginnend mit dem aktiven) ist Tisch-Anteil.

### R-MORALE-03
- **klasse**: A
- **status**: implementiert
- **getestet**: ja — test_flee_marks_morale_tested
- **quelle**: core_rules.txt — "A unit only needs to take one Morale test in each phase."
- **code**: moralePhase.py:_render_unit_morale / unit_mutations.py:flee_models
- **regel**: Jede Einheit testet pro Morale Phase höchstens einmal; das Flag `morale_tested` (gesetzt bei bestandenem Test bzw. bei Flucht) blockiert einen erneuten Test in derselben Phase.

### R-MORALE-04
- **klasse**: A
- **status**: implementiert
- **getestet**: ja — test_typical_case / test_auto_pass_above_6 / test_always_fails_threshold_1 / test_fails_only_on_6
- **quelle**: core_rules.txt — "roll one D6 and add the number of models from the unit that have been destroyed this turn. If the result is equal to or less than the highest Leadership … the Morale test is passed."
- **code**: moralePhase.py:_fail_threshold
- **regel**: Morale Test = D6 + diese Runde verlorene Modelle gegen den höchsten Ld der Einheit; `_fail_threshold` errechnet den kleinsten fehlschlagenden W6-Wert (Ld − Verluste + 1). Die Sonderregel „unmodifizierte 1 besteht immer" wird am Tisch beurteilt (kein App-Würfel).

### R-MORALE-05
- **klasse**: A
- **status**: implementiert
- **getestet**: ja — test_flee_reduces_models / test_flee_sets_fled_counter
- **quelle**: core_rules.txt — "the Morale test is failed, one model flees that unit … You decide which model … flees – that model is removed from play and counts as having been destroyed."
- **code**: unit_mutations.py:flee_models
- **regel**: Bei fehlgeschlagenem Test flieht mindestens ein Modell nach Wahl des Spielers; `flee_models` entfernt die Modelle, reduziert Wunden/Modelle entsprechend und führt den Flucht-Zähler (`fled_models_this_turn`).

### R-MORALE-06
- **klasse**: A
- **status**: offen
- **getestet**: nein
- **quelle**: core_rules.txt — "Combat Attrition Tests … roll one D6 for each remaining model in that unit … for each result of 1, one model … flees."
- **code**: —
- **regel**: Nach dem ersten fliehenden Modell wird für jedes verbleibende Modell 1 D6 gewürfelt; jede 1 lässt ein weiteres Modell fliehen. Die App rechnet die Attrition-Würfel nicht — sie erfragt nur die Gesamtzahl geflohener Modelle vom Spieler.

### R-MORALE-07
- **klasse**: A
- **status**: offen
- **getestet**: nein
- **quelle**: core_rules.txt — "Subtract 1 from Combat Attrition tests if unit is below Half-strength." / rules_appendix.txt — "below Half-strength … less than half that unit's Starting Strength"
- **code**: —
- **regel**: Eine Einheit ist unter Half-strength, wenn die verbleibenden Modelle weniger als die Hälfte der Starting Strength betragen; dann wird von jedem Combat-Attrition-Würfel 1 abgezogen (Ergebnis 1–2 → flieht). Die App wertet den Half-strength-Status für die Attrition nicht aus.

### R-MORALE-08
- **klasse**: A
- **status**: implementiert
- **getestet**: ja — test_flee_all_models_marks_destroyed
- **quelle**: core_rules.txt — "those models … count as having been destroyed, but they never trigger any rules that are used when a model is destroyed."
- **code**: unit_mutations.py:flee_models
- **regel**: Durch Flucht entfernte Modelle gelten als zerstört (markieren die Einheit als `destroyed`, wenn alle fliehen), lösen aber keine „bei Zerstörung"-Effekte aus — `flee_models` ist ein vom Kampfschaden getrennter Pfad.

### R-MORALE-09
- **klasse**: A
- **status**: offen
- **getestet**: nein
- **quelle**: core_rules.txt — "INSANE BRAVERY … Use this Stratagem before you take a Morale test … That test is automatically passed … once per battle."
- **code**: —
- **regel**: Insane Bravery (Core-Stratagem, 2 CP) lässt einen Morale Test automatisch bestehen (kein Modell flieht); einmal pro Schlacht. In der Morale-Phase-UI noch nicht als Stratagem angebunden.

### R-MORALE-10
- **klasse**: B
- **status**: offen
- **getestet**: nein
- **quelle**: rules_appendix.txt — "those that automatically pass Morale tests or cause no models to flee take precedence."
- **code**: —
- **regel**: Konfliktregel: Bei sich widersprechenden Morale-Regeln haben jene Vorrang, die einen Test automatisch bestehen lassen oder das Fliehen verhindern, vor solchen, die automatisch fehlschlagen lassen. Eine reine Schiedsregel — nur am Tisch anwendbar.

### R-MORALE-11
- **klasse**: A
- **status**: offen
- **getestet**: nein
- **quelle**: rules_appendix.txt — "such models do not count as having been destroyed this turn — exclude them when determining if a unit has to take a Morale test, and when determining what to add to a D6 roll."
- **code**: —
- **regel**: In derselben Runde zerstörte und wieder zurückgebrachte Modelle (z. B. Reanimation) zählen für den Morale Test nicht als zerstört: weder für die Test-Pflicht noch für die zum W6 addierte Verlustzahl. Die App verrechnet zurückgebrachte Modelle bisher nicht gegen `lost_models_this_turn`.

### R-MORALE-12
- **klasse**: B
- **status**: offen
- **getestet**: nein
- **quelle**: core_rules.txt — "Each player must now remove models, one at a time, from any of the units … that are no longer in unit coherency, until only a single group … remains in play and in unit coherency."
- **code**: —
- **regel**: Zweiter Schritt der Morale Phase: Jeder Spieler entfernt nacheinander Modelle aus nicht-kohärenten Einheiten, bis nur eine zusammenhängende, kohärente Gruppe bleibt. Kohärenz (2" horizontal, 5" vertikal) ist nur am Tisch prüfbar; in der App nicht umgesetzt.

### R-MORALE-13
- **klasse**: A
- **status**: offen
- **getestet**: nein
- **quelle**: core_rules.txt — "The models removed count as having been destroyed, but … never trigger any rules … Models removed because of this do not cause their unit to take another Morale test."
- **code**: —
- **regel**: Durch den Unit Coherency Check entfernte Modelle gelten als zerstört, lösen aber keine „bei Zerstörung"-Effekte aus und verursachen keinen weiteren Morale Test für ihre Einheit. Noch nicht umgesetzt (hängt an R-MORALE-12).

---

## Bereich: Psychic Phase

### R-PSYCHIC-01
- **klasse**: A
- **status**: implementiert
- **getestet**: ja — test_has_psyker_true
- **quelle**: core_rules.txt — "Some models have the PSYKER keyword. In the Psychic phase, PSYKERS can attempt to manifest psychic powers"
- **code**: psychicPhase.py:has_psyker
- **regel**: Eine Einheit kann in der Psychic Phase agieren, wenn mindestens ein Modell das Keyword PSYKER trägt.

### R-PSYCHIC-02
- **klasse**: A
- **status**: implementiert
- **getestet**: ja — test_retreated_blocks_cast
- **quelle**: core_rules.txt — "PSYKER units that Fell Back this turn (other than TITANIC units) are not eligible"
- **code**: psychicPhase.py:cast_eligibility
- **regel**: Eine PSYKER-Einheit, die in diesem Zug Fall Back gemacht hat (`retreated`), darf keine psychischen Kräfte manifestieren.

### R-PSYCHIC-03
- **klasse**: B
- **status**: offen
- **getestet**: nein
- **quelle**: core_rules.txt — "(other than TITANIC units) are not eligible"
- **code**: —
- **regel**: TITANIC-Einheiten sind von der Fall-Back-Sperre ausgenommen und dürfen nach einem Rückzug weiterhin manifestieren. `cast_eligibility` blockiert alle Retreated-Einheiten und kennt diese Ausnahme nicht.

### R-PSYCHIC-04
- **klasse**: A
- **status**: implementiert
- **getestet**: ja — test_already_cast_blocks_cast
- **quelle**: core_rules.txt — "No unit can be selected to manifest psychic powers more than once in each Psychic phase."
- **code**: psychicPhase.py:cast_eligibility
- **regel**: Eine PSYKER-Einheit darf pro Psychic Phase höchstens einmal zum Manifestieren ausgewählt werden (`cast`-Flag).

### R-PSYCHIC-05
- **klasse**: A
- **status**: implementiert
- **getestet**: ja — test_advanced_does_not_block
- **quelle**: core_rules.txt — "PSYKER units that Fell Back this turn … are not eligible" (nur Fall Back wird als Ausschluss genannt)
- **code**: psychicPhase.py:cast_eligibility
- **regel**: Eine PSYKER-Einheit, die in diesem Zug Advanced hat, bleibt manifestierberechtigt — Advanced ist kein Ausschlussgrund (`cast_eligibility` prüft nur `retreated`/`cast`).

### R-PSYCHIC-06
- **klasse**: A
- **status**: offen
- **getestet**: nein
- **quelle**: core_rules.txt — "All PSYKERS know the Smite psychic power."
- **code**: —
- **regel**: Jede PSYKER-Einheit kennt automatisch Smite; weitere Kräfte stehen auf dem Datasheet. Die App bietet nur Smite an, ohne die Kräfteliste je Einheit zu verwalten.

### R-PSYCHIC-07
- **klasse**: A
- **status**: offen
- **getestet**: nein
- **quelle**: core_rules.txt — "Each psychic power has a warp charge value – the higher this is, the more difficult it is to manifest the psychic power."
- **code**: —
- **regel**: Jede psychische Kraft hat einen Warp-Charge-Wert, der die Mindestsumme des Psychic Tests bestimmt. Generisch (über Smite hinaus) nicht abgebildet.

### R-PSYCHIC-08
- **klasse**: A
- **status**: offen
- **getestet**: nein
- **quelle**: core_rules.txt — "A PSYKER unit generates their powers before the battle."
- **code**: —
- **regel**: PSYKER-Einheiten bestimmen ihre psychischen Kräfte vor Spielbeginn. Kein Generierungs-Schritt in der App.

### R-PSYCHIC-09
- **klasse**: A
- **status**: offen
- **getestet**: nein
- **quelle**: core_rules.txt — "you cannot attempt to manifest the same psychic power more than once in the same battle round, even with different PSYKER units"
- **code**: —
- **regel**: Dieselbe Kraft (außer Smite) darf pro Schlachtrunde nur einmal manifestiert werden, auch über verschiedene PSYKER hinweg. Mangels Nicht-Smite-Kräften nicht implementiert.

### R-PSYCHIC-10
- **klasse**: A
- **status**: offen
- **getestet**: nein
- **quelle**: core_rules.txt — "The same PSYKER unit cannot attempt to manifest Smite more than once during the same battle round."
- **code**: —
- **regel**: Dieselbe PSYKER-Einheit darf Smite pro Schlachtrunde nur einmal versuchen. Die App sperrt pro Phase über das `cast`-Flag, nicht pro Schlachtrunde.

### R-PSYCHIC-11
- **klasse**: A
- **status**: implementiert
- **getestet**: ja — test_passes_when_equal_to_warp_charge / test_fails_when_below_warp_charge
- **quelle**: core_rules.txt — "you must take a Psychic test for that unit by rolling 2D6. If the total is equal to or greater than that power's warp charge value, the Psychic test is passed."
- **code**: psychicPhase.py:is_manifested
- **regel**: Psychic Test: 2D6 ≥ Warp-Charge-Wert = bestanden, Kraft manifestiert (`is_manifested(roll, wc)`).

### R-PSYCHIC-12
- **klasse**: A
- **status**: implementiert
- **getestet**: ja — test_is_perils_on_2 / test_is_perils_on_12
- **quelle**: core_rules.txt — "If you roll a double 1 or a double 6 when taking a Psychic test, that unit immediately suffers Perils of the Warp."
- **code**: psychicPhase.py:is_perils
- **regel**: Eine Doppel-1 (Summe 2) oder Doppel-6 (Summe 12) beim Psychic Test löst sofort Perils of the Warp aus.

### R-PSYCHIC-13
- **klasse**: B
- **status**: offen
- **getestet**: nein
- **quelle**: core_rules.txt — "select one of their PSYKER units that is within 24" of the PSYKER unit attempting to manifest the power"
- **code**: —
- **regel**: Deny the Witch ist nur möglich, wenn die deny-fähige Gegnereinheit innerhalb 24" der manifestierenden Einheit steht. Abstandsprüfung nur am Tisch.

### R-PSYCHIC-14
- **klasse**: A
- **status**: implementiert
- **getestet**: ja — test_can_deny_via_psyker_keyword / test_can_deny_via_gloom_prism
- **quelle**: core_rules.txt — "The opposing player can then select one of their PSYKER units … and attempt to deny that power"
- **code**: psychicPhase.py:can_deny
- **regel**: Deny the Witch kann von einer feindlichen PSYKER-Einheit oder einer Einheit mit Deny-Wargear (z. B. Gloom Prism) versucht werden.

### R-PSYCHIC-15
- **klasse**: A
- **status**: implementiert
- **getestet**: ja — test_deny_succeeds_greater / test_deny_fails_equal
- **quelle**: core_rules.txt — "If the total is greater than the result of the Psychic test, the Deny the Witch test is passed and the psychic power is denied."
- **code**: psychicPhase.py:deny_succeeds
- **regel**: Deny-the-Witch-Test: 2D6 muss strikt größer als das Psychic-Test-Ergebnis sein (gleich genügt nicht), um die Kraft zu verweigern.

### R-PSYCHIC-16
- **klasse**: A
- **status**: implementiert
- **getestet**: ja — test_possible_while_manifested_power_unresolved / test_blocked_after_deny_already_resolved
- **quelle**: core_rules.txt — "Only one attempt can be made to deny a psychic power."
- **code**: psychicPhase.py:can_attempt_deny
- **regel**: Pro psychischer Kraft ist nur ein Deny-Versuch erlaubt. Die App erzwingt das über den `denied`-Zustand (None→bool) und zusätzlich ein Deny pro Fraktion/Phase (`can_attempt_deny` / `faction_deny_used`).

### R-PSYCHIC-17
- **klasse**: A
- **status**: implementiert
- **getestet**: ja — test_base_warp_charge_is_5
- **quelle**: core_rules.txt — "Smite has a warp charge value of 5."
- **code**: psychicPhase.py:smite_warp_charge
- **regel**: Smite hat Warp Charge 5 — Basiswert der Manifestationsschwelle (`SMITE_BASE_WARP_CHARGE`).

### R-PSYCHIC-18
- **klasse**: A
- **status**: implementiert
- **getestet**: ja — test_rises_by_one_per_prior_attempt
- **quelle**: core_rules.txt — "Add 1 to the warp charge value of this psychic power for each other attempt that has been made to manifest this power by a unit from your army in this phase"
- **code**: psychicPhase.py:smite_warp_charge
- **regel**: Smites Warp Charge steigt je vorherigem Smite-Versuch der eigenen Armee in dieser Phase um 1 (`smite_warp_charge(psi_attempts_this_phase)`).

### R-PSYCHIC-19
- **klasse**: B
- **status**: offen
- **getestet**: nein
- **quelle**: core_rules.txt — "the closest enemy unit within 18" of and visible to the psyker suffers D3 mortal wounds"
- **code**: —
- **regel**: Smite trifft die nächste sichtbare Gegnereinheit innerhalb 18". Abstand und Sichtlinie sind nur am Tisch prüfbar; die App lässt das Ziel manuell wählen.

### R-PSYCHIC-20
- **klasse**: A
- **status**: implementiert
- **getestet**: ja — test_w3_on_5 / test_w3_on_10
- **quelle**: core_rules.txt — "the closest enemy unit within 18" … suffers D3 mortal wounds"
- **code**: psychicPhase.py:smite_damage_die
- **regel**: Bei erfolgreichem Smite mit Psychic-Test-Ergebnis ≤ 10 erleidet das Ziel D3 Mortal Wounds.

### R-PSYCHIC-21
- **klasse**: A
- **status**: implementiert
- **getestet**: ja — test_w6_on_11 / test_w6_on_12
- **quelle**: core_rules.txt — "If the result of the Psychic test was 11 or more, that unit suffers D6 mortal wounds instead."
- **code**: psychicPhase.py:smite_damage_die
- **regel**: Bei Smite mit Psychic-Test-Ergebnis ≥ 11 erleidet das Ziel stattdessen D6 Mortal Wounds.

### R-PSYCHIC-22
- **klasse**: A
- **status**: implementiert
- **getestet**: ja — test_pending_when_perils_and_not_applied / test_not_pending_once_applied
- **quelle**: core_rules.txt — "When a PSYKER unit suffers Perils of the Warp, it suffers D3 mortal wounds."
- **code**: psychicPhase.py:perils_pending
- **regel**: Bei Perils of the Warp erleidet die PSYKER-Einheit D3 Mortal Wounds (per `apply_damage`, mortal); das Perils-Gate (`perils_pending`) erzwingt die Auflösung vor allem anderen.

### R-PSYCHIC-23
- **klasse**: A
- **status**: offen
- **getestet**: nein
- **quelle**: core_rules.txt — "If a PSYKER unit is destroyed by Perils of the Warp while attempting to manifest a psychic power, that power automatically fails to manifest."
- **code**: —
- **regel**: Wird die PSYKER-Einheit durch Perils zerstört, schlägt die Kraft automatisch fehl. Die App revidiert `manifested` nach dem Perils-Schaden nicht — Mechanik fehlt.

### R-PSYCHIC-24
- **klasse**: C
- **status**: offen
- **getestet**: nein
- **quelle**: core_rules.txt — "every unit within 6" of it immediately suffers D3 mortal wounds"
- **code**: —
- **regel**: Wird ein PSYKER durch Perils zerstört, erleiden alle Einheiten in 6" je D3 Mortal Wounds (App-Anteil: Schaden anwenden; Tisch-Anteil: 6"-Reichweite). Splash-Schaden nicht implementiert.

---

## Bereich: Battle-Round-Struktur

### R-ROUND-01
- **klasse**: A
- **status**: implementiert
- **getestet**: ja — test_next_phase_setup_goes_to_command
- **quelle**: core_rules.txt — "Warhammer 40,000 is played in a series of battle rounds. In each battle round, both players have a turn."
- **code**: game_state.py:next_phase
- **regel**: Das Spiel besteht aus einer Folge von Battle Rounds. In jeder Battle Round hat jeder Spieler genau einen Turn.

### R-ROUND-02
- **klasse**: A
- **status**: implementiert
- **getestet**: ja — test_next_phase_switches_active_player_after_necrons_morale
- **quelle**: core_rules.txt — "The same player always takes the first turn in each battle round – the mission you are playing will tell you which player this is."
- **code**: game_state.py:init_state
- **regel**: Immer derselbe Spieler hat den ersten Turn jeder Battle Round. `first_player` wird bei Spielstart gesetzt und bleibt unveränderlich (Layout-Seitenleiste ist ebenfalls fest gebunden).

### R-ROUND-03
- **klasse**: A
- **status**: implementiert
- **getestet**: ja — test_next_phase_advances_index_within_turn
- **quelle**: core_rules.txt — "Each turn consists of a series of phases, which must be resolved in the following order: 1. COMMAND PHASE … 7. MORALE PHASE"
- **code**: game_state.py:next_phase
- **regel**: Innerhalb eines Turns sind die Phasen fix geordnet: Command → Movement → Psychic → Shooting → Charge → Fight → Morale. Die App erzwingt diese Reihenfolge über `phase_idx` (nur Vorwärts-Schritt). Für Command als ersten Schritt siehe auch R-CMD-01.

### R-ROUND-04
- **klasse**: A
- **status**: implementiert
- **getestet**: ja — test_next_phase_switches_active_player_after_necrons_morale
- **quelle**: core_rules.txt — "Once a player's turn has ended, their opponent then starts their turn."
- **code**: game_state.py:next_phase
- **regel**: Nach Abschluss der Morale Phase wechselt `active` zum anderen Spieler; dessen Turn beginnt (phase_idx zurück auf 1 = Command Phase).

### R-ROUND-05
- **klasse**: A
- **status**: implementiert
- **getestet**: ja — test_next_phase_increments_round_after_orks_morale
- **quelle**: core_rules.txt — "Once both players have completed a turn, the battle round has been completed and the next one begins"
- **code**: game_state.py:next_phase
- **regel**: Nachdem der zweite Spieler seine Morale Phase abgeschlossen hat, ist die Battle Round vollständig; `round` wird um 1 erhöht und der erste Spieler beginnt seinen Turn der neuen Runde.

### R-ROUND-06
- **klasse**: A
- **status**: implementiert
- **getestet**: ja — test_init_state_sets_round_to_one
- **quelle**: core_rules.txt — "The first battle round begins."
- **code**: game_state.py:init_state
- **regel**: Bei Spielstart wird der Rundenzähler auf 1 gesetzt (`st.session_state.round = 1`). Der erste Turn gehört dem `first_player`.

### R-ROUND-07
- **klasse**: A
- **status**: offen
- **getestet**: nein
- **quelle**: core_rules.txt — "The battle ends when all of the models in one player's army have been destroyed, or once the fifth battle round has ended (whichever comes first)."
- **code**: —
- **regel**: Das Spiel endet nach 5 Battle Rounds oder wenn alle Modelle einer Armee vernichtet sind. Die App zeigt keine automatische Spielende-Erkennung und keinen „Spiel beendet"-Zustand.

### R-ROUND-08
- **klasse**: B
- **status**: offen
- **getestet**: nein
- **quelle**: core_rules.txt — "Each mission will tell you when the battle ends. This will typically be after a set number of battle rounds have been completed, or when one player has achieved a certain victory condition."
- **code**: —
- **regel**: Missionsspezifische Siegbedingungen (z. B. Missionsziele, VP-Zählung) legen das Spielende fest. Die App zeigt keinen VP-Vergleich oder Siegbedingungscheck — nur am Tisch prüfbar.

### R-ROUND-09
- **klasse**: A
- **status**: offen
- **getestet**: nein
- **quelle**: core_rules.txt — "If these things occur before or after the battle, or at the start or end of a battle round, the players roll off and the winner decides in what order the rules are resolved."
- **code**: —
- **regel**: Gleichzeitige Regeln „am Start/Ende der Battle Round" werden per Roll-off entschieden (nicht per aktivem Spieler). Während des Turns entscheidet der aktive Spieler. Die App erzwingt diese Unterscheidung nicht.

### R-ROUND-10
- **klasse**: A
- **status**: offen
- **getestet**: nein
- **quelle**: core_rules.txt — "When this happens during the battle, the player whose turn it is chooses the order."
- **code**: —
- **regel**: Gleichzeitige Regeln *während* des Turns (nicht Battle-Round-Start/-Ende) werden vom Spieler aufgelöst, der am Zug ist. Die App unterstützt keine explizite Reihenfolge-Auswahl bei simultanen Effekten.

## Bereich: Deployment / Aufstellung

### R-DEPLOY-01
- **klasse**: B
- **status**: offen
- **getestet**: nein
- **quelle**: core_rules.txt — "The players then alternate deploying their units, one at a time, starting with the player who did not pick their deployment zone."
- **code**: —
- **regel**: Aufstellungsreihenfolge: Spieler stellen abwechselnd je eine Einheit auf; es beginnt der Spieler, der seine Aufstellungszone nicht gewählt hat. Jedes Modell muss vollständig in der eigenen Zone enden. Nur am Tisch prüfbar; die App kennt keine geometrische Aufstellungszone.

### R-DEPLOY-02
- **klasse**: C
- **status**: implementiert
- **getestet**: ja — test_in_reserve_cannot_shoot / test_in_reserve_cannot_fight / test_in_reserve_takes_priority
- **quelle**: core_rules.txt — "abilities that allow [a unit] to be set up in a location other than the battlefield"; "Reinforcement units … always count as having moved this turn."
- **code**: unit_mutations.py:set_deployment
- **regel**: Einheiten können als Reserve aufgestellt werden (`deployment = "reserve"`, `in_reserve = True`); die App sperrt dann Schießen, Kämpfen und Angreifen (App-Anteil). Mindestabstand 9", Aufstellungszone und früheste Runde sind Tisch-Anteil.

### R-DEPLOY-03
- **klasse**: B
- **status**: offen
- **getestet**: nein
- **quelle**: core_rules.txt — "the players must roll off after all other units have been set up and alternate setting up these units, starting with the winner."
- **code**: —
- **regel**: Post-Deployment-Aufstellung: Einheiten, die nach der normalen Aufstellung gesetzt werden, werden nach einem Roll-off abwechselnd platziert. Abfolge und Roll-off sind nur am Tisch prüfbar.

### R-DEPLOY-04
- **klasse**: B
- **status**: offen
- **getestet**: nein
- **quelle**: core_rules.txt — "such models can overhang a deployment zone if it is not possible to set them up otherwise … their base must still be wholly within their deployment zone."
- **code**: —
- **regel**: Große Modelle (typisch AIRCRAFT) dürfen die Aufstellungszone überhängen, wenn kein vollständiges Aufstellen möglich ist; die Base muss vollständig in der Zone liegen. Nur am Tisch prüfbar.

### R-DEPLOY-05
- **klasse**: B
- **status**: offen
- **getestet**: nein
- **quelle**: core_rules.txt — "that unit cannot be set up in any location other than on the battlefield unless specified in the redeployment ability itself."
- **code**: —
- **regel**: Wird eine eigentlich außerhalb des Schlachtfelds aufzustellende Einheit für eine Redeployment-Fähigkeit gewählt, darf sie nur noch auf dem Schlachtfeld aufgestellt werden (außer die Fähigkeit erlaubt anderes). Nur am Tisch prüfbar.

### R-DEPLOY-06
- **klasse**: A
- **status**: offen
- **getestet**: nein
- **quelle**: core_rules.txt — "Only Battle-forged armies can use Strategic Reserves … Must pay CPs to place units into Strategic Reserves."
- **code**: —
- **regel**: Strategic Reserves: Nur Battle-forged Armeen dürfen Einheiten in die Strategischen Reserven legen; vor der Schlacht werden CPs nach Power Rating bezahlt. Die App implementiert keinen Strategic-Reserve-Mechanismus.

### R-DEPLOY-07
- **klasse**: B
- **status**: offen
- **getestet**: nein
- **quelle**: core_rules.txt — "Strategic Reserve units cannot arrive in the first battle round … Cannot be set up within 9\" of enemy models."
- **code**: —
- **regel**: Einheiten aus Strategischen Reserven rücken frühestens in Runde 2 ein, ab Runde 2 nur innerhalb 6" eigener/neutraler Kanten, ab Runde 3 aller Kanten außer der feindlichen Grundkante; mindestens 9" Abstand zu Feinden. Nur am Tisch prüfbar.

### R-DEPLOY-08
- **klasse**: B
- **status**: offen
- **getestet**: nein
- **quelle**: core_rules.txt — "AIRCRAFT … can be set up anywhere on the battlefield that is more than 9\" from any enemy models … can move off the edge of the battlefield … placed into Strategic Reserves."
- **code**: —
- **regel**: AIRCRAFT dürfen beim Einrücken aus Strategischen Reserven überall (>9" von Feinden) statt nur an einer Kante aufgestellt werden und dürfen die Spielfeldkante freiwillig verlassen (zurück in die Reserven). Nur am Tisch prüfbar.

### R-DEPLOY-09
- **klasse**: B
- **status**: offen
- **getestet**: nein
- **quelle**: core_rules.txt — "Fortifications cannot be setup within 3\" of other terrain features (except hills). Fortifications cannot be placed into Strategic Reserves."
- **code**: —
- **regel**: Fortifikationen müssen mindestens 3" von anderem Gelände (außer Hügeln) aufgestellt werden und können nicht in Strategische Reserven gelegt werden. Nur am Tisch prüfbar.

## Bereich: Mission-Scoring / Victory Points

### R-SCORE-01
- **klasse**: A
- **status**: implementiert
- **getestet**: ja — test_adjust_vp_adds_delta_to_faction_score / test_adjust_vp_floors_at_zero
- **quelle**: core_rules.txt — "the player with the most victory points is the victor (in the case of a tie, the battle is a draw)."
- **code**: unit_mutations.py:adjust_vp
- **regel**: Siegpunkte werden je Fraktion verfolgt (`st.session_state.vp`); `adjust_vp` erhöht/senkt den Stand und kappt bei 0. Den automatischen Sieger-Check (meiste VP, Gleichstand = Unentschieden) macht die App nicht.

### R-SCORE-02
- **klasse**: B
- **status**: offen
- **getestet**: nein
- **quelle**: core_rules.txt — "Slay the Warlord: A player scores 1 victory point if the enemy Warlord is destroyed at the end of the battle."
- **code**: —
- **regel**: Slay the Warlord: 1 VP, wenn der gegnerische Warlord am Spielende zerstört ist. Die App kennt kein Warlord-Flag; der VP wird manuell eingetragen.

### R-SCORE-03
- **klasse**: B
- **status**: offen
- **getestet**: nein
- **quelle**: core_rules.txt — "At the end of each player's Command phase, the player whose turn it is scores 1 victory point for each objective marker they currently control."
- **code**: —
- **regel**: Capture and Control (primär): Am Ende der eigenen Command Phase 1 VP je kontrolliertem Missionsziel. Die App bietet keine Missionsziel-Kontrolle; VP werden manuell eingetragen.

### R-SCORE-04
- **klasse**: B
- **status**: offen
- **getestet**: nein
- **quelle**: core_rules.txt — "if one player controls more objective markers than their opponent does at the end of the battle, they score 1 bonus victory point."
- **code**: —
- **regel**: Capture and Control (Bonus): Am Spielende 1 Bonus-VP für den Spieler mit mehr kontrollierten Missionszielen. Nur am Tisch prüfbar.

### R-SCORE-05
- **klasse**: B
- **status**: offen
- **getestet**: nein
- **quelle**: core_rules.txt — "A model is in range of an objective marker if it is within 3\" horizontally and 5\" vertically of that objective marker."
- **code**: —
- **regel**: Reichweite zu einem Missionsziel: Modell ≤3" horizontal und ≤5" vertikal vom Marker. Distanz nur am Tisch messbar.

### R-SCORE-06
- **klasse**: B
- **status**: offen
- **getestet**: nein
- **quelle**: core_rules.txt — "a player controls an objective marker while they have more models within range of it than their opponent does. A model can only be counted towards controlling one objective marker per turn."
- **code**: —
- **regel**: Kontrollprinzip: Ein Missionsziel kontrolliert, wer mehr Modelle in Reichweite hat; ein Modell zählt pro Zug nur für ein Missionsziel. Nur am Tisch prüfbar.

### R-SCORE-07
- **klasse**: B
- **status**: offen
- **getestet**: nein
- **quelle**: core_rules.txt — "AIRCRAFT units and units with the Fortifications Battlefield Role can never control objective markers."
- **code**: —
- **regel**: AIRCRAFT und Fortifikationen können Missionsziele nie kontrollieren, auch bei Modellen in Reichweite. Nur am Tisch prüfbar.

### R-SCORE-08
- **klasse**: B
- **status**: offen
- **getestet**: nein
- **quelle**: core_rules.txt — "Objective Secured: A player controls an objective marker if they have any models with this ability within range … even if there are more enemy models within range."
- **code**: —
- **regel**: Objective Secured: Einheiten mit dieser Fähigkeit kontrollieren ein Missionsziel auch bei feindlicher Übermacht (bei beidseitigem OS gilt Mehrheit). Die App erfasst das Keyword in YAML, wertet es für Missionsziel-Kontrolle aber nicht aus.

### R-SCORE-09
- **klasse**: C
- **status**: implementiert
- **getestet**: ja — test_adjust_secondary_vp_adds_within_slot / test_adjust_secondary_vp_caps_at_fifteen / test_adjust_secondary_vp_floors_at_zero
- **quelle**: core_rules.txt — Matched-Play secondary objectives (manueller VP-Tracker)
- **code**: unit_mutations.py:adjust_secondary_vp
- **regel**: Sekundärziele: Die App führt bis zu 3 benannte Sekundärziel-Slots je Spieler mit manuellem VP-Tracker; `adjust_secondary_vp` kappt jeden Slot auf [0, 15] (App-Anteil). Die tatsächliche Erfüllung ist Tisch-Anteil.

### R-SCORE-10
- **klasse**: C
- **status**: implementiert
- **getestet**: ja — test_adjust_vp_adds_delta_to_faction_score
- **quelle**: core_rules.txt — "the player with the most victory points is the victor"; App-Konfiguration vp_phase / vp_from_round
- **code**: unit_mutations.py:adjust_vp
- **regel**: Primär-VP werden über +5/+1/-1/-5-Schaltflächen manuell angepasst (Kernlogik `adjust_vp`, getestet); die VP-Anzeige ist auf eine Phase (`vp_phase`) und früheste Runde (`vp_from_round`) konfigurierbar — das Gating liegt im Render-Code (manuell verifiziert, Coverage-ausgeschlossen).

### R-SCORE-11
- **klasse**: B
- **status**: offen
- **getestet**: nein
- **quelle**: core_rules.txt — "If neither player manages to achieve a victory then the game is considered to be a draw."
- **code**: —
- **regel**: Unentschieden bei gleicher VP-Zahl. Die App zeigt keinen automatischen Spielende-/Sieger-Status.

### R-SCORE-12
- **klasse**: B
- **status**: offen
- **getestet**: nein
- **quelle**: core_rules.txt — "If, at the end of the battle, one army has been destroyed, the player commanding the opposing army is the victor."
- **code**: —
- **regel**: Sieg durch vollständige Vernichtung der gegnerischen Armee, unabhängig vom VP-Stand. Die App verfolgt zerstörte Einheiten, prüft aber nicht, ob eine ganze Armee vernichtet ist.

### R-SCORE-13
- **klasse**: B
- **status**: offen
- **getestet**: nein
- **quelle**: core_rules.txt — "you can nominate one model … to be your Warlord. That model gains the WARLORD keyword."
- **code**: —
- **regel**: Warlord-Nominierung vor dem Spiel: genau ein Modell (kein FORTIFICATION) wird Warlord und erhält das WARLORD-Keyword; ein CHARACTER kann zusätzlich einen Warlord Trait erhalten. Die App kennt keinen Nominierungs-Schritt.

---

## Bereich: Fraktionsfähigkeiten — Necron Command Protocols

### R-PROTO-01
- **klasse**: A
- **status**: implementiert
- **getestet**: ja — test_eternal_guardian_d1_light_cover_true_when_stationary / test_eternal_guardian_d1_light_cover_false_when_moved / test_protocol_modifier_eternal_guardian_primary_no_generic_save_key / test_light_cover_if_stationary_eternal_guardian_primary_when_stationary / test_light_cover_if_stationary_eternal_guardian_primary_when_moved / test_light_cover_if_stationary_false_when_directive_inactive
- **quelle**: wahapedia_necrons/faction_overview.txt Z. 585–599 — "Directive 1: Each time an attack is made against this unit, if it did not make a Normal Move, Advance or Fall Back this battle round, this unit receives the benefit of Light Cover."
- **code**: ability_engine.py:get_active_round_choice_light_cover_if_stationary
- **regel**: Eternal Guardian Direktive 1 (Klasse A): App gewährt Light Cover automatisch, wenn das Protocol aktiv ist UND die Verteidiger-Einheit sich in dieser Runde nicht bewegt hat (`movement_choice == "stationary"`). Variante C: bestehende Light-Cover-Checkbox wird programmatisch vorgehakt und gesperrt; der +1-Save-Modifier fließt einmalig über die Checkbox-Mechanik — kein zweiter Collector-Eintrag. Gilt in jeder Phase (any); UI-Anzeige aktuell nur im Shooting-SAVE-Block (A1-Entscheidung Step 4).

### R-PROTO-02
- **klasse**: B
- **status**: implementiert
- **getestet**: ja — test_build_aura_range_hint_text_primary_contains_value_max_names_and_table_note / test_build_aura_range_hint_text_secondary_returns_none / test_build_aura_range_hint_text_other_protocol_without_effect_returns_none
- **quelle**: wahapedia_necrons/faction_overview.txt Z. 700–711 — "Directive 1: Add 3\" to the range of this unit's aura abilities (to a maximum of 12\") and increase the range of the following abilities this unit has by 3\" (to a maximum of 12\"): Lord's Will; My Will Be Done; Rites of Reanimation."
- **code**: ability_engine.py:build_aura_range_hint_text / uiLayout/armyCard.py:_render_aura_range_hint (Anzeige an drei Round-Choice-Stellen); faction_abilities.yaml:protocol_conquering_tyrant.directives.primary (enforcement: table, affects-Liste)
- **regel**: Conquering Tyrant Direktive 1 (Klasse B): +3" Aura-Reichweite (max 12"). Kein App-Effekt (keine Distanzmessung implementiert). App zeigt Tisch-Hinweis (`st.info`, design_system.md §3), sichtbar nur bei aktiver `aura_range_bonus`-Direktive. Text datengetrieben aus `value`/`max` + `affects`-Liste im YAML (keine Fraktions-/Namens-Literale in `src/`). YAML: `type: aura_range_bonus, enforcement: table`.

### R-PROTO-03
- **klasse**: A
- **status**: implementiert
- **getestet**: ja — test_conquering_tyrant_secondary_shoot_after_fall_back_returns_minus_one_when_fell_back / test_conquering_tyrant_secondary_shoot_after_fall_back_zero_when_not_fell_back / test_conquering_tyrant_secondary_shoot_after_fall_back_zero_when_inactive / test_conquering_tyrant_secondary_not_a_generic_numeric_modifier
- **quelle**: wahapedia_necrons/faction_overview.txt Z. 712–721 — "Directive 2: This unit is eligible to shoot in a turn in which it Fell Back, but if it does, then until the end of the turn, each time a model in this unit makes a ranged attack, subtract 1 from that attack's hit roll."
- **code**: ability_engine.py:get_active_round_choice_shoot_after_fall_back / uiLayout/_common.py:_render_resolution_tab
- **regel**: Conquering Tyrant Direktive 2 (Klasse A): Einheit darf nach Fall Back schießen; wenn sie es tut, −1 auf alle Treffer-Würfe (Fernkampf). Engine liest `movement_choice == "fall_back"` der angreifenden Einheit; Modifier wird als Eintrag in `final_atk_mods` (HIT, roll_type="hit", value=-1) in `_render_resolution_tab` injiziert. Nur in der Shooting-Phase aktiv.
