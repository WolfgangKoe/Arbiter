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

## Aktueller Stand (nach S161, 2026-07-17)

**Review S161: GO** (Vollsuite 1990 passed, Coverage 99,13 %, Arch 8 grün). Fünf Plan-Tasks
+ ein Wiring-Folge-Task, Welle 1 (T1/T2/T4/T5) parallel mit disjunkten Dateien:
- **Retro-M1 (T1) DONE:** neuer Handoff-Marker `AWAITING-VERIFICATION` für „wartet auf
  Stakeholder-Sichtprüfung" — definiert in `docs/handoff/README.md`, Wächter
  `tests/docs/test_handoff_hygiene.py` (in `_VALID_MARKERS`, NICHT `_STALE_MARKERS`),
  Brief-Pflicht in `agent_scopes.md`. `NEEDS-DECISION` bleibt echten Entscheidungen vorbehalten.
- **B-109 (T2) → UI-Verifikation:** Auto-Fail-Badge-Label verpflichtend aus YAML, Fallback
  `"Auto-fail"` entfernt, Loader-Guard (`loader.py`) wirft laut bei fehlendem Label.
- **B-105 (T3) + Wiring → UI-Verifikation:** generischer `go_source_chip`; Stärke-Chip
  rewired (Tooltip, **vom Stakeholder sichtbestätigt**); Invuln-Quellenname jetzt real
  durchgereicht (`_stratagem_invuln_best` in `src/uiLayout/_common.py`, Tiebreak: Gleichstand
  → Fähigkeitslabel). **Planungslücke-Erkenntnis:** „deckt Wunsch X" ≠ „Wunsch sichtbar
  geliefert" — B-105 brauchte den nachgeschobenen `_common.py`-Wiring-Task, damit „Inv N+
  [Quantum Deflection]" überhaupt im Spiel erscheint.
- **B-119 (T4):** im Backlog hinter B-028b einsortiert (teilt Deny-/GO-Infrastruktur).
- **Prozess (T5):** Retro-Entscheid = Input, nicht Planungsgegenstand — verankert in
  `operating_model.md` Event 1 (§ev1). Retro S161 = **M3** (nichts weiter verankern).

Aus S160 offen geblieben: `gloom_prism`-Migration auf die B-028a-Infrastruktur (B-028b-Rest).

Frühere Sessions (S60–S160): Verlauf in `docs/metrics/session_archive.md` (Session-Historie).

### ▶ Nächster Schritt (S162)

Priorität = `docs/goals/backlog.md` (einzige Quelle).

1. **Zwei offene `AWAITING-VERIFICATION`-Handoffs** warten auf Stakeholder-Sichtprüfung im
   Spiel: `docs/handoff/S161_B105_ui_verifikation.md` (Invuln-Chip-Teil noch offen — Strength
   bereits bestätigt) und `docs/handoff/S161_B105wiring_ui_verifikation.md`
   („Inv N+ [Quantum Deflection]" am Rettungswurf). Nach Bestätigung: B-105/B-109 auf DONE,
   Handoffs gemäß Lifecycle löschen.
2. Nächste Backlog-Priorität nach B-028b/B-119 laut `docs/goals/backlog.md`.

**Offene Handoff-Marker:** `S161_B105_ui_verifikation.md`, `S161_B105wiring_ui_verifikation.md`
(beide `AWAITING-VERIFICATION`), `S161_planning.md`, `S161_review.md`.

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
