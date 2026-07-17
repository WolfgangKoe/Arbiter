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
- **Kombi-Waffen (B-098 Teil 2, S156):** „Select one or both profiles" ist ein Wahlrecht
  **vor** der Zielwahl, nicht ein permanenter Waffenmalus wie Power Klaw/Killsaw
  (`hit_roll_penalty`). Der −1-Malus gilt nur, wenn **beide** Profile in derselben Phase
  gefeuert werden, und trifft **beide** Profile gleichermaßen — deshalb ein neues
  `WeaponProfile.combi: bool`-Feld statt Wiederverwendung von `effect` (das trägt pro Profil
  schon den eigenen Mechanik-Typ, z. B. `alternating_fire`/`auto_hit` auf dem Shoota/Skorcha-Teil
  desselben Kombi-Waffen-Datensatzes — inkompatibel mit einem zweiten Tag im selben Dict).
  `_combi_hit_penalty()` (attackMath.py) ist reine Berechnung, testbar ohne Streamlit.
  **S157 (R-COMBAT-35) erledigt:** die Profil-Auswahl (Checkbox je Profil statt Radio, sobald
  `any(p.combi for p in profiles)`, `render_group_assignment`/`_common.py`) trägt das Ergebnis
  als `combi_hit_mod` auf dem Deklarations-Entry; `compute_resolution_context` (`_common.py`)
  reicht es als benannten Hit-Modifier-Eintrag (`"Combi (both profiles)"`) in denselben Stack,
  den `resolve_attack_modifiers` (`combat.py`) für Dense Cover/Fall-Back/Heavy-advanced schon
  bedient — kein Sonderpfad in `combat.py` selbst nötig.
- **`weapon_swaps` mit überlappender `replaces`-Liste — Exklusivität nur bei `scope: group`:**
  Der Loader (`_check_exclusive_swaps`, `loader.py`) verweigert zwei **group**-Swaps derselben
  Modellgruppe, wenn beide dieselbe Basis-Waffe ersetzen (z. B. Boss Nob: 2-Waffen-Kombo vs.
  Kombi-Waffe, beide ersetzen slugga+choppa) — ein Roster darf nur eine wählen. **Keine**
  Prüfung bei `scope: per_model`: dort splitten mehrere Swaps unterschiedliche Modell-Untermengen
  derselben Gruppe (z. B. Ork Boyz: shoota_swap + per-10-Spezialwaffen-Swap ersetzen beide
  slugga+choppa, aber auf disjunkten Modellen) — das ist beabsichtigt, keine Kollision.
- **Quantum Shielding — zwei gleichnamige, unabhängige Mechaniken (B-056, S156):** Das
  Stratagem „Quantum Deflection" (temporärer FESTER 4+ Invuln) und die Fahrzeug-Fähigkeit
  „Quantum Shielding" (dauerhaft 5+ Invuln + unmod. Wound 1-3 auto-fail) sind trotz gleicher
  Wortwahl **verschiedene** Mechaniken auf verschiedenen Trägern (Stratagem vs. Unit-Ability) —
  nicht zusammenlegen. Die Wound-Auto-fail-Regel wird generisch als Floor abgebildet:
  `resolve_attack_modifiers(..., wound_auto_fail_max=N)` hebt den Verwundungswurf-Floor von 2
  auf `N+1`, weil der Check gegen den UNMODIFIZIERTEN Wurf greift — kein Wund-Buff kann darunter
  senken (`combat.py`). **INV-4b-Falle:** ein neuer `unit_abilities.yaml`-Ability-`id` mit dem
  Wort „fail" (z. B. `..._wound_auto_fail`) macht „fail" zu einem necron-exklusiven Token in
  `tests/architecture/_vocab.py`'s Datenbank-Scan — und flaggt dann JEDES generische Vorkommen
  von „fail" quer durch `src/` (fightPhase.py, moralePhase.py, chargePhase.py, …), auch in
  Dateien, die mit Necrons nichts zu tun haben. Fix: den `id`-Suffix auf bereits erlaubte
  Stopwords beschränken (`quantum_shielding_wound_deny` statt `..._wound_auto_fail`) — `effect.type`
  selbst ist unkritisch (nicht unter einem NAME_KEYS-Feld gescannt), nur `id`/`keywords`/
  `faction`/`subfaction`/… sind es.
