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

## Aktueller Stand (nach S172, 2026-07-19)

**S172 committet:** S171-Retro verankert (M2-Schärfung + PLANNING-Lifecycle → `agent_scopes.md`);
**d-Repair** (Bug 1: `st.rerun()` im `number_input`-Zweig `_common.py`; Bug 2: `last_touched`-Pin
in `pinned_explode_target_keys`, §1.7 neu); **b3 `auto_explode`-GO „Curse of the Phaeron"**
(generisches `cp_overrides`-Schema, GO-Karte Baustein ②, 15 Tests, R-COMBAT-45).
Stakeholder-Live-Verifikation Testfälle 1–3 positiv → **B-028c1 Done + archiviert**.
B-125 (Nach-Confirm-Reset setzt Wunden zurück, Lesart-A-Verstoß) + B-126 (MW-Cap fehlt) neu;
B-122 um Platzierungsvorgabe ergänzt; R-COMBAT-41–44-Drift gefixt. Review: **GO im ersten
Anlauf**. Gates: 2123 passed, 99,20 %, Arch 8/8, Doku 25.
**Token-Lehre (S172):** zwei Budget-Risse (Recherche+Schema+UI-Brief 292k vs. 190k;
Haiku-Archivierung 138k vs. 40k) und 2× verlorener Hintergrund-pytest → Retro-Maßnahmen 1–3
in `S172_RETRO.md`.

Frühere Sessions (S60–S171): Verlauf in `docs/metrics/session_archive.md` (Session-Historie).

### ▶ Nächster Schritt (S173)

1. **Retro-Entscheid** (`S172_RETRO.md` NEEDS-DECISION): Vollsuite-synchron-Baustein,
   Recherche-Budget-Aufschlag, Archivierungs-Brief-Typ.
2. **B-125 + B-126** (Explodes-Panel: Nach-Confirm-Reset-Wunden + MW-Cap; je S, ~40–60k) —
   gleicher Code-Bereich, ggf. ein gemeinsamer Brief ≤ M.
3. **B-122 „Careen!"** (XS–S; GO-Karte an Baustein ② wie Curse of the Phaeron, Vorgabe in
   Backlog-Zeile); danach B-028c2 (`reroll_rp`) / Spyder-Konzept laut `backlog.md`.

**Offene Handoff-Marker:** `Stakeholder_Beobachtungen.md` (STANDING);
`S172_RETRO.md` (NEEDS-DECISION).

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
