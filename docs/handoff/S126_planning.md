STATUS: ANSWERED

# S126 — Plan 040 Umsetzungsvermerk

Executor-Subagent (Opus), 2026-07-05 · Lifecycle: nach Review auf DONE setzen
und löschen, sobald der Sessionabschluss S126 committet ist (DoD Punkt 7).

## Ziel

Plan 040 in erweiterter Form (Stakeholder-Freigabe): tote Phasen-Stage-Maschine
(`start`/`active`/`end`) entfernen **plus** Mitfix Stratagem-Sichtbarkeit.

## Scope (umgesetzt)

- **Teil A — tote Stage-Maschine:** `advance_stage()` gelöscht;
  `render_current_phase()` auf Handler-Auflösung + `render_active()` reduziert;
  toter `get_triggered_abilities`-Import raus; `render_start`/`render_end` aus
  dem Protocol (`phase_handler.py`) und allen 7 Handlern entfernt (inkl. inertes
  Duplikat-Reset in `psychicPhase.render_end`); `phase_stage`-Init
  (`game_state.py`) und Reset-Tupel (`scenarios.py`) bereinigt;
  `ability.py`-Kommentar präzisiert (Feld bleibt).
- **Drift-Funde (erweiterter Scope):** `scenarios.py:save_scenario()` schrieb
  `phase_stage`, `gameProtocoll.py` las es — beide mitbereinigt. Legacy-
  Szenario-JSONs mit `phase_stage`-Key werden ignoriert (Regressionstest).
- **Teil B — Mitfix:** `stage`-Hart-Filter + `current_stage`-Parameter aus
  `stratagem_visibility()` entfernt (Option B; `Stratagem.stage`-Feld bleibt).
  Regelbefund bestätigt: `stage` ist App-Konstrukt, 9E kodifiziert nur die
  Phasen-Bindung; Timing steht im `rule_text`. Betroffene Stratagems (z. B.
  `dimensional_corridor`, `dimensional_destabilisation`, Ork-Klan-Stratagems
  mit `stage: start/end`) sind jetzt in ihrer Phase sichtbar.
- **Teil C — Tests:** `test_phase_runner.py` migriert (Registry + Dispatch,
  Stage-Tests raus); `test_stratagem.py` bereinigt + neuer Regressionstest
  `test_start_and_end_stage_stratagems_visible_in_matching_phase` (synthetisch
  + real geladen); `test_scenarios.py` migriert (Folge des erweiterten Scopes,
  transparent ausgewiesen — kein stilles Anpassen).
- **Teil D — Artefakte:** Plan-040-Doc (Status DONE, Mitfix-Absatz, Effort M),
  `plans/README.md`-Queue, `rules.md` R-CMD-05 (stage ≠ Sichtbarkeits-Kriterium).

## Gates

- Vollsuite: 1451 passed, Coverage 99,11 % (Gate 99 %) ✅
- Architektur-Gate (`tests/architecture/`): 8 passed ✅
- Lint (`ruff`/`black`/`isort`, src + tests): sauber ✅
- `grep -rn "phase_stage|advance_stage|render_start|render_end|current_stage" src/` → 0 ✅

## Offen (manuell in der App prüfen)

Stratagem-Spalten (gameProtocoll): start/end-Stratagems erscheinen jetzt in
ihrer Phase (Liste im Executor-Abschlussbericht S126).
