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
