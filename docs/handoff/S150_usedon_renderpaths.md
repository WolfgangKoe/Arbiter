STATUS: ANSWERED

## Used-On Badge: Alle Render-Pfade und Datenquellen

### 1. Zentrale Stratagem-Liste (gameProtocoll.py)

**Datei:Zeile:** `src/uiLayout/gameProtocoll.py:350`
**Funktion:** `_render_stratagem_column`
**Datenquelle Codezeilen:**
- Zeile 335: `stratagem_used_elsewhere_unit_name(player, strat.id)` — liest **gespeicherten** State
- Zeile 329: `state, locked_reason = _go_state_and_reason(..., stratagem_used_elsewhere_unit_name(player, strat.id))`
- Zeile 357: `locked_reason=locked_reason` an `render_go_card` übergeben

**Badge-Rendering:** `src/uiLayout/goCard.py:199-202`
- Zeile 199-202: HTML-String mit `"used on {locked_reason}"` wenn `state == "used_elsewhere"`

---

### 2. Advance Reroll Karte (movementPhase.py)

**Datei:Zeile:** `src/gameMechanic/movementPhase.py:325`
**Funktion:** `_render_advance_reroll_card`
**Datenquelle Codezeilen:**
- Zeile 323: `stratagem_used_elsewhere_unit_name(faction, strat.id)` — liest **gespeicherten** State
- Zeile 315: `card_state, reason = _advance_reroll_state(..., stratagem_used_elsewhere_unit_name(faction, strat.id))`
- Zeile 332: `locked_reason=reason` an `render_go_card` übergeben

**Badge-Rendering:** `src/uiLayout/goCard.py:199-202` (gleich wie Pfad 1)

---

### 3. Reactive Stratagem Boxes (mehrere Phasen)

**Datei:Zeile:** `src/uiLayout/_common.py:868`
**Funktion:** `render_reactive_stratagem_box`
**Datenquelle Codezeilen:**
- Zeile 857: `stratagem_used_elsewhere_unit_name(faction, strat.id)` — liest **gespeicherten** State
- Zeile 851: `state, locked_reason = _reactive_go_state(..., stratagem_used_elsewhere_unit_name(faction, strat.id))`
- Zeile 875: `locked_reason=locked_reason` an `render_go_card` übergeben

**Badge-Rendering:** `src/uiLayout/goCard.py:199-202` (gleich wie Pfad 1)

**Aufrufer dieser Funktion (reactive GO boxes):**
1. `src/gameMechanic/fightPhase.py:460` — im Fight Phase
2. `src/gameMechanic/chargePhase.py:174` — im Charge Phase
3. `src/gameMechanic/movementPhase.py:663` — im Movement Phase
4. `src/gameMechanic/psychicPhase.py:192` — im Psychic Phase
5. `src/gameMechanic/psychicPhase.py:527` — im Psychic Phase
6. `src/uiLayout/_common.py:1190` — Emergency Disembarkation (gerufen aus _common)

---

## Insane Bravery: Render-Pfade

**Definition:** `data/wh40k_9e/_shared/stratagems.yaml:102-103`
- `id: wh40k_9e.shared.stratagem.insane_bravery`
- `name_en: Insane Bravery`
- `phase: morale`
- **NICHT** `timing: phase_reactive` (→ nicht als reactive GO-Box)

**Button-Render:** `src/gameMechanic/moralePhase.py:165-175`
- Zeile 165: `st.success(f"{SYM_CHECK} Insane Bravery active — Morale test automatically passed.")`
- Zeile 166: `st.button("Confirm (Insane Bravery)", key=f"morale_insane_bravery_{uid}")`
- **KEIN `render_go_card` — nur einfacher Button + Message**

**GO-Card-Render in zentrale Liste:**
- **Insane Bravery erscheint AUCH in der zentrale Stratagem-Liste** (gameProtocoll.py) auf JEDER Phase ≠ 0
- Dort wird es als GO-Card über **Pfad 1** oben gerendert
- **Das ist der Ort, wo das used-on-Badge zeigt**

---

## Datenquellen-Kette für das Badge

Alle drei Render-Pfade verwenden die **gleiche Datenquelle**:

```
go_card_html() ← render_go_card(locked_reason=...)
  ← _go_state_and_reason() oder _reactive_go_state() oder _advance_reroll_state()
    ← stratagem_used_elsewhere_unit_name(faction, strat.id)
      ← stratagem_use_anchor(faction, strat.id)
        ← st.session_state.get("stratagem_use_anchors", {}).get(faction, {}).get(stratagem_id)
```

**Kritisch:** `stratagem_use_anchors` wird von `spend_stratagem()` geschrieben (siehe `stratagemEngine.py`).
Das ist der **gespeicherte State**, nicht die live Sidebar-Auswahl.

---

## Fazit: Geteilte Datenquelle?

**Ja.** Alle drei Render-Pfade (zentrale Liste, Advance Reroll, reactive boxes) verwenden exakt die gleiche Datenquelle-Kette (`stratagem_use_anchors`). Es gibt keine separaten Code-Pfade — nur ein Datenquelle + drei Call-Sites.

**S149-Fix Abdeckung:** Der Fix in gameProtocoll.py Zeile 335 und die Render-Pfade in _common.py (Zeile 857) und movementPhase.py (Zeile 323) sind parallel-strukturiert — alle rufen `stratagem_used_elsewhere_unit_name` auf, bevor sie den locked_reason an `render_go_card` übergeben.
