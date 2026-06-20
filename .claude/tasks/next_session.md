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

## Aktueller Stand (nach S71, 2026-06-20)

**S71 — Subagent-Checkliste verankert · Coverage-Floor 90 % · Katalog Deployment/Scoring.**
(1) **Selbstprüf-Checkliste für Subagenten** kanonisch im Operating Model (Event 3
„Sprint") verankert — „Subagent-grün ≠ verdrahtet"; Verdrahtung per `grep` belegen, Heimat,
Gates, Beleg zurückliefern; Querverweis in `CLAUDE.md` (Subagent-Muster). Dogfooded:
beide Subagenten lieferten grep-Belege + Ratchet-/LEGIT-Warnungen.
(2) **Coverage-Floor 88 → 90 %** (`pyproject.toml`); CLAUDE.md-Drift 80→90 gefixt;
Messbefehl-Zeile aktualisiert. (3) **Ziel-Fortschritt-Zeile** im Review-Event verankert
(`operating_model.md` Event 5). (4) **Regel-Katalog +2 Bereiche** via Sonnet-Subagent:
Deployment (R-DEPLOY-01..09) + Mission-Scoring (R-SCORE-01..13); die 3 implementiert-Fälle
(`adjust_vp`, `adjust_secondary_vp`, VP-Render) mit **5 neuen VP-Tests** als `getestet: ja`
→ keine neue Schuld. **995 grün, Cov 92.40 %, Floor 90.**

**Vorbereitet (Subagent reviewt, Verdrahtung offen) — INV-4b/INV-4 Ledger:**
- **LEGIT (keine Schuld):** `rosz_importer._FACTION_MAP` (I/O-Normalisierung), `typing.Protocol`.
  Mögliche **stale Ledger-Einträge:** `dynasty`/`gloom`/`prism` (nur in Docstrings).
- **Quick-Wins (S, kein Test):** Fallback `"Necrons"/"Orks"` → `"Player 1/2"` in
  `gameHeader.py`+`gameProtocoll.py`; `setupScreen.py:434` Caption ohne Fraktionsname.
- **Renames (M, Tests mit):** `pending_irongob` → `pending_triggered_relic`; `res_orb_*`-
  State-Keys → generisch (`commandPhase`/`unitCard`/`game_state`).
- **Schema-Urteil (Konsens nötig):** `dakka`/`klaw`/`tesla` (Prosa-Suche → typisierte YAML-
  Felder), `reanimationProtocols`-String, `arkana`-Sektion, Default-Roster-Hardcode
  (`game_state.py` → `list_available_rosters()`).

Frühere Sessions (S60–S70): Verlauf in `docs/goals/ziel6.md` (Session-Historie).

### ▶ Nächster Schritt — INV-4b verdrahten (je eigene Freigabe)
1. **Quick-Wins zuerst** (risikoarm), dann **Renames mit Test-Update**; je Token grep-
   Vollständigkeit belegen, Ledger in `architecture_invariants.md` schrumpfen.
2. **Schema-/`arkana`-/Default-Roster-Fälle = Konsens** (Gate-Aufweichung/Prämisse) —
   nicht im Autopilot; Optionen mit Stakeholder klären.
3. Übrige offene Punkte: #3 Gates leser-orientiert prüfen (ADR-0002); #5 Refinement-
   Automatisierung; #6 Subagent-Peak-Hook (Design, Opus).

### Offene Frage / Retro-Vormerkung
- **Retro-Maßnahme (Nutzer S71, Screenshots):** Die Subagent-Peak-Darstellung „je Subagent
  der letzten Session" soll je **abgeschlossener Session erhalten/archiviert** bleiben (nicht
  überschrieben) — Session-Archiv im Token-Report/`overview.md`. In nächster Session umsetzen
  (`tools/token_report.py`); Verlaufstabelle bleibt, zusätzlich Pro-Session-Subagent-Block sichern.
- **Output ↔ cache_read als Tempo-Indikator** (S68): Output gegen Qualität gewichten, nicht
  maximieren — Interpretation in der Retro gemeinsam geschärft; ggf. Zielwert-Feintuning in
  `token_report.py`-Legende nachziehen, falls sich ein konkreter Korridor ergibt.

---

## Gate-Netz (Messbefehle)
- Tests + Coverage: `pytest --tb=short` (Floor 90 %, `pyproject.toml`).
- **Schulden-Scoreboard** erscheint nach jedem `pytest` (`tests/conftest.py`): Vokabular-
  Tokens, Allowlist, AC-IDs, next_session-Zeilen, Regel-Katalog-%. Ziel: Zahlen sinken.
- Architektur (INV-1..4b): `pytest tests/architecture/ --no-cov -q` · Ledger:
  `architecture_invariants.md`. Doku/Akzeptanz (INV-5): `pytest tests/docs/ tests/acceptance/ --no-cov -q`.
- **Regel-Katalog** (Nenner): `docs/spec/acceptance/rules.md` — Klasse A/B/C,
  `getestet: ja — <testname>`. Parser: `tests/acceptance/_rules.py`.
- **Token-Korridor:** <150k, bei ~135k Session beenden; Fleißarbeit an Sonnet-Subagent.
  `tools/session_context.py` eskaliert ab 120k/135k automatisch (S66).
- **Token-Report:** `python tools/token_report.py --write` → `docs/metrics/overview.md`
  (läuft automatisch bei `pytest`; PostToolUse-Reminder zum Teilen, S66).
- **History-Rotation (Abschluss):** `python tools/rotate_history.py --session <N> --summary "…"`
  hängt den Stand-Einzeiler an `ziel6.md` an und setzt den Stand-Block hier zurück (S69).
- **Freigabe-Gate (S66, hart):** Edit/Write blockiert bis `touch .claude/.freigabe`;
  SessionStart re-armt. Vollzieht die Freigabe-Pflicht über die Harness (ADR-0003).
