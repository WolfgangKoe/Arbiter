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
  `necrons_quantum_shielding.yaml` (S158 umbenannt) mit 2× Overlord).
- ✅ **B1 aus S146-Review — Doppel-Rendering on_target-GOs — ERLEDIGT (S147):**
  Stakeholder-Entscheid: Ziel-Kachel einziger Ort; Hit-/Save-Anker für on_target-GOs
  entfernt (`_common.py`), 2 Positiv- + 2 Negativ-Tests (B2), `design_system.md` §6.2/6.3
  nachgezogen. Manuelle UI-Verifikation offen (§3, Roster `necrons_quantum_shielding.yaml`
  (S158 umbenannt)).

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
  — für MWBD 2× Roster `necrons_quantum_shielding.yaml` (S158 umbenannt) (2× Overlord) genutzt.
- ✅ **S147 B1-Fix — verifiziert (S148):** Ziel = Flayed Ones → „Shadows of Drazak" NUR an
  Ziel-Kachel, nicht im HIT-Block; Ziel = Annihilation Barge → „Quantum Deflection" NUR an
  Ziel-Kachel, nicht im SAVE-Block (Roster `necrons_quantum_shielding.yaml` (S158 umbenannt),
  Flayed Ones auf 10 Modelle korrigiert).
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

---

## Aus der ID-indizierten Liste (migriert S156)

