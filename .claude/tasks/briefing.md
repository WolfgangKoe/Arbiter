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

## Aktueller Stand (nach S179, 2026-07-23)

**S179 committet („Close S179"):** B-129 (`hardwiredForDestruction` Skorpekh Lord) + B-130
(Reroll-Marker Buff-Grün) + B-131 (Aura-Wound-Reroll-Hinweis, generisch) — alle drei vom
Stakeholder UI-verifiziert (positiv); B-129/B-130 archiviert, Log in `ui_verification_log.md`;
Governance B1–B4; Review GO (2 Minor-Doku-Fixes eingearbeitet); Vollsuite 2182 passed / 99,17 %.

**S180 Block A abgeschlossen + committet; Block B/C → frische Session (Sollbruchstelle laut
Plan, Koordinator-Kontext ~124k; Plan bleibt FREIGEGEBEN, `S180_planning.md`; Tier: Fable):**
Block B =
B-131-Nachbesserung (Stakeholder-Befunde aus Verifikation): (a) Hinweis-Kachel auf halbbreite
Player-Area-Spalte begrenzen (design_system.md §1.9.1), (b) neuer öffentlicher Accessor in
`abilityEngine.py` (analog `get_unit_rp_reroll_ability`) für lebende Aura-Spender, Hinweistext
listet Namen aus `unit.name_en` (INV-4b-konform, zerstörte Spender fallen raus). Danach Block C
(UI-Verif-Handoff `S180_B131b`, Vollsuite, Review, Retro, Commit).

### ▶ Nächster Schritt

1. Block B/C laut `S180_planning.md`; B-131 bleibt offen bis Stakeholder-Browser-Verifikation
   der Nachbesserung.
2. Danach (Backlog-Rang): B-128 · B-028c3/c4/c5 · B-005.

**Offene Handoff-Marker:** `Stakeholder_Beobachtungen.md` (STANDING); `S180_planning.md`
(NEEDS-APPROVAL — freigegeben, Datei löschen bei S180-Abschluss); `S180_retro.md`
(NEEDS-DECISION — Stakeholder sichtet am nächsten Session-Start).

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
