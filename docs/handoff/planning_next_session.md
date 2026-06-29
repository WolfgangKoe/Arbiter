# Planning — 2026-06-28 (S110)

**Stand nach S109:** Plan 030 (Conquering Tyrant UI-Bugs) vollständig abgeschlossen und committet. 1182 Tests grün, 93,02 % Coverage, Architektur 8/8. Branch `feature/016-protocol-rp-effects` — keine offenen Steps auf diesem Branch. Die Linie 016 → 018 → 015 → 026 → 017 ist die aktive Reihenfolge.

**Nächster Schritt laut `next_session.md`:**
- PRIO 1: Wound-Anzeige Verkettungs-Bug (`dice_html.py:126-138`, analog S109-Hit-Fix)
- PRIO 2: Coverage → ~100 % (Stakeholder-Wunsch S109)
- Dann: Plan 016 (016 ist der nächste Linienschritt)
- Carry-over: `rotate_history.py` Marker-Drift, Direktiv-Lock `#2b`, manuelle UI-Checks

---

## Aufgabe A — Wound-Verkettungs-Bug fixen (PRIO-1, Bugfix)

**Ziel:** `_render_dice_wound_block` in `src/uiLayout/dice_html.py` (Zeilen 126–138) hat denselben `current = next_thresh`-Verkettungsfehler wie der in S109 gefixte Hit-Block. Stacked Wound-Debuffs müssen base-verankert + ±1-Cap angezeigt werden — identischer Fix wie der in S109 umgesetzte `_render_dice_roll_block`-Fix.

**Vorgehen:**
1. `dice_html.py` Zeilen 126–138 lesen, `_render_dice_roll_block` als Vorlage (S109-Fix) nehmen
2. Analogen Fix auf `_render_dice_wound_block` anwenden: `current` immer vom Basis-Threshold ableiten, nicht kumulativ verketten
3. Regressionstest analog `test_stacked_hit_debuffs_both_reference_base_threshold` (bereits in `tests/uiLayout/test_resolution_tab.py`)

**Betroffene Dateien:**
- `src/uiLayout/dice_html.py` (Zeilen 126–138, WOUND-Block)
- `tests/uiLayout/test_resolution_tab.py` (neuer Regressionstest)

**Token-Schätzung:** ~8k (XS–S: isolierter Bugfix, klare Vorlage aus S109)
**Tier:** Sonnet (Fleißarbeit, Muster aus S109 ist vorgegeben, kein Design-Aufwand)
**Regel-Check:** nicht nötig (reiner Render-Bug, keine Regelinterpretation)

---

## Aufgabe B — Coverage auf ~100 % erhöhen (Stakeholder-Wunsch, mehrere Module)

**Ziel:** Die in `next_session.md` gelisteten Coverage-Lücken schließen:
- `scenarios.py` 81 % (Zeilen 78–88, 95–111)
- `unit_mutations.py` 87 %
- `attack_math.py` 87 %
- `loader.py` 89 %
- `game_state.py` 92 %
- `ability_engine.py` 94 % (Zeilen 71–72, 113, 151, 190, 211–216, 388, 392, 424, 427, 431)
- `rosz_importer.py` 95 %
- `unit.py` 99 %

**Betroffene Dateien (lesen):**
- `src/gameMechanic/scenarios.py`, `src/gameMechanic/unit_mutations.py`, `src/gameMechanic/attack_math.py`
- `src/gameObjects/loader.py`, `src/gameMechanic/game_state.py`, `src/gameMechanic/ability_engine.py`
- `src/gameObjects/rosz_importer.py`, `src/gameObjects/unit.py`
- Entsprechende Testdateien unter `tests/`

**Empfehlung:** In zwei Subagenten-Läufe teilen (Scope-Kontrolle): Lauf 1 = `scenarios.py` + `unit_mutations.py` + `attack_math.py`; Lauf 2 = `loader.py` + `game_state.py` + `ability_engine.py`.

**Token-Schätzung:** ~20–30k gesamt (M), je Lauf ~10–15k
**Tier:** Sonnet (mechanische Test-Ergänzung, Lücken per `--cov` sichtbar, kein Design)

---

## Aufgabe C — Plan 016 starten: RP-Block-Hints + Dynastiebonus-Anzeige

**Ziel:** Plan 016 Step 1–4 umsetzen (verbleibende Steps nach Plan 025):
- Step 1: Regel-Verifikation Undying Legions in `docs/work/wahapedia_necrons/` (kein Code)
- Step 2: `get_active_protocol_effects()` in `ability_engine.py` (generischer Helper)
- Step 3: RP-Block-Hints in `_common.py` (`_render_rp_block`)
- Step 4: Dynastiebonus-Kennzeichnung in `armyCard.py`

**Betroffene Dateien:**
- `docs/work/wahapedia_necrons/faction_overview.txt` (Regel-Verifikation, read-only)
- `src/gameMechanic/ability_engine.py`, `src/uiLayout/_common.py`, `src/uiLayout/armyCard.py`
- `tests/gameMechanic/test_ability_engine.py`

**Token-Schätzung:** ~20k (S–M; Step 1 = Haiku-Lookup, Steps 2–4 = Sonnet)
**Tier:** Step 1 Haiku (Regel-Lookup mit explizitem Suchobjekt); Steps 2–4 Sonnet (Code-Umsetzung nach Plan)
**Regel-Check:** `docs/work/wahapedia_necrons/faction_overview.txt`, Zeilen ~583 ff. (Command Protocols, Undying Legions Wortlaut)
**Hinweis:** Step 4 (Dynastiebonus-Badge-Platzierung) braucht ggf. ein Mini-Mockup → Stakeholder-Freigabe vor Render-Code einplanen.

---

## Empfehlung

**Reihenfolge: A → C** (B als eigene Folge-Session / paralleler Subagenten-Lauf)

- Aufgabe A (Wound-Bug) ist PRIO-1, kleinstes Stück, blockiert nichts, kurzer Sonnet-Lauf.
- Aufgabe C (Plan 016) ist der nächste Linienschritt, mehrfach aufgeschoben. Nach Plan 025 ✅ ist der Scope klein (RP-Hint + Dynastiebonus). Passt in eine Session.
- Aufgabe B (Coverage) wichtig, aber kein Block — eigene Folge-Session oder parallel.

**Carry-over:** `rotate_history.py` Marker-Drift (XS, Haiku); Planning-Template-Erweiterung in `agent_scopes.md` (Freigabe steht aus).

---

## Offene Fragen / Entscheidungsbedarf

1. **Planning-Template-Erweiterung** (`agent_scopes.md`, zwei Spalten „Subagent(en) + Tier" + „Scope-Zeile / Dateien"): Freigabe steht aus. In dieser Session miterledigen?
2. **`rotate_history.py` Marker-Fix**: Marker in `next_session.md` anpassen ODER Tool aufs aktuelle Format bringen?
3. **Direktiv-Lock `#2b`**: In nächsten Sessions priorisieren oder Backlog?

NEEDS-DECISION
