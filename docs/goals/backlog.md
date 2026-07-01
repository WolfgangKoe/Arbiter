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
  | Conquering Tyrant · P | **9E-D1:** +3" Aura-Reichweite (`aura_range_bonus`, **Klasse B**, `enforcement: table`) | n/a (Tisch) | 🔲 Tisch-Hinweis (Plan 025 Step 5) |
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
- 🔲 **R-CMD-03 — CP-Grant ohne Battle-forged-Gating** (S55, aus Regel-Katalog):
  Der „Grant +1 CP"-Button in `commandPhase._render_faction_actions` erscheint für die
  aktive Seite **unabhängig von `game_mode`/Battle-forged** → eine Unbound-Armee könnte
  den Command-Phase-Bonus ebenfalls erhalten (Regel: nur Battle-forged). Fix-Ort:
  `_render_faction_actions` an Battle-forged koppeln + Regressionstest. Ledger-Eintrag
  `R-CMD-03` in [../spec/acceptance/rules.md](../spec/acceptance/rules.md).
- 🔲 **#INV-4b Cluster-Entscheidungen (Refinement 2026-06-20):** Konsensentscheidungen für INV-4b Vokabular-Schulden:
  - **Cluster 1 — `dakka`/`klaw`/`tesla`**: YAML-gesteuert via `weapon_special`-Schema → Teil von Plan 022 oder eigenständig.
  - **INV-4 Default-Roster** (`game_state.py`, `loader.py`): 2 verbleibende Debt-Einträge (hardcodierte `"necrons"`-Defaults) → eigener kleiner Task nach Plan 019/020.
  - _(Cluster 3 ✅ Plan 020, Cluster 4/5 ✅ XS-Fix, Cluster 6 ✅ Plan 021/024 — erledigt, aus Backlog entfernt)_

---

## 1. Aktive Implementierungs-Pläne (Executor-Queue)

Plan-Status & Reihenfolge → [docs/audit/plans/README.md](../audit/plans/README.md) (kanonisch)

---

## 2. Offene Tasks (kleiner als ein Plan)

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
- 🟢 CP-Doppelvergabe-Fix + `collect_modifiers_for_phase()` (→ Plan 018)
- 🟢 **Operating-Model Phase C:** Refinement automatisieren — Sonnet-Subagent liest neue
  Bilder aus `Fotos/`, extrahiert die Idee als Text nach `docs/inbox/` (Format dort dokumentiert).
- 🟢 **Gates/Reports leser-orientiert prüfen (→ ADR-0002):** Debt-Scoreboard, Rule-Catalog-Prozente
  u. a. dahingehend durchsehen, ob sie dem Stakeholder *seine* Fragen verständlich beantworten —
  nicht nur maschinen-orientiert zählen.
