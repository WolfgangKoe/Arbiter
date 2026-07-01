# Startprompt — Nächste Session
<!-- Kanonisch: .claude/tasks/next_session.md — nie ins Root-Verzeichnis anlegen. -->
<!-- Nur „Stand + nächster Schritt + offene Fragen". Historie → session_archive.md; Backlog → backlog.md. -->
<!-- Referenz NICHT hier: Architektur → architecture.md, Regel-Gotchas → rules_insights.md, Constraints → CLAUDE.md. -->

## ⚠️ Session-Regeln
- **Start „start next session" → Planner-Subagent beauftragen** (liest `CLAUDE.md` + `docs/goals/ziel6.md`
  + `docs/goals/backlog.md`, Scope aus `docs/reference/agent_scopes.md`); Entwurf als Datei, Koordinator
  legt vor, erst nach Freigabe los. Shortcut „Plan ist freigegeben" = direkt los. Einstieg `LEITSTAND.md`;
  Rollen/Tier/Modi: `docs/governance/operating_model.md`.
- **ADR-0007 (verbindlich seit S102):** Koordinator routet — liest keine Quelldateien/Vollergebnisse;
  Detail-Planung → Planner-Subagent; finales Review → Reviewer-Subagent. Asynchrone Stakeholder-
  Entscheidungen über Mailbox (`docs/handoff/`, NEEDS-DECISION → ANSWERED), nicht Chat.
  Details: `docs/governance/operating_model.md` [#events].
- **Ende:** Review (Reviewer-SA) → Retro → **Maßnahmen-Entscheid** (Stakeholder wählt) →
  Abschluss: **diese Datei** aktualisieren (ZUERST lesen, dann ergänzen) + ggf. ziel6-Checkboxen.
- **Doku-Gate:** Decke **120** Zeilen (Test rot darüber). Beim Reißen **tief auf ≤ 70** kürzen —
  Erledigtes → `backlog.md`/`session_archive.md`, Referenz → s. o.
- **Freigabe vor Umsetzung; kein Memory/Skill(datei-ändernd) ohne Freigabe; Subagenten =
  stehende Freigabe (proaktiv, ADR-0005); rote vorher-grüne Tests = STOP + fragen.** → `CLAUDE.md`.

## Was ist Arbiter?
Digitaler Spielbegleiter WH40k 9E, Streamlit (Python). Start: `streamlit run src/app.py`
(Port 8501; **venv:** `source .venv/bin/activate`). Branch `feature/016` (Arbeit), `main` (nur PR).
**App permanent laufen lassen:** bei Session-Start nur kurz prüfen (`curl -s -o /dev/null -w "%{http_code}" http://localhost:8501` → 200), nur bei Bedarf neu starten — nicht den Nutzer fragen.

---

## Aktueller Stand (nach S116, 2026-07-01)

**S116 committed** (Review GO, 1390 passed, 99.11 %, Arch-Gate grün, Ledger „impl. ohne Test" = 0):
Design-System Schritt 1 (`badges.py`/`symbols.py`/`design_system.md`, 4 Badge-Stellen konsolidiert),
Regel-Ledger auf 0 (R-COMBAT-17 Rapid-Fire-Caption + R-PROTO-02 datengetriebener Aura-Hinweis),
Invuln-Cleanup (SAVE-Block ohne `active`/`AP-Cover`, nur `Inv N+`). Abschluss-Fixes: E501 in `_vocab.py`,
`.gitignore` gegen Tooling-Artefakte gehärtet.

**⚠️ OFFEN — manuelle UI-Verifikation S116** (Render-Code coverage-ausgenommen, vor P18-UI-Pass prüfen):
Badge-Optik pixelidentisch; Invuln-Zeile nur noch `Inv N+`; Aura-Info-Box nur bei Direktive-1-primary;
Rapid-Fire-Caption; Glyphen (`⚔`/`↺`/Pfeile). Report: `docs/handoff/review-S116.md` (untracked).

Frühere Sessions (S60–S115): Verlauf in `docs/goals/ziel6.md` (Session-Historie).

### ▶ Nächster Schritt — Ziel7-Cluster

**Erledigt in S116:** Design-System Schritt 1 (Task 0) ✓ · Regel-Ledger auf 0 (Task 2) ✓.
**P18 war stale-offen** — bereits in `e6fcdb3` (S43, Plan 013) umgesetzt; S117 verifiziert + abgehakt.

**1. Design-System Schritt 2** [offen, Sonnet]: die in `design_system.md` etablierten `badge()`/`chip()`-
   Helfer + Symbol-Konstanten auf die restlichen Render-Stellen ausrollen; Token-Wertesatz je Badge-Klasse
   final vom User bestätigen lassen, falls noch offen.

### ⚠️ Carry-over (offen)

- **Manuelle UI-Verifikation (PFLICHT, im Ziel7-UI-Pass):** once_per_battle-Undo/Label-Pfade
  (Stratagem-Phase, Spielerwechsel); Mirror-Protokoll Necron-vs-Necron Befehlsphase; stationär+D1
  grünes +1-Save-Badge in den Würfeln. Checkliste: `docs/handoff/review-S113.md`.
- **ADR-0007-Reste:** (c) `docs/handoff/context-audit-S91.md` verarbeiten + löschen; (e) SessionStart-Regel-Injektion.
- **Retro-Maßnahmen (S110):** (1) DRY-Helper Hit/Wound ±1-Cap in `dice_html.py`; (2) st-Mock-Fixture.
- **Plan-029-Datei fehlt** (in README.md als Divergenz markiert) — vor Beauftragung anlegen oder REJECTED.

Frühere Sessions (S60–S114): Verlauf in `docs/goals/ziel6.md` (Session-Historie).

---

## Gate-Netz (Messbefehle)
- Tests + Coverage: `pytest --tb=short` (Floor **99 %**, `pyproject.toml`); **Schulden-Scoreboard** danach.
- Architektur: `pytest tests/architecture/ --no-cov -q`. Doku/Akzeptanz: `pytest tests/docs/ tests/acceptance/ --no-cov -q`.
- **Token-Korridor** <150k, bei ~135k beenden; Fleißarbeit PROAKTIV an Sonnet-Subagent.
- **Token-Report + History (M4, PFLICHT beim Abschluss):** `python tools/token_report.py --write` + `python tools/rotate_history.py --session <N> --summary "…"` — Koordinator stößt an.
- **Freigabe-Gate:** Edit/Write blockiert bis `touch .claude/.freigabe`; SessionStart re-armt.
