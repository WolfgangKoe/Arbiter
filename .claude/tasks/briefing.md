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

## Aktueller Stand (nach S164, 2026-07-18)

**Review S164: NO-GO → minimal-GO-Auflagen umgesetzt** (2015 passed, Coverage 99,14 %,
Arch 8 grün, mypy 0, black/ruff sauber). Vier Tasks, parallelisiert per Stakeholder-Anweisung:

- **T0 DONE — B-028b/B-119 archiviert** nach positiver UI-Verifikation (S163-Handoff gelöscht,
  Archiv-Gruppe „Aus der ID-indizierten Liste (migriert S164)" in `backlog_archive.md`).
- **T1 DONE — B-028c1 Kernlogik:** generischer `mortal_wounds`-Handler in `abilityEngine.py`
  (`resolve_mortal_wounds_effect`/`mortal_wounds_target`), `Effect` um
  `roll_threshold`/`roll_type` erweitert, Loader-Parsing, 11 Tests, R-COMBAT-38–40.
- **T2 REDUZIERT + UI DEFEKT:** Regelkonformitäts-Befund aus T1 → NEEDS-DECISION-Entscheid:
  nur `vengeance_of_the_enchained` verdrahtet (`_render_mortal_wounds_on_destroy_card` in
  `_common.py` + `fightPhase.py`; YAML-Datenbug unerfüllbare `conditions` behoben).
  Stakeholder-Verifikation 3× negativ — **Review-Befund 1 (GO-kritisch): Karte hat keinen
  verlässlichen Sichtbarkeits-Pfad** (Anker hängt an Selektion, zerstörte Einheiten sind über
  `unitCard.py:232` nicht selektierbar). Ehrlich re-scoped statt als verifiziert eingecheckt;
  bekannte Zusatz-Lücke: psychicPhase-Spalte nicht verdrahtet.
- **F1/F2-Entscheid (Mailbox):** `infused_madness` nur YAML-Datenkorrektur (echte Fähigkeit =
  aktivierter Buff mit Risiko-Roll; Verdrahtung = eigenes Mini-Feature ~15–20k);
  `arc_fields`/`wrath_of_the_seraptek` zurückgestellt bis externe Wortlaut-Verifikation
  (IA-Compendium, lokal nicht belegt, in keinem Roster).
- **Retro-Lehren (Entscheid offen, `S164_RETRO.md`):** Executor-Budget-Sprengung (T2 ~311k vs.
  ~20k — Live-Verifikations-Schleife + Session-Limit-Abbruch), Formatter-Pflichtschritt fehlte,
  isolierter Render-Test bewies Erreichbarkeit nicht.

Frühere Sessions (S60–S163): Verlauf in `docs/metrics/session_archive.md` (Session-Historie).

### ▶ Nächster Schritt (S165)

1. Retro-Maßnahmen-Entscheid `docs/handoff/S164_RETRO.md` sichten.
2. **Vengeance-Sichtbarkeits-Bug (Top-Priorität)** — Lead in
   `docs/goals/backlog_details.md` B-028c1 (Selektions-Anker/`unitCard.py:232`).
3. Weiteres laut `docs/goals/backlog.md`.

**Offene Handoff-Marker:** `Stakeholder_Beobachtungen.md` (STANDING) ·
`S164_B028c1_ui_verifikation.md` (AWAITING-VERIFICATION, Ergebnis negativ — s. Zeile 2) ·
`S164_RETRO.md` (NEEDS-DECISION).

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
