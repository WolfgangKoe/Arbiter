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

## Aktueller Stand (nach S106, 2026-06-27)

**S106 — Governance-Konsistenz + Artefakt-Verschlankung (dünner Koordinator, voll delegiert).**
- **Steuerung gehärtet:** Coverage-Gate überall **92 %** (war divergent 80/90); Delegations-MUST in
  `operating_model` verankert + „führt selbst aus" entfernt (ADR-0007); Scope-Pflicht + Kanal-Regel
  repo-kanonisch; Subagent-Brief-Template in `agent_scopes`; Memory `proactive_subagent_prep` an ADR-0005.
- **M3 ✅:** `operating_model` mit Abschnitts-Karte + stabilen Ankern (`#ev1`–`#ev7`, `#events` …).
- **Verschlankung:** ziel1–5 + doku.md → `docs/goals/archive/`; ziel6 1744→1189 (6a–6d → archive/,
  offene Restpunkte konservativ zurückgeholt — **kein Offenes nur im Archiv**); backlog 370→292;
  plans/README DONE-Pläne in Archiv-Sektion. Vollsuite 1170 grün, 93,22 %, Arch-Gate grün.
- **M4 ✅:** diese Datei gekürzt (S103/S104-Detail → `session_archive.md`).

**S104/S103 (Detail → `session_archive.md`):** O2-Tiering MUST + Pläne 027/028; Plan 025 Step 4
(D1 light_cover) committed; ADR-0007 dünner Koordinator (S101/S102).

### Nächster Schritt — 025-Linie
Reihenfolge **025 → 016 → 018 → 015 → 026 → 017** (s. `docs/audit/plans/README.md`). Executor-SA mit **Write**.
- **M1 — Overwatch-Anzeige:** statische Caption `chargephase.py:144` („trifft auf 6+") erst mit
  Overwatch/Hold-Steady korrekt → in **Plan-015-Scope** (durch echtes Overwatch ersetzen).

### ⚠️ Carry-over (offen)
- **ADR-0007-Reste:** (c) `docs/handoff/context-audit-S91.md` verarbeiten + löschen;
  (e) SessionStart-Regel-Injektion (S95-Beleg). [(f) M3 ✅ · (g) M4 ✅ — S106]
- **Plan 025** aktive Hauptlinie; Bug 3 (Zweitspieler-Direktiv-Wahl) + INV-4b-Restschuld nebenher.
- **Manuelle UI-Verifikation (PFLICHT):** (a) Mirror-Protokoll Necron-vs-Necron Befehlsphase;
  (b) Bug 5 Runde-2-Fernkampf-Zielwahl; (c) S103 stationär+D1 grünes +1-Save-Badge IN den Würfeln.

### Offene Fragen / Vormerke
- **Design-System-Crew:** Buff-/Direktiv-Hinweis-Komponente, sobald 025 Effekte festlegt.
- **S95-Vormerk:** Regelkonformität beim YAML-Modellieren prüfen (DoD-#1-Ergänzung).
- **doku.md** nach `archive/` verschoben (war erledigtes Audit) — bei Bedarf ganz löschbar.

---

## Gate-Netz (Messbefehle)
- Tests + Coverage: `pytest --tb=short` (Floor **92 %**, `pyproject.toml`); **Schulden-Scoreboard** danach.
- Architektur: `pytest tests/architecture/ --no-cov -q`. Doku/Akzeptanz: `pytest tests/docs/ tests/acceptance/ --no-cov -q`.
- **Token-Korridor** <150k, bei ~135k beenden; Fleißarbeit PROAKTIV an Sonnet-Subagent.
- **Token-Report:** `python tools/token_report.py --write`. **History:** `python tools/rotate_history.py --session <N> --summary "…"`.
- **Freigabe-Gate:** Edit/Write blockiert bis `touch .claude/.freigabe`; SessionStart re-armt.
