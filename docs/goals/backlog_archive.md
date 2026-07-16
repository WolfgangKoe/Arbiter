# Backlog-Archiv — Erledigtes & Verworfenes

> **Dies ist KEIN zweiter Backlog.** Hier landet ausschließlich, was in
> [backlog.md](backlog.md) als erledigt oder bewusst verworfen markiert war und
> keinen offenen Rest mehr trägt. Offene Arbeit — auch wenn sie Teilaspekte eines hier
> archivierten Punkts berührt — gehört ausschließlich in `backlog.md`. Jeder Eintrag
> trägt seine Session-Angabe unverändert aus dem Backlog fort (keine Umformulierung).
>
> Angelegt S150 (Stakeholder-Auftrag „Alles was fertig ist, kann ins Archiv", S149-Wortlaut).
> Gruppiert nach Herkunfts-Abschnitt im Backlog zum Zeitpunkt der Verschiebung.

---

## Aus §0 Aktuelle Findings

- ✅ **R-CMD-03 — CP-Grant ohne Battle-forged-Gating — ERLEDIGT (S123-Verifikation):**
  `commandPhase.can_gain_command_point(game_mode)` gated den „Grant +1 CP"-Button bereits
  (`_render_faction_actions` returnt für Open Play früh, zeigt „Open Play — no Battle-forged
  CP grant."). Ledger-Eintrag [../spec/acceptance/rules.md](../spec/acceptance/rules.md) §R-CMD-03
  führt `status: implementiert`, getestet: `test_matched_play_is_battle_forged` /
  `test_open_play_is_not_battle_forged`. Eintrag hier war stale (Fix + Ledger-Update erfolgten,
  ohne diesen Backlog-Punkt zu schließen).
- **INV-4 Default-Roster** (`gameState.py`, `loader.py`) — Teilaspekt aus
  „#INV-4b Cluster-Entscheidungen" (Cluster 1 bleibt offen in `backlog.md`): ✅ **erledigt
  S128** — die 2 DEBT-Einträge (hardcodierte `"necrons"`-Defaults) sind aufgelöst:
  `init_state()`s `roster_p1`/`roster_p2` sind Pflichtparameter, `loader.py`s
  `faction_dir`-Default entfernt (klarer `ValueError` statt stillem Necron-Fallback).
  Allowlist 5 → 3 Einträge (nur noch LEGIT-Rest `roszImporter.py`, nicht 0 — der bleibt
  dauerhaft). Details: [architecture_invariants.md](../spec/architecture_invariants.md) INV-4.

---

## Aus §2 Offene Tasks

- ✅ **Command Re-Roll auf alle 9 Wurf-Arten ausweiten — ERLEDIGT (S136, R-CMD-12 9/9):**
  Stakeholder-AUFLAGE (S130) eingelöst: alle 9 regelerlaubten Wurf-Arten sind jetzt
  inline verdrahtet — Damage/Psychic/Deny als GO-Karte (S135 Paket 4b), Anzahl-Attacken
  (S135 Paket 4c), Advance/Charge (S132/S133), Hit-/Wound-/Save-Wurf in
  `_render_resolution_tab` (S136, pragmatischer Familie-2-Ansatz laut Stakeholder-Entscheid
  `S136_4cc_befund.md`). Details + Testnamen: [../spec/acceptance/rules.md](../spec/acceptance/rules.md) R-CMD-12.
- ✅ **B1 — Scroll-Sprung bei Command-Protocol-Wahl im Setup — ERLEDIGT (S136,
  Stakeholder-bestätigt):** Ursache Layout-Shift + Chrome Scroll-Anchoring (H1
  Fokus-Autoscroll und H2 Sechsfach-Key-Rewrite beide widerlegt, Playwright-Befund
  `docs/handoff/S136_B1_probe.md`: `activeElement` = `<body>`, Layout-Shift bis 0.92 auf
  `stLayoutWrapper`). Fix: `overflow-anchor: none` auf `section[data-testid="stMain"]`
  (`gameHeader.py` `CSS_THEME`) — Playwright-verifiziert Scroll-Delta 0/0/0 (vorher
  +2348). Verankert in `CLAUDE.md` §Streamlit CSS.
- ✅ **B5 — First-Player-Block Redundanz — ERLEDIGT (S134, UI-verifiziert 5/5):**
  Überschrift „Roll-Off for First Player", Buttons nur Armee-Name, „Currently
  selected"-Zeile entfernt. Fundort war `gameActionsArea.py::_render_setup` (NICHT
  `setupScreen.py`); Tests: `tests/uiLayout/test_first_player_block.py`. Screenshot
  `…21-23-28.png` kann gelöscht werden (Punkt DONE).
- ✅ **B6 — Faction-Ability-Wahl auf Player-Ebene — ERLEDIGT (S135, Commit `9993771`,
  stakeholder-verifiziert):** Wahl (Command Protocols, Canticles o. ä.) erscheint jetzt in
  den first/second-Spalten: Setup-Blöcke nebeneinander, „Read directive"-Dropdown
  (geteilter Helper mit `armyCard`, INV-4b 18→17), Trennlinie. Screenshot `…21-27-05.png`
  bereits gelöscht (`283d38e`).
- ✅ **B8 — Redundanter Statusbereich in jeder Phase — ERLEDIGT (S149):** Zeile
  „**{player}** ({role}) · CP: **{cp}**" + Divider in
  `gameProtocoll.py::_render_stratagem_column` entfernt. Verifiziert vor dem
  Löschen: CP wird bereits permanent im App-Header gezeigt
  (`gameHeader.py::_score_group`, aufgerufen von `render_game_header()` in
  `app.py`, first/second_player-Spalten) — keine einzige-Quelle-Regression.
  Screenshot `…21-36-36.png` gelöscht.
- ✅ **CP-Doppelvergabe-Fix — ERLEDIGT (Plan 018 Task 18.1, S128):** `cp_grants`-Set aus
  `(round, faction)`-Paaren ersetzt `cp_granted_this_phase`-Flag; übersteht ←/→-Phasennavigation.
- ✅ **Scraper-Trunkierung `abilities` — Daten-Anteil ERLEDIGT (S138):** 47 Einträge
  (Ork 42, Necron 5) in `faction_abilities.yaml`/`weapons.yaml` vervollständigt; neuer
  netzunabhängiger Wächter `tests/gameObjects/test_data_quality.py` verhindert Rückfall.
  Scraper-Fix-Anteil (Commit `4dcc560`) geprüft — Ursache war Datenstand von vor dem Fix.
- ✅ **color_hint-Feld im Modifier-Dict — ERLEDIGT (Plan 022 Step 3, S77):** Optionales
  `color_hint: "buff" | "debuff"` gewinnt gegen die wertbasierte Farbe (`_modifier_color`,
  `diceCompose.py`), rückwärtskompatibel ohne das Feld. Getestet: `test_color_hint_overrides_value_sign`,
  `test_always_fail_color_hint_buff_is_green` u. a. (`tests/uiLayout/test_dice_html.py`). Eintrag hier
  war stale — Quantum-Shield-Verdrahtung selbst (Konsument) bleibt offen (s. „Quantum Shielding" in `backlog.md`).
- ✅ *(erledigt S129, `3d9b26e` — Review-S130-Befund geschlossen)* **Effekt-Feld `modifier` → `success_on` umbenennen (S128-Folge, Paket 1c/Paket 3
  Parallelsperre):** Die Reanimation-Ability nutzt aktuell das generische `modifier`-Feld
  für die Erfolgsschwelle (5+); klarer wäre ein benanntes `success_on`-Feld. Betrifft
  `gameObjects/ability.py` + `gameObjects/loader.py` (beide durch Paket 3 in S128 gesperrt)
  + `necrons/faction_abilities.yaml` + 2 Asserts in den Ability-Tests. Reine Rename-Arbeit,
  kein Verhaltenswechsel.
- ✅ *(erledigt S129, `3d9b26e` — Review-S130-Befund geschlossen)* **`types-PyYAML` + `types-defusedxml` in `requirements-dev.txt` aufnehmen (S128-Folge):**
  danach die 3 `[import-untyped]`-`# type: ignore`-Kommentare in `gameObjects/` entfernen —
  im selben Schritt, sonst meldet mypy `unused-ignore` (neuer Fehler gegen die Baseline).
- ✅ **Dynastie-Affinität „beide Direktiven" beim rundenzugewiesenen Protokoll — ERLEDIGT (S140,
  S96-UI-Befund, S97 bestätigt):** Regel (`faction_overview.txt` Z. 862–871): wird das
  Affinitäts-Protokoll _aktiv_ (egal ob 6./permanent oder einer Runde zugeteilt) und hat die ganze
  Armee den Dynastie-Code, gelten **beide** Direktiven statt einer. S140: Round-Zweig von
  `_active_directive_effects` + `active_round_choice_buff_labels` werten `subfaction_affinity` aus
  (Gate `has_round` auf `bool(active_id)` gelockert); UI `_render_round_choice_ui` zeigt bei
  Affinität das „… BONUS (BOTH)"-Badge ohne Wahlzwang (analog Extra-Protokoll-Pfad,
  `_render_directive_buttons` unverändert). Regressionstests je Dynastie in
  `test_ability_engine.py` / `test_game_state.py`. Konzept `S139_dynastie_protokoll_konzept.md` → DONE.
