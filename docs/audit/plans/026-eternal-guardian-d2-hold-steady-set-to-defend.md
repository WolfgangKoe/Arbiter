# Plan 026 — Eternal Guardian D2: Hold Steady / Set to Defend

## Status

- **Priority**: P2 (MITTEL) — Regelkonformität Eternal Guardian vollständig abschließen
- **Effort**: M (zwei Mechanik-Hälften; single branch, zwei bis drei Commits)
- **Risk**: MITTEL — greift in Charge-Phase-Fenster und Fight-Phase-HIT-Block ein; Abhängigkeit an Plan 015 muss stehen
- **Depends on**: 025 ✅ (D2-YAML-Übergang steht, Korrekt-9E-Sekundärtext), **015 (ZWINGEND — Overwatch-Infrastruktur und Charge-Reaktiv-Fenster; Hold-Steady-Hälfte ohne Plan 015 nicht implementierbar)**
- **Category**: feature (Regelkonformität — Eternal Guardian D2)
- **Planned at**: 2026-06-26 (aus Plan 025 Step 4 B1-Entscheid / Handoff plan-025-step4.md Teil B)

---

## Abhängigkeitskette

```
Plan 025 Step 4 (D1 light_cover_if_stationary) ✅
        │
        └─► Plan 026 (D2 Hold Steady / Set to Defend)
                    │
                    ├─ Hold Steady (Overwatch 5+)
                    │      └─► HÄNGT AN Plan 015 Overwatch-Infrastruktur
                    │          (Charge-Reaktiv-Fenster + overwatch-Flag im HIT-Block)
                    │
                    └─ Set to Defend (+1 Hit nächste Fight Phase)
                           └─► Braucht Fight-Phase-Modifier + Persistenz-Logik
                               (in Plan 015 Z. 85 explizit out-of-scope;
                               hier erstmals implementiert)
```

**Kurzfassung:** Plan 015 baut die Overwatch-Infrastruktur (Charge-Reaktiv-Fenster, `overwatch`-Flag,
HIT-Block-Threshold). Plan 026 dockt darauf an: Hold Steady senkt die Schwelle 6→5+; Set to Defend
fügt einen persistenten +1-Hit-Modifier für die nächste Fight Phase hinzu.

---

## Why this matters

Nach Plan 025 Step 4 ist Eternal Guardian D1 (`light_cover_if_stationary`) vollständig
implementiert. D2 (Hold Steady / Set to Defend) bleibt vorerst als `enforcement: table`
(Tisch-Hinweis) mit TODO-Kommentar im YAML (`faction_abilities.yaml` Z. 63–71). Das ist ein
bewusster Übergangszustand: die YAML-Texte sind korrekt (9E-Wortlaut), aber die Engine hat
keinen Konsumenten. Dieser Plan beschreibt, wie der Übergangszustand auf echte Effekttypen
(`overwatch_hit_threshold` / `hit_bonus_next_fight`) migriert wird — sobald Plan 015 steht.

---

## 9E-Regeltext (verbatim)

Quelle: `docs/work/wahapedia_necrons/faction_overview.txt`

**Directive 2 (Z. 600–631):**

```
Directive 2: Each time an enemy unit declares a charge against this unit, if this unit is
not within Engagement Range of any enemy units, it can either Hold Steady or Set to Defend.
If it Holds Steady, then until the end of the phase, any Overwatch attacks made by models
in that unit score hits on unmodified rolls of 5+, instead of 6.
If it Sets to Defend, then until the end of the phase, it cannot fire Overwatch, but until
the end of the next Fight phase, each time a model in that unit makes a melee attack,
add 1 to that attack's hit roll.
```

Verbatim-Trigger (Z. 601–611): „Each time an enemy unit **declares a charge** against this
unit, if this unit is **not within Engagement Range** of any enemy units…"

