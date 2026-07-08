# Startprompt — Nächste Session
<!-- Kanonisch: .claude/tasks/next_session.md — nie ins Root-Verzeichnis anlegen. -->
<!-- Nur „Stand + nächster Schritt + offene Fragen". Historie → session_archive.md; Backlog → backlog.md. -->
<!-- Referenz NICHT hier: Architektur → architecture.md, Regel-Gotchas → rules_insights.md, Constraints → CLAUDE.md. -->

## ⚠️ Session-Regeln
- **Start:** „start next session" → Planner-Subagent (`CLAUDE.md`+`docs/goals/ziel7.md`+`docs/goals/backlog.md`, Scope `docs/reference/agent_scopes.md`) legt Entwurf vor, Koordinator zeigt ihn, erst nach Freigabe los; „Plan ist freigegeben" = Shortcut direkt los. Einstieg `LEITSTAND.md`, Rollen/Tier `docs/governance/operating_model.md`.
- **ADR-0007:** Koordinator routet, liest keine Quelldateien/Vollergebnisse — Detail-Planung/Review laufen als Subagenten; Stakeholder-Entscheidungen async über Mailbox (`docs/handoff/`, NEEDS-DECISION→ANSWERED), nicht Chat.
- **Ende:** Review (Reviewer-SA) → Retro → Maßnahmen-Entscheid (Stakeholder) → Abschluss: diese Datei aktualisieren (ZUERST lesen) + ggf. Ziel-Checkboxen.
- **Doku-Gate:** Decke 120 Zeilen (Test rot darüber); beim Reißen tief auf ≤ 70 kürzen (Erledigtes → `backlog.md`/`session_archive.md`).
- **Freigabe vor Umsetzung; kein Memory/Skill(datei-ändernd) ohne Freigabe; Subagenten = stehende Freigabe (ADR-0005); rote vorher-grüne Tests = STOP + fragen.** → `CLAUDE.md`.
- **Sync-Pflicht bei Session-Start:** Checkbox-Sync auch gegen Commit-Titel wie „archive/close" prüfen (S119/S120-Befund); `docs/handoff/` auf liegengebliebene ANSWERED/DONE-Dateien prüfen (r-proto-02 lag seit S116).
- **Executor-Klausel:** Dateiänderungen nur über Edit/Write, Bash nur lesend/git/pytest (S123); Selbstprüfliste enthält `python tools/mypy_gate.py` (S128).
- **mypy Zero-Error-Ratchet:** Baseline sinkt jede Session Richtung 0, Abweichung nach oben nur mit Begründung im Commit.
- **Parallel-Modus Standard für Ledger-Abbau:** dateidisjunkte Pakete, Vorher-Messung nur gegen `git show HEAD:` (kein `git stash` im geteilten Baum).
- **Retro-Merkposten:** ab ~6 Plänen splitten/an Sonnet delegieren (S124); Lösch-Pläne-Selbstprüfliste MUSS entfernte Bezeichner auch über `docs/spec/` greppen (S126); App VOR jeder UI-Verifikation neu starten + Prüfanleitungen gegen Roster-Realität validieren (S126).

## Was ist Arbiter?
Digitaler Spielbegleiter WH40k 9E, Streamlit (Python). Start: `streamlit run src/app.py` (Port 8501; **venv:** `source .venv/bin/activate`). Branch `feature/016` (Arbeit), `main` (nur PR). **App permanent laufen lassen:** bei Session-Start nur kurz prüfen (`curl -s -o /dev/null -w "%{http_code}" http://localhost:8501` → 200), nur bei Bedarf neu starten — nicht den Nutzer fragen.

---

## Aktueller Stand (nach S129, 2026-07-08)

S129: Psychic-Phase-Blocker gefixt (`initial_deny_state` liefert `denied=False` statt ewig `None`, wenn der Gegner nicht denyen kann) + Smite-Ziele waren nie wählbar (`_TARGET_PHASES` fehlte `"psychic"`, jetzt `smite_targets()` mit Parameter `own_faction`, INV-4b-konform); mypy `phase_runner.py` 7→0, Baseline 82→75; Plan 018.2 bestätigt erledigt. Vollsuite 1505 passed, Coverage 99,12 %. Details: `docs/goals/backlog.md`, `docs/audit/plans/README.md`; Historie S60–S128: `docs/metrics/session_archive.md`.

### ▶ Nächster Schritt

1. **rp/directive-Vokabular sichtbar machen** (Stakeholder-freigegeben, S129): (a) Seeds `directive`+`reanimate` (→necrons) in `tests/architecture/_vocab.py` — KEIN `revive` (Orks „Surly as a Squiggoth" ≠ Core Rules „Resurrected Models"); (b) „rp" in `src/` ausschreiben: `rp_reroll`→`reanimation_protocols_reroll` (`ability_engine.py:355`, `necrons/faction_abilities.yaml`, `_schema/round_choice.example.yaml`), `get_active_rp_modifiers`→`get_active_reanimation_protocols_modifiers`, `_render_rp_block`/`_render_unit_rp`/Widget-Keys/`_rp_directive_hints` (`_common.py`), `models_lost_since_last_rp` (`game_state.py:374`); YAML-Werte `stat: rp`/`reroll_rp`/`buff_rp` bleiben; (c) `directive`→`round_choice` in den 4 `ability_engine`-Helfern; (d) neue Scanner-Funde als LEGIT ins Ledger (`test_generic_src_vocab.py`, `architecture_invariants.md`); (e) Backlog-Eintrag: reanimate-Pfad-Erweiterbarkeit (Trigger nur `after_enemy_attack`, Formel nur `D6_per_wound` — Squiggoth-Muster passt nicht).
2. mypy-Ledger weiter senken (Rest `gameMechanic/` außer `game_state.py`/`phase_runner.py`, dann `uiLayout/` zuletzt). Details: `docs/goals/backlog.md`.
3. Queue: 018.4 offen (nach 017), dann 015 → 026 → 017; 041 erst nach 015/026. Details: `docs/audit/plans/README.md`.

**Offen:** 037 Docker-Smoke vor Merge (`docker build` + `docker run --rm arbiter-test id -u` → 1000, Port-7860 beim HF-Deploy); Deny-Caption-Prüfung (Task 2) blockiert — braucht Roster mit Deny-Einheit auf Gegenseite (Option: Rollen tauschen, Orks-Weirdboy denied); Smite-Fix manuell verifizieren (Psychic-Phase → Manifest ohne gegnerischen Deny → „No deny possible." → Klick auf Gegner-Einheit → Damage-Button); Direction-Entscheide (Audit S124: ziel9-Fetcher/Deployment-Phase/Mission-Scoring) → `docs/goals/backlog.md` §5.

---

## Gate-Netz (Messbefehle)
- Tests + Coverage: `pytest --tb=short` (Floor **99 %**, `pyproject.toml`); **Schulden-Scoreboard** danach.
- Architektur: `pytest tests/architecture/ --no-cov -q`. Doku/Akzeptanz: `pytest tests/docs/ tests/acceptance/ --no-cov -q`.
- **Token-Korridor** <150k, bei ~135k beenden; Fleißarbeit PROAKTIV an Sonnet-Subagent.
- **Token-Report + History (M4, PFLICHT beim Abschluss):** `python tools/token_report.py --write` + `python tools/rotate_history.py --session <N> --summary "…"` — Koordinator stößt an.
- **Freigabe-Gate:** Edit/Write blockiert bis `touch .claude/.freigabe`; SessionStart re-armt.
