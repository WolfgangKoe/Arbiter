# Plan 030 — Conquering Tyrant UI-Bugfixes: atk_uid in Entry-Dicts + Selection-State-Reset

> **Executor-Anweisung:** Plan vollständig lesen. Beide Steps als isolierte Einheiten
> behandeln; nach jedem Step Vollsuite + Lint. STOP-Bedingungen sind bindend.
> Bug 2 zuerst (kleiner, isoliert), dann Bug 1 (mehr Test-Aufwand).
>
> **Drift-Check (zuerst ausführen):**
> `grep -n "atk_uid" src/uiLayout/_common.py | head -20`
> Erwartet: `atk_uid = entry.get("atk_uid", "")` in `_render_resolution_tab` —
> aber KEIN `"atk_uid"` in den `entries.append`-Blöcken der Ranged/Melee-Pfade.
> Wenn `"atk_uid"` bereits in BEIDEN `entries.append`-Blöcken vorkommt → Bug 1
> bereits gefixt, melden.
>
> `grep -n "reset_group_declaration_state" src/uiLayout/_common.py`
> Erwartet: Aufrufe in `render_group_cards` / `unitCard.py`, aber NICHT beim
> „All done — Continue"- und „↺ Reset Declaration"-Button in `render_attack_resolution`.
> Wenn `reset_group_declaration_state()` dort bereits steht → Bug 2 bereits gefixt, melden.

## Status

- **Priority**: P1 (HOCH) — beide Bugs reproduzierbar und aus manueller UI-Verifikation
  (S108) entstanden; blockieren korrekten Conquering-Tyrant-D2-Workflow.
- **Effort**: XS–S (Bug 2: zwei Zeilen; Bug 1: vier Zeilen + HTML-Output-Test).
- **Risk**: NIEDRIG — minimale Code-Änderungen, kein Refactoring; rein additive Ergänzungen.
- **Depends on**: 025 ✅ (Conquering Tyrant D2 `shoot_after_fall_back` verdrahtet).
- **Category**: Bugfix (Regressionstest PFLICHT für Bug 2; Unit-Test PFLICHT für Bug 1).

## Why this matters

Nach Plan 025 Step 5 ist `shoot_after_fall_back` (−1 Hit) Engine-seitig korrekt
verdrahtet. Zwei UI-Bugs verhindern aber die korrekte Anzeige und Bedienbarkeit:

- **Bug 1** — Der `−1`-Hit-Modifier aus Conquering Tyrant D2 wird nie im HIT-Block
  angezeigt (rot), weil `"atk_uid"` in den Entry-Dicts fehlt und die Engine-Fn
  daher ein leeres Dict auswertet → kein Modifier.
- **Bug 2** — Nach „All done — Continue" (oder „↺ Reset Declaration") bleibt
  `group_autosel_done_<uid>` im Session-State → beim erneuten Auswählen derselben
  Einheit greift Auto-Select nicht → Enemy-Button disabled → kein Ziel wählbar.
  Workaround bisher: Einheit erst abwählen (triggert `reset_group_declaration_state()`),
  dann erneut auswählen.

## Scope (betroffene Dateien)

- `src/uiLayout/_common.py` — Bug 1: zwei `entries.append`-Blöcke (Melee + Ranged);
  Bug 2: zwei Button-Handler (`Reset Declaration` + `All done — Continue`).
- `tests/uiLayout/test_group_flow.py` — Bug 2 Regressionstest (PFLICHT).
- `tests/uiLayout/test_common.py` oder `tests/uiLayout/test_resolution_tab.py` —
  Bug 1 Unit-Test (PFLICHT; kann in bestehende Datei oder neuen Test).

## Steps

### Step 1 — Bug 2: `reset_group_declaration_state()` nach „All done" + „Reset Declaration" (XS)

**Root-Cause:** `_common.py:render_attack_resolution` — zwei Button-Handler setzen
`attack_declaration` zurück, rufen aber `reset_group_declaration_state()` nicht auf.
Die `group_autosel_done_<uid>`-Flags bleiben deshalb im Session-State. Selbe Einheit
erneut auswählen → Auto-Select-Guard `autosel_flag == True` → kein Auto-Select →
`selected_model_group` bleibt `None` → `group_target_selectable` gibt `False` →
Enemy-Button `disabled=True`.

