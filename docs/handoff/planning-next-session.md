<!-- READY -->
## Planning — 2026-06-27 (S108)

**Priorität:** P1   **Scope:** Zwei Conquering-Tyrant-Bugs fixen: D2-Debuff-Anzeige (−1 Hit fehlt in UI) + hängender Selection-State bei Zielauswahl (wiederkehrender Bug 5).

---

## Kontext (was vorher war)

S107 schloss Plan 025 (Necron-Protokolle 9E-konform) ab. Bugfix ffcdfe2 erlaubt
Schießen nach Fall Back. Nun zwei neue Bugs aus manueller UI-Verifikation.

---

## Bug 1 — D2-Debuff-Anzeige fehlt (−1 Hit wird nicht rot angezeigt)

### Root-Cause-Hypothese

**Ort:** `src/uiLayout/_common.py:render_group_assignment` (ca. Z. 1662–1673)

**Ursache:** In `render_group_assignment` baut `entries.append(...)` die Eintrags-Dicts auf
(für die spätere Resolution). Diese Dicts enthalten die Zieldaten, Waffendaten,
Modell-Zahl — aber KEIN `"atk_uid"`. Dasselbe gilt für den anderen Pfad (Z. 1595–1608).

Später liest `_render_resolution_tab` den Angreifer-Key aus:
```python
# _common.py:952
atk_uid = entry.get("atk_uid", "")
```
Weil `"atk_uid"` fehlt, ist `atk_uid == ""`.

`get_active_round_choice_shoot_after_fall_back(atk_faction, "")` schlägt dann in
`st.session_state[units_key_for(atk_player)].get("", {})` nach → leeres Dict →
`movement_choice` ist `None`, nicht `"retreated"` → gibt `0` zurück → kein Modifier
wird zu `final_atk_mods` hinzugefügt → HIT-Block zeigt keinen −1-Debuff.

Der Modifier-Farbweg ist korrekt: `_modifier_color` in `dice_compose.py:163–176` gibt
`_DEBUFF_COLOR_HEX` (rot) für `value < 0` zurück — aber der Modifier wird nie erreicht.

**Belege:**
- Modifier fehlt: `_common.py:952` `atk_uid = entry.get("atk_uid", "")` — kein `"atk_uid"` in entry-Dict
- Entry-Dicts ohne `atk_uid`: `_common.py:1595–1608` (Melee) und `1662–1673` (Ranged) — beide `entries.append`-Blöcke
- Korrekte atk_uid-Nutzung eine Ebene höher: `_common.py:1712` in `render_attack_resolution`
  liest `atk_uid = decl["atk_uid"]` — aber das wird nicht in den Entry-Dicts weitergegeben
- Engine-Fn korrekt implementiert: `ability_engine.py:290–308` prüft `movement_choice == "retreated"`

**Regel (Wahapedia, docs/work/wahapedia_necrons/faction_overview.txt Z. 712–718):**
"This unit is eligible to shoot in a turn in which it Fell Back, but if it does,
then until the end of the turn, each time a model in this unit makes a ranged attack,
subtract 1 from that attack's hit roll."

Der −1-Modifier ist Klasse A (App rechnet und zeigt), muss **rot** (Debuff) erscheinen.

### Konkrete Änderung

**Datei:** `src/uiLayout/_common.py`

An beiden `entries.append`-Stellen (Z. 1595–1608 Melee, Z. 1662–1673 Ranged) das Feld
`"atk_uid": atk_uid` in das Dict aufnehmen. `atk_uid` ist im Scope von
`render_group_assignment` (wird als Parameter hereingegeben, Z. 1316).

Alternativ: `_render_resolution_tab` aus `decl["atk_uid"]` lesen statt aus `entry`.
Aber der Entry-Ansatz ist konsistenter (das Entry-Dict ist self-contained).

### Betroffene Dateien

- `src/uiLayout/_common.py` — `render_group_assignment`: beide `entries.append`-Blöcke
- `tests/uiLayout/test_common.py` oder neues `tests/uiLayout/test_resolution_tab.py` — Test

### Test-Strategie

Laut Test-Mandat: Render-Code (`_render_resolution_tab`) braucht einen Test, der den
HTML-Output prüft (nicht rein Mock-basiert). Da `_render_resolution_tab` Streamlit direkt
aufruft (st.markdown), kann der Test über den `fall_back_hit_mod`-Rückgabewert der
Engine-Funktion prüfen.

Einfachster Ansatz (Unit-Test, kein Streamlit-Render):
- Prüfen, dass `render_group_assignment` (oder die Entry-Building-Logik) `"atk_uid"` korrekt
  in die Entry-Dicts schreibt.