- ✅ **Bug — MWBD-Ability bei zwei gleichen Einheiten gekoppelt — ERLEDIGT (S147):**
  `_buff_ability_state_key(bearer_uid, ability_id)` analog Wargear-Muster; State-/Widget-Keys
  + `TargetSelectionRequest.ability_id` instanz-eindeutig; 3 Regressionstests
  (`TestBuffRollAbilityInstanceScoping`). Manuelle UI-Verifikation offen (§3, Roster
  `necrons_b1_verification.yaml` mit 2× Overlord).
- ✅ **B1 aus S146-Review — Doppel-Rendering on_target-GOs — ERLEDIGT (S147):**
  Stakeholder-Entscheid: Ziel-Kachel einziger Ort; Hit-/Save-Anker für on_target-GOs
  entfernt (`_common.py`), 2 Positiv- + 2 Negativ-Tests (B2), `design_system.md` §6.2/6.3
  nachgezogen. Manuelle UI-Verifikation offen (§3, Roster `necrons_b1_verification.yaml`).

---

## Aus §4 Architektur-Schulden

- ✅ **Generic-src Vokabular (INV-4b DEBT, S51; `protocol` erledigt S52) — DEBT komplett
  aufgelöst (S128 Teil 2, Paket 1):** datengetriebenes Gate (`test_generic_src_vocab.py`)
  listet Fraktions-Eigennamen in `src/`. ✅ **S52:** `protocol`/`protocols` faktion-neutral
  als `round_choice` umbenannt (Klasse `RoundChoiceAbility`, Session-Keys `round_choice_*`,
  Datei `roundChoiceAbility.py`), Ledger-Einträge entfernt; Reste LEGIT (`typing.Protocol`
  in `phaseHandler`) bzw. zur `reanimation`-Schuld (`reanimationProtocols`). ✅
  **2026-06-20:** Quick-Wins (Spielerlabels `gameHeader`/`gameProtocoll`, Caption
  `setupScreen`) → generisch; Renames `pending_irongob` → `pending_triggered_relic`,
  `res_orb_*` → `revive_wargear_*` (`irongob` komplett raus; INV-4 Allowlist 10→5, INV-4b
  20→19 Tokens). ✅ **S128 Teil 2:** die drei verbliebenen DEBT-Cluster aufgelöst —
  **a)** `dynasty` (`movementPhase.py`): Teleport-Relic-Texte nach `necrons/relics.yaml`
  verlagert (`prompt_text`/`selector_label`); **b)** `gloom`/`prism` (`psychicPhase.py`):
  Deny-Caption fraktions-neutral formuliert; **c)** `protocols`/`reanimation`
  (`uiLayout/_common.py`): `reanimationProtocols`-Key-Abfrage durch den generischen
  Effekttyp `reanimate` ersetzt (Option B, Konsens-Entscheid
  `docs/handoff/decision_revive_key_s128.md`, seit S128 gelöscht) — Label + Schwelle
  (`success_on`) kommen jetzt aus der Necron-YAML, `src/` kennt nur noch den generischen
  Effekttyp. Ledger jetzt **nur noch LEGIT** (6 Tokens, 3 Dateien: `roszImporter.py` +
  `protocol`-Kollision in `phaseHandler.py`/`abilityEngine.py`). Die früher hier
  gelisteten Items `orb`/`overlord`/`phaeron`/`dakka`/`klaw`/`tesla`/`arkana` waren bereits
  vor S128 aus `src/` entfernt — dieser Eintrag war insofern Doku-Drift, jetzt korrigiert.
  Details: [architecture_invariants.md](../spec/architecture_invariants.md) INV-4b.