**Schlüssel-Timings aus dem Regeltext:**
- Trigger: Charge-**Ansage** (nicht Auflösung) → Charge Phase, vor 2D6-Würfelwurf
- Hold Steady-Effekt: „bis Ende der Phase" (= Charge Phase), Overwatch 5+ statt 6
- Set to Defend-Effekt Part A: „bis Ende der Phase, kein Overwatch"
- Set to Defend-Effekt Part B: „bis Ende der **nächsten** Fight Phase, +1 Hit Nahkampf"
- Bedingung: Verteidiger **nicht** in Engagement Range → Tisch-Prüfung (manuell bestätigen)
- Gegenseitiger Ausschluss: Hold Steady ODER Set to Defend (nie beide)

---

## YAML-Ausgangslage (Plan 025 Step 4)

`data/wh40k_9e/necrons/faction_abilities.yaml` Z. 62–71 (aktueller Übergang):

```yaml
secondary:
  # 9E Directive 2: Hold Steady / Set to Defend. Real attack-sequence effect, but
  # its wiring depends on Plan 015 Overwatch (not yet built). Modelled as table-only
  # transition so Step 4 carries the correct 9E text without claiming a dead engine
  # effect. TODO: replace `enforcement: table` with real effect types
  # (overwatch_hit_threshold / hit_bonus_next_fight) in the dedicated D2 plan.
  effect:
    type: hold_steady_or_set_to_defend
    phase: any
    enforcement: table
```

**Migration (Ziel dieses Plans):**

```yaml
secondary:
  effect:
    type: hold_steady_or_set_to_defend
    phase: charge
    hold_steady:
      type: overwatch_hit_threshold
      value: 5
      enforcement: app
    set_to_defend:
      type: hit_bonus_next_fight
      value: 1
      enforcement: app
    # Engagement-Range-Bedingung ist Tisch-Prüfung (manuell bestätigen)
    # Gegenseitiger Ausschluss hold_steady / set_to_defend wird in der UI erzwungen
```

Alternativ (je nach Engine-Architektur, die Plan 015 vorgibt): zwei separate
Sub-Effekte könnten auch als `enforcement: app` / `enforcement: table` getrennt
modelliert werden. Der Executor entscheidet abhängig vom Plan-015-Schema — die
Intention ist: App erzwingt beide Teile (Klasse A), Engagement-Range bleibt Tisch.

---

## Andock-Punkt: Charge-Ansage-Fenster

Quelle: `src/gameMechanic/chargephase.py` Z. 97–138 (`_active_charge`), Plan 015 Z. 46–49.

```
_active_charge (Z. 77–138):
    ...
    tgts = st.session_state.selected_targets   ← Z. 97
    if not tgts: [info-text]; return
    for tgt_faction, tgt_uid in tgts:          ← Z. 102
        st.markdown(f"**Target:** {tgt_unit.name_en}")
    st.caption("Roll 2D6 …")                   ← Z. 106
    [Charge Successful / Charge Failed Buttons] ← Z. 108–138
```

**Andock-Punkt für D2:** Nach Ziel-Deklaration (`tgts` nicht leer), vor dem 2D6-Caption/Buttons.
Plan 015 Step 2 baut an genau diesem Punkt die Fire-Overwatch-Reaktiv-Box in der Spalte des
**inaktiven Spielers** (= Verteidiger). Die D2-Defender-Choice (Hold Steady / Set to Defend)
dockt an **denselben Moment** — aber als Entscheidung des Verteidigers, nicht als GO-Spend.

**Render-Logik in `_inactive_charge` (Z. 140–145):**
Die Funktion existiert bereits, enthält aktuell nur `st.caption("Overwatch: only unmodified 6s hit.")`.
Sie ist der natürliche Ort für die D2-Defender-Choice-Box.

---

## Vorhandene und fehlende Hooks

