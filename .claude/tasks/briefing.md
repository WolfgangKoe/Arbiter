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

## Aktueller Stand (nach S158, 2026-07-17)

B-028-Zuschnitt freigegeben+verbucht (7 Teil-Tasks B-028b…c5); **B-028a fertig+archiviert**:
additive Reactive-Ability-Infrastruktur `reactive_abilities_for`/`ability_visibility`/
`spend_ability`/`undo_ability`/`render_reactive_ability_box`, State-Schlüssel
`used_ability_ids`/`ability_use_anchors`, 0 Produktiv-Callsites (Callsite folgt B-028b).
Design-Konsens: B-104 = Variante A (fertig, `_triggered_die_chip_html` in `_marker_row_html`,
`design_system.md` §4.1), B-105 = Variante A (offen, Design-Crew-Datei `S158_design_crew.md`
liegt), B-111 = Variante C (fertig, Truncation bleibt + `title`-Tooltip, Regressionstest per
Stakeholder-Entscheid Option 1 auf sichtbaren Inhalt präzisiert). Roster
`necrons_b1_verification.yaml` → `necrons_quantum_shielding.yaml` umbenannt (Stakeholder-
Entscheidung, alle 4 Archiv-Referenzen nachgezogen). Gates (Abschluss): Vollsuite
**1962 passed / 99,13 %**; Arch 8, Doku/Acceptance 23. mypy-Baseline stale (Baseline 24, real
25 auf HEAD `9a62f13`) → Backlog-Item B-112. Review S158: NO-GO→GO nach Blocker-Klärung
(Roster-Umbenennung war beabsichtigt, kein Datenverlust). Retro S158: Maßnahmen 1–6
übernommen — 1–4 in `docs/reference/agent_scopes.md` verankert (Git-Werkzeug-Verbot,
Parallel-Executor-Regel, Lösch-Whitelist-Pflicht, Core+UI+Test-Split-Default), 5–6 als
Backlog-Items B-112 (mypy-Baseline) und B-113 (Skorpekh/Destroyer-Lord-Reroll).

Frühere Sessions (S60–S157): Verlauf in `docs/metrics/session_archive.md` (Session-Historie).

### ▶ Nächster Schritt (S159)

Priorität = `docs/goals/backlog.md` (einzige Quelle).

- **B-028b** (Deny-Psychic-Konsolidierung, erste Callsite über B-028a-Infrastruktur).
- **B-109** (Auto-Fail-Fallback entfernen, verpflichtendes `badge_label` aus YAML).
- **B-105** (`go_source_chip`-Variante A umsetzen, Design-Crew-Datei liegt bereits vor).
- **B-112** (mypy-Ratchet-Baseline korrigieren).

**Offene UI-Verifikationen:** B-104 (Testfall 1 — Würfelsymbol-Sichtprüfung offen), B-111,
zusätzlich B-098/B-103 aus S157.

**Offene Handoff-Marker:** `S158_design_crew.md` (B-105 offen), `S158_B104_ui_verifikation.md`
(Testfall 1 offen; Skorpekh-Befund → B-113), `S158_B111_ui_verifikation.md` (offen).

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
