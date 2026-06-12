# Plan 018: Kleinkram-Sammelplan — CP-Doppelvergabe, Battle-Log-Reset, Gretchin Cowardly, Modifier-Konsolidierung

> **Executor instructions**: Die vier Tasks sind UNABHÄNGIG — einzeln
> ausführen und committen, Reihenfolge 18.1 → 18.2 → 18.3 → 18.4. Jeder Task
> hat eigene Verify-Schritte. STOP-Bedingungen beachten. When done, update
> the status row in `docs/audit/plans/README.md` (pro Task abhaken).
>
> **Drift check (run first)**:
> `git diff --stat f0f4e17..HEAD -- src/gameMechanic/commandPhase.py src/gameMechanic/game_state.py src/gameMechanic/moralePhase.py src/uiLayout/gameProtocoll.py`
> Drift durch Plan 015 (gameProtocoll/once_per_battle) ist ERWARTET und
> für 18.1 relevant — s. dort.

## Status

- **Priority**: P3 (NIEDRIG-Block aus next_session.md + Akzeptanzkriterium „CP-Doppelvergabe unmöglich")
- **Effort**: M gesamt (4 × S)
- **Risk**: LOW
- **Depends on**: — (18.4 NACH 014/016/017 ausführen, gleiche Dateien)
- **Category**: bugfix + feature + refactor
- **Planned at**: commit `f0f4e17`, 2026-06-12

---

## Task 18.1 — CP-Doppelvergabe unmöglich machen (Bug)

### Why / Current state

`cp_granted_this_phase` ist ein EIN globales Flag (`commandPhase.py:39-46`),
das `_reset_phase_state()` bei JEDEM Phasenwechsel löscht
(`game_state.py:348`) — auch beim Zurücknavigieren (←) in die Command Phase.
Wer ← → drückt, kann demselben Spieler beliebig oft +1 CP geben.
Akzeptanzkriterium ziel6.md: „CP-Doppelvergabe unmöglich".

### Steps

1. `game_state.py`: neuer persistenter Key `cp_grants: set[tuple[int, str]]`
   — `(round, faction)`-Paare; Init in `init_game`-Pfad; in
   `_reset_phase_state` NICHT anfassen; in `reset_game` fällt er mit dem
   kompletten Session-State weg (Z. 343-344 löscht alles — reicht).
2. `commandPhase.py` `_render_faction_actions`: Bedingung
   `(state["round"], faction) in st.session_state.cp_grants` statt
   `cp_granted_this_phase`; beim Grant das Tupel eintragen.
3. `cp_granted_this_phase` vollständig entfernen (`game_state.py:258, 348`,
   `commandPhase.py:39`) — `grep -rn "cp_granted_this_phase" src/ tests/`
   → 0 Treffer (Tests migrieren).

### Verify

- Neue Tests: Grant in Runde 1 → ←/→-Navigation → Button bleibt gesperrt;
  Runde 2 → Button wieder frei; zweiter Spieler (active wechselt) hat
  eigenen Anspruch.
- `pytest --tb=short` grün.

### STOP

- Es existiert ein gewollter „Undo CP"-Pfad, der das Flag braucht → melden.

---

## Task 18.2 — Battle Log nach Reset leer (6g-Rest, Bug-Verifikation)

### Why / Current state

ziel6/next_session: „Nach Reset keine alten Einträge im Battle Log."
`reset_game()` ruft `archive_and_reset_log()` (`game_state.py:339-344`;
`game_log.py:83-96` verschiebt die Datei nach `data/log/archive/`).
`gameProtocoll._load_game_log()` liest die Datei bei jedem Render. Der Bug
ist damit MÖGLICHERWEISE bereits behoben — aber unverifiziert, und
`game_log.py` könnte Modul-State (gepufferte Einträge, `set_log_players`)
über den Reset retten.

### Steps

1. Repro-Versuch (Streamlit): Spiel mit Log-Einträgen → Reset → neues Spiel
   → Battle-Log-Tab prüfen.
2. `game_log.py` auf Modul-globalen Zustand prüfen (gepufferte Liste,
   game_id, players). Wenn nach Reset alte Einträge auftauchen: Ursache
   benennen (Datei vs. Modul-Puffer) und minimal fixen —
   `archive_and_reset_log` muss auch den In-Memory-Zustand neu aufsetzen.
3. Regressionstest: `log_action` → `archive_and_reset_log` → Log-Quelle
   leer; Archivdatei enthält die alten Einträge.

### Verify

- Test grün; manueller Reset-Durchlauf sauber.
- Falls NICHT reproduzierbar: im Bericht „bereits behoben durch <Commit/
  Mechanik>" dokumentieren, Checkbox in ziel6.md abhaken, Test trotzdem
  ergänzen (sichert den Zustand).

---

## Task 18.3 — Gretchin Cowardly: Combat-Attrition-Hinweis (datengetrieben)

### Why / Current state

9E Morale: nach verlorenem Moraltest flieht 1 Modell, dann **Combat
Attrition** (1 W6 pro verbliebenem Modell; bei 1 flieht das Modell; −1 auf
den Wurf wenn die Einheit unter halber Stärke ist). Gretchin „Cowardly
Grots": −1 auf Attrition-Tests, wenn kein RUNTHERD in 6". Die App bildet
Attrition bisher GAR nicht ab (`moralePhase.py:131-148`: nur „Wie viele
Modelle sind geflohen?"-Eingabe). Distanz kennt die App nicht → die
RUNTHERD-Bedingung ist eine Nutzer-Checkbox (Tisch-Verantwortung, gleiches
Muster wie Cover).

### Steps

1. Regel-Wortlaut prüfen: Combat Attrition in
   `docs/work/wahapedia_core_rules/core_rules.txt` + Cowardly Grots in
   `docs/work/wahapedia_orks/`; Zitate in den Bericht.
2. Schema (6j-konform, generisch): Ability-Effekt-Typ
   `attrition_modifier` mit `value: -1` und optionaler
   `condition_prompt`-Angabe (Text der Nutzer-Checkbox, z. B.
   `"RUNTHERD within 6\"?"` mit `applies_when: false` — Modifier gilt, wenn
   die Checkbox NICHT gesetzt ist). Spec in `docs/spec/faction_abilities.md`
   ergänzen.
3. `orks/unit_abilities.yaml`: Cowardly-Grots-Eintrag für Gretchin.
4. `moralePhase.py` `_render_unit_morale`, im Failed-Zweig (nach der
   Fled-Eingabe): Attrition-Hinweisblock —
   `Combat Attrition: 1 W6 pro Modell, flieht bei ≤ N` mit N aus:
   Basis 1, +1 wenn unter halber Stärke (`models` vs. `models_initial` —
   im State vorhanden), +1 pro aktivem `attrition_modifier` (Checkbox).
   Reine Anzeige — die Würfe bleiben auf dem Tisch, die Fled-Eingabe
   unverändert.
5. Helper `_attrition_threshold(unit, unit_state, ability_mods) -> int` als
   reine Funktion (testbar, gemessen — in `moralePhase.py`-Modulkopf oder
   `ability_engine.py`).

### Verify

- Tests: Threshold-Helper (voll/halb-stark, mit/ohne Modifier);
  Ability-Parsing.
- Manuell: Gretchin mit Verlusten + Moraltest fehlgeschlagen → Block zeigt
  Checkbox + korrekten Schwellwert; Necron-Einheit → Block ohne
  Ability-Modifier (nur Halbstärke-Regel).
- Kein Orks-Literal in `src/` (Label/Prompt aus YAML).

### STOP

- Combat-Attrition-Wortlaut weicht vom obigen Modell ab (z. B. Modifier
  kumulativ anders) → Zitat vorlegen.

---

## Task 18.4 — Modifier-Sammlung konsolidieren (6e-Rest, Refactor)

### Why / Current state

6e sah `collect_modifiers_for_phase()` in der Engine vor. Real existieren
heute `_collect_atk_modifiers` + `_collect_def_save_modifiers` in
`_common.py:368-446` (UI-Modul, von Coverage ausgenommen!) — Logik, die in
die gemessene Engine gehört. Nach den Plänen 016/017 kommen weitere Quellen
dazu; die Sammelstellen sollen EINMAL existieren.

### Steps

1. Beide Funktionen nach `ability_engine.py` verschieben und umbenennen:
   `collect_attack_modifiers(...)` / `collect_save_modifiers(...)` —
   Signaturen beibehalten, `st.session_state`-Zugriffe bleiben (Engine nutzt
   Streamlit bereits).
2. `_common.py`: Re-Exports/Aufrufe umstellen; keine Logik-Änderung
   (byte-gleiches Verhalten).
3. Tests: bestehende UI-Tests laufen unverändert; NEUE direkte Engine-Tests
   für beide Collector (Protokoll-Quelle, Buff-Quelle, Stratagem-Quelle) —
   die Funktionen zählen jetzt ins Coverage-Gate.

### Verify

- `grep -n "_collect_atk_modifiers\|_collect_def_save_modifiers" src/uiLayout/_common.py`
  → nur noch Import/Delegation oder 0 Treffer.
- `pytest --tb=short` grün, Coverage ≥ 80 % (steigt leicht — neue gemessene
  Funktionen MIT Tests).

### STOP

- Pläne 016/017 sind IN PROGRESS → warten (gleiche Funktionen).

---

## Commands (alle Tasks)

| Zweck | Befehl |
|-------|--------|
| venv | `source .venv/bin/activate` |
| Lint | `ruff check src/ && black --check src/ && isort --check-only src/` |
| Vollsuite | `pytest --tb=short` |

## Git workflow

- Branch: `chore/018-low-prio-cleanup`; vier Commits
  (`Fix CP grant double-award across phase navigation`,
  `Ensure battle log starts empty after reset`,
  `Add data-driven combat attrition hints (Cowardly Grots)`,
  `Move modifier collectors into ability_engine`).
- Nicht pushen/PR ohne Anweisung.

## Done criteria

- [ ] 18.1: CP-Grant pro (Runde, Spieler) genau einmal; Flag entfernt; Tests
- [ ] 18.2: Reset-Log-Verhalten verifiziert/gefixt + Regressionstest
- [ ] 18.3: Attrition-Hinweis datengetrieben; Threshold-Helper getestet
- [ ] 18.4: Collector in der Engine, direkt getestet
- [ ] `pytest --tb=short` grün, ≥80 %; Lint passt
- [ ] ziel6.md: zugehörige Checkboxen (6g-Rest, 6e-CP, Gretchin) abgehakt
- [ ] Status-Zeile in `docs/audit/plans/README.md` aktualisiert
