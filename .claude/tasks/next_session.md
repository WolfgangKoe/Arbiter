# Startprompt — Nächste Session
<!-- Kanonisch: .claude/tasks/next_session.md — nie ins Root-Verzeichnis anlegen. -->

## ⚠️ Session-Regeln (immer beachten)

**Zu Beginn jeder Session lesen:**
- `CLAUDE.md` — Workflow, Freigabe-Pflicht, **Unklarheiten IMMER zuerst fragen**
- `docs/goals/ziel6.md` — vollständige Aufgabenliste mit allen Checkboxen

**Am Ende jeder Session:**
- Checkboxen in `docs/goals/ziel6.md` abhaken
- Diese Datei aktualisieren: Stand + nächster Schritt + neue Erkenntnisse (ZUERST lesen, dann ergänzen)

---

## Was ist Arbiter?

**Arbiter** ist ein digitaler Spielbegleiter für Warhammer 40.000 9. Edition, gebaut in Streamlit (Python).
Start: `streamlit run src/app.py` (Port 8501)
Branch: `dev` (Entwicklung), `main` (stabiler Stand, nur per PR)

---

## Aktueller Stand (nach Session 35, 2026-06-09)

- Ziel 1–5 vollständig abgeschlossen
- Ziel 6a–6k vollständig committed (inkl. 6j YAML-Konsolidierung)
- 6d-v3 Würfel-UI vollständig (Treffer/Verwundung/Save-Blöcke mit SVG-Würfeln, Modifier-Paaren, 7+-Handling)
- Cover: 3 phasengebundene Checkboxen (Dense → HIT, Light/Heavy → SAVE)
- Fight Phase: beide Spieler alternieren korrekt; CHARGED-Priorität; inaktiver Spieler startet
- Heroic Intervention: Step-2-Timing, CHARACTER-Check, Badge, Feind-Zielauswahl
- 6k: `persistent_effects` Interpreter; `wargear_ids`/`wargear_keywords` auf Unit; Resurrection Orb via Wargear-ID
- Session 28: WAAAGH! Advance+Charge, +1 Attacks in Melee, per-weapon atk_counter ✅
- Session 29: Ork Waffen-Audit — Befunde 1/2/3 dokumentiert in `docs/goals/ziel6.md`
- Session 30: extra_attacks + model_restriction implementiert — `WeaponProfile.max_attacks`, Klasse 3a/3b korrekt berechnet, Boss-Nob-Badges in Deklarations-UI, 25 neue Tests
- Session 31: Weapon-Strength-Bugfix + Architektur-Bereinigung — `_parse_strength` akzeptiert `int | str` nativ; `WeaponProfile.ap: int`; 510 Tests grün
- **Session 32: 6l Relic-Effekt-Interpreter + Bug Heavy Cover**
  - Bug: Heavy Cover `charged`-Check war `atk_state` → jetzt `def_state` (Regel: Defender verliert Cover wenn er selbst charged hat, nicht der Angreifer)
  - 6l Phase 1: `Unit.relic_id`; `load_relic_catalog()`; `_apply_relic()` (Waffenersatz + `persistent_effects`); `buff_stat: toughness/strength`; Roster-Key `relic: <id>`; Relic-Badge (gold) auf unitCard; 9 neue Tests → 519 grün
- **Session 33: Bugfix `_parse_strength` — User×N Notation**
  - Bug: `power_klaw`, `killsaw`, `gorks_klaw`, `dread_klaw` (alle `strength: User×2`) crashten die Resolution mit `ValueError` — `_parse_strength` kannte nur `"×N"` isoliert, nicht `"User×N"`
  - Fix: `_parse_strength` strippt jetzt optional das `"User"`-Präfix vor dem Operator → `"User×2"`, `"User+3"`, `"User-1"` alle korrekt
  - 14 neue Regressionstests in `tests/uiLayout/test_common.py` → 533 grün