| Hook | Status | Ort |
|------|--------|-----|
| Charge-Ansage-Fenster (`_active_charge`) | ✅ vorhanden | `chargephase.py` Z. 97–138 |
| Inaktiver-Spieler-Spalte in Charge Phase (`_inactive_charge`) | ✅ vorhanden (leer) | `chargephase.py` Z. 140–145 |
| `was_charged`-Flag in `turn_flags` | ✅ vorhanden (Z. 353) | `game_state.py` Z. 349–360 |
| `active_modifiers` mit `expires_at_phase`/`expires_at_round` | ✅ vorhanden | `game_state.py` Z. 534–541, `gameProtocoll.py` Z. 214–235 |
| Overwatch-Reaktiv-Box + `attack_declaration["overwatch"]`-Flag | ❌ **fehlt** | Wird von Plan 015 Step 2 gebaut |
| HIT-Block-Schwelle 5+ bei Overwatch | ❌ **fehlt** | Wird von Plan 015 Step 2 gebaut |
| `hit_bonus_next_fight`-Flag / Fight-Phase-+1-Hit-Modifier | ❌ **fehlt** | Erstmals hier gebaut |
| `overwatch_declined_{seq}`-Flag | ❌ **fehlt** | Wird von Plan 015 Step 2 gebaut |

**Grep-Beleg (Stand 2026-06-26):**
```
grep -rn "overwatch\|hold_steady\|set_to_defend" src/gameMechanic/
→ KEIN Treffer in Mechanik (nur set_charged in unit_mutations.py:407 setzt was_charged)
```

---

## Effekt-Klassen (Akzeptanz-Katalog)

| Effekt | Klasse | Begründung |
|--------|--------|------------|
| Hold Steady → Overwatch 5+ | **A** (App erzwingt) | Schwellenänderung ist messbar + erzwingbar sobald Overwatch-Hook (Plan 015) steht |
| Set to Defend → kein Overwatch | **A** (App erzwingt) | UI blockiert Overwatch-Button wenn set_to_defend aktiv |
| Set to Defend → +1 Hit nächste Fight Phase | **A** (App erzwingt) | Persistenter Modifier, App zählt bis Ende nächste Fight Phase |
| Engagement-Range-Bedingung | **B** (Tisch-Prüfung) | Distanz-Messung ist Tisch-Verantwortung; App zeigt Hinweis und fragt manuelle Bestätigung |

---

## Schritt-für-Schritt-Verdrahtung

### Voraussetzung (BLOCKING): Plan 015 muss mindestens Step 2 abgeschlossen haben

Step 2 von Plan 015 liefert:
- `chargephase.py`: Reaktiv-Fenster, `spend_stratagem`-Extraktion, `overwatch_declined_{seq}`-Flag
- `_common.py` `_render_resolution_tab`: `attack_declaration["overwatch"]`-Flag → HIT-Block zeigt fixe 6
- `src/gameMechanic/reactions.py` (oder analog): `reactive_stratagems_for`-Helper

Ohne diese Infrastruktur ist Hold Steady (Overwatch 5+) nicht sinnvoll anschließbar.

---

### Step 1: Engine — Defender-Choice-Flag + Persistenz

**Dateien:** `src/gameMechanic/game_state.py`, `src/gameMechanic/unit_mutations.py`

