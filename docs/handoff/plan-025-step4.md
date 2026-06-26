# Plan 025 Step 4 — Eternal Guardian (Detail-Planung)

Lebensdauer: temporär — Teil A löschen nach Umsetzung von Step 4; Teil B in eigenen Plan überführen.

Diese Datei ist zweigeteilt:
- **Teil A — D1 (Step 4, bereit für Executor)** — Status: ANSWERED (Stakeholder-Entscheidungen eingearbeitet).
- **Teil B — D2 (eigener Plan, NICHT Teil von Step 4)** — Status: NEEDS-DECISION (Schnitt: D2 raus aus Step 4).

---
---

# TEIL A — D1 light_cover_if_stationary (Step 4)
Status: ANSWERED — bereit für Executor

## Stakeholder-Entscheidungen (ANSWERED)

- **D1 Light-Cover-Anzeige = Variante C** (ANSWERED): die bestehende Light-Cover-Checkbox bleibt; bei aktivem D1 + `movement_choice=="stationary"` wird sie programmatisch **vorgehakt UND gesperrt** (`value=True, disabled=True`). Badge-Text via `light_cover_label`-Muster (Step 3), z.B. „Light Cover [Eternal Guardian]". Manuell nicht änderbar solange D1 greift.
- **Doku-Scope = überall** (ANSWERED): `docs/spec/acceptance/rules.md`, `docs/goals/backlog.md` (§0 + §4b), `docs/spec/processes.md` (D2-Attackensequenz, gehört aber zu Teil B), `docs/spec/rules_insights.md` (D1-Gotcha: `movement_choice=="stationary"` als Bedingung).

## Affected files (Teil A)

- `data/wh40k_9e/necrons/faction_abilities.yaml` Z. 50–66 — `primary`-Effekt `save_modifier` → `light_cover_if_stationary`; primary-Text auf 9E. `secondary` siehe Teil B (YAML-Konsequenz).
- `src/gameMechanic/ability_engine.py` — (a) `save_modifier` aus `_MODIFIER_RESULT_KEY` (Z. 84) entfernen NACH `grep -rn "type: save_modifier" data/`; (b) neue pure Fn `get_active_round_choice_light_cover_if_stationary(def_player, def_uid)`; (c) `_active_directive_has_type` (Z. 269) als Basis.
- `src/uiLayout/_common.py` — (a) `_collect_def_save_modifiers` (Z. 504): `proto.get("save")`-Zweig (Z. 515–517) entfernen, neue Engine-Fn einbinden (`def_uid`-Parameter ergänzen); (b) SAVE-Block (Z. 951–975): Auto-inject Light Cover; (c) Checkbox-Block (Z. 1052–1065): Variante C (pre-tick + disabled + Badge).
- `src/uiLayout/armyCard.py` Z. 156–157 (+ Z. 208–209, 228–229) — kein Code-Änderung nötig; Fix liegt vollständig in den YAML-Strings.
- `tests/gameMechanic/test_ability_engine.py` Z. 511–516, 762–773 — Tests migrieren (s. Migrationsliste). Z. 589–591 betrifft Teil B (Reroll-Entfernung).
- `tests/uiLayout/test_common.py` — neue Tests für Auto-inject Light Cover (stationary True/False).
- `docs/spec/acceptance/rules.md`, `docs/goals/backlog.md`, `docs/spec/rules_insights.md` — Doku (s. Scope).

## D1 — 9E-Regeltext (faction_overview.txt Z. 585–599)
> Directive 1: Each time an attack is made against this unit, if it did not make a Normal Move, Advance or Fall Back this battle round, this unit receives the benefit of Light Cover.

## YAML — neuer primary-Block (ersetzt Z. 58–62)
```yaml
primary: "Each time an attack is made against this unit, if it did not make a Normal Move, Advance or Fall Back this battle round, this unit receives the benefit of Light Cover"
directives:
  primary:
    effect:
      type: light_cover_if_stationary
      phase: any
```
Kein `value`-Feld (Boolean-Effekt). Kein `enforcement`: Klasse A, App setzt Light Cover automatisch.

## Engine — neue Fn
```python
def get_active_round_choice_light_cover_if_stationary(
    def_player: str, def_uid: str
) -> bool:
    """True if the defending unit benefits from Light Cover (Eternal Guardian D1):
    directive active AND unit did not move this battle round (movement_choice == 'stationary').

    Class A — the App grants Light Cover automatically. Aggregates round-assigned AND
    always-active 6th/dynasty directive via _active_directive_effects (same pattern as
    get_active_round_choice_ignores_cover_half_range, Z. 274).
    """
    if not _active_directive_has_type(def_player, "light_cover_if_stationary"):
        return False
    from gameMechanic.game_state import lookup  # noqa: PLC0415
    try:
        _, state = lookup(def_player, def_uid)
    except KeyError:
        return False
    return state.get("movement_choice") == "stationary"
```

