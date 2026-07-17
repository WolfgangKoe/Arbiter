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

---

## Aktueller Stand (nach S159, 2026-07-17)

Würfelsymbol-Katalog freigegeben + `design_system.md` §4.1–§4.4 übernommen (Ratchet: erst
Katalog-Zeile, dann Code) — §4.2 Würfelflächen-Katalog, §4.3 Effekt-Symbol-Katalog (ersetzt
altes §4.1), §4.4 Wurf-Block-Pattern inkl. 6 dokumentierten Vereinheitlichungs-Lücken
(SAVE/Invuln/DAMAGE, B-114…B-118). B-104 auf S158 negativ verifiziert (Text-Chip statt echtem
SVG) → neuer Zuschnitt gegen den Katalog, Executor-Brief `S159_planning.md` Task 2. B-028b:
erste B-028a-Callsite (`noctilith_beacons`, Necron-Silent-King), additiv nicht gatend,
`can_deny()` um Ability-Quellen erweitert; UI-Testfall 1+2 positiv, Testfall 3 (Regression)
offen — β-Roster (`data/rosters/necrons_beta.yaml`) um Canoptek Spyder/Gloom Prism ergänzt,
Loader-Test jetzt 6 Einheiten (Stakeholder-Freigabe), Prüfung selbst steht noch aus. B-112:
mypy-Baseline 24→25 angehoben (Drift stale seit vor S158) — die 25 realen Fehler bleiben
sichtbare Schuld, Ratchet-Ziel weiterhin senken statt Baseline halten. Gates (Abschluss):
Doku/Acceptance 23 passed, Arch 8. Review S159: GO (kein inhaltlicher Blocker).

Dice-Cluster B-104→B-109→B-105 (Task 2–4 aus `S159_planning.md`) nach S160 verschoben
(Token-Korridor) — Briefs liegen fertig vor, direkt gegen `design_system.md` §4 beauftragbar.

Frühere Sessions (S60–S158): Verlauf in `docs/metrics/session_archive.md` (Session-Historie).

### ▶ Nächster Schritt (S160)

Priorität = `docs/goals/backlog.md` (einzige Quelle).

1. **Retro-Maßnahmen-Kandidaten entscheiden:** [M1] Subagent-Briefs: Verbot, auf
   Hintergrund-Monitore zu warten — Gates im Vordergrund abschließen (2× Nachstoß nötig in
   S159); [M2] Testfall-Voraussetzungen (Roster-Bestand) beim Task-Zuschnitt prüfen
   (Testfall-3-Blocker B-028b).
2. **Dice-Cluster:** B-104 (Task 2) → B-109 (Task 3) → B-105 (Task 4), Briefs in
   `S159_planning.md`.
3. **B-028b Testfall 3 Befund** (Stakeholder, β-Roster jetzt bereit).

**Offene Handoff-Marker:** `S158_B104_ui_verifikation.md` (neuer Zuschnitt, B-104 negativ),
`S159_B028b_ui_verifikation.md` (Testfall 3 offen), `S159_planning.md` (bleibt als
Brief-Quelle für Task 2–4).

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
