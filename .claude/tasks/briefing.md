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

## Aktueller Stand (nach S171, 2026-07-19)

**S171 committet:** Retro-Entscheid alle 3 Maßnahmen (M1 ×2,5 + M2 Marker-Sofort → `agent_scopes.md`,
M3 ↺-Glyph); Verifikation Testfälle 4–7 positiv → a/b/c/e/f verifiziert; Royal-Warden-Frage geklärt
(kein Bug — D6 MW pro Einheit); **Nacharbeit d komplett umgesetzt** (d1 State: Direkt-Apply +
Undo-Snapshots `unitMutations.py:578–650`; d2 Render: Nach-Confirm-Reset Lesart A, Sort-to-top
`gameState.py:318–352`, ↺-Glyph auf allen 4 Reset-Buttons; 22 neue Tests, 2 Alt-Tests begründet an
§1.6/§1.7 angepasst). Review: NO-GO→GO nach Marker-Korrektur (ANSWERED-Fehlgriff → Retro-M1 S171).
Gates: 2101 passed, 99,19 %, Arch 8/8, Doku 25, mypy 0.
**B-028c1 bleibt In Progress:** d-UI-Verifikation ausstehend (`S171_d_ui_verifikation.md`), b3 offen.
**Token-Lehre (S171):** ×2,5-Faktor kalibriert — d1 ~148k, d2 ~166k bei je 180k-Budget, kein Riss.

Frühere Sessions (S60–S170): Verlauf in `docs/metrics/session_archive.md` (Session-Historie).

### ▶ Nächster Schritt (S172)

1. **Retro-Entscheid** (`S171_RETRO.md` NEEDS-DECISION): M2-Schärfung (ANSWERED nur bei Löschung im selben Abschluss) + PLANNING-Lifecycle kodifizieren.
2. **d-Verifikation auswerten** (`S171_d_ui_verifikation.md`, 6 Testfälle) → bei Grün: 3 Verifikationsdateien löschen + B-028c1-Teilhaken d.
3. **T6/b3 `auto_explode`-GO** (~M, Annihilation Barge im Roster) + **B-122 „Careen!"** (XS–S); danach Spyder-Konzept / `backlog.md`.

**Offene Handoff-Marker:** `Stakeholder_Beobachtungen.md` (STANDING);
`S171_RETRO.md` (NEEDS-DECISION); `S171_d_ui_verifikation.md` (AWAITING-VERIFICATION);
`S170_b2bc_ui_verifikation.md` + `S169_b2_ui_verifikation.md` (AWAITING-VERIFICATION bis d grün, dann DELETE).

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
