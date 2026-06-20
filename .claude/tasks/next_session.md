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

### ▶ Nächste Session = REFINEMENT (Themen herunterbrechen, dann je eigener Plan + Freigabe)

**Neu vom Nutzer (S72):**
1. **Silent King — Command-Protocol-Switch:** Der Stille König hat eine Fähigkeit, die
   Command Protocols wechselt. Regeln **recherchieren** (`docs/work/wahapedia_necrons/`,
   Szarekh/Triarchen) — Vorgehen: erst lesen. Ergebnis: entweder **BUG/Anforderungslücke**
   anlegen (+ ggf. **Regel-Katalog-Ledger-Eintrag**) **oder** „regelkonform → nichts zu tun"
   dokumentieren. Kein Code ohne Regelbeleg.
2. **Subagent-Archiv REWORK (Missverständnis korrigieren!):** Die in S72 gebaute **Duplikat-
   Tabelle** in `overview.md` ist NICHT gewünscht. Soll: **je Session eine sinnvolle
   Zusammenfassung MIT den Pro-Session-Diagrammen** (Zusammensetzungs-Balken/Peak/Modell-Mix
   wie im Fokus-Block) **automatisiert** in eine **gesonderte Datei** (oder klar abgetrennt)
   archiviert — KEINE zweite Tabelle. Duplikat-Tabelle + ggf. `subagent_archive.json`-Format
   überarbeiten. **Bei Unklarheit ZUERST fragen** (Lehre S72).

**Herunterzubrechen (Backlog, Prio):** Plan 014 (Mockup-STOP), #2 Protokoll-Buff-Audit
(9/12 Direktiv-Effekte unverdrahtet), #3/#4 Würfelanzeige (Soll-Bild als AC), Schema-/
`arkana`-/Default-Roster-Konsens.

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
