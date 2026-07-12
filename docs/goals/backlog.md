# Backlog — zentraler Index

> **Ein Ort für „was ist offen".** Dieser Index führt die bisher verstreuten Quellen
> zusammen (Executor-Pläne, offene Tasks, manuelle Verifikation, Architektur-Schulden).
> **Details bleiben in den verlinkten Artefakten** — hier wird nicht dupliziert, nur verwiesen.
>
> Pflege: Wird ein Punkt erledigt, hier abhaken **und** in der Detailquelle. Neue Arbeit
> entweder als Plan in [../audit/plans/](../audit/plans/) oder als Task-Zeile hier.

Letzter Abgleich: 2026-06-30 (S112 — Coverage-Schuld M3 erledigt (100 %), §5 Ziel7 neu definiert, Ziel6 6e/6f/6h Kat1–3 nach Ziel7 ausgelagert)

---

## 0. Aktuelle Findings (S51 — Badge / Protokoll / Würfel)

Aus manueller UI-Verifikation. Vorgehen phasenweise, je Finding eigener Plan +
Freigabe. Akzeptanzkriterien (testbar) unter [../spec/acceptance/index.md](../spec/acceptance/index.md).

- 🟡 **#PSI Generische Flow-/Reset-Struktur für die Psychic Phase** (S64 Befund, S65 Code
  fertig — **committed** cc75490/1d8b8ba; offen nur noch manuelle UI-Checks): Code + Tests grün
  (Stand jetzt ≥1109 Tests, 93 %; die Zahlen „900/88 %" waren der S65-Stand).
  Reine Helfer `refund_deny`/`cleared_deny` in `psychicPhase.py`; einheitlicher
  `_reset_active_power()` refundiert das Deny-Budget der inaktiven Fraktion (fixt: denied +
  reset = permanent verbranntes Budget); symmetrisches „Undo deny"-Button (`_render_undo_deny_button`);
  „Skip Deny" verbraucht kein Budget; `deny_faction`-Feld in `psi_result`. +8 Tests
  (`TestRefundDeny`/`TestClearedDeny`). Token-Gauge-Hook ist live. **Noch offen:** manuelle UI-Checks (a) „Undo deny"
  nach erfolgreichem Deny; (b) aktiv-Reset → nächste Power denybar; (c) Skip Deny = kein
  Budgetverbrauch; (d) Undo nach fehlgeschlagenem Deny — dann gemeinsamer Commit mit
  Token-Gauge-Hook. Verwandt: `can_deny` via `rules` statt `wargear_ids`+`handler` (Gloom
  Prism als echter Wargear-Choice — eigenständiger Task).
- 🔴 **[PRIO-NÄCHSTE] #2b Direktiv-Lock** (Phase 2, S52 Root-Cause): **Setup-Leck erledigt 2026-06-20.**
  Bug (Nutzer-Screenshots): Protokoll-Direktiven-Buttons + WAAAGH-Status erschienen im Setup
  und wurden durch den First-Player-Toggle (`active` gesetzt) sogar wählbar; der Auto-Block
  `if not active_id` schrieb `round_choice_active_*` schon im Setup. **Fix:** reiner Helfer
  `_ability_section_visible(phase_key)` (`!= "setup"`) + früher `return` in
  `armyCard._render_round_choice_ui` **und** `_render_once_per_battle_ability_ui`;
  Regressionstest `test_ability_sections_hidden_in_setup_only`. Render-Code → manuelle
  Verifikation steht (s. u.). **Offen (Rest #2b, nächste größere Aufgabe):** Direktive ab Bewegungsphase sperren.
- 🟡 **#2 Protokoll-Buff-Audit** (Phase 3): **Engine-Wiring erledigt (Plan 024,
  S86/S87)** — alle 12 Direktiv-Effekte sind jetzt engine-seitig verdrahtet
  (vorher 3/12); offen bleibt nur noch die **Anzeige** (Badge/Block) je Direktive.
  Spalte „Engine" = liefert die Funktion den Effekt; Spalte „Anzeige" = Render-Code
  (Plan 016/017-Gebiet, manuelle Verifikation):

  | Protokoll · Direktive | Effekt | Engine | Anzeige |
  |---|---|---|---|
  | Eternal Guardian · P | **9E-D1:** `light_cover_if_stationary` (**Klasse A**, nur Shooting-Block; Variante C = Checkbox vorgehakt+disabled bei stationär) | ✅ `get_active_round_choice_light_cover_if_stationary` (Plan 025 Step 4) | ✅ Variante C im SAVE-Block (Plan 025 Step 4) — ✅ in Würfeln sichtbar (Bug 1 Render-Reihenfolge + Bug 2 blau→grün gefixt, S103) |
  | Eternal Guardian · S | **9E-D2:** Hold Steady (Overwatch 5+) / Set to Defend (+1 Hit next Fight) — **eigener Plan, abhängig Plan 015 Overwatch** | ✅ YAML-Übergang `hold_steady_or_set_to_defend` + TODO-Kommentar (Step 4) | 🔲 D2-Plan (nach Plan 015) |
  | Hungry Void · P | **9E-D1:** unmod. Wound-6 → AP +1 (**melee**, `ap_on_unmod_wound_6`, Klasse B) | n/a (Tisch) | ✅ `[AP-1]`-Zeile im WOUND-Block (S97/Plan 025 Step 2) |
  | Hungry Void · S | **9E-D2:** +1 S bei Charge/was-charged/HI (**melee**, `strength_if_charged`, Klasse A) | ✅ (`get_active_round_choice_strength_if_charged`) | ✅ S blau im WOUND-Block (wie WAAAGH; Plan 025 Step 2) |
  | Conquering Tyrant · P | **9E-D1:** +3" Aura-Reichweite (`aura_range_bonus`, **Klasse B**, `enforcement: table`) | n/a (Tisch) | ✅ Tisch-Hinweis (umgesetzt S116, nachgezogen S127) |
  | Conquering Tyrant · S | **9E-D2:** nach Fall Back schießen, −1 Hit (**ranged**, `shoot_after_fall_back`, **Klasse A**) | ✅ `get_active_round_choice_shoot_after_fall_back` (Plan 025 Step 5) | ✅ −1-Hit-Modifier im HIT-Block Shooting (Plan 025 Step 5) |
  | Sudden Storm · P | move_bonus +1 | ✅ | 🔲 Bewegungs-Badge |
  | Sudden Storm · S | advance_and_charge | ✅ (`charge_after_advance_allowed`) | 🔲 Charge-Phase |
  | Undying Legions · P | rp_reroll (one die) | ✅ (`get_active_rp_modifiers`) | ✅ RP-Block-Hint (S89; UI-verifiziert S93) |
  | Undying Legions · S | **heal_bonus** Living Metal +1 (war fälschlich `rp_bonus` „model returned" — S89-Datenfix) | ✅ (`get_active_heal_bonus`) | ✅ Caption (S89; UI-verifiziert S93) |
  | Vengeful Stars · P | **9E-D1:** unmod. Wound-6 → AP +1 (**ranged**, `ap_on_unmod_wound_6`, Klasse B) | n/a (Tisch) | ✅ `[AP-1]`-Zeile im WOUND-Block (Plan 025 Step 3) |
  | Vengeful Stars · S | **9E-D2:** kein Light Cover ≤ halbe Reichweite (**ranged**, `ignore_cover_half_range`, Klasse B/Hybrid) | ✅ (`get_active_round_choice_ignores_cover_half_range` → Hinweis) | ✅ grüne Badge an Light-Cover-Checkbox (Plan 025 Step 3) |

  Buff-Badge grün (`design_colors.md` §3), nur bei betroffenen Einheiten + im
  Phasen-Block (wie MWBD). Anzeige-Rest überschneidet sich mit Plan 016/017.
  **S93-Engine-Befund:** alle Direktiv-Reads lasen bisher nur die runden-zugewiesene Direktive; das **6. (immer-aktive)
  Protokoll** (`extra_directive`) + der **Dynastie-Affinitäts-Fall** (beide Direktiven) wurden ignoriert — kosmetisch, nicht
  wirksam. Gefixt: `_active_directive_effects` aggregiert beide Quellen (alle 5 Reads). Damit ist auch der **Dynastiebonus
  (6e Bug 3) erstmals wirksam** verdrahtet. Offen bleibt nur Eternal Guardian **S** SAVE-Hinweis (Plan 016 Group A).
  **S97-Befund (Nutzer-Screenshots + Scoping) — die Tabelle ist zu optimistisch:**
  - **Reroll-of-1-Save-Hinweis fehlt in der UI** (Eternal Guardian S, Z. „🔲 SAVE-Hinweis"): Soll laut
    Plan 024 = Reroll-Hinweis im SAVE-Block (⟳-Caption wie RP, `_rp_directive_hints`-Muster). Screenshot
    S97 zeigt den SAVE-Block **ohne** diesen Hinweis. Bestätigter Anzeige-Bug, nicht nur „offen".
  - **„Engine ✅" ist irreführend für `strength_modifier`/`ap_bonus`:** Die Engine-Fn liefert den Wert,
    aber **kein UI-Konsument liest ihn** (`_collect_atk_modifiers`/`_collect_def_save_modifiers` fragen
    nur `hit`/`wound`/`save` ab, nicht `strength`/`ap`). Hungry-S/Vengeful-S wirken im Kampf **gar nicht**.
    **S98:** Hungry-S ist behoben — Plan 025 Step 2 faltet den bedingten +1-S in `str_bonus`
    (eigener `strength_if_charged`-Pfad, **nicht** der tote `strength`-Modifier). **S98+ (Step 3):
    der tote `ap_bonus`-Pfad ist entfernt — Vengeful-S ist jetzt 9E-D2 `ignore_cover_half_range`
    (Klasse B/Hybrid, Hinweis an der Light-Cover-Checkbox), Vengeful-P ist 9E-D1 `ap_on_unmod_wound_6`.**
  - **Wurzel-Lösung (Design-Korrektur S98):** Kein generischer Caption-Block mehr — Direktiv-Effekte
    werden ins **Dice-UI** integriert (S blau wie WAAAGH; trigger-bedingt als Würfelzeile mit Symbol,
    `value_triggered_die_row_html`). **Anzeige ist ab S97 Pflichtteil jedes 025-Steps.** Reine
    B-Tisch-Hinweise ohne Würfel-Mechanik (Sudden Storm S) bleiben gesondert offen.
- 🔲 **#3/#4 Würfelanzeige** (Phase 4): Pfeilrichtung/-länge der Modifier-Zeile +
  Badge-Breite (ragt in Würfel „1"). **Badge-Wert bleibt** (`AP-1`/`AP-2`, Stakeholder-
  Entscheid 2026-06-21 — Gewohnheit + Konsistenz zu anderen Profilwerten; Pfeil ist
  bewusst redundant). Labels nur **kürzen** (truncate/ellipsis), nicht den Wert entfernen.
  Soll-Bild als AC in `docs/spec/dice_display.md` festgelegt → Plan 022, dann per AC
  einrasten (Lehre aus Finding 9.2 — nie still ändern).
- ✅ **R-CMD-03 — CP-Grant ohne Battle-forged-Gating — ERLEDIGT (S123-Verifikation):**
  `commandPhase.can_gain_command_point(game_mode)` gated den „Grant +1 CP"-Button bereits
  (`_render_faction_actions` returnt für Open Play früh, zeigt „Open Play — no Battle-forged
  CP grant."). Ledger-Eintrag [../spec/acceptance/rules.md](../spec/acceptance/rules.md) §R-CMD-03
  führt `status: implementiert`, getestet: `test_matched_play_is_battle_forged` /
  `test_open_play_is_not_battle_forged`. Eintrag hier war stale (Fix + Ledger-Update erfolgten,
  ohne diesen Backlog-Punkt zu schließen).
- 🔲 **#INV-4b Cluster-Entscheidungen (Refinement 2026-06-20):** Konsensentscheidungen für INV-4b Vokabular-Schulden:
  - **Cluster 1 — `dakka`/`klaw`/`tesla`**: YAML-gesteuert via `weapon_special`-Schema → Teil von Plan 022 oder eigenständig.
  - **INV-4 Default-Roster** (`game_state.py`, `loader.py`): ✅ **erledigt S128** — die 2
    DEBT-Einträge (hardcodierte `"necrons"`-Defaults) sind aufgelöst: `init_state()`s
    `roster_p1`/`roster_p2` sind Pflichtparameter, `loader.py`s `faction_dir`-Default entfernt
    (klarer `ValueError` statt stillem Necron-Fallback). Allowlist 5 → 3 Einträge (nur noch
    LEGIT-Rest `rosz_importer.py`, nicht 0 — der bleibt dauerhaft). Details:
    [architecture_invariants.md](../spec/architecture_invariants.md) INV-4.
  - _(Cluster 3 ✅ Plan 020, Cluster 4/5 ✅ XS-Fix, Cluster 6 ✅ Plan 021/024 — erledigt, aus Backlog entfernt)_

---

## 1. Aktive Implementierungs-Pläne (Executor-Queue)

Plan-Status & Reihenfolge → [docs/audit/plans/README.md](../audit/plans/README.md) (kanonisch)

---

## 2. Offene Tasks (kleiner als ein Plan)

- ✅ **GO-UI-Design-System — ENTSCHIEDEN (S131, 2026-07-09, Retro-Maßnahme 5 aus S130
  eingelöst):** GO-Karte (4 Zustände ruhend/bereit/verwendet/gesperrt, Voll-/Kompaktform,
  Akkordeon-Fix), Orte-Zuordnung über die GO-Klassifikation, Tisch-Wurf-Eingabe-Baustein
  inkl. Command-Re-Roll-Muster, Wortlaut-Konventionen (eine Vokabel-Familie Use/Undo/
  Confirm) — verbindliche Spec: [../spec/design_system.md](../spec/design_system.md) §6.
  Klassifikations-Referenz (95 GOs, 3 Achsen):
  [../reference/go_klassifikation.md](../reference/go_klassifikation.md). Umsetzung läuft
  als 6-Pakete-Roadmap, **jedes Paket geht einzeln durchs Freigabe-Gate**:
  - 🟢 **Paket 1 (S132):** GO-Karten-Baustein (4 Zustände, Voll/Kompakt, Akkordeon-Fix) +
    zentrale Stratagem-Liste auf den Baustein umstellen.
  - 🟢 **Paket 2 (S132):** Command Re-Roll für Advance/Charge (ohne Wurf-Eingabe-Baustein) —
    löst die Stakeholder-Auflage S130 (s. u.) ein.
  - ✅ **Paket 3a (S133):** Reaktive Boxen → GO-Karte migriert (Fire Overwatch/Cut Them
    Down/Counter-Offensive als Kompaktkarte, Pass-Button entfällt per §6.1).
  - 🟢 **Paket 3b (S134):** `before_battle`-Liste im ArmySetup (macht die 13 bisher nie
    matchenden GOs erstmals sichtbar — löst den S131-Kandidaten „`before_battle` sichtbar
    machen" unten ab).
  - ✅ **§6.2 statisches Modell (S134):** reaktiv (on-trigger, Stakeholder-Definition
    S134-Review) ⇒ nur inline; proaktiv ⇒ nur zentrale Liste; Overwatch-Reaktivbox mit
    ↺ Undo; Desperate-Breakout-Doppler behoben. **Bestätigter MAJOR:** 14
    `phase_reactive`-GOs bis Paket 4 nirgends aktivierbar (Schuld-Tabelle
    `design_system.md` §6.2) — deshalb Paket 4 = S135 Top-Prio.
  - ✅ **Paket 4 (ERLEDIGT S135, Commits `d66755e`/`0aa7dc6`/`96e7997`):** Inline-Anker
    Hit/Wound/Save + Damage/Psychic/Deny-Reroll-Ablösung + Attacken-Feld-Re-Roll —
    3 Schuld-GOs aktivierbar. Rest: 10 GOs an 3 fehlenden Ereignis-Fenstern →
    Folge-Split lt. 4c-Bewertung (`design_system.md` §6.2): generisches `on_destroy`
    (7 GOs) und `on_set_up`+`on_target` — Paket-Nummern bei Einplanung NEU vergeben
    (Kollision mit Paket 5/6 unten vermeiden).
  - 🟢 **Paket 5 (S134+):** Wortlaut-/Sprach-Bereinigung (Englisch durchgehend, Use/Undo/
    Confirm-Familie), eine CP-Anzeige, ein Stepper-Baustein.
  - 🟢 **Paket 6 (S134+, eigenes Konzept-Inkrement):** Einheiten-Auswahl in die
    GameActionArea ziehen (Heroische-Intervention-Muster verallgemeinern), Zielauswahl
    entschlacken.
  - 🔲 **Danach:** manuelle UI-Verifikation (S130-Checkliste + neues Design), Stakeholder.
- ✅ **Command Re-Roll auf alle 9 Wurf-Arten ausweiten — ERLEDIGT (S136, R-CMD-12 9/9):**
  Stakeholder-AUFLAGE (S130) eingelöst: alle 9 regelerlaubten Wurf-Arten sind jetzt
  inline verdrahtet — Damage/Psychic/Deny als GO-Karte (S135 Paket 4b), Anzahl-Attacken
  (S135 Paket 4c), Advance/Charge (S132/S133), Hit-/Wound-/Save-Wurf in
  `_render_resolution_tab` (S136, pragmatischer Familie-2-Ansatz laut Stakeholder-Entscheid
  `S136_4cc_befund.md`). Details + Testnamen: [../spec/acceptance/rules.md](../spec/acceptance/rules.md) R-CMD-12.
- 🟢 **Fraktions-Stratagems `before_battle` sichtbar machen (S131-Kandidat):** 6 Necron- +
  7 Ork-Stratagems matchen nie (`PHASES` kennt kein `before_battle`) — löst über Paket 3
  (S133, s. o.) mit der neuen ArmySetup-Liste; danach §6e-Modifier-Engine für die ~56
  teilintegrierten proaktiven Stratagems (s. Ziel7 §6e).
- 🔲 **„Alt. Fire"-Chip unerklärt (S132-Befund 5, überführt S134):** `src/uiLayout/dice_html.py:70`
  rendert `special_die_html("Alt. Fire")` ohne Erklärtext (anders als „Extra Hits" mit
  „unmod. 6 = +2 Hits"). Vorgehen: Regel-Wortlaut „Alternating Fire" gegen `docs/work/`
  verifizieren (Haiku-Lookup), dann Kurzerklärung analog Extra-Hits ergänzen. Effort XS.
- 🔲 **Stakeholder-Beobachtungen S131 (verlustfrei hierher überführt S134;
  `docs/handoff/Stakeholder_Beobachtungen.md` besteht als STANDING-Eingangskanal weiter —
  nie löschen; referenzierte Screenshots verbleiben in `docs/handoff/`, Löschung erst wenn
  der jeweilige Punkt DONE ist):**
  - ✅ **B1 — Scroll-Sprung bei Command-Protocol-Wahl im Setup — ERLEDIGT (S136,
    Stakeholder-bestätigt):** Ursache Layout-Shift + Chrome Scroll-Anchoring (H1
    Fokus-Autoscroll und H2 Sechsfach-Key-Rewrite beide widerlegt, Playwright-Befund
    `docs/handoff/S136_B1_probe.md`: `activeElement` = `<body>`, Layout-Shift bis 0.92 auf
    `stLayoutWrapper`). Fix: `overflow-anchor: none` auf `section[data-testid="stMain"]`
    (`gameHeader.py` `CSS_THEME`) — Playwright-verifiziert Scroll-Delta 0/0/0 (vorher
    +2348). Verankert in `CLAUDE.md` §Streamlit CSS.
  - **B2 — Spielvorbereitungsscreen überarbeiten:** noch kein Konzept. Vorgehen: Screen-Inventar
    erstellen (Sonnet, read-only), Redundanz-Befunde B5/B7 einarbeiten, Konzept-Handoff mit
    Grundannahmen-Block → Stakeholder-Entscheid → eigener Plan. (Hinweis: der frühere Punkt 3
    „Start-Game-Button-Position" wurde in S133 aus der Beobachtungsdatei entfernt/erledigt.)
    **Entschieden S135:** Struktur = Option C (Option A jetzt, Wizard-Zielbild erst mit B4-
    Datenkarte); Faction-Ability-Wahl (B6) läuft unabhängig vom B2-Konzept (`S134_offene_punkte.md`).
  - **B4-Rest — profileCard als Datenkarte (Setup):** Doppel-Zoll + Profilwert-Reihenfolge in
    S133 gefixt; offen: tabellarische Waffenanzeige + „schöne Datenkarte" nur mit der echten
    Roster-Auswahl (Screenshots `Bildschirmfoto vom 2026-07-09 20-53-48.png` = Ist,
    `…20-58-07.png` = Wahapedia-Anmutung als Inspiration, ausdrücklich NICHT 1:1). Bereitet
    den Armybuilder vor. Vorgehen: profileCard als definierten Baustein in `design_system.md`
    spezifizieren (Refinement mit Stakeholder: Spalten, Waffen-Tabelle, Abgrenzung zur
    unitCard), danach eigener Plan.
    **Entschieden S135:** App-Design-System mit Wahapedia-Informationsarchitektur, nur
    9E-Datasheet-Spalten (keine berechneten Werte), Wargear-/Relic als Chip; nur Setup-
    Screen, In-Game-Anzeige bleibt wie jetzt (Stakeholder-Kommentar, `S134_offene_punkte.md`).
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
  - **B7 — Redundanter Kopfbereich + schwache Hinweise (Screenshot `…21-29-43.png`):** rot
    markierter Bereich ist redundant; wichtige Hinweise darunter („Select unit", „No PSYKER
    unit available") sind zu schwach sichtbar. Vorgehen: Bereich identifizieren + entfernen,
    Hinweis-Stil als design_system-Konvention stärken; mit B8/B9 als ein Paket
    „Phasen-UI entrümpeln" schneiden.
    **Entschieden S135:** Kopfbereich → Mini-Header (nur Phasenname, Option B, solange kein
    B9-Stepper existiert); Hinweis-Konvention → eigener Design-System-Baustein (Option B);
    B7+B9 als EIN Konzept-Handoff (`S134_offene_punkte.md`).
  - **B8 — Redundanter Statusbereich in jeder Phase (Screenshot `…21-36-36.png`):** in jeder
    Phase redundant → entfernen, Battle-Log-Eintrag genügt. Vorgehen: XS-Entfernung +
    Render-Test; Teil des B7/B9-Pakets.
  - **B9 — Subphasen-Schritte unsichtbar:** je Phase die Unterschritte explizit anzeigen
    (z. B. Movement: erst alle Feldbewegungen, dann Reinforcements), während redundante Texte
    (B7/B8) verschwinden. Vorgehen: „Subphasen-Stepper"-Baustein als design_system-Erweiterung
    entwerfen (Refinement, Layout-Entscheid beim Stakeholder), dann eigener Plan; die
    B7/B8-Entfernungen schaffen den Platz dafür.
    **Entschieden:** Zwischenlösung C (statischer Hinweistext, kein Zustand), Zielbild
    vertikale Checkliste statt horizontaler Chips (Stakeholder-Kommentar); B7+B9 laufen
    als EIN Konzept-Handoff (S135, `S134_offene_punkte.md`).
  - **B10 — Kommentar-Hygiene im Code:** viele Erklär-Kommentare im Code; Soll: Erklärung in
    der Spec, Code selbsterklärend (Clean Code), höchstens ein Verweis-Kommentar auf die
    zuständige Spec. Vorgehen: (a) Konvention im CLAUDE.md-Clean-Code-Abschnitt schärfen
    (freigabepflichtig), (b) danach als Ratchet-Praxis bei jeder Modul-Berührung Kommentare
    in die zuständige Spec verschieben — kein Big-Bang-Durchgang.
    **Entschieden S135:** (a) erledigt — Konvention in `CLAUDE.md` §Clean Code eingetragen;
    (b) läuft als Ratchet-Praxis weiter (`S134_offene_punkte.md`).
  - 🔲 **B11 — Rest-Wahrnehmung nach B1-Fix (Stakeholder-Beobachtung S136):** Beim
    Slot-Wechsel geschieht optisch noch ein kurzer Sprung/Zucken, aber das Fenster bleibt
    an derselben Stelle (kein Scroll-Delta mehr, Playwright-Beleg B1). Beobachten, ggf.
    Dropdown-Höhen stabilisieren (optionaler zweiter Schritt aus `S136_B1_probe.md`).
  - 🔲 **B12 — GO-„used"-Zustand mit Auslöser-Tracking (Stakeholder-Entscheid S137):**
    Undo-Button nur bei der Einheit, bei der die GO angewendet wurde; an allen anderen
    Angebotsstellen der Phase Einsatz unterbinden, Button-Text „Used". Inline-Angebote
    (Attacken-/Charge-Sequenz) zeigen NIE Undo; Once-per-Phase wird erzwungen (nach
    Hit-Einsatz zeigen Wound/Save „used"). Größerer Eingriff: Konzept
    `docs/handoff/S137_B12_konzept.md` (S137), Umsetzung als Teil-Briefs ≤ M danach.
    - ✅ **B12b — Header-Suffix „used on ⟨Einheit⟩" verdrahtet (S141, Commit `cdb55e2f`):**
      Resolver `stratagem_used_elsewhere_unit_name` (`src/uiLayout/_common.py`) + 3
      Zustands-Mapper + Render-Bedingung in `go_card.py`; 9 neue Tests, Vollsuite 1781
      grün / 99,15 %. **Randfall (bewusst offen, spec-konform):** Advance-Reroll-/Inline-
      Spends übergeben konstruktionsbedingt kein `unit_key` an `spend_stratagem` → Suffix
      bleibt dort leer („falls Einheit bekannt"). Optionaler XS-Folge-Task: uid durch
      `spend_stratagem` durchreichen, falls das je gewünscht wird. **Manuelle UI-Verifikation
      steht noch aus** (s. §3).
  - 🔲 **B13 — GO-Karte: Keyword-Badges (Stakeholder-Beobachtung S137):** GO-Karten zeigen
    keine Schlüsselwort-Chips (nur Name/CP/Regeltext). Neues Feature, eigener kleiner Plan;
    erweitert den GO-Card-Baustein (`design_system.md` §6). Keine Eil-Priorität
    (Stakeholder-Entscheid S137: „ins Backlog"). **S141-Nachtrag:** Vorziehen der Daten-
    Nachpflege geprüft und zurückgestellt — `keywords:` existiert in **keiner** der 3
    Stratagem-YAML-Dateien (0 Treffer `_shared`/`necrons`/`orks`) und fehlt auch auf der
    `Stratagem`-Dataclass (`src/gameObjects/stratagem.py`); die Aufgabe ist Schema-
    Erweiterung **plus** Datenpflege, kein reiner YAML-Task. Stakeholder-Entscheid S141:
    zurückstellen, bis B13 selbst geplant wird (dann Schema+Loader+Daten in einem Aufwasch;
    Details `docs/handoff/S141_planning.md` Aufgabe 4).
  - 🔲 **B14 — Badge-Kontrast-Pass (Stakeholder-Beobachtung S137):** Badges schwer
    erkennbar, v. a. STATIONARY (`--arb-muted` `#6b5f44`) zu dunkel. Vorschlag: heller
    Khaki `#9c8f6a`; prüfen, ob weitere gedämpfte Badges mit angehoben werden müssen.
    Farbschema-Entscheidung liegt beim Stakeholder → Hex-Vorschläge vorlegen, dann
    mechanischer Edit `design_colors.md` + `unitCard.py` (Stakeholder S137: „ins Backlog").

Quelle + Details: [../../.claude/tasks/next_session.md](../../.claude/tasks/next_session.md) „Offene Tasks".

- 🟢 **Psychic-Ledger schrumpfen (S62):** Smite-Manifest-Logik (`R-PSYCHIC-11/16/17/18/22`) lebt
  im Render-Code (`_render_smite_flow`/`_render_psi_result`/`_render_deny_column`) → policy-
  ungetestet. Reine Funktionen extrahieren (Schwelle `roll≥wc`, Warp-Charge-Eskalation, Perils-
  Schaden, Deny-once) + Tests → Ledger 15→10.
- 🟢 **Psychic-Lücken (S62, aus Regel-Katalog):** `R-PSYCHIC-23` (Perils zerstört Psyker ⇒ Power
  schlägt fehl; App revidiert `manifested` nicht) und `R-PSYCHIC-24` (Perils-Splash D3 an Einheiten
  in 6") sind `offen` — beide brauchen einen Unit-Destroyed-Check nach Perils-Schaden.
- 🟡 GO-Buttons kontextuell in gameActionArea (aktiver + inaktiver Spieler) statt Liste
- 🟡 Necron Command Phase: Regelkasten immer ganz oben (alle Phasen prüfen)
- 🟡 SAVE-Block: Fähigkeit + AP als eine Badge (`Enslaved AP-1`) — YAML-Erweiterung (→ Plan 017)
- 🟢 Gretchin Cowardly: −1 Attrition ohne RUNTHERD in 6" (→ Plan 018)
- 🟢 Battle-Log: nach Reset keine alten Einträge (→ Plan 018)
- ✅ **CP-Doppelvergabe-Fix — ERLEDIGT (Plan 018 Task 18.1, S128):** `cp_grants`-Set aus
  `(round, faction)`-Paaren ersetzt `cp_granted_this_phase`-Flag; übersteht ←/→-Phasennavigation.
- 🟢 `collect_modifiers_for_phase()` (→ Plan 018 Task 18.4, noch offen)
- ✅ **Scraper-Trunkierung `abilities` — Daten-Anteil ERLEDIGT (S138):** 47 Einträge
  (Ork 42, Necron 5) in `faction_abilities.yaml`/`weapons.yaml` vervollständigt; neuer
  netzunabhängiger Wächter `tests/gameObjects/test_data_quality.py` verhindert Rückfall.
  Scraper-Fix-Anteil (Commit `4dcc560`) geprüft — Ursache war Datenstand von vor dem Fix.
- 🔲 **Totalvernichtungs-Spielende (S138-Befund, Stakeholder: eigener Punkt):** Der
  „army destroyed"-Teil von R-ROUND-07 (`docs/spec/acceptance/rules.md`) ist bewusst
  NICHT implementiert — Sieg durch vollständige Vernichtung der gegnerischen Armee vor
  Ende Runde 5 fehlt als eigener Spielende-Pfad. Eigener kleiner Plan.
- 🔲 **Tote Produktionsfunktion `build_aura_range_hint_text` entfernen (S138-Retro-
  Maßnahme 2, XS):** Einziger Produktions-Konsument (`armyCard._render_aura_range_hint`)
  wurde in S138 entfernt (Conquering-Tyrant-Aura-Hinweis raus); Funktion in
  `ability_engine.py:324` + ihre Tests (`test_ability_engine.py`) werden nur noch von
  Tests referenziert. Mit Tests gemeinsam entfernen, `acceptance/rules.md`-Eintrag
  nachziehen (Code-Referenz wird sonst stale).
- 🔲 **Fold-Heuristik nur Hauptfraktion + Subfaction-Wiring Roster→Unit (S138-Retro-
  Maßnahme 3, zusammen schneiden):** `unitCard.py:_fold_faction_keyword` filtert aktuell
  nur das Hauptfraktions-Keyword (Trailing-„S"-Fold); Subfraktions-Keywords werden nicht
  gefoldet, weil der Loader den `<DYNASTY>`/`<CLAN>`-Platzhalter mangels Roster→Unit-
  Wiring aktuell droppt. Sobald echte Subfraktions-Keywords in die Unit-Listen kommen
  (Klan-Chip statt Drop), muss die Fold-Filterung erneut geprüft werden — beide Teile in
  einem Aufwasch planen.
- 🟢 **Operating-Model Phase C:** Refinement automatisieren — Sonnet-Subagent liest neue
  Bilder aus `Fotos/`, extrahiert die Idee als Text nach `docs/inbox/` (Format dort dokumentiert).
- 🟢 **Gates/Reports leser-orientiert prüfen (→ ADR-0002):** Debt-Scoreboard, Rule-Catalog-Prozente
  u. a. dahingehend durchsehen, ob sie dem Stakeholder *seine* Fragen verständlich beantworten —
  nicht nur maschinen-orientiert zählen.
- ✅ **color_hint-Feld im Modifier-Dict — ERLEDIGT (Plan 022 Step 3, S77):** Optionales
  `color_hint: "buff" | "debuff"` gewinnt gegen die wertbasierte Farbe (`_modifier_color`,
  `dice_compose.py`), rückwärtskompatibel ohne das Feld. Getestet: `test_color_hint_overrides_value_sign`,
  `test_always_fail_color_hint_buff_is_green` u. a. (`tests/uiLayout/test_dice_html.py`). Eintrag hier
  war stale — Quantum-Shield-Verdrahtung selbst (Konsument) bleibt offen (s. „Quantum Shielding" unten).
- 🔲 **Invuln-SAVE-Badge-Bereich chaotisch (S78):** Zeigt drei Teile („Inv 4+", „active", „AP/Cover N/A"), die teils keinen Sinn ergeben. Soll: **eine** klare Badge, z. B. „Invuln 4+". Überschneidet sich mit **Plan 017** (SAVE-Block Fähigkeit+AP kombinierte Badge) → dort mitlösen oder eigener kleiner Task.
- 🔲 **Dice-Display Modifier-Geometrie (Befund B/C, S78):** HIT/WOUND-**Debuff** spreizt nicht mit der Magnitude — `modifier_die_pair_html` zeigt immer `from-1 → from` (−1/−2/−3 sehen identisch aus), Spec §3.1 will den farbigen Würfel mit der Magnitude nach rechts wandern lassen. Zusätzlich verletzt HIT-**Buff** die Slot-1-Invariante (grauer Würfel rutscht auf Spalte 1, §3.3 will min. 2). SAVE-Geometrie ist korrekt. **Eigener Plan** (`modifier_die_pair_html` getestet → Regressionsfläche; eigenes Test-Netz). Die Pfeil-**Zahl** (Befund A) ist bereits umgesetzt (S78).
- 🔲 **Silent-King-Zielaufteilung Fernkampf (S79-UI-Befund; Regel S80 GEKLÄRT):** Ein Modell mit **zwei** Fernkampfwaffen (Silent King: Sceptre of Eternal Glory / Staff of Stars) kann aktuell nur **eine** Feind-Einheit als Ziel wählen — **regelwidrig**. Core Rules: „If a model has more than one ranged weapon, it can split the weapons between different enemy units." Alle Attacken **einer** Waffe gehen auf dieselbe Einheit. → UI auf **Ziel-pro-Waffe** umbauen + alle Ziele vor dem ersten Wurf deklarieren; Staff-of-Stars-Sperre ≤8 W beachten; Regressionstest. Detail: `docs/inbox/finding-silent-king-target-split.md`. Eigener Plan.
- 🔲 **Off-Scale-/„7+"-Save-Grenze (S79-UI-Befund):** Sv 7+ (z. B. Gretchin) bzw. durch AP jenseits 6 verschlechterte Saves brauchen einen „7-Augen"-Würfel **plus** Erfolgsgrenze `|`. Soll lt. Stakeholder: Kopfzeile `[6] | [✕]`; Cover-Randfall `[6] 1→[7]`; AP-Fall `[6] ←4 [✕]` (konsequente Fortschreibung der D5-Spec). → `docs/spec/dice_display.md` ergänzen, **alle** Fälle mit Tests. Verwandt mit Befund B/C.
- 🔲 **AP-/SAVE-Modifier-Magnitude-Position (S79-UI-Befund):** Die Magnitude-Zahl (`-N`/`←N`) gehört in die **Erfolgsgrenz-Spalte** unter `|` (Screenshot AP-2: „-2" unter die Grenze; Basis-AP: erwartetes `-`/Marker in Spalte Würfel „6"). → Spec prüfen, für **alle** Fälle (Buff/Debuff, HIT/WOUND/SAVE) Tests hinterlegen. Eng verwandt mit Befund B/C-Geometrie.
- 🔲 **Lethal Hits (R-CMB-XX, Refinement 2026-06-20):** Unmod. Treffer-6 = kein Wundwurf, Schaden direkt mit Overflow (wie Mortal Wounds). Nicht implementiert. Eigener Plan nach Plan 014.
- 🔲 **Deadly Demise (R-CMB-YY, Refinement 2026-06-20):** Modell zerstört → Mortal Wounds auf Einheiten in X". YAML-Daten vorhanden, Handler fehlt. Eigener Plan.
- 🔲 **Voice of the Triarch (R-CMD-XX, Refinement 2026-06-20):** Silent King — `voiceOfTheTriarch`-Handler fehlt (YAML-Basis fertig: `alter_command_protocol`). → Plan 016 oder eigener kleiner Plan.
- 🔲 **Failsafe/Arkana-Aktivator-UI fehlt (S88-Befund, eigener kleiner Plan):** `activated`-Einträge
  aus `faction_abilities.yaml` mit `once_per_battle: false` werden bei `round_choice`-Fraktionen
  (Necrons/Custodes) **nirgends** als Aktivator gerendert. Ursache: `armyCard._render_once_per_battle_ability_ui`
  ([armyCard.py:356-364](../../src/uiLayout/armyCard.py#L356-L364)) `return`-t früh, wenn die Fraktion
  `round_choice`-Fähigkeiten hat, **und** surface-t nur eine `once_per_battle: true`-Fähigkeit; die
  commandPhase-Pfade (`get_activated_command_abilities`/`activated_wargear_ids`) lesen nur
  `unit_abilities.yaml` + `wargear.yaml`, **nie** `faction_abilities.yaml`. Folge: Failsafe Overcharger
  ist engine-dispatchbar (`buff_stat_bonus`, unit-getestet) **aber nie aktivierbar**. Kein
  Regressions-Bug (Picker war Plan-024-Scope-Out), aber generische Lücke für künftige aktivierbare
  Fraktionsfähigkeiten. Fix: generischen Aktivator für `activated`-`faction_abilities` (unabhängig von
  `once_per_battle`/`round_choice`) + CANOPTEK-Target-Picker (9"). Lehre: **Engine-Test-grün ≠ UI-verdrahtet**
  (vgl. INV-4b-Memory) — Step 5 hätte einen „grep-belege-den-Konsumenten"-Schritt gebraucht.
- ✅ *(erledigt S129, `3d9b26e` — Review-S130-Befund geschlossen)* **Effekt-Feld `modifier` → `success_on` umbenennen (S128-Folge, Paket 1c/Paket 3
  Parallelsperre):** Die Reanimation-Ability nutzt aktuell das generische `modifier`-Feld
  für die Erfolgsschwelle (5+); klarer wäre ein benanntes `success_on`-Feld. Betrifft
  `gameObjects/ability.py` + `gameObjects/loader.py` (beide durch Paket 3 in S128 gesperrt)
  + `necrons/faction_abilities.yaml` + 2 Asserts in den Ability-Tests. Reine Rename-Arbeit,
  kein Verhaltenswechsel.
- ✅ *(erledigt S129, `3d9b26e` — Review-S130-Befund geschlossen)* **`types-PyYAML` + `types-defusedxml` in `requirements-dev.txt` aufnehmen (S128-Folge):**
  danach die 3 `[import-untyped]`-`# type: ignore`-Kommentare in `gameObjects/` entfernen —
  im selben Schritt, sonst meldet mypy `unused-ignore` (neuer Fehler gegen die Baseline).
- 🟢 **`condition_prompt`/`applies_when` als First-Class-Felder in der Effect-Dataclass +
  Loader (S128-Folge, Plan 018 Task 18.3):** Aktuell reiten beide Felder als Roh-Dict in der
  `effects`-Subliste mit, weil `Ability`/`Effect` keine eigenen Felder dafür haben (s.
  Kommentar in `orks/unit_abilities.yaml` beim Gretchin-Cowardly-Eintrag). Sauberere
  Modellierung, sobald ein zweiter Konsument auftaucht.
- 🟢 **Daten-Altlast `gretchin_mob` (S128-Fund, `orks/unit_abilities.yaml`):** `rule_text`
  klingt nach einer 8E-Formulierung („must take a Morale test if it suffers any
  casualties") — gegen `docs/work/wahapedia_orks/` prüfen, ob die 9E-Bedingung abweicht
  (9E: Morale Test nur bei Verlusten UND unter Half-strength, sonst optional?), ggf.
  korrigieren.
- 🔲 **Custodes Rendax Ka'tah Secondary — toter `strength_modifier`-Pfad (Plan 025 Step 6):** In
  `data/wh40k_9e/adeptus_custodes/faction_abilities.yaml`, Protokoll `type: rendax_kath` (oder
  ähnlich), `secondary`-Effekt `type: strength_modifier` mit Zielwert `+1 S nach Charge` — der
  `strength_modifier`-Typ wurde bei Plan 025 Step 6 aus der Engine entfernt (war toter Pfad, vorher
  nie konsumiert). Braucht eigene `strength_if_charged`-Verdrahtung analog Hungry Void D2 (auch
  Charge-bedingt; S97-S98-Befund). YAML → `type: strength_if_charged, value: 1, phase: melee`; Engine-Fn
  existiert bereits; nur Konsum + Test.

- 🔲 **Army-List-UX „weniger Scrollen" (Refinement-Skizze IMG_4051, S94 gesichert):** Übergeordnetes
  UX-Ziel, abgehandelte Einheiten weniger im Weg zu haben. Drei Bausteine: (a) abgehandelte Unit-Card
  automatisch ans **Ende** der Armeeliste schieben; (b) nach **Phasenwechsel** den Fokus auf die nächste
  relevante Unit-Card setzen; (c) optionales manuelles **Umsortieren/Switch** von Cards. Offene technische
  Frage aus der Skizze: ist Reorder/Auto-Scroll in Streamlit überhaupt sauber umsetzbar? → eigener Plan,
  zuerst Streamlit-Machbarkeit klären.
- 🔲 **Quantum Shielding (Refinement-Skizze IMG_4041, S94 gesichert):** Setzt den Rettungswurf (Invuln)
  auf einen **festen Wert (4+)** — keine additive Modifikation, kein Modifier-Pfeil in der Würfelanzeige.
  Eigener Mechanik-Typ „Invuln auf festen Wert setzen" (vs. der bestehenden additiven Modifier-Logik).
  Überschneidet sich mit dem SAVE-/Invuln-Badge-Bereich (Plan 017, „Invuln-Badge chaotisch"). Regel
  zuerst gegen `docs/work/wahapedia_necrons/` prüfen. Eigener Plan oder Teil von Plan 017.
- 🔲 **Waffen-Block: Rapid-Fire-Count + Range anzeigen (Refinement-Skizze IMG_4038, S94 gesichert):** Im
  Waffen-Auswahl-Block der Schussphase je Waffe die **Anzahl Attacken inkl. Rapid Fire** sowie die
  **Reichweite** anzeigen; eligible vs. nicht-eligible Waffen visuell absetzen (durchgestrichen/ausgegraut
  statt nur ausgeblendet). Anzeige-/UX-Thema (verwandt mit der Eligibility-Anzeige der Schussphase und
  dem Silent-King-Ziel-pro-Waffe-Finding). Eigener Plan.
- ✅ **Dynastie-Affinität „beide Direktiven" beim rundenzugewiesenen Protokoll — ERLEDIGT (S140,
  S96-UI-Befund, S97 bestätigt):** Regel (`faction_overview.txt` Z. 862–871): wird das
  Affinitäts-Protokoll _aktiv_ (egal ob 6./permanent oder einer Runde zugeteilt) und hat die ganze
  Armee den Dynastie-Code, gelten **beide** Direktiven statt einer. S140: Round-Zweig von
  `_active_directive_effects` + `active_round_choice_buff_labels` werten `subfaction_affinity` aus
  (Gate `has_round` auf `bool(active_id)` gelockert); UI `_render_round_choice_ui` zeigt bei
  Affinität das „… BONUS (BOTH)"-Badge ohne Wahlzwang (analog Extra-Protokoll-Pfad,
  `_render_directive_buttons` unverändert). Regressionstests je Dynastie in
  `test_ability_engine.py` / `test_game_state.py`. Konzept `S139_dynastie_protokoll_konzept.md` → DONE.
- 🔲 **Dynastie-Code je Einheit statt Roster-Ebene (Konzept-Frage 2 aus
  S139_dynastie_protokoll_konzept, Stakeholder-Entscheid S140):** `subfaction_value_for` liest die
  Subfaction heute auf **Roster-Ebene**; regelseitig trägt jede _Einheit_ den Dynastie-Code. Prüfen,
  ob Einheiten-Ebene nötig ist (Mixed-Dynasty-Roster) und die `subfaction_value_for`-Konsumenten
  (ability_engine, game_state, armyCard) entsprechend umstellen. Eigenes Konzept vor Umsetzung.
- 🟢 **Regel-Index für Wahapedia-Texte (context-audit-S91, verarbeitet S118):** additiver
  Stichwort→`datei:zeilenbereich`-Index als `docs/work/rule_index.md` (Format:
  `Lethal Hits → core_rules.txt:1420-1435`) — ~23k Zeilen Regeltext sind nur per `grep`
  durchsuchbar; kein Wortlaut berührt, beschleunigt Haiku-Lookups.
- 🟢 **CLAUDE.md Token-Disziplin entschlacken (context-audit-S91, verarbeitet S118):**
  `session_context.py`-Implementierungsdetails (Transcript-Pfad, Regex-Fallstrick S65) aus dem
  Token-Disziplin-Abschnitt nach `operating_model.md` Event 6 verlagern; in CLAUDE.md nur
  2-Zeilen-Verweis. Freigabepflichtig (CLAUDE.md-Änderung).
- 🟢 **Backlog-§0-Hygiene (context-audit-S91, verarbeitet S118):** §0-Überschrift „S51" datieren;
  erledigte ✅-Einträge inline nach `session_archive.md`-Historie auslagern statt hier stehen lassen.
- 🔲 **Sudden Storm S — B-Hinweis anzeigen (`shoot_during_action`, S96):** Plan 025 Step 1 hat die Direktive
  datenseitig auf 9E-D2 korrigiert (Typ `shoot_during_action`, kein Engine-Effekt). Der Tisch-Hinweis hat
  noch **keine** sichtbare Anzeige. **S97: wird vom generischen Direktiv-Hinweisblock (Plan 025 Step 2b,
  `enforcement: table`) mit abgedeckt** — nicht mehr separat nachzuziehen.

---

- 🔲 **Audit-Pläne bereinigen (Stakeholder-Auftrag S122, für S123+):** Subagent-Durchgang über
  `docs/audit/plans/` + README-Queue — erledigte/überholte Pläne archivieren bzw. Status
  korrigieren; jeden Plan gegen Code + `git log` verifizieren, nicht nur Statuszeilen lesen
  (Anlass: Plan-015-Step-1-Befund S122 — Plan-Inhalte waren durch den Ziel7-Track längst
  abgedeckt). Tier: Sonnet (Abgleich mit Bewertung, kein reiner Lookup).
- 🔲 **Boarding-Actions-Stratagems laden (Stakeholder-Entscheid S122, → ziel7 Stufe C):**
  NANOSCARAB VIRUS + MINDSHACKLE SCARABS in `necrons/stratagems.yaml` aufnehmen, sobald die
  Hatchway-Abhängigkeit geklärt ist (Entscheid: JA, laden — nicht dauerhaft ausschließen).
  **S134-Nachtrag (✅ Bereinigung erledigt):** Rapid Reanimation, Shield-Piercer Projectors,
  Flensing Capacitors + `resurrection_protocols_character` sind laut Live-Wahapedia ebenfalls
  BA-only und wurden S134 aus dem YAML **entfernt** (Stakeholder-Entscheid) — sie kommen wie
  die zwei obigen erst mit ziel7 Stufe C zurück. Nebenbefund gesichert: `phase: any` +
  `event: after_roll` fehlmatcht jeden Advance-/after_roll-Anker (Rapid-Reanimation-Karte
  erschien als „Advance-Re-Roll" mit „no Advance roll open") — Events künftig wurfspezifisch
  wählen (Merkposten für Paket 4 / Stufe C).
- 🔲 **Variable CP-Kosten in der UI anzeigen (Stakeholder-Entscheid S122):** 5 Necron-Stratagems
  haben variable Kosten (z. B. „3/1 CP"); YAML trägt bewusst das Minimum, `rule_text` erklärt.
  UI soll die Variabilität zeigen (z. B. „1 CP (3 CP für TITANIC)") — es wird mit titanischen
  Einheiten gespielt. UI-Design für Stratagem-Karte nötig.
- 🔲 **/improve-Session vorbereiten (Stakeholder-Auftrag S122, für S123+):** Eigene Session für
  den `/improve`-Skill (read-only Codebase-Audit → priorisierte, in sich geschlossene
  Umsetzungspläne für Executor-Subagenten). Vorbereitung: bereinigte Plan-Queue (Task oben
  zuerst), grüne Vollsuite als Baseline, Scope-Entscheid des Stakeholders (Bugs/Tech-Debt/
  UX/Roadmap) einholen; Ergebnis-Pläne in die `docs/audit/plans/`-Queue einsortieren.
  Token-intensiv → eigene Session.

## 3. Offene manuelle UI-Verifikation (PFLICHT vor „fertig")

Render-Code ist von der Coverage ausgenommen → muss manuell geprüft werden.
Vollständige Checkliste: [../../.claude/tasks/next_session.md](../../.claude/tasks/next_session.md)
(„Manuelle UI-Verifikation" + S48 H1–H7).

- [ ] WAAAGH Boss-Nob: 4 Attacken auf Power Klaw, Wound-Block S 11
- [ ] Cover Option B: Dense im HIT-, Light/Heavy im SAVE-Block, je Tab
- [ ] Veil aus Nahkampf: kein „IN MELEE" danach; Undo stellt wieder her
- [ ] Skorpekh-Roster: 2× Threshers + 1× Reap-Blade getrennt
- [ ] S48 H1–H7 (Big Mek Wargear, Silent King Waffen, Living Metal, MWBD 2×, Badge-Farben, RP)
- [ ] **B12b (S141, Commit `cdb55e2f`):** zentrale Stratagems-Liste — GO auf Einheit
  einsetzen → Karte zeigt an allen anderen Angebotsstellen „Used" + „used on ⟨Einheit⟩"
- [ ] **B12b (S141):** Charge-Phase Fire Overwatch zeigt den Suffix korrekt
- [ ] **B12b (S141):** Movement Advance-Reroll zeigt **keinen** Suffix (kein `unit_key`
  übergeben — spec-konformer Randfall, s. Backlog §2 B12b)
- [ ] **Ziel7 Stufe C-Vorbereitung (S141, Commit `cbaeeb2`):** Emergency Disembarkation +
  Klan-Affinität am neuen Ork-Transport-Roster (`data/rosters/orks_transport.yaml`, Evil
  Sunz, Gunwagon TRANSPORT) real prüfen — war zuvor mangels TRANSPORT-Roster blockiert

---

## 4. Architektur-Schulden

Messbar über das Architektur-Gate → [../spec/architecture_invariants.md](../spec/architecture_invariants.md).

- **Generic-src (INV-4 DEBT):** hartcodierte Fraktions-Defaults aus `src/` entfernen —
  Default-Roster in `game_state.py`, `faction_dir`-Default in `loader.py`, Spielerlabels
  in `gameHeader.py`/`gameProtocoll.py`, Caption in `setupScreen.py`. Ziel: Allowlist leeren.
- ✅ **Generic-src Vokabular (INV-4b DEBT, S51; `protocol` erledigt S52) — DEBT komplett
  aufgelöst (S128 Teil 2, Paket 1):** datengetriebenes Gate (`test_generic_src_vocab.py`)
  listet Fraktions-Eigennamen in `src/`. ✅ **S52:** `protocol`/`protocols` faktion-neutral
  als `round_choice` umbenannt (Klasse `RoundChoiceAbility`, Session-Keys `round_choice_*`,
  Datei `round_choice_ability.py`), Ledger-Einträge entfernt; Reste LEGIT (`typing.Protocol`
  in `phase_handler`) bzw. zur `reanimation`-Schuld (`reanimationProtocols`). ✅
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
  Effekttyp. Ledger jetzt **nur noch LEGIT** (6 Tokens, 3 Dateien: `rosz_importer.py` +
  `protocol`-Kollision in `phase_handler.py`/`ability_engine.py`). Die früher hier
  gelisteten Items `orb`/`overlord`/`phaeron`/`dakka`/`klaw`/`tesla`/`arkana` waren bereits
  vor S128 aus `src/` entfernt — dieser Eintrag war insofern Doku-Drift, jetzt korrigiert.
  Details: [architecture_invariants.md](../spec/architecture_invariants.md) INV-4b.
- 🟡 **mypy-Bestand modulweise abbauen** (Baseline **28**, Stand 2026-07-12 S141;
  Folgearbeit zu Plan 038): `gameMechanic/game_state.py` (−34, Paket 2), `gameObjects/`
  komplett (−18, Paket 3), `gameMechanic/phase_runner.py` (−7, Root Cause: `phase_name`
  in den sieben Phase-Handlern war als Instanzattribut statt `ClassVar[str]` annotiert —
  Protocol-Mismatch gegen `PhaseHandler.phase_name: ClassVar[str]`) sowie **S141: `state`-
  Contract-Fix `dict` → `MutableMapping[str, Any]`** in `ability_engine.py`/
  `unit_mutations.py`/`scenarios.py` (Commit `42af867`, Baseline blieb bei 48) und in
  `phase_handler.py`/`phase_runner.py` + den 7 `*Phase.py`-Dateien + `_common.py` (Commit
  `292b3ad`, Baseline **48 → 28**) sind erledigt. Verbleibend (Stand S141, 28 Fehler):
  **`uiLayout/` zuletzt** (17 Fehler, manuelle Render-Verifikation nötig —
  `armyCard.py`/`gameProtocoll.py`/`unitCard.py`/`armyList.py`/`detachmentCard.py`) plus
  ein Rest von 11 Fehlern in `gameMechanic/` außerhalb des `state`-Contracts
  (`ability_engine.py`/`attack_math.py` `type-arg`, `moralePhase.py`/`unit_mutations.py`
  `no-any-return`/`arg-type` — kein `state: dict`-Fall mehr, andere Fehlerklassen). Pro
  Schritt Baseline in `tools/mypy_gate.py` im selben Commit senken (Ratchet-Regel,
  s. [architecture_invariants.md](../spec/architecture_invariants.md) Typ-Ratchet).
- **Layer-Kopplung:** `gameMechanic/*Phase.py` importiert `uiLayout._common` (Render-Hub).
  Aufräum-Pfad: Phasen-Render nach `uiLayout/` ziehen (vgl. Audit-Plan 008). Bewusst (noch)
  nicht als Wächter erzwungen.
- 🔲 **`_common.py` refactoren (Stakeholder-Auftrag S132):** `src/uiLayout/_common.py`
  (2218 Zeilen) in logische Teile zerlegen; die Attackensequenz sollte eine eigene Datei
  werden. Verwandt mit der Layer-Kopplung oben (gleicher Render-Hub).
- **Test-Mock-Fragilität (S51 entdeckt):** Mehrere `src`-Module lesen das globale
  `st.session_state` und rufen einander auf (`unit_mutations.set_movement_status` →
  `game_state.units_key_for`; `ability_engine` → `game_state`/`unit_mutations`). Tests mocken
  `streamlit` **pro Datei**; wer ein Modul zuerst importiert, bindet dessen `st`. Reihenfolge-
  abhängig → leicht zerbrechlich (S51: ein neuer Test als erster Importer brach 15 Movement-Tests).
  Workaround: Akzeptanztest importiert `game_state` lazy. Saubere Lösung: **eine geteilte
  `streamlit`-Fixture** (conftest) + Tests auf `module.st` statt lokalem `_st_mock` umstellen.
  Tieferliegend ein Smell: viel globaler `session_state`-Zugriff quer durch die Logik-Module.
- 🔲 **DRY ±1-Cap-Helper (S110-Retro-M1):** Hit- und Wound-Block in `dice_html.py` teilen
  identische ±1-Cap-Logik (`_render_dice_roll_block` + `_render_dice_wound_block`) → gemeinsamen
  Helper extrahieren. Kleiner Refactor, kein Verhaltenswechsel; Tests müssen weiter grün bleiben.
- 🔲 **Test-Schuld conftest-Mock-Hack (S110-Retro-M2):** `tests/gameMechanic/conftest.py`
  re-pointet st-Mocks global über `sys.modules` (reihenfolge-abhängiger Quick-Fix aus S110
  Isolations-Fix) → mittelfristig durch eine **session-scoped Streamlit-Mock-Fixture** ersetzen,
  die alle `gameMechanic`-Tests einheitlich nutzen (analog zur sauberen Lösung aus Test-Mock-Fragilität oben).
- ✅ **Coverage-Schuld: game_state + ability_engine (S110-Retro-M3) — ERLEDIGT (S111):**
  `game_state.py` 100 % (+17 Tests) + `ability_engine.py` 100 % (+9 Tests). Coverage-Gate
  auf **99 %** angehoben (`pyproject.toml fail_under = 99`). Toter Reroll-Code entfernt.
- 🔲 **Prozess: Executor-Auftrags-Checkliste härten (S110-Retro-M4):** Executor-Brief muss
  echtes `ruff`/pre-commit **VOR** dem „grün"-Claim verlangen (nicht nur pytest). Außerdem:
  Token-/Zeit-Budget-Cap im Auftrag gegen Rabbit-Holes (Lehre aus S110-Lauf 2b: 161k/66 min);
  Schätzung + harter Stop-Punkt obligatorisch. Betrifft `docs/reference/agent_scopes.md`
  (Executor-Brief-Checkliste, Z. 91–93 ff.) → bei nächster Scope-Pflege einarbeiten.

---

## 4b. Doku-Drift-Befunde (Abgleich 2026-06-15) — zur Klärung, nicht still ändern

`docs/spec/architecture.md` ist teils veraltet (Gesamtbild stimmt, Details nicht):

- **session_state-Schema** (architecture.md): nennt `unit_state` ohne `group_models`/`group_wounds`
  (per-Gruppe-Wunden, real in `game_state.py`); Armee ohne `dynasty`/`protocol_order` (real vorhanden);
  „Owned by `gameMechanic/state.py`" → Datei heißt `game_state.py`.
- **Colour System** (architecture.md §Colour): beschreibt `COLOR_*`-Aliase „als CSS in app.py" —
  das **Live-Theme** sind aber `--arb-*`-Variablen in `gameHeader.py`. Kanonisch ist
  [../spec/design_colors.md](../spec/design_colors.md); die `COLOR_*` (Tailwind-Extrakte in
  `constants/colors.py`) existieren noch, treiben das Theme aber nicht.
- **uiLayout „No game logic in this layer"** (architecture.md): widerlegt durch `_common.py`
  (Attack-Mathe wurde gerade deshalb nach `attack_math.py` ausgelagert) → siehe Layer-Kopplung (§4).
- **Refactoring Plan / Open Design Questions** (architecture.md): historisch, alle Phasen erledigt,
  viele Fragen beantwortet (Stratagems implementiert, CP-Werte bekannt) → als Historie kennzeichnen.

Vorschlag: architecture.md in einer eigenen kleinen Doku-Session aktualisieren (Schema +
Colour-Verweis auf design_colors.md + Historien-Markierung). **Vor Änderung freigeben.**

- **`faction_abilities.md` Z. 42/197 — entferntes `auto_round_1` (S88-Befund):** Tabelle Z. 42
  („Runde 1: Eternal Guardian auto-aktiv (`auto_round_1: true`)") + Phase-2-Liste Z. 197
  referenzieren noch das `auto_round_1`-Flag, das in 6e Bug 1 aus YAML/Dataclass/UI/commandPhase
  **entfernt** wurde (Regeln erlauben freie Verteilung der Protokolle auf Runden 1–5). Reine
  Doku-Altlast → bei der `architecture.md`-Doku-Session mitbereinigen. **Vor Änderung freigeben.**

- **Mortal Wounds Text-Match-Erkennung:** `_detect_weapon_special` nutzt `"mortal wound" in abilities.lower()` — kein strukturiertes YAML-Feld. Technische Schuld, kein akuter Block.
- 🔴 **Command-Protocol-Direktiven nicht regelkonform (S95-Befund, Plan 016 Group A blockiert;
  Plan 025 Step 4 = D1 bereit → Mailbox-Plan `docs/handoff/plan-025-step4.md` Teil A vom
  **Executor-Subagent** umsetzen lassen, nicht im Koordinator-Fenster):**
  Die in `data/wh40k_9e/necrons/faction_abilities.yaml` modellierten Direktiv-Effekte weichen
  von den echten 9E-Protokollen ab (`docs/work/wahapedia_necrons/faction_overview.txt` Z. 583 ff.):
  | Protokoll · Direktive | YAML-Modell | Wahapedia 9E (kanonisch) |
  |---|---|---|
  | Eternal Guardian · P | „+1 to all saving throws" | D1: Light Cover, wenn nicht bewegt |
  | Eternal Guardian · S | „Re-roll saving throws of 1" (`reroll_save_1`) | D2: Hold Steady / Set to Defend bei gegner. Charge |
  | Conquering Tyrant · P | „+1 Leadership" | D1: +3" Aura-Reichweite |
  | Conquering Tyrant · S | „Re-roll hit & wound of 1 (Melee)" (`reroll_hit_wound_1`) | D2: nach Fall Back schießen (−1 Hit) |
  **Entscheid gefallen (S95): Variante (b)** — auf echte 9E-Regeln umstellen.
  → **[Plan 025](../audit/plans/archive/025-protocol-9e-conformance.md)** (heruntergebrochen, je
  Protokoll ein Step). Vollständige Regelprüfung aller 6 Protokolle dort. Nuance: **Sudden
  Storm P** (+1" Move) ist bereits konform, **Undying Legions** substanziell konform (nur P/S
  vs. D1/D2 vertauscht); die anderen vier sind erfunden. 025 rückt **vor 016/017** — Plan 016
  Group A + Conquering-Tyrant-P-Morale werden dadurch obsolet (Effekte verschwinden), 016
  behält nur RP-Hint + Dynastiebonus.

## 4c. Design-System — ERLEDIGT (S116–S118; Doku-Abgleich S120, 2026-07-03)

Kernbefund (S114): 4 divergente Badge-Implementierungen. Vollständig umgesetzt:
- `docs/spec/design_system.md` angelegt (§0–§5), Farben bleiben in `design_colors.md` (Commit `143d848`, S116).
- Schritt 1: `badges.py` (`badge()`/`chip()`) + `symbols.py` (8 Konstanten), 4 Call-Sites konsolidiert; Invuln-Block (`dice_html.py`) bewusst gestrichen statt umgestellt (`143d848`).
- Schritt 2: Glyph-/Chip-Rollout auf die restlichen 10 Produktivdateien (`3915f8c` S117, `29f4f81` S118) — Ratchet-Rest auf Null (Details: `design_system.md` §5).
- Stakeholder hat den Wertesatz + Hinweis-Konvention S120 (2026-07-03) final bestätigt; Handoff-Dateien (`design-system-proposal.md`, `design-system-consensus.md`) gemäß Lifecycle gelöscht.

---

## 4d. Test-Schuld (klein)

Zwei Tautologie-Tests in `tests/gameMechanic/test_damage_block_reanimation.py` bei Gelegenheit schärfen (Quelle: DoD-Review S114; Handoff gelöscht S120):
- Z.394–401: rechnet `4*2==8` selbst nach — kein echter System-Under-Test-Nachweis.
- Z.403–417: prüft nur Fixtures statt RP-Gate-Logik.

Kein Blocker; schärfen wenn ohnehin in der Datei.

Modul-Level-`sys.modules["streamlit"]`-Mocks in 11 Testdateien konsolidieren (Follow-up aus
S118-M2: `tests/gameMechanic/conftest.py` hat jetzt die session-scoped Fixture
`_canonical_streamlit_mock`; die per-File-Mocks vor dem ersten src-Import sind noch dezentral).
Kein Blocker; bei nächster Test-Infra-Arbeit mitnehmen.

- 🔲 **Kein Test lädt alle Roster durch (S141-Befund):** `tests/gameObjects/test_loader.py:1259`
  lädt nur `necrons_alpha` + `orks_test` fest verdrahtet — neue Roster in `data/rosters/`
  (z. B. `orks_transport.yaml`, S141) werden von keinem Test automatisch mitgeprüft. Test-
  Lücken-Kandidat: Loader-Test auf ein Verzeichnis-Glob über `data/rosters/*.yaml` umstellen,
  damit ein kaputtes neues Roster den Loader-Gate bricht statt unbemerkt zu bleiben.

---

## 5. Größere geplante Ziele

- [ziel7.md](ziel7.md) — **Gefechtsoptionen + subfaction-Mechanik** (definiert 2026-06-30):
  Bündelt (a) `collect_modifiers_for_phase` Execute-Logik (§6e), (b) 6f Ability-Badges,
  (c) 6h Kat1–3 neue Fraktionen (AdMech, Tyranids, T'au, Space Marines …).
  - **Ziel7-Cluster: P18** (aus Ziel6 ausgelagert S114; P17 erledigt S115):
    - **P17 — erledigt (S115):** Mechanik steht+getestet — Pre-Apply-Zielauswahl (`_render_subgroup_selector`,
      `_common.py`) + Wounded-Lock (`apply_damage`/`get_locked_group`, `unit_mutations.py`); Vor-Auswahl+Lock
      akzeptiert, ±-Zähler verworfen. Details: `docs/goals/archive/ziel6.md` P17.
    - **P18 — erledigt (bereits S43, `e6fcdb3` Plan 013; Checkbox war stale-offen, verifiziert S117):**
      einheitlicher Deklarations-Flow (`render_group_cards`/`render_group_assignment`, synthetische
      Einzelgruppe für Einheiten ohne `model_groups`) + `melee_with`-Ziel-Anzeige. Getestet: `test_group_flow.py`.
    - **P19 — once_per_battle pro Spieler — ERLEDIGT (2026-07-03, Commit `1f9d82b`):** eingesetzte
      once_per_battle-Gefechtsoption blockte zuvor BEIDE Spieler (Bug — 9E: Einschränkung gilt
      je Spieler) + UI zeigte nicht, welcher Spieler sie eingesetzt hat. Vollsuite 1405 passed /
      99,11 %, UI-Verifikation vom Stakeholder bestätigt. Quelle: `ui-pass-S118.md` S113-Punkt 3.
    - **P20 — Rapid Fire halbe Reichweite — ERLEDIGT (2026-07-03, Commit `dfebd27`):** Attackenzahl
      ist jetzt angebbar, wenn Modelle Ziele innerhalb halber Reichweite wählen; gecappt auf die
      Attackenzahl bei voller Reichweite (z. B. 10 bei 10 Warriors mit Gauss Flayer). Vollsuite
      1405 passed / 99,11 %, UI-Verifikation vom Stakeholder bestätigt. Quelle: `ui-pass-S118.md` S116-Punkt 4.
    - **P21 — BUG: Stratagem-Undo überlebt Phasenwechsel — ERLEDIGT (2026-07-03, Commit `dde16f3`):**
      ↺-Undo-Button wurde nach Phasenwechsel/im nächsten Zug noch angeboten — jetzt nur im selben
      Phasenfenster verfügbar. Widersprach dem S113-Blocker-B1-Codebefund („laut Code NICHT
      angeboten") — Live-Verhalten vs. Code-Analyse abgeglichen, Root Cause gefixt. Vollsuite
      1405 passed / 99,11 %, UI-Verifikation vom Stakeholder bestätigt. Quelle: `ui-pass-S118.md` S113-Punkt 5.

    **Neue offene Befunde (S119-Live-Test + Code-Analyse) — Stufe A erledigt (S120/S121):**
    - ✅ **Stratagem-Doppelanzeige — ERLEDIGT (Task 1, Commit `8c124c3`):** Zwei-Spalten-Split
      (`first_player`/`second_player`) + `stratagem_usable_by_player()`, je Spieler eigene Liste
      (kein `_shared`-Konkat mehr).
    - ✅ **Stratagem-Attributions-Bug — ERLEDIGT (Task 1, Commit `8c124c3`):** Die Spalte selbst ist
      der spending player — keine Ableitung aus `s.player` mehr nötig.
    - ✅ **`used_stratagem_ids` (phase-scoped) global statt per Spieler-Slot — ERLEDIGT (Task 2,
      Commit `396fdec`):** Dict-Form pro Spieler, analog `cp`/`used_stratagem_battle_ids`.
    - Umsetzung: `docs/handoff/plan-ziel7-restruktur.md` Stufe A Task 0 (`f9279fe`, YAML-Drift
      Counter-Offensive/Insane Bravery → `both`), Task 1 (`8c124c3`), Task 2 (`396fdec`). Handoff-
      Datei nach Abschluss gelöscht (S121), Struktur+Kandidatenliste in `docs/goals/ziel7.md` §0
      überführt (kein Informationsverlust).
    - **Manuelle UI-Verifikation S121:** Punkte 1, 2, 5–7 der Checkliste bestätigt; Punkte 3+4
      (Fire Overwatch/Counter-Offensive, `timing: phase_reactive`) NICHT prüfbar — brauchen die
      reaktive Stratagem-UI aus Plan 015 (`docs/audit/plans/015-contextual-reactive-stratagems.md`,
      TODO) → s. F4 unten.

    **Neue Findings (S121-UI-Verifikation, noch offen):**
    - ✅ **F1 — Disruption Fields: Effekt-Semantik korrigiert (S122):**
      Kartentext (`docs/work/wahapedia_necrons/faction_overview.txt:2379`) „add 1 to the Strength
      characteristic of models in that unit" — `data/wh40k_9e/necrons/stratagems.yaml`
      `disruption_fields.modifier.roll_type` war `wound` (+1 auf den Verwundungswurf, nur
      zufällig gleichwertig solange die Toughness-Schwelle nicht kippt), jetzt `strength` (echter
      Stat-Modifier vor der Wound-Tabelle). Totes `effect: {type: buff_stat, ...}`-Feld entfernt
      (bei Stratagems nirgends konsumiert, nur `Ability.effect` wird gelesen — per grep bestätigt).
      Neue reine Funktion `stratagem_strength_bonus()` (`src/gameMechanic/ability_engine.py`)
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
      (`dice_compose.py`) zeichnet den Wert-1-Würfel bei Schwelle ≤ 1 als ✕-Miss innerhalb des
      Erfolgsrahmens. Spec: `docs/spec/dice_display.md` §1 Randfall; Tests:
      `test_dice_row_natural_one_always_shows_miss_marker_even_in_success_frame`,
      `test_save_floored_at_2_armour_path`, `test_save_floored_at_2_invuln_path`.
    - 🟡 **F4 — Stufe-A-Verifikationspunkte 3+4 setzen Plan 015 voraus** (s. o.): Plan 015
      (Priorität P2, `docs/audit/plans/README.md`) schaltet damit auch die Reaktiv-UI-Prüfung für
      Fire Overwatch/Counter-Offensive frei — als Kandidat für die nächste Session vormerken.
- [ziel8.md](ziel8.md) — Crusade-Erweiterung (geplant)
- [ziel9.md](ziel9.md) — Wahapedia Faction Fetcher (geplant)
- 🟡 **Richtungsentscheid offen (Audit S124, aus next_session.md verschoben S129):** ziel9-Fetcher
  vorziehen? Eigene Deployment-Phase bauen oder ADR „bleibt am Tisch"? Mission-Scoring (eine
  Mission end-to-end)? — noch nicht entschieden, Stakeholder-Input nötig.
- [index.md](index.md) — Ziel-Gesamtübersicht

---

## Wo was steht (Artefakt-Verweise)

| Frage | Artefakt |
|---|---|
| Was mache ich als Nächstes? | [next_session.md](../../.claude/tasks/next_session.md) |
| Was ist insgesamt offen? | **dieser Index** |
| Detailplan eines Features? | [../audit/plans/](../audit/plans/) |
| Architektur-Bild + Invarianten? | [../spec/architecture.md](../spec/architecture.md) · [../spec/architecture_invariants.md](../spec/architecture_invariants.md) |
| Ziel-Historie / Changelog? | [session_archive.md](../metrics/session_archive.md) „Session-Historie" |
