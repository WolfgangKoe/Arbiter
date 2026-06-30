# Startprompt — Nächste Session
<!-- Kanonisch: .claude/tasks/next_session.md — nie ins Root-Verzeichnis anlegen. -->
<!-- Nur „Stand + nächster Schritt + offene Fragen". Historie → session_archive.md; Backlog → backlog.md. -->
<!-- Referenz NICHT hier: Architektur → architecture.md, Regel-Gotchas → rules_insights.md, Constraints → CLAUDE.md. -->

## ⚠️ Session-Regeln
- **Start „start next session" → Planner-Subagent beauftragen** (liest `CLAUDE.md` + `docs/goals/ziel6.md`
  + `docs/goals/backlog.md`, Scope aus `docs/reference/agent_scopes.md`); Entwurf als Datei, Koordinator
  legt vor, erst nach Freigabe los. Shortcut „Plan ist freigegeben" = direkt los. Einstieg `LEITSTAND.md`;
  Rollen/Tier/Modi: `docs/governance/operating_model.md`.
- **ADR-0007 (verbindlich seit S102):** Koordinator routet — liest keine Quelldateien/Vollergebnisse;
  Detail-Planung → Planner-Subagent; finales Review → Reviewer-Subagent. Asynchrone Stakeholder-
  Entscheidungen über Mailbox (`docs/handoff/`, NEEDS-DECISION → ANSWERED), nicht Chat.
  Details: `docs/governance/operating_model.md` [#events].
- **Ende:** Review (Reviewer-SA) → Retro → **Maßnahmen-Entscheid** (Stakeholder wählt) →
  Abschluss: **diese Datei** aktualisieren (ZUERST lesen, dann ergänzen) + ggf. ziel6-Checkboxen.
- **Doku-Gate:** Decke **120** Zeilen (Test rot darüber). Beim Reißen **tief auf ≤ 70** kürzen —
  Erledigtes → `backlog.md`/`session_archive.md`, Referenz → s. o.
- **Freigabe vor Umsetzung; kein Memory/Skill(datei-ändernd) ohne Freigabe; Subagenten =
  stehende Freigabe (proaktiv, ADR-0005); rote vorher-grüne Tests = STOP + fragen.** → `CLAUDE.md`.

## Was ist Arbiter?
Digitaler Spielbegleiter WH40k 9E, Streamlit (Python). Start: `streamlit run src/app.py`
(Port 8501; **venv:** `source .venv/bin/activate`). Branch `feature/016` (Arbeit), `main` (nur PR).
**App permanent laufen lassen:** bei Session-Start nur kurz prüfen (`curl -s -o /dev/null -w "%{http_code}" http://localhost:8501` → 200), nur bei Bedarf neu starten — nicht den Nutzer fragen.

---

## Aktueller Stand (nach S112, 2026-06-30)

**S112** lief glatt: **Plan 031** (Protokoll-Direktiven-Timing) ist gefixt und committet (533e313) —
Wahl von `is_active` entkoppelt (beide Spieler wählen am Rundenanfang), „Change extra directive"-
Button raus, Haupt- und Extra-Direktive über `_directive_window_open()` UNABHÄNGIG gegated,
Runde-1-Fenster geschlossen. Stakeholder hat den Doppel-Direktiven-Fix am App verifiziert.
Danach **Ziel6 konsolidiert + Ziel7 ausgelagert + Renumbering** committet (efe12e1): neues
**Ziel7 = Gefechtsoptionen + subfaction-Mechanik**, Crusade→ziel8, Faction Fetcher→ziel9; Doku-Drift
92→99 %. Vollsuite 1303 / 99,09 %, Architektur 8/8, Docs-Tests 8/8 grün. **Offen für S113:** der
neue Befund zur Extra-Direktiven-Permanenz (s. Priorität 1) und die manuelle UI-Re-Verifikation läuft.

Frühere Sessions (S60–S111): Verlauf in `docs/goals/ziel6.md` (Session-Historie).

### ▶ Nächster Schritt — Prioritäten (S113)

**1. NEUER BEFUND (P-hoch, regel-prüfen DANN fixen) — Permanenz der Extra-Direktive.**
   Stakeholder-Vermutung: Direktive des permanent aktiven (Extra-)Protokolls wird EINMAL zu
   Spielbeginn gewählt und bleibt den Rest des Spiels FIX (nur eine Silent-King-Fähigkeit
   könnte das beeinflussen). Aktuelles Verhalten: `_reset_round_choice_state()` öffnet das
   Extra-Fenster JEDE Runde neu → Extra-Direktive ist aktuell pro Runde neu wählbar.
   **Regel-Spannung:** `faction_overview.txt` Z. 579 sagt wörtlich „select which directive …
   **at the start of each battle round**" — das stützt eher „jede Runde wählbar", NICHT „einmal fix".
   → ZUERST Regel sauber klären (Z. 568/579 + Silent-King/Szarekh-Fähigkeit in
   `wahapedia_necrons/` suchen), DANN entscheiden ob Fix nötig. Nicht raten.

**2. Ziel6-Reste (klein, NICHT YAML-blockiert):** (a) Fix B WAAAGH! generisch — `active_text`-
   Feld im YAML fehlt noch; (b) `once_per_battle`-Enforcement battle-scope statt phase-scope
   (`stratagem.py:59`, `used_stratagem_ids` ist phase-scoped). Beide bewusst Ziel6-Rest (Stakeholder-Entscheid S112).

**3. Ziel7 ausdetaillieren:** wenn aktiv — `ziel7.md` ist aktuell nur Scope-Stub.

### ⚠️ Carry-over (offen)

- **ADR-0007-Reste:** (c) `docs/handoff/context-audit-S91.md` verarbeiten + löschen; (e) SessionStart-Regel-Injektion.
- **Manuelle UI-Verifikation (PFLICHT):** (a) Mirror-Protokoll Necron-vs-Necron Befehlsphase;
  (c) stationär+D1 grünes +1-Save-Badge in den Würfeln.
- **Retro-Maßnahmen (S110):** (1) DRY-Helper Hit/Wound ±1-Cap in `dice_html.py`; (2) st-Mock-Fixture.
- **Plan-029-Datei fehlt** (in README.md als Divergenz markiert) — vor Beauftragung anlegen oder REJECTED.
- **`docs/handoff/planning-S112.md`** ist verarbeitet (committet) — kann bei Bedarf archiviert werden.
- **Ledger (impl. ohne Test):** R-COMBAT-17, R-PROTO-02 — bei Gelegenheit Tests nachziehen.

---

## Gate-Netz (Messbefehle)
- Tests + Coverage: `pytest --tb=short` (Floor **99 %**, `pyproject.toml`); **Schulden-Scoreboard** danach.
- Architektur: `pytest tests/architecture/ --no-cov -q`. Doku/Akzeptanz: `pytest tests/docs/ tests/acceptance/ --no-cov -q`.
- **Token-Korridor** <150k, bei ~135k beenden; Fleißarbeit PROAKTIV an Sonnet-Subagent.
- **Token-Report + History (M4, PFLICHT beim Abschluss):** `python tools/token_report.py --write` + `python tools/rotate_history.py --session <N> --summary "…"` — Koordinator stößt an.
- **Freigabe-Gate:** Edit/Write blockiert bis `touch .claude/.freigabe`; SessionStart re-armt.
