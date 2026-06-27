# Plan 025 — Command Protocols auf echte 9E-Direktiven bringen

## Status

- **Priority**: P1 (HOCH) — blockiert die Anzeige-Pläne 016/017, die auf dem
  bisherigen (nicht-kanonischen) Direktiv-Modell aufsetzen.
- **Effort**: L (sechs Protokolle, mehrere neue Engine-Effekt-Typen).
- **Depends on**: 024 ✅ (Directive-Wiring-Infrastruktur steht).
- **Risk**: MITTEL — verändert verdrahtete + getestete Effekte; jeder Schritt ist
  ein eigener Freigabe-Punkt, Vollsuite nach jedem Daten-/Verhaltens-Step.

## Update S97 (2026-06-25) — Reklassifikation D1, Anzeige als Pflichtteil

Beim Scoping von Step 2 (Hungry Void) zwei strukturelle Befunde + Konsens-Entscheide:

1. **Combat ist zähl-basiert** (`resolve_attack(... wounds_rolled: int ...)` — *player-provided
   dice counts*, `combat.py:86-94`). Die App sieht **nie einzelne Würfelaugen**. Damit ist
   `ap_on_unmod_wound_6` (Hungry D1, später Vengeful D1) **nicht** als A-Effekt abbildbar →
   **Konsens: D1 Hungry + Vengeful von A → B reklassifiziert** (Tisch-Hinweis). Eine
   Pro-Würfel-Umstellung wäre ein eigener großer Plan (vom Stakeholder vorerst nicht gewollt).
2. **Latente Drift (S97):** `strength_modifier`/`ap_bonus` sind in der Engine gemappt **und
   getestet** (`get_active_round_choice_modifier` → `{"strength":1}`/`{"ap":-1}`), werden aber
   in `_collect_atk_modifiers`/`_collect_def_save_modifiers` (`_common.py:440/498`) **nie
   konsumiert** → die aktuellen Hungry-S/Vengeful-S-Effekte wirken im Kampf **gar nicht**. Die
   `backlog.md`-§0-Tabelle „Engine ✅" ist insoweit irreführend (liefert Wert ≠ Konsument liest ihn).

