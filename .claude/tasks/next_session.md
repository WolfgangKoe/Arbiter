# Startprompt — Nächste Session
<!-- Kanonisch: .claude/tasks/next_session.md — nie ins Root-Verzeichnis anlegen. -->
<!-- Nur „Stand + nächster Schritt + offene Fragen". Historie → session_archive.md; Backlog → backlog.md. -->
<!-- Referenz NICHT hier: Architektur → architecture.md, Regel-Gotchas → rules_insights.md, Constraints → CLAUDE.md. -->

## ⚠️ Session-Regeln
- **Start „start next session" → Planner-Subagent beauftragen** (liest `CLAUDE.md` + `docs/goals/archive/ziel6.md`
  + `docs/goals/backlog.md`, Scope aus `docs/reference/agent_scopes.md`); Entwurf als Datei, Koordinator
  legt vor, erst nach Freigabe los. Shortcut „Plan ist freigegeben" = direkt los. Einstieg `LEITSTAND.md`;
  Rollen/Tier/Modi: `docs/governance/operating_model.md`.
- **ADR-0007 (verbindlich seit S102):** Koordinator routet — liest keine Quelldateien/Vollergebnisse;
  Detail-Planung → Planner-Subagent; finales Review → Reviewer-Subagent. Asynchrone Stakeholder-
  Entscheidungen über Mailbox (`docs/handoff/`, NEEDS-DECISION → ANSWERED), nicht Chat.
  Details: `docs/governance/operating_model.md` [#events].
- **Ende:** Review (Reviewer-SA) → Retro → **Maßnahmen-Entscheid** (Stakeholder wählt) →
  Abschluss: **diese Datei** aktualisieren (ZUERST lesen, dann ergänzen) + ggf. Ziel-Checkboxen.
- **Doku-Gate:** Decke **120** Zeilen (Test rot darüber). Beim Reißen **tief auf ≤ 70** kürzen —
  Erledigtes → `backlog.md`/`session_archive.md`, Referenz → s. o.
- **Freigabe vor Umsetzung; kein Memory/Skill(datei-ändernd) ohne Freigabe; Subagenten =
  stehende Freigabe (proaktiv, ADR-0005); rote vorher-grüne Tests = STOP + fragen.** → `CLAUDE.md`.
- **Checkbox-Sync prüft auch Commit-Behauptungen:** Session-Start-Sync nicht nur gegen Ziel-Checkboxen,
  sondern auch Titel wie „archive/close" gegen Datei-Realität verifizieren (b3ebfd5 behauptete
  Archivierung ohne Vollzug, S119→S120-Befund). Restrisiko bewusst nicht test-bewacht — Kompensation:
  Reviewer-Pflicht + dieser Sync.

## Was ist Arbiter?
Digitaler Spielbegleiter WH40k 9E, Streamlit (Python). Start: `streamlit run src/app.py`
(Port 8501; **venv:** `source .venv/bin/activate`). Branch `feature/016` (Arbeit), `main` (nur PR).
**App permanent laufen lassen:** bei Session-Start nur kurz prüfen (`curl -s -o /dev/null -w "%{http_code}" http://localhost:8501` → 200), nur bei Bedarf neu starten — nicht den Nutzer fragen.

---

## Aktueller Stand (nach S121, 2026-07-04)

**S121 committed:** Stufe A Spieler-Spalten-Split komplett (`f9279fe`/`8c124c3`/`396fdec`:
`player: both`-Regelfix, zwei feste Spalten mit `stratagem_usable_by_player()`,
`used_stratagem_ids` als Dict pro Spieler-Slot) + `464bb40` (Bugfix aus UI-Test: CCW-Fallback
`ap="0"`→`ap=0`, Crash bei Einheiten ohne Nahkampfwaffe) + `6ebb04a` (ziel7 §0, Findings
F1–F4 im Backlog, Handoff gelöscht). Review: **GO ohne Auflagen.** UI-Verifikation: 1, 2, 5–7
bestätigt; 3+4 blockiert durch Plan 015. Retro M1+M2 in `agent_scopes.md` verankert.

Frühere Sessions (S60–S120): Verlauf in `docs/metrics/session_archive.md` (Session-Historie).

### ▶ Nächster Schritt

Planungskandidaten S122 (Stakeholder priorisiert im Planning):
(a) **Plan 015** reaktive Stratagem-UI (`docs/audit/plans/015-contextual-reactive-stratagems.md`,
TODO) — entsperrt Checkpunkte 3+4 (Fire Overwatch, Counter-Offensive sichtbar/nutzbar);
(b) **F1** Disruption Fields: Stärke-Modifier statt Wound-Roll-Modifier (`backlog.md` §5);
(c) **F3** natürliche 1 nie als Erfolg in der Würfel-UI (Berechnung prüfen + Darstellung);
(d) danach ziel7 **Stufe B** (Necrons) / **C** (Orks) aus `ziel7.md` §0, UX-Pass vor Ziel8.

**Merksatz S121:** Verifikations-Checklisten nur mit gegen den Ist-Stand prüfbaren Punkten;
Executor-Endbericht immer in derselben Antwort wie das Suite-Ende.

---

## Gate-Netz (Messbefehle)
- Tests + Coverage: `pytest --tb=short` (Floor **99 %**, `pyproject.toml`); **Schulden-Scoreboard** danach.
- Architektur: `pytest tests/architecture/ --no-cov -q`. Doku/Akzeptanz: `pytest tests/docs/ tests/acceptance/ --no-cov -q`.
- **Token-Korridor** <150k, bei ~135k beenden; Fleißarbeit PROAKTIV an Sonnet-Subagent.
- **Token-Report + History (M4, PFLICHT beim Abschluss):** `python tools/token_report.py --write` + `python tools/rotate_history.py --session <N> --summary "…"` — Koordinator stößt an.
- **Freigabe-Gate:** Edit/Write blockiert bis `touch .claude/.freigabe`; SessionStart re-armt.
