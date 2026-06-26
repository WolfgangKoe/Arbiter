# Plan 015: Reaktive Stratagems kontextuell — Overwatch, Counter-Offensive, HI-Erweiterung, once_per_battle

> **Executor instructions**: Follow this plan step by step. Run every
> verification command and confirm the expected result before moving to the
> next step. If anything in the "STOP conditions" section occurs, stop and
> report — do not improvise. When done, update the status row for this plan
> in `docs/audit/plans/README.md`.
>
> **Drift check (run first)**:
> `git diff --stat f0f4e17..HEAD -- src/gameObjects/stratagem.py src/gameMechanic/chargephase.py src/gameMechanic/fightPhase.py src/uiLayout/gameProtocoll.py`
> Drift in `fightPhase.py` durch Plan 013 ist ERWARTET (Dispatch-Umbau).
> Wenn `stratagem_visibility` oder die Charge-Buttons strukturell anders
> aussehen als unter Current state: STOP.

## Status

- **Priority**: P2 (MITTEL — next_session.md „GOs in gameActionArea")
- **Effort**: L (vier Teilstücke; einzeln committen)
- **Risk**: MEDIUM (greift in Phasen-Abläufe ein: Charge-Unterbrechung, Fight-Reihenfolge)
- **Depends on**: 013 empfohlen (Fight-Phase-Dispatch ist danach stabil; nicht parallel zu 013)
- **Category**: feature (Regelkonformität reaktive Stratagems)
- **Planned at**: commit `f0f4e17`, 2026-06-12

## Why this matters

Reaktive Stratagems (`timing: phase_reactive`) sind daten-seitig vollständig
(`_shared/stratagems.yaml`: Fire Overwatch Z. 68-80, Counter-Offensive
Z. 82-94), werden aber von `stratagem_visibility` (`stratagem.py:92-93`)
KOMPLETT versteckt — sie sind im Spiel schlicht nicht benutzbar. Außerdem
wird `once_per_battle` nicht enforced (`used_stratagem_ids` wird bei jedem
Phasenwechsel geleert, `game_state.py:356`), und Heroic Intervention ist
hart auf CHARACTER beschränkt (`chargephase.py:176`), obwohl Fähigkeiten
wie *Enslaved Protectors* Non-CHARACTER-HI erlauben. Nutzer-Vorgabe: GOs
erscheinen **kontextuell in der gameActionsArea** (beim betroffenen
Spieler), nicht als zentrale Liste.

## Current state

- `stratagem.py:71-101` — `stratagem_visibility()`: `phase_reactive` →
  immer `"hidden"`. Felder `timing`/`event` existieren bereits
  (`fire_overwatch: event: on_declaration`; `counter_offensive: event:
  on_declaration`).
- `gameProtocoll.py:120-236` — zentrale Stratagem-Liste; CP-Abzug,
  `used_stratagem_ids`, `active_modifiers`-Eintrag, Undo. Diese Mechanik
  (Spend/Undo/Modifier) ist wiederverwendbar.
- `chargephase.py:97-138` — `_active_charge`: Ziele gewählt → „Roll 2D6"-
  Hinweis → Buttons „Charge Successful"/„Charge Failed". **Das reaktive
  Fenster für Overwatch liegt GENAU hier**: Ziele deklariert, Würfelwurf
  noch nicht bestätigt.
- `fightPhase.py:77-113` — `_advance_fight_turn_if_needed`: wechselt
  `fight_current_player` nach „fought". **Das reaktive Fenster für
  Counter-Offensive**: unmittelbar nach diesem Wechsel, bevor der nun
  aktive Spieler eine Einheit wählt.
- `chargephase.py:152-189` — `_render_hi_phase`: Kandidaten =
  `u.has_keyword("CHARACTER")` (Z. 176) + nicht in Melee + nicht bereits
  interveniert.
- `game_state.py:356` — `_reset_phase_state`: `used_stratagem_ids = set()`
  → `once_per_battle`-GOs (z. B. Insane Bravery) sind jede Phase erneut
  nutzbar. `stratagem_visibility` bekommt nur `used_this_phase`.
- Overwatch-Regel (core_rules.txt): Schüsse wie in der Shooting Phase, aber
  Treffer NUR auf unmodifizierte 6 (BS/Modifier irrelevant).

## Commands you will need

| Zweck | Befehl | Erwartet |
|-------|--------|----------|
| venv | `source .venv/bin/activate` | `(.venv)` |
| Stratagem-Tests | `python -m pytest tests/gameObjects/test_stratagem.py -q` | grün |
| Phasen-Tests | `python -m pytest tests/gameMechanic/ -q` | grün |
| Vollsuite | `pytest --tb=short` | grün, ≥80 % |

## Scope

**In scope**:
- `src/gameObjects/stratagem.py` — Visibility um reaktiven Kontext erweitern
- `src/uiLayout/gameProtocoll.py` — Spend-Logik in wiederverwendbare Funktion extrahieren
- `src/gameMechanic/chargephase.py` — Overwatch-Fenster + HI-Eligibility-Hook
- `src/gameMechanic/fightPhase.py` — Counter-Offensive-Fenster
- `src/gameMechanic/ability_engine.py` — `can_heroic_intervene(unit, faction)`-Hook
- `src/gameMechanic/game_state.py` — `used_stratagem_ids_battle` (persistenter Set)
- `src/uiLayout/_common.py` — Overwatch-Flag in der Hit-Block-Darstellung
- Tests + ggf. `data/wh40k_9e/necrons/unit_abilities.yaml` (HI-Fähigkeit, Step 4)

**Out of scope** (NICHT anfassen):
- Set to Defend (kein Stratagem, separate Regel) — nicht bauen im Rahmen dieses Plans.
  **Abhängiger Konsument (S102-Vermerk, Plan 026):** Eternal Guardian D2 hängt an diesem
  Plan als Voraussetzung: Hold Steady → Overwatch trifft 5+ statt 6 (braucht Overwatch-Hook
  aus Step 2 dieses Plans); Set to Defend → +1 Hit im nächsten Fight (Fight-Modifier,
  erstmals in Plan 026 gebaut). Sobald Plan 015 Step 2 abgeschlossen ist, kann Plan 026
  (D2-Hold-Steady/Set-to-Defend) umgesetzt werden — er dockt an `_inactive_charge` und
  den HIT-Block-Threshold-Mechanismus aus diesem Plan. Plan 025 Step 4 B3-Entscheid
  (S102): eigener D2-Plan deckt beide Hälften; Vermerk hier ergänzt 2026-06-26.
- Automatische Distanz-/Sichtlinien-Prüfung — Tisch-Verantwortung wie überall.
- Übrige `timing: phase_reactive`-GOs (z. B. Emergency Disembarkation):
  Infrastruktur aus Step 2 trägt sie, aber eigene Effekt-UIs sind NICHT Teil
  dieses Plans — im Bericht als „jetzt sichtbar, Effekt manuell" ausweisen.

## Git workflow

- Branch: `feature/015-reactive-stratagems`.
- Vier Commits empfohlen: (1) once_per_battle, (2) Reaktiv-Infrastruktur +
  Overwatch, (3) Counter-Offensive, (4) HI-Hook.
- Nicht pushen/PR ohne Anweisung.

## Steps

### Step 1: `once_per_battle` enforced

1. `game_state.py`: neuer Session-Key `used_stratagem_ids_battle: set[str]`
   (Init + `reset_game`; in `_reset_phase_state` NICHT leeren).
2. `stratagem_visibility`: neuer Parameter `used_this_battle: set[str]`;
   `once_per_battle`-GOs mit ID darin → `"greyed"` (Label „(used)").
3. `gameProtocoll.py`: beim Spend in BEIDE Sets eintragen; Undo entfernt aus
   beiden.

**Verify**: Neue Tests in `tests/gameObjects/test_stratagem.py` (Visibility
mit `used_this_battle`) + bestehende grün.

### Step 2: Reaktiv-Infrastruktur + Fire Overwatch — MOCKUP ZUERST

**⚠️ Layout vor Implementierung dem Nutzer zeigen** (kontextuelle GO-Box).
Vorschlag fürs Mockup — in der Charge Phase, sobald der aktive Spieler Ziele
deklariert hat (Fenster `chargephase.py` vor den 2D6-Buttons), erscheint in
der **Spalte des inaktiven Spielers** eine GO-Box:

```
⚡ Reaktion möglich — Fire Overwatch (1 CP)
   Necron Warriors wurde gechargt.
   [Fire Overwatch — 1 CP]   [Passen]
```

Implementierung:
1. `gameProtocoll.py`: `spend_stratagem(strat, faction)` aus dem
   Button-Handler extrahieren (CP-Abzug, Sets, `active_modifiers`,
   `log_action`) — von Liste UND Kontext-Boxen aufrufbar.
2. Helper `reactive_stratagems_for(phase, event, faction)` (neues Modul
   `src/gameMechanic/reactions.py` oder in `stratagem.py`): lädt per
   `load_stratagems`, filtert `timing == "phase_reactive"`, `event`,
   `player == "inactive"`, CP ausreichend, nicht used (phase/battle).
3. Charge-Fenster: Während Ziele deklariert, aber Charge nicht bestätigt
   (`selected_targets` nicht leer, aktiver Spieler hat Charge-Einheit
   selektiert), in der inaktiven Spalte die Box rendern. „Passen" setzt ein
   `overwatch_declined_{seq}`-Flag, damit die Box nicht erneut nervt.
4. Overwatch-Ausführung: Klick → `spend_stratagem` + Start einer normalen
   Schuss-Deklaration des GECHARGTEN Ziels gegen die Charge-Einheit über den
   Gruppen-Flow, mit `attack_declaration["overwatch"] = True`.
5. `_common.py` `_render_resolution_tab`: wenn `overwatch`-Flag → HIT-Block
   zeigt fixe **6** (unmodifiziert; alle Hit-Modifier unterdrückt, Caption
   „Overwatch — hits only on unmodified 6"). Wound/Save/Damage unverändert.
6. Nach Abschluss der Overwatch-Resolution kehrt die UI ins Charge-Fenster
   zurück (Charge-Buttons wieder sichtbar); das Ziel bekommt KEIN
   `shot`-Flag (Overwatch zählt nicht als normales Schießen — Regel prüfen
   in core_rules.txt, Abschnitt Overwatch, und im Bericht zitieren).

**Verify**: Manuell: Charge deklarieren → Box erscheint beim Verteidiger;
Overwatch durchspielen → Hit-Block zeigt nur 6; Charge danach normal
auflösbar. CP um 1 reduziert, GO als used markiert.

### Step 3: Counter-Offensive

Fenster: `_advance_fight_turn_if_needed` hat gerade gewechselt, der neue
`fight_current_player` ist der Spieler, der NICHT zuletzt gekämpft hat —
Counter-Offensive erlaubt dem INAKTIVEN (= dem, der den Zug eigentlich
abgeben müsste? — Nein:) **dem Spieler, der nicht dran wäre**, 2 CP zu
zahlen und als Nächster zu kämpfen. Konkret: nach jedem „fought" eines
Spielers X, BEVOR Spieler Y seine Einheit aktiviert, darf X (sofort wieder)
per Counter-Offensive kämpfen — d. h. die Box erscheint beim Spieler, der
NICHT `fight_current_player` ist, solange Y noch keine Einheit selektiert
hat und X eligible Einheiten besitzt.

1. Box (gleiche Optik wie Step 2) in der Spalte des Nicht-Zug-Spielers:
   `[Counter-Offensive — 2 CP]` → `spend_stratagem` +
   `fight_current_player` auf diesen Spieler setzen + `st.rerun()`.
2. `_advance_fight_turn_if_needed` darf den manuell gesetzten Spieler nicht
   sofort zurückwechseln: Flag `counter_offensive_pending` setzen, das den
   Auto-Skip für genau einen Aktivierungszyklus unterdrückt (gelöscht, sobald
   die Einheit `fought` ist).
3. Regel-Detail: Counter-Offensive umgeht NICHT die CHARGED-Priorität
   (charged units fight first bleibt; RAW: nur die Alternation wird
   unterbrochen). `can_fight_now`-Prüfung bleibt aktiv.

**Verify**: Test: Reihenfolge X-fought → Counter-Offensive durch X →
X kämpft erneut → danach normale Alternation. Manuell durchspielen.

### Step 4: HI-Eligibility datengetrieben erweitern

1. `ability_engine.py`: `can_heroic_intervene(unit: Unit, faction: str) ->
   bool` — True wenn `unit.has_keyword("CHARACTER")` ODER eine
   Unit-/Faction-Ability mit `effect.type: heroic_intervention` auf die
   Einheit zutrifft (`_unit_matches_target`-Muster).
2. `chargephase.py:176`: `u.has_keyword("CHARACTER")` durch den Hook ersetzen.
3. Datenseite: in `docs/work/wahapedia_necrons/` nach *Enslaved Protectors*
   suchen (Cryptothralls). Falls vorhanden: Eintrag in
   `necrons/unit_abilities.yaml` mit `effect.type: heroic_intervention` +
   `rule_text` ergänzen. Falls NICHT auffindbar: Hook trotzdem bauen
   (generisch), Datenpflege im Bericht als offen markieren.

**Verify**: Test: Einheit ohne CHARACTER, mit HI-Ability → erscheint in den
HI-Kandidaten; ohne Ability → nicht.

### Step 5: Vollsuite + Lint + Doku

- `pytest --tb=short` grün, ≥80 %; Lint passt.
- `docs/spec/processes.md` (P-06 GO-Visibility): reaktive Zustände +
  `used_stratagem_ids_battle` dokumentieren.

## Test plan

- Visibility: `once_per_battle` über Phasengrenzen; reaktive GOs weiterhin
  unsichtbar in der zentralen Liste, aber von `reactive_stratagems_for`
  geliefert.
- Overwatch: Flag im `attack_declaration`; Hit-Threshold-Override;
  CP-Buchung; kein `shot`-Flag am Verteidiger.
- Counter-Offensive: Spieler-Wechsel-Sequenz inkl. CHARGED-Priorität.
- HI-Hook: CHARACTER, Ability-Grant, keins von beiden.

## Done criteria

ALLE müssen gelten:

- [ ] `once_per_battle` wirkt über Phasen hinweg (Test)
- [ ] Fire Overwatch im Charge-Fenster nutzbar; Hit nur auf unmodifizierte 6
- [ ] Counter-Offensive unterbricht die Alternation regelkonform
- [ ] HI-Eligibility über `can_heroic_intervene` (kein CHARACTER-Hardcode in chargephase)
- [ ] Kontext-Boxen nach Mockup-Freigabe des Nutzers umgesetzt
- [ ] `pytest --tb=short` grün, ≥80 %; Lint passt
- [ ] Bericht: manuelle Verifikationsliste + Zitat der Overwatch-/
      Counter-Offensive-Regelstellen aus core_rules.txt
- [ ] Status-Zeile in `docs/audit/plans/README.md` aktualisiert

## STOP conditions

- Die Overwatch-Regel in core_rules.txt weicht von „unmodifizierte 6" ab
  → Regeltext melden, nicht raten.
- Counter-Offensive-Timing kollidiert mit der A2-Logik aus Session 39
  (fought beim ersten Apply): wenn der Wechsel-Unterdrückungs-Flag-Ansatz
  `_advance_fight_turn_if_needed` verkompliziert statt vereinfacht → STOP,
  Alternativen vorlegen.
- Kontext-Box-Layout ohne Nutzer-Freigabe NICHT implementieren (Step 2/3).
- Ein bestehender Fight-Reihenfolge-Test wird rot → STOP (A2-Regression).

## Maintenance notes

- `reactive_stratagems_for` ist der EINE Einstiegspunkt für künftige
  reaktive GOs (Emergency Disembarkation, Auto-Pass-Morale …) — neue Events
  nur dort registrieren, keine Ad-hoc-Abfragen in Phase-Handlern.
- `spend_stratagem` ist jetzt die einzige Stelle für CP-Buchung von GOs —
  Reviewer: direkte `adjust_cp`-Aufrufe für Stratagems ablehnen.
