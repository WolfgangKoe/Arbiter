# Koordinator-Briefing

<!-- Kanonisch: .claude/tasks/briefing.md — nie ins Root-Verzeichnis anlegen. -->
<!-- Zweck: Koordinator-Briefing bei Session-Start + Kontext-Zwischenspeicher -->
<!-- über Kontextfenster-Grenzen hinweg. Regeln → CLAUDE.md/operating_model.md/agent_scopes.md. -->

## Was ist Arbiter?

Digitaler Spielbegleiter WH40k 9E, Streamlit (Python). Start: `streamlit run src/app.py`
(Port 8501; **venv:** `source .venv/bin/activate`). Branch `dev` (Arbeit), `main` (nur PR).

---

## Session-Routine — nur Verweise

- **Workflow/Freigabe-Gates/Session-Ablauf:** `CLAUDE.md`
- **Rollen/Model-Tier/Events:** `docs/governance/operating_model.md`
- **Scopes + Brief-Pflichten je Aufgabentyp:** `docs/reference/agent_scopes.md`
- **Einstieg für den Stakeholder:** `LEITSTAND.md`

---

## Aktueller Stand (nach S151, 2026-07-16)

S151: Backlog-Restrukturierung komplett — `backlog.md` = eine ID-Prioritätsliste (B-001–B-099,
Ziel oben, Legende unten), Details in `backlog_details.md`, 46 Einträge + Ziel-Historie archiviert,
`index.md` aufgelöst; `next_session.md` → `briefing.md` (Regelblock in operating_model/agent_scopes
konsolidiert); 5 neue Wächter (`tests/docs/test_backlog_structure.py`). Vollsuite 1870 passed /
99,14 %, mypy 24. **Review + Retro S151 ÜBERSPRUNGEN (Stakeholder-Entscheid).**

Frühere Sessions (S60–S150): Verlauf in `docs/metrics/session_archive.md` (Session-Historie).

### ▶ Nächster Schritt (S151-Fortsetzung / S152)

Priorität = `docs/goals/backlog.md` (einzige Quelle). **B-099 zuerst** (Backlog-Feinschliff:
Stale-Kandidaten B-092–B-097 löschen, Spalten-/Effort-Format, Details-Template), danach die
bisherigen ID-Referenzen behalten:

- **B-001** FixD Brief 2 + 3 (Compute/Render-Folge)
- **B-002** K1-Daten-Fix (Nihilakh/Mephrit-Wortlaute)
- **B-026 / B-028** used-on-Generalkonzept (Suffix auf alle reaktiven GOs)
- **B-056** Quantum Shielding (fester Invuln 4+ + Anzeige-Bug)
- **B-098** Boss Nob 7b (Kombi-Waffenprofile `orks/weapons.yaml`)

**Offene Handoff-Marker:** `S151_backlog_inventar.md` (ANSWERED — nach
Stakeholder-Kenntnisnahme löschen); `S147_go_audit_ork_abilities.md` +
`S147_go_audit_stratagems.md` (ANSWERED); `S141_ui_befunde_group_a.md` (ANSWERED, behalten
bis FixC + FixD Brief 2/3); `S150_usedon_renderpaths.md` (ANSWERED, behalten bis
used-on-Generalkonzept).

**Offene manuelle UI-Verifikation:**

- Spend-Guard (tisch-aufgelöstes Stratagem ohne Einheit) — blockiert bis Roster-Builder (B-067).
- B12b-Rest (Movement-Advance-Reroll-Randfall) — B-027, spec-konform, kein Bug.

**Offene Stakeholder-Entscheidung:** markdownlint-Trial (S137–S139, `.markdownlint.jsonc` +
`npm run lint:md`) — behalten oder entfernen? Kein Backlog-Eintrag; ohne Governance-Zielort,
bleibt hier bis zur Entscheidung.

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
