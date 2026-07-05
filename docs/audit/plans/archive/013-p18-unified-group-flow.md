# Plan 013: P18 — Einheitlicher Gruppen-Flow für ALLE Einheiten + Ziele neben Untergruppen

> **Executor instructions**: Follow this plan step by step. Run every
> verification command and confirm the expected result before moving to the
> next step. If anything in the "STOP conditions" section occurs, stop and
> report — do not improvise. When done, update the status row for this plan
> in `docs/audit/plans/README.md`.
>
> **Drift check (run first)**:
> `git diff --stat f0f4e17..HEAD -- src/gameObjects/loader.py src/uiLayout/_common.py src/gameMechanic/shootingPhase.py src/gameMechanic/fightPhase.py src/uiLayout/unitCard.py`
> Erwartung: leer (kein Drift). Bei Abweichungen in den Dispatch-Stellen
> (s. Current state): STOP.

## Status

- **Priority**: P1 (HOCH — archive/ziel6.md §6n P18, vom Nutzer freigegebene Review-Runde 2)
- **Effort**: M–L
- **Risk**: MEDIUM (entfernt den Legacy-Deklarationspfad; viele Tests betroffen — erwartete Migrationen unten gelistet)
- **Depends on**: —
- **Category**: feature/UX + Architektur-Vereinheitlichung
- **Planned at**: commit `f0f4e17`, 2026-06-12

## Why this matters

Es gibt heute ZWEI Deklarations-Flows: den Gruppen-Flow (subUnitCards +
`render_group_assignment`) für Einheiten mit `model_groups` und den
Legacy-Flow (`render_attack_declaration`, Multiselect + Counter im
Center-Display) für homogene Einheiten. Doppelte UI-Logik, doppelte Bugs
(Stikkbombz-Cap, Budget-Deckelung etc. existieren nur im Gruppen-Pfad).
P18 (Nutzer-Entscheidung): **Einheiten ohne Untergruppen werden als EINE
Gruppe behandelt → ein einziger Flow für alles.** Zusätzlich sollen in der
Fight Phase die infrage kommenden Ziele (App kennt `melee_with`) direkt
neben den Untergruppen erscheinen, statt dass man sie im gegnerischen
Army-Listing per ▷ suchen muss.

## Current state

**Dispatch-Stellen (Gruppen- vs. Legacy-Pfad):**

| Stelle | Verhalten heute |
|---|---|
| `loader.py:1014-1017` | `_resolve_model_groups` nur wenn `unit.model_group_specs` aus YAML vorhanden; sonst `model_groups == []` |
| `game_state.py:181` | `group_models` init aus `u.model_groups` — leer bei homogenen Einheiten |
| `_common.py:1297-1300` | `render_attack_declaration` bricht für Gruppen-Einheiten ab; danach folgt der komplette Legacy-Body (Multiselect, Modell-Counter, atk_counter — Zeilen 1302–1515) |
| `shootingPhase.py:144-156` | `_active_shooting`: Gruppen-Einheit → `render_group_cards`; sonst Legacy-Waffenliste |
| `shootingPhase.py:205-231` | `_render_display`: Legacy-Einheit + Ziel → `render_attack_declaration` im Center |
| `shootingPhase.py:74-90` | `group_override` für die Verteidiger-Spalte nur im Gruppen-Flow |
| `fightPhase.py:462-464` | `_active_fight`: Gruppen-Einheit → `render_group_cards`; sonst Legacy-Caption-Liste |
| `fightPhase.py:529-568` | `_render_display`: Legacy-Pfad ruft `render_attack_declaration` |
| `fightPhase.py:403-415` | Verteidiger-Spalte: `render_group_assignment` nur im Gruppen-Flow |
| `unitCard.py:296-306` | ▷-Button: `toggle_group_target()` mit Fallback auf `selected_targets` (Legacy) |
| `_common.py:905-929` | `toggle_group_target`: Einzelmodell-Gruppe (`alive == 1`) → max 1 Ziel |
| `_common.py:881-902` | `group_target_selectable`: Fight → nur engaged; Shooting → friendly-melee-Sperre |