- ✅ **Coverage-Schuld: gameState + abilityEngine (S110-Retro-M3) — ERLEDIGT (S111):**
  `gameState.py` 100 % (+17 Tests) + `abilityEngine.py` 100 % (+9 Tests). Coverage-Gate
  auf **99 %** angehoben (`pyproject.toml fail_under = 99`). Toter Reroll-Code entfernt.

---

## Aus §4d Test-Schuld

- ✅ **Kein Test lädt alle Roster durch (S141-Befund):** erledigt S143 — Loader-Test auf
  `pytest.mark.parametrize` über `sorted(_ROSTER_DIR.glob("*.yaml"))` umgestellt
  (`tests/gameObjects/test_loader.py`), alle 8 Roster werden automatisch mitgeprüft.

---

## Aus §5 ziel7 — S121-UI-Verifikation Findings

- ✅ **F1 — Disruption Fields: Effekt-Semantik korrigiert (S122):**
  Kartentext (`docs/work/wahapedia_necrons/faction_overview.txt:2379`) „add 1 to the Strength
  characteristic of models in that unit" — `data/wh40k_9e/necrons/stratagems.yaml`
  `disruption_fields.modifier.roll_type` war `wound` (+1 auf den Verwundungswurf, nur
  zufällig gleichwertig solange die Toughness-Schwelle nicht kippt), jetzt `strength` (echter
  Stat-Modifier vor der Wound-Tabelle). Totes `effect: {type: buff_stat, ...}`-Feld entfernt
  (bei Stratagems nirgends konsumiert, nur `Ability.effect` wird gelesen — per grep bestätigt).
  Neue reine Funktion `stratagem_strength_bonus()` (`src/gameMechanic/stratagemEngine.py`)
  summiert `roll_type=="strength"`-Einträge aus `active_modifiers`; als dritte Quelle in
  `str_bonus` (`src/uiLayout/_common.py`, vor `wound_threshold()`) verdrahtet, analog
  `buff_stat_bonus()`/`get_active_round_choice_strength_if_charged()`. Kein Doppel-Konsum:
  `_collect_atk_modifiers()`s bestehendes `rt in ("hit","wound")`-Gate lässt `"strength"`
  bereits unberührt.
