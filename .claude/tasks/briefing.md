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

## Aktueller Stand (nach S156, 2026-07-17)

S155-Review nachgeholt (R3-Regel): GO, `docs/handoff/S156_review.md`. S156-Abschluss-Review:
GO (`docs/handoff/S156_close_review.md`). B-056 Quantum Shielding fertig **und**
Stakeholder-UI-verifiziert (3 UI-Folge-Items B-103/104/105 gesichert) → archiviert. B-098
Teil 2 teilfertig: Berechnung+Loader-Guard+Daten stehen, Verdrahtung `combat.py` +
Profil-Auswahl-UI `_common.py` offen (R-COMBAT-35 `offen`). B-028 → per Stakeholder-Entscheid
auf Scope-Dokument (Option A) reduziert, Umsetzung S157 (11 reaktive Non-Stratagem-GOs ohne
GO-Card-Renderer). Handoff-Großreinigung durchgeführt (8 Dateien gesichert→gelöscht).
Gates (Abschluss-Vollsuite S156): **1903 passed / 99,11 %**; Arch+Doku+Acceptance 31 passed.

Frühere Sessions (S60–S155): Verlauf in `docs/metrics/session_archive.md` (Session-Historie).

### ▶ Nächster Schritt (S157)

Priorität = `docs/goals/backlog.md` (einzige Quelle).

- **(0) Retro-Maßnahmen-Entscheid** (`docs/handoff/S156_retro_s155.md`, NEEDS-DECISION,
  Maßnahmen 1–9) — Stakeholder wählt/gibt frei, danach übernommene Maßnahmen verankern.
- **(a) B-098-Rest:** −1-Hit-Malus-Verdrahtung in `combat.py` + Profil-Auswahl-UI in
  `_common.py` (R-COMBAT-35).
- **(b) B-028-Scope-Dokument** (Option A, kein Code) — Ist-Zustand der 11 Fähigkeiten,
  Aufwand neu schätzen.

**Offene Handoff-Marker:** `S156_planning.md` (ANSWERED), `S156_review.md` (ANSWERED),
`S156_close_review.md` (ANSWERED) — alle drei behalten bis S157-Start, dann löschbar;
`S156_retro_s155.md` (**NEEDS-DECISION**, Maßnahmen 1–9).

**Offene UI-Verifikationen:** keine offene Sammeldatei mehr — nächste Verifikationen erst
wieder mit dem neuen Template (Retro-Maßnahme 5) übergeben. Inhaltlich noch offen:
Counter-Offensive-Regelklärung + Dauersichtbarkeit (B-102), Silent-King-Fernkampf-Default
(B-068), PSI-Flow (B-009, Voraussetzungen zuerst klären); Spend-Guard weiter blockiert bis
Roster-Builder (B-067).

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
