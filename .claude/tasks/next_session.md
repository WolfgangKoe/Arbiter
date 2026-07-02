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

## Aktueller Stand (nach S117, 2026-07-02)

**S117 committed** (Review GO, 1390 passed, 99.11 %, Arch-Gate 8/8): DS-2 Glyph-Rollout fertig
(28 Stellen + 1 Chip-Migration, 10 Dateien; `design_system.md` Ratchet-Rest = 0); P18 als stale-offen
erkannt (bereits S43/`e6fcdb3`) + abgehakt; **Fable integriert** (ADR-0008: Koordinator „Fable
präferiert, Opus Fallback", Fable-Tiering-Zeile, Reviewer-Ausnahme; `token_report.py` rendert
Fable als `▚`, Legende aus einer Quelle). Retro-Maßnahmen M1 (Vollsuite einmal/Ende/Vordergrund)
+ M2 (Budget-Eskalation >2×) in `operating_model.md` verankert.

**⚠️ OFFEN — gesammelte manuelle UI-Verifikation** (Render-Code coverage-ausgenommen):
S116-Punkte (Badges, `Inv N+`, Aura-Box, Rapid-Fire-Caption; `docs/handoff/review-S116.md`) +
S117 DS-2-8-Punkte-Checkliste (`docs/handoff/exec-DS2.md` §5) — beide Handoffs untracked.

Frühere Sessions (S60–S116): Verlauf in `docs/goals/ziel6.md` (Session-Historie).

### ▶ Nächster Schritt — Ziel7-Cluster

**Ziel7-Cluster ist LEER** — Design-System Schritt 1+2 ✓, Regel-Ledger 0 ✓, P17 ✓, P18 ✓ (stale, S43).

**1. Nächste Priorität im Planning klären** (Planner-Subagent gegen `backlog.md`): Kandidaten sind
   die Carry-over unten (ADR-0007-Reste, S110-Retro-Maßnahmen, Plan-029-Klärung) oder ein neues
   Backlog-Ziel (z.B. §6-Cluster: collect_modifiers/6f/6h — siehe backlog.md).
**2. Gesammelte manuelle UI-Verifikation abzeichnen** (S113/S116/S117, siehe oben + Carry-over) —
   idealerweise ein einziger UI-Pass am laufenden Streamlit.

### ⚠️ Carry-over (offen)

- **Manuelle UI-Verifikation (PFLICHT, im Ziel7-UI-Pass):** once_per_battle-Undo/Label-Pfade
  (Stratagem-Phase, Spielerwechsel); Mirror-Protokoll Necron-vs-Necron Befehlsphase; stationär+D1
  grünes +1-Save-Badge in den Würfeln. Checkliste: `docs/handoff/review-S113.md`.
- **ADR-0007-Reste:** (c) `docs/handoff/context-audit-S91.md` verarbeiten + löschen; (e) SessionStart-Regel-Injektion.
- **Retro-Maßnahmen (S110):** (1) DRY-Helper Hit/Wound ±1-Cap in `dice_html.py`; (2) st-Mock-Fixture.
- **Plan-029-Datei fehlt** (in README.md als Divergenz markiert) — vor Beauftragung anlegen oder REJECTED.

---

## Gate-Netz (Messbefehle)
- Tests + Coverage: `pytest --tb=short` (Floor **99 %**, `pyproject.toml`); **Schulden-Scoreboard** danach.
- Architektur: `pytest tests/architecture/ --no-cov -q`. Doku/Akzeptanz: `pytest tests/docs/ tests/acceptance/ --no-cov -q`.
- **Token-Korridor** <150k, bei ~135k beenden; Fleißarbeit PROAKTIV an Sonnet-Subagent.
- **Token-Report + History (M4, PFLICHT beim Abschluss):** `python tools/token_report.py --write` + `python tools/rotate_history.py --session <N> --summary "…"` — Koordinator stößt an.
- **Freigabe-Gate:** Edit/Write blockiert bis `touch .claude/.freigabe`; SessionStart re-armt.
