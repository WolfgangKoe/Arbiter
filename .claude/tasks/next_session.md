# Startprompt — Nächste Session
<!-- Kanonisch: .claude/tasks/next_session.md — nie ins Root-Verzeichnis anlegen. -->
<!-- Nur „Stand + nächster Schritt + offene Fragen". Historie → ziel6.md; Backlog → backlog.md. -->
<!-- Referenzwissen NICHT hier: Architektur-Muster → architecture.md, Regel-Gotchas →
     rules_insights.md, Constraints → CLAUDE.md. -->

## ⚠️ Session-Regeln
- **Start lesen:** `CLAUDE.md` (Freigabe-Pflicht, bei Unklarheit zuerst fragen)
  + `docs/goals/ziel6.md` (Aufgaben/Historie) + `docs/goals/backlog.md` (Backlog).
  Einstieg: `LEITSTAND.md`; Rollen/Tier/Events/Modi: `docs/governance/operating_model.md`.
- **Ende:** Checkboxen in `ziel6.md` + Historien-Zeile; **diese Datei** aktualisieren
  (ZUERST lesen, dann ergänzen — nie blind überschreiben).
- **Doku-Gate:** Decke **120** Zeilen (Test rot darüber). Beim Reißen **tief auf ≤ 70**
  kürzen, nicht knapp drunter — Erledigtes → `backlog.md`/`ziel6.md`, Referenz → s. o.
- **Freigabe vor Umsetzung; kein Memory/Subagent/Skill ohne Freigabe; rote vorher-grüne
  Tests = STOP + fragen.** Details: `CLAUDE.md`.

## Was ist Arbiter?
Digitaler Spielbegleiter für WH40k 9E, Streamlit (Python). Start:
`streamlit run src/app.py` (Port 8501). Branch `dev` (Arbeit), `main` (nur per PR).

---

## Aktueller Stand (nach S72, 2026-06-20)

