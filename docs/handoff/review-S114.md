DONE

# DoD-Review S114 — Reviewer-Subagent (Opus)

Scope: Session-Diff S114 — `src/gameMechanic/commandPhase.py` (armee-weiter Befehlsphase-Hinweis)
+ vier Testdateien (1× erweitert, 3× neu P1/P2/P4).

## DoD-Punkte

1. ✅ **Regelkonform** — Tests treffen echtes Produktivverhalten, nicht Mocks. Verifiziert:
   `heal_unit` (unit_mutations.py:259) cappt auf `models_max` und reduziert `lost_models_this_turn`
   (RP-Tests P2 decken die reale Funktion); `apply_damage_attacks` (combat.py:264) = `models_lost ×
   wounds + front + mortal` (P2 deckt Formel exakt); `resolve_attack_modifiers` (combat.py) liefert
   Heavy-Malus nur bei `use_melee=False`, Cap ±1, Min 2+ (P1 echt); `get_active_rp_modifiers`
   (ability_engine.py:324) gibt `{rp_reroll: True}` nur bei aktivem Effekt. Overwatch-als-Shooting
   gegen core_rules.txt belegt.
2. ✅ **Generisch** — Eigener grep über `commandPhase.py`: KEINE Fraktions-Strings/-Checks
   (necron/ork/custodes/… = 0 Treffer). `unit_has_command_ability` entscheidet rein datengetrieben
   über drei Quellen (unit_abilities `phase==command`, `activated_wargear_ids`, triggered
   `gain_cp_roll`). Sauber.
3. ⚠️ **BEFUND** — Tests laufen grün (76/76 in den vier Dateien), aber einige im P2-File sind
   inhaltlich schwach (Tautologien, s. u.). Mehrheit ist aussagekräftig (negative Fälle vorhanden:
   `test_warriors_have_no_command_ability`, `test_unit_without_activated_wargear...`,
   `test_rp_zero_models_back_leaves_state_unchanged`).
4. ✅ **Architektur-Gate** — grün. Neuer Helper bricht keine Invariante: `unit_has_command_ability`
   / `units_with_command_abilities` sind render-frei (kein `st.`-Zugriff), nur `_render_command_ability_hint`
   nutzt `st.caption`. Layer-Richtung (commandPhase → loader/game_state) unverändert.
5. ✅ **Clean Code** — sprechende Namen, Early Returns in `unit_has_command_ability`, Type Hints
   vollständig, keine Magic Strings (Phasen-/Effektnamen aus Daten bzw. dokumentierten Literalen).
6. ✅ **UI manuell** — `_render_command_ability_hint` vom Stakeholder bestätigt (Caption erscheint,
   Early Return bei leerem/abilityslosem Roster). Erledigt.
7. ✅ **Doku-Drift** — kein Widerspruch zu einer Spec aufgefallen. Ledger zeigt unverändert
   2 offene impl-ohne-Test (R-COMBAT-17, R-PROTO-02) — vom S114-Scope nicht berührt.

## Befunde

- **Nicht-blockierend** — `test_damage_block_reanimation.py:394-401`
  (`test_rp_dice_count_equals_models_lost_times_wounds`): Tautologie — rechnet `4*2==8` in der
  Testfunktion selbst nach, ruft KEINEN Produktivcode. Beweist nichts über `_render_rp_block`.
- **Nicht-blockierend** — `test_damage_block_reanimation.py:403-417`
  (`test_rp_not_triggered_for_unit_without_reanimation_protocols`,
  `test_warriors_have_reanimation_protocols_rule`): prüfen nur das Test-Fixture (`overlord.rules` /
  `warriors.rules`), nicht das RP-Gate in `_render_rp_block`. Schwacher Informationsgewinn — die
  eigentliche Gate-Bedingung `"reanimationProtocols" not in unit.rules` bleibt ungetestet (Render-Code,
  bewusst ausgeschlossen — daher nur Nice-to-have, kein Loch).
- **Nice-to-have** — `test_command_phase.py:160-168`
  (`test_two_bearers_target_state_no_conflict`): testet reine dict-pop-Semantik auf lokalen Variablen,
  kein Produktivcode. Der eigentliche Regressionswert steckt im daneben liegenden
  `test_two_orb_bearers_render_distinct_button_keys` (das ruft echten Renderer) — dieser ist gut.
- **Nice-to-have** — `test_phase_stage_values.py:52` führt `"setup"` in `VALID_PHASES`, obwohl der
  Datei-Docstring (Z.8-11) `setup` nicht als erlaubten phase-Wert listet. Konsistenz-Drift im Test
  selbst, keine Produktivauswirkung.

Keine blockierenden Befunde. Verdikt: grün mit vier nicht-blockierenden/Nice-to-have-Hinweisen zur
Testqualität (P2-Tautologien). Empfehlung: die drei genannten Tautologie-Tests bei Gelegenheit
durch echte Produktivaufrufe ersetzen oder entfernen — nicht aufschieben als stille Schuld.
