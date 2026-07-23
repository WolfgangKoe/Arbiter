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

## Aktueller Stand (nach S180, 2026-07-23)

**S180 komplett (Block A + B/C):** B-131-Nachbesserung umgesetzt und ABGESCHLOSSEN —
(a) Aura-Hinweis-Kachel halbbreit (`st.columns(2)`-Linksspalte, `rp_col`-Muster, §1.9.1),
(b) Accessor `get_wound_reroll_aura_donor_names` in `abilityEngine.py` (lebende Spender),
`ResolutionContext.wound_reroll_aura_donor_names`, Hinweistext nennt Spender aus `unit.name_en`
(INV-4b-Scoreboard unverändert 6/16/3). Stakeholder hat noch in S180 im Browser verifiziert
(Prüfpunkte 1–3 positiv; Mehr-Spender nur unit-getestet → Retro-M4); B-131 archiviert, Log in
`ui_verification_log.md`. Review GO (2 Minor eingearbeitet: Lokhust-Tippfehler, Loader-Caching
→ Retro-M5). Retro-Entscheide: Block A M1/M2 abgelehnt, M3 bestätigt; Block C M4 ANGENOMMEN.
Vollsuite 2187 passed / 99,08 %; Architektur 8/8; Docs+Acceptance 25/25.

Frühere Sessions (S60–S179): Verlauf in `docs/metrics/session_archive.md` (Session-Historie).

### ▶ Nächster Schritt

1. **Retro-M4 (Stakeholder-Entscheid noch in S180: ANGENOMMEN):** zweiten Aura-Spender
   (z. B. Lokhust Lord) in `necrons_test.yaml` aufnehmen (~5k, reine Daten-Änderung), danach
   Mehr-Spender-Hinweis im Browser verifizieren (bislang nur unit-getestet).
2. Backlog-Rang (umsortiert S180): B-128 · B-028c3/c4/c5 · B-005.
3. Retro-Rest sichten: M5 (Loader-Caching-Backlog-Item) noch unentschieden; M6 nur Bestätigung.

**Offene Handoff-Marker:** `Stakeholder_Beobachtungen.md` (STANDING); `S180_retro.md`
(NEEDS-DECISION — Block A entschieden, Block-C-Maßnahmen sichtet der Stakeholder am
nächsten Session-Start).

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