- Separater Integration-Test: `get_active_round_choice_shoot_after_fall_back` mit korrekt
  ausgefülltem Entry-Dict gibt `−1` zurück.

Für Render-Code: HTML-Output-Test via `st.markdown`-Mock der den generierten HTML-String
auf `modifier_die_pair_html` mit negativem `value` prüft (entspricht rotem Modifier).

### DoD-Check Bug 1

1. **Regelkonform:** Wahapedia Z. 712–718 bestätigt: −1 Hit Roll — ✅ gecheckt.
2. **Generisch:** Fix ist generisch (kein Fraktions-String; `atk_uid` ist ein State-Key,
   kein Fraktionsname) — ✅ kein Generic-src-Problem.
3. **Tests grün:** Vollsuite + Coverage ≥ 92 % nach Fix prüfen.
4. **Architektur-Gate:** Keine Layer-Verletzung (Render-Code bleibt in uiLayout).
5. **Clean Code:** Minimale Änderung — nur fehlende Key in zwei Dict-Literale eintragen.
6. **UI manuell verifizieren:**
   - Conquering Tyrant D2 aktiv + Warriors haben Fall Back gemacht → Shooting Resolution
     HIT-Block: roter `−1` Modifier mit Label (z.B. „Conquering Tyrant (Fall Back)") sichtbar.
   - Ohne Fall Back (stationary/moved): kein Modifier.
   - Ohne D2-Direktive: kein Modifier auch nach Fall Back.
7. **Artefakte:** `next_session.md` + `docs/goals/backlog.md` §0 Zeile „(d) 025 Step 5" abhaken.

### Token-Schätzung Bug 1

~8–12k (Sonnet). Minimale Code-Änderung; Hauptaufwand ist der HTML-Output-Test.

---

## Bug 2 — Hängender Selection-State bei Zielauswahl (Bug-5-Regression)

### Root-Cause-Hypothese

**Ort:** `src/uiLayout/_common.py:1774–1776` („All done — Continue"-Button)
und `src/uiLayout/_common.py:1725–1727` („↺ Reset Declaration"-Button)

**Ursache:** Wenn der Nutzer eine vollständige Attack-Resolution abschließt (alle Tabs
applied → „All done — Continue"), wird nur `attack_declaration` zurückgesetzt:

```python
# _common.py:1775
st.session_state.attack_declaration = _empty_attack_declaration()
```

`reset_group_declaration_state()` wird NICHT aufgerufen — die `group_autosel_done_<uid>`-Flags
bleiben im Session-State.

Wählt der Nutzer danach **dieselbe Einheit erneut** aus, prüft `render_group_cards`:

```python
# _common.py:1338
if sel_gid is None and not st.session_state.get(autosel_flag):
    # auto-select code...
```

`autosel_flag` ist noch `True` → Auto-Select läuft nicht →
`st.session_state.selected_model_group` bleibt `None` →
`group_target_selectable(def_faction, def_uid)` gibt `False` zurück (Z. 1216) →
Enemy-Unit-Button im unitCard ist `disabled=True` → Nutzer kann kein Ziel wählen.

**Workaround des Nutzers:** Eigene Einheit abwählen (unitCard-Klick) →
`reset_group_declaration_state()` wird aufgerufen (unitCard.py Z. 292–293) →
Flag wird gecleart → erneut auswählen → Auto-Select greift.

**Früheres Auftreten:** Commit `f365a3d` ("Fix round-choice directive lifecycle +
group-autosel target-selection bugs") identifizierte diesen Bug als "Bug 5":
"group_autosel_done_* guard was never cleared on phase change". Damaliger Fix: Clearing
in `_reset_phase_state` (`game_state.py:521`). Dieser Fix deckt Phase-Wechsel aber NICHT
den Fall „gleiche Phase, gleiche Einheit, neue Deklaration nach All-done".

### Konkrete Änderung

**Datei:** `src/uiLayout/_common.py`

An beiden Stellen, wo `attack_declaration` zurückgesetzt wird, zusätzlich
`reset_group_declaration_state()` aufrufen:

```python
# Z. 1725–1727 (Reset Declaration):
if st.button("↺ Reset Declaration", key="reset_decl"):
    st.session_state.attack_declaration = _empty_attack_declaration()
    reset_group_declaration_state()   # NEU — Bug 2 Fix
    st.rerun()

# Z. 1774–1776 (All done — Continue):
if st.button("✓ All done — Continue", type="primary", key="all_done"):
    st.session_state.attack_declaration = _empty_attack_declaration()
    reset_group_declaration_state()   # NEU — Bug 2 Fix
    st.rerun()
```

### Betroffene Dateien

- `src/uiLayout/_common.py` — zwei Stellen: „Reset Declaration" + „All done — Continue"
- `tests/uiLayout/test_group_flow.py` — Regressionstest (Pflicht)

### Test-Strategie (Regressionstest — PFLICHT)

Neuer Test in `tests/uiLayout/test_group_flow.py`:

```
def test_all_done_clears_group_autosel_guard():
    """Regression: group_autosel_done_* must be cleared when attack resolution
    completes (All done / Reset Declaration), so re-selecting the same unit
    in the same phase triggers auto-select and enemy targets become selectable.
    """
    session["group_autosel_done_warrior-uid"] = True
    session["attack_declaration"] = {"active": True, ...}
    # Simuliere "All done" → reset_group_declaration_state() muss laufen
    reset_group_declaration_state()
    assert "group_autosel_done_warrior-uid" not in session
```

Zweiter Test: `group_target_selectable` gibt `True` zurück, wenn `selected_model_group`
nach Auto-Select gesetzt ist (existiert bereits in `test_group_flow.py`, Lücke ist der
Post-All-done-Pfad).

### DoD-Check Bug 2

1. **Regelkonform:** Keine Regeländerung — State-Management-Fix.
2. **Generisch:** `reset_group_declaration_state()` ist bereits generisch (kein Fraktions-String).
3. **Tests grün:** Regressionstest + Vollsuite ≥ 92 % prüfen.
4. **Architektur-Gate:** Nur uiLayout-Änderung, kein Layer-Verstoß.
5. **Clean Code:** Zwei-Zeilen-Ergänzung, kein Refactoring nötig.
6. **UI manuell verifizieren:**
   - Necron Warriors (eine Gruppe) auswählen → Feindeinheit wählen → Resolution
     durchführen → „All done — Continue" klicken → Warriors erneut auswählen →
     Enemy-Button muss direkt klickbar sein (nicht disabled).
   - Auch „↺ Reset Declaration" → dann erneut auswählen → Enemy-Button klickbar.
7. **Artefakte:** `next_session.md` + Carry-over-Liste aktualisieren
   („Bug 5 Runde-2-Fernkampf-Zielwahl" → abgehakt).

### Token-Schätzung Bug 2

~5–8k (Sonnet). Sehr minimale Code-Änderung, Hauptaufwand ist der Regressionstest
plus manuelle UI-Verifikation.

---

## Aufgaben-Übersicht

| Aufgabe | Effort | Token-Schätzung | Modus | Tier |
|---------|--------|-----------------|-------|------|
| Bug 1 — D2 −1-Hit-Anzeige (atk_uid in Entry) | S | ~8–12k | Gate | Sonnet |
| Bug 2 — Selection-State-Reset nach All-done | XS | ~5–8k | Gate | Sonnet |

**Empfohlene Reihenfolge:** Bug 2 zuerst (kleiner, isoliert, kein Risiko von Nebeneffekten),
dann Bug 1 (etwas mehr Test-Aufwand). Beide können in einem Commit, wenn alle Tests grün.

**Gesamt-Schätzung:** ~13–20k Token (Sonnet-Executor).

---

## Offene Fragen / NEEDS-DECISION

Keine offenen Entscheidungen für den Stakeholder — beide Root-Causes sind eindeutig
identifiziert und die Fixes sind minimal und nicht mehrdeutig.

---

## Selbstprüf-Checkliste

- [x] Beide Bugs mit Root-Cause-Hypothese belegt (Datei:Funktion per grep/Read verifiziert)
  - Bug 1: `_common.py` Z. 952 `entry.get("atk_uid", "")` + Z. 1595–1608 / 1662–1673 (kein `atk_uid`)
  - Bug 2: `_common.py` Z. 1775 + 1726 (kein `reset_group_declaration_state()` nach Reset/All-done)
- [x] Conquering Tyrant D2-Regel gegen docs/work/wahapedia_necrons/faction_overview.txt geprüft
  (Z. 712–718: "subtract 1 from that attack's hit roll")
- [x] Früheres Auftreten von Bug 2 gefunden: Commit f365a3d, "Bug 5 group_autosel_done_*
  guard not cleared on phase change" — neues Auftreten ist derselbe Flag-Mechanismus,
  aber ausgelöst durch "All done — Continue" statt Phase-Wechsel
- [x] Vollständige Dateiliste je Bug (s. oben — je 2 Dateien)
- [x] Test-Strategie je Bug benannt (Bug 2: Regressionstest PFLICHT in test_group_flow.py)
- [x] Token-Schätzungen vorhanden (8–12k Bug 1, 5–8k Bug 2, ~13–20k Gesamt)