## SAVE-Block-Konsum in `_common.py`
Verteidiger im SAVE-Block bekannt: `def_uid = entry["def_uid"]` (Z. 865), `def_faction = entry["def_faction"]` (Z. 864), `def_unit, def_state = lookup(def_faction, def_uid)` (Z. 876). `def_state["movement_choice"]` direkt lesbar.

`_collect_def_save_modifiers` (Z. 504) bekommt `def_uid: str` als Parameter; ruft `get_active_round_choice_light_cover_if_stationary(def_faction, def_uid)`; bei True → der Light-Cover-Modifier wird über die Checkbox-Mechanik gesetzt (Variante C), NICHT als zweiter separater Modifier — sonst doppelte +1. Konkret:

**Variante C-Verdrahtung (Z. 1052–1065):**
- Wenn D1+stationary → `st.session_state[f"light_cover_{cover_key}"] = True` programmatisch setzen, Checkbox mit `value=True, disabled=True` rendern, Label via `light_cover_label("Eternal Guardian")`.
- Der bestehende Zweig Z. 974–975 (`if light_cover: final_save_mods.append({"label": "Light Cover", "value": 1})`) greift dann automatisch — keine Doppel-+1.
- Wichtig: Auto-Grant nur in `is_shooting`? NEIN — D1 gilt „each time an attack is made" (jede Phase). Aber die Light-Cover-Checkbox lebt aktuell nur im Shooting-Block (Z. 951: `is_shooting and ...`). → OFFENER PUNKT, s. NEEDS-DECISION A1.

## Test-Migrationsliste (Teil A, aus grep)

| Datei:Zeile | Pinnt altes Verhalten | Migration |
|---|---|---|
| `tests/gameMechanic/test_ability_engine.py:511–516` | Eternal Guardian primary → `{"save": 1}` via `get_active_round_choice_modifier` | Umbau: prüft `get_active_round_choice_light_cover_if_stationary(player, uid) == True` wenn stationary, `== False` wenn bewegt |
| `tests/gameMechanic/test_ability_engine.py:762–773` | Accumulate-Test: Eternal Guardian primary → `{"save": 1}` im generischen Modifier-Dict | Umbau: kein `save`-Key mehr; nur der Vengeful-ap_on_wound_6-Teil bleibt |

**Bleiben unverändert (anderer Namespace):** `tests/uiLayout/test_dice_html.py:52–239` (`save_modifier_die_pair_html` UI-Fn), `tests/gameMechanic/test_combat.py:497–521` (`resolve_save` Kernel). `combat.py:78,125,134,135` = Dataclass-Feld; `dice_compose.py:299` = UI-Fn — beide bleiben.

## Manuelle UI-Verifikation (Teil A)
1. Necron-Einheit stationary + Eternal Guardian D1 aktiv → SAVE-Block: Light-Cover-Checkbox vorgehakt + disabled, Badge „[Eternal Guardian]", +1 Save greift.
2. Necron-Einheit bewegt (Normal/Advance/Fall Back) + D1 aktiv → Checkbox frei, kein Auto-Grant.
3. Nihilakh-Subfaktion mit Eternal Guardian als 6. Protokoll → Dynasty Bonus, Auto-Grant greift wenn stationary.

---
---

# TEIL B — D2 Hold Steady / Set to Defend (eigener Plan)
Status: NEEDS-DECISION — Schnitt: D2 raus aus Step 4, eigener Plan, abhängig von Plan 015 Overwatch.

## KORREKTUR der Klassifikation
D2 ist **kein reiner Tisch-Hinweis (Klasse B)**, sondern ein echter Attacken-Sequenz-Effekt mit Defender-Choice. Re-Recherche-Belege:

### 9E-Regeltext (faction_overview.txt Z. 600–631, verbatim-Trigger Z. 601–611)
> Directive 2: Each time an enemy unit **declares a charge** against this unit, if this unit is not within Engagement Range of any enemy units, it can either Hold Steady or Set to Defend.
> If it **Holds Steady**, then until the end of the phase, any **Overwatch** attacks made by models in that unit score hits on unmodified rolls of **5+, instead of 6**.
> If it **Sets to Defend**, then until the end of the phase, it cannot fire Overwatch, but until the end of the next **Fight phase**, each time a model in that unit makes a melee attack, **add 1 to that attack's hit roll**.

Trigger = „declares a charge" → Charge Phase, Moment der Charge-**Ansage** (nicht Auflösung). Bestätigt: core_rules.txt Charge Phase Z. 1768–1776 (zwei Schritte: erst chargen, dann HI). Die Ansage ist Schritt 1.

