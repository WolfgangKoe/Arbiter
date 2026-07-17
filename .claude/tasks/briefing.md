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

## Aktueller Stand (nach S160, 2026-07-17)

**B-104 DONE:** Auto-fail-/Reroll-Marker als echtes Würfel-SVG gemäß `design_system.md`
§4.2/§4.3 — `dice_face_svg`/`miss_die_html` mit additivem `miss_color`-Parameter (Default
bytegleich, per Snapshot-Regressionstests gepinnt), `always_fail_marker_row_html` nutzt
`miss_die_html(color=_modifier_color(…))`; Reroll-↺ ebenfalls SVG (`_reroll_die_svg`, noch
ohne Producer — wartet auf B-113). Stakeholder visuell bestätigt; Review S160: **GO**
(Vollsuite 1975 passed, Coverage 99,13 %, Arch 8, Doku 23, mypy 25 = Baseline). **B-028b
UI-Verifikation komplett** (Testfälle 1–3 positiv, Testfall 3 mit Canoptek Spyder/Gloom
Prism) — offener Rest: `gloom_prism`-Migration auf die B-028a-Infrastruktur. Daraus neue
Beobachtung als **B-119** überführt (Deny-Quellen-Anzeige: gameActionsArea nennt beim
Wargear-Deny keine Einheit/Quelle — beim Silent King via GO-Karte eindeutig, beim Spyder
nicht). Retro-Maßnahmen S159 verankert: Hintergrund-Monitor-Verbot (Retro-M1, S160) +
Testfall-Voraussetzungs-Pflicht (Retro-M2, S160) in `agent_scopes.md`. Backlog umsortiert
(B-109/B-105 direkt hinter B-028b). Stakeholder-Wunsch „Badge am Quantum-Deflection-
Rettungswurf" = exakt **B-105** (bereits als nächster Task nach B-109 eingeplant).

Frühere Sessions (S60–S159): Verlauf in `docs/metrics/session_archive.md` (Session-Historie).

### ▶ Nächster Schritt (S161)

Priorität = `docs/goals/backlog.md` (einzige Quelle).

1. **Retro-Maßnahmen-Kandidaten S160 entscheiden** (Stakeholder kündigte Entscheid zum
   Session-Start an — Planner berücksichtigt das Ergebnis direkt im Plan): [M1] neuer
   Handoff-Marker `AWAITING-VERIFICATION` für „wartet auf Stakeholder-Sichtprüfung"
   (+ Hygiene-Test nachziehen) — `NEEDS-DECISION` bleibt echten Entscheidungsfragen
   vorbehalten (Anlass: Stakeholder-Verwirrung S160, „was soll ich hier entscheiden?");
   [M2] Berechtigungsregel für Handoff-Lifecycle-Löschungen (Koordinator wurde 2× vom
   Berechtigungs-Classifier blockiert, Lifecycle „DONE = löschen" braucht den Umweg über
   Subagenten); [M3] Lösch-Belege in Doku-Briefs per `ls`, nicht `git status` (untracked
   Dateien hinterlassen nach `rm` keine Git-Spur — Fehlbericht „existierten nicht" in S160).
2. **B-109** (Brief: `S159_planning.md` Task 3) → **B-105** (Task 4; deckt den
   Quantum-Deflection-Badge-Wunsch).
3. **B-119 priorisieren** (neu am Listenende, ohne Prio).

**Offene Handoff-Marker:** `S159_planning.md` (bleibt Brief-Quelle für Task 3–4).

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