**Früheres Auftreten (S-Befund):** Commit `f365a3d` ("Bug 5 group_autosel_done_*
guard not cleared on phase change") — damaliger Fix deckte nur Phase-Wechsel via
`_reset_phase_state` (`game_state.py`), nicht den Post-All-done-Pfad.

**Konkrete Änderung in `src/uiLayout/_common.py`:**

An beiden Button-Handlern `reset_group_declaration_state()` ergänzen:

```python
# „↺ Reset Declaration"-Button (ca. Z. 1725–1727):
if st.button("↺ Reset Declaration", key="reset_decl"):
    st.session_state.attack_declaration = _empty_attack_declaration()
    reset_group_declaration_state()   # NEU — Bug 2 Fix
    st.rerun()

# „✓ All done — Continue"-Button (ca. Z. 1774–1776):
if st.button("✓ All done — Continue", type="primary", key="all_done"):
    st.session_state.attack_declaration = _empty_attack_declaration()
    reset_group_declaration_state()   # NEU — Bug 2 Fix
    st.rerun()
```

**Scoping-Pflichtschritt:**
`grep -rn "reset_group_declaration_state\|group_autosel_done" tests/` ausführen —
alle Treffer sichten, keine bestehenden Tests brechen (nur neue Tests erwartet).

**Regressionstest (PFLICHT) in `tests/uiLayout/test_group_flow.py`:**

```python
def test_all_done_clears_group_autosel_guard():
    """Regression: group_autosel_done_* muss gecleart sein, wenn Attack-Resolution
    abgeschlossen wird (All done / Reset Declaration), damit dieselbe Einheit
    in der gleichen Phase wieder auswählbar ist und Enemy-Targets klickbar werden.
    """
    session["group_autosel_done_warrior-uid"] = True
    session["attack_declaration"] = {"active": True}
    reset_group_declaration_state()
    assert "group_autosel_done_warrior-uid" not in session
```

**Verify:**
`pytest tests/uiLayout/test_group_flow.py -q` → grün.
Dann Vollsuite: `pytest --tb=short` → Coverage ≥ 92 %, Architektur-Gate grün.

**Manuelle UI-Verifikation:**
- Necron Warriors auswählen → Feindeinheit wählen → Resolution durchführen →
  „✓ All done — Continue" → Warriors erneut auswählen → Enemy-Button direkt klickbar (nicht disabled).
- Dasselbe nach „↺ Reset Declaration".

**Token-Schätzung:** ~5–8k (Sonnet).

---

### Step 2 — Bug 1: `"atk_uid"` in Entry-Dicts von `render_group_assignment` (S)

**Root-Cause:** `_common.py:render_group_assignment` — beide `entries.append`-Blöcke
(Melee ca. Z. 1595–1608, Ranged ca. Z. 1662–1673) übergeben kein `"atk_uid"`. Später
liest `_render_resolution_tab` (`_common.py:952`):

```python
atk_uid = entry.get("atk_uid", "")
```

Weil `"atk_uid"` fehlt, ist `atk_uid == ""`. Die Engine-Fn
`get_active_round_choice_shoot_after_fall_back(atk_faction, "")` schlägt in
`st.session_state[units_key_for(atk_player)].get("", {})` nach → leeres Dict →
`movement_choice` ist `None` → gibt `0` zurück → kein Modifier in `final_atk_mods` →
HIT-Block zeigt keinen −1-Debuff. (Modifier-Farbweg in `dice_compose.py:_modifier_color`
ist korrekt — der Modifier wird nur nie erreicht.)

**Belege:**
- `_common.py:_render_resolution_tab` — `entry.get("atk_uid", "")`
- `_common.py:render_group_assignment` — beide `entries.append`-Blöcke ohne `"atk_uid"`
- `_common.py:render_attack_resolution` — `atk_uid = decl["atk_uid"]` vorhanden (aber
  nicht in Entry-Dicts weitergegeben)
- `ability_engine.py:get_active_round_choice_shoot_after_fall_back` — korrekt verdrahtet

**Regelgrundlage (Wahapedia, `docs/work/wahapedia_necrons/faction_overview.txt` Z. 712–718):**
"This unit is eligible to shoot in a turn in which it Fell Back, but if it does,
then until the end of the turn, each time a model in this unit makes a ranged attack,
subtract 1 from that attack's hit roll."
→ −1 Hit Roll = Klasse A (App rechnet/erzwingt); muss rot angezeigt werden.

**Konkrete Änderung in `src/uiLayout/_common.py`:**

In `render_group_assignment` an beiden `entries.append`-Blöcken `"atk_uid": atk_uid`
eintragen (`atk_uid` ist im Scope — als Parameter übergeben, ca. Z. 1316):

```python
# Melee-Block (ca. Z. 1595–1608) — Beispiel:
entries.append({
    ...existing keys...,
    "atk_uid": atk_uid,   # NEU — Bug 1 Fix
})

# Ranged-Block (ca. Z. 1662–1673) — analog:
entries.append({
    ...existing keys...,
    "atk_uid": atk_uid,   # NEU — Bug 1 Fix
})
```

**Scoping-Pflichtschritt:**
`grep -rn "entries.append\|atk_uid" src/uiLayout/_common.py` — alle `entries.append`-
Stellen lokalisieren und sicherstellen, dass beide geänderten Blöcke vollständig sind.
`grep -rn "atk_uid" tests/` — bestehende Tests sichten, Migrationen notieren.

**Test (PFLICHT):**

Einfachster Ansatz (Unit-Test, kein Streamlit-Render) in `tests/uiLayout/test_common.py`
oder `tests/uiLayout/test_resolution_tab.py`:

1. Prüfen, dass die Entry-Building-Logik von `render_group_assignment` `"atk_uid"` in
   den Entry-Dicts enthält (Mock der Streamlit-Calls, nur Entry-Dict-Inhalt assertieren).
2. Integration: `get_active_round_choice_shoot_after_fall_back` mit korrekt befülltem
   Entry-Dict liefert `−1` wenn `movement_choice == "retreated"` gesetzt ist.

Für Render-Code: HTML-Output-Test via `st.markdown`-Mock, der generierten HTML-String
auf negativen Modifier-Wert prüft (entspricht roter Modifier-Badge).

**Verify:**
`pytest tests/uiLayout/ -q` → grün.
Dann Vollsuite: `pytest --tb=short` → Coverage ≥ 92 %, Architektur-Gate grün.

**Manuelle UI-Verifikation:**
- Conquering Tyrant D2 aktiv + Warriors haben Fall Back gemacht → Shooting Resolution
  HIT-Block: roter `−1` Modifier mit Label sichtbar (z.B. „Fall Back (−1 Hit)").
- Ohne Fall Back (stationary/moved): kein Modifier.
- Ohne D2-Direktive: kein Modifier auch nach Fall Back.

**Token-Schätzung:** ~8–12k (Sonnet).

---

## DoD-Checkliste (beide Steps)

1. **Regelkonform** — Wahapedia Z. 712–718 bestätigt −1 Hit Roll bei Fall Back ✅.
2. **Generisch** — beide Fixes enthalten keinen Fraktions-String; `atk_uid` ist ein
   State-Key, `reset_group_declaration_state()` ist bereits generisch ✅.
3. **Tests grün** — Vollsuite `pytest --tb=short`, Coverage ≥ 92 % nach jedem Step.
4. **Architektur-Gate** — nur `uiLayout/_common.py` geändert, kein Layer-Verstoß.
5. **Clean Code** — additive Minimal-Änderungen, kein Refactoring, `black`/`isort`/`ruff` sauber.
6. **UI manuell verifiziert** — Verifikationsschritte je Step benannt (s. o.); nie
   „fertig" ohne manuelle Prüfung.
7. **Artefakte aktuell** — `next_session.md` + `docs/goals/backlog.md` §0 aktualisieren;
   „Bug 5 Runde-2-Fernkampf-Zielwahl" und D2-Anzeige-Lücke abgehakt.

## STOP conditions

- Vorher grüner Test wird rot und steht nicht in der Migrations-Liste → STOP, Nutzer fragen.
- `reset_group_declaration_state()` hat unerwartete Seiteneffekte auf anderen State →
  STOP, Scope klären.
- `atk_uid` ist in `render_group_assignment` nicht im Scope (nicht als Parameter) →
  STOP, alternativen Ansatz klären (dann aus `decl["atk_uid"]` in `_render_resolution_tab`).