- **Session 34: 1_per_10 Restrictions + Cover-Würfel-Bugfix**
  - `model_restriction: "1_per_10"` für Boyz (big_shoota, rokkit_launcha) und Kommandos (6 Waffen) in `units.yaml`; 2 neue Tests → 535 grün
  - Bugfix Cover-Würfelpaare in `_common.py`: Dense Cover grau=from_thresh−1/rot=from_thresh; Light/Heavy Cover beide Würfel zeigen from_thresh−1 (Übergang fail→save); Effective-Save-Zeile zeigt immer Rüstungsweg (nicht Invuln)
- **Session 35: 6l Phase 2 data-driven + Da Irongob Workflow**
  - `TriggeredEffect` Dataclass + `Unit.get_triggered_effect()` + `relic_name`; Loader parsed `triggered_effects` aus YAML
  - Alle hardcodierten Fraktions-IDs aus `src/` entfernt (`_VEIL_ID`, `_MORGOG_CAP_ID`, `da_irongob`-Literal) — rein datengetrieben über `effect`-Typ
  - Relic-Badge zeigt jetzt `relic_name` statt deutschen ID-Fragment
  - Veil of Darkness: `movement_locked` flag → Bewegungsbuttons nach Teleport gesperrt; `_undo_teleport` via Undo-Button (bis Zugwechsel)
  - Da Irongob: 2-stufiger Workflow — Zielauswahl + Failed/Continue, dann +/−-Counter für D3-Ergebnis + Apply; Undo-Banner bis Zugwechsel; 547 Tests grün

---

## Nächste Schritte (priorisiert)

1. 🔴 **Bugfix: Da Irongob Zielfilter** — Zielauswahl muss auf Einheiten beschränkt werden, die `in_melee` mit dem Träger sind (Regel: "within 1\"" = im Nahkampf). Aktuell werden alle nicht-zerstörten Feinde angezeigt. Fix: in `fightPhase.py → _render_mortal_after_melee` Step "initial" die `candidates`-Liste um `[atk_faction, uid] in enemy_units_state.get(sk, {}).get("melee_with", [])` filtern.
2. 🔴 **Bugfix: Light/Heavy Cover Würfelfarben** — Screenshot zeigt falsches Ergebnis: grauer Würfel müsste `2` zeigen, blauer `3`, und die Farben sind vertauscht. Fix in `src/uiLayout/_common.py` Cover-Würfel-Rendering-Logik. Regelkontext: Light Cover = +1 Save (Schwelle save−1), Heavy Cover = +2 Save. Grau = Fail-Schwelle (save−1), Blau/Rot = Erfolg-Schwelle.
3. **GOs in gameActionArea** — kontextuelle GO-Buttons für aktiven + inaktiven Spieler
3. **Necron Command Phase** — Protokoll-Effekte auf Living Metal / RP-Verbesserungen; Dynastiebonus; Anzeigereihenfolge
4. **WAAAGH! Gretchin Cowardly** — Moralphase: −1 Attrition wenn kein RUNTHERD in 6"

---

## Offene Tasks

### 🔴 HOCH — extra_attacks-Effekt implementieren (Audit Session 29)

Waffen mit `effect.type: extra_attacks` werden von `_compute_attacks()` und `_total_attacks_int()` ignoriert. Zwei Klassen:

**Klasse 3b — fester Cap** (`max_attacks: N`, unabhängig von `unit.attacks`):
- [ ] `data/wh40k_9e/orks/weapons.yaml`: `max_attacks`-Feld für attack_squig (2), squighog_jaws (2), squigosaur's_jaws (3), smasha_squig_jaws (2), grabbin_klaw (1), wreckin_ball (1), butcha_boyz (4), savage_horns_and_hooves (4) ergänzen
- [ ] `gameObjects/weapon.py`: `WeaponProfile.max_attacks: int | None = None`
- [ ] `gameObjects/loader.py`: `max_attacks` parsen
- [ ] `uiLayout/_common.py`: `_compute_attacks()` + `_total_attacks_int()` — wenn `max_attacks` gesetzt: `models × max_attacks`; sonst wenn `extra_attacks.amount`: `models × (unit.attacks + amount)`

**Klasse 3a — additiv** (`unit.attacks + N`):
- Waffen: choppa, beastchoppa, 'urty syringe, grabba stikk, dread klaw, grot_prod
- Wird durch obige Änderung automatisch mit abgedeckt (kein `max_attacks` → `+amount`)