- ✅ **F2 — Weirdboy-Stab VERIFIZIERT (S121):** App zeigt effektive Stärke S8 — korrekt.
  Wahapedia (`docs/work/wahapedia_orks/units_all.txt:143/147`): Weirdboy S5, Staff „+3" →
  5+3=8; YAML (`units.yaml:262`, `weapons.yaml:250`) konsistent. Kein Handlungsbedarf.
- ✅ **F3 — Natürliche 1 in der Würfel-UI — ERLEDIGT (S122, 2026-07-04):**
  (a) `resolve_save()` (`combat.py`) floort den effektiven Save jetzt analog zu Hit/Wound
  auf 2 (`max(2, …)`) — „Eff. 1+" wird weder gewertet noch angezeigt; (b) `dice_row_html()`
  (`diceCompose.py`) zeichnet den Wert-1-Würfel bei Schwelle ≤ 1 als ✕-Miss innerhalb des
  Erfolgsrahmens. Spec: `docs/spec/dice_display.md` §1 Randfall; Tests:
  `test_dice_row_natural_one_always_shows_miss_marker_even_in_success_frame`,
  `test_save_floored_at_2_armour_path`, `test_save_floored_at_2_invuln_path`.

---

## Aus der Prioritätenliste (S145; migriert S151)

Herkunft: `backlog.md` Prioritätenliste (Stand S145), Ränge 1–4 und 8 — die einzigen bereits
abgeschlossenen Ränge zum Zeitpunkt der Migration (Rang 5–7/9–11/∥ blieben offen, s. neue
`backlog.md`).

- ✅ **Rang 1 — Klan/Dynastie-Entscheid (Frage 3 + Prioritätenliste) — ERLEDIGT (kanonisiert
  S150, `ziel7.md` Stufe C §K1):** blockierte Rang 6–7; Konsens-Entscheid gehört an den
  Session-Anfang.
- ✅ **Rang 2 — on_target-Anker Option A — ERLEDIGT (Code S146):** S143 freigegeben, kleiner
  bestätigter UX-Fix. (UI-Prüfung durch den Stakeholder separat offen, s. `backlog.md` B-008.)
- ✅ **Rang 3 — Vigilus-Warlord-Traits entfernen — ERLEDIGT (S146):** S144 entschieden,
  Datenqualitäts-Schuld.
- ✅ **Rang 4 — FixD Brief 1 (Compute/Render-Trennung) — ERLEDIGT (S150,
  `docs/audit/plans/README.md`):** einziger P1-Plan; entblockt Brief 2+3 und den
  mypy-uiLayout-Abbau (s. `backlog.md` B-001/B-004).
- ✅ **Rang 8 — Stufe-B-Rest: Necron-Roster-UI-Verifikation — ERLEDIGT (S146, alle 7 Schritte
  bestanden, `ziel7.md` Z.76):** hielt das ziel7-Stufengate ehrlich; reine
  Stakeholder-Bildschirmzeit.

---

## Aus §0 Aktuelle Findings (weitere Einträge; migriert S151)

- ✅ **#INV-4b Cluster 3 — ERLEDIGT (Plan 020):** Teil der INV-4b-Vokabular-Cluster-Entscheidungen
  (Refinement 2026-06-20). Cluster 1 (`dakka`/`klaw`/`tesla`) bleibt offen (s. `backlog.md`
  B-012).
- ✅ **#INV-4b Cluster 4/5 — ERLEDIGT (XS-Fix).**
- ✅ **#INV-4b Cluster 6 — ERLEDIGT (Plan 021/024).**
- ✅ **INV-4 Default-Roster — bereits archiviert:** Detailtext lebt oben unter „Aus §0 Aktuelle
  Findings" (Eintrag „INV-4 Default-Roster (`gameState.py`, `loader.py`)"); dieser Punkt ist ein
  reiner Verweis, kein neuer Inhalt (Alt-`backlog.md` Z.131 verwies bereits hierher).
- ✅ **Setup-Leck #2b Direktiv-Lock — ERLEDIGT (2026-06-20):** Bug (Nutzer-Screenshots):
  Protokoll-Direktiven-Buttons + WAAAGH-Status erschienen im Setup und wurden durch den
  First-Player-Toggle (`active` gesetzt) sogar wählbar; der Auto-Block `if not active_id` schrieb
  `round_choice_active_*` schon im Setup. Fix: reiner Helfer `_ability_section_visible(phase_key)`
  (`!= "setup"`) + früher `return` in `armyCard._render_round_choice_ui` **und**
  `_render_once_per_battle_ability_ui`; Regressionstest `test_ability_sections_hidden_in_setup_only`.
  Rest (Direktive ab Bewegungsphase sperren) bleibt offen, s. `backlog.md` B-005.
  *(⚠ Übertragungs-Unklarheit: dies ist einer von 3 im Inventar `S151_backlog_inventar.md`
  abstrakt erwähnten „Fließtext-Erledigt-Vermerken ohne eigene Zeile" — vom Executor anhand des
  Alt-Textes identifiziert, nicht im Inventar selbst namentlich benannt.)*
