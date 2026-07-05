# Plan 035: `active_buffs` überleben den Zugwechsel — Expiry „bis zur nächsten eigenen Command Phase" korrekt umsetzen

> **Executor instructions**: Schritt für Schritt folgen, jede Verifikation
> ausführen. Bei STOP-Bedingung: stoppen und berichten. Am Ende Status-Zeile in
> `docs/audit/plans/README.md` aktualisieren.
>
> **Drift check (zuerst ausführen)**:
> `git diff --stat f6c464a..HEAD -- src/gameMechanic/game_state.py src/gameMechanic/commandPhase.py tests/gameMechanic/test_game_state.py`
> Bei Änderungen: Exzerpte gegen Live-Code prüfen; Abweichung → STOP.
> Hinweis: Plan 033 ändert `next_phase()` in derselben Datei — sein Diff ist
> **erwartete** Drift; nur der `else`-Zweig-Tausch aus Plan 033 ist zulässig.

## Status

- **Priority**: P1
- **Effort**: M
- **Risk**: MED (geteilter Reset-Pfad für beide Spieler)
- **Depends on**: 033 (gleiche Datei `game_state.py` — strikt nacheinander, 033 zuerst)
- **Category**: bug
- **Planned at**: commit `f6c464a`, 2026-07-05

## Why this matters