**Dataclass** (`unit.py:39-47`): `ModelGroup(id, name_en, count, weapons, priority)` —
alles vorhanden, was eine synthetische Gruppe braucht.

**Resolution** (`render_attack_resolution` / `_render_resolution_tab`) ist bereits
flow-agnostisch: sie liest nur `attack_declaration["entries"]` — KEINE Änderung nötig.

## Commands you will need

| Zweck | Befehl | Erwartet |
|-------|--------|----------|
| venv | `source .venv/bin/activate` | `(.venv)` |
| Lint | `ruff check src/ && black --check src/ && isort --check-only src/` | passt |
| Gruppen-Tests | `python -m pytest tests/uiLayout/test_group_flow.py tests/gameObjects/test_loader.py -q` | grün |
| Vollsuite | `pytest --tb=short` | grün, ≥80 % |
| App | `streamlit run src/app.py` | Port 8501 |

## Scope

**In scope**:
- `src/gameObjects/loader.py` — synthetische Einzelgruppe für Einheiten ohne `model_groups`
- `src/uiLayout/_common.py` — Auto-Select bei genau einer Gruppe; Ziel-Buttons neben Gruppen (Fight); Legacy-Body von `render_attack_declaration` entfernen
- `src/gameMechanic/shootingPhase.py`, `src/gameMechanic/fightPhase.py` — Legacy-Dispatch entfernen
- `src/uiLayout/unitCard.py` — ▷-Fallback auf `selected_targets` prüfen/anpassen
- Tests: Migration der Legacy-Deklarationstests auf den Gruppen-Pfad

**Out of scope** (NICHT anfassen):
- Verteidiger-Korrektur bei Schadenszuweisung → Plan 014
- `render_attack_resolution` / Resolution-Tabs — bleiben unverändert
- YAML-Daten — KEINE `model_groups` in `units.yaml` nachtragen; die
  synthetische Gruppe entsteht ausschließlich im Loader
- Charge Phase (`selected_targets` wird dort weiter direkt benutzt)

## Git workflow

- Branch: `feature/013-unified-group-flow`.
- Commit-Stil imperativ Englisch, z. B. `Unify attack declaration on the group flow`.
- Mehrere Commits erlaubt (sinnvolle Schnitte: Step 1+2 / Step 3 / Step 4).
- Nicht pushen/PR ohne Anweisung.

## Steps

### Step 1: Synthetische Einzelgruppe im Loader

In `loader.py` an der Stelle, wo Roster-Einheiten gebaut werden
(`loader.py:1014-1017`): wenn nach `_resolve_model_groups` (bzw. ohne Specs)
`unit.model_groups` leer ist UND die Einheit Waffen hat, eine synthetische
Gruppe erzeugen:

```python
ModelGroup(
    id="models",
    name_en=unit.name_en,
    count=<models der Roster-Einheit>,
    weapons=list(unit.weapons),
    priority=1,
)
```

WICHTIG: `count` muss exakt dem Wert entsprechen, den `_make_unit_state_dict`
in `game_state.py` als `models`-Init verwendet (dort nachsehen — Roster-`models`
bzw. `models_max`). `game_state.py:181` initialisiert `group_models` dann
automatisch korrekt; `_apply_group_losses`/`_restore_group_models` greifen ab
sofort für alle Einheiten (Verhalten identisch, da nur eine Gruppe).

**Verify**:
`python -m pytest tests/gameObjects/test_loader.py tests/gameMechanic/ -q` → grün.
Zusätzlich Mini-Check in Python-REPL: Necron-Roster laden → jede Einheit hat
`len(unit.model_groups) >= 1`.

### Step 2: Auto-Select bei genau einer Gruppe

`render_group_cards` (`_common.py:948`): Wenn die Einheit GENAU EINE Gruppe
mit `alive > 0` und nutzbaren Phasen-Waffen hat und noch keine
`group_decl` für sie existiert → `st.session_state.selected_model_group`
automatisch auf diese Gruppe setzen (kein zusätzlicher Klick auf ▶).
Die Karte zeigt dann direkt den „selektiert"-Zustand. Der Toggle-Button
bleibt (Abwählen möglich), aber bei einer einzigen Gruppe entfällt der
Pflicht-Klick.