- ✅ **S93-Engine-Befund — Dynastiebonus (6e Bug 3) erstmals wirksam verdrahtet:** Alle
  Direktiv-Reads lasen bisher nur die runden-zugewiesene Direktive; das 6. (immer-aktive)
  Protokoll (`extra_directive`) + der Dynastie-Affinitäts-Fall (beide Direktiven) wurden ignoriert
  (kosmetisch, nicht wirksam). Gefixt: `_active_directive_effects` aggregiert beide Quellen (alle
  5 Reads). Damit ist auch der Dynastiebonus erstmals wirksam verdrahtet.
  *(⚠ Übertragungs-Unklarheit: zweiter der 3 Fließtext-Fälle, s. o.)*
- ✅ **S98-Befund — Hungry-S/Vengeful-S wirksam gemacht (Plan 025 Steps 2+3):** „Engine ✅" war
  irreführend für `strength_modifier`/`ap_bonus` — kein UI-Konsument las die Werte
  (`_collect_atk_modifiers`/`_collect_def_save_modifiers` fragten nur `hit`/`wound`/`save` ab).
  Hungry-S ist behoben: Plan 025 Step 2 faltet den bedingten +1-S in `str_bonus` (eigener
  `strength_if_charged`-Pfad, nicht der tote `strength`-Modifier). Step 3: der tote `ap_bonus`-Pfad
  ist entfernt — Vengeful-S ist jetzt 9E-D2 `ignore_cover_half_range` (Klasse B/Hybrid, Hinweis an
  der Light-Cover-Checkbox), Vengeful-P ist 9E-D1 `ap_on_unmod_wound_6`.
  *(⚠ Übertragungs-Unklarheit: dritter der 3 Fließtext-Fälle, s. o.)*

---

## Aus §2 Offene Tasks (weitere Einträge; migriert S151)

- ✅ **GO-UI-Design-System — ENTSCHIEDEN (S131, Retro-Maßnahme 5 aus S130 eingelöst):** GO-Karte
  (4 Zustände ruhend/bereit/verwendet/gesperrt, Voll-/Kompaktform, Akkordeon-Fix), Orte-Zuordnung
  über die GO-Klassifikation, Tisch-Wurf-Eingabe-Baustein inkl. Command-Re-Roll-Muster,
  Wortlaut-Konventionen (eine Vokabel-Familie Use/Undo/Confirm) — verbindliche Spec:
  `docs/spec/design_system.md` §6. Klassifikations-Referenz (95 GOs, 3 Achsen):
  `docs/reference/go_klassifikation.md`. Umsetzung lief als 6-Pakete-Roadmap (offene Pakete s.
  `backlog.md` B-013 bis B-017).
- ✅ **GO-UI Paket 3a — ERLEDIGT (S133):** Reaktive Boxen → GO-Karte migriert (Fire
  Overwatch/Cut Them Down/Counter-Offensive als Kompaktkarte, Pass-Button entfällt per §6.1).
- ✅ **GO-UI §6.2 statisches Modell — ERLEDIGT (S134):** reaktiv (on-trigger, Stakeholder-Definition
  S134-Review) ⇒ nur inline; proaktiv ⇒ nur zentrale Liste; Overwatch-Reaktivbox mit ↺ Undo;
  Desperate-Breakout-Doppler behoben. Bestätigter MAJOR (damals): 14 `phase_reactive`-GOs bis
  Paket 4 nirgends aktivierbar (Schuld-Tabelle `design_system.md` §6.2).
- ✅ **GO-UI Paket 4 — ERLEDIGT (S135, Commits `d66755e`/`0aa7dc6`/`96e7997`):** Inline-Anker
  Hit/Wound/Save + Damage/Psychic/Deny-Reroll-Ablösung + Attacken-Feld-Re-Roll — 3 Schuld-GOs
  aktivierbar. Rest: 10 GOs an 3 fehlenden Ereignis-Fenstern → Folge-Split (s. `backlog.md`
  B-014).
- ✅ **B1 (Scroll-Sprung), B5 (First-Player-Block), B6 (Faction-Ability-Wahl), B8 (Redundanter
  Statusbereich) — bereits archiviert:** Detailtexte leben oben unter „Aus §2 Offene Tasks"; diese
  vier Punkte sind reine Verweise, kein neuer Inhalt.
