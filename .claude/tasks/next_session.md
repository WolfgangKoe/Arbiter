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

## Aktueller Stand (nach Session 2026-06-12 — 783 Tests grün, 90 % Coverage)

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
- **Session 36: Bugfixes + offene Cover/Attacken-Konzeptfragen**
  - Da Irongob Zielfilter: `_render_mortal_after_melee` filtert `candidates` jetzt per `_is_target_engaged` ✅
  - Dakka-Format `"5/3"` in `_compute_attacks` + `_total_attacks_int`: `N` (Würfelanzahl) korrekt extrahiert ✅
  - Boss-Nob-Limit per Ziel: `max_value=weapon_max` statt `total_attacks` im atk_counter; `1_per_5` ebenfalls abgedeckt ✅
  - Save-Modifier-Würfelpaar: AP-Farben korrekt (grau=from_thresh, rot=to_thresh). Cover-Farben noch offen — siehe neue Aufgaben unten.
- **Session 37: Save-Modifier-Fix + Shooting-Restriction-Fix + 6m-Planung**
  - Save-Modifier: `save_modifier_die_pair_html` neue Signatur `(armour, value, label, color)`; alle Rows jetzt relativ zu `armour` (nicht kumulativ). Buff: blue(armour-N)→grey(armour); Debuff: grey(armour-1)→red(armour+N-1). ✅
  - Shooting model_restriction: `1_per_10`/`boss_nob_only`/`1_per_5` jetzt auch im Schussangriffs-Pfad korrekt (eff_models aus models_alive, nicht slider). ✅
  - 6m Modellgruppen vollständig geplant → dokumentiert in `docs/goals/ziel6.md##6m`
- **Session 39: 6m Tasks F+J + Doppelklick-Fix + Gruppe-für-Gruppe-Flow + Review (13 Punkte → 6n)**
  - Task F final: subUnitCards in den PlayerAreas der gameActionsArea (`render_group_cards`/`render_group_assignment` in `_common.py`), NICHT in der Armeeliste (Nutzer-Entscheidung). Ziel-Button ▷ weist Ziele der selektierten Gruppe zu (`group_targets`); Einzelmodell-Gruppe → max 1 Ziel; fertige Gruppe kollabiert (`group_decl`), ✎ Edit möglich; „Start Resolution →" sammelt alle Entries.
  - Task J: loader_contract.md (`group_loadouts`) + unit_states.md (`group_models` + Flow) dokumentiert
  - Doppelklick-Bug Fight Phase GEFIXT: app.py rendert linke Armeeliste VOR dem Phase-Handler; `fight_current_player`-Wechsel ohne `st.rerun()` ließ veraltete Buttons stehen (1. Klick traf ▷ statt ▶). Fix: rerun bei jeder Änderung (Init + `_advance_fight_turn_if_needed`). 4 Regressionstests.
  - State-Reset: `reset_group_declaration_state()` bei Unit-Wechsel, Phasenwechsel (`_reset_phase_state` + ←-Button), Resolution-Start
  - 574 Tests grün (15 neue: test_group_flow.py, test_fight_turn_advance.py)
  - **Nutzer-Review mit Screenshots: 13 Befunde → vollständig dokumentiert in `docs/goals/ziel6.md##6n`** (Blöcke A–E, freigegeben). Entscheidungen: Reihenfolge A→B→C→D→E; Boss-Nob-Zweifachwahl GENERISCH; für Würfel-Sequenz (D5) und Farben (E2) erst Schema/Mockup vorlegen.
  - **6n A–D + E2 umgesetzt (gleiche Session):** A1 Engagement-Check (`group_target_selectable`, ▷ disabled); A2 kein fight-turn-Advance während aktiver Resolution (fought wird beim ersten Apply gesetzt!); A3 `seq`-Namespacing der res_*-Keys; A4 `show_wound_buttons=False` Charge; B1 Waffen-Zeilen + Grenade-Cap 1; B2 dynamische Counter-Caps + Budget oben; C1 weapons-Union im Loader; C2 generisches `weapon_swaps`-Schema (ersetzt optional_* komplett, alle 8 Ork-Einheiten + Roster migriert); D1 Regelkasten oben/alle Phasen + VP unten; D2/D3 Damage/RP halbe Breite; D4 Tab-CSS (`stTab`-Selektor verifiziert); E2 `docs/spec/design_colors.md`-Entwurf. 583 Tests grün.
  - **Manuell zu verifizieren:** Fight Phase: nur engaged Ziele wählbar, Wechsel erst nach „All done"; Resolution-Tabs starten frisch; Charge ohne Wound-Buttons; Schuss-Zuweisung ohne Multiselect, Überbuchung unmöglich, Stikkbombz max 1; Boyz-Roster: 5 Slugga-Boys + 3 Shoota-Boys + 1 Big-Shoota + Boss Nob (PK+BC); Nobz-Untergruppen; Regelkasten in allen Phasen oben, VP unten.
