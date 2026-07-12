# Regelerkenntnisse — nicht-offensichtliche Implementierungs-Hinweise

Destillierte 9E-Regel-Gotchas, die beim Implementieren leicht falsch gemacht werden.
Dies ist **kein** Akzeptanz-Katalog (das ist `acceptance/rules.md`, parser-geprüfter
Nenner) und **keine** Rohquelle (das sind `docs/work/wahapedia_*/`), sondern die kurze
Merkliste der Fallen. Quelle bei Zweifel immer `docs/work/wahapedia_*/` — nie Gedächtnis.

- **Necron Command Protocols — Direktiv-Wahl ist runden-scoped:** Haupt- wie Extra-Direktive
  werden **jede Runde** neu gewählt (`faction_overview.txt` Z. 568/579: „at the start of each
  battle round"). Sie bleiben NICHT einmal fix. App-Implementierung: `gameState.py`
  `_reset_round_choice_state()` (~Z. 583) öffnet das Fenster pro Runde. Einzige Ausnahme: **Voice
  of the Triarch** (Silent King) schaltet das *aktive Protokoll* um — ändert aber nicht die
  pro-Runde-Direktiv-Wahl.
- **WAAAGH! Stage 1:** ORKS CORE/CHARACTER dürfen nach Advance chargen; +1 S / +1 A für
  ALLE ORKS.
- **Cover:** Dense (−1 Hit) + Light (+1 Save) nur Shooting; Heavy (+1 Save) nur Melee,
  außer der Verteidiger hat gechargt.
- **Resurrection Orb / RP:** keine KERN-Einschränkung; `<DYNASTY>`-Einheiten; RP-Gate
  läuft über `unit.rules`.
- **FNP (Feel No Pain):** greift gegen normale UND tödliche Wunden; pro Wunde nur eine
  Ignore-Regel.
- **Fight Phase:** startet mit dem inaktiven Spieler; CHARGED-Einheiten zuerst, dann
  abwechselnd. (Katalog: `R-COMBAT-32`.)
- **Heroic Intervention:** Schritt 2 der Charge Phase, nur CHARACTER, ≤ 3", muss näher
  zum Feind enden.
- **extra_attacks — zwei Klassen:** „+N additional" → `unit.attacks + N`; „+N AND no
  more than N" → fester Cap N (`max_attacks`). Boss-Nob-Waffen: nur der Boss Nob trägt
  Spezialwaffen.
- **Skorpekh Destroyers:** feste Komposition 1 Reap-Blade je 3 Modelle (kein Wahl-Wargear).
- **⚠️ Necron Command Protocols — App-Modell ≠ 9E-Regel:** Die YAML-Direktiven
  (`faction_abilities.yaml`: „+1 save / reroll save 1", „+1 Ld / reroll hit&wound 1") sind eine
  **vereinfachte, nicht-kanonische** Fassung. Echte 9E-Direktiven (z. B. Eternal Guardian = Light
  Cover / Charge-Reaktion; Conquering Tyrant = Aura-Range / Fall-Back-Schuss) stehen in
  `wahapedia_necrons/faction_overview.txt`. Offener Entscheid → `backlog.md` §4b. Nicht still
  „korrigieren" — Engine + Tests hängen am vereinfachten Modell.
- **Eternal Guardian D1 — Stationär-Bedingung (Plan 025 Step 4):** D1 gilt 9E-wörtlich „each
  time an attack is made against this unit" (jede Phase). Implementiert: Bedingung ist
  `state["movement_choice"] == "stationary"` (gesetzt in `unitMutations.py`). **Variante C:**
  Checkbox vorgehakt + disabled nur im Shooting-SAVE-Block (A1-Entscheidung: pragmatisch, deckt
  90 %). Light Cover wird **NICHT** zusätzlich in `_collect_def_save_modifiers` gesammelt — das
  würde Doppel-+1 erzeugen. Die Checkbox-Mechanik setzt den +1 genau einmal. Engine-Fn:
  `get_active_round_choice_light_cover_if_stationary(def_player, def_uid)`. Fallback-Label im
  Badge kommt aus YAML via `get_short_label_for_effect_type` — kein Fraktions-String im Code.