### Vorhandene Hooks in der Codebasis (grep-Belege)
- **Charge-Ansage-Fenster existiert:** `src/gameMechanic/chargephase.py` `_active_charge` Z. 97–138 — Ziele gewählt (`selected_targets`), „Roll 2D6"-Hinweis, Buttons „Charge Successful"/„Charge Failed". Plan 015 nennt diesen Punkt explizit (Z. 46–49): „Das reaktive Fenster für Overwatch liegt GENAU hier: Ziele deklariert, Würfelwurf noch nicht bestätigt." → **exakt der Andock-Punkt für die D2-Defender-Choice (Hold Steady / Set to Defend).**
- **Kein Overwatch-/Hold-Steady-/Set-to-Defend-Hook im Code:** `grep -rn "overwatch\|hold_steady\|set_to_defend" src/gameMechanic/` → KEIN Treffer in Mechanik (nur `set_charged` in `unit_mutations.py:407` setzt `was_charged`-Flag). Es gibt aktuell KEINEN Punkt, an dem eine Charge ANGESAGT (nicht aufgelöst) wird und der Verteidiger reagieren könnte — das Reaktiv-Fenster ist erst durch Plan 015 geplant, nicht gebaut.
- **`turn_flags`** (game_state.py Z. 349–360) hat `was_charged`, aber kein Reaktions-Flag und kein `overwatch_hit_on`/`set_to_defend`.

### Plan 015 ist der natürliche Andock-Punkt
`docs/audit/plans/015-contextual-reactive-stratagems.md`:
- Z. 77: „`chargephase.py` — Overwatch-Fenster + HI-Eligibility-Hook" (in scope).
- Z. 60–61: Overwatch-Regel = Treffer nur auf unmod. 6 (BS irrelevant). **Hold Steady ändert genau diese Schwelle auf 5+** → setzt das Overwatch-Feature voraus.
- Z. 112–146 Step 2: baut die Reaktiv-Infrastruktur + Fire Overwatch im Charge-Fenster (`attack_declaration["overwatch"] = True`, HIT-Block-Schwelle).
- **ABER Z. 85 (out of scope): „Set to Defend (kein Stratagem, separate Regel) — nicht bauen."** → Set to Defend ist in Plan 015 bewusst ausgeklammert.

**Fazit:** Hold Steady (Overwatch 5+) dockt natürlich an Plan 015 Overwatch an. Set to Defend (+1 Hit next Fight) ist von Plan 015 ausgeklammert und braucht zusätzlich einen Fight-Phase-Modifier + eine „bis Ende nächste Fight Phase"-Persistenz. Beides setzt Plan 015 voraus.

## Rechercheplan/Skizze D2-Verdrahtung (für eigenen Plan)
1. **Defender-Choice-UI:** im Charge-Ansage-Fenster (`chargephase.py` `_active_charge`, nach Ziel-Deklaration, vor 2D6) eine Box in der Spalte des **inaktiven** Spielers (= Verteidiger) — analog zur Plan-015-Overwatch-Box (Z. 119–123). Bedingung: Verteidiger nicht in Engagement Range (Tisch-Prüfung → manuell bestätigen). Buttons „Hold Steady" / „Set to Defend".
2. **Hold Steady** → setzt ein Flag (z.B. `turn_flags["overwatch_hit_on"] = 5`), das die Plan-015-Overwatch-Resolution (HIT-Block-Schwelle) von 6 auf 5+ senkt. **Hängt an Plan 015 Overwatch.**
3. **Set to Defend** → setzt ein persistentes Flag (z.B. `set_to_defend_until_fight`), das im FightPhase-HIT-Block (`_common.py`) +1 Trefferwurf für diese Einheit gibt, bis Ende der nächsten Fight Phase. Braucht: (a) Fight-Phase-Modifier-Hook, (b) „bis Ende nächste Fight Phase"-Persistenz über Phasen/Runden hinweg (neue Lebensdauer-Logik im `turn_flags`/`active_buffs`-Reset). Von Plan 015 ausgeklammert (Z. 85).
4. **Gegenseitiger Ausschluss:** Hold Steady ODER Set to Defend, nicht beide; Set to Defend verbietet zusätzlich Overwatch in derselben Phase.

**EXPLIZITER VERMERK:** Die Verdrahtung von D2 hängt an **Plan 015 Overwatch** — dort als abhängige Aufgabe eintragen (Plan 015 baut Overwatch-Infrastruktur; D2-Hold-Steady senkt nur die Schwelle; D2-Set-to-Defend braucht zusätzlich den Fight-Modifier, der in Plan 015 Z. 85 ausgeklammert ist). D2 darf NICHT in Step 4 implementiert werden.

