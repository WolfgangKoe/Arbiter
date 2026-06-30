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

## Aktueller Stand (nach S113, 2026-06-30)

**S113** abgeschlossen — vier Tasks erledigt:
- **T1 — Extra-Direktiv-Permanenz GEKLÄRT**: Regelcheck + dokumentiert. Direktiven (Haupt+Extra) sind
  **jede Runde** neu wählbar, nicht einmal fix. App korrekt; nur Voice of the Triarch (Silent King)
  noch nicht verdrahtet (Folge-Task S114/T3).
- **T2b — `once_per_battle` battle-scope**: `used_stratagem_battle_ids` ersetzt phase-scoped
  `used_stratagem_ids`, überlebt Phasen-/Spielerwechsel. Vollständig getestet.
- **T2a — Fix B WAAAGH! generisch**: `active_text`-Feld wird aus YAML geladen + gerendert;
  Inhaltstest (S1+S2) ergänzt. ✅ ERLEDIGT (nicht wie Z.54 behauptet noch „offen").
- **B1/B2 — Undo + Label-Fix**: Stratagem-Undo nach Phasenwechsel möglich; Label zeigt jetzt
  korrekt `(used)` vs. `(CP insufficient)`.
Vollsuite: **1311 passed, 99.10 % Coverage**, Architektur 8/8. **DoD-Punkt 6 offen:**
manuelle UI-Prüfung der once_per_battle-Undo/Label-Pfade (Stratagem-Phase, Spielerwechsel).

Frühere Sessions (S60–S111): Verlauf in `docs/goals/ziel6.md` (Session-Historie).

### ▶ Nächster Schritt — Prioritäten (S113)

**1. GEKLÄRT — Extra-Direktiven-Permanenz (regelkonform, kein Fix nötig).**
   Stakeholder-Vermutung war, Direktive des permanent aktiven (Extra-)Protokolls würde EINMAL
   zu Spielbeginn fest gewählt. **Regelcheck (faction_overview.txt Z. 568/579) belegt:**
   „When a command protocol becomes active … select which directive … **at the start of each battle
   round**" — beide Direktiven (Haupt + Extra) sind **jede Runde** neu wählbar, NICHT einmal fix.
   App korrekt: `_reset_round_choice_state()` in `game_state.py` (~Z. 583) öffnet das Fenster
   pro Runde neu (docstring zitiert Z. 568/579). Einzige Ausnahme: **Voice of the Triarch**
   (Silent King, `unit_abilities.yaml:272–288`) schaltet das *aktive Protokoll* um — ändert aber
   nicht die pro-Runde-Direktiv-Wahl. Handler noch nicht verdrahtet → Folge-Task T3.

**2. Ziel6-Rückhalt:** (a) ✅ Fix B WAAAGH! generisch — `active_text` geladen+gerendert (S113, erledigt);
   (b) ✅ `once_per_battle`-Enforcement battle-scope (S113, erledigt).

**3. S114 = T3 Voice of the Triarch** — Silent-King-Handler `voiceOfTheTriarch` verdrahten;
   hängt an generischer Aktivator-UI (backlog §0; S113 Befund: `faction_abilities`-Aktivatoren
   ohne `once_per_battle: false` sind nirgends gemountet). Eigener kleiner Plan.

### ⚠️ Carry-over (offen)

- **S113 DoD-Punkt 6 offen:** Manuelle UI-Prüfung der `once_per_battle`-Undo/Label-Pfade:
  Stratagem-Undo nach Phasenwechsel testen; Label „(used)" nach Spielerwechsel prüfen.
  (s. `docs/handoff/review-S113.md` für Checkliste — Review-Subagent hat das gesichert)
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