- ✅ **B12b — Header-Suffix „used on ⟨Einheit⟩" verdrahtet — ERLEDIGT (S141, Commit `cdb55e2f`);
  manuelle UI-Verifikation ABGESCHLOSSEN (S148, `docs/handoff/S148_ui_verifikation.md`):**
  Resolver `stratagem_used_elsewhere_unit_name` (`src/uiLayout/_common.py`) + 3
  Zustands-Mapper + Render-Bedingung in `goCard.py`; 9 neue Tests, Vollsuite 1781 grün / 99,15 %.
  Randfall (bewusst offen, spec-konform, S148 verifiziert PASS): Advance-Reroll-/Inline-Spends
  übergeben konstruktionsbedingt kein `unit_key` an `spend_stratagem` → Suffix bleibt dort leer,
  ebenso Fire Overwatch. Optionaler XS-Folge-Task (uid durchreichen) bleibt offen, s. `backlog.md`
  B-027.
- ✅ **BUG — Insane-Bravery-Repro Moralphase — ERLEDIGT (S150, UI-verifiziert):** Root Cause: Der
  Zustand `used` las `target_name` weiterhin **live** aus `unit_for_check` statt aus dem
  gespeicherten Anker (`stratagem_used_elsewhere_unit_name`) — ein Wechsel der Sidebar-Auswahl
  NACH dem Einsatz beschriftete die bereits verwendete Karte still um. Fix in `gameProtocoll.py::_render_stratagem_column`:
  `state == "used"` zeigt jetzt den aufgezeichneten Namen (`recorded_target_name`).
  Regressionstest `test_render_stratagem_column_used_here_shows_recorded_target_not_live_selection`.
  Render-Pfad-Notizen für das Generalkonzept: `docs/handoff/S150_usedon_renderpaths.md`.
- ✅ **Sudden Storm S — B-Hinweis anzeigen (`shoot_during_action`) — ABGEDECKT (S97):** Plan 025
  Step 1 hatte die Direktive datenseitig auf 9E-D2 korrigiert; der Tisch-Hinweis wird vom
  generischen Direktiv-Hinweisblock (Plan 025 Step 2b, `enforcement: table`) mit abgedeckt — nicht
  mehr separat nachzuziehen. **Hinweis:** der 🔲-Glyph an dieser Stelle war im Alt-Backlog stale
  (Inventar-Befund A-020).
- ✅ **Boarding-Actions Bereinigung — ERLEDIGT (S134):** Rapid Reanimation, Shield-Piercer
  Projectors, Flensing Capacitors + `resurrection_protocols_character` sind laut Live-Wahapedia
  Boarding-Actions-only und wurden aus dem YAML entfernt (Stakeholder-Entscheid) — sie kommen wie
  NANOSCARAB VIRUS/MINDSHACKLE SCARABS erst mit ziel7 Stufe C zurück (s. `backlog.md` B-063).
  Nebenbefund gesichert: `phase: any` + `event: after_roll` fehlmatchte jeden Advance-/after_roll-Anker.

---

## Aus §4 Architektur-Schulden (weitere Einträge; migriert S151)

- ✅ **Generic-src (INV-4 DEBT) — bereits archiviert:** Pointer auf denselben Sachverhalt wie
  „INV-4 Default-Roster" oben (Aus §0) — kein neuer Inhalt, Details dort +
  `docs/spec/architecture_invariants.md` INV-4.
- ✅ **Generic-src Vokabular (INV-4b DEBT) — bereits archiviert:** Detailtext lebt oben unter „Aus
  §4 Architektur-Schulden" (Eintrag „Generic-src Vokabular (INV-4b DEBT, S51; …)"); kein neuer
  Inhalt.

---

## Aus §4c Design-System — ERLEDIGT (S116–S118; Doku-Abgleich S120, migriert S151)

Kernbefund (S114): 4 divergente Badge-Implementierungen. Vollständig umgesetzt:
- `docs/spec/design_system.md` angelegt (§0–§5), Farben bleiben in `design_colors.md` (Commit
  `143d848`, S116).
- Schritt 1: `badges.py` (`badge()`/`chip()`) + `symbols.py` (8 Konstanten), 4 Call-Sites
  konsolidiert; Invuln-Block (`diceHtml.py`) bewusst gestrichen statt umgestellt (`143d848`).
- Schritt 2: Glyph-/Chip-Rollout auf die restlichen 10 Produktivdateien (`3915f8c` S117, `29f4f81`
  S118) — Ratchet-Rest auf Null (Details: `design_system.md` §5).
- Stakeholder hat den Wertesatz + Hinweis-Konvention S120 (2026-07-03) final bestätigt;
  Handoff-Dateien (`design-system-proposal.md`, `design-system-consensus.md`) gemäß Lifecycle
  gelöscht.

*(Dieser Abschnitt hatte im Alt-Backlog KEINE ✅-Glyphen — der namentlich im Auftrag S151 genannte
Anlassfall, der einen reinen Glyphen-Scan übersehen hätte.)*

---

## Aus §5 ziel7-Cluster P17–P21 und Stufe A Task 0–2 (migriert S151)

