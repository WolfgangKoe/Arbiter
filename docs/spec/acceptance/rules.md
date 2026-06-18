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
(diese Datei: Attackenabfolge/Combat (Schießen + Nahkampf), Command Phase).

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
- **getestet**: nein
- **quelle**: core_rules.txt — "Invulnerable Saves" — "If a model has more than one invulnerable save, it can only use one of them"
- **code**: combat.py:resolve_save
- **regel**: Hat ein Modell mehrere Invulnerable Saves, wird nur der beste verwendet (kleinster Zahlenwert). (Schuld: bisher nur implizit über R-08 abgedeckt.)

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
- **klasse**: A
- **status**: implementiert
- **getestet**: nein
- **quelle**: core_rules.txt — "RAPID FIRE … double the number of attacks … if its target is within half the weapon's range"
- **code**: attack_math.py:_compute_attacks / attack_math.py:_total_attacks_int
- **regel**: Rapid-Fire-Waffe: Angriffszahl wird verdoppelt, wenn das Ziel innerhalb der halben Reichweite ist. (Schuld: bisher nur Integrations-Smoke in test_shooting.py, kein Unit-Test der Berechnung.)

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
- **status**: offen
- **getestet**: nein
- **quelle**: core_rules.txt — "Charging Units Fight First" (Fight Phase)
- **code**: —
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
- **getestet**: nein
- **quelle**: core_rules.txt — "If your army is Battle-forged, then at the start of your Command phase … you gain 1 Command point"
- **code**: commandPhase.py:_render_faction_actions
- **regel**: Der CP-Gewinn pro Command Phase ist regelseitig an den Battle-forged-Status gebunden. (Schuld + Befund: Der Grant-Button wird unabhängig von `game_mode`/Battle-forged angezeigt — eine Unbound-Armee könnte den Bonus ebenfalls erhalten; kein Test prüft das Gating.)

### R-CMD-04
- **klasse**: A
- **status**: implementiert
- **getestet**: nein
- **quelle**: core_rules.txt — Battle-forged CP-Bonus / Spielgröße: Combat Patrol 3 · Incursion 6 · Strike Force 12 · Onslaught 18
- **code**: game_state.py:init_game_state
- **regel**: Der CP-Startvorrat richtet sich nach der Spielgröße (`CP_BY_GAME_SIZE`: 3/6/12/18). (Schuld: kein Test prüft die vier Stufen.)

### R-CMD-05
- **klasse**: A
- **status**: implementiert
- **getestet**: ja — test_clickable_when_all_conditions_met / test_greyed_when_insufficient_cp / test_greyed_when_already_used_this_phase
- **quelle**: core_rules.txt — "CPs … can be spent to utilise Stratagems"
- **code**: stratagem.py:stratagem_visibility
- **regel**: Stratagems kosten CP; `stratagem_visibility()` schaltet einen Button auf `clickable` (CP ausreichend, nicht verwendet), `greyed` (CP fehlen oder bereits genutzt) oder `hidden` (Bedingungen/Phase nicht erfüllt).

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
- **getestet**: nein
- **quelle**: core_rules.txt — "Some abilities found on datasheets … are used in your Command phase"
- **code**: commandPhase.py:_render_buff_roll_ability
- **regel**: Aktivierte Command-Phase-Fähigkeiten vom Typ `buff_roll`/`reroll_hit_1` werden pro ausgewählter Einheit gerendert und ihr Effekt als `active_buffs` im Einheitenzustand eingetragen. (Schuld: kein Test prüft das Eintragen des Buffs.)

### R-CMD-11
- **klasse**: A
- **status**: implementiert
- **getestet**: nein
- **quelle**: core_rules.txt — "Some abilities found on datasheets … are used in your Command phase"
- **code**: commandPhase.py:_render_gain_cp_roll
- **regel**: Fähigkeiten mit `gain_cp_roll`-Effekt (Würfelwurf am Phase-Start; bei Schwellenwert+ erhält die aktive Seite CP) sind einmal pro Command Phase auflösbar und danach gesperrt. (Schuld: kein Test prüft den CP-Gewinn.)

### R-CMD-12
- **klasse**: A
- **status**: implementiert
- **getestet**: nein
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
