STATUS: NEEDS-DECISION

# S136 Aufgabe 3 — 4c-Befund (c): Command Re-Roll in Hit/Wound/Save (Stufe 1, Investigation)

Bezug: `docs/handoff/S136_plan.md` Aufgabe 3, Stakeholder-Befund 4c(c),
`docs/spec/acceptance/rules.md` R-CMD-12, `docs/spec/design_system.md` §6.2/§6.3.
Effort-Deckel M, reines Investigations-Ergebnis — **kein Code geändert**.

## Regelwortlaut (core_rules.txt Z. 3124-3130, wörtlich)

> COMMAND RE-ROLL — 1CP — Core Stratagem — Use this Stratagem after you have
> made a hit roll, a wound roll, a damage roll, a saving throw, an Advance
> roll, a charge roll, a Psychic test, a Deny the Witch test or you have
> rolled the dice to determine the number of attacks made by a weapon.
> Re-roll that roll, test or saving throw.

→ 9 Wurf-Arten. „cannot use the same Stratagem more than once in the same
phase" (allgemeine Stratagem-Regel, nicht Command-Re-Roll-spezifisch) — 1 CP,
einmal pro Phase, `player: both`. YAML: `data/wh40k_9e/_shared/stratagems.yaml:11-22`
(`phase: [movement, psychic, shooting, charge, fight]`, `event: after_roll`,
`effect.type: reroll`, kein `effect.stat` — greift generisch für jeden
`after_roll`-Anker, unabhängig davon welcher Wurf gemeint ist).

## Befund b) — R-CMD-12: 9 Stellen, Ist-Stand korrigiert auf 6/9 (nicht 4/9)

`rules.md` R-CMD-12 (Z. 399-405) zählt aktuell **4 verdrahtet / 5 offen** und
listet Advance- und Charge-Wurf unter „offen". Das ist **veraltet** — Code-Prüfung
zeigt beide sind bereits seit S130/S133 verdrahtet und getestet:

