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

## Aktueller Stand (nach S118, 2026-07-03)

**S118 committed** (Review GO, 1393 passed, 99,11 %, Arch-Gate 8/8; `docs/handoff/review-S118.md`):
Carry-over-Cluster abgebaut — Plan 029 REJECTED; Carry-over (e) gestrichen (überholt);
`context-audit-S91.md` verarbeitet + gelöscht; DRY-Helper `_capped_modifier_threshold`
(`dice_html.py`); session-scoped `_canonical_streamlit_mock`-Fixture (`conftest.py`).
**UI-Pass S118 DONE** (17/20, `ui-pass-S118.md`) → Ziel7-Anforderungen **P19/P20/P21** in
`backlog.md` §5 (P21 = Bug: ↺-Undo überlebt Phasenwechsel). Retro verankert: Marker-Kontinuität
(operating_model Event 2), Test-Schuld §4d, Handoff-Hygiene.
**Merksatz (P21):** UI-Verhaltens-Claims aus Code-Analysen erst nach Live-Verifikation glauben.

Frühere Sessions (S60–S117): Verlauf in `docs/goals/ziel6.md` (Session-Historie).

### ▶ Nächster Schritt — Ziel7-Cluster (P19/P20/P21)

Planner-Subagent plant gegen `backlog.md` §5 (Ziel7-Cluster): **P21 (Bug) zuerst** — Undo-
Lebensdauer fixen, dabei Live-Verhalten vs. S113-Code-Analyse abgleichen (Root Cause). Danach
P19 (per-Spieler-Tracking) und P20 (Rapid-Fire-Eingabe). Alternative im Planning abwägen:
§6-Cluster (collect_modifiers/6f/6h).

### ⚠️ Carry-over (offen)

- **Manuelle UI-Verifikation (Rest aus S113 — war NICHT im S118-Pass):** Mirror-Protokoll
  Necron-vs-Necron Befehlsphase; stationär+D1 grünes +1-Save-Badge in den Würfeln.
  Quelle: `docs/handoff/review-S113.md`.

---

## Gate-Netz (Messbefehle)
- Tests + Coverage: `pytest --tb=short` (Floor **99 %**, `pyproject.toml`); **Schulden-Scoreboard** danach.
- Architektur: `pytest tests/architecture/ --no-cov -q`. Doku/Akzeptanz: `pytest tests/docs/ tests/acceptance/ --no-cov -q`.
- **Token-Korridor** <150k, bei ~135k beenden; Fleißarbeit PROAKTIV an Sonnet-Subagent.
- **Token-Report + History (M4, PFLICHT beim Abschluss):** `python tools/token_report.py --write` + `python tools/rotate_history.py --session <N> --summary "…"` — Koordinator stößt an.
- **Freigabe-Gate:** Edit/Write blockiert bis `touch .claude/.freigabe`; SessionStart re-armt.
