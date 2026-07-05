# Startprompt — Nächste Session
<!-- Kanonisch: .claude/tasks/next_session.md — nie ins Root-Verzeichnis anlegen. -->
<!-- Nur „Stand + nächster Schritt + offene Fragen". Historie → session_archive.md; Backlog → backlog.md. -->
<!-- Referenz NICHT hier: Architektur → architecture.md, Regel-Gotchas → rules_insights.md, Constraints → CLAUDE.md. -->

## ⚠️ Session-Regeln
- **Start „start next session" → Planner-Subagent beauftragen** (liest `CLAUDE.md` + `docs/goals/ziel7.md`
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

## Aktueller Stand (nach S126, 2026-07-05)

**S126 (Plan 040 + Mitfix):** `5982751` — tote Stage-Maschine entfernt (`advance_stage`,
`render_start/end`, `phase_stage`) **plus** Stakeholder-Mitfix: Stage-Hart-Filter aus
`stratagem_visibility()` raus — `stage: start/end`-Stratagems waren dauerhaft `hidden`
(Bestandsbug). `Stratagem.stage`/`Ability.stage` bleiben als Datenfelder ohne Verhalten.
2 vorher grüne Szenario-Tests mit Stakeholder-OK migriert (`test_legacy_phase_stage_key_
is_ignored`). Vollsuite 1451 passed, Coverage 99,11 %, alle Gates grün. Plan 040 archiviert.
Review-Blocker (Spec-Drift `architecture.md`/`processes.md`/`ui_layout.md`) noch in S126
nachgezogen. **UI verifiziert (Stakeholder):** 034 alle 4 Punkte ✅, 036 Header ✅,
040 Dimensional Corridor sichtbar ✅ + RP-Gegenprobe ✅ + Legacy-Szenarien laden ✅.

Frühere Sessions (S60–S125): Verlauf in `docs/metrics/session_archive.md` (Session-Historie).

### ▶ Nächster Schritt

**Plan 038 ausführen** (mypy-Ratchet-Gate, P2, M), danach **039 → 041**. Regeln:
041 zwingend nach 034 (✅) + 040 (✅), NICHT parallel zu 015/026, erst nach 015/026.
Pläne self-contained → Executor-Subagent direkt beauftragbar.

**Offene Verifikation (VOR Merge nach `main`):**
- **037 Docker**: `docker build` + `docker run --rm arbiter-test id -u` → 1000 +
  Port-7860-Smoke beim nächsten HF-Spaces-Deploy (lokal kein Docker).

**Offene Punkte / Merksätze:**
(a) Retro S123: Archiv-Executor umging das Freigabe-Gate per Bash-Schreibzugriff —
Maßnahme in nächster Retro entscheiden.
(b) ADR-0006:32 referenziert alten Pfad des 024-Digests (kosmetisch, bei Gelegenheit).
(c) Merkposten `hand_of_the_phaeron`/ExtraUses steht in Plan 032.
(d) Direction-Entscheide offen (Audit S124): ziel9-Fetcher vorziehen? Deployment-Phase
bauen oder ADR „bleibt am Tisch"? Mission-Scoring (eine Mission end-to-end)?
(e) Merkposten: 6 ungenutzte Loader-Funktionen (`load_points` u. a.) — Intent klären
(ziel9-Scaffolding?), dann löschen/behalten (Rejected-Liste plans/README).
(f) Retro S124: ab ~6 Plänen splitten oder Entwürfe an Sonnet delegieren.
(g) Retro S126: Lösch-Pläne → Executor-Selbstprüfliste MUSS entfernte Bezeichner
auch über `docs/spec/` greppen (S126-Blocker: 2 Specs beschrieben Gelöschtes).
(h) Retro S126: App VOR jeder UI-Verifikation neu starten (alter Prozess/State
lieferte 4 falsche ❌); UI-Prüfanleitungen vorher gegen Roster-Realität validieren
(Flayed-Ones-Check ohne Roster-Deckung, „Szenario-UI" existiert nicht — nur
`?scenario=`-Query-Param).

---

## Gate-Netz (Messbefehle)
- Tests + Coverage: `pytest --tb=short` (Floor **99 %**, `pyproject.toml`); **Schulden-Scoreboard** danach.
- Architektur: `pytest tests/architecture/ --no-cov -q`. Doku/Akzeptanz: `pytest tests/docs/ tests/acceptance/ --no-cov -q`.
- **Token-Korridor** <150k, bei ~135k beenden; Fleißarbeit PROAKTIV an Sonnet-Subagent.
- **Token-Report + History (M4, PFLICHT beim Abschluss):** `python tools/token_report.py --write` + `python tools/rotate_history.py --session <N> --summary "…"` — Koordinator stößt an.
- **Freigabe-Gate:** Edit/Write blockiert bis `touch .claude/.freigabe`; SessionStart re-armt.
