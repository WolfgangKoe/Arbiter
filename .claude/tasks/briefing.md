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

## Aktueller Stand (nach S170, 2026-07-19)

**S170 committet:** Explodes-Kachel-Nacharbeiten b/c/a/e/f umgesetzt (Menhir-Hinweis weg,
Wurf-Karten-Resets, playerArea-Spaltensplit ①③/④ voll breit, Phasenwechsel räumt Kachel +
Log-Einträge, Reset unter Info-Kasten); Spec-first-Abnahme komplett (design_system §1.5–1.9.1,
P-16; Reset-Semantik = Lesart A in §1.6); P-16-Screenshots → In-Spec-Diagramme (5 PNGs weg);
Retro-M1/M2 verankert, M3-Allowlist eingetragen. Review S170: GO nach Marker-Korrektur.
Gates: 2080 passed, Coverage 99,18 %, Arch 8/8, Doku 25, mypy 0.
**B-028c1 bleibt In Progress:** offen d (Direkt-Apply + Nach-Confirm-Reset ins Panel, Lesart A)
+ ↺-Glyph-Minorfix, b3 `auto_explode`-GO, UI-Verifikation Testfälle 4–7.
**Token-Lehre:** T2 ~121k/60k, T4-aef ~244k/120k — je ×2 über ×1,5-Budget (→ Retro-M1 ×2,5).

Frühere Sessions (S60–S169): Verlauf in `docs/metrics/session_archive.md` (Session-Historie).

### ▶ Nächster Schritt (S171)

1. **Retro-Entscheid** (`S170_RETRO.md` NEEDS-DECISION): 3 Maßnahmen (×2,5-Faktor, Marker-Sofortwechsel, ↺-Glyph).
2. **UI-Verifikation einlösen** (`S170_b2bc_ui_verifikation.md` Testfälle 4–7 + `S169_b2_ui_verifikation.md`) → B-028c1-Teilhaken wenn grün.
3. **T4-d + T5/b3** (~M je Item): Direkt-Apply + Nach-Confirm-Reset ins Panel (Lesart A, §1.6/§1.7) inkl. ↺-Glyph; `auto_explode`-GO (Annihilation Barge als Träger vorhanden, kein Roster-Prep nötig).
4. **Backlog**: B-122 „Careen!" (Ork-GO vor Explodes-Wurf); Spyder-Konzept; weitere Prio laut `backlog.md`.

**Offene Handoff-Marker:** `Stakeholder_Beobachtungen.md` (STANDING);
`S170_RETRO.md` (NEEDS-DECISION);
`S170_b2bc_ui_verifikation.md` + `S169_b2_ui_verifikation.md` (AWAITING-VERIFICATION — letztere bleibt bis a–d verifiziert);
`S170_PLANNING.md` (nach S171-Sichtung löschen).

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
