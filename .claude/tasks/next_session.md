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

## Aktueller Stand (nach S108, 2026-06-27)

**S108 — Plan 030 (Conquering-Tyrant-UI-Bugs), voll delegiert; am Wochenlimit gestoppt — NICHT committet.**
- **Bug 1 ✅ gefixt + UI-verifiziert:** `atk_uid` in beide Entry-Dicts (`_common.py:render_group_assignment`)
  → D2 −1-Hit-Debuff erscheint rot. Schließt Carry-over (d). Test `test_fall_back_hit_mod_wiring_requires_atk_uid_in_entry`.
- **Bug 2 ✗ NICHT gefixt (= Carry-over (b) „Bug 5"):** Selection-State-Hang bei Zielwahl besteht WEITER,
  trotz `reset_group_declaration_state()` an „Reset Declaration" + „All done" (`_common.py:render_attack_resolution`).
  ⚠️ Root-Cause war fehldiagnostiziert; Test `test_all_done_clears_group_autosel_guard` prüft nur den Reset-Helper
  isoliert (Tautologie) → fing den echten Hang NICHT. Nächste Session: echten Blockier-State im UI-Pfad finden
  (Enemy-Target bleibt disabled, bis die Eigen-Einheit ab-/angewählt wird). Code+Test bleiben vorerst (kein Schaden), neu untersuchen.
- **Neuer Befund — Multi-Debuff-Anzeige (P3, niedrig):** Bei gestapelten Hit-Debuffs (Conquering Tyrant −1
  + Dense Cover −1) wählt für die DARSTELLUNG der zweite Debuff (Dense Cover) die effektive Erfolgsgrenze.
  Der ±1-Cap rechnet korrekt (Eff. 4+, nicht 5+) — reines Anzeige-/Attributionsproblem im Hit-Modifier-Renderpfad
  (`_render_resolution_tab` / `dice_compose.py`). Nur gesammelt, keine Umsetzung.
- **Plan 030** geschrieben (`docs/audit/plans/030-conquering-tyrant-ui-bugfixes.md`) + Queue (README.md);
  Status anpassen: Bug 1 done, Bug 2 RE-OPEN. Working-Tree offen: `_common.py` (4 Z.) + 2 Test-Dateien, Vollsuite 1177 grün/93,02 %.

**S107 — Plan 025 abgeschlossen (Necron-Protokolle 9E-konform), voll delegiert.**
- **Plan 025 ✅ DONE** (alle Steps 1–6). Step 4 (Eternal Guardian D1) war schon S104 committet;
  Step 5 (Conquering Tyrant: D1 +3" Aura = Klasse B, D2 `shoot_after_fall_back` −1 Hit = Klasse A);
  Step 6 (Aufräumen verwaiste Effekt-Typen). Vollsuite 1171 grün, 93,02 %, Architektur-Gate grün.
- **Bugfix (UI-Verifikation):** Conquering Tyrant D2 funktionierte nie in der App — Engine-Fn prüfte
  `movement_choice == "fall_back"`, die App setzt aber `"retreated"`; zusätzlich blockte `can_shoot` ohne D2-Ausnahme.
  Fix committet (ffcdfe2): `ability_engine.py` auf `"retreated"` angeglichen, `can_shoot` mit generischer D2-Ausnahme
  (über Effekt-Typ `shoot_after_fall_back`). Vollsuite 1175 grün, 93,02 %.
- **Test-Validitäts-Befund (fürs Retro):** Step-5-Tests setzten `movement_choice: "fall_back"` direkt — ein App-fremder Zustand →
  der Bug rutschte durch Review+Tests. Lehre: Tests müssen den von der App tatsächlich gesetzten State verwenden.
- **Retro-Maßnahmen (verbindlich):** M1 Executor-Brief „KEIN Commit" (agent_scopes); M2 Planner gleicht
  offene/erledigte Steps gegen `git log` + diese Datei ab; M3 Custodes-`strength_if_charged`-Schuld als Queue-Eintrag;
  M4 Metrik-Automatisierung beim Abschluss (`token_report.py --write` + `rotate_history.py` — Koordinator stößt an).
- **Governance-Befund:** Haiku-Executor committete Step 5+6 eigenmächtig (633b00f) → soft-reset, Review
  nachgezogen, sauber neu committet. M1 verhindert Wiederholung.

**S106 (Detail → `session_archive.md`):** Governance-Konsistenz + Artefakt-Verschlankung; Coverage-Gate 92 % überall.

**Abschluss-Artefakte S107 fertig:** Executor-Brief M1+M2 (agent_scopes.md Pflichtschritte), M3 Queue-Eintrag (README.md Zeile 35), next_session.md aktualisiert.

### Nächster Schritt — 016-Linie
Plan 025 ✅ DONE → Reihenfolge jetzt **016 → 018 → 015 → 026 → 017** (`docs/audit/plans/README.md`). Executor-SA mit **Write**.
016 behält nur RP-Block-Hint + Dynastiebonus-Anzeige (Group A/C nach 025 obsolet).
- **M1 — Overwatch-Anzeige:** statische Caption `chargephase.py:144` erst mit Overwatch korrekt → Plan-015-Scope.
- **rotate_history.py Marker-Drift (Erstaufgabe):** Tool erwartet Marker `### ▶ Nächster Schritt`, diese Datei nutzt
  `### Nächster Schritt — 016-Linie`. Entweder Tool an aktuelles Format anpassen ODER Marker angleichen —
  entscheiden + fixen, damit die M4-Automatisierung beim Abschluss durchläuft.
- **Planning-Template-Erweiterung (offen, unbestätigt):** Stakeholder wünscht im Planner-Ausgabe-Template (`docs/reference/agent_scopes.md` Z. 33 ff.)
  zwei zusätzliche Spalten — „Subagent(en) + Tier" (Tier-Default nach O2/operating_model, ggf. Executor→Reviewer-Paar)
  und „Scope-Zeile / Dateien" (konkrete Pflicht-Lesen-Dateien aus der Scope-Tabelle). Vorschlag lag vor, Freigabe steht noch aus.

**Maßnahmen aus S107-Retro:**
1. ✅ M1 — Executor-Brief-Regel „KEIN Commit" (agent_scopes.md Zeilen 91–93) bereits vorhanden.
2. ✅ M2 — Planner-Pflichtschritt Step-Abgleich (agent_scopes.md Zeilen 50–52) bereits vorhanden.
3. ✅ M3 — Custodes `strength_if_charged`-Plan 029 (README.md Zeile 35) bereits in Queue.

### ⚠️ Carry-over (offen)
- **ADR-0007-Reste:** (c) `docs/handoff/context-audit-S91.md` verarbeiten + löschen;
  (e) SessionStart-Regel-Injektion (S95-Beleg). [(f) M3 ✅ · (g) M4 ✅ — S106]
- **Bug 3 (Zweitspieler-Direktiv-Wahl) + INV-4b-Restschuld nebenher.**
- **Manuelle UI-Verifikation (PFLICHT):** (a) Mirror-Protokoll Necron-vs-Necron Befehlsphase;
  (b) **Bug 5 / Bug 2 = OFFEN** — Zielwahl-Hang besteht trotz S108-Fixversuch (s. Stand oben), echten Blockier-State finden;
  (c) S103 stationär+D1 grünes +1-Save-Badge IN den Würfeln; (d) **025 Step 5 ✅ verifiziert S108** (D2 −1 rot).

### Offene Fragen / Vormerke
- **Design-System-Crew:** Buff-/Direktiv-Hinweis-Komponente, sobald 025 Effekte festlegt.
- **S95-Vormerk:** Regelkonformität beim YAML-Modellieren prüfen (DoD-#1-Ergänzung).
- **doku.md** nach `archive/` verschoben (war erledigtes Audit) — bei Bedarf ganz löschbar.

---

## Gate-Netz (Messbefehle)
- Tests + Coverage: `pytest --tb=short` (Floor **92 %**, `pyproject.toml`); **Schulden-Scoreboard** danach.
- Architektur: `pytest tests/architecture/ --no-cov -q`. Doku/Akzeptanz: `pytest tests/docs/ tests/acceptance/ --no-cov -q`.
- **Token-Korridor** <150k, bei ~135k beenden; Fleißarbeit PROAKTIV an Sonnet-Subagent.
- **Token-Report + History (M4, PFLICHT beim Abschluss):** `python tools/token_report.py --write` + `python tools/rotate_history.py --session <N> --summary "…"` — Koordinator stößt an.
- **Freigabe-Gate:** Edit/Write blockiert bis `touch .claude/.freigabe`; SessionStart re-armt.