1. **`game_state.py` `turn_flags`** (Z. 349–360): kein neues Flag in `turn_flags` nötig für die
   Choice selbst — die Choice wird per `active_modifiers` mit Expiry modelliert (s. Step 2 + 3).
   Für Set-to-Defend-Persistenz über die Phasengrenze hinweg:
   - `active_modifiers` hat `expires_at_phase` (löscht beim Eintritt in die benannte Phase).
   - „Bis Ende nächste Fight Phase" = der Modifier existiert, bis `expires_at_phase == "fight"`
     **das zweite Mal** erreicht wird — aber das bestehende `expires_at_phase` löscht beim
     **ersten** Eintritt in die Fight Phase (wenn Set to Defend in der Charge Phase gesetzt wird
     und die Fight Phase noch in **derselben** Runde kommt, wird der Modifier in der aktuellen
     Fight Phase gelöscht statt zu persistieren bis zur **nächsten** Fight Phase).
   - **Lösung:** `expires_at_round`-Mechanismus nutzen: `expires_at_round = current_round + 1`
     (löscht zu Beginn der Fight Phase in Runde current_round+1 → persistiert bis Ende der
     Fight Phase in current_round, was „bis Ende der nächsten Fight Phase" erfüllt, wenn der
     Effekt in der Charge Phase von Runde N gesetzt wird und in der Fight Phase von Runde N
     zuerst konsumiert werden soll, aber bis Ende Fight Runde N gilt).

   > **ACHTUNG:** Falls Set to Defend **in der Fight Phase** derselben Runde greift (was 9E
   > erlaubt — der Verteidiger kann in der Charge Phase Set to Defend wählen, und die Fight
   > Phase folgt direkt danach), muss der Modifier die aktuelle Fight Phase **überleben** und
   > erst in der nächsten Fight Phase ablaufen. → Konkrete Implementierung:
   > - `expires_at_round = current_round + 1` (nicht `expires_at_phase = "fight"`).
   > - ODER: neues `expires_at_fight_phase_count`-Feld (Zähler, wie viele Fight-Phase-Eintritte
   >   noch überleben soll). Empfehlung Planner: Einfachere Option = `expires_at_round + 1`;
   >   Executor prüft ob das in der Praxis (Runde N Charge → Runde N Fight → Runde N+1 Fight)
   >   korrekt ist. Falls nicht: STOP, Alternativen vorlegen.

2. **`unit_mutations.py`**: neue Fn `set_hold_steady(uid, faction)` und
   `set_set_to_defend(uid, faction)` — setzen `active_modifiers` in
   `st.session_state` mit passenden Feldern. Oder inline in der UI-Fn (Step 2/3).
   Empfehlung: inline in der UI bleiben (analog zu `spend_stratagem` aus Plan 015), keine
   neue Mutation-Fn nötig, da kein `turn_flags`-Eintrag.

**Verify:** Unit-Test: `active_modifiers` enthält nach Set-to-Defend den Modifier mit
korrektem `expires_at_round`-Wert; nach Fight-Phase-Eintritt in Runde N+1 ist er gelöscht.

---

### Step 2: UI — Defender-Choice-Box in `_inactive_charge`

**Datei:** `src/gameMechanic/chargephase.py` Z. 140–145 (`_inactive_charge`)

**⚠️ Layout vor Implementierung dem Nutzer zeigen** (Mockup-Pflicht, analog Plan 015 Step 2).

Vorschlag Defender-Choice-Box:

```
🛡️ Eternal Guardian D2 — Reaktion möglich
   [Name des gechargten Ziels] wird gechargt.
   Bedingung: Einheit nicht in Engagement Range (am Tisch prüfen).

   [Hold Steady]     [Set to Defend]     [Passen]
```

- Bedingung anzeigen als Warnung/Caption: „Check: not in Engagement Range (table)".
- **Hold Steady**: setzt `active_modifiers`-Eintrag `{type: "overwatch_hit_threshold", value: 5,
  expires_at_phase: "charge"}` für die Einheit des Verteidigers.
  → Wird von der Plan-015-Overwatch-Resolution konsumiert (HIT-Block zeigt 5+ statt 6).
- **Set to Defend**: setzt zwei Einträge:
  - `{type: "set_to_defend_no_overwatch", expires_at_phase: "charge"}` → blockiert Overwatch-Button
  - `{type: "hit_bonus_next_fight", value: 1, expires_at_round: current_round + 1}` → Fight-+1-Hit
- **Passen**: setzt `d2_declined_{charge_seq}`-Flag (analog `overwatch_declined_{seq}`) → Box
  erscheint nicht erneut für diesen Charge.
- Gegenseitiger Ausschluss: Hold Steady und Set to Defend schließen sich aus; nach Klick
  auf einen der Buttons ist der andere nicht mehr wählbar (State-Check).
