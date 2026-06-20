# Startprompt — Nächste Session
<!-- Kanonisch: .claude/tasks/next_session.md — nie ins Root-Verzeichnis anlegen. -->
<!-- Nur „Stand + nächster Schritt + offene Fragen". Historie → ziel6.md; Backlog → backlog.md. -->
<!-- Referenzwissen NICHT hier: Architektur-Muster → architecture.md, Regel-Gotchas →
     rules_insights.md, Constraints → CLAUDE.md. -->

## ⚠️ Session-Regeln
- **Start lesen:** `CLAUDE.md` (Freigabe-Pflicht, bei Unklarheit zuerst fragen)
  + `docs/goals/ziel6.md` (Aufgaben/Historie) + `docs/goals/backlog.md` (Backlog).
  Einstieg: `LEITSTAND.md`; Rollen/Tier/Events/Modi: `docs/governance/operating_model.md`.
- **Ende:** Checkboxen in `ziel6.md` + Historien-Zeile; **diese Datei** aktualisieren
  (ZUERST lesen, dann ergänzen — nie blind überschreiben).
- **Doku-Gate:** Decke **120** Zeilen (Test rot darüber). Beim Reißen **tief auf ≤ 70**
  kürzen, nicht knapp drunter — Erledigtes → `backlog.md`/`ziel6.md`, Referenz → s. o.
- **Freigabe vor Umsetzung; kein Memory/Subagent/Skill ohne Freigabe; rote vorher-grüne
  Tests = STOP + fragen.** Details: `CLAUDE.md`.

## Was ist Arbiter?
Digitaler Spielbegleiter für WH40k 9E, Streamlit (Python). Start:
`streamlit run src/app.py` (Port 8501). Branch `dev` (Arbeit), `main` (nur per PR).

---

## Aktueller Stand (nach S75, 2026-06-20)

**S75 (kein Code committet):** Hartes Kontext-Gate (PreToolUse-Block) prototypisiert
und auf Stakeholder-Entscheid **wieder entfernt**. Grund: bei *einer* Schwelle = 135k
blockt das Gate genau den Wind-down (Edit/Commit), den es selbst fordert → latenter
Deadlock. **Offen bleibt:** Kontext-Schutz ist weiter NUR Advisory (`session_context.py`
am Turn-Start) — er warnt, stoppt nicht; deshalb liefen S63/S70 auf 154/156k. Falls
erneut angegangen: Block-Schwelle **oberhalb** des 135k-Wind-downs (z. B. 145k), damit
Speichern+Commit noch durchgehen.

**Plan 019 DONE:** `TargetSelectionRequest` + `pending_target_request` ersetzt
`cmd_awaiting_ability_id`/`cmd_awaiting_required_kw`/`wargear_awaiting_bearer_uid`;
`render_unit_selectbox` für Veil + Mortal-Target. 1007 grün, Cov 92.40 %.

**INV-4b/INV-4 Restschuld:**
- **LEGIT:** `rosz_importer._FACTION_MAP`, `typing.Protocol`
- **Schema-Urteil (Konsens nötig):** `dakka`/`klaw`/`tesla`, `reanimationProtocols`/`reanimation`,
  `arkana`, Items `orb`/`overlord`/`phaeron`/`gloom`/`prism`/`dynasty`,
  Default-Roster-Hardcode (`game_state.py`), `faction_dir`-Default `"necrons"` in `loader.py`

### ▶ Nächste Session = Plan 022 (Dice Display Rework)

**Reihenfolge (neu 2026-06-21):** 022 → 014 → 020 → 021 → 016 → 018 → 015 → 017
**022 zuerst:** aktiver Arrow-Direction-Bug (`dice_html.py:200`, Buff/Debuff invertiert),
Risk MEDIUM, Spec + Testkatalog fertig (`docs/spec/dice_display.md` §8/§10).
**014 danach:** Refinement 2026-06-21 **neu geplant** (alte Fassung hatte
`group_wounds`-Namenskollision + Scope-Selbstwiderspruch). Neue Richtung: `group_wounds`
universell für ALLE Gruppen-Einheiten → ein Schadenspfad. **Risk HIGH** (Regressionsfläche
Heal-/Damage-Pfad) — Plan: `docs/audit/plans/014-p17-defender-loss-allocation.md`.
Beide Pläne: vor Start Freigabe einholen.

### Offene Fragen / Retro-Vormerke
- **Output ↔ cache_read als Tempo-Indikator:** Zielwert-Feintuning `token_report.py`-Legende.

---

## Gate-Netz (Messbefehle)
- Tests + Coverage: `pytest --tb=short` (Floor 90 %, `pyproject.toml`).
- **Schulden-Scoreboard** nach jedem `pytest` (`tests/conftest.py`).
- Architektur (INV-1..4b): `pytest tests/architecture/ --no-cov -q`.
- Doku/Akzeptanz (INV-5): `pytest tests/docs/ tests/acceptance/ --no-cov -q`.
- **Token-Korridor:** <150k, bei ~135k Session beenden; Fleißarbeit PROAKTIV an Sonnet-Subagent.
- **Token-Report:** `python tools/token_report.py --write` → `docs/metrics/overview.md`.
- **History-Rotation:** `python tools/rotate_history.py --session <N> --summary "…"`.
- **Freigabe-Gate:** Edit/Write blockiert bis `touch .claude/.freigabe`; SessionStart re-armt.