- **Session 38: 6m Modellgruppen vollständig implementiert (Tasks A–E, G/H, I)**
  - YAML: `model_groups` für boyz, kommandos, stormboyz, warbikers, beast_snagga_boyz, meganobz, nobz, tankbustas; squighog_boyz homogen (kein `model_groups` nötig); `model_restriction` entfernt
  - Rosters: `group_loadouts` für boyz + warbikers (boss_nob → power_klaw)
  - `ModelGroup` + `ModelGroupSpec` dataclasses in `unit.py`; `Unit.model_groups: list[ModelGroup]`
  - `loader.py`: `_parse_model_group_specs()` + `_resolve_model_groups()` (remainder/models_max/per_model + optional_one_of/per_10/per_5 aus Roster aufgelöst)
  - `game_state.py`: `group_models` init aus aufgelösten `model_groups`
  - `unit_mutations.py`: `_apply_group_losses()` → reduziert nach priority bei `apply_damage()`
  - `_common.py`: `_render_group_declaration()` — Schuss- + Nahkampfdeklaration per Gruppe (Waffen aus `group.weapons`, Budget = `group.count × attacks`); `render_attack_declaration` dispatcht wenn `unit.model_groups` gesetzt
  - 13 neue Tests → 559 grün
- **Coverage-Session 2026-06-11: 80 %-Gate aktiv — 760 Tests grün (90 % Coverage)**
  - `pyproject.toml`: `[tool.coverage.run]` omit-Liste (uiLayout, *Phase.py, app.py) + `fail_under=80`; `pytest --tb=short` mißt jetzt automatisch
  - `deploy.yml` (GitHub Actions): installiert `requirements-dev.txt`; Gate wirkt in CI
  - `CLAUDE.md`: Sicherheitsnetz-Regel „rote Tests → STOP, Nutzer fragen" + Meßbefehl dokumentiert
  - 166 neue Tests: test_game_log, test_scenarios, test_phase_runner, test_stratagem, test_weapon, test_game_state (swap_players, _reset_phase_state, WAAAGH-Upgrade, reset_game), test_fight, test_shooting
  - Audit-Bericht `docs/audit/2026-06-11-repo-audit.md` + 5 Executor-Pläne `docs/audit/plans/001–005`
  - Plan 001 vollständig abgeschlossen: Lint-Gates (ruff/black/isort) + mypy (informational) + 80%-Coverage in beiden CIs
- **Audit-Session 2026-06-11 — alle 5 Pläne + 3 Findings erledigt (767 Tests grün):**
  - Plan 001-Rest: `.woodpecker.yml` + Lint-Gates ✅
  - Plan 002: `defusedxml` schützt XML-Parser vor Entity-Expansion-DoS ✅
  - Plan 003: `waaagh_attack_bonus()` zentralisiert, 3 Duplikate in `_common.py` entfernt ✅
  - Plan 004: `lookup()` wirft klare `KeyError` statt nacktem `StopIteration` ✅
  - Plan 005: `_ROUND_CHOICE_CACHE` + `_ROUND_CHOICE_LABEL_CACHE` in `loader.py` ✅
  - Finding #8: `.woodpecker.yml` gelöscht — GitHub Actions ist einzige CI ✅
  - Finding #9: `Makefile` (Flask/Tailwind-Reste) gelöscht ✅
  - Finding #10: `.env.example` auf `DATA_DIR=data` bereinigt ✅