- 🔲 **color_hint-Feld im Modifier-Dict (Refinement 2026-06-20):** Optionales `color_hint: "buff" | "debuff"` im Modifier-Dict für nicht-numerische Modifier (z.B. Quantum Shield). Default: wertbasiert. Rückwärtskompatibel. → `ability_engine.py`, `dice_html.py`, Tests.
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
- 🔲 **Dynastie-Affinität „beide Direktiven" greift nicht beim rundenzugewiesenen Protokoll (S96-UI-Befund, S97 vom Stakeholder erneut bestätigt — als Bug zu führen, nicht nur Notiz):**
  Regel (`faction_overview.txt` Z. 862–871): wird das Affinitäts-Protokoll *aktiv* (egal ob 6./permanent
  oder einer Runde zugeteilt) und hat die ganze Armee den Dynastie-Code, gelten **beide** Direktiven statt
  einer. Aktuell greift das nur für das **6. (permanent aktive)** Protokoll (`_extra_directive_effects` in
  [ability_engine.py](../../src/gameMechanic/ability_engine.py)); im **Round-Zweig** von `_active_directive_effects`
  ([ability_engine.py:139-144](../../src/gameMechanic/ability_engine.py#L139)) wird nur die *eine* gewählte
  Direktive angehängt, und die UI ([armyCard.py](../../src/uiLayout/armyCard.py) `_render_directive_buttons`)
  verlangt weiter eine manuelle Primary/Secondary-Wahl. Soll: bei Affinität auch im Round-Zweig **beide**
  automatisch aktivieren + UI analog zum Extra-Protokoll-Pfad (kein Wahlzwang, „beide aktiv"-Anzeige).
  Engine + UI + Regressionstest. Verwandt mit Plan 016 (Dynastiebonus-Anzeige).
- 🔲 **Sudden Storm S — B-Hinweis anzeigen (`shoot_during_action`, S96):** Plan 025 Step 1 hat die Direktive
  datenseitig auf 9E-D2 korrigiert (Typ `shoot_during_action`, kein Engine-Effekt). Der Tisch-Hinweis hat
  noch **keine** sichtbare Anzeige. **S97: wird vom generischen Direktiv-Hinweisblock (Plan 025 Step 2b,
  `enforcement: table`) mit abgedeckt** — nicht mehr separat nachzuziehen.

---

## 3. Offene manuelle UI-Verifikation (PFLICHT vor „fertig")

Render-Code ist von der Coverage ausgenommen → muss manuell geprüft werden.
Vollständige Checkliste: [../../.claude/tasks/next_session.md](../../.claude/tasks/next_session.md)
(„Manuelle UI-Verifikation" + S48 H1–H7).

- [ ] WAAAGH Boss-Nob: 4 Attacken auf Power Klaw, Wound-Block S 11
- [ ] Cover Option B: Dense im HIT-, Light/Heavy im SAVE-Block, je Tab
- [ ] Veil aus Nahkampf: kein „IN MELEE" danach; Undo stellt wieder her
- [ ] Skorpekh-Roster: 2× Threshers + 1× Reap-Blade getrennt
- [ ] S48 H1–H7 (Big Mek Wargear, Silent King Waffen, Living Metal, MWBD 2×, Badge-Farben, RP)

---

## 4. Architektur-Schulden

Messbar über das Architektur-Gate → [../spec/architecture_invariants.md](../spec/architecture_invariants.md).

- **Generic-src (INV-4 DEBT):** hartcodierte Fraktions-Defaults aus `src/` entfernen —
  Default-Roster in `game_state.py`, `faction_dir`-Default in `loader.py`, Spielerlabels
  in `gameHeader.py`/`gameProtocoll.py`, Caption in `setupScreen.py`. Ziel: Allowlist leeren.
- **Generic-src Vokabular (INV-4b DEBT, S51; `protocol` erledigt S52):** datengetriebenes
  Gate (`test_generic_src_vocab.py`) listet Fraktions-Eigennamen in `src/`. ✅ **S52:**
  `protocol`/`protocols` faktion-neutral als `round_choice` umbenannt (Klasse
  `RoundChoiceAbility`, Session-Keys `round_choice_*`, Datei `round_choice_ability.py`),
  Ledger-Einträge entfernt; Reste LEGIT (`typing.Protocol` in `phase_handler`) bzw. zur
  `reanimation`-Schuld (`reanimationProtocols`). ✅ **2026-06-20:** Quick-Wins (Spielerlabels
  `gameHeader`/`gameProtocoll`, Caption `setupScreen`) → generisch; Renames
  `pending_irongob` → `pending_triggered_relic`, `res_orb_*` → `revive_wargear_*`
  (`irongob` komplett raus; INV-4 Allowlist 10→5, INV-4b 20→19 Tokens). Verbleibend:
  benannte Items (`orb`, `overlord`, `phaeron`, `gloom`, `prism`, `dakka`, `klaw`, `tesla`,
  `reanimation`, `arkana`, `dynasty`) aus Phasen-/Render-Modulen in YAML/Daten ziehen
  (Schema-Urteil → Konsens). Ziel: Ledger schrumpfen (Ratchet).
- **Layer-Kopplung:** `gameMechanic/*Phase.py` importiert `uiLayout._common` (Render-Hub).
  Aufräum-Pfad: Phasen-Render nach `uiLayout/` ziehen (vgl. Audit-Plan 008). Bewusst (noch)
  nicht als Wächter erzwungen.
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
  → **[Plan 025](../audit/plans/025-protocol-9e-conformance.md)** (heruntergebrochen, je
  Protokoll ein Step). Vollständige Regelprüfung aller 6 Protokolle dort. Nuance: **Sudden
  Storm P** (+1" Move) ist bereits konform, **Undying Legions** substanziell konform (nur P/S
  vs. D1/D2 vertauscht); die anderen vier sind erfunden. 025 rückt **vor 016/017** — Plan 016
  Group A + Conquering-Tyrant-P-Morale werden dadurch obsolet (Effekte verschwinden), 016
  behält nur RP-Hint + Dynastiebonus.

## 4c. Design-System — Entscheidungen getroffen, Umsetzung nächste Session

Vorschlag: `docs/handoff/design-system-proposal.md` (→ ANSWERED, S114 2026-06-30). Kernbefund: 4 divergente Badge-Implementierungen im Codebase. Entscheidungen gefallen:
- `docs/spec/design_system.md` anlegen + `design_colors.md` integrieren/konsolidieren.
- Schritt-1-Umfang: `_common._badge()` + `unitCard._badge()` + `armyCard.py` + Invuln-Block (`dice_html.py:188-204`).
- Token-Wertesatz (Radius/Padding/Font-Size): Umsetzungs-Session schlägt simpelsten Satz vor, User bestätigt.
- Zentrale Symbol-Konstantenliste (▶◀✓✕＋⚔↺) anlegen.
- Hinweis-Konvention (info/warning/success/error): Umsetzungs-Session legt Regel vor, User bestätigt.

**Umsetzung = nächste Session. Freigabe vor Code-Änderungen einholen.**

---

## 4d. Test-Schuld (klein)

Zwei Tautologie-Tests in `tests/gameMechanic/test_damage_block_reanimation.py` bei Gelegenheit schärfen (Quelle: review-S114.md):
- Z.394–401: rechnet `4*2==8` selbst nach — kein echter System-Under-Test-Nachweis.
- Z.403–417: prüft nur Fixtures statt RP-Gate-Logik.

Kein Blocker; schärfen wenn ohnehin in der Datei.

---

## 5. Größere geplante Ziele

- [ziel7.md](ziel7.md) — **Gefechtsoptionen + subfaction-Mechanik** (definiert 2026-06-30):
  Bündelt (a) `collect_modifiers_for_phase` Execute-Logik (§6e), (b) 6f Ability-Badges,
  (c) 6h Kat1–3 neue Fraktionen (AdMech, Tyranids, T'au, Space Marines …).
  - **Ziel7-Cluster: P18** (aus Ziel6 ausgelagert S114; P17 erledigt S115):
    - **P17 — erledigt (S115):** Mechanik steht+getestet — Pre-Apply-Zielauswahl (`_render_subgroup_selector`,
      `_common.py`) + Wounded-Lock (`apply_damage`/`get_locked_group`, `unit_mutations.py`); Vor-Auswahl+Lock
      akzeptiert, ±-Zähler verworfen. Details: `docs/goals/ziel6.md` P17.
    - **P18** — Einheitlicher Deklarations-Flow + Untergruppen-Ziel-Anzeige in PlayerArea (~25k, Sonnet); manuelle UI-Verifikation Pflicht.
- [ziel8.md](ziel8.md) — Crusade-Erweiterung (geplant)
- [ziel9.md](ziel9.md) — Wahapedia Faction Fetcher (geplant)
- [index.md](index.md) — Ziel-Gesamtübersicht

---

## Wo was steht (Artefakt-Verweise)

| Frage | Artefakt |
|---|---|
| Was mache ich als Nächstes? | [next_session.md](../../.claude/tasks/next_session.md) |
| Was ist insgesamt offen? | **dieser Index** |
| Detailplan eines Features? | [../audit/plans/](../audit/plans/) |
| Architektur-Bild + Invarianten? | [../spec/architecture.md](../spec/architecture.md) · [../spec/architecture_invariants.md](../spec/architecture_invariants.md) |
| Ziel-Historie / Changelog? | [ziel6.md](ziel6.md) „Session-Historie" |