Aktivierte Command-Fähigkeiten wie „My Will Be Done"
(`data/wh40k_9e/necrons/unit_abilities.yaml:15`: *"Until the start of your next
Command phase … add 1 to that attack's hit roll"*) sollen regelkonform den
**gesamten gegnerischen Zug** überdauern (z. B. für die gegnerische Fight Phase,
in der die gebuffte Einheit mitkämpft). Tatsächlich leert `_reset_turn_state()`
die `active_buffs` **jeder** Einheit **beider** Spieler bei **jedem**
Spielerwechsel. Der Buff wirkt also nur im eigenen Zug; die UI
(`commandPhase.py:188`: „Active — … until your next Command Phase.") und die
Badges zeigen ihn trotzdem weiter als aktiv, und das Nutzungsbudget ist
verbraucht. Die Regel ist de facto halbiert, ohne dass es sichtbar wird.

## Current state

**Der Bug** — `src/gameMechanic/game_state.py:556-568`, `_reset_turn_state()`:

```python
def _reset_turn_state() -> None:
    st.session_state.pending_mortal_undo = None
    current_round = st.session_state.get("round", 1)
    for key in ("p1_units", "p2_units"):
        for state in st.session_state[key].values():
            flags = state["turn_flags"]
            for flag in flags:
                flags[flag] = False
            state["lost_models_this_turn"] = 0
            state["fled_models_this_turn"] = 0
            state["movement_choice"] = "stationary"
            state["movement_chosen"] = False
            state["active_buffs"] = []        # ← leert BEIDE Spieler bei JEDEM Zugwechsel
```

Aufgerufen wird `_reset_turn_state()` ausschließlich im Spielerwechsel-Zweig von
`next_phase()` (`game_state.py:627-635`) — **nachdem** `st.session_state.active`
bereits auf den neuen aktiven Spieler gesetzt wurde:

```python
    elif idx >= num - 1:  # Morale done → switch player
        new_active = second if st.session_state.active == first else first
        st.session_state.active = new_active
        if new_active == first:
            st.session_state.round += 1
            _reset_round_choice_state()
        _reset_turn_state()
```

**Die intendierte Semantik** existiert bereits — `src/gameMechanic/commandPhase.py:161-173`
(`_render_buff_roll_ability`) führt pro Fähigkeit `active_since_round` und räumt
die Buffs der Ziele erst ab, wenn die Runde weitergezählt hat:

```python
    if active_since_round is not None and state["round"] > active_since_round:
        for t in targets:
            if t in units_state:
                bufs: list[dict] = units_state[t].get("active_buffs", [])
                units_state[t]["active_buffs"] = [
                    b for b in bufs if b.get("ability_id") != ability_id
                ]
```

**Konsumenten** der `active_buffs` (dürfen sich nicht ändern):
- `src/uiLayout/_common.py:488-496` (`_collect_atk_modifiers`): `effect_type == "buff_roll"` → +1 hit.
- `src/uiLayout/_common.py:188` (Badges): rendert `badge_label` je Buff.

**Zuordnung Spieler ↔ Unit-Key**: `p1_units` gehört zu `first_player`,
`p2_units` zu `second_player` (Initialisierung `game_state.py:409-412`). Es gibt
einen bestehenden Helper, der Faction → Units-Key auflöst (wird z. B. in
`moralePhase.py` als `units_key_for` importiert) — per
`grep -n "def units_key_for" src/gameMechanic/game_state.py` lokalisieren und
wiederverwenden.

## Zielsemantik (die Regel, die der Fix implementiert)

„Until the start of your next Command phase" = Der Buff erlischt genau dann, wenn
der **Besitzer** (der Spieler, dessen Einheiten den Buff tragen — Buffs zielen
immer auf eigene Einheiten) wieder am Zug ist. Da `_reset_turn_state()` genau am
Zugwechsel läuft und `st.session_state.active` dann schon der **neue** aktive
Spieler ist, gilt:

> In `_reset_turn_state()` werden `active_buffs` nur noch für die Einheiten des
> **neuen aktiven Spielers** geleert (dessen „nächste Command Phase" beginnt
> jetzt). Die Buffs des nicht-aktiven Spielers bleiben stehen.

Beispielverläufe (beide müssen als Test existieren):
- First Player aktiviert MWBD in seiner Command Phase (Runde N). Zugwechsel zum
  Second Player → Buff bleibt (First ist nicht der neue Aktive). Zugwechsel zurück
  zu First (Runde N+1 beginnt) → Buff wird geleert. ✔ regelkonform.
- Second Player aktiviert MWBD (Runde N, zweite Zughälfte). Zugwechsel zu First
  (Runde N+1) → Buff bleibt. Zugwechsel zu Second → geleert. ✔ regelkonform
  (überdauert Firsts kompletten Zug der Runde N+1).

## Commands you will need

| Purpose | Command | Expected on success |
|---|---|---|
| Vollsuite + Coverage | `pytest --tb=short` | exit 0, Coverage ≥ 99 % |
| Betroffene Tests | `pytest tests/gameMechanic/test_game_state.py --no-cov -q` | all pass |
| Lint | `ruff check src/ && black --check src/ && isort --check-only src/` | exit 0 |

## Scope

**In scope:**
- `src/gameMechanic/game_state.py` — nur die `active_buffs`-Zeile in
  `_reset_turn_state()` (wird bedingt) und ggf. ein kleiner Helper.
- `tests/gameMechanic/test_game_state.py` — zwei bestehende Tests migrieren,
  neue Tests ergänzen.

**Out of scope:**
- `commandPhase.py:161-173` — die dortige `active_since_round`-Räumung bleibt
  unverändert als zweite Verteidigungslinie (räumt auch, wenn ein Spieler den
  Buff-Owner betrachtet, und setzt das Nutzungsbudget zurück).
- `_collect_atk_modifiers` / Badges (`_common.py`) — Konsumenten, nicht anfassen.
- Alle anderen Resets in `_reset_turn_state()` (`turn_flags`,
  `lost_models_this_turn`, `movement_choice` …) — die sind korrekt beidseitig
  pro Zug.

## Git workflow

- Branch: `fix/035-active-buffs-expiry`
- Commit z. B. `Expire active buffs only when their owner's next turn begins`
- Nicht pushen ohne Anweisung.

## Steps

### Step 1: Besitzer-bedingtes Leeren implementieren

In `_reset_turn_state()` die Zeile `state["active_buffs"] = []` aus der
beidseitigen Schleife herausziehen. Neuer Block (nach der bestehenden Schleife
oder integriert — Lesbarkeit entscheidet):

```python
    # "Until the start of your next Command phase": Buffs erlöschen genau dann,
    # wenn ihr Besitzer wieder am Zug ist. st.session_state.active ist an dieser
    # Stelle bereits der NEUE aktive Spieler (next_phase setzt active vor dem
    # Reset) — also werden nur dessen Einheiten geleert.
    new_active = st.session_state.get("active")
    for key, player in (
        ("p1_units", st.session_state.get("first_player")),
        ("p2_units", st.session_state.get("second_player")),
    ):
        if player == new_active:
            for state in st.session_state[key].values():
                state["active_buffs"] = []
```

Falls `units_key_for(faction)` existiert (grep, s. o.), stattdessen diesen Helper
nutzen — keine zweite Mapping-Logik erfinden.

**Verify**: `pytest tests/gameMechanic/test_game_state.py --no-cov -q` →
**genau 2 erwartete Failures** (siehe Step 2), sonst nichts.

### Step 2: Erwartete Test-Migrationen (Rote-Tests-Policy: NUR diese zwei)

Diese beiden Tests kodieren das alte (fehlerhafte) Blanket-Clearing und werden
durch Step 1 rot — sie sind die **einzigen** erwarteten Migrationen:

1. `tests/gameMechanic/test_game_state.py:205`
   `test_reset_turn_state_clears_active_buffs` — asserted bisher, dass `p1_units`
   **und** `p2_units` geleert werden (Zeilen 221-222).
2. `tests/gameMechanic/test_game_state.py:764`
   `TestResetTurnState.test_clears_active_buffs` — asserted Leerung für `p1_units`.

Beide auf die neue Semantik umschreiben: Es wird nur die Seite geleert, deren
Spieler == `active` ist. Testnamen sprechend anpassen, z. B.
`test_reset_turn_state_clears_active_buffs_only_for_new_active_player`.

**Verify**: `pytest tests/gameMechanic/test_game_state.py --no-cov -q` → all pass.

### Step 3: Neue Verhaltens-Tests (die eigentliche Regression)

Auf `next_phase()`-Ebene (Integrationspfad, Muster wie in Plan 033 Step 2):

1. `test_buff_survives_switch_to_opponent` — Buff auf `p1_units`-Einheit,
   `active` = first, `phase_idx` = 7 → `next_phase()` (Wechsel zu second) →
   Buff noch vorhanden.
2. `test_buff_cleared_when_owner_turn_returns` — danach erneut `phase_idx` = 7
   → `next_phase()` (Wechsel zurück zu first) → Buff geleert.
3. `test_second_player_buff_survives_full_first_turn` — Buff auf `p2_units`,
   Wechsel zu first → bleibt; Wechsel zu second → geleert.

**Verify**: `pytest tests/gameMechanic/test_game_state.py --no-cov -q` → all pass, 3 neue Tests.

### Step 4: Vollsuite + Lint

**Verify**: `pytest --tb=short` → exit 0, Coverage ≥ 99 %.
**Verify**: `ruff check src/ && black --check src/ && isort --check-only src/` → exit 0.

## Test plan

Siehe Steps 2–3: zwei migrierte, drei neue Tests, alle in
`tests/gameMechanic/test_game_state.py`.

## Done criteria

- [ ] `pytest --tb=short` exit 0, Coverage ≥ 99 %
- [ ] Die 2 migrierten + 3 neuen Tests sind grün
- [ ] `_reset_turn_state()` leert `active_buffs` nur noch für den neuen aktiven Spieler
- [ ] `git status`: nur In-Scope-Dateien geändert
- [ ] Status-Zeile in `docs/audit/plans/README.md` aktualisiert

## STOP conditions

- Ein **anderer** als die zwei in Step 2 genannten Tests wird rot →
  Sicherheitsnetz-Regel: auflisten, Nutzer fragen, nicht anpassen.
- `_reset_turn_state()` hat inzwischen weitere Aufrufer als den
  Spielerwechsel-Zweig (`grep -rn "_reset_turn_state" src/`) — die Annahme
  „active ist beim Aufruf schon der neue Spieler" gilt dann evtl. nicht überall.
- Es zeigt sich, dass Buffs auch auf **gegnerische** Einheiten gelegt werden
  können (Debuff-Fall) — dann greift die Besitzer-Heuristik „Buff liegt auf
  eigener Einheit" nicht; berichten statt improvisieren.

## Maintenance notes

- Die Expiry lebt jetzt an zwei Stellen: zentral (Besitzer-Zugbeginn in
  `_reset_turn_state`) und lokal (`commandPhase.py:164`, `active_since_round`,
  räumt zusätzlich das Nutzungsbudget). Das ist beabsichtigte Redundanz; wer
  eine der beiden entfernt, muss die andere prüfen.
- Künftige Buff-Typen mit anderer Dauer („until end of turn") brauchen ein
  explizites Dauer-Feld am Buff-Eintrag — dann diese pauschale
  Besitzer-Regel durch eintragsbasierte Expiry ersetzen (nicht vorher).
- Reviewer-Fokus: Verhalten bei Mirror-Matches (gleiche Fraktion beidseitig) —
  die Zuordnung läuft über Spieler-Slots (`first_player`/`second_player`), nicht
  über Fraktionsnamen; `player == new_active`-Vergleich muss Slot-Namen nutzen.