### 🔴 HOCH — model_restriction in YAML + UI-Filter (Audit Session 29)

- [ ] `data/wh40k_9e/orks/units.yaml`: `model_restriction: boss_nob_only` für betroffene Waffen in boyz, warbikers, stormboyz, kommandos; `model_restriction: "1_per_10"` / `"1_per_5"` für Spezialwaffen
- [ ] `gameObjects/unit.py`: `WeaponRef`-Dataclass um `model_restriction: str | None = None` erweitern
- [ ] `gameObjects/loader.py`: `model_restriction` aus `weapons[]`-Einträgen parsen
- [ ] `uiLayout/_common.py`: `render_attack_declaration()` — Boss-Nob-Waffen kennzeichnen (Badge) oder aus Standard-Auswahl herausfiltern

### 🟡 MITTEL — GOs in gameActionArea

- [ ] GO-Buttons kontextuell direkt in gameActionArea (aktiver + inaktiver Spieler), nicht als Liste
- [ ] Overwatch als reaktive GO in Charge Phase
- [ ] Counterattack GO in Fight Phase (reaktive Unterbrechung) — Teil von 6e
- [ ] GOs die Non-CHARACTER HI erlauben (z.B. `enslaved_protectors`) → HI-Eligibility erweiterbar

### 🟡 MITTEL — Necron Command Phase

- [x] Living Metal: einmalig pro Phase ✅ (2026-06-08)
- [ ] Protokoll-Effekte auf Living Metal / RP-Verbesserungen abbilden
- [ ] Dynastiebonus: wenn Direktive durch Dynastiezugehörigkeit gilt → Effekt anzeigen
- [ ] Anzeigereihenfolge: Regelkasten immer ganz oben in allen Phasen

### 🟡 MITTEL — WAAAGH!

- [x] WAAAGH!-Badge auf unitCards ✅ (2026-06-08)
- [x] **Advance & Charge:** `chargephase.py` — WAAAGH! Stage 1 + ORKS CORE/CHARACTER → advanced-Block überspringen ✅ (2026-06-08)
- [x] **+1 Attacks:** `render_attack_declaration` → `_total_attacks_int()`: +1 auf `unit.attacks` wenn WAAAGH! aktiv + ORKS-Keyword; gilt für Stage 1 und Stage 2 ✅ (2026-06-08)

### ✅ Nahkampf-Deklaration regelkonform — ERLEDIGT (2026-06-08)

Melee-Pfad auf per-weapon `atk_counter` umgestellt. Jede Waffe bekommt eigenen Counter pro Ziel (kein Multiselect mehr). Summe aller Counters = Gesamtattacken. 15 neue Tests.

### 🟡 MITTEL — Fähigkeit + AP kombiniert (SAVE-Block)

- [ ] `Enslaved AP-1` o.ä. als kombinierte Badge darstellen — erfordert 6j/6l YAML-Erweiterung

### 🟢 NIEDRIG

- [ ] Gretchin Cowardly: −1 auf Combat Attrition Tests wenn kein RUNTHERD in 6" (Ld 4)
- [ ] Nach Reset keine alten Einträge im Battle Log (6g)
- [ ] CP-Doppelvergabe-Fix + `collect_modifiers_for_phase()` (6e)
- [ ] Hardcoded Fraktionslogik herauslösen (6h)

---

## Wichtige Constraints (unveränderlich)

- **Freigabe vor Umsetzung** — Plan + Dateiliste zeigen, auf „ja" warten
- **Planergänzung ≠ Freigabe** — Plan neu zeigen, nochmal warten
- **Kein Memory/Subagent/Skill ohne Freigabe**
- dev-Branch, kein direktes Committen auf main
- Seitenleisten: `first_player` links, `second_player` rechts (unveränderlich)
- Keywords immer `UPPERCASE` in YAML
- `_parse_strength(raw: int | str, unit_strength)` für Waffenstärke — akzeptiert native YAML-Typen; nie `int(strength)` oder `str(strength)` direkt
- Weapon strength in YAML: plain int = feste Stärke, `"+N"` = User+N, `"×N"` = User×N, `"User"` = User; **auch `"User×N"`, `"User+N"`, `"User-N"` werden von `_parse_strength` akzeptiert** — Ork-YAML nutzt diese Form (power_klaw, killsaw etc. = `User×2`)
- Regelreferenz: Immer erst lokal nachschlagen (`docs/work/wahapedia_*/`), nie Nutzer fragen