| # | Wurf-Art | Status | Fundstelle | Test |
|---|---|---|---|---|
| 1 | Damage-Wurf | ✅ verdrahtet | `_common.py:1399` `render_reactive_stratagem_box(effect_type="reroll")` | `test_damage_block_offers_command_reroll_after_apply` |
| 2 | Psychic Test (Manifest) | ✅ verdrahtet | `psychicPhase.py:191` | `test_manifest_reroll_offered_when_failed` |
| 3 | Deny the Witch | ✅ verdrahtet | `psychicPhase.py:528` | `test_deny_reroll_offered_when_deny_roll_was_made` |
| 4 | Anzahl-Attacken-Wurf | ✅ verdrahtet | `_common.py:2451` `render_inline_command_reroll` (S135 Paket 4c) | `test_render_group_assignment_offers_command_reroll_on_attack_count` |
| 5 | **Advance-Wurf** | ✅ verdrahtet (in rules.md fälschlich als „offen" geführt) | `movementPhase.py:245-288` `_render_advance_reroll_card` (S133 K2 item 1, `render_go_card` direkt, kein Wertfeld — bewusste §6.3-Ausnahme) | `tests/gameMechanic/test_movement_transitions.py:493-536` (5 Tests) |
| 6 | **Charge-Wurf** | ✅ verdrahtet (in rules.md fälschlich als „offen" geführt) | `chargephase.py:114` `render_inline_command_reroll(faction, "charge", reopen_key=uid, on_reroll=lambda: None)` (S130 Plan 015 Option c) | generische `render_inline_command_reroll`-Tests (`test_common.py:1347ff`) decken den Mechanismus; Aufrufstelle selbst ungetestet — kleine Test-Lücke, nicht Teil dieses Befunds |
| 7 | **Hit-Wurf** | ❌ offen | `_common.py:1821` `_render_dice_roll_block("HIT", ...)` — reine Schwellenanzeige | — |
| 8 | **Wound-Wurf** | ❌ offen | `_common.py:1847-1854` `_render_dice_wound_block` — reine Schwellenanzeige | — |
| 9 | **Save-Wurf** | ❌ offen | `_common.py:1873` `_render_dice_save_block` — reine Schwellenanzeige | — |

**Tatsächlich offen: nur 3 von 9** (Hit/Wound/Save), nicht 5. `rules.md` braucht
eine Korrektur (Doku-Drift, CLAUDE.md-Pflicht „Widerspricht Code einer Spec,
ist das ein Befund"). Vorschlag: Teil des Stufe-2-Briefs (kleine Nebenarbeit).

## Befund a) — Reopen-Mechanik: uneinheitlich, zwei Familien (bestätigt)

Der Planner-Verdacht trifft zu — es gibt **zwei** Familien, keine einheitliche:

**Familie 1 — GO-Karte mit echtem Wertfeld ("Push", `render_reactive_stratagem_box`, `effect_type="reroll"`):**
Damage-Wurf (`_common.py:1399`), Psychic Test (`psychicPhase.py:191`), Deny the
Witch (`psychicPhase.py:528`). Der Wert steht in einem `applied`-gesperrten
Feld; `on_resolved` poppt die Sperre, das Feld wird neu editierbar. Passt nur
dort, wo die App den Tischwurf tatsächlich als Zahl erfasst.

**Familie 2 — Inline-Button ohne Sperre ("Pull", `render_inline_command_reroll`, `on_reroll` No-op oder trivial):**
Anzahl-Attacken (`_common.py:2451` — Feld bleibt vor „Group done" ohnehin
editierbar, `on_reroll=lambda: None`), Charge-Wurf (`chargephase.py:114`,
echter No-op — die App erfasst gar keinen Zahlenwert für den Charge-Wurf,
nur `in_melee`-Flag), Advance-Wurf (`movementPhase.py:245`, eigene
Variante mit `render_go_card` direkt statt der generischen Helper-Funktion,
aber gleiches Prinzip: kein Wertfeld, reines CP-Buchungs-Angebot).

Design_system.md §6.3 nennt Familie 2 explizit als **bewusste Ausnahme**
(„Gegenbeispiel — Advance/Charge: Diese Wurf-Arten haben KEINE Werterfassung").
Für Hit/Wound/Save gilt dasselbe: `_render_dice_roll_block`/`_render_dice_wound_block`/
`_render_dice_save_block` zeigen nur Schwellenwert + Würfelbild (Wahrscheinlichkeits-
Referenz für den Tischwurf), es gibt **keinen** `number_input` für den tatsächlich
gewürfelten Wert — geprüft per Volltext-Suche in der gesamten `_render_resolution_tab`
(`_common.py:1588-1942`): der einzige `number_input`/erfasste Wert in der ganzen
Attackenauflösung ist der finale Damage-Wert im Damage-Block. Damit gehören
Hit/Wound/Save strukturell zu **Familie 2**, nicht zu Familie 1 — es gibt nichts
zum Wiedereröffnen.

**Wichtige Doku-Spannung (kein Widerspruch, aber präzisierungsbedürftig):**
`design_system.md` §6.3 nennt Hit/Wound/Save/Save/Damage („Treffer / Verwundung /
Rüstung / Rettung / Schadenszuweisung") als Stellen, die „so je einen Anker"
bekommen — liest sich wie der volle Familie-1-Baustein. Das ist aber nur für
Damage bereits so umgesetzt; für Hit/Wound/Save fehlt nicht nur der Anker,
sondern die Werterfassung selbst (ein deutlich größerer Umbau als „Button
ergänzen"). `processes.md` P-14 („Spieler gibt Hits/Wounds/Saves ein") ist
in der Praxis eine vereinfachte Flowchart-Beschriftung des Gesamtschritts,
kein Beleg für separate Zahlenfelder pro Hit/Wound/Save — Code-Check bestätigt:
es gibt sie nicht.

## Befund c) — CP/Once-per-Phase-Erzwingung: vollständig generisch, wiederverwendbar

`spend_stratagem()` (`_common.py:433`) schreibt zentral in
`st.session_state.used_stratagem_ids[faction]`. Beide Familien lesen daraus:
`render_reactive_stratagem_box` (`_common.py:721`) und
`render_inline_command_reroll` (`_common.py:801`) — beide filtern über
`stratagem_visibility()` (`gameObjects/stratagem.py:119`), die `used_ids` +
`phase` gemeinsam prüft. Keine neue Buchungslogik nötig — ein dritter Aufrufer
(Hit/Wound/Save) bekommt „1 CP, einmal pro Phase" automatisch korrekt, exakt
wie die bereits verdrahteten 6 Stellen.

## Befund d) — Kollision mit dem parallel laufenden 4c-a/b-Umbau: keine Zeilenüberlappung

`git diff --stat` (Stand dieser Untersuchung) zeigt unkommittete Änderungen in
`src/uiLayout/_common.py` (11 Zeilen) — ausschließlich in `render_group_assignment`
(Import `_is_variable_attacks` Z. 28-35, Reroll-Sichtbarkeits-Gate Z. 2444-2453).
Das liegt **weit entfernt** von `_render_resolution_tab` (Z. 1588-1942, hier
relevante Blöcke Z. 1821/1847-1854/1873) — keine Zeilenkonflikte. Zusätzlich
liegt `docs/handoff/S136_4c_platzierung.md` (Aufgabe 2, Teil a) vor: dort
wurde die „mehrere Anker pro Ziel"-Frage **bewusst an diese Untersuchung
delegiert** („dort wird über mehrere Anker/Reopen-Mechanismen grundsätzlich neu
entschieden"). Antwort aus diesem Befund: Hit/Wound/Save brauchen **keine**
Mehrfach-Anker-Struktur — ein Anker pro Block reicht (analog Charge/Advance,
nicht analog Anzahl-Attacken, das pro Waffe×Ziel mehrfach vorkommt). Für
Aufgabe 2 heißt das: Option A (waffen-äußere Vor-Iteration) ist **nicht**
durch diesen Befund erzwungen — Option B bleibt die einfachere, konsistente
Wahl für beide Aufgaben.

---

## Umsetzungsvorschlag Stufe 2 (Brief-Skizze)

**Ansatz:** pragmatisch, Familie 2 (Analogie Advance/Charge) — **kein**
neuer Tisch-Wurf-Eingabe-Baustein für Hit/Wound/Save. Grund: die App erfasst
diese Würfe grundsätzlich nicht (reine Schwellenanzeige); ein echter
Wertfeld-Umbau wäre ein eigenständiges, deutlich größeres Feature (Neugestaltung
der ganzen Auflösung von „Wahrscheinlichkeits-Referenz" zu „Würfe eintragen"),
keine Command-Re-Roll-Nachbesserung. Diese Wahl ist die erste Entscheidungsfrage
unten.

**Betroffene Dateien:**
- `src/uiLayout/_common.py` — drei `render_inline_command_reroll(...)`-Aufrufe:
  - nach `_render_dice_roll_block("HIT", ...)` (Z. 1821), Zahler `atk_faction`
    (Angreifer würfelt den Hit-Wurf), `reopen_key=f"{tab_key}_hit"`
  - nach `_render_dice_wound_block(...)` (Z. 1847-1854), Zahler `atk_faction`
    (Angreifer würfelt den Wound-Wurf), `reopen_key=f"{tab_key}_wound"`
  - nach `_render_dice_save_block(...)` (Z. 1873), Zahler `def_faction`
    (Verteidiger würfelt die Rettung), `reopen_key=f"{tab_key}_save"`
  - `phase_key`-Parameter ist bereits vorhanden (Funktionsparameter), keine
    neue Herleitung nötig. `on_reroll=lambda: None` (kein gesperrter Wert,
    analog Charge).
- `docs/spec/acceptance/rules.md` — R-CMD-12 korrigieren: Ist-Stand vor
  Umsetzung auf „6/9 verdrahtet, 3 offen" richtigstellen (Doku-Drift-Fix),
  nach Umsetzung auf „9/9".
- `docs/spec/design_system.md` §6.2 — „Mit Anker erreichbar"-Liste (Z. 245)
  ergänzen (Hit-/Wound-/Save-Command-Re-Roll jetzt vollständig erreichbar,
  keine offene GO-Fensterfrage mehr für Command Re-Roll insgesamt).
- Neue/erweiterte Tests: `tests/uiLayout/test_common.py` — 3 neue Tests nach
  bestehendem Muster (`test_render_group_assignment_offers_command_reroll_on_attack_count`
  als Vorlage): `test_render_resolution_tab_offers_command_reroll_on_hit_roll`,
  `..._on_wound_roll`, `..._on_save_roll` — inkl. Zahler-Assertion
  (atk_faction bei Hit/Wound, def_faction bei Save).

**Testplan (4-Schichten-Mandat):**
1. Business-Logik: die 3 neuen Tests oben (Sichtbarkeit, CP-Abzug, korrekter
   Zahler, „einmal pro Phase" via geteiltem `used_stratagem_ids`).
2. Render-Code-HTML-Test: nicht separat nötig — `render_inline_command_reroll`
   ist bereits in `_common.py` (Business-Logik-Modul, nicht `*Phase.py`/`uiLayout`-
   Render-Ausschluss) und wird per Streamlit-AppTest/Mock wie die 4 bestehenden
   Aufrufer getestet — kein neuer HTML-Output-Test-Typ.
3. Architektur-Gate: `pytest tests/architecture/ --no-cov -q` — keine neue
   Cross-Layer-Verletzung erwartet (gleiche Funktion, gleiches Modul).
4. Regel-Akzeptanz: `rules.md` R-CMD-12 auf 9/9 nachziehen, neue Testnamen
   eintragen (s. o.).

**Effort-Schätzung: S, kein Split nötig.** Ursprünglicher M-Deckel war auf die
befürchtete Uneinheitlichkeit (5 Stellen, neue Mechanik) ausgelegt — Befund
zeigt: 3 Stellen, gleiche Funktion, bereits existierendes Muster (Familie 2),
keine neue (phase, event)-Fensterinfrastruktur nötig (`after_roll` existiert
in shooting/fight bereits). Grobe Schätzung: ~12-15k Token (3× mechanisch
identischer Call + 3 Tests + 2 Doku-Zeilen).

---

## Entscheidungsfragen an den Stakeholder

1. **Ansatz bestätigen:** pragmatische Variante (Inline-Button ohne Wertfeld,
   Familie 2, analog Advance/Charge) statt Vollausbau (echtes
   Tisch-Wurf-Eingabefeld für Hit/Wound/Save, das die App bisher nirgends
   hat)? Vollausbau wäre ein eigenständiges, deutlich größeres Feature —
   Empfehlung: pragmatisch, wie oben skizziert. - Ja, wir nehmen den pragmatischen ANsatz.
2. **Doku-Korrektur mitnehmen:** `rules.md` R-CMD-12 von „4/9 verdrahtet,
   5 offen" auf den korrekten Ist-Stand „6/9 verdrahtet, 3 offen" (vor
   Umsetzung) richtigstellen — als Teil desselben Stufe-2-Briefs? - Ja, auf jeden Fall
3. **UI-Ort:** Bestätigst du die Platzierung des Inline-Buttons direkt unter
   dem jeweiligen Block (Hit/Wound/Save), analog zum bestehenden Muster bei
   Charge (`chargephase.py:114`, Button direkt nach dem Wurf-Hinweis) — oder
   bevorzugst du eine andere Position (z. B. alle drei gebündelt am Ende des
   Blocks statt je einzeln)? - Ja. 

---

## Selbstprüf-Checkliste

- [x] Regelwortlaut Command Re-Roll aus core_rules.txt zitiert (Z. 3124-3130)
- [x] R-CMD-12: alle 9 Stellen benannt, Ist-Stand korrigiert auf 6 abgedeckt
      (Damage, Psychic Test, Deny the Witch, Anzahl-Attacken, Advance, Charge)
      vs. 3 fehlende (Hit, Wound, Save) — rules.md-Text war veraltet
- [x] Reopen-Mechanik-Befund mit Datei:Zeile (zwei Familien, Hit/Wound/Save
      gehören strukturell zu Familie 2, kein Wertfeld vorhanden)
- [x] Kollisionscheck mit 4c-a/b durchgeführt (`git diff --stat`, keine
      Zeilenüberlappung; Aufgabe-2-Delegation an diese Untersuchung beantwortet)
- [x] Handoff geschrieben, Zeile 1 = NEEDS-DECISION
