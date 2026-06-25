# Backlog — zentraler Index

> **Ein Ort für „was ist offen".** Dieser Index führt die bisher verstreuten Quellen
> zusammen (Executor-Pläne, offene Tasks, manuelle Verifikation, Architektur-Schulden).
> **Details bleiben in den verlinkten Artefakten** — hier wird nicht dupliziert, nur verwiesen.
>
> Pflege: Wird ein Punkt erledigt, hier abhaken **und** in der Detailquelle. Neue Arbeit
> entweder als Plan in [../audit/plans/](../audit/plans/) oder als Task-Zeile hier.

Letzter Abgleich: 2026-06-22

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
- ✅ **#1 Faktion-/Subfaction-Badge** (S51): Faktion-Badge zeigt Faktionsnamen
  (nicht Roster-Titel); Subfaction-Badge generisch + **immer sichtbar** (Wert /
  „No <Label>" / „No Subfaction"); helles Blau `#a5b4fc`. Alle Roster mit Pflicht-
  Subfaction. Pins: `AC-SUBFACTION-01..05`. „dynasty"-Vokabular aus `src/` entfernt.
- 🟡 **#2b Direktiv-Lock** (Phase 2, S52 Root-Cause): **Setup-Leck erledigt 2026-06-20.**
  Bug (Nutzer-Screenshots): Protokoll-Direktiven-Buttons + WAAAGH-Status erschienen im Setup
  und wurden durch den First-Player-Toggle (`active` gesetzt) sogar wählbar; der Auto-Block
  `if not active_id` schrieb `round_choice_active_*` schon im Setup. **Fix:** reiner Helfer
  `_ability_section_visible(phase_key)` (`!= "setup"`) + früher `return` in
  `armyCard._render_round_choice_ui` **und** `_render_once_per_battle_ability_ui`;
  Regressionstest `test_ability_sections_hidden_in_setup_only`. Render-Code → manuelle
  Verifikation steht (s. u.). **Offen (Rest #2b):** Direktive ab Bewegungsphase sperren
  (eigener kleiner Task).
- 🟡 **#2 Protokoll-Buff-Audit** (Phase 3): **Engine-Wiring erledigt (Plan 024,
  S86/S87)** — alle 12 Direktiv-Effekte sind jetzt engine-seitig verdrahtet
  (vorher 3/12); offen bleibt nur noch die **Anzeige** (Badge/Block) je Direktive.
  Spalte „Engine" = liefert die Funktion den Effekt; Spalte „Anzeige" = Render-Code
  (Plan 016/017-Gebiet, manuelle Verifikation):

  | Protokoll · Direktive | Effekt | Engine | Anzeige |
  |---|---|---|---|
  | Eternal Guardian · P | save_modifier +1 | ✅ | ✅ SAVE-Block grün |
  | Eternal Guardian · S | reroll_save_1 | ✅ (`get_active_round_choice_rerolls`) | 🔲 SAVE-Hinweis |
  | Hungry Void · P | hit_modifier +1 (Shooting) | ✅ | ✅ HIT-Block |
  | Hungry Void · S | strength_modifier +1 (Shooting) | ✅ | 🔲 WOUND-Block S+1 |
  | Conquering Tyrant · P | leadership_bonus +1 | ✅ (informativ, kein UI-Konsument) | 🔲 Morale |
  | Conquering Tyrant · S | reroll_hit_wound_1 (Melee) | ✅ (`get_active_round_choice_rerolls`) | 🔲 HIT+WOUND Melee |
  | Sudden Storm · P | move_bonus +1 | ✅ | 🔲 Bewegungs-Badge |
  | Sudden Storm · S | advance_and_charge | ✅ (`charge_after_advance_allowed`) | 🔲 Charge-Phase |
  | Undying Legions · P | rp_reroll (one die) | ✅ (`get_active_rp_modifiers`) | ✅ RP-Block-Hint (S89; UI-verifiziert S93) |
  | Undying Legions · S | **heal_bonus** Living Metal +1 (war fälschlich `rp_bonus` „model returned" — S89-Datenfix) | ✅ (`get_active_heal_bonus`) | ✅ Caption (S89; UI-verifiziert S93) |
  | Vengeful Stars · P | wound_modifier +1 (Shooting) | ✅ | ✅ WOUND-Block |
  | Vengeful Stars · S | ap_bonus -1 (Shooting) | ✅ | 🔲 SAVE-Block AP |

  Buff-Badge grün (`design_colors.md` §3), nur bei betroffenen Einheiten + im
  Phasen-Block (wie MWBD). Anzeige-Rest überschneidet sich mit Plan 016/017.
  **S93-Engine-Befund:** alle Direktiv-Reads lasen bisher nur die runden-zugewiesene Direktive; das **6. (immer-aktive)
  Protokoll** (`extra_directive`) + der **Dynastie-Affinitäts-Fall** (beide Direktiven) wurden ignoriert — kosmetisch, nicht
  wirksam. Gefixt: `_active_directive_effects` aggregiert beide Quellen (alle 5 Reads). Damit ist auch der **Dynastiebonus
  (6e Bug 3) erstmals wirksam** verdrahtet. Offen bleibt nur Eternal Guardian **S** SAVE-Hinweis (Plan 016 Group A).
- 🔲 **#3/#4 Würfelanzeige** (Phase 4): Pfeilrichtung/-länge der Modifier-Zeile +
  Badge-Breite (ragt in Würfel „1"). **Badge-Wert bleibt** (`AP-1`/`AP-2`, Stakeholder-
  Entscheid 2026-06-21 — Gewohnheit + Konsistenz zu anderen Profilwerten; Pfeil ist
  bewusst redundant). Labels nur **kürzen** (truncate/ellipsis), nicht den Wert entfernen.
  Soll-Bild als AC in `docs/spec/dice_display.md` festgelegt → Plan 022, dann per AC
  einrasten (Lehre aus Finding 9.2 — nie still ändern).
- ✅ **R-COMBAT-32 — Doku-Drift im Regel-Katalog** (S60→S62 erledigt): „Charging Units Fight
  First" stand als `offen`/`getestet: nein`, war aber implementiert. Bei der Verifikation (S62)
  zeigte sich: nur die *Berechtigung* war getestet, der *Reihenfolge*-Zweig (Nicht-Gecharger
  wartet, solange ein Gecharger offen ist — `can_fight_now`/`_any_charged_remain`) war ungedeckt.
  Daher Regressionstest `test_non_charged_waits_while_charged_pending` ergänzt, dann R-COMBAT-32
  auf `implementiert` + `getestet: ja` + `code: fightPhase.py:can_fight_now` gesetzt. Klasse-A-
  Abdeckung 28→29. (Ledger unberührt: Regel war `offen`, nicht impl.-ohne-Test.)
- 🔲 **R-CMD-03 — CP-Grant ohne Battle-forged-Gating** (S55, aus Regel-Katalog):
  Der „Grant +1 CP"-Button in `commandPhase._render_faction_actions` erscheint für die
  aktive Seite **unabhängig von `game_mode`/Battle-forged** → eine Unbound-Armee könnte
  den Command-Phase-Bonus ebenfalls erhalten (Regel: nur Battle-forged). Fix-Ort:
  `_render_faction_actions` an Battle-forged koppeln + Regressionstest. Ledger-Eintrag
  `R-CMD-03` in [../spec/acceptance/rules.md](../spec/acceptance/rules.md).
- 🔲 **#INV-4b Cluster-Entscheidungen (Refinement 2026-06-20):** Konsensentscheidungen für INV-4b Vokabular-Schulden:
  - ✅ **Konsens 2026-06-21 (jetzt umsetzbar, kein Schema-Risiko):** Cluster 4 + 5 als XS-Fixes
    freigegeben — entweder kleiner gemeinsamer Plan oder Teil von Plan 018. Cluster 1/2/3/6 bleiben
    an ihren Plänen (022/020/021), weil sie das YAML-Schema berühren (eigener Designentscheid je Plan).
  - **Cluster 4 — `dynasty`** (`movementPhase.py`) ✅ Konsens: UI-String `"DYNASTY CORE unit"` raus → Label aus Unit-YAML lesen (Keyword `DYNASTY` steht dort). XS-Fix.
  - **Cluster 5 — `gloom`/`prism`** (`psychicPhase.py`) ✅ Konsens: `"Gloom Prism"` ist **Necron**-Wargear (nicht Custodes). Tooltip-Text generalisieren → Wargear-Name aus YAML lesen, Fallback: `"Deny-Once-Wargear"`. XS-Fix.
  - ✅ **Cluster 3 — `orb`/`overlord`/`resurrection` + `phaeron`** (`commandPhase.py`) **erledigt S83 (Plan 020):** generischer Activated-Wargear-Flow (`_render_activated_wargear`, Lookup via `ability_type: activated`); PHAERON-Bonus datengetrieben (`extra_uses`); Allowlist-Eintrag entfernt.
  - ✅ **Cluster 6 — `arkana`** (`loader.py`) **erledigt S84 (Plan 021):** Arkana in `faction_abilities.yaml`, `load_points` liest `cost_pts` generisch (`_add_faction_ability_costs`), `"arkana"`-Literal aus `loader.py` entfernt. **Effekt-Modellierung Plan 024 (S87) abgeschlossen:** alle 12 Arkana haben strukturiertes `trigger`/`conditions`/`effect` + engl. `rule_text`; **1 dispatchbar** (Failsafe Overcharger → `activated`, `buff_stat`), **11 bleiben begründet `descriptive`** (fehlende Engine-Subsysteme — Tabelle in `docs/spec/faction_abilities.md`). Kein neuer Faction-String in `src/` → INV-4b unverändert.
  - **Cluster 1 — `dakka`/`klaw`/`tesla`**: YAML-gesteuert via `weapon_special`-Schema → Teil von Plan 022 oder eigenständig.
  - **INV-4 Default-Roster** (`game_state.py`, `loader.py`): 2 verbleibende Debt-Einträge (hardcodierte `"necrons"`-Defaults) → eigener kleiner Task nach Plan 019/020.

---

## 1. Aktive Implementierungs-Pläne (Executor-Queue)

Detailpläne + Abhängigkeiten: [../audit/plans/README.md](../audit/plans/README.md). Pläne 001–013 = DONE.

| Plan | Titel | Prio | Status |
|------|-------|------|--------|
| [014](../audit/plans/014-p17-defender-loss-allocation.md) | P17: Verteidiger-Korrektur Schadenszuweisung (Gruppen) | HOCH | ✅ DONE (S82) — manuelle UI-Verifikation offen |
| [016](../audit/plans/016-necron-protocol-effects.md) | Protokoll-Effekte auf RP/Living Metal + Dynastiebonus | MITTEL | TODO |
| [018](../audit/plans/018-low-prio-cleanup.md) | Kleinkram: CP-Doppelvergabe, Battle-Log-Reset, Gretchin, Modifier | NIEDRIG | TODO |
| [015](../audit/plans/015-contextual-reactive-stratagems.md) | Reaktive Stratagems: Overwatch, Counter-Offensive, HI-Hook | MITTEL | TODO |
| [017](../audit/plans/017-ability-ap-combined-badge.md) | SAVE-Block: Fähigkeit+AP kombinierte Badge | MITTEL | TODO |
| [019](../audit/plans/019-ui-target-consolidation.md) | UI Target Consolidation: `pending_target_request` (MWBD/Orb/Subgruppe) | MITTEL | ✅ DONE (2026-06-20) |
| [020](../audit/plans/020-generic-activated-wargear.md) | Generic Activated Wargear: Resurrections-Orb → generisch (Option B) | MITTEL | ✅ DONE (S83) |
| [021](../audit/plans/021-faction-abilities-arkana.md) | Arkana → `faction_abilities.yaml` + Loader generisch | MITTEL | ✅ DONE (S84) — nur Daten-Migration + generischer Loader + INV-4b-Literal; Effekte offen → Plan 024 |
| [022](../audit/plans/022-dice-display-rework.md) | Dice Display Rework: Arrow-Fix + Edge Cases + color_hint + Tests | HOCH | ✅ DONE (S77) |
| [023](../audit/plans/023-overview-archive-rework.md) | Subagent-Archiv Rework: schlanke overview.md + separate session_archive.md | MITTEL | ✅ DONE (S85, 2026-06-21) |
| [024](../audit/plans/024-arkana-protocol-effect-modeling.md) | Directive-Wiring + Arkana-Schema + Failsafe-Dispatch-Pilot | MITTEL-HOCH | ✅ DONE (S88) — Steps 1–4 (Direktiv-Wiring + RP, S86) · 5–6 (Failsafe `activated`-Dispatch + Arkana-Schema + Kosten, S87) · 7 (Doku, S88); 11/12 Arkana begründet `descriptive`. Manuelle UI-Verifikation offen |

**Empfohlene Reihenfolge (akt. S88): 019·022·014·020·021·023·024 DONE → 016 → 018 → 015 → 017.**
024 abgeschlossen (S88). **Offen nur** die manuelle UI-Verifikation (Failsafe aktivierbar + Direktiv-Anzeigen). Nächstes Stück: **016**.

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
- ✅ **Operating-Model Phase B (S57):** `tools/token_report.py` + `docs/metrics/overview.md` —
  Token-/Wer-leistete-was-Report; führt Haupt- + Subagent-Verbrauch getrennt zusammen
  (je Tier + je Session); aus Leitstand-Feld 4 verlinkt. `--write` regeneriert den Report.
- 🟢 **Operating-Model Phase C:** Refinement automatisieren — Sonnet-Subagent liest neue
  Bilder aus `Fotos/`, extrahiert die Idee als Text nach `docs/inbox/` (Format dort dokumentiert).
- ✅ **Token-Report v2 (leser-orientiert, → ADR-0002, S57):** Akzeptanzkriterien erfüllt —
  (a) Session-Label = Datum + Uhrzeit + Kurz-ID (S-Nummer nicht im Transcript, daher Datum
  statt S-Nr); (b) jüngste Session oben (nach Startzeit sortiert); (c) Σ als „Σ (alle Sessions)"
  beschriftet; (d) je Session Subagenten-Anzahl + eigene Detailtabelle (Agent + Aufgabe aus
  `*.meta.json`); (e) Mermaid-Tortendiagramm der Token je Tier.
- ✅ **Token-Report v3 (Effizienz statt Menge, → ADR-0002, S58):** Umbau zu einer Effizienz-Anzeige
  („wurden die Token gut ausgegeben, werden wir besser/schlechter?"). Akzeptanz a–f erfüllt:
  (a) Fokus-Block letzte Session (Text + Zusammensetzungs-Balken input/cache_creation/cache_read/
  output); (b) Verlauf 6 Sessions mit theme-sicheren Unicode-Balken Peak-Kontext/Subagent-Anteil/
  Modell-Mix (`█`Opus·`▓`Sonnet·`▒`Haiku) + Trend ↑/↓; (c) auto-Hinweise (Korridor/Subagent/Tiering);
  (d) Subagenten-Tabelle Session·Modell·Agent·Aufgabe; (e) Aufgabe aus 1. User-Nachricht +
  optionaler `docs/metrics/session_notes.yaml`-Link; (f) All-Time-Torte entfernt. 23 Tool-Tests grün.
  Frühere Spec:
  - (a) **Fokus letzte Session**: Text (Aufgabe, Modelle je Rolle, Tokens, Peak-Kontext vs. 150k,
    Subagent-Anteil, cache_read/Output) **+ Diagramm** = Zusammensetzungs-Balken (input /
    cache_creation / cache_read / output).
  - (b) **Verlauf letzte 6 Sessions** (inkl. der aktuellen als jüngste Zeile), je als Balken,
    theme-sicher (Unicode/Schattierung, keine Farb-Legende): **Peak-Kontext** (vs. 150k) +
    **Subagent-Anteil** + **Modell-Mix** (segmentierter Balken, `█` Opus · `▓` Sonnet · `▒` Haiku),
    jeweils mit **Trend ↑/↓** ggü. den davorliegenden Sessions.
  - (c) **Hinweise** auto-generiert, usage-fenster-artig (>150k-Anteil, subagent-heavy, Modellwahl).
  - (d) **Subagenten-Tabelle**: Session | Modell | Agent | Aufgabe.
  - (e) **Aufgabe je Session** automatisch aus erster User-Nachricht + optionaler Backlog-Link via
    `docs/metrics/session_notes.yaml` (`<session-id>: link`).
  - (f) All-Time-Tortendiagramm **entfernen** (nützt nicht; dunkle Mermaid-Legende unlesbar).
  - Peak-Kontext = max(`input + cache_read + cache_creation`) je Antwort der Session.
- 🟢 **Gates/Reports leser-orientiert prüfen (→ ADR-0002):** Debt-Scoreboard, Rule-Catalog-Prozente
  u. a. dahingehend durchsehen, ob sie dem Stakeholder *seine* Fragen verständlich beantworten —
  nicht nur maschinen-orientiert zählen.
- 🔲 **color_hint-Feld im Modifier-Dict (Refinement 2026-06-20):** Optionales `color_hint: "buff" | "debuff"` im Modifier-Dict für nicht-numerische Modifier (z.B. Quantum Shield). Default: wertbasiert. Rückwärtskompatibel. → `ability_engine.py`, `dice_html.py`, Tests.
- ✅ **BUG Heroic Intervention crasht (S78 → FIXED S79):** Wurzel war `StreamlitDuplicateElementKey` bei **Duplikat-Squads**, die `unit.id` teilen (z. B. Necron 3× Warriors) — **nicht** `int("User×N")` (Hypothese per Laufzeit-Repro widerlegt). Fix: State-Key (`#N`) durch den HI-Flow gefädelt (`hi_eligible_units`, beide Render-Fn, Confirm) + Mutation in getestete `perform_heroic_intervention()` (`unit_mutations.py`) extrahiert. 16 Regressionstests (inkl. „erste Squad bleibt unberührt").
- ✅ **BUG Badge „AP-4 -4" doppelt (S78 → FIXED S79):** Label-Komposition für AP in gemessenen Helper `save_ap_modifier_row_html` geholt (Label „AP", Wert genau einmal angehängt → „AP -4"). Tests pinnen „AP -4" und Nicht-Vorkommen „-4 -4".
- ✅ **BUG Buff-Badge nicht grün (S78 → FIXED S79):** Badge nutzt jetzt semantische `badge_color` (`_modifier_color`/`color_hint`) statt `right_color` → Light Cover grün (`design_colors.md` §0, manuell bestätigt). Tests pinnen Buff=grün / Debuff=rot. Perspektiv-Frage durch §0 entschieden (Cover = Buff).
- 🔲 **Invuln-SAVE-Badge-Bereich chaotisch (S78):** Zeigt drei Teile („Inv 4+", „active", „AP/Cover N/A"), die teils keinen Sinn ergeben. Soll: **eine** klare Badge, z. B. „Invuln 4+". Überschneidet sich mit **Plan 017** (SAVE-Block Fähigkeit+AP kombinierte Badge) → dort mitlösen oder eigener kleiner Task.
- 🔲 **Dice-Display Modifier-Geometrie (Befund B/C, S78):** HIT/WOUND-**Debuff** spreizt nicht mit der Magnitude — `modifier_die_pair_html` zeigt immer `from-1 → from` (−1/−2/−3 sehen identisch aus), Spec §3.1 will den farbigen Würfel mit der Magnitude nach rechts wandern lassen. Zusätzlich verletzt HIT-**Buff** die Slot-1-Invariante (grauer Würfel rutscht auf Spalte 1, §3.3 will min. 2). SAVE-Geometrie ist korrekt. **Eigener Plan** (`modifier_die_pair_html` getestet → Regressionsfläche; eigenes Test-Netz). Die Pfeil-**Zahl** (Befund A) ist bereits umgesetzt (S78).
- 🔲 **Silent-King-Zielaufteilung Fernkampf (S79-UI-Befund; Regel S80 GEKLÄRT):** Ein Modell mit **zwei** Fernkampfwaffen (Silent King: Sceptre of Eternal Glory / Staff of Stars) kann aktuell nur **eine** Feind-Einheit als Ziel wählen — **regelwidrig**. Core Rules: „If a model has more than one ranged weapon, it can split the weapons between different enemy units." Alle Attacken **einer** Waffe gehen auf dieselbe Einheit. → UI auf **Ziel-pro-Waffe** umbauen + alle Ziele vor dem ersten Wurf deklarieren; Staff-of-Stars-Sperre ≤8 W beachten; Regressionstest. Detail: `docs/inbox/finding-silent-king-target-split.md`. Eigener Plan.
- 🔲 **Off-Scale-/„7+"-Save-Grenze (S79-UI-Befund):** Sv 7+ (z. B. Gretchin) bzw. durch AP jenseits 6 verschlechterte Saves brauchen einen „7-Augen"-Würfel **plus** Erfolgsgrenze `|`. Soll lt. Stakeholder: Kopfzeile `[6] | [✕]`; Cover-Randfall `[6] 1→[7]`; AP-Fall `[6] ←4 [✕]` (konsequente Fortschreibung der D5-Spec). → `docs/spec/dice_display.md` ergänzen, **alle** Fälle mit Tests. Verwandt mit Befund B/C.
- 🔲 **AP-/SAVE-Modifier-Magnitude-Position (S79-UI-Befund):** Die Magnitude-Zahl (`-N`/`←N`) gehört in die **Erfolgsgrenz-Spalte** unter `|` (Screenshot AP-2: „-2" unter die Grenze; Basis-AP: erwartetes `-`/Marker in Spalte Würfel „6"). → Spec prüfen, für **alle** Fälle (Buff/Debuff, HIT/WOUND/SAVE) Tests hinterlegen. Eng verwandt mit Befund B/C-Geometrie.
- 🔲 **Lethal Hits (R-CMB-XX, Refinement 2026-06-20):** Unmod. Treffer-6 = kein Wundwurf, Schaden direkt mit Overflow (wie Mortal Wounds). Nicht implementiert. Eigener Plan nach Plan 014.
- 🔲 **Deadly Demise (R-CMB-YY, Refinement 2026-06-20):** Modell zerstört → Mortal Wounds auf Einheiten in X". YAML-Daten vorhanden, Handler fehlt. Eigener Plan.
- 🔲 **Voice of the Triarch (R-CMD-XX, Refinement 2026-06-20):** Silent King — `voiceOfTheTriarch`-Handler fehlt (YAML-Basis fertig: `alter_command_protocol`). → Plan 016 oder eigener kleiner Plan.
- ✅ **Subagent-Archiv REWORK (Plan 023, DONE 2026-06-21):** overview.md schlank (18 KB→3.9 KB), Reihenfolge nach `overview_concept.md`; separate auto-generierte `session_archive.md` (Hauptzeile + SA-Subzeilen, dedup je Session-ID); Schema-Migration verlustfrei; tote Renderer entfernt; 1011 Tests grün. — _Ursprung:_ S72-Bug: Duplikat-Tabellen in `overview.md`. Fix: (1) `docs/metrics/session_archive.md` als separate, wachsende Archiv-Datei; (2) `overview.md` bekommt Link + SA-Peaks als Inline-Subzeilen im Verlaufsblock (Format: `Refinement/overview_concept.md`); (3) **Session-ID-Deduplizierung bei `--write`** — überschreibt `overview.md` während einer Session mehrfach, darf dieselbe Session-ID **nicht** doppelt ins Archiv anhängen (idempotent je Session-ID). Die **Anzahl der Auslösungen wird NICHT dokumentiert** (Stakeholder 2026-06-21). Render-Funktionen `_render_subagent_archive` + `_render_subagents` zusammenführen; die breite Tabelle „## Subagenten — wer wurde wofür gestartet" entfällt komplett.

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

- ✅ **Dice Display Arrow-Direction-Bug (`dice_html.py`)** — erledigt (Plan 022, S77): `rightward = (value > 0)` in `dice_compose.py`, Buff=rechts[→]/Debuff=links[←]; Tests `test_buff_arrow_points_right`/`test_debuff_arrow_points_left` pinnen das Verhalten.
- ✅ **commandPhase.py State-Keys nicht orb-id-gebunden** — erledigt (Plan 020, S83): globale Slots durch `pending_target_request` mit `TargetSelectionRequest.ability_id`-Diskriminator ersetzt; `revive_wargear_awaiting_target` existiert nicht mehr in `src/`.
- **Mortal Wounds Text-Match-Erkennung:** `_detect_weapon_special` nutzt `"mortal wound" in abilities.lower()` — kein strukturiertes YAML-Feld. Technische Schuld, kein akuter Block.

## 5. Größere geplante Ziele

- [ziel7.md](ziel7.md) — Crusade-Erweiterung (geplant)
- [ziel8.md](ziel8.md) — Wahapedia Faction Fetcher (geplant)
- [index.md](index.md) — Ziel-Gesamtübersicht 1–8

---

## Wo was steht (Artefakt-Verweise)

| Frage | Artefakt |
|---|---|
| Was mache ich als Nächstes? | [next_session.md](../../.claude/tasks/next_session.md) |
| Was ist insgesamt offen? | **dieser Index** |
| Detailplan eines Features? | [../audit/plans/](../audit/plans/) |
| Architektur-Bild + Invarianten? | [../spec/architecture.md](../spec/architecture.md) · [../spec/architecture_invariants.md](../spec/architecture_invariants.md) |
| Ziel-Historie / Changelog? | [ziel6.md](ziel6.md) „Session-Historie" |