**S72 — 4 Tasks via 3 parallele Sonnet-Subagenten (disjunkte Dateimengen), Opus reviewt.**
(1) **Setup-Bug (Nutzer-Fund, = Backlog #2b):** Protokoll-Direktiven + WAAAGH erschienen im
Setup und wurden per First-Player-Toggle wählbar → reiner Helfer `_ability_section_visible`
+ früher `return` in `armyCard._render_round_choice_ui`/`_render_once_per_battle_ability_ui`;
Test `test_ability_sections_hidden_in_setup_only`. (2) **INV-4b Quick-Wins:** Spielerlabels
(`gameHeader`/`gameProtocoll` → `Player 1/2`) + `setupScreen`-Caption generisch. (3) **Renames:**
`pending_irongob` → `pending_triggered_relic`, `res_orb_*` → `revive_wargear_*` (`irongob` ganz
raus). → **INV-4 Allowlist 10→5, INV-4b 20→19 Tokens.** (4) **Subagent-Peak-Archiv** (Retro S71):
`token_report.py` akkumuliert je Session den Subagent-Peak idempotent in
`docs/metrics/subagent_archive.json` → in `overview.md` „Subagent-Archiv (je Session)".
**1004 grün, Cov 92.40 %, Floor 90.** Setup-Fix vom Nutzer manuell verifiziert ✅.
⚠️ **#4 falsch verstanden** — Duplikat-Tabelle statt Pro-Session-Zusammenfassung (s. Refinement).

**S71 — Subagent-Checkliste verankert · Coverage-Floor 90 % · Katalog Deployment/Scoring.**
(1) **Selbstprüf-Checkliste für Subagenten** kanonisch im Operating Model (Event 3
„Sprint") verankert — „Subagent-grün ≠ verdrahtet"; Verdrahtung per `grep` belegen, Heimat,
Gates, Beleg zurückliefern; Querverweis in `CLAUDE.md` (Subagent-Muster). Dogfooded:
beide Subagenten lieferten grep-Belege + Ratchet-/LEGIT-Warnungen.
(2) **Coverage-Floor 88 → 90 %** (`pyproject.toml`); CLAUDE.md-Drift 80→90 gefixt;
Messbefehl-Zeile aktualisiert. (3) **Ziel-Fortschritt-Zeile** im Review-Event verankert
(`operating_model.md` Event 5). (4) **Regel-Katalog +2 Bereiche** via Sonnet-Subagent:
Deployment (R-DEPLOY-01..09) + Mission-Scoring (R-SCORE-01..13); die 3 implementiert-Fälle
(`adjust_vp`, `adjust_secondary_vp`, VP-Render) mit **5 neuen VP-Tests** als `getestet: ja`
→ keine neue Schuld. **995 grün, Cov 92.40 %, Floor 90.**

**INV-4b/INV-4 Ledger — Restschuld (Quick-Wins + `irongob`/`res_orb` erledigt S72):**
- **LEGIT (keine Schuld):** `rosz_importer._FACTION_MAP` (I/O-Normalisierung), `typing.Protocol`.
- **Schema-Urteil (Konsens nötig, NICHT Autopilot):** `dakka`/`klaw`/`tesla` (Prosa-Suche →
  typisierte YAML-Felder), `reanimationProtocols`-String/`reanimation`, `arkana`-Sektion,
  benannte Items `orb`/`overlord`/`phaeron`/`gloom`/`prism`/`dynasty`, Default-Roster-Hardcode
  (`game_state.py` → `list_available_rosters()`), `faction_dir`-Default `"necrons"` in `loader.py`.

Frühere Sessions (S60–S70): Verlauf in `docs/goals/ziel6.md` (Session-Historie).

### ▶ Nächste Session = Plan 019 (UI Target Consolidation)

Refinement-Session 2026-06-20 abgeschlossen. Mit Plan 019 beginnen.
**Reihenfolge:** 019 → 014 → 022 → 020 → 021 → 016 → 018 → 015 → 017.

**Neue Pläne angelegt (019–022):**
- **Plan 019** (MITTEL, VOR 014): UI Target Consolidation — `pending_target_request`-Mechanismus
  konsolidiert MWBD/Orb/Subgruppen-Auswahl; `render_unit_selectbox()` für Veil+Mortal-Target.
- **Plan 020** (MITTEL): Resurrections-Orb → generischer Activated-Wargear-Flow (Option B);
  State-Keys orb-id-gebunden (Bug: 2 Overlords = Konflikt); YAML `once_per_battle: true`.
- **Plan 021** (MITTEL): Arkana → `faction_abilities.yaml`, `loader.py` generisch.
- **Plan 022** (HOCH, aktiver Bug): Dice Display Rework — Arrow-Direction-Fix + Badge-Truncate +
  Edge-Cases + `color_hint`-Feld. **KOMPLETTE HTML-TEST-SUITE PFLICHT.**

**Refinement-Entscheidungen (2026-06-20):**
- **Plan 014 neu:** interaktive Echtzeit-Subgruppen-Auswahl VOR Apply (3 Zustände A/B/C), nicht Post-hoc.
  Mortal-Wound-Overflow via `mortal=True` bereits implementiert. Lethal Hits = eigener Plan.
- **Tests = HARTES Akzeptanzkriterium** (dauerhaft): Unit/AC/Architektur/Manuell je Plan.
  Render-Code (`dice_html`, `uiLayout`) braucht HTML-Output-Tests.
- **Arrow-Direction-Bug** in `dice_html.py:200`: `rightward = value < 0` FALSCH → `rightward = value > 0`.
  Spec: `docs/spec/dice_display.md` angelegt.
- **INV-4b:** Cluster 4 (`dynasty`) + 5 (`gloom/prism`) XS-Fix; Cluster 3 → Plan 020; Cluster 6 → Plan 021.
- **Neue Regel-Lücken:** Voice of the Triarch (YAML fertig, Handler fehlt → Plan 016);
  Lethal Hits + Deadly Demise (je eigener Plan).
- **Subagent-Archiv REWORK:** `session_archive.md` als separate wachsende Datei;
  Session-ID-Deduplizierung bei `--write`; SA-Peaks als Subzeilen im Verlaufsblock.

### Offene Frage / Retro-Vormerkung
- ✅ **Retro-Maßnahme (Nutzer S71): Subagent-Peak je Session archivieren — erledigt S72.**
  `token_report.py` merged idempotent in `docs/metrics/subagent_archive.json`; `overview.md`
  zeigt „Subagent-Archiv (je Session)" (neueste zuerst), Verlaufstabelle bleibt.
- **Output ↔ cache_read als Tempo-Indikator** (S68): Output gegen Qualität gewichten, nicht
  maximieren — Interpretation in der Retro gemeinsam geschärft; ggf. Zielwert-Feintuning in
  `token_report.py`-Legende nachziehen, falls sich ein konkreter Korridor ergibt.

---

## Gate-Netz (Messbefehle)
- Tests + Coverage: `pytest --tb=short` (Floor 90 %, `pyproject.toml`).
- **Schulden-Scoreboard** erscheint nach jedem `pytest` (`tests/conftest.py`): Vokabular-
  Tokens, Allowlist, AC-IDs, next_session-Zeilen, Regel-Katalog-%. Ziel: Zahlen sinken.
- Architektur (INV-1..4b): `pytest tests/architecture/ --no-cov -q` · Ledger:
  `architecture_invariants.md`. Doku/Akzeptanz (INV-5): `pytest tests/docs/ tests/acceptance/ --no-cov -q`.
- **Regel-Katalog** (Nenner): `docs/spec/acceptance/rules.md` — Klasse A/B/C,
  `getestet: ja — <testname>`. Parser: `tests/acceptance/_rules.py`.
- **Token-Korridor:** <150k, bei ~135k Session beenden; Fleißarbeit an Sonnet-Subagent.
  `tools/session_context.py` eskaliert ab 120k/135k automatisch (S66).
- **Token-Report:** `python tools/token_report.py --write` → `docs/metrics/overview.md`
  (läuft automatisch bei `pytest`; PostToolUse-Reminder zum Teilen, S66).
- **History-Rotation (Abschluss):** `python tools/rotate_history.py --session <N> --summary "…"`
  hängt den Stand-Einzeiler an `ziel6.md` an und setzt den Stand-Block hier zurück (S69).
- **Freigabe-Gate (S66, hart):** Edit/Write blockiert bis `touch .claude/.freigabe`;
  SessionStart re-armt. Vollzieht die Freigabe-Pflicht über die Harness (ADR-0003).
