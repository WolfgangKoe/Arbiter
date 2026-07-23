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

## Aktueller Stand (nach S181, 2026-07-23)

**S181 abgeschlossen.** B-128(a) Doku-Angleichung erledigt — Warnhinweis-Text im
Subgruppen-Selector geprüft, Ergebnis: Silent-King bleibt bewusst hinweislos (S169-Entscheidung
bestätigt, kein Code-Rest). Retro-M4 (S180, ANGENOMMEN) umgesetzt: zweiter Aura-Spender
(`lokhust_lord`) im Test-Roster ergänzt — im Browser noch zu verifizieren
(`docs/handoff/S181_M4_verifikation.md`, AWAITING-VERIFICATION). B-128(b)
(Apply-Damage-Bereich vereinheitlichen) Mockup-Vorschlag vorgelegt
(`docs/handoff/S181_B128b_mockup.md`, NEEDS-DECISION, 4 offene Design-Entscheidungen D1–D4) —
B-128 bleibt OFFEN bis (b) entschieden. B-028c5 aus Token-Gründen vertagt.

**Governance:** Fehl-Commit `d88abca` (ein Screenshot-Subagent hatte eigenmächtig
`git add -A` + Commit ausgeführt) per soft-reset zurückgenommen. Zwei Retro-Regeln
eingepflegt: (1) „Subagenten führen NIE git-Operationen aus" —
`docs/reference/agent_scopes.md` §Pflichten für den Executor-Subagent; (2)
„Entscheidungs-Umkehr-Kontext-Pflicht" — `docs/governance/operating_model.md` §ev1 Planning.
Zwei neue Backlog-Items angelegt: B-132 (Loader-Caching-Prüfung, Retro-M5), B-133
(technischer Git-Commit-Blockier-Hook für Subagenten, Retro-1-Folge-Item).

Vollsuite: s. unten (nach Testlauf einzutragen).

Frühere Sessions (S60–S180): Verlauf in `docs/metrics/session_archive.md` (Session-Historie).

### ▶ Nächster Schritt

1. **Stakeholder verifiziert im Browser + entscheidet:** (a) M4 Mehr-Spender-Hinweis
   (`S181_M4_verifikation.md`), (b) B-128(b)-Mockup-Vorschlag (`S181_B128b_mockup.md`,
   D1–D4).
2. **B-028c5 nachholen** (in S181 aus Token-Gründen vertagt).
3. Backlog-Rang neu sortieren (nach M4/B-128(b)-Entscheid, plus B-132/B-133 einordnen).

**Offene Handoff-Marker:** `Stakeholder_Beobachtungen.md` (STANDING);
`S181_M4_verifikation.md` (AWAITING-VERIFICATION); `S181_B128b_mockup.md`
(NEEDS-DECISION); 2 behaltene Screenshots (`20-53-48` B-108 offen, `10-20-01` orphaned).

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