- Box erscheint nur wenn:
  - Aktiver Spieler hat Charge-Einheit selektiert und `selected_targets` nicht leer.
  - Einheit des Verteidigers hat Eternal Guardian D2 aktiv (`ability_engine.py` Check:
    `_active_directive_has_type(def_faction, "hold_steady_or_set_to_defend")`).
  - Noch keine Choice getroffen (kein `d2_declined_{seq}`-Flag, kein vorhandener
    `overwatch_hit_threshold`/`set_to_defend_no_overwatch`-Modifier für diese Einheit).

**Render-Kontext:** `_inactive_charge(faction, uid, unit, unit_state)` kennt Einheit +
Zustand des Verteidigers; `st.session_state.selected_targets` liefert Charge-Ziele (der
Verteidiger ist das **Ziel** des Angreifers). Aktive Direktive per
`get_active_round_choice_directive(faction)` / `_active_directive_has_type`.

**Verify:** Manuell: Charge deklarieren → D2-Box erscheint beim Verteidiger; Hold Steady klicken →
Box verschwindet, Overwatch-Box (Plan 015) zeigt 5+ Schwelle; Set to Defend klicken →
Box verschwindet, Overwatch gesperrt, Fight-Phase-+1-Hit aktiv bis Ende nächste Fight Phase.

---

### Step 3: Overwatch-Threshold-Konsum (Hold Steady → 5+ statt 6)

**Datei:** `src/uiLayout/_common.py` (HIT-Block in `_render_resolution_tab`)

Plan 015 Step 2 implementiert: wenn `attack_declaration["overwatch"]` → HIT-Block zeigt fixe **6**.
D2-Hold-Steady ersetzt diese fixe 6 durch **5+** wenn der Modifier vorhanden ist.

**Verdrahtung:**
- Neue Fn `get_overwatch_hit_threshold(def_faction, def_uid) -> int`:
  - Checkt `active_modifiers` des Verteidigers auf `{type: "overwatch_hit_threshold"}`.
  - Gibt `value` zurück (Standard: 6, mit Hold Steady: 5).
- Im HIT-Block (`_render_resolution_tab`): wenn `overwatch`-Flag → zeige Schwelle aus
  `get_overwatch_hit_threshold(def_faction, def_uid)` statt hardcodierter 6.
- Caption: „Overwatch — hits only on unmodified {threshold}+" (bzw. „…5+ (Hold Steady)").

**Verify:** Test: Modifier gesetzt → `get_overwatch_hit_threshold` gibt 5; kein Modifier → 6.
Manuell: Overwatch mit Hold Steady zeigt 5+ im HIT-Block; ohne Hold Steady zeigt 6.

---

### Step 4: Set-to-Defend-+1-Hit-Konsum (Fight Phase)

**Datei:** `src/uiLayout/_common.py` (`_collect_atk_modifiers`, Z. 445–501)

Der bestehende `_collect_atk_modifiers` sammelt Hit-Modifier aus `active_buffs`, `active_modifiers`,
und `get_active_round_choice_modifier`. Der `hit_bonus_next_fight`-Modifier aus Set to Defend
liegt in `active_modifiers` → wird dort automatisch aufgegriffen, wenn der `roll_type`-Filter passt.

**Verdrahtung (Prüfpunkt):**
- `active_modifiers`-Eintrag für Set to Defend: `{roll_type: "hit", value: 1, target: "attacker",
  expires_at_round: N+1}`.
- In `_collect_atk_modifiers` Z. 488–500: Filter `rt in ("hit", "wound") and tgt in ("attacker",
  "any")` erfasst diesen Modifier **automatisch**, wenn das Schema stimmt.
