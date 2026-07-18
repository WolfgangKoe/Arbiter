# Koordinator-Briefing

<!-- Kanonisch: .claude/tasks/briefing.md — nie ins Root-Verzeichnis anlegen. -->
<!-- Zweck: Koordinator-Briefing bei Session-Start + Kontext-Zwischenspeicher -->
<!-- über Kontextfenster-Grenzen hinweg. Regeln → CLAUDE.md/operating_model.md/agent_scopes.md. -->

## Was ist Arbiter?

Digitaler Spielbegleiter WH40k 9E, Streamlit (Python). Start: `streamlit run src/app.py`
(Port 8501; **venv:** `source .venv/bin/activate`). Branch `dev` (Arbeit), `main` (nur PR).

**Die App muss dauerhaft laufen** (Stakeholder-Anweisung S152): bei Session-Start prüfen
(`curl -s -o /dev/null -w "%{http_code}" http://localhost:8501` → 200) und andernfalls im
Hintergrund starten (`streamlit run src/app.py --server.headless true`) — nicht beenden.

---

## Session-Routine — nur Verweise

- **Workflow/Freigabe-Gates/Session-Ablauf:** `CLAUDE.md`
- **Rollen/Model-Tier/Events:** `docs/governance/operating_model.md`
- **Scopes + Brief-Pflichten je Aufgabentyp:** `docs/reference/agent_scopes.md`
- **Einstieg für den Stakeholder:** `LEITSTAND.md`
- **Retro-Maßnahmen-Entscheid am Session-Start:** docs/governance/operating_model.md Event 1 (§ev1)

---

## Aktueller Stand (nach S167, 2026-07-18)

**Review S167: GO** (2018 passed, Coverage 99,14 %, Arch 8/8, Doku/Akzeptanz 25/25).
Governance-Session (kein `src/`-Code): **Spec-first-Gate** — jede neue ODER geänderte
UI-Bauform durchläuft erst Spec-Änderung (Mockup + `design_system.md`-Update) zur Abnahme,
dann Code (`agent_scopes.md` Punkt c) — plus Screenshot-Konvention (e), Diagnose-Ratchet
(„kein Bug" nur mit echtem Klickpfad-Repro) und **B-124** Design-System-Ratchet (bei jeder
UI-Berührung Bauform in `design_system.md` §1 nachtragen; Ist: ~9 dokumentierte Bauformen
vs. 48 Render-Funktionen). **Planner-Tier: ADR-0009** — durchgängig Opus + Lesedisziplin;
Sonnet-Ausarbeitung nur bei Schreib-Artefakten >~300 Zeilen (Anlass: S167-Planner lief
regelwidrig auf Sonnet, Drift gegen ADR-0008). **Explodes-Mockup V3 abgenommen** mit 3
verbindlichen Auflagen (kanonisch in `backlog_details.md` B-028c1 + §h-Antwort in
`S166_MOCKUP_EXPLODES.md`): ein Hinweiskasten unter der GO-Karte (Blau = Hinweis, kein
„Resolved"-Status), armyList nicht in der Spalte der Auswahlliste, „D6 Mortal Wounds" über
den Schadens-Zahlenfeldern. B-123 unangetastet (Budget-Check laut Plan).

Frühere Sessions (S60–S166): Verlauf in `docs/metrics/session_archive.md` (Session-Historie).

### ▶ Nächster Schritt (S168)

1. **Retro-Maßnahmen-Entscheid** (`docs/handoff/S167_RETRO.md`) — Tier-Abgleich beim
   Subagent-Start, Abschluss-Reihenfolge-Klausel.
2. **B-123-Umsetzung** (erster Task, frischer Kontext; Stakeholder-Richtung + Grenzfall-
   Testmatrix-Auflage in `backlog_details.md` B-123; Regel-Check Menhir-Lock +
   Boyz/Nob-Vergleich).
3. **§7-Spec-Überführung** Pflicht-Trigger-Kachel nach `design_system.md` inkl. der 3
   V3-Auflagen (Spec-first-Gate!) → danach B-028c1-Umsetzung planen.
4. Weiteres laut `docs/goals/backlog.md`.

**Offene Handoff-Marker:** `Stakeholder_Beobachtungen.md` (STANDING);
`S166_MOCKUP_EXPLODES.md` (+ `S167_MOCKUP_EXPLODES_V3.html` + `_V2.html` + Screenshots,
für die §7-Überführung gebraucht), `S167_REVIEW.md`, `S167_RETRO.md` NEEDS-DECISION —
Sichtung im S168-Planning.

---

## Gate-Netz (Messbefehle)

- Tests + Coverage: `pytest --tb=short` (Floor **99 %**); Architektur:
  `pytest tests/architecture/ --no-cov -q`; Doku/Akzeptanz:
  `pytest tests/docs/ tests/acceptance/ --no-cov -q`.
- **Token-Korridor** <150k, ab ~120k Wind-down, spätestens ~135k beenden; ab ~100k nichts
  Neues bei ausstehendem Review.
- **Abschluss-PFLICHT:** `python tools/token_report.py --write` +
  `python tools/rotate_history.py --session <N> --summary "…"`.
- **Freigabe-Gate:** Edit/Write blockiert bis `touch .claude/.freigabe`; SessionStart re-armt
  (Ausnahmen: `docs/handoff/`, außerhalb Repo).