ACHTUNG: `reset_group_declaration_state()` (Unit-Wechsel, Phasenwechsel,
Resolution-Start) setzt `selected_model_group = None` — das Auto-Select muss
danach beim nächsten Render wieder greifen (idempotent), darf aber eine
BEWUSSTE Abwahl nicht sofort überschreiben. Lösungsmuster: Auto-Select nur
ausführen, wenn `selected_model_group is None` UND ein Flag
`group_autosel_done_{uid}` für die aktuell selektierte Einheit noch nicht
gesetzt ist; Flag in `reset_group_declaration_state()` mitlöschen.

**Verify**: Manuell (Streamlit): Necron Warriors (homogen) in der Shooting
Phase selektieren → Gruppe ist sofort aktiv, ▷ am Ziel funktioniert direkt.

### Step 3: Legacy-Deklarationspfad entfernen

Jetzt ist `unit.model_groups` nie mehr leer → die Legacy-Zweige sind tot:

1. `_common.py`: `render_attack_declaration` — kompletten Body NACH dem
   Gruppen-Guard (Zeilen 1302–1515) löschen. Die Funktion selbst entfernen,
   wenn danach keine Call-Sites mehr existieren (siehe 2./3.), sonst auf einen
   schlanken Hinweis reduzieren.
2. `shootingPhase.py`: `_render_display` — Legacy-Aufruf von
   `render_attack_declaration` entfernen (der Gruppen-Flow läuft über die
   PlayerAreas, nicht über das Center-Display); `_active_shooting` —
   Legacy-Waffenliste (Zeilen 158–191) durch den Gruppen-Pfad ersetzen
   (`render_group_cards` für alle).
3. `fightPhase.py`: analog — `_render_display`-Legacy-Zweig (Zeilen 541–567)
   und `_active_fight`-Legacy-Liste (Zeilen 466–488) entfernen;
   die Hinweise „Charged units must fight first" / „Target is not engaged"
   in den Gruppen-Pfad übernehmen (gleiche Bedingungen, gleiche Texte).
4. `unitCard.py:296-306`: ▷-Fallback auf `selected_targets` bleibt für die
   CHARGE Phase erhalten (dort gibt es keinen Gruppen-Flow) — prüfen, dass
   `toggle_group_target` in Shooting/Fight immer greift (tut es, sobald
   `group_flow_attacker()` nie mehr None liefert bei selektierter Einheit)
   und in der Charge Phase weiterhin False liefert → Fallback aktiv.
5. `grep -n "render_attack_declaration" src/ tests/` → Call-Sites in `src/`
   müssen 0 sein (bzw. nur noch die Definition, falls behalten).

**Erwartete Test-Migrationen** (bekannter, vom Nutzer freigegebener
Verhaltensbruch — diese Tests auf den Gruppen-Pfad umstellen und im
Abschlussbericht auflisten): alle Tests, die `render_attack_declaration`
direkt aufrufen oder den Legacy-Multiselect/`decl_m_{uid}_{def_uid}`-Keys
testen (suchen mit `grep -rn "render_attack_declaration\|decl_m_\|decl_ws_" tests/`).
Wird ein Test rot, der NICHT in dieser Kategorie liegt: STOP.

**Verify**: `pytest --tb=short` → grün (nach Migration), Coverage ≥ 80 %.

### Step 4: Ziele neben den Untergruppen (Fight Phase) — MOCKUP ZUERST

**⚠️ Vor Implementierung: Kurz-Mockup dem Nutzer zeigen und Freigabe abwarten**
(CLAUDE.md: UI-Varianten-Entscheidung). Vorschlag für das Mockup:

In `render_group_cards`, innerhalb der selektierten Gruppe (`is_sel`-Zweig,
`_common.py:1015-1021`): statt nur „Designate a target (▷) from the enemy
army list." die engaged Gegner als Toggle-Buttons direkt anbieten:

```
◀ Boss Nob (1)        ← selektierte Gruppe
   4 attacks
   power klaw, slugga
   Ziele (engaged):
   [＋ Necron Warriors]   [✓ Skorpekh Destroyers]
```