**Konsens-Entscheide (S97):**
- **Step 2 (Logik):** Hungry D1 → `ap_on_unmod_wound_6` (phase melee, **B**); D2 →
  `strength_if_charged` (value 1, phase melee, **A**). D2 braucht ein neues `was_charged`-Flag
  (`set_charged` markiert bisher nur den Charger; `turn_flags` kennt `charged`/`heroic_intervened`,
  nicht „was charged"). Neue pure Engine-Fn `get_active_round_choice_strength_if_charged`; Konsum
  in `_common.py` Strength-Berechnung (repariert nebenbei den toten `strength`-Pfad).
- **Step 2b (Anzeige) — NEU, eigener Freigabe-Punkt direkt nach Step 2:** generischer
  **Direktiv-Hinweisblock**, der **jede** aktive Direktive zeigt (A wie B), datengetrieben aus
  den YAML-`primary`/`secondary`-Texten. Neues YAML-Feld **`enforcement: app|table`** je
  `effect` (deckt sich mit A/B/C-Katalog); pure Fn `directive_hints(player, use_melee) ->
  [{text, enforced}]`; Render als Caption im Attacken-Block (konsistent zu `_rp_directive_hints`):
  `✓ … — von der App angewandt` / `⚠ … — am Tisch anwenden`. `enforcement` wird **nur** für die
  schon-9E-konformen Direktiven gesetzt (Sudden Storm, Undying Legions, Hungry Void); die noch
  erfundenen (Vengeful/Eternal/Conquering) bekommen es in ihren Steps 3-5 → erscheinen erst dann
  im Block (keine falsche Anzeige). **Sammelt die verschobene Sudden-Storm-B-Hint-Schuld (Step 1)
  mit ein.**
- **DoD-Ergänzung (verbindlich ab jetzt):** **Anzeige ist Pflichtteil JEDES 025-Steps** — kein
  Verschieben von Render auf „später/Backlog". Jeder neue/geänderte Effekt nennt seine Anzeige.

**Design-Korrektur S98 (Stakeholder):** Der separate **Caption-Hinweisblock** aus Step 2b wurde
für die kampf-relevanten Direktiven **verworfen**. Stattdessen werden Direktiv-Effekte ins
bestehende **Dice-UI-Vokabular** integriert: numerische Buffs wie WAAAGH (S blau im WOUND-Block),
trigger-bedingte Effekte als eigene Würfelzeile mit Symbol in der Auslöser-Spalte
(`value_triggered_die_row_html`, z. B. `[AP-1]` in der 6er-Spalte). Step 2b als Caption-Block
entfällt damit; sein Rest-Anliegen (reine B-Tisch-Hinweise wie **Sudden Storm S**, die keine
Würfel-Mechanik haben) bleibt offen und wird gesondert gelöst (nicht als Caption-Sammelblock).
Begründung Stakeholder: Konsistenz „wie jeder andere Buff" + Bedarf nach echtem Design-System.

> Der generische Hinweisblock ist die Wurzel-Lösung für die aufgelaufenen 🔲-Anzeige-Lücken
> in `backlog.md` §0 #2 (Reroll-Save-Hinweis, S+1-WOUND, AP-im-SAVE …) — diese werden über
> `enforcement` Schritt für Schritt vom Block abgedeckt statt einzeln nachgezogen.

## Decision (Konsens, S95)

Der Stakeholder hat entschieden: **Variante (b)** — die in
`data/wh40k_9e/necrons/faction_abilities.yaml` modellierten Command-Protocol-
Direktiven werden auf die **echten 9E-Regeln** (`docs/work/wahapedia_necrons/
faction_overview.txt` Z. 583–716) umgestellt. Das bisherige Modell war eine
vereinfachte, nicht-kanonische Fassung (S95-Befund, `backlog.md` §4b). Kein
separater ADR — die zugrunde liegende Regel „gegen Wahapedia prüfen, nicht aus
dem Gedächtnis" steht bereits in CLAUDE.md DoD #1; dieser Plan ist die Umsetzung
des konkreten Daten-Entscheids.

## Why this matters

Die App rechnet/erzwingt Direktiv-Effekte, die es im 9E-Regelwerk nicht gibt
(z. B. Eternal Guardian „+1 Save", Conquering Tyrant „+1 Leadership"). Das ist
ein Regelkonformitäts-Bruch (DoD #1) und macht jede darauf aufbauende Anzeige
(Plan 016 Group A/C) falsch. Erst nach (b) sind 016/017 sinnvoll.

## Rule-check — alle 6 Protokolle (9E vs. bisheriges YAML)

| Protokoll | YAML P / S (alt) | 9E Direktive 1 / 2 (kanonisch) | Befund |
|---|---|---|---|
| **Eternal Guardian** | save +1 / reroll save 1 | Light Cover wenn nicht bewegt / Hold Steady·Set to Defend bei gegner. Charge | beide erfunden |
| **Sudden Storm** | +1" Move / advance+charge | +1" Move / Aktion + Ranged-Angriff erlaubt | **P konform**, S erfunden |
| **Vengeful Stars** | wound +1 (Sh) / AP −1 (Sh) | unmod Wound-6 → AP+1 (ranged) / kein Cover ≤ halbe Reichweite | beide erfunden |
| **Hungry Void** | hit +1 (Sh) / str +1 (Sh) | unmod Wound-6 → AP+1 (**melee**) / charged·charge·HI → +1 S (melee) | beide erfunden |
| **Undying Legions** | rp_reroll / heal+1 Living Metal | Living Metal +1 / RP reroll one die | **substanziell konform** (P/S vs. D1/D2 vertauscht) |
| **Conquering Tyrant** | leadership +1 / reroll hit&wound melee | +3" Aura-Reichweite / nach Fall Back schießen (−1 Hit) | beide erfunden |

## Effekt-Klassen (Akzeptanz-Katalog A/B/C)

- **A (App rechnet/erzwingt):** Light Cover bedingt (Eternal D1), +1" Move
  (Sudden Storm D1, schon da), AP+1 auf unmod Wound-6 ranged/melee (Vengeful D1,
  Hungry D1), kein Cover ≤ halbe Reichweite (Vengeful D2), bedingtes +1 S melee
  (Hungry D2), Fall-Back-Schuss −1 Hit (Conquering D2), Living Metal +1 / RP-
  reroll (Undying, schon da).
- **B (nur am Tisch prüfbar → App zeigt Hinweis):** Hold Steady/Set to Defend
  (Eternal D2), Aktion + Ranged erlaubt (Sudden Storm D2), +3" Aura-Reichweite
  (Conquering D1).
- Neue Engine-Effekt-Typen, die A braucht: `light_cover_if_stationary`,
  `ap_on_unmod_wound_6` (Parameter: phase ranged/melee), `ignore_cover_half_range`,
  `strength_if_charged` (melee), `shoot_after_fall_back` (mit Hit-Malus).

## Scope (betroffene Dateien)

- `data/wh40k_9e/necrons/faction_abilities.yaml` — alle 6 Protokoll-`effect`-Blöcke
  + `primary`/`secondary`-Beschreibungstexte auf 9E.
- `src/gameMechanic/ability_engine.py` — neue Effekt-Typ-Behandlung + `_REROLL_*`/
  Modifier-Maps anpassen (alte erfundene Flags entfernen).
- `src/gameMechanic/combat.py` / `src/uiLayout/_common.py` — Konsum der neuen
  A-Effekte (Cover-Grant, AP-on-6, bedingte S).
- `tests/gameMechanic/test_ability_engine.py` + `tests/uiLayout/test_common.py` —
  Tests der alten erfundenen Effekte ersetzen; neue Effekt-Tests.
- `docs/spec/acceptance/rules.md` — neue Direktiv-Regeln als A/B-Einträge.
- `docs/goals/backlog.md` §0 + §4b — Direktiv-Tabelle + Befund nachziehen.

## Steps (je Step = eigener Freigabe-Punkt, Vollsuite danach)

> Reihenfolge: erst die **schon konformen** Protokolle verifizieren/relabeln (klein,
> risikoarm), dann die A-Effekte (neue Engine-Typen), zuletzt die reinen B-Hinweise.

1. **Sudden Storm + Undying Legions — verifizieren & relabeln (XS).** Beide
   substanziell konform. Sudden Storm S (`advance_and_charge`) → echtes D2
   (Aktion + Ranged); P/S-Labels von Undying Legions an D1/D2-Nummerierung
   angleichen. Keine neuen Engine-Typen außer Sudden Storm D2 (B-Hinweis).
2. ✅ **DONE (S98) — Hungry Void.** D1 `ap_on_unmod_wound_6` (melee, **Klasse B** —
   Combat zähl-basiert, Tisch-Hinweis als `[AP-1]`-Zeile im WOUND-Block via neuem
   `value_triggered_die_row_html`). D2 `strength_if_charged` (melee, **Klasse A**) über
   neues `was_charged`-Flag (`turn_flags`-Init + `set_charged` markiert Ziel) + Engine-Fn
   `get_active_round_choice_strength_if_charged`; +1 S in `str_bonus` gefaltet → S blau im
   WOUND-Block wie WAAAGH. Test-Migrationen (Hungry-Vehikel-Tests → Vengeful/dedizierte
   Fns) + neue Engine-/Dice-Tests. 1144 grün, 93,18 %. Anzeige = Pflichtteil erfüllt.
3. ✅ **DONE (S99) — Vengeful Stars.** D1 `ap_on_unmod_wound_6` (**ranged, Klasse B** —
   teilt Logik/Anzeige mit Step 2; bereits phasen-generisch verdrahtet → nur YAML-Tausch
   + Verifikationstest, `[AP-1]`-Zeile im Schuss-WOUND-Block). D2 `ignore_cover_half_range`
   (**Klasse B/Hybrid** — halbe Reichweite ist Tischmessung) über neue Engine-Fn
   `get_active_round_choice_ignores_cover_half_range` + reine Label-Fn `light_cover_label`:
   grüne `:green-badge`-Inline-Anzeige an der Light-Cover-Checkbox (Häkchen bleibt manuell).
   Tot-Pfad `ap_bonus` ersetzt. 1150 grün / 93,16 %. Anzeige = Pflichtteil erfüllt;
   manuelle UI-Verifikation offen (s. u.).
   - **Test-Migration (Sicherheitsnetz):** `test_ability_engine.py` (Primary `{"wound":1}`
     → `{}` + dedizierte AP-on-6-Fn; Secondary `ap_bonus` → `ignore_cover_half_range`)
     **und** `tests/gameMechanic/test_round_choice_player_keyed.py` — zwei Mirror-Match-
     Tests prüften Vengeful-Primary noch als `{"wound":1}`; migriert auf `{}` +
     player-keyed `get_active_round_choice_ap_on_wound_6(..., use_melee=False)==1` (+ neuer
     Secondary-Mirror-Test für `ignore_cover_half_range`). (Nachgetragen S99.)
4. **Eternal Guardian — nur D1 (S102-Entscheid).** `light_cover_if_stationary` (Klasse A):
   bei `movement_choice == "stationary"` erhält die Einheit Light Cover; Anzeige Variante C
   (Checkbox bleibt, bei D1 aktiv + stationär vorgehakt + disabled; Badge via
   `light_cover_label`-Muster). **Nur im Shooting-Block** (A1: Fight-SAVE-Block als
   Backlog-Notiz). Detail-Plan in Mailbox: `docs/handoff/plan-025-step4.md` Teil A → vom
   **Executor-Subagent** umsetzen lassen.
   **D2 herausgeschnitten (B1):** Hold Steady (Overwatch 5+ statt 6) / Set to Defend
   (+1 Hit im nächsten Fight) = eigener Plan, abhängig Plan 015 (Overwatch). YAML-Übergang
   (B2): `type: hold_steady_or_set_to_defend, phase: any, enforcement: table` + TODO-Kommentar
   mit Verweis auf D2-Plan + 9E-Sekundärtext (ersetzt erfundenes `reroll_save_1`). D2-Plan
   deckt beide Hälften (B3); Hold-Steady-Hälfte hängt an Plan-015-Overwatch, Set-to-Defend
   ist ein Fight-+1-Hit-Modifier; Vermerk in Plan 015 ergänzt.
5. **Conquering Tyrant (A + B).** D1 +3" Aura = B-Hinweis, D2 `shoot_after_fall_back`
   (−1 Hit) = A. Engine + Phasen-Konsum + Tests.
6. **Aufräumen + Akzeptanz-Katalog.** Alte erfundene Effekt-Typen (`save_modifier`
   als Direktive, `leadership_bonus`, `reroll_save_1`, `reroll_hit_wound_1`,
   `hit_modifier`/`strength_modifier` als Protokoll, `wound_modifier`/`ap_bonus`
   als Protokoll) aus Engine/Tests entfernen, sofern kein anderer Konsument bleibt;
   `rules.md` + `backlog.md` nachziehen; Lint.

## Supersedes / Auswirkung auf andere Pläne

- **Plan 016 Group A** (Eternal Guardian S / Conquering Tyrant S Reroll-Hints) und
  **Group C Conquering Tyrant P Morale** werden **obsolet** — diese Effekte
  verschwinden. 016 behält nur den **RP-Block-Hint + Dynastiebonus-Anzeige**
  (Undying Legions — konform). Group C **Sudden Storm P Move-Badge** bleibt gültig.
- **Plan 017** (SAVE-AP-Badge) muss die neuen AP-on-6-Effekte mitdenken.

## Test plan

- **Scoping-Pflichtschritt vor jedem Daten-Step (S99-Lehre):** `grep -rn "<alter_effekt_typ>" tests/`
  über den zu ersetzenden Effekt-Typ laufen lassen → ALLE Testdateien in die Migrationsliste
  aufnehmen (Step 3 verfehlte `test_round_choice_player_keyed.py`, weil die Liste unvollständig war).
- Pro Step: neue Effekt-Tests (Engine + ggf. HTML-Output/Hint), dann **Vollsuite**
  `pytest --tb=short` (nicht nur `-k`), Coverage ≥ 90 %, Architektur-Gate grün.
- Jeder ersetzte erfundene Effekt: alter Test wird zum neuen Verhalten migriert
  (im Step explizit als „erwartete Test-Migration" auflisten — Sicherheitsnetz-Regel).

## Done criteria

- [x] Alle 6 Protokolle: `primary`/`secondary` + `effect` = 9E-Direktiven.
- [x] Keine erfundenen Direktiv-Effekt-Typen mehr in `src/`/Tests ohne Konsument.
- [x] Neue A-Effekte engine-seitig verdrahtet + getestet; B-Effekte als Hinweis.
- [x] `rules.md` + `backlog.md` §0/§4b aktuell; INV-4b grün.
- [x] Manuelle UI-Verifikation je A-Effekt benannt (Render-Code).
- [x] README-Status-Zeile aktualisiert.

## STOP conditions

- Vorher grüner Test wird rot und steht nicht in der Step-Migrationsliste → STOP, fragen.
- Neue UI-Elemente (Badges/Hinweise) → erst Kurz-Mockup zeigen, Freigabe abwarten.
- Eine 9E-Direktive ist mechanisch nicht eindeutig abbildbar → STOP, Layout/Scope klären.