## YAML-Konsequenz für D2-secondary in Step 4
Da D2 noch nicht implementierbar ist, modellieren wir den `secondary`-Block als **Tisch-/Übergangs-Effekt mit TODO-Verweis**, damit Step 4 den `secondary`-Text trotzdem auf 9E-Wortlaut bringt, ohne einen toten Engine-Effekt zu behaupten (kein erfundener Modifier, keine Engine-Konsumtion):
```yaml
secondary: "When an enemy declares a charge against this unit and it is not in Engagement Range: Hold Steady (Overwatch hits on 5+) or Set to Defend (no Overwatch, but +1 Hit in next Fight phase)"
directives:
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

## Test-Konsequenz für Step 4 (Teil B-Berührung)
`tests/gameMechanic/test_ability_engine.py:589–591` (`test_reroll_save_1_eternal_guardian_s`) pinnt `{"reroll_save_1"}` aus `get_active_round_choice_rerolls`. Da `reroll_save_1` ersatzlos entfällt (D2 ist kein Reroll), muss dieser Test in Step 4 **entfernt/umgeschrieben** werden → er wird sonst rot. `reroll_save_1` aus `_REROLL_DIRECTIVE_FLAGS` (ability_engine.py Z. 205) entfernen NACH `grep -rn "type: reroll_save_1" data/`.

---
---

## NEEDS-DECISION (für Stakeholder)

**A1 (Teil A, neu):** D1 gilt 9E-wörtlich „each time an attack is made against this unit" — also **jede Phase** (Shooting UND Fight), nicht nur Shooting. Die Light-Cover-Checkbox lebt aber aktuell nur im Shooting-SAVE-Block (`_common.py` Z. 951: `is_shooting and ...`; Heavy Cover ist die Fight-Variante Z. 1066–1069). Soll der D1-Auto-Light-Cover (a) nur im Shooting greifen wie die bestehende Light-Cover-Checkbox [pragmatisch, deckt 90 %], oder (b) auch im Fight-SAVE-Block als zusätzlicher Auto-Modifier erscheinen [regelgenau, mehr Render-Aufwand]? → Empfehlung Planner: (a) für Step 4, (b) als Folge-Notiz im Backlog.

Antwort: (a)

**B1 (Teil B):** Schnitt bestätigen — D2 raus aus Step 4, eigener Plan, eingetragen als abhängige Aufgabe unter Plan 015 Overwatch?

Antwort: Gut machen wir so, bitte hinreichenden Plan anlegen.

**B2 (Teil B):** YAML-Übergang für D2-secondary akzeptiert (`enforcement: table` + TODO-Kommentar, 9E-Text), oder soll der `secondary`-Block in Step 4 ganz unverändert/leer bleiben bis der D2-Plan kommt?

Antwort: Übergang — bringt den korrekten 9E-Wortlaut, behauptet keinen toten Engine-Effekt, ersetzt das erfundene reroll_save_1.

**B3 (Teil B):** Plan-015-Anpassung — soll Set to Defend (Z. 85 dort als out-of-scope) in Plan 015 nachgezogen werden, oder bleibt es ein separater dritter Plan zusätzlich zum Overwatch-Andock?

Antwort: igener D2-Plan deckt beide (Hold Steady + Set to Defend); Hold-Steady-Hälfte hängt an Plan-015-Overwatch, Set-to-Defend ist ein Fight-+1-Hit-Modifier. Vermerk in Plan 015.

---

## Selbstprüf-Checkliste

- [x] D1/D2-Texte mit Zeilenbeleg aus faction_overview.txt zitiert (D1 Z. 585–599; D2 Z. 600–631, Trigger Z. 601–611)
- [x] Light-Cover-Konsumpunkt in _common.py mit Zeile belegt (Z. 951 Checkbox-State, Z. 974–975 Modifier-Append, Z. 1052–1065 Checkbox-Render); Verteidiger-Ermittlung Z. 864–876
- [x] movement_choice-Stationär-Wert per Code-Beleg verifiziert: `"stationary"` (game_state.py Z. 343+346 initial; unit_mutations.py Z. 396 setter)
- [x] grep save_modifier/reroll_save_1 über tests/ UND src/ gelaufen, alle Treffer gelistet (Teil A + Teil B)
- [x] save_modifier/reroll_save_1 andere Konsumenten geprüft: combat.py = Dataclass-Feld (bleibt); save_modifier_die_pair_html = UI-Fn (bleibt); YAML-Effekttyp ohne Produzent nach Migration
- [x] armyCard-Render-Stelle mit Zeile belegt (Z. 156–157, 208–209, 228–229)
- [x] D2-Re-Recherche: Charge-Ansage-Fenster (chargephase.py Z. 97–138) + KEIN bestehender Overwatch-Hook (grep leer) + Plan 015 Andock (Z. 46–49, 77, 85) belegt
