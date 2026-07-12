STATUS: ANSWERED

# S143 Plan-Aufgabe 6 — abilityEngine.py: Konsolidierungs-/Refactor-Optionen nach S142

Recherche-Subagent W1-C (Sonnet, Effort S), read-only. Bezug: S142 konsolidierte
`_apply_stratagem_effect`, `_effect_gate_met`, `stratagem_strength_bonus` in
`src/gameMechanic/stratagemEngine.py`. Diese Datei fragt: was ergibt sich jetzt
für `src/gameMechanic/abilityEngine.py`?

## Grundannahmen (bestätigungspflichtig)

- App würfelt NICHT — Tischwürfe. Effekt-Dispatch/Gate-Logik in beiden Engines
  berechnet nur Modifikatoren/Zustände, nie Würfelergebnisse (bestätigt durch
  Docstrings, z.B. `get_active_round_choice_ap_on_wound_6`: "the App never sees
  individual dice faces").
- Coverage-Gate (99 %) deckt `gameMechanic/` vollständig ab (kein Render-Code) —
  ein reiner Extract-Function-Refactor ohne Verhaltensänderung ist durch
  bestehende Tests abgesichert, solange kein Verhalten (Filter-Prädikate,
  sum vs. min) versehentlich verschoben wird.
- `gameMechanic/` ist laut `docs/spec/architecture_invariants.md` (Zeile ~198)
  **bewusst noch nicht** Streamlit-frei (abweichend von der ursprünglichen
  Architektur-Vision) — beide Engines importieren `streamlit as st` direkt und
  lesen `st.session_state`. Das ist dokumentierte Schuld, kein neuer Befund.
- Layer-Richtung: `abilityEngine.py` importiert bereits aus `gameMechanic.gameState`
  (`faction_dir_for`, `round_choice_state_key`, `short_round_choice_label`,
  `subfaction_value_for`, `units_key_for`). Ein Import in die Gegenrichtung
  (`gameState` → `abilityEngine`) wäre ein Zyklus.

## Ist-Analyse (kompakt, mit Belegen)

**1. mypy-Restfehler (11 in `gameMechanic/`, gemessen mit `mypy src/gameMechanic`):**

`abilityEngine.py` trägt 3 davon, `stratagemEngine.py` 1:

- `abilityEngine.py:270` — `return state.get("movement_choice") == "stationary"`
  in `get_active_round_choice_light_cover_if_stationary`: `state` kommt aus
  verschachteltem `st.session_state.get(...).get(...)` (untypisiert → `Any`),
  der Vergleich "leakt" `Any` in eine `-> bool`-Signatur.
- `abilityEngine.py:408` — `def _unit_matches_target(unit: Unit, effect: dict) -> bool:`
  — bare `dict` ohne Typparameter, **ohne** das `# type: ignore[type-arg]`,
  das an 7 Schwester-Funktionen im selben File bereits klebt (Zeilen 89, 98,
  131, 156, 171, 318 — grep-Beleg).
- `abilityEngine.py:419` — `def _active_effects_for_faction(faction: str) -> list[dict]:`
  — gleiches Muster, gleiche Lücke.
- `stratagemEngine.py:134` — `def stratagem_strength_bonus(active_modifiers: list[dict], ...) -> int:`
  — gleiches Muster.

  Befund: `gameMechanic/gameState.py` nutzt durchgängig **typisierte** Generics
  (`dict[str, Any]`, `dict[str, dict[str, Any]]` — Zeilen 133, 317-326 laut
  grep). Der bare-`dict` + `# type: ignore[type-arg]`-Stil in `abilityEngine.py`/
  `stratagemEngine.py` ist eine Abweichung von der im übrigen `gameMechanic/`
  etablierten Konvention, keine bewusste Design-Entscheidung.

**2. Effekt-Dispatch — strukturell parallel, aber kein Vokabular-Overlap:**

`execute_effect` (`abilityEngine.py:68-77`, dispatcht `Ability.effect.type`,
aktuell nur `"heal"`) und `_apply_stratagem_effect`
(`stratagemEngine.py:22-63`, dispatcht `Stratagem.effect.type`:
`auto_pass_morale`/`move`+`fall_back_through_models`/`invuln_save`) sind beide
elif-Ketten auf `effect.type` — der Docstring in `stratagemEngine.py:1-11`
nennt das explizit ("mirrors the Ability effect-dispatch pattern"). Aber:
beide dispatchen auf **unterschiedliche** `Effect`-Dataclasses
(`gameObjects/ability.py` vs. `gameObjects/stratagem.py`) mit **disjunkten**
`type`-Werten. Ein Merge würde die beiden GO-Effect-Schemas vereinheitlichen
müssen — invasiv, ohne aktuellen Wiederverwendungs-Gewinn (DRY-Regel „erst ab
dritter Wiederholung" aus CLAUDE.md ist hier nicht erreicht: 2 Instanzen,
unterschiedliches Vokabular).

Gleiches gilt für `check_conditions` (`abilityEngine.py:48-65`, Liste
benannter Condition-Flags: `has_rules`, `has_keywords`, `needs_healing` …) vs.
`_effect_gate_met` (`stratagemEngine.py:80-131`, dispatcht auf `effect.type`/
`effect.handler` + prüft Unit-State-Felder wie `movement_chosen`, `in_melee`).
Unterschiedliche Form (Condition-Liste vs. Type-Dispatch) — kein sauberer
gemeinsamer Nenner ohne Verhaltensrisiko.

**3. Accumulate-Muster — die eigentliche Wiederholung (≥5 Instanzen, davon 1
modulübergreifend):**

Innerhalb `abilityEngine.py` wiederholt sich ein Filter+Akkumulier-Muster
("für jeden Effect-Dict in einer Liste: wenn `type`==X [und Zusatz-Prädikat]:
akkumuliere `value`/`modifier`") mindestens 4×:

- `get_active_round_choice_strength_if_charged` (Zeilen 219-224, `sum`)
- `get_active_round_choice_ap_on_wound_6` (235-240, `sum`)
- `get_active_heal_bonus` (397-405, `sum` + `target_rule`-Filter)
- `buff_stat_bonus` (437-441, `sum` + `_unit_matches_target`-Filter)
- `ability_invuln_save` (450-456, **`min`** statt `sum` — Sonderfall)

`stratagemEngine.stratagem_strength_bonus` (134-155) ist eine 6. Instanz
desselben Musters, operiert aber auf `active_modifiers` (Stratagem-Quelle)
statt `_active_effects_for_faction` (Ability-Quelle) — Docstring
(`stratagemEngine.py:135-137`) nennt die Parallele selbst: "Mirrors
abilityEngine.buff_stat_bonus's role". Das ist die einzige Stelle, an der das
Wiederholungsmuster tatsächlich die Modulgrenze abilityEngine ↔
stratagemEngine überschreitet.

**4. Verwandter, aber außerhalb des engeren Scopes liegender Befund:**
`gameMechanic/gameState.py:242-283` (`active_round_choice_buff_labels`)
dupliziert einen Teil der "welches Directive ist aktiv"-Logik
(`assignments`/`subfaction_affinity`/6.-Protokoll-Sonderfall), die
`abilityEngine._active_directive_effects` (131-168) bereits kapselt — aber
`gameState.py` kann `abilityEngine.py` nicht importieren (Zyklus, siehe
Grundannahmen). Lösung würde eine dritte, tieferliegende Modul-Ebene brauchen
— das ist eine Architektur-Frage, keine kleine Refactor-Aufgabe, daher nur
als Beobachtung notiert, nicht als Option unten.

## Refactor-Optionen

**Option A — mypy-Typparameter nachziehen (XS, Risiko niedrig)**
Bare `dict`/`list[dict]` in `abilityEngine.py` (Zeilen 89, 98, 131, 156, 171,
318, 408, 419) und `stratagemEngine.py:134` durch `dict[str, Any]`/
`list[dict[str, Any]]` ersetzen (Konvention aus `gameState.py` übernehmen),
`# type: ignore[type-arg]`-Kommentare entfernen. `abilityEngine.py:270` braucht
zusätzlich eine explizite Typannotation auf `state` (z. B.
`dict[str, Any]`) statt der impliziten `Any`-Kette.
Erwarteter Effekt: löst 4 von 11 `gameMechanic`-mypy-Fehlern (3 in
abilityEngine, 1 in stratagemEngine) auf einen Schlag.
Testauswirkung: keine neuen Tests nötig (reine Typannotation, keine
Verhaltensänderung) — Vollsuite + `mypy src/gameMechanic` als Beleg laufen
lassen.

**Option B — geteilten Accumulate-Helfer extrahieren (S, Risiko niedrig-mittel)**
Kleine generische Funktion (z. B. `_sum_effect_value(effects, effect_type,
value_key="value", predicate=None, combine=sum)` o. ä.) in
`abilityEngine.py` einführen, die die 5 innermodularen Instanzen (Punkt 3
oben) auf sich zieht, UND von `stratagemEngine.stratagem_strength_bonus`
importiert wird — die einzige Instanz, die die Modulgrenze bereits nachweislich
überschreitet (Docstring-Beleg). `ability_invuln_save`s `min`-Sonderfall braucht
einen `combine`-Parameter statt hartcodiertem `sum` — sonst Verhaltensbruch.
Risiko: mittel, weil 6 Call-Sites gleichzeitig angefasst werden und ein
Prädikat-Fehler (z. B. `_directive_phase_excluded`-Filter falsch verdrahtet)
still einen Bonus falsch berechnen könnte, ohne dass ein Test es zwingend
auffängt, falls die Vollsuite nicht jeden Filter-Zweig abdeckt.
Testauswirkung: bestehende Tests müssen grün bleiben (Coverage-Gate deckt
diese Funktionen bereits ab); pro extrahiertem Call-Site wird empfohlen, den
bestehenden Test explizit gegen den Helfer laufen zu lassen (kein Blind-Vertrauen
auf "Coverage ist grün" laut Sicherheitsnetz-Regel).

**Option C — Effekt-Dispatch/Gate-Logik zusammenlegen (NICHT empfohlen, daher
nur als verworfene Option benannt)**
`execute_effect`/`_apply_stratagem_effect` bzw. `check_conditions`/
`_effect_gate_met` in ein gemeinsames Dispatch-Modul zusammenführen. Verworfen:
disjunkte `Effect`-Vokabulare (Punkt 2), DRY-Schwelle "3. Wiederholung" nicht
erreicht, Merge würde `gameObjects/ability.py` und `gameObjects/stratagem.py`
anfassen — Aufwand M+, Risiko hoch, aktuell kein Wiederverwendungs-Gewinn.

## Empfehlung

Option A zuerst (XS, kein Restrisiko) — danach Option B (S), aber Option B
nur mit dem `combine`-Parameter für den `min`-Sonderfall in
`ability_invuln_save` und mit expliziten Regressionstests pro verschobenem
Call-Site, nicht als reiner "sollte äquivalent sein"-Umzug. Option C nicht
verfolgen, bis eine 3. Instanz des gleichen Dispatch-Vokabulars auftaucht
(DRY-Schwelle aus CLAUDE.md).

## Entscheidungsfragen an den Stakeholder

1. Option A + B in einer Executor-Session bündeln (beide XS/S, zusammen noch
   im M-Rahmen für Executor-Briefs), oder getrennt takten (A sofort, B erst
   nach separater Freigabe)?
2. Soll der Punkt-4-Befund (`gameState.active_round_choice_buff_labels` vs.
   `abilityEngine._active_directive_effects`, Zyklus-Problem) als eigener
   Backlog-Eintrag aufgenommen werden, oder reicht die Notiz hier als
   Wiedervorlage?

## Stakeholder-Entscheid (S143, 2026-07-12)

Option A + B freigegeben, Umsetzung S144. Option C (Engine-Zusammenlegung) bleibt verworfen.
