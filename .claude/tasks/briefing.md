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

## Aktueller Stand (nach S157, 2026-07-17)

S157-Review: GO (Befund gesichert→gelöscht, neue Abschluss-Regel). Geliefert: Retro-Maßnahmen
S155/S156 verankert (0a/0b); B-028-Scope-Dokument + Stakeholder-Entscheid **Option B** (Zuschnitt =
Planner-Auftrag S158; Auflagen: sessiongroße Tasks, App je Task lauffähig, `reanimation_protocols`
ist factionAbility — Klassifikation klären); **B-098-Rest fertig** (R-COMBAT-35 implementiert,
Kombi-Checkbox-UI, Nebenfund ranged `p.name` gefixt, melee = B-110); **B-103 fertig**
(`badge_label` aus YAML). Neue Items B-106–B-111. Retro S157: Maßnahmen 1, 2, 4 übernommen
(1+4 in `agent_scopes.md` verankert), 3 gestrichen. Gates (Abschluss-Vollsuite, Reviewer-Lauf):
**1915 passed / 99,12 %**; Arch 8, docs+acceptance 23, Ledger 0.

Frühere Sessions (S60–S156): Verlauf in `docs/metrics/session_archive.md` (Session-Historie).

### ▶ Nächster Schritt (S158)

Priorität = `docs/goals/backlog.md` (einzige Quelle).

- **(0) B-028-Zuschnitt** (Planner) — sessiongroße Tasks, App je Task lauffähig,
  RP-Klassifikation klären (Stakeholder-Auflagen aus S157-Entscheid Option B).
- **(a) B-109 Auto-fail-Fallback entfernen** (Stakeholder-Auftrag) — hartcodierten
  „Auto-fail"-Fallback in `always_fail_marker_row_html` durch verpflichtendes
  `badge_label`/Loader-Guard ersetzen.
- **(b) B-104/B-105/B-111** — Design-Crew-Schritt zuerst (Design-System-Baustein), dann
  Umsetzung.

**Offene UI-Verifikationen:** Kombi-Checkboxen (B-098) + Quantum-Shielding-Badge (B-103;
Badge erscheint, aber Truncation-Befund B-111).

**Offene Handoff-Marker:** keine.

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
