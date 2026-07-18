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

## Aktueller Stand (nach S165, 2026-07-18)

**Review S165: GO** (2018 passed, Coverage 99,14 %, Arch 8/8, mypy 0). Alle 4 S164-Retro-
Maßnahmen umgesetzt + in `agent_scopes.md` verankert. B-028c1: Sichtbarkeits-Bug behoben
(Diagnose 1a: Group-Flow-Früh-Return `fightPhase.py` + `inactive_override`-Zwilling; Fix 1b:
selektionsunabhängiger Scan `render_mortal_wounds_cards_for_destroyed` in 5 Phasen inkl.
psychicPhase, 4 alte Call-Sites entfernt, Erreichbarkeits-Tests mit Stash-Beweis). UI-
Verifikation Runde 1 dennoch **negativ** → Fable-Direktanalyse: fachliche Fehlklassifikation —
Vengeance ist die Standard-Familie **Explodes** (Pflicht-Trigger, KEINE GO; Wahapedia wörtlich
„it explodes", im YAML-rule_text verloren); dazu Design-System-Verstoß (Vollbreiten-Anker statt
Trigger-Ort §6.2) und Engine-Selbstwurf gegen „App würfelt nicht" (§6.3). Stakeholder folgt
den Empfehlungen: B-028c1 re-scoped auf „Explodes-Familie" (Blocked bis Mockup-Abnahme),
Governance-Ratchet in `agent_scopes.md` (UI-Briefs zitieren design_system-§, fachliche
Einordnung mit Wahapedia-Zitat, Mockup-Gate, Reviewer-Punkt Design-Konformität). Neue Items
B-122 (Menhir-LP 5 vs. 7, Scraper-Lücke) + B-123 (Schadens-Spillover Mehrmodell-Einheiten).

Frühere Sessions (S60–S164): Verlauf in `docs/metrics/session_archive.md` (Session-Historie).

### ▶ Nächster Schritt (S166)

1. **Mockup „Pflicht-Trigger-Kachel" (Explodes)** zur Stakeholder-Abnahme — erster Schritt vor
   jedem Code (Mockup-Gate). Danach Explodes-Paket: Schema (`effect.type: explode`,
   `mandatory`-Achse), Komponente + Anker, Tisch-Wurf-Baustein, `auto_explode`-GO (CP-Kosten,
   3 CP TITANIC), Datennacherfassung beider Fraktionen — Details B-028c1 in
   `docs/goals/backlog_details.md`.
2. Neue Items B-122 (Menhir-LP) + B-123 (Schadens-Spillover) einplanen.
3. Weiteres laut `docs/goals/backlog.md`.

**Offen:** Memory-Ergänzung `feedback_test_mandate` — Freigabe noch ausstehend.

**Offene Handoff-Marker:** `Stakeholder_Beobachtungen.md` (STANDING) ·
`S165_RETRO.md` (NEEDS-DECISION, Sichtung Start S166 — enthält DoR-Maßnahme,
Budget-Kalibrierung, Verifikations-Vorlage, Memory-Entscheid) — alle übrigen
S164/S165-Marker überführt und gelöscht.

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
