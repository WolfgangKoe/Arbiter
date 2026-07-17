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

## Aktueller Stand (nach S162, 2026-07-17)

**Review S162: GO** (Vollsuite 1992 passed, Coverage 99,13 %, Arch 8 grün, Docs+Acceptance
25 grün). Zwei parallele Sonnet-Executoren (disjunkte Dateien) + DONE-Hygiene + Opus-Review:

- **B-115 DONE (Kern der Session):** Invuln-Zweig von `_render_dice_save_block`
  (`src/uiLayout/diceHtml.py`) auf das WOUND-Block-Muster umgestellt — Titel-Zeile
  `Inv N+` + `go_source_chip` OBERHALB, Würfelreihe vollbreit/zentriert. BEIDE Label-Fälle
  sichtbestätigt („Sieht gut so aus"): Stratagem „Quantum Deflection" 4+ und Fähigkeit
  „WAAAGH! S1" 5+ (damit auch der aus S161 offene Fähigkeits-Label-Fall geschlossen).
  2 neue HTML-Struktur-Tests.
- **B-105 + B-109 DONE, B-043 überholt — alle drei archiviert;** die S161-Layout-Kritik
  war kein neues Item, sondern deckte sich wörtlich mit `design_system.md` §4.4 (→ B-115).
- **Drift-Korrektur:** B-119-Referenz ist real
  `src/gameMechanic/psychicPhase.py::_render_deny_column` (nicht `gameActionsArea.py`).
- **Retro S162:** M1' = mypy in S163 aktiv reduzieren; M2 = Vollsuite-Klausel für
  Parallel-Executoren in `agent_scopes.md` verankert (belastbare Vollsuite beim Koordinator
  auf dem kombinierten Endstand, Executor-Suiten nur Selbstprüfung); M3 = stale
  Planning-Handoffs gelöscht. M4 (Archiv-Kosmetik „1991→1992") bewusst NICHT beauftragt.

**⚠ Bekannte Schuld:** mypy-Gate rot (26 Fehler vs. Baseline 25) — pre-existing seit S161
(Stash-Probe, Review-S162 Befund 1), CI auf dev seit S161 rot; NICHT durch S162 verursacht.

Aus S160 offen geblieben: `gloom_prism`-Migration auf die B-028a-Infrastruktur (B-028b-Rest).

Frühere Sessions (S60–S161): Verlauf in `docs/metrics/session_archive.md` (Session-Historie).

### ▶ Nächster Schritt (S163)

Priorität = `docs/goals/backlog.md` (einzige Quelle).

1. **mypy-Drift zuerst (Retro-M1', Stakeholder-Entscheid S162):** Fehlerzahl aktiv
   reduzieren (Stand 26, Baseline 25) — nicht nur Baseline anheben.
2. **B-028b-Rest:** `gloom_prism`-Migration auf B-028a-Infrastruktur (~20k; Roster-Bestand
   verifiziert: `necrons_beta.yaml`, `necrons_test.yaml`).
3. **B-119:** Deny-Quellen-Anzeige, Fall b (Canoptek Spyder/Gloom Prism) — Referenz s. o.

**Offene Handoff-Marker:** nur `Stakeholder_Beobachtungen.md` (STANDING) — Ordner sauber.

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