- **Prüfen:** Welche Einheit ist Angreifer? Im Fight-Block ist der **Verteidiger** (der Set to
  Defend gewählt hat) der Angreifer in seiner Nahkampf-Aktivierung. Der `target: "attacker"`-Check
  muss auf die **eigene** Einheit zeigen — d. h. beim Render der Einheit, die Set to Defend
  gewählt hat, wird sie als Angreifer behandelt. Dieser Fall ist im bestehenden Schema korrekt
  abgedeckt (der Modifier gilt für „attacker" = die Einheit, die kämpft).
- **Falls das Schema nicht direkt passt:** neue kleine Fn
  `get_set_to_defend_hit_bonus(atk_faction, atk_uid) -> int` (analog `get_overwatch_hit_threshold`),
  die `active_modifiers` nach `type: hit_bonus_next_fight` für die Einheit filtert; Konsum in
  `_collect_atk_modifiers`.

**No-Overwatch-Block für Set to Defend:**
- Wenn `active_modifiers` `type: set_to_defend_no_overwatch` für die Einheit enthält und
  `attack_declaration["overwatch"]` gesetzt ist → Overwatch-Button deaktivieren / Caption
  „Set to Defend active — cannot fire Overwatch". Ort: Charge-Phase-UI oder Overwatch-Fn aus Plan 015.

**Verify:** Test: Modifier `hit_bonus_next_fight` gesetzt → `_collect_atk_modifiers` liefert
`[{"label": "Eternal Guardian D2", "value": 1, "roll_type": "hit"}]`.
Manuell: Nahkampfangriff der Einheit die Set to Defend gewählt hat → HIT-Block zeigt +1.
Nach Ende der Fight Phase (Runde N+1 Beginn) ist der Modifier aus `active_modifiers` gelöscht.

---

### Step 5: Engine — `_active_directive_has_type`-Check + Ability-Engine-Anpassung

**Datei:** `src/gameMechanic/ability_engine.py`

- `_active_directive_has_type(faction, "hold_steady_or_set_to_defend")` (bereits vorhanden aus
  Plan 025 — Muster: prüft ob die aktive Direktive den angegebenen Effekttyp hat).
- Nach YAML-Migration (Step 6): `_active_directive_has_type` muss auf den neuen kombinierten
  Effekttyp `hold_steady_or_set_to_defend` reagieren (oder auf die Sub-Typen `overwatch_hit_threshold`/
  `hit_bonus_next_fight`). Schema-Entscheidung abhängig von Plan-015-Architektur.

---

### Step 6: YAML — `enforcement: table` ersetzen

**Datei:** `data/wh40k_9e/necrons/faction_abilities.yaml` Z. 62–71

Nach vollständiger Verdrahtung (Steps 1–5) den Übergangs-Block durch echte Effekttypen ersetzen:

```yaml
secondary:
  effect:
    type: hold_steady_or_set_to_defend
    phase: charge
    hold_steady:
      type: overwatch_hit_threshold
      value: 5
      enforcement: app
    set_to_defend_no_overwatch:
      type: set_to_defend_no_overwatch
      enforcement: app
    set_to_defend_hit_bonus:
      type: hit_bonus_next_fight
      value: 1
      enforcement: app
```

`enforcement: table` und TODO-Kommentar entfernen.

---

## Affected files (vermutet, mit Begründung)

| Datei | Warum |
|-------|-------|
| `data/wh40k_9e/necrons/faction_abilities.yaml` | YAML-Effekttypen migrieren (Step 6) |
| `src/gameMechanic/chargephase.py` | Defender-Choice-Box in `_inactive_charge` (Step 2) |
| `src/gameMechanic/ability_engine.py` | `_active_directive_has_type`-Check; ggf. neue Helper-Fn (Step 5) |
| `src/uiLayout/_common.py` | Overwatch-Threshold-Konsum (Step 3); Set-to-Defend-+1-Hit-Konsum (Step 4) |
| `src/gameMechanic/game_state.py` | Ggf. neue Expiry-Logik falls `expires_at_round`-Schema nicht ausreicht (Step 1) |
| `tests/gameMechanic/test_ability_engine.py` | Test für `_active_directive_has_type` auf D2-Effekttyp |
| `tests/gameMechanic/test_combat.py` | Ggf. Regression wenn HIT-Block-Threshold-Fn neu eingeführt |
| `tests/uiLayout/test_common.py` | Neue Tests für Overwatch-Threshold + Set-to-Defend-Konsum |
| `docs/spec/acceptance/rules.md` | D2-Einträge auf `status: implementiert` + `getestet: ja` |
| `docs/goals/backlog.md` | §0-Tabelle D2 nachziehen |

**Nicht anfassen:**
- `src/gameMechanic/fightPhase.py` — Set-to-Defend-Modifier liegt in `active_modifiers`, keine Phase-spezifische Fn nötig
- `src/uiLayout/armyCard.py` — YAML-Text schon korrekt nach Plan 025 Step 4
- Plan-015-Dateien (`src/gameMechanic/reactions.py` etc.) — Infrastruktur-Seite Plan 015

---

## Test-Skizze

### Neue Tests

| Test | Datei | Was wird geprüft |
|------|-------|-----------------|
| `test_hold_steady_sets_overwatch_threshold_5` | `test_ability_engine.py` | Nach Hold-Steady-Wahl: `get_overwatch_hit_threshold` gibt 5 |
| `test_no_hold_steady_overwatch_threshold_6` | `test_ability_engine.py` | Ohne Hold Steady: `get_overwatch_hit_threshold` gibt 6 |
| `test_set_to_defend_hit_bonus_in_atk_modifiers` | `test_common.py` | `_collect_atk_modifiers` enthält +1 Hit wenn `hit_bonus_next_fight`-Modifier in `active_modifiers` |
| `test_set_to_defend_modifier_expires_fight_phase_next_round` | `test_common.py` oder `test_ability_engine.py` | Modifier mit `expires_at_round: N+1` ist nach `_reset_phase_state` in Runde N+1 Fight nicht mehr vorhanden |
| `test_hold_steady_set_to_defend_mutual_exclusion` | `test_ability_engine.py` oder `test_chargephase.py` | Nach Hold-Steady-Wahl ist kein Set-to-Defend-Modifier gesetzt, und umgekehrt |
| `test_set_to_defend_blocks_overwatch` | `test_common.py` oder `test_chargephase.py` | `active_modifiers` mit `set_to_defend_no_overwatch` → Overwatch-Button nicht nutzbar |

### Erwartete Test-Migrationen (Scoping-Pflicht: `grep -rn "hold_steady_or_set_to_defend" tests/`)

- Aktuell kein Test in `tests/` der `hold_steady_or_set_to_defend` pinnt (Übergangs-YAML wird
  als `enforcement: table` behandelt, keine Engine-Fn). → Keine Migration nötig.
- Nach Step 5 YAML-Migration: prüfen ob `_MODIFIER_RESULT_KEY` oder `_REROLL_DIRECTIVE_FLAGS`
  in `ability_engine.py` den alten Typ noch referenzieren → dann bereinigen.

---

## Manuelle UI-Verifikation (Render-Code, nicht durch Tests abgedeckt)

1. Eternal Guardian D2 aktiv + Charge deklariert (Verteidiger nicht in ER → manuell bestätigen):
   → Defender-Choice-Box erscheint in der Spalte des Verteidigers in `_inactive_charge`.
2. Hold Steady gewählt → Box verschwindet; Overwatch-GO nutzbar → HIT-Block zeigt **5+** statt 6.
3. Set to Defend gewählt → Box verschwindet; Overwatch-GO deaktiviert/gesperrt.
4. Nächste Fight Phase: Nahkampf-HIT-Block der Set-to-Defend-Einheit zeigt **+1 Hit**
   (Modifier aktiv, Badge „Eternal Guardian D2" oder ähnlich).
5. Nach Ende der Fight Phase (Phasenwechsel zu Morale oder neue Runde → `_reset_phase_state`
   in der **nächsten** Fight Phase): +1-Hit-Modifier verschwunden.
6. Passen-Button → Box erscheint nicht erneut für denselben Charge.
7. D2 **nicht** aktiv (anderes Protokoll gewählt): keine Box erscheint.
8. Nihilakh-Subfaktion mit Eternal Guardian als 6. Protokoll (Dynasty Bonus): D2-Box
   erscheint ebenfalls (Direktive auch via Dynasty-Bonus aktiv).

---

## STOP conditions

- Plan 015 Step 2 ist nicht abgeschlossen → D2-Hold-Steady-Verdrahtung (Step 3) blockiert; STOP.
- Die `active_modifiers`-Expiry-Logik (`expires_at_round + 1`) deckt „bis Ende nächste Fight
  Phase" nicht korrekt ab (z. B. Fight Phase in Runde N passiert vor dem Expiry-Check →
  Modifier schon in Runde N Fight gelöscht) → STOP, Alternativen vorlegen (neues Expiry-Schema
  oder Fight-Phase-Count-Zähler).
- Vorher grüner Test wird rot und steht nicht in der Migrationsliste → STOP, fragen.
- Charge-Phase-Reaktiv-Fenster aus Plan 015 verwendet eine andere State-Struktur als
  `selected_targets` / `_inactive_charge` → STOP, Andock-Punkt neu klären.
- Layout/Mockup der Defender-Choice-Box nicht freigegeben → Implementierung warten.

---

## Git workflow

- Branch: `feature/026-eternal-guardian-d2`.
- Empfohlene Commits: (1) Engine-Helper (Threshold-Fn, Hit-Bonus-Konsum), (2) UI-Charge-Box
  (`_inactive_charge`), (3) YAML-Migration + Doku.
- Nicht pushen/PR ohne Anweisung.

---

## Done criteria

Alle müssen gelten:

- [ ] Plan 015 Step 2 abgeschlossen (Abhängigkeit erfüllt)
- [ ] D2-Defender-Choice-Box erscheint nach Mockup-Freigabe in `_inactive_charge`
- [ ] Hold Steady → Overwatch 5+ im HIT-Block (Test + manuell)
- [ ] Set to Defend → Overwatch gesperrt (aktive Phase); +1 Hit in nächster Fight Phase (Test + manuell)
- [ ] +1-Hit-Modifier korrekt abgelaufen nach Ende nächste Fight Phase (Test)
- [ ] Gegenseitiger Ausschluss Hold Steady / Set to Defend erzwungen (Test)
- [ ] YAML `enforcement: table` entfernt; TODO-Kommentar entfernt
- [ ] `pytest --tb=short` grün, ≥ 90 %; INV-4b grün; Lint sauber
- [ ] `rules.md` + `backlog.md` §0/§4b: D2 als implementiert + getestet
- [ ] Status-Zeile in `docs/audit/plans/README.md` aktualisiert

---

## Selbstprüf-Checkliste

- [x] D2-Regeltext mit Zeilenbeleg zitiert (`faction_overview.txt` Z. 600–631, Trigger Z. 601–611)
- [x] Charge-Ansage-Fenster Andock-Punkt belegt (`chargephase.py` Z. 97–138, Plan 015 Z. 46–49)
- [x] `_inactive_charge` als Render-Ort belegt (`chargephase.py` Z. 140–145)
- [x] Plan 015 Out-of-Scope-Beleg für Set to Defend zitiert (Plan 015 Z. 85)
- [x] Plan 015 Overwatch-Infrastruktur-Beleg (Plan 015 Z. 112–146 Step 2)
- [x] YAML-Ausgangslage (`faction_abilities.yaml` Z. 62–71) verifiziert (grep-Beleg: Z. 66–71)
- [x] `was_charged`-Flag in `turn_flags` belegt (`game_state.py` Z. 353) — nicht genutzt für D2, aber dokumentiert
- [x] `active_modifiers`-Expiry-Schema belegt (`game_state.py` Z. 534–541)
- [x] `_collect_atk_modifiers`-Pfad für `active_modifiers`-Konsum belegt (`_common.py` Z. 488–500)
- [x] grep `overwatch\|hold_steady\|set_to_defend` src/gameMechanic/ → kein Treffer (korrekt: fehlt)
- [x] Plan 015 als Abhängigkeit in README.md eingetragen
- [x] Vermerk in Plan 015 ergänzt