- Quelle: `atk_state["melee_with"]` (nur Fight Phase; Shooting behält das
  Army-Listing-▷, da dort jede sichtbare Einheit legales Ziel sein kann).
- Klick auf einen Ziel-Button → `toggle_group_target(def_faction, def_uid)`
  (identische Logik wie ▷; Anzeige ✓ wenn zugewiesen).
- Das Army-Listing-▷ bleibt funktional (zwei Wege, eine Logik).
- Zerstörte/Reserve-Ziele filtern (wie `_render_mortal_after_melee` es
  vormacht, `fightPhase.py:167-173`).

**Verify**: Manuell (Streamlit): Fight Phase, Boyz in Melee mit 2 Feinden →
beide erscheinen als Buttons unter der selektierten Gruppe; Toggle setzt/
entfernt das Ziel; ▷ im Army-Listing spiegelt denselben Zustand.

### Step 5: Vollsuite + Lint + Doku

- `pytest --tb=short` → grün, ≥80 %.
- `ruff check src/ && black --check src/ && isort --check-only src/` → passt.
- `docs/spec/unit_states.md` (Gruppen-Flow-Abschnitt): „Einheiten ohne
  YAML-`model_groups` erhalten im Loader eine synthetische Einzelgruppe
  `models`" ergänzen. `docs/spec/loader_contract.md` analog.

## Test plan

- NEU `tests/gameObjects/test_loader.py`: homogene Einheit (z. B. Necron
  Warriors) hat nach Roster-Load genau eine Gruppe `models` mit
  `count == models`-Init und allen Unit-Waffen.
- NEU `tests/uiLayout/test_group_flow.py`: Auto-Select-Verhalten (eine Gruppe
  → `selected_model_group` gesetzt; nach `reset_group_declaration_state` beim
  nächsten Render wieder gesetzt).
- MIGRIERT: Legacy-Deklarationstests → Gruppen-Pfad (Liste im Abschlussbericht).
- Bestehende Gruppen-Tests (Boyz, Nobz) bleiben unverändert grün.

## Done criteria

ALLE müssen gelten:

- [x] Jede Roster-Einheit hat `len(model_groups) >= 1` (Loader-Test beweist es)
- [x] `grep -rn "render_attack_declaration" src/` → 0 Call-Sites
- [x] Auto-Select bei Einzelgruppe funktioniert (Test + manuell noch ausstehend)
- [x] Fight Phase: engaged Ziele als Buttons neben der selektierten Gruppe
      (nach Mockup-Freigabe), ▷ im Army-Listing konsistent
- [x] `pytest --tb=short` grün, Coverage ≥ 80 %; Lint passt
- [ ] Manuelle Verifikation ausstehend (Shooting homogen, Shooting Gruppen,
      Fight homogen, Fight Gruppen, Pistol-in-Melee, Grenade-Cap, Charge-▷)
- [x] Status-Zeile in `docs/audit/plans/README.md` aktualisiert

## STOP conditions

- Ein Test wird rot, der NICHT in der Kategorie „Legacy-Deklarationspfad"
  liegt → melden, nicht anpassen.
- `_make_unit_state_dict` initialisiert `models` aus einer Quelle, die zum
  Loader-Zeitpunkt nicht verfügbar ist (z. B. Setup-UI-Eingabe) → melden;
  dann muss die synthetische Gruppe stattdessen in `game_state` entstehen
  (Designentscheidung des Nutzers).
- Die Charge Phase nutzt `selected_targets` an einer Stelle, die durch den
  ▷-Umbau bricht → melden.
- Step 4 ohne Mockup-Freigabe des Nutzers NICHT implementieren.

## Maintenance notes

- Ab diesem Plan gilt: **Es gibt nur noch EINEN Deklarations-Flow.** Neue
  Deklarations-Features (z. B. Plan 014 Korrektur-UI) bauen ausschließlich
  auf `render_group_cards`/`render_group_assignment` auf.
- Die synthetische Gruppe `models` ist ein Loader-Artefakt — sie darf NIE in
  YAML auftauchen. Reviewer: `model_groups` mit nur einem Eintrag in
  `units.yaml` ablehnen (überflüssig).