---

## Architekturmuster

### Reset-Button-Pattern für Fähigkeits-gesetzte Zustände
Wenn eine Fähigkeit/ein Relikt den Zustand einer Einheit setzt (z.B. `movement_choice`, `turn_flags`), MUSS es eine Undo-Möglichkeit geben, solange der Zug noch läuft. Implementierungsmuster:
- `turn_flags["<ability>_locked"] = True` setzen beim Aktivieren → dient als Unterscheidungsmerkmal zu normalem Spielerzug
- In der betroffenen Phase-UI: wenn `<ability>_locked`, Buttons deaktivieren + Undo-Button zeigen
- Undo löscht das `_locked`-Flag und setzt betroffene Felder zurück
- Nach Zugwechsel (`reset_turn_flags`): `_locked`-Flags automatisch weg → kein Undo mehr möglich (State ist "fest")
- Beispielimplementierung: Veil of Darkness (`turn_flags["veil_moved"]`) in `movementPhase.py`

---

## Regelerkenntnisse (nicht-offensichtlich)

- **WAAAGH! Stage 1:** Nur ORKS CORE und ORKS CHARACTER dürfen nach Advance chargen (nicht alle ORKS). +1 Strength und +1 Attacks gilt für ALLE ORKS-Modelle. GRETCHIN-Ausnahme gilt nur für Waaagh! Energy-Zählung.
- **WAAAGH! Aktivierung:** Erfordert, dass der WARLORD ein WARBOSS ist (nicht nur irgendein WARBOSS auf dem Feld). Aktuell prüft die App nur ob irgendeine Einheit das WARBOSS-Keyword hat — streng genommen müsste der WARLORD-Status geprüft werden (noch nicht implementiert, pragmatische Näherung akzeptiert).
- **Resurrection Orb**: Keine KERN-Einschränkung — gilt für alle `<DYNASTY>`-Einheiten.
- **FNP**: Gilt für alle Wunden — normale UND tödliche. Pro Wunde nur eine Ignore-Regel verwendbar.
- **Fight Phase**: Startet mit dem **inaktiven** Spieler. CHARGED-Einheiten aller Spieler kämpfen zuerst, dann abwechselnd.
- **Heroic Intervention**: Schritt 2 der Charge Phase (nach allen Charges). Nur CHARACTER. ≤3" Bewegung, muss näher zum nächsten Feind enden.
- **extra_attacks — zwei Klassen:** Waffen mit „+N additional attacks" geben `unit.attacks + N` Attacken. Waffen mit „+N additional attacks AND no more than N attacks" geben immer genau N Attacken (cap), unabhängig von `unit.attacks`. Zweite Klasse: attack_squig (2), squighog_jaws (2), squigosaur's_jaws (3), grabbin_klaw (1), wreckin_ball (1), butcha_boyz (4), savage_horns_and_hooves (4).
- **Boss-Nob-Waffen:** In Ork-Einheiten mit mehreren Modellen trägt nur der Boss Nob Spezialwaffen (power klaw, big choppa, killsaw). Bestätigt für: boyz, warbikers, stormboyz, kommandos. Nicht betroffen (alle Modelle): nobz, meganobz, squighog boyz.
- **Stärke-Parsing:** `_parse_strength(raw: int|str, unit_strength)` in `_common.py` — int → feste Stärke, `"+2"` → unit_strength+2, `"×2"` → unit_strength×2, `"User"` → unit_strength, `"*"` → 0 (Spezialwaffe). YAML-Bug war: `+2` wurde von PyYAML als int 2 geparst (Plus verloren) — gefixt durch Quoting `"+2"` in Ork-YAML und Normalisierung `"User+2"` → `"+2"` in Necron-YAML.