- ✅ **P17 — ERLEDIGT (S115):** Mechanik steht+getestet — Pre-Apply-Zielauswahl
  (`_render_subgroup_selector`, `_common.py`) + Wounded-Lock (`apply_damage`/`get_locked_group`,
  `unitMutations.py`); Vor-Auswahl+Lock akzeptiert, ±-Zähler verworfen. Details:
  `docs/goals/archive/ziel6.md` P17.
- ✅ **P18 — ERLEDIGT (bereits S43, `e6fcdb3` Plan 013; Checkbox war stale-offen, verifiziert
  S117):** einheitlicher Deklarations-Flow (`render_group_cards`/`render_group_assignment`,
  synthetische Einzelgruppe für Einheiten ohne `model_groups`) + `melee_with`-Ziel-Anzeige.
  Getestet: `test_group_flow.py`.
- ✅ **P19 — once_per_battle pro Spieler — ERLEDIGT (2026-07-03, Commit `1f9d82b`):** eingesetzte
  once_per_battle-Gefechtsoption blockte zuvor BEIDE Spieler (Bug — 9E: Einschränkung gilt je
  Spieler) + UI zeigte nicht, welcher Spieler sie eingesetzt hat. Vollsuite 1405 passed / 99,11 %,
  UI-Verifikation vom Stakeholder bestätigt. Quelle: `ui-pass-S118.md` S113-Punkt 3.
- ✅ **P20 — Rapid Fire halbe Reichweite — ERLEDIGT (2026-07-03, Commit `dfebd27`):** Attackenzahl
  ist jetzt angebbar, wenn Modelle Ziele innerhalb halber Reichweite wählen; gecappt auf die
  Attackenzahl bei voller Reichweite (z. B. 10 bei 10 Warriors mit Gauss Flayer). Vollsuite 1405
  passed / 99,11 %, UI-Verifikation vom Stakeholder bestätigt. Quelle: `ui-pass-S118.md` S116-Punkt 4.
- ✅ **P21 — BUG: Stratagem-Undo überlebt Phasenwechsel — ERLEDIGT (2026-07-03, Commit
  `dde16f3`):** ↺-Undo-Button wurde nach Phasenwechsel/im nächsten Zug noch angeboten — jetzt nur
  im selben Phasenfenster verfügbar. Widersprach dem S113-Blocker-B1-Codebefund („laut Code NICHT
  angeboten") — Live-Verhalten vs. Code-Analyse abgeglichen, Root Cause gefixt. Vollsuite 1405
  passed / 99,11 %, UI-Verifikation vom Stakeholder bestätigt. Quelle: `ui-pass-S118.md` S113-Punkt 5.
- ✅ **Stratagem-Doppelanzeige — ERLEDIGT (Stufe A Task 1, Commit `8c124c3`):** Zwei-Spalten-Split
  (`first_player`/`second_player`) + `stratagem_usable_by_player()`, je Spieler eigene Liste (kein
  `_shared`-Konkat mehr).
- ✅ **Stratagem-Attributions-Bug — ERLEDIGT (Stufe A Task 1, Commit `8c124c3`):** Die Spalte
  selbst ist der spending player — keine Ableitung aus `s.player` mehr nötig.
- ✅ **`used_stratagem_ids` (phase-scoped) global statt per Spieler-Slot — ERLEDIGT (Stufe A
  Task 2, Commit `396fdec`):** Dict-Form pro Spieler, analog `cp`/`used_stratagem_battle_ids`.
  Umsetzung: `docs/handoff/plan-ziel7-restruktur.md` Stufe A Task 0 (`f9279fe`, YAML-Drift
  Counter-Offensive/Insane Bravery → `both`), Task 1 (`8c124c3`), Task 2 (`396fdec`). Handoff-Datei
  nach Abschluss gelöscht (S121), Struktur+Kandidatenliste in `docs/goals/ziel7.md` §0 überführt.
- ✅ **Ziel7 Stufe A — Findings F1–F3 — bereits archiviert:** Detailtext lebt oben unter „Aus §5
  ziel7 — S121-UI-Verifikation Findings"; dieser Punkt ist ein reiner Verweis (Alt-`backlog.md`
  Z.770–771 verwies bereits hierher). Einzig F4 blieb offen (s. `backlog.md` B-087).

---

## Aus §3 Manuelle UI-Verifikation — abgeschlossene Checkliste (migriert S151)

Vollständige Historie der abgehakten (`- [x]`) Prüfpunkte aus dem Alt-Backlog §3. Der einzige
offene Punkt (Ziel7 Stufe C-Vorbereitung, Emergency Disembarkation) ist NICHT hier — er bleibt
in `backlog.md` als B-074.