- ✅ **B-056 — Quantum Shielding fester Invuln-Wert — ERLEDIGT (S156, UI-verifiziert):**
  Zwei gleichnamige Mechaniken sauber getrennt umgesetzt: (1) Stratagem „Quantum Shielding"
  gibt einen temporären **festen** 4+ Invuln (neuer Mechanik-Typ „Invuln auf festen Wert
  setzen", kein additiver Modifier); (2) die Fahrzeug-Fähigkeit „Quantum Shielding" war
  bereits seit S135 als permanenter 5+ Invuln korrekt verdrahtet (`ability_invuln_save()`,
  `combine=min`) — neu hinzugekommen ist der zweite Teil der Fähigkeit: „unmod. Wound 1–3 =
  Attacke schlägt automatisch fehl" als neuer generischer Effekttyp `wound_auto_fail`
  (`unit_wound_auto_fail_max`, Ability-`id` bewusst `quantum_shielding_wound_deny` statt
  `..._wound_auto_fail`, um den INV-4b-Vokabular-Scanner nicht auf „fail" als Necron-Token
  zu ziehen — dokumentiert in `docs/spec/rules_insights.md`). Regeltext deckt sich wörtlich
  mit `wahapedia_necrons/units_all.txt:112`. **Stakeholder-UI-Verifikation S156** (Schuss-/
  Kampfphase-Resolution-Tab gegen QS-Fahrzeuge): „funktioniert wie erwartet" — WOUND-Block
  zeigt korrekt 3× ✕ gegen QS-Fahrzeuge, keine Marker gegen normale Ziele
  (`docs/handoff/S155_ui_verifikationen.md` Punkt 5). Drei UI-Folge-Befunde aus derselben
  Verifikation wurden als eigene Items gesichert: B-103 (Debuff-Label „Auto-fail" statt
  Keyword), B-104 (Würfelsymbol-Design-System-Abweichung), B-105 (fehlende GO-Referenz
  „Quantum Deflection" am Wound-Wurf). DoD-Review GO (`docs/handoff/S156_close_review.md`).

## Aus der ID-indizierten Liste (migriert S157)

- ✅ **B-098 — Boss Nob 7b Kombi-Waffenprofile, Teil 2 — ERLEDIGT (S157):** Rest-Scope
  (−1-Hit-Malus-Verdrahtung in `src/gameMechanic/combat.py` + Profil-Auswahl-UI in
  `src/uiLayout/_common.py`, Checkbox statt Selectbox bei `combi`-geflaggten Profilen)
  geliefert. `docs/spec/acceptance/rules.md` R-COMBAT-35 von `status: offen` auf
  `status: implementiert` gehoben, 5 Tests referenziert. Nebenfund: latenter
  `p.name`-Bug im Ranged-Profil-Zweig (`_common.py`) auf `p.name_en` korrigiert; das
  Melee-Pendant desselben Bugs ist latent (kein aktueller Crash-Pfad) und als eigenes
  Item B-110 dokumentiert. DoD-Review GO (`docs/handoff/S157_review.md`).
- ✅ **B-103 — Wound-Debuff-Label zeigt Keyword statt „Auto-fail" — ERLEDIGT (S157):**
  Label kommt jetzt generisch aus `badge_label` in `unit_abilities.yaml`
  (`quantum_shielding_wound_deny` trägt `badge_label: Quantum Shielding`) statt dem
  hartcodierten Fallback-Textbaustein „Auto-fail"; HTML-Output-Test verifiziert das
  Keyword in der gerenderten Wound-Zeile. Härtung des Fallback-Pfads (verpflichtendes
  YAML-Feld + Loader-Guard) bewusst als eigenes Folge-Item B-109 ausgelagert. Ein
  UI-Folgebefund derselben Session (Badge-Truncation in der Wound-Zeile) wurde als
  eigenes Item B-111 gesichert. DoD-Review GO (`docs/handoff/S157_review.md`).

## Aus der ID-indizierten Liste (migriert S158)

- ✅ **B-028a — Reactive-Ability-Infrastruktur — ERLEDIGT (S158):** Reines Plumbing,
  additiv, keine Pflicht-Callsite geändert (App bleibt unverändert lauffähig).
  `reactive_abilities_for()`/`ability_usable_by_player()`/`ability_visibility()`/
  `ability_undo_visible()` neu in `src/gameObjects/ability.py` (Ability-Pendants zu
  `gameObjects/stratagem.py`s Stratagem-Helfern — eigene Kopien statt Adapter, da
  `Trigger` verschachtelt statt flach und `Ability` kein `cp_cost` kennt, S157-Grundannahmen
  1+2). `spend_ability()`/`undo_ability()`/`ability_use_anchor()`/`ability_used_here()`/
  `ability_used_elsewhere_unit_name()`/`render_reactive_ability_box()` neu in
  `src/uiLayout/_common.py`, mit eigenen Session-State-Schlüsseln
  (`used_ability_ids`/`ability_use_anchors`, S157-Grundannahme 3) — die Stratagem-Schlüssel
  und `spend_stratagem()`/`undo_stratagem()` bleiben unangetastet. Durchstich-Testfall: der
  bestehende `heal`-Dispatch (`abilityEngine._execute_heal`) läuft unverändert über den
  neuen `spend_ability()`-Pfad. Kein Konsument verdrahtet (`grep -rn` bestätigt 0
  Nicht-Test-Aufrufer) — der erste reale Call-Site folgt in B-028b. 39+25 neue Tests
  (`tests/gameObjects/test_ability.py`, `tests/uiLayout/test_common.py`), Coverage
  `gameObjects/ability.py` 100 %. Gates: Vollsuite grün bis auf eine Vorbefund-Kollision
  (siehe unten), Architektur-/Doku-Gate grün, mypy-Fehlerzahl unverändert (siehe Befund).
  **Zwei Befunde für die Session-Review (nicht Teil des B-028a-Scopes, nicht selbst
  behoben):** (1) mypy-Baseline in `tools/mypy_gate.py` (`BASELINE = 24`) ist bereits vor
  dieser Änderung stale — ein sauberer HEAD-Checkout (Commit `9a62f13`, Cache geleert)
  misst 25 Fehler, nicht 24; mit den B-028a-Dateien unverändert bleibt die Zahl bei 25 (0
  neue Fehler durch B-028a). Baseline-Korrektur ist ein eigener Schritt, keiner der
  hier committeten Dateien gehört. (2) `tests/docs/test_backlog_structure.py::
  test_backlog_status_column_uses_known_vocabulary` schlägt parallel fehl wegen einer
  ungültigen Statuszeile `B-104: 'Erledigt (S158)'` in `backlog.md` — stammt aus einem
  zeitgleich in derselben Arbeitskopie laufenden Executor-Auftrag (Design-Crew
  B-104/105/111), nicht aus B-028a; nicht selbst korrigiert, da außerhalb des eigenen
  Scopes und im selben Moment von einem anderen Prozess bearbeitet.

## Aus der ID-indizierten Liste (migriert S159)

- ✅ **B-111 — Quantum Shielding Badge Truncation in der Wound Zeile — ERLEDIGT (S158,
  UI-verifiziert S159, Variante C):** Truncation bleibt bestehen, `_badge_chip`
  (`src/uiLayout/diceCompose.py`) trägt seither das volle Label im `title`-Attribut
  (Hover-Tooltip) — Stakeholder-Entscheid Option 1 legte den Regressionstest bewusst auf
  sichtbaren Inhalt statt auf die volle Breite fest. `design_system.md` §1.1 um den
  Tooltip-Baustein ergänzt. Stakeholder-UI-Verifikation S159: Testfall 1 „Verifiziert"
  (`docs/handoff/S158_B111_ui_verifikation.md`, im selben Abschluss gelöscht). DoD-Review GO
  (`docs/handoff/S159_review.md`).
- ✅ **B-112 — Mypy Ratchet Baseline stale — ERLEDIGT (S159):** Baseline in
  `tools/mypy_gate.py` von 24 auf 25 angehoben, um den seit vor S158 stale gewordenen
  Ist-Stand wieder abzudecken (`python tools/mypy_gate.py` → 25 errors == baseline 25).
  **Schuld-Vermerk (Review-Auflage, nicht als „behoben" verschwinden lassen):** die
  Baseline-Anhebung 24→25 dokumentiert nur die vor S158 entstandene Drift — die 25 realen
  mypy-Fehler bleiben als sichtbare Schuld bestehen, das Ratchet-Ziel ist weiterhin, sie zu
  senken (nicht die Baseline dauerhaft oben zu halten). DoD-Review GO
  (`docs/handoff/S159_review.md`, Auffälligkeit-Abschnitt).

## Aus der ID-indizierten Liste (migriert S160)

- ✅ **B-104 — Würfelergebnis-Symbole folgen nicht dem Design System — ERLEDIGT (S160):**
  Re-Fix als echtes Würfel-SVG gemäß `docs/spec/design_system.md` §4.2/§4.3: `dice_face_svg`/
  `miss_die_html` bekommen einen optionalen Farbparameter (`miss_color`), `_marker_row_html`-
  Auto-fail-Zweig rendert die SVG-Miss-Variante mit Perspektivfarbe statt Text-✕; Auto-fail +
  Reroll auf SVG umgestellt. Betroffene Dateien: `src/uiLayout/diceCompose.py`, `tests/uiLayout/
  test_dice_html.py`. Stakeholder visuell bestätigt (S160). DoD-Review GO.

## Aus der ID-indizierten Liste (migriert S162)

- ✅ **B-105 — Wound-Wurf zeigt keine Referenz auf GO „Quantum Deflection" — ERLEDIGT (S162
  DONE — Strength-Chip + Invuln-Funktion vom Stakeholder bestätigt; Invuln-Layout-Kritik an
  B-115 übergeben):** Generischer GO-Quellen-Chip `go_source_chip(label, color)`
  (`src/uiLayout/diceCompose.py`) rewired den bestehenden Strength-Buff-Chip in
  `_render_dice_wound_block` (S161) und liefert seit dem S161-Folge-Task auch das
  Invuln-Save-Label: `_stratagem_invuln_best()` + `compute_resolution_context()`
  (`src/uiLayout/_common.py`) ermitteln Wert **und** Quellenname (Stratagem-`source` bzw.
  `ability_badge_label()`), durchgereicht an `_render_dice_save_block` als
  `invuln_source_label`. Stakeholder-UI-Verifikation S161 (`S161_B105_ui_verifikation.md`):
  Strength-Chip „sieht gut aus" — bestätigt. Folge-Verifikation
  (`S161_B105wiring_ui_verifikation.md`): Punkt 1 (Stratagem-Name erscheint neben `Inv N+`)
  bestätigt; Punkt 2 (Fähigkeits-Invuln-Label-Fall) mangels passendem Testroster nicht
  verifiziert — bleibt offen für eine kombinierte Verifikationsrunde mit B-115. Die
  Layout-Kritik am Invuln-Block (kein horizontal zentriertes, konsistentes Layout, Umbruch bei
  langen GO-Namen) ist keine neue B-105-Anforderung, sondern die bereits in
  `design_system.md` §4.4 katalogisierte Lücke — Kritik wörtlich nach B-115 übertragen
  (`backlog_details.md`). Belege: `docs/handoff/S155_ui_verifikationen.md` Punkt 5,
  `docs/handoff/S156_close_review.md` DoD-Punkt 6c, Commit `2a05447` (S161-Abschluss).
  Herkunft: Stakeholder-UI-Verifikation S156.
- ✅ **B-109 — Auto-Fail-Badge-Label verpflichtend aus YAML — ERLEDIGT (S162 DONE —
  Loader-Guard + Label-aus-YAML, unit-getestet; für aktuelle Datenlage visuell nicht
  unterscheidbar, keine UI-Prüfung nötig):** `always_fail_marker_row_html`s hartcodierter
  Fallback `label or "Auto-fail"` entfernt; jeder `wound_auto_fail`-Effekt bezieht sein
  Badge-Label jetzt verpflichtend über `unit_wound_auto_fail_label()`
  (`src/gameMechanic/abilityEngine.py`, liest `badge_label or name_en`) aus der YAML. Neuer
  Loader-Guard lehnt `wound_auto_fail`-Effekte ohne `badge_label` UND `name_en` ab, statt
  still zu fallbacken. Regressionstest
  `test_load_unit_abilities_still_loads_quantum_shielding_with_its_badge_label`
  (`tests/gameObjects/test_loader.py:1846-1878`) bestätigt: der einzige existierende Effekt
  (`quantum_shielding_wound_deny`, `data/wh40k_9e/necrons/unit_abilities.yaml:922`) hatte
  bereits vorher `badge_label: Quantum Shielding` gesetzt — der Fallback-Pfad wurde nie
  ausgelöst, die Änderung ist für die aktuelle Datenlage visuell nicht unterscheidbar. Reine
  Loader-Absicherung, kein Render-Pfad betroffen → keine manuelle UI-Prüfung nötig, kein
  eigenes AWAITING-VERIFICATION-Handoff angelegt. Commit `2a05447` (S161-Abschluss). Herkunft:
  Stakeholder-Auftrag S157 (Leitstand), Folge von B-103-Umsetzung S156.
- ✅ **B-043 — Invuln-SAVE-Badge-Bereich chaotisch — S162 überholt** (beschriebener Zustand —
  „Inv 4+"/„active"/„AP-Cover N/A" als drei separate Teile — existiert im Code nicht mehr;
  durch die S115-Invuln-Neufassung bereits gelöst, Rest-Layout-Anspruch durch B-115
  abgedeckt): Die ursprüngliche Beschreibung (Herkunft §2 Alt-`backlog.md` Z.346, S78) stammte
  aus einem älteren Code-Zustand vor der S115-Invuln-Neufassung. Code-Prüfung S162:
  `_render_dice_save_block` (`src/uiLayout/diceHtml.py:248-260`) zeigt heute nur noch
  `Inv N+` (+ optionaler `go_source_chip` seit S161) — kein „active"-Text, kein
  „AP/Cover N/A" mehr vorhanden. Die verbleibende, aktuelle Layout-Kritik am Invuln-Block ist
  bereits vollständig in B-115 (Wurf-Block-Pattern-Übertragung) erfasst — kein separates
  Nachfolge-Item nötig. Die Abhängigkeit „überschneidet Plan 017" bleibt für B-034 relevant,
  nicht für einen eigenen Nachfolger von B-043.
- ✅ **B-115 — Invuln-Sektion folgt Wurf-Block-Pattern — S162 DONE — Invuln-Block auf
  WOUND-Block-Muster umgestellt (Titel-Zeile `Inv N+` + Quellen-Chip oberhalb, Würfelreihe
  vollbreit); beide Label-Fälle (Stratagem Quantum Deflection 4+, Fähigkeit WAAAGH! S1 5+) vom
  Stakeholder sichtbestätigt (S162_B115_ui_verifikation.md); Tests:
  test_render_dice_save_block_invuln_follows_wound_block_header_pattern +
  _no_bonus_has_no_chip_and_bare_threshold:** Betroffene Datei: `src/uiLayout/diceHtml.py`,
  Invuln-Zweig in `_render_dice_save_block` (ehem. Z. 248–260). Statt einem einzigen
  `grid_row_html(inv_label, ...)`-Aufruf jetzt zwei `st.markdown`-Calls — erst die Titel-Zeile
  (`Inv N+` + optionaler `go_source_chip`), dann `grid_row_html("", threshold_header_html(...) +
  dice_row_html(...))` — 1:1 das Muster von `_render_dice_wound_block`. Verhalten unverändert:
  kein Bonus-Invuln aktiv → kein Chip, Threshold wie bisher; `invuln_source_label`-Wiring aus
  S161 (B-105-Folge) unangetastet. Stakeholder-Vorgabe (S161/S162, wörtliches Zitat): „Ich würde
  die Angabe des Inv. Saves oberhalb der Würfel-Reihe anzeigen, wie es bei den anderen Abschnitt
  (HIt, Wound,..) ist. Dann hat die Badge links neben den Würfeln Platz, sollte trunced sein und
  dann ist alles konsistent." Manuelle Verifikation deckte beide Quellen-Pfade ab: Fall (a)
  Stratagem-Invuln (Roster `necrons_quantum_shielding.yaml`, Annihilation Barge, Stratagem
  „Quantum Deflection" 4+) und Fall (b) Fähigkeits-Invuln (Roster `orks.yaml`, Boyz unter
  Waaagh!-Fähigkeit „WAAAGH! S1" 5+, offener Punkt aus B-105wiring Checkpunkt 2) — beide vom
  Stakeholder mit „Sieht gut so aus." bestätigt. Vollsuite grün (1991 passed, Coverage 99.13 %),
  Architektur-Gate unverändert, keine Fraktions-Strings/-Checks ergänzt (INV-4b geprüft). Belege:
  `docs/spec/design_system.md` §4.4; `docs/handoff/S161_B105wiring_ui_verifikation.md` Zeile 61
  (Layout-Kritik + Screenshot `Bildschirmfoto vom 2026-07-17 21-26-55.png`, beide gelöscht);
  `docs/handoff/S162_planning.md` Punkt 3; `docs/handoff/S162_B115_ui_verifikation.md`
  (Verifikationsprotokoll, gelöscht nach DONE). Herkunft: Würfelsymbol-Katalog-Freigabe S159
  (`design_system.md` §4.4); Layout-Kritik übernommen aus Stakeholder-UI-Verifikation S161/S162
  (B-105wiring-Folge).

## Aus der ID-indizierten Liste (migriert S164)

- ✅ **B-028b — Deny Psychic Konsolidierung — ERLEDIGT (S164 DONE — UI-Verifikation positiv,
  `docs/handoff/S163_B028b_ui_verifikation.md`, Datei nach Abschluss gelöscht):** Betroffene
  Dateien: `src/uiLayout/_common.py`, `src/gameMechanic/psychicPhase.py`,
  `data/wh40k_9e/necrons/unit_abilities.yaml`, `data/wh40k_9e/necrons/wargear.yaml`,
  `src/gameObjects/loader.py`. Erste komplette GO-Card-Migration: `noctilith_beacons`
  (`the_silent_king`, `deny_psychic`-Effekt) als erste unit-eigene Ability über die
  B-028a-Infrastruktur gerendert — additiv, nicht gatend (erscheint neben dem bestehenden
  Deny-the-Witch-Wurf-UI, blockiert dieses aber nicht; PSYKER-Pfad unverändert). `can_deny()`
  generisch um Ability-Quellen erweitert (S160: nur Wargear `gloom_prism` +
  `noctilith_beacons` über `find_unit_ability_by_effect`). **S163-Nachtrag (gloom_prism-Rest):**
  `gloom_prism` vom alten Wargear-Namens-Gate (`load_deny_wargear_names`, Match gegen
  `unit.rules`) auf einen echten `unit_ability`-Eintrag migriert —
  `wh40k_9e.necrons.unit.canoptek_spyder.gloom_prism` in `unit_abilities.yaml`,
  `conditions: [has_rules: [gloom_prism]]` (Muster wie die bestehende
  `fabricator_claw_array`-Ability derselben Einheit — Gloom Prism ist laut Wahapedia
  optionales Wargear, anders als Noctilith's bedingungslose Ownership). `wargear.yaml`-Eintrag
  auf reine Katalog-Beschreibung reduziert (kein `effect`-Block mehr, analog
  `fabricator_claw_array`). `can_deny()` dadurch vereinfacht: nur noch PSYKER-Keyword ODER
  `find_unit_ability_by_effect` — der Wargear-Namens-Pfad ist für keine Fraktion mehr aktiv,
  `load_deny_wargear_names` bleibt als dokumentierte, generische Fallback-Infra in `loader.py`
  bestehen (bewusste Scope-Entscheidung, kein größerer Umbau — Folge-Item B-121 prüft die
  Löschkandidatur). Neue reaktive GO-Karte für Canoptek Spyder löst B-119 Fall b mit (D-1
  Entscheidung Variante A, Stakeholder-Freigabe S163) — kein separater Chip. UI-Verifikation
  S160 (`docs/handoff/S160_B104_ui_verifikation.md`, B-028b-Teil): Testfall 1 (Karte erscheint
  im Deny-Column), Testfall 2 (Use/Undo-Zyklus, Vollrückgängig-Garantie), Testfall 3
  (Regression bestehender Deny-Pfade) — alle positiv. UI-Verifikation S164
  (`S163_B028b_ui_verifikation.md`): Gloom-Prism-Karte erscheint additiv in der Deny-Spalte für
  Canoptek Spyder, Roll-UI unverändert — vom Stakeholder mit „positiv" bestätigt. Belege:
  `docs/handoff/S158_planning.md` (Aufgabe Z.17, Tabelle Z.49–57);
  `docs/handoff/S159_B028b_ui_verifikation.md` (Testfälle 1–3); `docs/handoff/S159_review.md`
  DoD-Punkt 6; `docs/handoff/S163_PLANNING.md` (T2 + D-1). Herkunft: B-028-Zuschnitt S158, Teil
  der „deny_psychic"-Konsolidierung (zwei bestehende Teil-Pfade über B-028a vereinheitlicht).
- ✅ **B-119 — Deny Quellen Anzeige gameActionsArea — ERLEDIGT (S164 — fachlich gelöst via
  B-028b, S163; UI-Sichtprüfung positiv im selben Handoff wie B-028b):** Betroffene Datei:
  `src/gameMechanic/psychicPhase.py::_render_deny_column` (S162-Korrektur — vorherige Referenz
  `src/uiLayout/gameActionsArea.py` war falsch, per `grep -rn "def _render_deny_column" src/`
  verifiziert: die Funktion liegt in `psychicPhase.py:469`, `gameActionsArea.py` enthält keinen
  Deny-Code). Bei einem Deny-the-Witch-Wurf zeigte die gameActionsArea-Spalte nur den
  Roll-Input ohne Angabe der Deny-Quelle. Zwei Fälle: **(a) Silent King Noctilith Beacons
  (GO-Karte, B-028b):** eindeutig über die GO-Karte sichtbar — gelöst seit S160. **(b) Canoptek
  Spyder Gloom Prism:** war auf dem Wargear-Pfad ohne GO-Karte, seit S163 (B-028b-Rest)
  ebenfalls über eine reaktive GO-Karte gerendert (`_render_deny_ability_cards`, identisches
  Muster wie Fall a) — die ausführende Einheit ist damit sichtbar, **ohne** zusätzlichen
  Chip/Hinweistext (D-1 Entscheidung Variante A, Stakeholder-Freigabe S163: „ein einheitlicher
  Rendering-Pfad für alle Deny-Quellen ist DRY und deckt sich mit dem Noctilith-Muster" — ein
  separater Chip hätte doppelt gerendert). Fall b damit über B-028b mitgelöst, kein eigener
  Code-Beitrag von B-119 nötig. Regressionstests:
  `tests/gameMechanic/test_psychic_phase.py::TestGloomPrismAbilityMigration` (Ability-Daten,
  die die Karte speist) + `test_can_deny_via_gloom_prism_ability_without_wargear_rules_tag`
  (Migration vollständig, kein Wargear-Namens-Pfad mehr nötig). Belege: Stakeholder-Kommentar
  S160 zu B-028b Testfall 3 (`docs/handoff/S160_B104_ui_verifikation.md`,
  B-028b-Testfall-3-Notiz); `docs/handoff/S163_PLANNING.md` D-1 (Entscheidung Variante A);
  `docs/handoff/S163_B028b_ui_verifikation.md` (gemeinsame UI-Sichtprüfung mit B-028b).
  Herkunft: Stakeholder-Beobachtung S160 (B-028b UI-Verifikation Testfall 3,
  Gloom-Prism-Regression).

## Aus der ID-indizierten Liste (migriert S166)

- ✅ **B-122 — Menhir-Lebenspunkte verifizieren — ERLEDIGT (S166, extern verifiziert + positive
  UI-Sichtprüfung):** `data/wh40k_9e/necrons/units.yaml:1106` trug `wounds: 7` je Menhir-Modell
  (Silent King, 2 Menhirs → 14 Wunden gesamt + Szarekh 16 = 30 gesamt). Stakeholder-Angabe (S165):
  5 Wunden je Menhir → 10 gesamt (26 gesamt inkl. Szarekh 16). Der lokale Wahapedia-Dump
  (`docs/work/wahapedia_necrons/units_all.txt`) enthält nur Szarekhs eigene Statszeile
  (`W:9-16`), keine separate Menhir-Profilzeile — bestätigte Scraper-Lücke. Extern verifiziert
  (WebSearch/WebFetch, drei unabhängige Quellen — Wahapedia
  `wahapedia.ru/wh40k9ed/factions/necrons/The-Silent-King`,
  `40k.app/factions/necrons/units/the-silent-king`,
  `twinnedminiatures.blogspot.com/p/9th-edition-necrons-silent-king.html` — konvergieren auf
  Wounds=5 je Triarchal Menhir; andere abgeleitete Stat-Werte der Fetches widersprachen sich
  untereinander und wurden verworfen, nur der übereinstimmende Wounds-Wert übernommen).
  `units.yaml:1106` auf `wounds: 5` korrigiert (nur der Wounds-Wert, `ws`/`bs`/`attacks`
  unverändert gelassen — außerhalb des B-122-Scopes). Erklärkommentar in Zeile 1099 (W7→W5)
  mitgezogen. Ein direkt betroffener Test
  (`tests/uiLayout/test_group_flow.py::test_front_group_hp_menhirs_then_szarekh`) pinnte den
  alten Wert (14/7/9-Fixture-Zahlen) und wurde auf die neuen Werte (10/5/7) nachgezogen —
  erwarteter Rot→Grün-Fix, kein Verhaltensbruch. Kein Code-Pfad hängt an der Zahl (reine
  Datenkorrektur). Manuelle Stakeholder-UI-Sichtprüfung S166 bestätigt positiv — dieser
  Stakeholder-Befund selbst legte den Grundstein für B-123 (Root Cause). Belege:
  Stakeholder-Entscheid S165 (Explodes-Einordnung); `docs/handoff/S166_B122_VERIFIKATION.md`
  (gelöscht nach Abschluss, Inhalt hier archiviert). Herkunft: Stakeholder-Ergänzung im
  S165-Explodes-Entscheid.

## Aus der ID-indizierten Liste (weitere Einträge; migriert S155)

- ✅ **B-060 — CLAUDE.md Token-Disziplin entschlacken — ERLEDIGT (S155):** `session_context.py`-Implementierungsdetails (Transcript-Pfad, Regex-Fallstrick S65) aus dem Token-Disziplin-Abschnitt nach `operating_model.md` Event 6 verlagert; in CLAUDE.md nur 2-Zeilen-Verweis. Commit `6ca8ef8`.
- ✅ **B-027 — B12 optionaler XS Task unit key durch spend stratagem — ERLEDIGT (S155):** `unit_key`/uid wird jetzt durch `spend_stratagem` bei Advance-Reroll und Fire Overwatch durchgereicht, damit der „used on ⟨Einheit⟩"-Suffix korrekt gesetzt wird. Commit `316240f`; UI-Verifikation offen → docs/handoff/S155_ui_verifikationen.md Punkt 2+3.
- ✅ **B-087 — F4 Stufe A Verifikationspunkte 3+4 — ERLEDIGT (S155, Fix committet):** Counter-Offensive/Fire-Overwatch Regel-Konformität verifiziert — Box erscheint korrekt erst NACH gegnerischem Fight (Trigger-Timing regelkonform), Hinweistext zur Verfügbarkeit ergänzt. Hypothesis A bestätigt (Triggermechanik korrekt, kein Code-Fix nötig). UI-Konsistenz-Punkt (Box ausgrauen statt ausblenden) wird mit B-031 gelöst. Commit `ab36b80`; UI-Verifikation offen → docs/handoff/S155_ui_verifikationen.md Punkt 1.

---

## Aus der ID-indizierten Liste (migriert ab S152)

- ✅ **B-002 — Klan/Dynastie K1 Wortlaut-Fix Nihilakh+Mephrit — ERLEDIGT (S152):**
  `data/wh40k_9e/necrons/subfaction_abilities.yaml` — die 2 fachlich falschen Einträge
  (Nihilakh + Mephrit) sind korrigiert; Entscheid war bereits S150 kanonisiert
  (`docs/goals/ziel7.md` §K1 Stufe C), reiner Daten-Fix ohne Code-Abhängigkeit. Commit folgt
  am Session-Ende.
- ✅ **B-099 — Backlog-Feinschliff (Stakeholder-Auflagen S151) — ERLEDIGT (S151/S152):**
  Fünf Stakeholder-Auflagen eingelöst — (1) sechs Stale-Verdachtskandidaten ersatzlos aus
  Liste+Details gelöscht (B-099a, S151); (2) Beschreibungsspalte trägt Typ farbig+fett per
  `<span style>` nach `<br>`, Blocker bei Status `Blocked` als dritte `<br>`-Zeile; (3)
  ID-Spalte verbreitert (non-breaking-space-Padding), ID bleibt einzeilig; (4) Effort auf
  Token-Schätzung umgestellt (~5k/~15k/~35k/~70k+ statt XS/S/M/L), Ist-Verbrauch bleibt in
  `docs/metrics/overview.md`; (5) Details-Template neu geordnet (Typ/Status/Tier/Effort/
  Detail-Beschreibung/Abhängigkeiten/Belege/Benötigte Regeln-Scopes/Herkunft) mit
  bidirektionalen Backlinks (B-099b, S152). Format s. `backlog.md` Legende +
  `backlog_details.md` Feldschema; Wächter `tests/docs/test_backlog_structure.py`.
- ✅ **B-008 — on_target-Anker Option A UI-Prüfung — ERLEDIGT (S152):** Stakeholder-UI-
  Verifikation positiv („Passt alles"). Ziel-Kachel (`render_group_assignment` in
  `src/uiLayout/_common.py`) ist der einzige Ort für `on_target`-GOs, keine Dopplung in
  Hit-/Wound-/Save-Tabs. Code seit S146/S147, Prüfung S152 abgeschlossen.
- ✅ **B-074 — Ziel7 Stufe C Vorbereitung Emergency Disembarkation — ERLEDIGT (S152):**
  Stakeholder-UI-Verifikation am Ork-Transport-Roster (`data/rosters/orks_transport.yaml`)
  positiv — Emergency-Disembarkation-Box erscheint zuverlässig beim TRANSPORT-Tod, richtige
  Spieler-Spalte, korrekte CP-Buchung.
- ✅ **B-039 — Tote Produktionsfunktion `build_aura_range_hint_text` entfernen —
  ERLEDIGT (bereits S139 entfernt, stale seit dem; archiviert S154 auf
  Stakeholder-Entscheid):** Einziger Produktions-Konsument
  (`armyCard._render_aura_range_hint`, Conquering-Tyrant-Aura-Hinweis) wurde bereits S138/S139
  entfernt — der Backlog-Eintrag blieb als Leiche stehen, 0 Treffer für den Funktionsnamen
  in `src/`/`tests/`.
- ✅ **B-061 — Backlog-§0-Hygiene — ERLEDIGT (strukturell durch B-007-Restrukturierung
  erledigt; archiviert S154 auf Stakeholder-Entscheid):** §0 als Abschnitt existiert seit der
  ID-indizierten Restrukturierung (B-007, S151) nicht mehr — der Auftrag „erledigte
  ✅-Einträge aus §0 auslagern" ist durch die neue Struktur strukturell hinfällig.
- ✅ **B-082 — Executor-Auftrags-Checkliste härten — ERLEDIGT (bereits erfüllt durch
  `agent_scopes.md`-Selbstprüf-Checkliste + Selbst-Stopp-Klausel, Commit `1861d9d`;
  archiviert S154 auf Stakeholder-Entscheid):** Die geforderten Härtungen — `ruff`/
  pre-commit vor „grün"-Claim, Token-/Zeit-Budget-Cap gegen Rabbit-Holes — sind in
  `docs/reference/agent_scopes.md` bereits verankert (§„Selbstprüf-Checkliste (Pflicht vor
  Rückgabe)" + „Selbst-Stopp-Klausel in jedem Brief").
- ✅ **B-036 — Battle Log nach Reset alte Einträge — ARCHIVIERT (S155, Duplikat des
  S129-Fixes, Stakeholder-Entscheid S154):** Bug „nach Reset zeigt das Battle-Log noch alte
  Einträge" war bereits durch den S129-Fix behoben; die Backlog-Zeile blieb als Duplikat
  stehen (ursprünglich Teil von Plan 018). Umsetzung scheiterte 2× an API-529 (reine
  Ausführungspanne), in S155 nachgeholt.
- ✅ **B-053 — Daten-Altlast `gretchin_mob` — gelöscht in S155, 8E-Relikt ohne
  Referenzen:** Eintrag `wh40k_9e.orks.unit.gretchin.gretchin_mob` in
  `data/wh40k_9e/orks/unit_abilities.yaml` war ein 8E-Relikt („must take a Morale test if it
  suffers any casualties" ohne 9E-Bedingung) mit 0 Referenzen außerhalb der eigenen
  Definition (grep über `data/`, `src/`, `tests/`, `docs/`) — die 9E-Mechanik wird bereits
  durch die benachbarte `cowardly`-Ability abgedeckt. Ersatzlos gelöscht;
  `pytest tests/gameObjects/ --no-cov -q` grün (321 passed) danach.
- ✅ **B-079 — DRY ±1-Cap-Helper (`diceHtml.py`) — stale, bereits erledigt in S118
  (`29f4f81c`), festgestellt S155:** Der geforderte gemeinsame Helper existiert bereits als
  `_capped_modifier_threshold` in `src/uiLayout/diceHtml.py` (3 Aufrufstellen: Hit-Block,
  Wound-Block) samt Tests in `tests/uiLayout/test_dice_html.py`
  (`test_capped_modifier_threshold_*`) seit Commit `29f4f81c` („Close S118: … dice cap DRY
  helper"). Backlog-Eintrag blieb als Leiche stehen — nichts mehr zu tun.

## B-028 — B12 Feature Wunsch (S158: Zuschnitt in B-028a–c5 überführt)

[↩ Archiv-Anmerkung] Dieser Abschnitt enthält die S156/S157-Herleitung des B-028-Items. Der fachliche Zuschnitt wurde S158 in die neuen Items B-028a, B-028b, B-028c1–c5 überführt; die kritischen Grundannahmen 1–3 und die Ist-Zustand-Tabelle sind in den jeweiligen Detail-Abschnitten integriert. Dieser Abschnitt dient historischen Nachschlags-Zwecken.

---

## B-028 — B12 Feature Wunsch used on Suffix auf alle GOs

[↩ Zeile in backlog.md](backlog.md#b-028)

**Typ:** <span style="color:#166534">**Fachlichkeit (Ziel 7)**</span>

**Status:** ToDo

**Tier:** Executor

**Effort:** ~35k

**Detail-Beschreibung:** „used on ⟨Einheit⟩"-Suffix soll auf **alle** reaktiven GOs ausgeweitet werden (aktuell nur die zentrale Stratagems-Liste betroffen). **S150-Renderpfad-Kartierung** (`docs/handoff/S150_usedon_renderpaths.md`, gelöscht S156 — Inhalt hier verlustfrei übernommen): alle drei bestehenden Render-Pfade (zentrale Stratagem-Liste `gameProtocoll.py:350`, Advance-Reroll-Karte `movementPhase.py:325`, reaktive Stratagem-Boxen `_common.py:868` mit sechs Aufrufern in `fightPhase.py`/`chargePhase.py`/`movementPhase.py`/`psychicPhase.py`(×2)/`_common.py`) teilen exakt dieselbe Datenquellen-Kette `render_go_card(locked_reason=...) ← _go_state_and_reason()/_reactive_go_state()/_advance_reroll_state() ← stratagem_used_elsewhere_unit_name(faction, strat.id) ← stratagem_use_anchor() ← session_state["stratagem_use_anchors"]`, geschrieben von `spend_stratagem()` — keine separaten Code-Pfade, nur eine Datenquelle mit drei Call-Sites. **S156-Planner-Befund (Vorab-Zählung, M1-Pflicht):** `render_reactive_stratagem_box` ist laut Code (lädt nur `stratagems.yaml`) ausschließlich auf Stratagems zugeschnitten. Es gibt **11 reaktive Non-Stratagem-GOs** (`timing: phase_reactive`), die aktuell **nirgends** über einen Reactive-GO-Card-Pfad gerendert werden — `grep -rn "phase_reactive" src/` findet nur zwei Konsumenten, beide ausschließlich für Stratagems. Die 11 IDs (aus `docs/handoff/S156_planning.md`, Datei gelöscht S156 nach ANSWERED):

| Datei | Anzahl | IDs |
|---|---|---|
| `data/wh40k_9e/necrons/unit_abilities.yaml` | 8 | `the_silent_king.noctilith_beacons`, `the_silent_king.vengeance_of_the_enchained`, `warriors.their_number_is_legion`, `canoptek_plasmacyte.infused_madness`, `hexmark_destroyer.inescapable_death`, `gauss_pylon.arc_fields`, `seraptek_heavy_construct.wrath_of_the_seraptek`, `triarch_stalker.targeting_relay` |
| `data/wh40k_9e/necrons/faction_abilities.yaml` | 1 | `reanimation_protocols` |
| `data/wh40k_9e/necrons/wargear.yaml` | 1 | `gloom_prism` |
| `data/wh40k_9e/orks/subfaction_abilities.yaml` | 1 | `klan.freebooterz.competitive_streak` |

**Konsequenz:** B-028 ist damit nicht nur „Suffix auf bestehende Boxen ausweiten", sondern setzt voraus, dass diese 11 Fähigkeiten überhaupt erst als reaktive GO-Card gerendert werden — eine größere Vorstufe als der Backlog-Eintrag ursprünglich suggerierte. **Stakeholder-Entscheid S156:** Option A — S156/S157 liefert zunächst nur ein Scope-/Konzeptdokument (Ist-Zustand der 11 Fähigkeiten dokumentieren, Aufwand neu schätzen), direkte Umsetzung folgt als eigener, danach geplanter Schritt (S157).

**Abhängigkeiten:** Nach dem BUG-Fix (Archiv A-019, Insane-Bravery-Repro Moralphase). Scope-Dokument (Option A) für S157 geplant (Stakeholder-Entscheid S156).

**Belege:** `docs/handoff/S156_planning.md` (Vorab-Zählung, Tabelle oben — Datei gelöscht nach Übernahme).

**Benötigte Regeln-Scopes:** —

**Herkunft:** §2 Alt-`backlog.md` Z.284–286 (Stakeholder-Wunsch S148); Renderpfad-Kartierung S150; Scope-Befund + Stakeholder-Entscheid S156.

### Ergebnis — Scope-Dokument Option A (S157)

**Korrektur zum Plan:** `docs/handoff/S157_planning.md` nennt die dritte Datenquellen-Kette als
`src/uiLayout/movementPhase.py:325` — diese Datei existiert nicht unter `uiLayout/`. Der tatsächliche
Pfad ist `src/gameMechanic/movementPhase.py:326` (`_render_advance_reroll_card`, Aufruf von
`render_go_card`). Verifiziert per `find`/`grep`, kein Blocker, nur Pfad-Korrektur für die Belege
unten.

#### Grundannahmen (zur Bestätigung vor Option B)

1. **Timing-Vertrag ist strukturell ähnlich, aber nicht identisch.** Beide Modelle kennen
   `phase_reactive`, aber bei `Stratagem` liegen `timing`/`phase`/`event`/`player` als flache
   Felder (`gameObjects/stratagem.py:66-67`), bei `Ability` liegen dieselben Informationen
   verschachtelt in `Trigger` (`gameObjects/ability.py:8-15`: `trigger.timing`, `trigger.phase`,
   `trigger.event`, `trigger.player`). Ein generischer Filter (analog `reactive_stratagems_for()`)
   braucht entweder eine zweite, Ability-spezifische Funktion oder eine Adapter-Schicht — kein
   Ein-Zeilen-Wiederverwenden.
2. **Abilities sind CP-frei, Karten dürfen das nicht falsch darstellen.** `Ability` hat kein
   `cp_cost`-Feld. `render_go_card()` selbst ist bereits generisch (Name, `cp_cost`, `state`,
   Callbacks — kennt weder `Stratagem` noch `Ability`), kann also mit `cp_cost=0` fest aufgerufen
   werden. Das CP-Gate in `stratagem_visibility()` entfällt für Abilities ersatzlos (nicht
   nachbilden).
3. **Usage-/Anchor-Bookkeeping existiert für Abilities nicht und wird nicht „mitbenutzt".**
   `spend_stratagem()`/`undo_stratagem()` (`_common.py:439-551`) sind auf den Typ `Stratagem`
   getippt und lesen `strat.cp_cost`, `strat.once_per_battle`, `strat.modifier` — Felder, die
   `Ability` nicht hat. Empfehlung (kein Fait accompli, zur Bestätigung): **eigene, schlanke
   `spend_ability()`/`undo_ability()`** mit eigenen Session-State-Schlüsseln
   (`used_ability_ids`/`ability_use_anchors`), keine Wiederverwendung der Stratagem-Schlüssel und
   kein Umbau von `spend_stratagem()` auf einen gemeinsamen Protocol-Typ — zweite Wiederholung
   eines kleinen Musters unterschreitet die projekteigene DRY-Schwelle „ab der dritten
   Wiederholung" (CLAUDE.md „Clean Code").
4. **Reanimation Protocols bleibt bewusst außerhalb des GO-Card-Umbaus.** Von den 11 GOs hat
   `reanimation_protocols` (`faction_abilities.yaml`) bereits eine funktionierende, aber
   card-fremde UI (`_render_rp_block`, `_common.py:1448-1508`: Markdown-Zusammenfassung +
   `number_input` + zwei Buttons, gespeist über `get_after_attack_revive_ability()` +
   `revive_dice_count()`). Annahme: Option B migriert **nur die übrigen 10** GOs auf
   `render_go_card`; `reanimation_protocols` bleibt bei seiner bestehenden UI, weil eine Migration
   hier reine Form-Änderung ohne Fachlichkeitsgewinn wäre (die Dice-Count-Eingabe passt nicht in
   das Use/Undo-Schema einer GO-Karte ohne Funktionsverlust).
5. **Effekt-Ausführung ist Teil von Option B, nicht nur das Rendering.** Von den verbleibenden 10
   Effekt-Typen ist heute **keiner** über `abilityEngine._EFFECT_HANDLERS` ausführbar (einziger
   Dispatch-Eintrag ist `"heal"`, `abilityEngine.py:82-84`) und für `deny_psychic`, `mortal_wounds`,
   `reroll_rp`, `free_attack`, `mark_target`, `buff_roll` existiert **keine** Ausführungslogik
   außerhalb der beiden bereits erwähnten Sonderpfade (s. Ist-Zustand-Tabelle). Annahme: Option B
   umfasst sowohl Kartenanzeige **als auch** die fachliche Umsetzung der Effekte — eine
   Rendering-only-Variante (Karte erscheint, Effekt bleibt manuelle Tischnotiz) wäre ein deutlich
   kleinerer, alternativer Zuschnitt und müsste explizit gewählt werden.
6. **Neue Ereignis-Auslöser haben keine generischen Hooks.** `model_destroyed`,
   `enemy_falls_back`, `enemy_melee_attack`, `after_unit_fights`, `after_unit_shoots`,
   `friendly_unit_destroys_enemy` (die sechs `event`-Werte der 10 GOs, s. Tabelle) existieren im
   App-Code an keiner Stelle als automatisch erkannte Ereignisse. Annahme: wie bei den bestehenden
   reaktiven Stratagem-Boxen bestätigt der Spieler das Eintreten manuell (ein Button/Trigger an der
   passenden Phasen-Stelle), keine automatische Ereigniserkennung.

#### Ist-Zustand je der 11 GOs (verifiziert gegen YAML + `grep -rn` über `src/`)

| ID (gekürzt) | Datei | `trigger.phase` / `event` | `effect.type` | Heute im UI? |
|---|---|---|---|---|
| `the_silent_king.noctilith_beacons` | `necrons/unit_abilities.yaml:349` | psychic / `opponent_psychic_phase` | `deny_psychic` | **Nein** — `can_deny()` (`psychicPhase.py:51-62`) prüft nur PSYKER-Keyword + `load_deny_wargear_names()` (nur `wargear.yaml`); diese unit-eigene Ability wird nicht erfasst, selbst wenn Szarekh kein PSYKER ist. |
| `the_silent_king.vengeance_of_the_enchained` | `necrons/unit_abilities.yaml:385` | any / `model_destroyed` | `mortal_wounds` | **Nein.** Kein Dispatch, keine Karte. |
| `warriors.their_number_is_legion` | `necrons/unit_abilities.yaml:408` | shooting+fight / `reanimation_roll` | `reroll_rp` | **Nein** — RP läuft im Code als aggregierte Würfelzahl (`_render_rp_block`, kein Einzelwurf), ein „Reroll von Einsen" ist mit dieser Datenrepräsentation gar nicht abbildbar (Class-B-Kandidat, s. Aufwandsschätzung). |
| `canoptek_plasmacyte.infused_madness` | `necrons/unit_abilities.yaml:488` | any / `model_destroyed` | `mortal_wounds` | **Nein.** |
| `hexmark_destroyer.inescapable_death` | `necrons/unit_abilities.yaml:510` | movement / `enemy_falls_back` | `free_attack` | **Nein** — bräuchte eine vollständige Attacke-Sequenz mitten in der Movement-Phase des Gegners. |
| `gauss_pylon.arc_fields` | `necrons/unit_abilities.yaml:763` | fight / `enemy_melee_attack` | `mortal_wounds` | **Nein.** |
| `seraptek_heavy_construct.wrath_of_the_seraptek` | `necrons/unit_abilities.yaml:784` | fight / `after_unit_fights` | `mortal_wounds` | **Nein.** |
| `triarch_stalker.targeting_relay` | `necrons/unit_abilities.yaml:884` | shooting / `after_unit_shoots` | `mark_target` | **Nein** — bräuchte zustandsbehaftetes „Ziel markiert" über Einheiten-/Phasengrenzen hinweg. |
| `reanimation_protocols` (Faction) | `necrons/faction_abilities.yaml:28` | shooting+fight / `after_enemy_attack` | `reanimate` | **Teilweise** — Effekt vollständig implementiert und im Spiel aktiv genutzt (`get_after_attack_revive_ability()`, `_render_rp_block`), aber **nicht** als GO-Card, sondern eigene Custom-UI (s. Grundannahme 4). Kein „Nachbau", nur Konsolidierung. |
| `gloom_prism` (Wargear) | `necrons/wargear.yaml:78` | psychic / **kein `event`-Feld** | `deny_psychic` | **Teilweise** — `can_deny()` erfasst diesen Wargear-Effekt generisch über `load_deny_wargear_names()`, aber wieder nicht als eigene GO-Card mit Use/Undo, sondern als reines Ja/Nein-Gate im bestehenden Deny-Flow. Auffällig: als einzige der 11 Abilities fehlt hier das `event`-Feld im Trigger — kleine Schema-Inkonsistenz gegenüber den übrigen 10 (Beleg für Grundannahme 1: das Ability-Trigger-Schema ist weniger streng befüllt als das Stratagem-Pendant). |
| `klan.freebooterz.competitive_streak` | `orks/subfaction_abilities.yaml:132` | any / `friendly_unit_destroys_enemy` | `buff_roll` | **Nein** — `buff_roll` als String kommt zwar in `commandPhase.py:391`/`gameState.py:37` vor, das ist aber eine andere (round-choice-basierte) Ability, kein Bezug zu `competitive_streak`. |

**Konsolidierter Befund:** von 11 GOs haben 2 (`reanimation_protocols`, `gloom_prism`) bereits einen
funktionierenden, aber card-fremden Teil-Pfad; 9 haben **keinerlei** UI- oder Ausführungs-Spur im
Code. Die S156-Aussage „nirgends über einen Reactive-GO-Card-Pfad gerendert" ist für alle 11 korrekt
(kein einziges nutzt `render_go_card`), verdeckt aber, dass 2 der 11 fachlich bereits vollständig
funktionieren — nur eben nicht im GO-Card-Format.

#### Renderer-Konzept

**`render_go_card()` selbst ist bereits generisch** (`_common.py:1052`, Parameter: `key, name,
cp_cost, state, keywords, rule_text, compact, locked_reason, target_name, expanded_content, on_use,
on_undo` — keine Stratagem-/Ability-Typbindung). Der fehlende Teil ist die Schicht **davor**: die
drei bestehenden Aufrufer (`_render_stratagems` in `gameProtocoll.py:336-379`,
`render_reactive_stratagem_box` in `_common.py:750-884`, `_render_advance_reroll_card` in
`gameMechanic/movementPhase.py:282-337`) berechnen `state`/`locked_reason`/`target_name` alle aus
Stratagem-spezifischen Helfern (`stratagem_visibility`, `stratagem_conditions_met`,
`_weapon_conditions_met_for_unit`, `stratagem_used_here`, `stratagem_used_elsewhere_unit_name`).

Vorgeschlagene Signatur eines neuen `render_reactive_ability_box()` (Name in Anlehnung an
`render_reactive_stratagem_box`, wohnt ebenfalls in `_common.py`):

```python
def render_reactive_ability_box(
    faction: str,
    phase: str,
    event: str,
    *,
    unit_for_conditions: Unit | None,
    decline_key: str,
    on_resolved: Callable[[], None] | None = None,
) -> None:
```

Bewusst **kein** `effect_type`/`effect_stat`-Filterpaar wie beim Stratagem-Original (dort dient es
dazu, aus einer gemeinsamen Kandidatenliste die eine passende Stratagem-Instanz für genau diesen
Call-Site herauszufiltern) — bei nur 11 GOs über vier verschiedene Loader kann der Aufrufer die
passende Ability direkt per `id` oder `unit_id` referenzieren, ein generischer Typ-Filter lohnt sich
hier noch nicht (YAGNI, gegebenenfalls in einer zweiten Iteration nachziehen, falls die Anzahl
wächst).

**Was wiederverwendbar ist:**
- `render_go_card()` — vollständig, unverändert.
- Das **Muster** der drei Aufrufer (Kandidaten sammeln → Sichtbarkeit prüfen → State/Reason
  mappen → `render_go_card` aufrufen) — als Vorlage, nicht als Code (andere Feldnamen, andere
  Loader).
- `go_card_container_style()`/`go_card_html()` (CSS/HTML-Bausteine unter `render_go_card`) —
  vollständig, kennen nur `GoCardState`, keine Quelltyp-Bindung.

**Was neu gebaut werden muss:**
- `reactive_abilities_for(abilities, phase, event)` — Pendant zu `reactive_stratagems_for()`
  (`gameObjects/stratagem.py:198-218`), liest aber `ability.trigger.timing/.phase/.event` statt
  der flachen Stratagem-Felder. Gehört fachlich neben `Ability` (z. B. `gameObjects/ability.py`
  oder ein neues `gameObjects/abilityVisibility.py`, analog zur Trennung `stratagem.py` vs.
  `_common.py`).
- Eine Ability-Sichtbarkeits-Funktion (kein CP-Zweig, sonst analog `stratagem_visibility()`):
  conditions_met (bereits vorhanden: `check_conditions()`, `abilityEngine.py:49-66`) + reactive-
  Gate + noch-nicht-benutzt-Gate.
- `spend_ability()`/`undo_ability()` mit eigenen Session-State-Schlüsseln (Grundannahme 3).
- Vier Loader-Aufrufe statt einem (`load_unit_abilities`, `load_faction_abilities`,
  `load_wargear_abilities`, `load_subfaction_abilities`) — der Aufrufer muss wissen, aus welcher
  YAML-Quelle seine jeweilige Ability stammt (keine kombinierte „alle Abilities einer Faction"-
  Funktion existiert bisher).
- Sechs Effekt-Ausführungen (`deny_psychic` als eigenständiger — nicht nur Wargear-Gate — Pfad,
  `mortal_wounds` ×4 GOs, `reroll_rp`, `free_attack`, `mark_target`, `buff_roll`) — jede mit eigener
  Fachlogik, drei davon (`free_attack`, `mark_target`, `reroll_rp`) mit nicht-trivialer
  Zustandshaltung über Phasen-/Einheitengrenzen hinweg.
- 9 neue Call-Sites (die 9 GOs ohne bestehenden Teil-Pfad) in `movementPhase.py`, `fightPhase.py`,
  `psychicPhase.py`, ggf. `shootingPhase.py` — analog zu den sechs bestehenden Stratagem-Call-Sites,
  aber in anderen/zusätzlichen Phasen-Dateien.

#### Aufwandsschätzung Option B (neu)

Die bisherige Backlog-Schätzung (~35k, Zeile „Effort" oben) war für „Suffix auf bestehende Boxen
ausweiten" kalkuliert — nach diesem Scope-Befund ist der tatsächliche Umfang „Ability-seitige
Reactive-GO-Infrastruktur komplett neu bauen + 6 bislang nirgends implementierte Effekt-Typen
fachlich umsetzen". Das sprengt den M-Rahmen (Executor-Brief-Obergrenze) deutlich — **Split-Vorschlag
in drei Schritte**, jeder für sich innerhalb M:

| Teil | Inhalt | Schätzung |
|---|---|---|
| **B-028a — Infrastruktur** | `reactive_abilities_for()`, Ability-Sichtbarkeitsfunktion, `spend_ability()`/`undo_ability()` + Session-State-Schlüssel, `render_reactive_ability_box()`. Kein neuer Effekt, nur Plumbing — als Testfall kann ein bereits existierender Dispatch (`heal`) durch den neuen Pfad laufen. | ~30k |
| **B-028b — Die beiden Teil-Pfade konsolidieren** | `reanimation_protocols` bewusst NICHT migrieren (Grundannahme 4); `gloom_prism`/`noctilith_beacons` `deny_psychic` vereinheitlichen — `noctilith_beacons` als erste komplett neue Karte über B-028a rendern, `can_deny()` generisch um Ability-Quellen (nicht nur Wargear) erweitern. Kleinster, am besten abgegrenzter zweiter Schritt. | ~20k |
| **B-028c — Die 8 „mortal_wounds/reroll_rp/free_attack/mark_target/buff_roll"-GOs** | Fachlich heterogenste Gruppe — vier `mortal_wounds`-GOs vermutlich gemeinsam lösbar (ein Effekt-Handler, vier Call-Sites), `reroll_rp`/`free_attack`/`mark_target`/`buff_roll` sind vier verschiedene, jeweils nicht-triviale Mechaniken. **Muss vor Beauftragung noch einmal in der Planung selbst unterteilt werden** (mind. 2 Executor-Briefs) — hier nur als Sammelposten geschätzt, keine belastbare Einzelzahl. | ~50k+ (grobe Sammelschätzung, vor Beauftragung erneut aufteilen) |

**Gesamt (grob):** ~100k+ für volle Option B — mehr als das Doppelte der ursprünglichen ~35k-Schätzung
und deutlich über der Session-typischen Wind-down-Grenze (~120–135k) in einem Stück. Empfehlung:
B-028a und B-028b sind reif für eine Beauftragung (S158), B-028c braucht einen eigenen
Planungsdurchgang, sobald B-028a steht (Sichtbarkeits-/Spend-Infrastruktur muss zuerst existieren,
damit sich die acht heterogenen Effekte sauber daran andocken lassen).

Stakeholder-Entscheidung: Wir gehen Option-B an. Task bitte kleinschneiden und darauf achten, dass die kleineren Tasks in einer Session umsetzbar sind und die App funktioniert. Ich war mir beim Lesen nicht sicher, ob reanimation_protocols nicht fälschlicherweise als GO interpretiert wird. Das ist eine factionAbility, auf die ggf. eine GO oder eine andere GO wirken kann.

**Übernahme des Entscheids (S157):** Option B freigegeben. Auflagen für den Zuschnitt: (a) sessiongroße Tasks (je ≤ M-Effort), (b) die App ist nach jedem Task lauffähig — kein Zwischenzustand mit toter UI. (c) Klassifikations-Klärung vorab: `reanimation_protocols` ist eine **factionAbility**, auf die GOs wirken können — kein GO; der Zuschnitt prüft die 11er-Liste auf diese Fehlklassifikation und nimmt RP ggf. heraus (deckt sich mit der Grundannahme oben, dass die RP-UI nicht migriert wird). Der Zuschnitt (Verfeinerung von B-028a/b/c in Backlog-Items) ist ein **Planner-Auftrag S158**.

## Aus der ID-indizierten Liste (migriert S168)

- ✅ **B-123 — Schadenszuweisungs-Bug Mehrmodell-Einheiten — ERLEDIGT (S168, Core-Fix T2 +
  UI-Nachzug T3, Stakeholder-verifiziert):** Root Cause (S166-Nachdiagnose):
  `_render_damage_block` erzwang für Mehrgruppen-Einheiten mit >1 lebenden Gruppen immer eine
  Subgruppen-Wahl, wodurch `_apply_directed_group_damage` jeden Schaden über den Restpool der
  gewählten Gruppe hinaus verwarf — der spillover-fähige `_apply_group_wound_damage`-Zweig war
  über die UI praktisch unerreichbar (Repro: 26 Schaden auf den vollen Silent King → nur die
  Menhirs (10 HP) sterben, Szarekh 16/16 unberührt). **T2 (Core, S168,
  `src/gameMechanic/unitMutations.py`):** `_apply_directed_group_damage` verwirft Überschuss
  nicht mehr — nach Depletion der gewählten Gruppe läuft der Rest generisch über
  `_apply_group_wound_damage` (Prioritäts-Spill) weiter; `get_locked_group` generalisiert um
  einen Zwangs-Lock von Anfang an für Einheiten mit `unit.has_per_group_wounds()` (Gruppen mit
  unterschiedlichen Pro-Modell-Wundwerten — im gesamten YAML-Bestand ausschließlich der Silent
  King) — Szarekh kann nicht mehr vor den Menhirs gewählt werden (`apply_damage` wirft
  `ValueError` bei Verstoß); homogene Mehrgruppen-Einheiten (z. B. Ork Boyz/Boss Nob) bleiben
  unverändert bei freier Verteidiger-Erstwahl, generisch aus `model_groups`-Daten abgeleitet.
  14 neue Tests (`tests/gameMechanic/test_unit_mutations.py`, Matrix
  directed×resolved×locked×mortal, S166-Regressionstest
  `test_apply_damage_directed_resolved_regression_s166_26_damage`, Grenzfall-Vollzerstörung,
  K1-Einzelattacken-Cap, K3-Freiwahl-Gegenbeispiel). Vollsuite nach T2: 2028 passed, Coverage
  99,18 %, Architektur-Gate 8/8 grün. **T3 (UI, S168, `src/uiLayout/_common.py`
  `_render_subgroup_selector`/`_render_damage_block`):** bildet den neuen Zwangs-Lock ab — für
  gelockte Einheiten (Silent King) kein wählbarer Radio-Button mehr für die geschützte Gruppe,
  stattdessen ein Warnhinweis, der die Pflichtgruppe (Triarchal Menhirs) nennt; nach Depletion
  der Pflichtgruppe verhält sich der Block wie bei einer Einheit mit nur einer aktiven Gruppe.
  **Stakeholder-Verifikation S168** (`docs/handoff/S168_B123_ui_verifikation.md`, gelöscht nach
  Abschluss): Checkpunkt 1 (Regelkonformität Menhir-Lock) bestätigt — „Das Verhalten ist im
  Vergleich zu vorher nun regelkonform." Kritik aus Checkpunkt 2 (Design-System-Spec-Qualität)
  und Checkpunkt 3 (Warnhinweis-Wortlaut/Apply-Damage-Uneinheitlichkeit) wurde NICHT hier
  begraben, sondern als Backlog-Substanz bei B-124 verankert (`backlog_details.md` B-124,
  Herkunft „T3-V S168"). Belege: `docs/handoff/S166_B123_DIAGNOSE.md`/`_NACHDIAGNOSE.md`
  (gelöscht nach Abschluss, Root Cause hier archiviert); Stakeholder-Entscheid S165
  (Explodes-Einordnung). Herkunft: Stakeholder-Ergänzung im S165-Explodes-Entscheid;
  Root-Cause-Verifikation S166; Core-Fix + UI-Nachzug + Verifikation S168.

## Aus der ID-indizierten Liste (migriert S172)

- ✅ **B-028c1 — Explodes-Familie (Destruction-Trigger) — ERLEDIGT (S172, Stakeholder-Abnahme, d + b3 verifiziert):** Pflicht-Trigger-Mechanik + `auto_explode`-GO vollständig verdrahtet. S172: b3 (`auto_explode`-GO für Curse of the Phaeron, TITANIC-differenzierte CP-Kosten, 15 Tests, Vollsuite grün). Verifikations-Set: Testfall 1–7 (S171, design_system.md §7) PASS, Testfall 3 (S172, repair-Karte) PASS. Datenumfang: Necrons vollständig (Command Barge/Triarch Stalker/Spyders/Reanimator + C'tan/Silent King/Tesseract Vault), Orks-Kandidaten separates Refinement-Item B-125/B-126. **Folge-Bugs erkannt + dokumentiert:** Reset-Callback-Seiteneffekt auf bereits zugewiesene Mortal Wounds (B-125), Mortal-Wounds-Cap pro Einheit fehlt im Multi-Panel (B-126).

