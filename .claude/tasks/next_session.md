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

## Aktueller Stand (nach S110, 2026-06-29)

**S110 — Wound-Verkettungs-Bug + Coverage-Sprint + Test-Isolations-Fix (Commit b25e1f7).**
- **Wound-Verkettungs-Bug ✅ GEFIXT:** `_render_dice_wound_block` (`dice_html.py`) hatte denselben
  `current = next_thresh`-Fehler wie S109-Hit-Fix. Jetzt base-verankert + ±1-Cap; Test
  `test_stacked_wound_debuffs_both_reference_base_threshold`.
- **Coverage 97,29 %** (war 93,02 %): scenarios 100 %, attack_math 99 %, unit_mutations 99 %, loader 98 %.
  Noch offen: `game_state.py` 92 %, `ability_engine.py` 94 % (siehe nächster Schritt).
- **Test-Isolations-Fix:** 2 neue conftest.py (gameObjects = Loader-Caches leeren; gameMechanic =
  st-Mock re-pointing via sys.modules) → behob 50 Subset-Run-Failures.
- Nebenpunkte: Planning-Template in `agent_scopes.md` +2 Spalten; Backlog #2b hochgestuft;
  rotate_history-Marker-Drift (▶) behoben.
- Vollsuite **1260 grün / 97,29 %**, Architektur **8/8**, ruff+black sauber.

**S109 — Plan 030 (Conquering-Tyrant-UI-Bugs) abgeschlossen + committet, voll delegiert.**
- **Bug 1 (D2 −1-Hit nicht sichtbar) ✅ VERIFIZIERT ok:** Kein Code-Defekt — `atk_uid` greift (synthetische
  `models`-Gruppe via `loader.py:1089`), `can_shoot` und −1-Erzeuger lesen denselben State.
  In der App geprüft: roter „Conquering (Fall Back) −1" erscheint korrekt.
- **Bug 2 (Zielwahl-Hang) ✅ GEFIXT:** Helfer `_single_eligible_group` (`_common.py`) verdrahtet.
- **Dense-Cover-Anzeige (Hit) ✅ GEFIXT:** base-verankert + ±1-Cap; Test `test_stacked_hit_debuffs_both_reference_base_threshold`.

**S107 — Plan 025 DONE (Necron-Protokolle 9E) + D2 Fall-Back-Schuss-Bugfix.** Retro M1–M4 verbindlich (Executor
„KEIN Commit"; Planner Step-Abgleich; M3 Custodes-Schuld Queue; M4 Metrik-Automatisierung). Detail → `session_archive.md`.

**S106 (Detail → `session_archive.md`):** Governance-Konsistenz + Artefakt-Verschlankung; Coverage-Gate 92 % überall.

### ▶ Nächster Schritt — Coverage-Reste + 016-Linie
Plan 025 ✅ DONE, Wound-Bug ✅ DONE → Reihenfolge jetzt **016 → 018 → 015 → 026 → 017** (`docs/audit/plans/README.md`).
016 behält nur RP-Block-Hint + Dynastiebonus-Anzeige (Group A/C nach 025 obsolet).

**1. Coverage-Reste → ~100 % (PRIO, zwei verbleibende Module):**
- **`game_state.py` 92 %** — ungedeckte Zeilen: 119, 129, 181-182, 204-205, 237-238, 256-264, 384, 394-399, 444, 477, 567-568.
- **`ability_engine.py` 94 %** — ungedeckte Zeilen: 71-72, 113, 151, 190, 211-216, 388, 392, 424, 427, 431.
  Tests ergänzen bis ~98–99 % je Modul. Executor-SA mit Write, Tier Sonnet.

**2. Plan 016 (C) — RP-Block-Hints + Dynastiebonus-Anzeige** (war für S110 vorgesehen, verschoben).

- **M1 — Overwatch-Anzeige:** statische Caption `chargephase.py:144` erst mit Overwatch korrekt → Plan-015-Scope.
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
  (c) S103 stationär+D1 grünes +1-Save-Badge IN den Würfeln. [(b) Bug 2 ✅ S109 · (d) D2 −1 ✅ S109]
- **Manuelle UI-Prüfung (DoD-6, S110 offen):** Wound-Block bei 2 gestapelten −1-Wound-Debuffs
  (base 4+) → beide Modifier müssen auf base 4+ verankert sein, Eff.-Zeile „5+" (nicht 6+).
  Im laufenden Streamlit visuell prüfen.
- **Retro-Maßnahme 1 (DRY, S110):** Hit- und Wound-Block teilen identische ±1-Cap-Logik →
  gemeinsamen Helper in `dice_html.py` extrahieren (Backlog-Eintrag vorhanden).
- **Retro-Maßnahme 2 (Test-Schuld, S110):** `gameMechanic/conftest.py` re-pointet st-Mocks global
  über sys.modules (reihenfolge-abhängiger Quick-Fix) → mittelfristig durch eine session-scoped
  Streamlit-Mock-Fixture ersetzen (Backlog-Eintrag vorhanden).

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