- ✅ **WAAAGH Boss-Nob:** 4 Attacken auf Power Klaw, Wound-Block S 11 — verifiziert.
- ✅ **Cover Option B:** Dense im HIT-, Light/Heavy im SAVE-Block, je Tab — verifiziert.
- ✅ **Veil aus Nahkampf:** kein „IN MELEE" danach; Undo stellt wieder her — verifiziert.
- ✅ **Skorpekh-Roster:** 2× Threshers + 1× Reap-Blade getrennt (S146 verifiziert,
  Stakeholder-Verifikation 2026-07-14).
- ✅ **S48 H1–H7** (Big Mek Wargear, Silent King Waffen, Living Metal, MWBD 2×, Badge-Farben, RP)
  — für MWBD 2× Roster `necrons_b1_verification.yaml` (2× Overlord) genutzt.
- ✅ **S147 B1-Fix — verifiziert (S148):** Ziel = Flayed Ones → „Shadows of Drazak" NUR an
  Ziel-Kachel, nicht im HIT-Block; Ziel = Annihilation Barge → „Quantum Deflection" NUR an
  Ziel-Kachel, nicht im SAVE-Block (Roster `necrons_b1_verification.yaml`, Flayed Ones auf 10
  Modelle korrigiert).
- ✅ **S147 MWBD-Fix — verifiziert (S148):** beide Overlords nacheinander auswählen/aktivieren →
  unabhängige Activate-Buttons + Ziel-Auswahl, keine gegenseitige Sperre.
- ✅ **B12b (S141, Commit `cdb55e2f`) — verifiziert S150:** zentrale Stratagems-Liste zeigte „used
  on ⟨Einheit⟩" für die aktuell gewählte statt der angewendeten Einheit — Root Cause + Fix s. oben
  (BUG Insane-Bravery-Repro); UI-Verifikation vom Stakeholder BESTÄTIGT (S150).
- ✅ **B12b (S141) — verifiziert (S148):** Charge-Phase Fire Overwatch — Suffix bleibt leer (kein
  `unit_key` übergeben, spec-konformer Randfall).
- ✅ **B12b (S141) — verifiziert (S148):** Movement Advance-Reroll zeigt **keinen** Suffix (kein
  `unit_key` übergeben — spec-konformer Randfall).

---

## Ziel-Historie (aus index.md überführt S151)

`docs/goals/index.md` wurde S151 gelöscht (Inhalte hierher + nach `backlog.md` überführt).
Vollständige Detailplanungen je Ziel: [archive/](archive/) (Ziel 1A–6, erledigt/archiviert) sowie
`ziel7.md`–`ziel9.md` (Ziel 7 aktiv, 8/9 geplant — s. `backlog.md` Kopf).

| Ziel | Status |
|------|--------|
| Ziel 1A — uiLayout/ Struktursplit | ✅ fertig (archiviert) |
| Ziel 1B — gameObjects/ Foundation | ✅ fertig (archiviert) |
| Ziel 2 — Command Phase | ✅ fertig (archiviert) |
| Ziel 3 — Combat Foundation | ✅ fertig (archiviert) |
| Ziel A — Architektur-Review | ✅ fertig (archiviert) |
| Ziel 4a — Badges & Einheitenzustand | ✅ fertig (archiviert) |
| Ziel 4b — armyCard + unitCard Redesign | ✅ fertig (archiviert) |
| Ziel 4c — Ability Engine Refactoring | ✅ fertig (archiviert) |
| Ziel 4d — Befehlsphase vollständig | ✅ fertig (archiviert) |
| Ziel 4e — Bewegungsphase vollständig | ✅ fertig (archiviert) |
| Ziel 4f — Psychic Phase | ✅ fertig (archiviert) |
| Ziel 4f.1 — Psychic Phase Nachbesserungen | ✅ fertig (archiviert) |
| Ziel 4g — Angriffsphase (Charge Phase) | ✅ fertig (archiviert) |
| Ziel 4h — Moralphase | ✅ fertig (archiviert) |
| Ziel 5 — Setup & Datenlage | ✅ fertig (2026-06-03, archiviert) |
| Ziel 5a — Datenstruktur & Spec | ✅ fertig (archiviert) |
| Ziel 5b — Necrons Katalog | ✅ fertig (archiviert) |
| Ziel 5c — Loader-Refactoring | ✅ fertig (archiviert) |
| Ziel 5d — BattleScribe Importer | ✅ fertig (archiviert) |
| Ziel 5e — Setup-Screen Redesign | ✅ fertig (archiviert) |
| Ziel 5f — Stratagems PoC | ✅ fertig (2026-06-03, archiviert) |
| Ziel 5g — Regelkonformer Setup-Flow | ✅ fertig (archiviert) |
| Ziel 5h — Orks-Katalog | ✅ fertig (archiviert) |
| Ziel 5i — Abschluss: Offene Punkte | ✅ fertig (2026-06-03, archiviert) |
| Ziel 5j — FW Necrons + Ork Datenqualität | ✅ fertig (2026-06-03, archiviert) |
| Ziel 6 — UI-Overhaul, ArmyCard, Attackensequenz | ✅ erreicht (S119, 2026-07-03) |
