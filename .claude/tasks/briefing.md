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

## Aktueller Stand (nach S166, 2026-07-18)

**Review S166: GO** (2018 passed, Coverage 99,14 %, Arch 8/8, Doku/Akzeptanz 25/25). Retro-
Maßnahmen 1–3 in `docs/handoff/S166_RETRO.md` zur Entscheidung im S167-Planning (Diagnose-
Ratchet „UI-Erreichbarkeit des Beweispfads", Grenzfall-Test-Auflage B-123-Brief, dritte
Maßnahme s. Retro-Datei). B-122 (Menhir-Lebenspunkte) erledigt: extern verifiziert (3
Wahapedia-9E-Quellen, Wounds 7→5 je Menhir), UI-Sichtprüfung positiv — nach
`docs/goals/backlog_archive.md` archiviert. B-123 (Schadens-Spillover): Root Cause verifiziert
— `_render_damage_block` erzwingt bei Mehrgruppen-Einheiten immer eine Subgruppen-Wahl,
`apply_damage` nimmt dadurch den directed-Zweig, der Schaden über den Restpool der gewählten
Gruppe hinaus verwirft (Repro: 26 Schaden auf vollen Silent King → nur Menhirs sterben, Szarekh
unberührt). Stakeholder-Richtung: kein pauschaler Spillover, bestehende Subgruppen-
Zuweisungslogik vereinheitlichen (auch für identische Modelle), Menhir-Lock für Erstschaden
prüfen — Details in `docs/goals/backlog_details.md` B-123. Explodes-Mockup (B-028c1): V1
abgelehnt, V2 (`docs/handoff/S166_MOCKUP_EXPLODES_V2.html`, reine Bestandskomponenten) vom
Stakeholder positiv bewertet, 7 Korrekturwünsche für V3 in `docs/handoff/S166_MOCKUP_EXPLODES.md`
§g.

Frühere Sessions (S60–S165): Verlauf in `docs/metrics/session_archive.md` (Session-Historie).

### ▶ Nächster Schritt (S167)

1. **Retro-Maßnahmen-Entscheid** (`docs/handoff/S166_RETRO.md`) — Stakeholder wählt/verwirft.
2. **Explodes-Mockup V3** mit den 7 Korrekturen aus `docs/handoff/S166_MOCKUP_EXPLODES.md` §g
   erstellen → Abnahme → dann B-028c1-Umsetzung planen (Schema, Komponente+Anker,
   Tisch-Wurf-Baustein, `auto_explode`-GO, Datennacherfassung).
3. **B-123-Umsetzung** nach Stakeholder-Richtung (inkl. Regel-Check Menhir-Lock +
   Boyz/Nob-Vergleich, Test-Auflage Grenzfall-Matrix directed×resolved×locked×mortal).
4. Weiteres laut `docs/goals/backlog.md`.

**Offene Handoff-Marker:** `Stakeholder_Beobachtungen.md` (STANDING); `S166_REVIEW.md`,
`S166_RETRO.md`, `S166_MOCKUP_EXPLODES.md` (+ `_V2.html` + 6 Screenshots, für V3 gebraucht)
NEEDS-DECISION — Stakeholder-Sichtung im S167-Planning.

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