- **Audit-Executor-Session 2026-06-11 — Pläne 009/010/006/007 erledigt (776 Tests grün):**
  - Plan 009: `_resolve_refs` helper + Merge-Block in `_resolve_model_groups`; stille Weapon-Ref-Filter entfernt; 2 neue Tests
  - Plan 010: 5 tote Variablen entfernt (`waaagh` ×3, `effective`, `hit_mod`); `hit_mod` ins Log aufgenommen; F841 aus per-file-ignores; 2 neue Tests
  - Plan 006: `YamlDataError` + `load_yaml` in `loader.py`; alle 17 `yaml.safe_load`-Stellen umgestellt; `game_state.py` 2 Stellen + `import yaml` entfernt; 2 neue Tests
  - Plan 007: `_VALID_NAME` Regex in `scenarios.py`; Pfad-Traversal blockiert; `save_scenario` wirft ValueError; 3 neue Tests
  - 9 neue Tests gesamt; 776 Tests grün, 90 % Coverage
- **Re-Audit-Session 2026-06-11 (abends) — Bericht + 7 neue Executor-Pläne (kein Code geändert):**
  - Bericht: `docs/audit/2026-06-11-reaudit.md` — 8 Findings R1–R8 (3 bestätigte Alt-Findings #6/#7/#11, 5 neue)
  - Neue Pläne `docs/audit/plans/006–012` (Format wie 001–005); `plans/README.md` fortgeschrieben
  - Wichtigste neue Funde: Duplikat-Subgruppen-IDs kollidieren still in `group_models` (009);
    unbekannte Weapon-Refs in Roster-Swaps werden still verworfen (009); 5 tote Variablen
    inkl. `combat.py:105` `hit_mod` (Docstring verspricht Logging) hinter `F841`-Ignore (010);
    ORK-Hardcode-Reste in `waaagh_attack_bonus`/`chargephase` (011); Stratagem-/Ability-Loader
    parsen YAML pro Rerun (012)
  - Coverage-Nuance dokumentiert: `src/uiLayout/*` ist in der omit-Liste → Plan 008 extrahiert
    die reine Attack-Mathematik nach `src/gameMechanic/attack_math.py` (gemessen), Re-Exports
    halten alle Call-Sites/Tests stabil
  - Sicherheits-Callout (Token in Remote-URL) ERLEDIGT: widerrufen + entfernt, Abschnitt in
    `plans/README.md` abgeschlossen

---

## Feature-Plan-Queue (Executor-Sessions) — ⬅️ HIER STARTET DIE NÄCHSTE SESSION

**Session 42 (2026-06-12): Plan 012 abgeschlossen + Feature-Pläne 013–018 erstellt.**
- Plan 012: 5 Cache-Dicts + Guards in `loader.py`; `_ABILITIES_CACHE` aus `armyList.py` entfernt; 4 neue Tests → 787 grün, 90 % Coverage. Commit `f0f4e17`. **Audit-Queue 001–012 damit KOMPLETT.**
- UI-Verifikationen (Plan 008, Session 39/41) vom Nutzer als erledigt bestätigt.
- P16 verifiziert: bereits in `dice_html.py:98-106,193-213` implementiert (×-Marker) → in ziel6.md abgehakt.
- **NEU: `docs/audit/plans/` — 6 Executor-Pläne 013–018** (Format wie Audit-Pläne, README mit Status-Tabelle):

| Plan | Titel | Prio | Status |
|------|-------|------|--------|
| 013 | P18: Einheitlicher Gruppen-Flow (synthetische Einzelgruppe im Loader, Legacy-Pfad raus, Ziele neben Gruppen) | HOCH | TODO ⬅️ NEXT |
| 014 | P17: Verteidiger-Korrektur Schadenszuweisung (±-Counter pro Gruppe, Snapshot, Waffen-Wegfall-Anzeige) | HOCH | TODO (zwingend NACH 013) |
| 015 | Reaktive Stratagems: Overwatch, Counter-Offensive, HI-Hook, once_per_battle | MITTEL | TODO |
| 016 | Protokoll-Effekte auf RP (`rp_reroll`/`rp_bonus`) + Dynastiebonus-Anzeige | MITTEL | TODO |
| 017 | SAVE-Block: Fähigkeits-AP kombinierte Badge (`ap_modifier`-Schema) | MITTEL | TODO |
| 018 | Kleinkram: CP-Doppelvergabe (Bug!), Battle-Log-Reset, Gretchin Cowardly, Modifier-Konsolidierung | NIEDRIG | TODO |

Empfohlene Reihenfolge: **013 → 014 → 016 → 018 → 015 → 017** (Begründung + Konfliktregeln in `docs/audit/plans/README.md`).
Wichtig: Pläne 013/014/015 enthalten **Mockup-Stopps** — UI-Layouts erst dem Nutzer zeigen, dann implementieren.

---

## Audit-Queue (ERLEDIGT — Historie)

Das Re-Audit vom 2026-06-11 (`docs/audit/2026-06-11-reaudit.md`) hat die Queue mit
7 neuen Plänen gefüllt. Alle Pläne sind abgeschlossen.

**Session 40 (2026-06-12): Plan 008 abgeschlossen.**
- `src/gameMechanic/attack_math.py` (NEU): 6 reine Mathe-Funktionen aus `_common.py` extrahiert; 89 % Coverage; zählt ab sofort ins 80 %-Gate.
- `src/uiLayout/dice_html.py` (NEU): kompletter SVG-Würfel-Block (13 Funktionen + Konstanten); 490 Zeilen.
- `src/uiLayout/_common.py`: von 2084 → 1594 Zeilen; Re-Exports halten alle Aufrufer/Tests stabil.
- **Manuelle UI-Verifikation ausstehend:** Shooting- und Fight-Phase bis zur Resolution durchspielen.

**Session 41 (2026-06-12): Plan 011 + vollständige Fraktions-Bereinigung abgeschlossen.**
- `activated_abilities` (generisch) ersetzt `waaagh_state` in game_state, armyCard, ability_engine
- `buff_stat_bonus`, `ability_invuln_save`, `ability_badge_label` — generisch, YAML-datengetrieben
- `waaagh_attack_bonus()` Wrapper entfernt; alle `waaagh_*` lokalen Variablen umbenannt
- RP-Gate: `fdir.startswith("necron")` → `"reanimationProtocols" not in def_unit.keywords`
- Resurrection Orb: `_RES_ORB_ID`-Konstante entfernt; `handler: resurrection_orb` in `wargear.yaml`; `wargear_ids_with_handler()` in `loader.py`; commandPhase findet Orb-ID zur Laufzeit
- WAAAGH-Effekte in Combat (grüner Rahmen) + unitCard-Badge vollständig
- `grep -rn "waaagh|startswith.*necron|_RES_ORB_ID" src/` → 0 Treffer
- 783 Tests grün, 90 % Coverage

Reihenfolge einhalten — nächster Plan = erster offener Eintrag:

| Plan | Datei | Titel | Status |
|------|-------|-------|--------|
| 001–005 | *(Erst-Audit)* | CI-Gates, defusedxml, WAAAGH-Bonus, lookup, Loader-Cache | **DONE** (2026-06-11) |
| 009 | `009-roster-group-validation.md` | Duplikat-Subgruppen mergen + unbekannte Weapon-Refs laut melden | **DONE** (2026-06-11) |
| 010 | `010-dead-vars-f841-gate.md` | 5 tote Variablen raus + F841-Lint scharf | **DONE** (2026-06-11) |
| 006 | `006-safe-yaml-load.md` | `yaml.safe_load` → `load_yaml`-Helper mit klarer Fehlermeldung | **DONE** (2026-06-11) |
| 007 | `007-scenario-name-validation.md` | Scenario-Namen-Allowlist (Pfad-Traversal) | **DONE** (2026-06-11) |
| 008 | `008-split-common-god-module.md` | `_common.py`: Attack-Mathe → gemessenes Modul + Dice-HTML auslagern | **DONE** (2026-06-12) |
| 011 | `011-data-driven-waaagh.md` | WAAAGH datengetrieben (P3 — spätestens vor 4. Fraktion) | **DONE** (2026-06-12) |
| 012 | `012-loader-cache-consolidation.md` | Restliche Loader cachen (P3 — zwingend NACH 006) | **DONE** (2026-06-12) |

**Konflikt-Regeln:** 006/009/012 ändern alle `loader.py` → nie parallel; 010 zwingend vor 008;
008 und 011 nicht parallel. Details in `docs/audit/plans/README.md`.

**Dazwischenschieben:** Dringende Bugs (P20-Klasse) oder Nutzer-Entscheidungen können jederzeit vorgezogen werden — danach einfach beim nächsten offenen Eintrag in der Tabelle weitermachen.

---

## Nächste Schritte (Feature-Plan, priorisiert) — ⚠️ VERALTET, ersetzt durch `docs/audit/plans/` (Session 42)

> **Stand 2026-06-12: Diese Liste ist Historie.** Von den Punkten unten sind
> P20, P14, D5, Farbkonzept, P15, P19 und P16 ERLEDIGT (Details in ziel6.md §6n).
> P17 + P18 sind als ausgearbeitete Executor-Pläne 014 + 013 in `docs/audit/plans/`;
> GOs/Necron Command Phase/Gretchin = Pläne 015/016/018. Nur dort weiterarbeiten.
>
> Review-Runde 2 wurde FREIGEGEBEN und größtenteils umgesetzt (2026-06-10, Session 39, 594 Tests grün).
> Erledigt: P14, P15 (inkl. per_3 + Necron-Gruppen), P16 (im D5-Renderer), P19, P20 (Logik gepinnt),
> D5 komplett, Farbkonzept komplett (Buff=grün #4a9a5a, MOVED=blau #60a5fa, RESERVE=#ff9060,
> Relic-/Wargear-Badges entfernt, E1 Army-Ability datengetrieben in armyCard).
> Dazu 3 Nutzer-Bugmeldungen gefixt: Boss-Nob-Budget (_group_melee_budget), Reanimation vs.
> Moralverluste (heal_unit generisch + group_models-Restore), Cover-Checkbox pro Ziel.
> **NOCH OFFEN: P17 (Verteidiger-Korrektur Schadenszuweisung) + P18 (Ziele neben Untergruppen,
> einheitlicher Flow für Einheiten ohne Gruppen)** — Details in ziel6.md §6n.

1. **P20 (Bug, HOCH):** Heroic Intervention hinterlässt ADVANCED+IN MELEE → Einheit kämpft nicht, Kämpfer-Wechsel blockiert. **Analyse-Stand:** `enter_melee` setzt in_melee beidseitig korrekt; `can_fight` prüft nur in_melee/charged/fought — advanced blockiert das Kämpfen NICHT (RAW: Advance verbietet Charge+Schuss, nicht Kampf). ADVANCED-Badge an den Scarabs (= Einheit des AKTIVEN Spielers, in die interveniert wurde) ist regelkonform möglich (Advance im eigenen Zug). Zu reproduzieren: WO genau blockiert der Wechsel — vermutlich nicht can_fight, sondern UI-Pfad (_active_fight-Warnung? auto-skip-Bedingung? selected_unit-Zustand). Repro: Necrons aktiv, Scarabs ADVANCED, Ork-Charakter interveniert in Scarabs, Fight Phase durchspielen.
2. **P14:** Wound-Buttons in Schussphase-Zielspalte raus; Ziele in-melee mit Freunden ▷-sperren
3. **6n D5 — Würfel-Sequenz:** Detail-Spez ist FESTGELEGT (ziel6.md) — Umsetzung in `_common.py` (Dice-HTML); Randfall P16 (Sv>6+) mit abdecken
4. **Farbkonzept umsetzen:** Beschlüsse in `docs/spec/design_colors.md` §0 — Buff=grün `#4a9a5a` / MOVED=blau `#60a5fa` (FESTGELEGT), Cover=Buff-Grün, RESERVE=`#ff9060`, Relic-/Wargear-Badges entfallen, E1 Army-Ability=Buff-Grün datengetrieben
5. **P15:** Necron-Modellgruppen komplett: Skorpekh (`limit: per_3` neu!), Ophydian, Lokhust (+Heavy, gemischte Einheit?), Plasmacyte (Begleitmodell), Cryptothralls (Bodyguard?), Lychguard; Scraper-Lücke (Wargear-Zeilen fehlen in wahapedia_necrons!)
6. **P17 (Task, nachgeschärft):** Verteidiger-Korrektur bei Schadenszuweisung gegen Gruppen-Einheiten — ±-Counter pro Gruppe nach Apply Damage (Default: priority); danach klar zeigen, welche Waffen wegfallen (Nobz-Fall!)
7. **P18:** Nahkampf-UX: Ziele neben Untergruppen anzeigen; Einheiten ohne Gruppen = eine Gruppe (einheitlicher Flow)
8. **P19:** Heavy Cover fehlt beim Power-Klaw-Tab — klären
9. Danach: GOs in gameActionArea / Necron Command Phase / Gretchin Cowardly (s. unten)

---

## Offene Tasks

### 🔴 HOCH — 6n: Reste (D5 + E1, warten auf Nutzer-Entscheidung)

> Blöcke A, B, C, D1–D4, E2 sind FERTIG (2026-06-10, Session 39) — Details + Häkchen in
> `docs/goals/ziel6.md##6n`. Offen: D5 (Mockup-Freigabe), E1 (Farb-Entscheidung §4a in
> `docs/spec/design_colors.md`), Fraktionsfarben-Frage §4c.

**Wichtig (C2):** `weapon_swaps` hat `optional_one_of`/`optional_per_10`/`optional_per_5`/
`per_model_weapon_counts` VOLLSTÄNDIG ersetzt — Schema in `loader_contract.md`.
Roster-Format: group-scope `swaps: {id: {weapons: [...]}}`; per_model-scope
`swaps: {id: [{weapons: [...], count: n}]}` → Sub-Gruppen-Split im Loader.

---

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

### ModelGroup-Pattern (6m)

Einheiten mit strukturell verschiedenen Modellen (z.B. Boyz: 9 Boys + 1 Boss Nob) werden durch `model_groups` in `units.yaml` abgebildet. Drei Typen:
- **Homogen** (alle gleich): kein `model_groups` → alter Pfad bleibt aktiv
- **Strukturell gemischt** (feste Sondermodelle): `count: 1` / `count: remainder`; `optional_one_of` im Roster aufgelöst
- **Per-Model** (jedes Modell wählt individuell): `optional_mode: per_model`; Loader splittet in Sub-Gruppen

State: `unit_state["group_models"]: dict[str, int]` — Modelle pro Gruppe; `models` = Summe daraus.
Tod: `apply_damage()` reduziert nach `priority` (1 = stirbt zuerst = Standardmodelle).
UI: subUnitCard pro Gruppe; Deklaration läuft Gruppe-für-Gruppe, fertige Gruppe kollabiert.

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
